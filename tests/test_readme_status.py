from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_filters as builder
from tests import test_builder as fixtures
from workflow_status import BUILD_END, BUILD_START, update_readme


class ReadmeStatusTests(unittest.TestCase):
    def write_readme(self, root):
        path = root / 'README.md'
        path.write_text(f'# Title\n\n{BUILD_START}\nold\n{BUILD_END}\n\n## Sources\nkeep credits\n', encoding='utf-8')
        return path

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
