import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
import unittest
from urllib.request import ProxyHandler, build_opener

from export_mihomo import convert_rule, export, reject_rules, kernel_errors
from workflow_status import mihomo_content


class ConversionTests(unittest.TestCase):
    def test_normal_linux_shutdown_is_not_a_rule_validation_warning(self):
        self.assertEqual(kernel_errors('level=warning msg="Mihomo shutting down"\n'), [])
        self.assertEqual(len(kernel_errors('level=warning msg="skip invalid domain"\n')), 1)
        self.assertEqual(len(kernel_errors('level=error msg="failed to load rule provider"\n')), 1)

    def test_exact_suffix_wildcard_and_priority(self):
        self.assertEqual(convert_rule('|child.parent.example|'), ('block', 'domain', 'child.parent.example'))
        self.assertEqual(convert_rule('||child.parent.example^'), ('block', 'domain', '+.child.parent.example'))
        self.assertEqual(convert_rule('@@||safe.example^$important'), ('allow-important', 'domain', '+.safe.example'))
        bucket, behavior, rule = convert_rule('||ads*.example^')
        self.assertEqual((bucket, behavior), ('block', 'classical'))
        self.assertIn(r'^', rule)
        self.assertIn(r'ads.*\.example', rule)
        self.assertEqual(convert_rule(r'/^rx[0-9]{2,3}\.example$/')[2], r'DOMAIN-REGEX,^rx[0-9]{2,3}\.example$')
        with self.assertRaises(ValueError):
            convert_rule('||example.com^$client=foo')

    def test_exceptions_preserve_priority_and_do_not_force_direct(self):
        providers = {name: {'bucket': name} for name in ('block', 'allow', 'block-important', 'allow-important')}
        rules = reject_rules(providers)
        self.assertEqual(rules, [
            'AND,((RULE-SET,block-important),(NOT,((RULE-SET,allow-important)))),REJECT',
            'AND,((RULE-SET,block),(NOT,((RULE-SET,allow))),(NOT,((RULE-SET,allow-important)))),REJECT'])
        self.assertNotIn('DIRECT', ''.join(rules))

    def test_readme_rejects_stale_conversion(self):
        dns = {'profiles': {'china': {'fileSha256': 'new'}}}
        with self.assertRaisesRegex(ValueError, 'checksum'):
            mihomo_content(dns, {'profiles': {'china': {'inputSha256': 'old'}}}, 'fixture/rules')


@unittest.skipUnless(os.environ.get('MIHOMO_BINARY') and os.environ.get('DNS_RULE_VALIDATOR'),
                     'Set both MIHOMO_BINARY and DNS_RULE_VALIDATOR for real engine comparisons')
