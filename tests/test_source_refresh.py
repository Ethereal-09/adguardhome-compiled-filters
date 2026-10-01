import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from refresh_source_registry import refresh


class SourceRefreshTests(unittest.TestCase):
    def test_browser_exception_rejects_source_and_native_exceptions_survive(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            entries=[dict(id=sid,name=sid,repository='https://github.com/test/rules',repositoryAccount='test',
                url=f'https://raw.githubusercontent.com/test/rules/main/{sid}.txt',role='filter',
                categories=['ads'],strength={'value':'unknown'},regionalFocus={'value':'unknown'})
                for sid in ('dns','browser')]
            catalog=root/'reviewed.json'
            catalog.write_text(json.dumps(dict(sources=entries)),encoding='utf-8')
            def body(url,*args):
                return ('||ads.example^\n@@||safe.ads.example^' if url.endswith('/dns.txt')
                        else '||ads.example^\n@@||ads.example/allowed.js$script')
            with patch('build_filters.fetch',side_effect=body):
                report=refresh(catalog,root/'sources.json',root/'cache',None)
            sources={s['id']:s for s in report['sources']}
            self.assertEqual(sources['dns']['dnsBlocks'],1)
            self.assertEqual(sources['dns']['dnsExceptions'],1)
            self.assertTrue(sources['dns']['eligibleForSubscription'])
            self.assertFalse(sources['browser']['eligibleForSubscription'])
            self.assertIn('Unsupported exception',sources['browser']['error'])
            self.assertEqual(len(list((root/'cache/sources').glob('*.json'))),1)


if __name__=='__main__':
    unittest.main()
