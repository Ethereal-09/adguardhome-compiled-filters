from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

import build_filters as app


class BuilderTests(unittest.TestCase):
    def test_personal_exceptions_apply_only_to_selected_profiles(self):
        with tempfile.TemporaryDirectory() as folder:
            config, _, args = self.setup_project(Path(folder))
            config['profiles'][0]['includeCustom'] = True
            args[0].write_text(json.dumps(config), encoding='utf-8')
            (args[3] / 'allow.txt').write_text('@@||safe.example^\n', encoding='utf-8')
            with patch.object(app, 'fetch', return_value=self.rule_body('base')):
                app.build(*args)
            self.assertIn('@@||safe.example^$important', (args[2] / 'alpha.txt').read_text())
            self.assertNotIn('safe.example', (args[2] / 'beta.txt').read_text())

    def test_growth_and_lost_exceptions_are_guarded_but_small_lists_can_change(self):
        checks = dict(maxGrowthFraction=1, growthMinIncrease=1000,
                      maxExceptionDropFraction=.3, exceptionMinBaseline=20)
        with self.assertRaisesRegex(ValueError, 'increased'):
            app.check_changes(dict(accepted=3001, exceptionRules=30), dict(accepted=1000, exceptionRules=30), checks, 'source')
        with self.assertRaisesRegex(ValueError, 'Exception'):
            app.check_changes(dict(totalRules=1000, exceptionRules=20), dict(totalRules=1000, exceptionRules=30), checks, 'profile')
        app.check_changes(dict(accepted=25, exceptionRules=0), dict(accepted=9, exceptionRules=1), checks, 'small')

    def setup_project(self, root):
        custom = root / 'custom'
        custom.mkdir()
        for name in ('block.txt', 'allow.txt'):
            (custom / name).write_text('! no personal rules\n', encoding='utf-8')
        sources = [dict(id=sid, name=sid, repository='https://github.com/test/rules',
            repositoryAccount='test', url=f'https://raw.githubusercontent.com/test/rules/main/{sid}.txt',
            role='filter', status='checked', eligibleForSubscription=True, dnsBlocks=3, dnsExceptions=0,
            strength={'value': 'unknown'}, variantFamily=None, representationGroup=None) for sid in ('a', 'b')]
        config = dict(schemaVersion=1, defaultProfile='alpha', maxDropFraction=.3,
            download=dict(timeoutSeconds=1, retries=1, workers=2, cacheMaxAgeHours=72),
            profiles=[dict(id=pid, name=pid, kind='blocklist', axis='type', value='ads', enabled=True,
                           sourceIds=ids) for pid, ids in [('alpha', ['a']), ('beta', ['b']), ('both', ['a', 'b'])]])
        config_path, registry = root / 'profiles.json', root / 'registry.json'
        config_path.write_text(json.dumps(config), encoding='utf-8')
        registry.write_text(json.dumps(dict(sources=sources)), encoding='utf-8')
        return config, sources, (config_path, registry, root / 'dist', custom, root / '.cache')

    def rule_body(self, prefix, count=5):
        return '\n'.join(f'||{prefix}{i}.example.com^' for i in range(count))

    def test_optimizer_preserves_scope_actions_and_priority(self):
        original = {'||parent.example^', '||child.parent.example^', '|child.parent.example|',
                    '@@||safe.parent.example^', '@@|safe.parent.example|',
                    '||child.parent.example^$important', '|other.example|',
                    '@@||deep.safe.parent.example^$important', '/regex.*/', '||*.wild.example^'}
        kept, removed = app.optimize_rules(original)
        self.assertEqual(removed, 3)
        self.assertIn('||child.parent.example^$important', kept)
        self.assertIn('@@||safe.parent.example^', kept)
        self.assertIn('|other.example|', kept)
        self.assertIn('/regex.*/', kept)
        self.assertIn('||*.wild.example^', kept)

    def test_optimization_preserves_effective_decisions_across_rule_combinations(self):
        names = ['parent.example', 'a.parent.example', 'b.parent.example', 'deep.a.parent.example']
        pool = [prefix + anchor + name + end + modifier for name in names
                for prefix in ('', '@@') for anchor, end in (('||', '^'), ('|', '|'))
                for modifier in ('', '$important')]

        def decision(rules, name):
            matches = []
            for rule in rules:
                allow, important, scope, host = app.simple_rule(rule)
                if name == host or (scope == 'suffix' and name.endswith('.' + host)):
                    matches.append((important, allow))
            return not max(matches)[1] if matches else False

        rng = random.Random(17)
        for _ in range(100):
            rules = set(rng.sample(pool, rng.randint(1, len(pool))))
            optimized, _ = app.optimize_rules(rules)
            for name in names + ['x.' + n for n in names] + ['unrelated.example']:
                self.assertEqual(decision(rules, name), decision(optimized, name), (rules, name))

    def test_masks_regex_hosts_and_unsupported_exceptions(self):
        rules, stats = app.parse_source('0.0.0.0 exact.example\n||parent.example^\n'
            '@@||*cdn.example^$important\n/^ad[0-9]+\\.example$/\n||parent.example^\n'
            '||browser.example^$third-party', 'filter')
        self.assertIn('|exact.example|', rules)
        self.assertIn('@@||*cdn.example^$important', rules)
        self.assertIn('/^ad[0-9]+\\.example$/', rules)
        self.assertEqual(stats['duplicates'], 1)
        self.assertEqual(stats['unsupported'], 1)
        with self.assertRaisesRegex(ValueError, 'Unsupported exception'):
            app.parse_source('||ads.example^\n@@||safe.example^$client=phone', 'filter')
        with self.assertRaisesRegex(ValueError, 'badfilter'):
            app.parse_source('||ads.example^\n||ads.example^$badfilter', 'filter')
        with self.assertRaisesRegex(ValueError, 'non-exception'):
            app.parse_source('plain.example', 'independent_allowlist')
        allows, _ = app.parse_source('@@||*-go.example^\n@@||safe.example^', 'independent_allowlist')
        self.assertTrue(all(rule.startswith('@@') for rule in allows))

    def test_official_website_requires_exact_reviewed_subscription_and_same_origin(self):
        source = dict(id='official', repository='https://lists.example/hosts/',
                      url='https://lists.example/hosts/hosts')
        with self.assertRaisesRegex(ValueError, 'Unverified official'):
            app.validate_source_origin(source)
        source['provenance'] = dict(kind='official_website', status='verified',
            subscriptionUrl=source['url'], evidenceUrl='https://lists.example/hosts/',
            checkedUtc='2026-10-01T00:00:00Z')
        app.validate_source_origin(source)
        for key, value in [('subscriptionUrl', 'https://lists.example/other'),
                           ('evidenceUrl', 'https://other.example/'), ('status', 'inferred')]:
            changed = dict(source, provenance=dict(source['provenance'], **{key: value}))
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Unverified official'):
                app.validate_source_origin(changed)
        source['url'] = 'http://lists.example/hosts/hosts'
        source['provenance']['subscriptionUrl'] = source['url']
        with self.assertRaisesRegex(ValueError, 'Unverified official'):
            app.validate_source_origin(source)

    def test_one_download_per_source_and_no_timestamp_only_output_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', side_effect=lambda url, *_: self.rule_body('a' if url.endswith('a.txt') else 'b')) as fetch:
                self.assertEqual(app.build(*args), 0)
                self.assertEqual(fetch.call_count, 2)
                original = {p.name: p.read_bytes() for p in args[2].iterdir()}
                self.assertEqual(app.build(*args), 0)
                self.assertEqual(fetch.call_count, 4)
                self.assertEqual(original, {p.name: p.read_bytes() for p in args[2].iterdir()})
                self.assertEqual((args[2] / 'alpha.txt').read_bytes(), (args[2] / 'adguard.txt').read_bytes())

    def test_failed_source_retains_affected_profiles_and_other_profiles_update(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', return_value=self.rule_body('base')):
                self.assertEqual(app.build(*args), 0)
            retained = {pid: (args[2] / (pid + '.txt')).read_bytes() for pid in ('beta', 'both')}

            def fetch(url, *_):
                if url.endswith('b.txt'):
                    raise ValueError('invalid response')
                return self.rule_body('changed', 6)

            with patch.object(app, 'fetch', side_effect=fetch):
                self.assertEqual(app.build(*args), 1)
            for pid, content in retained.items():
                self.assertEqual(content, (args[2] / (pid + '.txt')).read_bytes())
            manifest = app.read_json(args[2] / 'manifest.json')
            self.assertEqual(manifest['profiles']['beta']['status'], 'retained')
            self.assertEqual(manifest['profiles']['alpha']['totalRules'], 6)
            self.assertIn(b'changed0.example.com', (args[2] / 'adguard.txt').read_bytes())

    def test_cache_fallback_and_expiry_keep_existing_subscriptions(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', return_value=self.rule_body('base')):
                self.assertEqual(app.build(*args), 0)
            before = (args[2] / 'adguard.txt').read_bytes()
            with patch.object(app, 'fetch', side_effect=OSError('offline')):
                self.assertEqual(app.build(*args), 0)
            runtime = app.read_json(args[4] / 'last-run.json')
            self.assertEqual(len(runtime['cacheSources']), 2)
            for meta_path in (args[4] / 'sources').glob('*.json'):
                meta = app.read_json(meta_path)
                meta['downloadedUtc'] = (datetime.now(timezone.utc)-timedelta(days=5)).isoformat()
                meta_path.write_text(json.dumps(meta), encoding='utf-8')
            with patch.object(app, 'fetch', side_effect=OSError('offline')):
                self.assertEqual(app.build(*args), 1)
            self.assertEqual(before, (args[2] / 'adguard.txt').read_bytes())

    def test_profile_count_decrease_is_checked_after_optimization(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', return_value=self.rule_body('base')):
                app.build(*args)
            before = (args[2] / 'adguard.txt').read_bytes()
            body = '||parent.example^\n' + '\n'.join(f'||sub{i}.parent.example^' for i in range(4))
            with patch.object(app, 'fetch', return_value=body):
                self.assertEqual(app.build(*args), 1)
                self.assertEqual(before, (args[2] / 'adguard.txt').read_bytes())
                self.assertEqual(app.build(*args, allow_large_drop=True), 0)

    def test_first_failed_source_can_recover_without_previous_accepted_count(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            def fetch(url, *_):
                if url.endswith('b.txt'):
                    raise ValueError('first download failed')
                return self.rule_body('base')
            with patch.object(app, 'fetch', side_effect=fetch):
                self.assertEqual(app.build(*args), 1)
            self.assertFalse((args[2] / 'beta.txt').exists())
            with patch.object(app, 'fetch', return_value=self.rule_body('recovered')):
                self.assertEqual(app.build(*args), 0)
            self.assertTrue((args[2] / 'beta.txt').exists())

    def test_version_family_and_path_traversal_are_rejected_before_download(self):
        with tempfile.TemporaryDirectory() as folder:
            config, sources, args = self.setup_project(Path(folder))
            for source in sources:
                source['variantFamily'] = 'tiers'
            args[1].write_text(json.dumps(dict(sources=sources)), encoding='utf-8')
            with patch.object(app, 'fetch') as fetch:
                with self.assertRaisesRegex(ValueError, 'multiple versions'):
                    app.build(*args)
                fetch.assert_not_called()
            config['profiles'][0]['id'] = '../escape'
            args[0].write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'profile id'):
                app.load_plan(args[0], args[1])

    def test_deduplication_does_not_remove_shared_rules_from_other_profiles(self):
        with tempfile.TemporaryDirectory() as folder:
            _, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', return_value=self.rule_body('shared')):
                self.assertEqual(app.build(*args), 0)
            for pid in ('alpha', 'beta', 'both'):
                text = (args[2] / (pid + '.txt')).read_text(encoding='utf-8')
                self.assertEqual(text.count('||shared0.example.com^'), 1)

    def test_coverage_can_be_disabled_without_expanding_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            config, _, args = self.setup_project(Path(folder))
            config['profiles'][0]['coverageOptimization'] = False
            args[0].write_text(json.dumps(config), encoding='utf-8')
            with patch.object(app, 'fetch', return_value='||example.com^\n||ads.example.com^'):
                self.assertEqual(app.build(*args), 0)
            text = (args[2] / 'alpha.txt').read_text(encoding='utf-8')
            self.assertIn('||ads.example.com^', text)
            self.assertIn('||example.com^', text)

    def test_failed_reconfiguration_reports_actual_retained_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            config, _, args = self.setup_project(Path(folder))
            with patch.object(app, 'fetch', return_value=self.rule_body('base')):
                self.assertEqual(app.build(*args), 0)
            config['profiles'][0]['sourceIds'] = ['b']
            args[0].write_text(json.dumps(config), encoding='utf-8')
            with patch.object(app, 'fetch', side_effect=ValueError('invalid source')):
                self.assertEqual(app.build(*args), 1)
            retained = app.read_json(args[2] / 'manifest.json')['profiles']['alpha']
            self.assertEqual(retained['sourceIds'], ['a'])
            self.assertEqual(retained['requestedSourceIds'], ['b'])


if __name__ == '__main__':
    unittest.main()