class RealMihomoTests(unittest.TestCase):
    def test_actual_kernel_matches_adguard_scope_masks_regex_and_exception_priority(self):
        rules = [
            '||parent.example^', '@@||safe.parent.example^', '|exact.example|',
            '||ads*.wild.example^', '@@||ads-safe.wild.example^',
            '||forced.example^$important', '@@||forced.example^',
            '||double.example^$important', '@@||double.example^$important',
            '||partial.example', '*track*.free.example*', r'/^rx[0-9]{2,3}\.example$/',
            '||*.suffix.example^']
        hosts = ['parent.example', 'child.parent.example', 'safe.parent.example', 'deep.safe.parent.example',
                 'exact.example', 'child.exact.example', 'example', 'ads1.wild.example',
                 'deep.ads1.wild.example', 'notads1.wild.example', 'ads-safe.wild.example',
                 'forced.example', 'child.forced.example', 'double.example', 'child.double.example',
                 'partial.example', 'partial.example-extra', 'child.partial.example',
                 'notpartial.example', 'tracking.free.example', 'nottrack.free.example', 'other.example',
                 'rx12.example', 'rx123.example', 'rx1.example', 'rx1234.example',
                 'suffix.example', 'child.suffix.example', 'deep.child.suffix.example']
        comparison = subprocess.run([os.environ['DNS_RULE_VALIDATOR'], '--match'],
            input=json.dumps([dict(rules=rules, hosts=hosts)]), capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(comparison.returncode, 0, comparison.stderr)
        expected = json.loads(comparison.stdout)[0]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, output = root / 'dns', root / 'mihomo'
            source.mkdir()
            body = '\n'.join(sorted(rules)) + '\n'
            (source / 'fixture.txt').write_text(body, encoding='utf-8', newline='\n')
            checksum = hashlib.sha256(body.encode()).hexdigest()
            manifest = {'profiles': {'fixture': dict(status='ready', sourceIds=['a'], fileSha256=checksum,
                updatedUtc='2026-10-02T00:00:00Z', totalRules=len(rules),
                blockingRules=sum(not r.startswith('@@') for r in rules), exceptionRules=sum(r.startswith('@@') for r in rules))}}
            (source / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            config = {'profiles': [dict(id='fixture', name='fixture', enabled=True, kind='blocklist', sourceIds=['a'])]}
            config_path = root / 'profiles.json'
            config_path.write_text(json.dumps(config), encoding='utf-8')
            report = export(source, output, config_path, os.environ['MIHOMO_BINARY'], 'fixture/rules')
            self.assertEqual(report['profiles']['fixture']['inputRules'], len(rules))
            boki = json.loads((output / 'fixture-boki.yaml').read_text(encoding='utf-8'))
            self.assertTrue(all(p['url'].startswith('https://github.boki.moe/https://raw.githubusercontent.com/fixture/rules/')
                                for p in boki['rule-providers'].values()))
            files_before = {p.name: p.read_bytes() for p in output.iterdir()}
            (source / 'fixture.txt').write_text(body + '||tampered.example^\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                export(source, output, config_path, os.environ['MIHOMO_BINARY'], 'fixture/rules')
            self.assertEqual(files_before, {p.name: p.read_bytes() for p in output.iterdir()})

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'allowed')
                def log_message(self, *args):
                    pass
            server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            def free_port():
                with socket.socket() as sock:
                    sock.bind(('127.0.0.1', 0))
                    return sock.getsockname()[1]
            proxy_port, controller_port = free_port(), free_port()
            runtime = json.loads((output / 'fixture.yaml').read_text(encoding='utf-8'))
            for name, provider in runtime['rule-providers'].items():
                provider['type'] = 'file'
                provider['path'] = report['profiles']['fixture']['providers'][name]['file']
                provider.pop('url')
            runtime.update({'mixed-port': proxy_port, 'bind-address': '127.0.0.1',
                            'external-controller': f'127.0.0.1:{controller_port}',
                            'hosts': {host: '127.0.0.1' for host in hosts}, 'log-level': 'warning'})
            runtime['rules'].append('MATCH,DIRECT')
            runtime_path = output / 'runtime.json'
            runtime_path.write_text(json.dumps(runtime), encoding='utf-8')
            with (root / 'runtime.log').open('w', encoding='utf-8') as log:
                process = subprocess.Popen([os.environ['MIHOMO_BINARY'], '-d', str(output), '-f', str(runtime_path)],
                    stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                try:
                    opener = build_opener(ProxyHandler({}))
                    for attempt in range(100):
                        try:
                            with opener.open(f'http://127.0.0.1:{controller_port}/providers/rules', timeout=1) as response:
                                loaded = json.load(response)['providers']
                            if all(loaded.get(n, {}).get('ruleCount') == p['rules']
                                   for n, p in report['profiles']['fixture']['providers'].items()):
                                break
                        except OSError:
                            pass
                        time.sleep(.1)
                    else:
                        self.fail('mihomo providers did not initialize')
                    observed = []
                    for host in hosts:
                        connection = http.client.HTTPConnection('127.0.0.1', proxy_port, timeout=3)
                        try:
                            connection.request('GET', f'http://{host}:{server.server_port}/check')
                            response = connection.getresponse()
                            observed.append(response.status != 200)
                            response.read()
                        except (OSError, http.client.HTTPException):
                            observed.append(True)
                        finally:
                            connection.close()
                    self.assertEqual(observed, expected, list(zip(hosts, observed, expected)))
                finally:
                    process.terminate()
                    process.wait(timeout=10)
                    server.shutdown()
                    server.server_close()


if __name__ == '__main__':
    unittest.main()
