"""Behavioral regressions for the new Excel-driven compiler."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from compiler import pipeline
from compiler.engines import export_mihomo, match_dns, mihomo_rule, rejection_rules, validate_dns
from compiler.network import Cache, check_body, count_guard, json_text
from compiler.rules import active_lines, dns_line, merge, parse
from tools.import_excel import extract


class ScopeTests(unittest.TestCase):
    def test_exact_and_subdomain_scopes(self):
        rules = parse('0.0.0.0 ads.example.com\n||track.example.com^\n', 'dns').rules
        self.assertEqual(match_dns([{'rules': rules, 'hosts': ['example.com', 'ads.example.com',
                        'x.ads.example.com', 'track.example.com', 'x.track.example.com']}]),
                         [[False, True, False, True, True]])

    def test_dedup_each_output_independently(self):
        first = merge([['||ads.example.com^'], ['||ads.example.com^', '||other.example.com^']])
        second = merge([['||ads.example.com^']])
        self.assertEqual(len(first), 2)
        self.assertEqual(second, ['||ads.example.com^'])

    def test_no_coverage_pruning(self):
        expected = ['|ads.example.com|', '||ads.example.com^', '||example.com^']
        self.assertEqual(merge([expected]), sorted(expected))

    def test_paths_never_become_domain_rules(self):
        parsed = parse('||video.example.com/v1/resource^$important\n||ads.example.com^', 'mixed')
        self.assertEqual(parsed.rules, ['||ads.example.com^'])
        self.assertEqual(parsed.skipped, {'url-path': 1})

    def test_unsupported_exception_quarantines_source(self):
        parsed = parse('||example.com^\n@@||example.com/player.js$script', 'mixed')
        with self.assertRaisesRegex(ValueError, 'unsupported exception'):
            parsed.require_dns_safe()
        self.assertEqual(parsed.rules, ['||example.com^'])

    def test_badfilter_not_lost(self):
        parsed = parse('||example.com^\n||example.com^$badfilter', 'mixed')
        with self.assertRaises(ValueError):
            parsed.require_dns_safe()

    def test_browser_cosmetic_survives_browser_merge(self):
        body = '! heading\n##.ad-banner\nexample.com##.popup\n@@||example.com/x.js$script\n'
        self.assertIn('##.ad-banner', active_lines(body))
        parsed = parse(body, 'browser')
        self.assertEqual(parsed.rules, [])
        self.assertEqual(parsed.unsafe_exceptions, 1)

    def test_dns_format_drift_fails(self):
        with self.assertRaisesRegex(ValueError, 'changed format'):
            parse('||example.com^$script', 'dns')

    def test_important_exception_priority(self):
        cases = [
            {'rules': ['||example.com^', '@@||safe.example.com^'], 'hosts': ['safe.example.com', 'example.com']},
            {'rules': ['||example.com^$important', '@@||safe.example.com^'], 'hosts': ['safe.example.com']},
            {'rules': ['||example.com^$important', '@@||safe.example.com^$important'], 'hosts': ['safe.example.com']},
        ]
        self.assertEqual(match_dns(cases), [[False, True], [True], [False]])

    def test_masks_keep_native_match_boundaries(self):
        hosts = ['ads.example.com', 'ADS.example.com', 'x.ads.example.com', 'badads.example.com',
                 'ads.example.com.evil', 'x.pcdn.biliapi.net', 'pcdn123.biliapi.net', 'biliapi.net',
                 'abc-ad.sm.cn', 'a.abc-ad.sm.cn', 'sm.cn', 'x-ad.sm.cn.evil']
        for line in ['||ads*.example.com^', '||*.ads.example.com^', '||*pcdn*.biliapi.net^$important', '*-ad.sm.cn*']:
            with self.subTest(line=line):
                _, kind, payload = mihomo_rule(line)
                self.assertEqual(kind, 'classical')
                pattern = re.compile(payload.removeprefix('DOMAIN-REGEX,'))
                self.assertEqual([bool(pattern.search(h)) for h in hosts], match_dns([{'rules': [line], 'hosts': hosts}])[0])

    def test_invalid_go_regex_rejected(self):
        with self.assertRaises(ValueError):
            validate_dns(['/[/'])


class DownloadTests(unittest.TestCase):
    def test_html_and_truncated_declared_list(self):
        for body in [b'<html>Error</html>', b'! Entries: 2\n||one.example^\n', b'']:
            with self.assertRaises(ValueError):
                check_body(body)

    def test_count_and_exception_guard(self):
        for count, allow in [(60, 3), (2000, 3), (100, 0)]:
            with self.assertRaises(ValueError):
                count_guard({'active': 100, 'allow': 3}, count, allow)
        count_guard({'active': 100, 'allow': 3}, 100, 3)
        with self.assertRaises(ValueError):
            count_guard({'active': 11, 'allow': 0}, 5, 0)

    def test_cache_integrity_and_expiry(self):
        with tempfile.TemporaryDirectory() as temp:
            cache = Cache(Path(temp))
            source = {'url': 'https://example.com/rules.txt'}
            cache.store(source, '||ads.example^\n', 1, 0, 'https')
            body, meta = cache.load(source)
            self.assertEqual(body, '||ads.example^\n')
            path, info = cache.paths(source)
            meta['fetched_at'] = (datetime.now(timezone.utc) - timedelta(hours=73)).isoformat()
            info.write_text(json_text(meta), encoding='utf8')
            with self.assertRaisesRegex(ValueError, 'expired'):
                cache.load(source)
            path.write_text('||tampered.example^\n', encoding='utf8')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                cache.load(source, enforce_age=False)

    def test_failed_fresh_source_uses_unexpired_validated_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            source = {'id': 'one', 'url': 'https://example.com/rules.txt', 'mode': 'dns', 'name': 'one',
                      'repository': 'https://example.com', 'author': 'author', 'license': 'unspecified'}
            cache = Cache(Path(temp))
            before = cache.store(source, '||ads.example^\n', 1, 0, 'https')['fetched_at']
            with patch('compiler.pipeline.retry_download', side_effect=ValueError('HTML response')):
                result = pipeline.source_result(source, cache, False, False)
            self.assertEqual(result['record']['state'], 'cache-fallback')
            self.assertEqual(result['record']['fetched_at'], before)
            self.assertEqual(result['dns'], ['||ads.example^'])


class WorkbookTests(unittest.TestCase):
    def test_exact_workbook_urls_and_blank_rows(self):
        root = Path(__file__).resolve().parents[1]
        extracted = extract(root / 'sources.xlsx')
        catalog = pipeline.load_catalog(root / 'sources.json')
        self.assertEqual(len(extracted['sources']), 11)
        self.assertEqual(len(extracted['blank_rows']), 4)
        self.assertEqual([s['url'] for s in extracted['sources']], [s['url'] for s in catalog['sources']])
        self.assertTrue(extracted['sources'][1]['url'].startswith('https://'))
        self.assertEqual(extracted['sources'][4]['repository'], 'https://github.com/TG-Twilight/AWAvenue-Ads-Rule')


class PublicationTests(unittest.TestCase):
    def test_retire_only_owned_files_preserve_health(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); stage = root / 'stage'; dist = root / 'dist'
            stage.mkdir(); dist.mkdir()
            (stage / 'new.txt').write_text('new', encoding='utf8')
            (dist / 'old.txt').write_text('old', encoding='utf8')
            health = dist / 'health_keep'; health.mkdir(); (health / 'user.json').write_text('user')
            (dist / 'manifest.json').write_text(json_text({'schema': 2, 'files': {'old.txt': 'old'}}), encoding='utf8')
            manifest = {'schema': 2, 'files': pipeline.generated_files(stage)}
            pipeline.publish(stage, dist, manifest)
            self.assertFalse((dist / 'old.txt').exists())
            self.assertEqual((dist / 'new.txt').read_text(), 'new')
            self.assertEqual((health / 'user.json').read_text(), 'user')

    def test_checksum_failure_rolls_back_written_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); stage = root / 'stage'; dist = root / 'dist'
            stage.mkdir(); dist.mkdir()
            for name in ('a.txt', 'b.txt'):
                (stage / name).write_text('new', encoding='utf8')
                (dist / name).write_text('old', encoding='utf8')
            files = pipeline.generated_files(stage); files['b.txt'] = 'bad'
            with self.assertRaisesRegex(ValueError, 'checksum'):
                pipeline.publish(stage, dist, {'schema': 2, 'files': files})
            self.assertEqual((dist / 'a.txt').read_text(), 'old')
            self.assertEqual((dist / 'b.txt').read_text(), 'old')

    def test_manifest_paths_cannot_escape_or_erase_user_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            for path in ('../outside', '/absolute', 'health_keep/user.json'):
                with self.assertRaises(ValueError):
                    pipeline.safe_target(Path(temp), path)

    def test_failed_publication_retains_previous_published_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'dist').mkdir()
            (root / 'dist/ads.txt').write_text('previous rules', encoding='utf8')
            previous = {'schema': 2, 'built_at': '2026-10-01T00:00:00+00:00', 'profiles': [], 'sources': []}
            (root / 'dist/manifest.json').write_text(json_text(previous), encoding='utf8')
            catalog = {'schema': 2, 'repository': 'owner/repo', 'sources': [], 'profiles': [], 'browser_profiles': []}
            with patch('compiler.pipeline.load_catalog', return_value=catalog), patch('compiler.pipeline.publish', side_effect=ValueError('publication failed')):
                result = pipeline.run(root)
            self.assertEqual(result['status'], 'failed')
            self.assertEqual((root / 'dist/ads.txt').read_text(), 'previous rules')
            self.assertEqual(json.loads((root / 'dist/manifest.json').read_text()), previous)

    def test_failed_source_cannot_publish_partial_subscription(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'dist').mkdir()
            (root / 'dist/ads.txt').write_text('previous rules', encoding='utf8')
            previous = {'schema': 2, 'built_at': '2026-10-01T00:00:00+00:00', 'profiles': [], 'sources': []}
            (root / 'dist/manifest.json').write_text(json_text(previous), encoding='utf8')
            source = {'id': 'missing', 'author': 'author', 'repository': 'https://example.com',
                      'name': 'missing', 'url': 'https://example.com/rules.txt', 'category': 'test'}
            catalog = {'schema': 2, 'repository': 'owner/repo', 'sources': [source],
                       'profiles': [], 'browser_profiles': []}
            with patch('compiler.pipeline.load_catalog', return_value=catalog), patch('compiler.pipeline.source_result', side_effect=ValueError('download failed')), patch('compiler.pipeline.publish') as publisher:
                result = pipeline.run(root)
            publisher.assert_not_called()
            self.assertEqual(result['errors'], {'missing': 'download failed'})
            self.assertEqual((root / 'dist/ads.txt').read_text(), 'previous rules')


class MihomoTests(unittest.TestCase):
    def test_real_kernel_loads_all_buckets_including_empty(self):
        rules = ['|exact.example.com|', '||suffix.example.com^', '@@||safe.example.com^',
                 '||pcdn*.example.com^$important', '@@||safe.pcdn.example.com^$important']
        with tempfile.TemporaryDirectory() as temp:
            result = export_mihomo(Path(temp), 'test', rules, 'owner/repo')
            self.assertEqual(len(result['files']), 11)
            config = json.loads((Path(temp) / 'test.yaml').read_text(encoding='utf8'))
            self.assertEqual(len(config['rule-providers']), 8)
            self.assertEqual(config['rules'], rejection_rules('test'))
            self.assertNotIn('DIRECT', '\n'.join(config['rules']))


if __name__ == '__main__':
    unittest.main()
