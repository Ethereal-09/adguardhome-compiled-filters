"""Behavior checks using AdGuard's actual DNSEngine, enabled in every CI run."""
import json
import os
import random
import subprocess
import unittest

from build_filters import optimize_rules, validate_engine


@unittest.skipUnless(os.environ.get('DNS_RULE_VALIDATOR'), 'Set DNS_RULE_VALIDATOR to run real AdGuard engine tests')
class RealEngineTests(unittest.TestCase):
    def match_cases(self, cases):
        result = subprocess.run([os.environ['DNS_RULE_VALIDATOR'], '--match'],
                                input=json.dumps(cases), capture_output=True, text=True, encoding='utf-8', timeout=90)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_invalid_regex_and_non_dns_modifiers_are_rejected(self):
        for rule in ('/[/', '/(?=ads)/', '@@/[/', '||ads.example^$third-party'):
            with self.subTest(rule=rule), self.assertRaisesRegex(ValueError, 'validation failed'):
                validate_engine({rule}, os.environ['DNS_RULE_VALIDATOR'])

    def test_subdomain_exact_hosts_and_exception_priority(self):
        hosts = ['example.com', 'ads.example.com', 'a.ads.example.com', 'safe.example.com']
        cases = [dict(rules=rules, hosts=hosts) for rules in [
            ['||ads.example.com^'], ['|ads.example.com|'],
            ['||example.com^', '@@||safe.example.com^'],
            ['||ads.example.com^$important', '@@||ads.example.com^'],
            ['||ads.example.com^$important', '@@||ads.example.com^$important'],
        ]]
        self.assertEqual(self.match_cases(cases), [
            [False, True, True, False], [False, True, False, False],
            [True, True, True, False], [False, True, True, False], [False, False, False, False],
        ])

    def test_coverage_optimization_preserves_actual_engine_decisions(self):
        names = ['parent.example', 'a.parent.example', 'b.parent.example', 'deep.a.parent.example']
        pool = [prefix + anchor + name + end + modifier for name in names
                for prefix in ('', '@@') for anchor, end in (('||', '^'), ('|', '|'))
                for modifier in ('', '$important')]
        hosts = names + ['x.' + name for name in names] + ['unrelated.example']
        rng, cases = random.Random(17), []
        for _ in range(100):
            original = set(rng.sample(pool, rng.randint(1, len(pool))))
            optimized, _ = optimize_rules(original)
            cases.extend([dict(rules=sorted(original), hosts=hosts), dict(rules=sorted(optimized), hosts=hosts)])
        results = self.match_cases(cases)
        for i in range(0, len(results), 2):
            self.assertEqual(results[i], results[i+1], cases[i])
