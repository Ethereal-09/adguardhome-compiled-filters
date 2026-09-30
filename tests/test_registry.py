import unittest

from organize_repository_rules import describe, load_sources, make_groups, mark_eligibility, split_rules, stable_id


class RegistryTests(unittest.TestCase):
    def test_exception_scope_and_priority_are_preserved(self):
        body = '\n'.join(['||parent.example^', '@@||child.parent.example^',
                          '@@||important.example^$important', '0.0.0.0 exact.example'])
        blocks, allows, counts, unsupported, _ = split_rules(body)
        self.assertEqual(blocks, {'||parent.example^', '|exact.example|'})
        self.assertEqual(allows, {'@@||child.parent.example^', '@@||important.example^$important'})
        self.assertEqual(counts['exceptionLines'], 2)
        self.assertEqual(unsupported, 0)

    def test_browser_and_wildcard_rules_are_reported_as_partial(self):
        blocks, allows, raw, unsupported, _ = split_rules('##.ad\n@@||*.example.com^\n@@||safe.example^')
        self.assertEqual(blocks, set())
        self.assertEqual(allows, {'@@||safe.example^'})
        self.assertEqual(unsupported, 2)
        self.assertEqual(raw['exceptionLines'], 2)

    def test_allowlist_does_not_turn_blocked_domains_into_exceptions(self):
        with self.assertRaises(ValueError):
            split_rules('0.0.0.0 example.com', 'independent_allowlist')
        with self.assertRaises(ValueError):
            split_rules('example.com', 'independent_allowlist')
        blocks, allows, *_ = split_rules('@@||example.com^', 'independent_allowlist')
        self.assertFalse(blocks)
        self.assertEqual(allows, {'@@||example.com^'})

    def test_mini_is_size_optimized_pro_not_light_tier(self):
        meta = describe('https://github.com/hagezi/dns-blocklists', 'adblock/pro.mini.txt', 'evidence')
        self.assertEqual(meta['strength']['value'], 'extended')
        self.assertEqual(meta['variantFamily'], 'hagezi-multi')

    def test_unknown_strength_not_guessed_from_size_or_name(self):
        meta = describe('https://github.com/jerryn70/GoodbyeAds', 'Hosts/GoodbyeAds.txt', 'evidence')
        self.assertEqual(meta['strength']['value'], 'unknown')
        a = stable_id('https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt')
        b = stable_id('https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt')
        self.assertNotEqual(a, b)

    def test_china_focus_requires_explicit_upstream_dns_source(self):
        meta = describe('https://github.com/Cats-Team/AdRules', 'dns.txt', 'verified-dns-file')
        self.assertEqual(meta['regionalFocus']['value'], 'CN')
        self.assertEqual(meta['regionalFocus']['basis'], 'repository_documentation')
        self.assertEqual(meta['strength']['value'], 'unknown')
        for repo, path in [('https://github.com/Cats-Team/AdRules', 'adblock.txt'),
                           ('https://github.com/AdguardTeam/FiltersRegistry', 'filters/filter_224_Chinese/filter.txt'),
                           ('https://github.com/banbendalao/ADgk', 'ADgk.txt')]:
            self.assertEqual(describe(repo, path, 'evidence')['regionalFocus']['value'], 'unknown')

    def test_china_group_excludes_failed_review_allow_and_inferred_sources(self):
        meta = describe('https://github.com/Cats-Team/AdRules', 'dns.txt', 'evidence')
        base = dict(status='checked', role='filter', eligibleForSubscription=True, **meta)
        sources = [dict(base, id='ok'), dict(base, id='failed', status='failed'),
                   dict(base, id='review', eligibleForSubscription=False),
                   dict(base, id='white', role='independent_allowlist'),
                   dict(base, id='inferred', regionalFocus=dict(value='CN', basis='filename_inference', scope='dns'))]
        groups = make_groups(sources)['groups']
        china = next(g for g in groups if g['id'] == 'region-china-optimized')
        self.assertEqual(china['sourceIds'], ['ok'])
        self.assertEqual(china['axis'], 'region')
        self.assertFalse(china['strengthGuaranteed'])
        self.assertEqual(china['status'], 'catalog_only')

    def test_source_lists_deduplicate_and_keep_candidate_enabled_state(self):
        sources, _ = load_sources()
        self.assertEqual(len(sources), len({s['url'] for s in sources}))
        self.assertTrue(sources)
        for source in sources:
            if source['repository'] == 'https://github.com/blocklistproject/Lists':
                self.assertFalse(source['enabledInCurrentConfig'])

    def test_failed_sources_do_not_enter_category_groups(self):
        sources = [dict(id='ok', status='checked', categories=['ads'], strength={'value':'unknown'}),
                   dict(id='bad', status='failed', categories=['ads'], strength={'value':'unknown'})]
        groups = make_groups(sources)['groups']
        self.assertTrue(groups)
        self.assertTrue(all('bad' not in group['sourceIds'] for group in groups))

    def test_count_drop_requires_review_before_profile_selection(self):
        source = dict(id='shrunk', status='checked', categories=['scam'], strength={'value':'unknown'},
                      previousSupportedRules=1000, dnsBlocks=5, dnsExceptions=0)
        mark_eligibility(source)
        self.assertFalse(source['eligibleForSubscription'])
        self.assertFalse(make_groups([source])['groups'])


if __name__ == '__main__':
    unittest.main()
