import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_filters as builder
import publish_filters as publisher
from tests import test_builder as fixtures


class SelectionPolicyTests(unittest.TestCase):
    def test_only_verified_language_or_documented_china_focus_qualifies(self):
        with tempfile.TemporaryDirectory() as folder:
            config, sources, args = fixtures.BuilderTests().setup_project(Path(folder))
            config['sourcePolicy'] = dict(mode='chinese-or-china')
            sources[0]['selectionEvidence'] = dict(repositoryLanguage='zh',
                basis='reviewed_repository_documentation', evidenceUrl=sources[0]['repository']+'#readme')
            sources[1]['regionalFocus'] = dict(value='CN', basis='repository_documentation', scope='dns')
            args[0].write_text(json.dumps(config), encoding='utf-8')
            args[1].write_text(json.dumps(dict(sources=sources)), encoding='utf-8')
            builder.load_plan(args[0], args[1])
            sources[1]['regionalFocus']['basis'] = 'account_name_guess'
            args[1].write_text(json.dumps(dict(sources=sources)), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Chinese/China policy'):
                builder.load_plan(args[0], args[1])

    def test_retired_cleanup_preserves_active_and_unknown_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'mihomo').mkdir()
            files=['retired.txt','active.txt','user-health.json','mihomo/retired.mrs',
                   'mihomo/retired.yaml','mihomo/retired-boki.yaml','mihomo/retired-ghfast.yaml']
            for name in files:
                (root/name).write_text('unchanged', encoding='utf-8')
            retired = publisher.prune_retired(root, dict(profiles={'retired':{},'active':{}}),
                dict(profiles={'retired':dict(providers={'one':dict(file='retired.mrs')})}), {'active'})
            self.assertEqual(retired, ['retired'])
            self.assertTrue((root/'active.txt').exists())
            self.assertTrue((root/'user-health.json').exists())
            self.assertFalse((root/'retired.txt').exists())
            self.assertFalse((root/'mihomo/retired.mrs').exists())

    def test_engine_compatibility_gate_preserves_previous_subscription(self):
        if not __import__('os').environ.get('DNS_RULE_VALIDATOR'):
            self.skipTest('Requires the official AdGuard validator')
        from tests.test_publication import PublicationTests
        with tempfile.TemporaryDirectory() as folder:
            fixture=fixtures.BuilderTests()
            config, _, args=fixture.setup_project(Path(folder))
            runner=PublicationTests()
            with patch.object(builder,'fetch',return_value=fixture.rule_body('safe')), patch.object(publisher,'export',side_effect=runner.fake_export):
                runner.run_publish(args)
            previous=(args[2]/'alpha.txt').read_bytes()
            config['compatibilityHosts']=['service0.example.com']
            args[0].write_text(json.dumps(config),encoding='utf-8')
            with patch.object(builder,'fetch',return_value=fixture.rule_body('service')), patch.object(publisher,'export',side_effect=runner.fake_export):
                report=runner.run_publish(args)
            self.assertEqual(report['status'],'failed')
            self.assertIn('Compatibility samples blocked',report['failures']['alpha']['dns'])
            self.assertEqual((args[2]/'alpha.txt').read_bytes(),previous)
