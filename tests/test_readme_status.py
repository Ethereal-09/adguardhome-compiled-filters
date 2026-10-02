from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import build_filters as builder
from tests import test_builder as fixtures
from workflow_status import (BUILD_END, BUILD_START, SUBSCRIPTIONS_START, SUBSCRIPTIONS_END,
                             UPSTREAM_START, UPSTREAM_END, MIHOMO_START, MIHOMO_END, update_readme)


class ReadmeStatusTests(unittest.TestCase):
    def test_partial_publication_refreshes_ready_counts_and_marks_retained_versions(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            publication = self.publication_fixture()
            publication['manifest']['profiles']['full']['status'] = 'retained'
            report = dict(status='partial', checkedUtc='2026-10-02T00:02:00Z',
                          publishedUtc='2026-10-02T00:02:00Z', dnsValidated=['new-category'], mihomoValidated=[])
            update_readme(path, dict(checkedUtc='2026-10-02T00:00:00Z'), publication=report, **publication)
            text = path.read_text(encoding='utf-8')
            self.assertIn('最近成功发布：**2026-10-02 08:02:00', text)
            self.assertIn('全量版（保留旧版） | 1,200', text)
            self.assertIn('新增用途 | 7', text)
            self.assertIn('部分更新', text)
            update_readme(path, dict(checkedUtc='2026-10-03T00:00:00Z', status='failed'), 'failure', 'failure')
            self.assertIn('最近成功发布：**2026-10-02 08:02:00', path.read_text(encoding='utf-8'))

    def write_readme(self, root, with_publication=False):
        path = root / 'README.md'
        publication = (f'\n{SUBSCRIPTIONS_START}\nprevious subscriptions\n{SUBSCRIPTIONS_END}\n'
                       f'\n{UPSTREAM_START}\nprevious upstream counts\n{UPSTREAM_END}\n') if with_publication else ''
        path.write_text(f'# Title\n\n{BUILD_START}\nold\n{BUILD_END}\n{publication}\n## Sources\nkeep credits\n', encoding='utf-8')
        return path

    def publication_fixture(self):
        config = dict(defaultProfile='full', profiles=[
            dict(id='full', name='全量', enabled=True, kind='blocklist', axis='composition', sourceIds=['a']),
            dict(id='new-category', name='新增用途', enabled=True, kind='blocklist', axis='type', sourceIds=['a']),
            dict(id='allow-test', name='测试放行', enabled=True, kind='allowlist', axis='type', sourceIds=['b'])])
        registry = dict(sources=[dict(id=sid, repository='https://github.com/fixture/rules',
            path=filename, url='https://raw.githubusercontent.com/fixture/rules/main/'+filename,
            dnsBlocks=99999) for sid, filename in [('a', 'block.txt'), ('b', 'allow.txt')]])
        manifest = dict(profiles={
            'full': dict(status='ready', sourceIds=['a'], totalRules=1200, blockingRules=1190, exceptionRules=10),
            'new-category': dict(status='ready', sourceIds=['a'], totalRules=7, blockingRules=7, exceptionRules=0),
            'allow-test': dict(status='ready', sourceIds=['b'], totalRules=3, blockingRules=0, exceptionRules=3)},
            sources={source['id']: dict(url=source['url'], accepted=2200 if source['id']=='a' else 3)
                     for source in registry['sources']})
        return dict(config=config, manifest=manifest, registry=registry, repository='fixture/compiled')

    def test_every_subscription_and_actual_upstream_counts_refresh_after_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            publication = self.publication_fixture()
            run = dict(checkedUtc='2026-09-30T20:23:00+00:00', status='success')
            update_readme(path, run, 'success', 'success', **publication)
            text = path.read_text(encoding='utf-8')
            self.assertIn('| 全量版 | 1,200 |', text)
            self.assertIn('| 新增用途 | 7 |', text)
            self.assertIn('| 测试放行 | 3 |', text)
            self.assertIn('main/dist/adguard.txt', text)
            self.assertIn('main/dist/new-category.txt', text)
            self.assertIn('[block.txt](https://raw.githubusercontent.com/fixture/rules/main/block.txt) | 2,200 |', text)
            self.assertIn('**2 个来源文件**', text)
            self.assertNotIn('99,999', text)
            self.assertTrue(text.endswith('## Sources\nkeep credits\n'))
            subscriptions = text.split(SUBSCRIPTIONS_START)[1].split(SUBSCRIPTIONS_END)[0]
            self.assertIn('<summary>其他分类订阅（2 项）', subscriptions)
            self.assertLess(subscriptions.index('| 全量版 |'), subscriptions.index('<details>'))
            self.assertLess(subscriptions.index('<details>'), subscriptions.index('| 新增用途 |'))
            self.assertLess(subscriptions.index('| 测试放行 |'), subscriptions.index('</details>'))

            publication['manifest']['profiles']['full'].update(totalRules=1600, blockingRules=1590)
            publication['manifest']['sources']['a']['accepted'] = 3300
            update_readme(path, run, 'success', 'success', **publication)
            text = path.read_text(encoding='utf-8')
            self.assertIn('| 全量版 | 1,600 |', text)
            self.assertIn(' | 3,300 |', text)
            self.assertNotIn('| 全量版 | 1,200 |', text)
            self.assertEqual(text.count('<summary>其他分类订阅'), 1)

    def test_official_website_attribution_is_not_counted_as_a_github_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            publication = self.publication_fixture()
            source = publication['registry']['sources'][0]
            source.update(repository='https://lists.example/hosts/', repositoryAccount='Original Author',
                          url='https://lists.example/hosts/block.txt')
            publication['manifest']['sources']['a']['url'] = source['url']
            update_readme(path, dict(checkedUtc='2026-10-01T00:00:00Z',status='success'),
                          'success','success',**publication)
            content=path.read_text(encoding='utf-8')
            self.assertIn('**1 个 GitHub 原仓库**及 **1 个官方站点**',content)
            self.assertIn('[Original Author](https://lists.example/hosts/)',content)

    def test_accelerators_wrap_each_exact_original_including_default_and_allowlist(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            publication = self.publication_fixture()
            run = dict(checkedUtc='2026-10-02T00:00:00Z', status='success')
            update_readme(path, run, 'success', 'success', **publication)
            text = path.read_text(encoding='utf-8')
            subscriptions = text.split(SUBSCRIPTIONS_START)[1].split(SUBSCRIPTIONS_END)[0]
            rows = [line for line in subscriptions.splitlines() if '[原始](' in line]
            self.assertEqual(len(rows), 3)
            for filename, row in zip(['adguard.txt', 'new-category.txt', 'allow-test.txt'], rows):
                original = f'https://raw.githubusercontent.com/fixture/compiled/main/dist/{filename}'
                self.assertEqual(re.findall(r'\]\(([^)]+)\)', row), [original,
                    'https://github.boki.moe/' + original, 'https://ghfast.top/' + original])
            self.assertNotIn('jsdelivr.net', subscriptions)
            before = path.read_bytes()
            update_readme(path, run, 'success', 'success', **publication)
            self.assertEqual(before, path.read_bytes())

    def test_build_or_audit_failure_preserves_published_counts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            publication = self.publication_fixture()
            run = dict(checkedUtc='2026-09-30T20:23:00+00:00', status='success')
            update_readme(path, run, 'success', 'success', **publication)
            before = path.read_text(encoding='utf-8')
            publication['manifest']['profiles']['full'].update(totalRules=1600, blockingRules=1590)
            publication['manifest']['sources']['a']['accepted'] = 3300
            for build, audit in [('failure', 'skipped'), ('success', 'failure')]:
                with self.subTest(build=build, audit=audit):
                    update_readme(path, run, build, audit, **publication)
                    text = path.read_text(encoding='utf-8')
                    for start, end in [(SUBSCRIPTIONS_START, SUBSCRIPTIONS_END), (UPSTREAM_START, UPSTREAM_END)]:
                        self.assertEqual(text.split(start)[1].split(end)[0], before.split(start)[1].split(end)[0])

    def test_mihomo_readme_updates_only_with_matching_validated_outputs(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            with path.open('a', encoding='utf-8') as handle:
                handle.write(f'\n{MIHOMO_START}\nold mihomo links\n{MIHOMO_END}\n')
            publication = self.publication_fixture()
            converted = {'profiles': {}}
            for pid, item in publication['manifest']['profiles'].items():
                item['fileSha256'] = pid + '-sha256'
                converted['profiles'][pid] = dict(name=pid, inputSha256=item['fileSha256'],
                    blockingRules=item['blockingRules'], exceptionRules=item['exceptionRules'])
            publication['mihomo_manifest'] = converted
            run = dict(checkedUtc='2026-10-02T00:00:00Z', status='success')
            update_readme(path, run, 'success', 'success', **publication)
            text = path.read_text(encoding='utf-8')
            self.assertIn('main/dist/mihomo/full.yaml', text)
            self.assertIn('https://github.boki.moe/https://raw.githubusercontent.com/fixture/compiled/main/dist/mihomo/full-boki.yaml', text)
            before = text.split(MIHOMO_START)[1].split(MIHOMO_END)[0]
            converted['profiles']['full']['inputSha256'] = 'stale'
            update_readme(path, run, 'success', 'failure', **publication)
            self.assertEqual(path.read_text(encoding='utf-8').split(MIHOMO_START)[1].split(MIHOMO_END)[0], before)
            contents = path.read_bytes()
            with self.assertRaisesRegex(ValueError, 'checksum'):
                update_readme(path, run, 'success', 'success', **publication)
            self.assertEqual(contents, path.read_bytes())

    def test_unready_outputs_cannot_replace_readme_numbers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder), with_publication=True)
            before = path.read_bytes()
            publication = self.publication_fixture()
            publication['manifest']['profiles']['full']['status'] = 'retained'
            with self.assertRaisesRegex(ValueError, 'require ready outputs'):
                update_readme(path, dict(checkedUtc='2026-09-30T20:23:00+00:00', status='success'),
                              'success', 'success', **publication)
            self.assertEqual(path.read_bytes(), before)

    def test_converts_build_completion_to_beijing_and_preserves_credits(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder))
            run = dict(checkedUtc='2026-09-30T20:23:00+00:00', status='success', profileCount=30,
                       failedProfiles=[], sources={'a': {'status': 'fresh'}, 'b': {'status': 'cached'}})
            update_readme(path, run, 'success', 'success')
            text = path.read_text(encoding='utf-8')
            self.assertIn('2026-10-01 04:23:00（北京时间）', text)
            self.assertIn('新下载 1，缓存 1', text)
            self.assertIn('已通过发布校验', text)
            self.assertTrue(text.endswith('## Sources\nkeep credits\n'))

    def test_audit_failure_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_readme(Path(folder))
            update_readme(path, dict(checkedUtc='2026-09-30T20:23:00+00:00', status='success'), 'success', 'failure')
            text = path.read_text(encoding='utf-8')
            self.assertIn('发布校验失败，订阅保留旧版', text)
            self.assertNotIn('已通过发布校验', text)

    def test_unchanged_subscriptions_still_update_readme_completion_time(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            fixture = fixtures.BuilderTests()
            _, _, args = fixture.setup_project(root)
            readme = self.write_readme(root)
            with patch.object(builder, 'fetch', return_value=fixture.rule_body('same')), patch.object(
                    builder, 'utcnow', return_value='2026-09-30T20:23:00+00:00'):
                self.assertEqual(builder.build(*args, readme=readme), 0)
            before = {p.name: p.read_bytes() for p in args[2].iterdir()}
            with patch.object(builder, 'fetch', return_value=fixture.rule_body('same')), patch.object(
                    builder, 'utcnow', return_value='2026-10-01T20:23:00+00:00'):
                self.assertEqual(builder.build(*args, readme=readme), 0)
            self.assertEqual(before, {p.name: p.read_bytes() for p in args[2].iterdir()})
            self.assertIn('2026-10-02 04:23:00（北京时间）', readme.read_text(encoding='utf-8'))

    def test_configuration_failure_records_failed_completion_time(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            fixture = fixtures.BuilderTests()
            _, _, args = fixture.setup_project(root)
            readme = self.write_readme(root)
            args[0].write_text('{invalid json', encoding='utf-8')
            with patch.object(builder, 'utcnow', return_value='2026-09-30T20:23:00+00:00'):
                with self.assertRaises(ValueError):
                    builder.build(*args, readme=readme)
            text = readme.read_text(encoding='utf-8')
            self.assertIn('构建失败', text)
            self.assertIn('2026-10-01 04:23:00（北京时间）', text)
