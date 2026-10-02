import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_filters
import publish_filters as app
from workflow_status import mihomo_content
from tests import test_builder as fixtures


@unittest.skipUnless(os.environ.get('DNS_RULE_VALIDATOR'), 'Requires the official AdGuard validator')
class PublicationTests(unittest.TestCase):
    def fake_export(self, source, output, config, binary, repository):
        """A controllable converter boundary; DNS audits still run the real engine."""
        output.mkdir(parents=True, exist_ok=True)
        profiles = {}
        dns = app.read_json(source / 'manifest.json')
        for p in app.read_json(config)['profiles']:
            pid = p['id']
            data = (source / (pid + '.txt')).read_bytes()
            filename = pid + '.mrs'
            (output / filename).write_bytes(data)
            for suffix in ('', '-boki', '-ghfast'):
                (output / (pid + suffix + '.yaml')).write_text('rules: []\n', encoding='utf-8')
            item = dns['profiles'][pid]
            profiles[pid] = dict(name=p['name'], kind=p['kind'], sourceIds=p['sourceIds'],
                updatedUtc=item['updatedUtc'], inputSha256=item['fileSha256'],
                blockingRules=item['blockingRules'], exceptionRules=item['exceptionRules'],
                inputRules=item['totalRules'], providers={pid: dict(file=filename, rules=item['totalRules'],
                    sha256=hashlib.sha256(data).hexdigest())}, rules=[])
        return dict(profiles=profiles)

    def run_publish(self, args):
        return app.publish(*args, os.environ['DNS_RULE_VALIDATOR'], 'test-boundary')

    def test_source_failure_retains_only_affected_outputs_and_updates_healthy_default(self):
        with tempfile.TemporaryDirectory() as folder:
            fixture = fixtures.BuilderTests()
            _, _, args = fixture.setup_project(Path(folder))
            with patch.object(build_filters, 'fetch', return_value=fixture.rule_body('base')), patch.object(app, 'export', side_effect=self.fake_export):
                self.assertEqual(self.run_publish(args)['status'], 'success')
            before = {name: (args[2] / name).read_bytes() for name in ('beta.txt', 'both.txt', 'mihomo/beta.mrs')}
            def fetch(url, *_):
                if url.endswith('b.txt'):
                    raise ValueError('deliberately bad source')
                return fixture.rule_body('changed', 6)
            with patch.object(build_filters, 'fetch', side_effect=fetch), patch.object(app, 'export', side_effect=self.fake_export):
                report = self.run_publish(args)
            self.assertEqual(report['status'], 'partial')
            self.assertEqual(report['dnsValidated'], ['alpha'])
            self.assertEqual(report['mihomoValidated'], ['alpha'])
            self.assertEqual(report['changes']['alpha'], dict(added=6, removed=5))
            for name, data in before.items():
                self.assertEqual((args[2] / name).read_bytes(), data)
            self.assertEqual((args[2] / 'adguard.txt').read_bytes(), (args[2] / 'alpha.txt').read_bytes())
            self.assertIn(b'changed', (args[2] / 'adguard.txt').read_bytes())

    def test_mihomo_failure_does_not_block_dns_or_other_mihomo_profiles(self):
        with tempfile.TemporaryDirectory() as folder:
            fixture = fixtures.BuilderTests()
            _, _, args = fixture.setup_project(Path(folder))
            with patch.object(build_filters, 'fetch', return_value=fixture.rule_body('base')), patch.object(app, 'export', side_effect=self.fake_export):
                self.run_publish(args)
            before = (args[2] / 'mihomo/beta.mrs').read_bytes()
            def export(source, output, config, *rest):
                if any(p['id'] == 'beta' for p in app.read_json(config)['profiles']):
                    raise ValueError('deliberate beta conversion failure')
                return self.fake_export(source, output, config, *rest)
            with patch.object(build_filters, 'fetch', return_value=fixture.rule_body('updated', 6)), patch.object(app, 'export', side_effect=export):
                report = self.run_publish(args)
            self.assertEqual(report['status'], 'partial')
            self.assertEqual(len(report['dnsValidated']), 3)
            self.assertEqual(set(report['mihomoValidated']), {'alpha', 'both'})
            self.assertEqual((args[2] / 'mihomo/beta.mrs').read_bytes(), before)
            self.assertIn(b'updated', (args[2] / 'beta.txt').read_bytes())
            dns = app.read_json(args[2] / 'manifest.json')['profiles']['beta']
            mi = app.read_json(args[2] / 'mihomo/manifest.json')['profiles']['beta']
            self.assertEqual(mi['status'], 'retained')
            self.assertNotEqual(mi['inputSha256'], dns['fileSha256'])
            text = mihomo_content(app.read_json(args[2] / 'manifest.json'),
                app.read_json(args[2] / 'mihomo/manifest.json'), 'fixture/rules', allow_stale=True)
            self.assertIn('beta（保留旧版）（与 DNS 版本不同）', text)

    def test_post_build_checksum_failure_preserves_previous_file(self):
        with tempfile.TemporaryDirectory() as folder:
            fixture = fixtures.BuilderTests()
            _, _, args = fixture.setup_project(Path(folder))
            with patch.object(build_filters, 'fetch', return_value=fixture.rule_body('base')), patch.object(app, 'export', side_effect=self.fake_export):
                self.run_publish(args)
            before = (args[2] / 'beta.txt').read_bytes()
            real_audit = app.audit
            def audit(output, config, registry, validator, selected, **options):
                if 'beta' in selected:
                    (output / 'beta.txt').write_text('||tampered.example^\n', encoding='utf-8')
                return real_audit(output, config, registry, validator, selected, **options)
            with patch.object(build_filters, 'fetch', return_value=fixture.rule_body('updated', 6)), patch.object(app, 'export', side_effect=self.fake_export), patch.object(app, 'audit', side_effect=audit):
                report = self.run_publish(args)
            self.assertEqual(report['status'], 'partial')
            self.assertNotIn('beta', report['dnsValidated'])
            self.assertEqual((args[2] / 'beta.txt').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
