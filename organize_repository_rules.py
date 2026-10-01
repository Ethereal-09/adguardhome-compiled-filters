"""Build an evidence-backed source registry and keep DNS blocks/exceptions per source."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlparse

from update_rules import ROOT, UNSUPPORTED, atomic_write, fetch, parse_line
from verify_github_sources import get_json, decode_github

OUTPUT = ROOT / 'registry'
CATEGORIES = {
    'ads': '广告', 'tracking': '跟踪/遥测', 'security': '安全综合',
    'malware': '恶意软件', 'phishing': '钓鱼', 'scam': '诈骗',
    'ransomware': '勒索软件', 'mining': '挖矿', 'annoyance': '网页干扰',
    'video': '视频场景', 'smart_tv': '电视', 'game_console': '游戏机',
    'windows': 'Windows', 'xiaomi': '小米', 'samsung': '三星',
    'spotify': 'Spotify', 'youtube': 'YouTube', 'social_blocking': '社交平台整站限制',
    'shortener_blocking': '短链接服务限制', 'dyndns_blocking': '动态 DNS 服务限制',
    'hosting_blocking': '托管服务限制', 'referral_allow': '推广/跳转链接放行',
    'shortener_allow': '短链接放行', 'unknown': '未明确用途',
    'tld_blocking': '高滥用顶级域名限制', 'native_tracking': '设备原生遥测',
    'compatibility': '浏览器兼容修复', 'compatibility_allow': '兼容放行',
}
STRENGTHS = {
    'unknown': '上游未明确分级', 'balanced': '均衡', 'extended': '扩展',
    'aggressive': '激进', 'maximum': '最强', 'specialized': '专项，不按通用强度排序',
    'allow_only': '放行，不适用拦截强度',
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def stable_id(url):
    repo, _, path = decode_github(url)
    label = re.sub(r'[^a-z0-9]+', '-', (repo + '-' + path).lower()).strip('-')
    return label + '-' + hashlib.sha256(url.encode()).hexdigest()[:8]


def describe(repo, path, evidence):
    """Curated classifications, explicitly distinguishing upstream docs from inference."""
    filename = path.rsplit('/', 1)[-1]
    result = dict(categories=['unknown'], categoryBasis='unclassified',
                  strength=dict(value='unknown', basis='not_declared', evidenceUrl=None),
                  regionalFocus=dict(value='unknown', basis='not_assessed', evidenceUrl=None),
                  variantFamily=None, representationGroup=None, notes=[], lifecycle='not_assessed',
                  categoryEvidence=evidence)

    def tags(*values, basis='repository_documentation', url=None):
        result['categories'] = list(values)
        result['categoryBasis'] = basis
        result['categoryEvidence'] = url or repo + '#readme'

    if repo == 'https://github.com/Cats-Team/AdRules' and path == 'dns.txt':
        tags('ads', 'tracking', 'security')
        result['regionalFocus'] = dict(value='CN', basis='repository_documentation',
            evidenceUrl=repo + '#readme', sourceEvidence=evidence, evidenceReviewedOn='2026-10-01',
            scope='dns', description='上游明确面向中国地区，覆盖广告、跟踪、恶意软件、HTTPDNS 和 PCDN。')
        result['notes'].append('国内优化描述使用环境；不按 .cn 后缀或域名解析 IP 所在地筛选，不代表低误杀或特定拦截强度。')
    elif repo.endswith('/hagezi/dns-blocklists'):
        if filename.startswith('whitelist-'):
            tags('shortener_allow' if 'urlshortener' in filename else 'referral_allow',
                 basis='source_header', url=evidence)
            result['strength'] = dict(value='allow_only', basis='source_header', evidenceUrl=evidence)
            result['variantFamily'] = 'hagezi-referral-allow' if 'referral' in filename else None
            result['notes'].append('独立放行组件，按需求选择；与拦截档位分开配置。')
        elif filename in ('multi.txt', 'pro.txt', 'pro.mini.txt', 'pro.plus.txt', 'ultimate.txt'):
            tags('ads', 'tracking', 'security')
            strength = {'multi.txt': 'balanced', 'pro.txt': 'extended', 'pro.mini.txt': 'extended',
                        'pro.plus.txt': 'aggressive', 'ultimate.txt': 'maximum'}[filename]
            result['strength'] = dict(value=strength, basis='upstream_tier', evidenceUrl=repo + '#readme')
            result['variantFamily'] = 'hagezi-multi'
            if filename == 'pro.mini.txt':
                result['notes'].append('Pro 的体积优化版本，不将 Mini 名称当作低强度证据。')
        else:
            tags({'hoster.txt': 'hosting_blocking', 'dyndns.txt': 'dyndns_blocking',
                  'urlshortener.txt': 'shortener_blocking'}.get(filename, 'unknown'))
            result['strength'] = dict(value='specialized', basis='upstream_scope', evidenceUrl=repo + '#readme')
            result['notes'].append('服务类别拦截组件，应与通用广告过滤分开。')
    elif repo.endswith('/badmojr/1Hosts'):
        tags('ads', 'tracking', 'security')
        value = 'balanced' if path.startswith('Lite/') else 'aggressive'
        result['strength'] = dict(value=value, basis='upstream_tier', evidenceUrl=repo + '#readme')
        result['variantFamily'] = '1hosts'
    elif repo.endswith('/blocklistproject/Lists'):
        category = {'ads': 'ads', 'tracking': 'tracking', 'crypto': 'mining', 'fraud': 'scam',
                    'scam': 'scam', 'abuse': 'security', 'ransomware': 'ransomware',
                    'redirect': 'security', 'smart-tv': 'smart_tv', 'phishing': 'phishing'}
        tags(category.get(filename.removesuffix('-ags.txt'), 'unknown'))
    elif repo.endswith('/anudeepND/blacklist'):
        if filename == 'facebook.txt':
            tags('social_blocking')
            result['notes'].append('Facebook 相关域名的整站限制，不作为普通跟踪过滤。')
        elif filename == 'CoinMiner.txt':
            tags('mining')
            result['lifecycle'] = 'discontinued_by_upstream'
            result['notes'].append('上游 README 标注该文件停止更新；可下载不等于持续维护。')
        else:
            tags('ads', 'tracking', 'security')
    elif repo.endswith('/jerryn70/GoodbyeAds'):
        tags('ads', 'tracking', 'security')
        if filename in ('GoodbyeAds.txt', 'GoodbyeAds-AdBlock-Filter.txt'):
            result['representationGroup'] = 'goodbyeads-main'
        else:
            result['notes'].append('用途按上游文件名识别；下载成功不证明应用去广告有效。')
            tags(next((category for token, category in [('Xiaomi', 'xiaomi'), ('Samsung', 'samsung'),
                 ('Spotify', 'spotify'), ('YouTube', 'youtube')] if token in filename), 'unknown'),
                 basis='filename_inference', url=evidence)
            if 'YouTube' in filename:
                result['representationGroup'] = 'goodbyeads-youtube'
    else:
        known = {
            'https://github.com/AdguardTeam/FiltersRegistry': ['ads'],
            'https://github.com/AdguardTeam/AdguardFilters': ['ads'],
            'https://github.com/Cats-Team/AdRules': ['ads', 'tracking'],
            'https://github.com/cjx82630/cjxlist': ['annoyance'],
            'https://github.com/xinggsf/Adblock-Plus-Rule': ['video'],
            'https://github.com/damengzhu/banad': ['ads'],
            'https://github.com/TG-Twilight/AWAvenue-Ads-Rule': ['ads', 'tracking'],
            'https://github.com/StevenBlack/hosts': ['ads', 'tracking', 'security'],
            'https://github.com/banbendalao/ADgk': ['ads'],
            'https://github.com/jdlingyu/ad-wars': ['ads'],
            'https://github.com/AdAway/adaway.github.io': ['ads'],
            'https://github.com/Perflyst/PiHoleBlocklist': ['smart_tv'],
            'https://github.com/durablenapkin/scamblocklist': ['scam'],
            'https://github.com/DandelionSprout/adfilt': ['game_console'],
            'https://github.com/hoshsadiq/adblock-nocoin-list': ['mining'],
            'https://github.com/Spam404/lists': ['security'],
            'https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites': ['malware'],
            'https://github.com/crazy-max/WindowsSpyBlocker': ['windows', 'tracking'],
        }
        if repo in known:
            # Older sources have not all had their README content assessed in this run.
            tags(*known[repo], basis='source_name_inference', url=evidence)
    return result


def load_sources():
    reviewed_path = ROOT / 'registry/reviewed_sources.json'
    if reviewed_path.exists():
        reviewed = json.loads(reviewed_path.read_text(encoding='utf-8'))
        return reviewed['sources'], reviewed.get('unresolvedLinks', [])
    config = read('config.json')
    enabled = {s['url']: s.get('enabled', False) for s in config['sources']}
    items = {}
    skipped = []
    audits = [read('github_sources/audit.json'), read('new_sources/audit.json')]
    for audit in audits:
        for record in audit.get('records', audit.get('results', [])):
            if record['status'] != 'verified':
                url = record.get('suppliedUrl', record.get('url'))
                # Discovery accidentally considered image links; exclude non-rule artifacts.
                if url and not url.lower().endswith(('.png', '.jpeg', '.jpg', '.svg')):
                    skipped.append(dict(name=record.get('name', ' / '.join(record.get('names', []))),
                                        url=url, reason=record.get('reason'),
                                        previousCheckedUtc=audit.get('checkedUtc')))
                continue
            url = record.get('subscriptionUrl', record.get('url'))
            if url in items:
                continue
            repo, ref, path = decode_github(url)
            repository = record['repository']
            blob = f'{repository}/blob/{ref}/{path}'
            items[url] = dict(id=stable_id(url), name=record.get('name', record.get('names', [''])[0]),
                              repository=repository, repositoryAccount=repo.split('/')[0], ref=ref,
                              path=path, url=url, role='filter', enabledInCurrentConfig=enabled.get(url, False),
                              subscriptionEvidence=record.get('evidence', blob),
                              previousCheckedUtc=audit.get('checkedUtc'),
                              previousSupportedRules=record.get('supportedRules'),
                              **describe(repository, path, blob))
    return list(items.values()), skipped


def discover_allowlists(sources):
    """Inventory allow/exclusion paths. Only identified published allowlists are imported."""
    repositories = {}
    for source in sources:
        repositories.setdefault(source['repository'], source['ref'])
    findings, extra = [], []

    def scan(pair):
        repository, ref = pair
        repo = repository.removeprefix('https://github.com/')
        evidence = f'https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1'
        try:
            tree = get_json(evidence)
            paths = [entry['path'] for entry in tree.get('tree', []) if entry['type'] == 'blob'
                     and any(word in entry['path'].lower() for word in ('whitelist', 'allowlist', 'exceptions'))
                     and not any(word in entry['path'].lower() for word in ('__pycache__', 'issue_template', 'test'))]
            finding = dict(repository=repository, evidence=evidence, status='checked',
                           complete=not tree.get('truncated', False), candidatePaths=paths,
                           interpretation='候选路径不自动等于独立白名单，内部代码/样例不作为订阅。')
            new_sources = []
            if repo == 'hagezi/dns-blocklists':
                for path in ('adblock/whitelist-referral.txt', 'adblock/whitelist-referral-native.txt',
                             'adblock/whitelist-urlshortener.txt'):
                    if path not in paths:
                        continue
                    url = f'https://raw.githubusercontent.com/{repo}/{ref}/{path}'
                    blob = f'{repository}/blob/{ref}/{path}'
                    new_sources.append(dict(id=stable_id(url), name='HaGeZi / ' + path.rsplit('/', 1)[-1],
                        repository=repository, repositoryAccount='hagezi', ref=ref, path=path, url=url,
                        role='independent_allowlist', enabledInCurrentConfig=False,
                        subscriptionEvidence=evidence, **describe(repository, path, blob)))
            return finding, new_sources
        except Exception as error:
            return dict(repository=repository, evidence=evidence, status='failed', error=str(error)), []

    with ThreadPoolExecutor(max_workers=3) as pool:
        for finding, additions in pool.map(scan, repositories.items()):
            findings.append(finding)
            extra.extend(additions)
            print('Allowlist inventory:', finding['repository'], finding['status'], flush=True)
    return findings, extra


def split_rules(body, role='filter'):
    blocks, exceptions, unsupported = set(), set(), 0
    original = Counter()
    examples = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith(('!', '[Adblock')):
            continue
        if line.startswith('#') and not line.startswith(('##', '#@#', '#?#', '#$#', '#@$#')):
            continue
        is_exception = line.startswith('@@') or any(token in line for token in ('#@#', '#@?#', '#@$#'))
        original['exceptionLines' if is_exception else 'blockingOrOtherLines'] += 1
        if line.startswith(('@@||', '||')):
            original['adblockLines'] += 1
        elif re.match(r'^(?:0\.0\.0\.0|127\.0\.0\.1|::|::1)\s+', line):
            original['hostsLines'] += 1
        elif line.startswith(('http://', 'https://')):
            original['urlLines'] += 1
        else:
            original['otherLines'] += 1
        parsed = parse_line(line)
        if not parsed:
            # Global cosmetic rules starting with # are not comments here.
            parsed = [UNSUPPORTED]
        for rule in parsed:
            if rule == UNSUPPORTED:
                unsupported += 1
                if len(examples) < 3:
                    examples.append(line[:120])
            elif rule.startswith('@@'):
                exceptions.add(rule)
            else:
                blocks.add(rule)
    if role == 'independent_allowlist' and (blocks or not exceptions or original['blockingOrOtherLines']):
        raise ValueError('预期纯放行订阅，但内容不满足条件；不自动把域名或拦截条目转成放行。')
    return blocks, exceptions, dict(original), unsupported, examples


def inspect_source(source):
    result = dict(source)
    try:
        body = fetch(source['url'], 35, 2)
        blocks, exceptions, raw, unsupported, examples = split_rules(body, source['role'])
        if not blocks and not exceptions:
            raise ValueError('没有当前程序支持的 DNS 规则')
        folder = OUTPUT / 'sources' / source['id']
        folder.mkdir(parents=True, exist_ok=True)
        outputs = {}
        for key, rules in [('blacklist', blocks), ('whitelist', exceptions)]:
            path = folder / (key + '.txt')
            header = [f"! Source: {source['url']}", f"! Repository: {source['repository']}",
                      '! DNS subset only; original modifiers and source scope are preserved.']
            atomic_write(path, '\n'.join(header + sorted(rules)) + '\n')
            outputs[key] = str(path.relative_to(OUTPUT)).replace('\\', '/')
        result.update(status='checked', checkedUtc=datetime.now(timezone.utc).isoformat(),
                      bodySha256=hashlib.sha256(body.encode()).hexdigest(), rawCounts=raw,
                      dnsBlocks=len(blocks), dnsExceptions=len(exceptions), unsupported=unsupported,
                      unsupportedExamples=examples, outputs=outputs,
                      compatibility='dns_subset' if unsupported else 'supported_dns_syntax')
        result['kind'] = ('independent_allowlist' if source['role'] == 'independent_allowlist' else
                          'mixed_filter' if raw.get('exceptionLines', 0) else 'blocklist')
        if raw.get('urlLines', 0):
            result['notes'] = result['notes'] + ['存在 URL 条目，只提取 DNS 子集；不能视为完整 URL 过滤。']
    except Exception as error:
        result.update(status='failed', checkedUtc=datetime.now(timezone.utc).isoformat(),
                      error=str(error), outputs={})
    print(f"Source: {source['id']} {result['status']} black={result.get('dnsBlocks', 0)} white={result.get('dnsExceptions', 0)}", flush=True)
    return result


def make_groups(sources):
    checked = [s for s in sources if s['status'] == 'checked' and s.get('eligibleForSubscription', True)]
    groups = []
    for category, label in CATEGORIES.items():
        ids = [s['id'] for s in checked if category in s['categories']]
        if ids:
            groups.append(dict(id='type-' + category, name=label, axis='type', sourceIds=ids,
                               status='catalog_only', strengthGuaranteed=False))
    for value in ('balanced', 'extended', 'aggressive', 'maximum', 'unknown'):
        ids = [s['id'] for s in checked if s['strength']['value'] == value]
        if ids:
            groups.append(dict(id='strength-' + value, name=STRENGTHS[value], axis='strength',
                               sourceIds=ids, status='catalog_only'))
    china_ids = [s['id'] for s in checked if s.get('role') == 'filter'
                 and s.get('regionalFocus', {}).get('value') == 'CN'
                 and s['regionalFocus'].get('basis') == 'repository_documentation'
                 and s['regionalFocus'].get('scope') == 'dns']
    if china_ids:
        groups.append(dict(id='region-china-optimized', name='中国国内优化（黑名单）', axis='region',
            sourceIds=china_ids, status='catalog_only', strengthGuaranteed=False,
            scope='面向中国使用环境的 DNS 拦截来源，不按 .cn 后缀或 IP 所在地筛选。',
            exceptionPolicy='随所选来源携带其原生 DNS 放行例外，不套用全部独立白名单。'))
    return dict(schemaVersion=1, groups=groups, publicationStatus='not_published',
                compositionRules=[
                    '同一 variantFamily 的版本择一，例如 HaGeZi Multi 和 1Hosts。',
                    '同一 representationGroup 的格式择一；格式可改变匹配范围，不能直接视为规则语义相同。',
                    '选择来源时携带该来源的放行例外，保留修饰符，不统一提升 important。',
                    '独立白名单为可选组件，不能默认跨来源覆盖，尤其是推广和短链接放行。',
                    '未分级来源不能直接归入均衡或低误杀档位；小体积不代表低强度。',
                    '用途标签属于整个来源，不是每条域名的类别；综合列表不能按标签切成纯广告列表。',
                    '地域分类与拦截强度独立；中国国内优化只纳入上游明确说明地区用途的 DNS 来源。',
                    '下载失败来源不进入本次可用分类；黑白规则冲突交由 AdGuard 语法优先级处理。',
                ])


def mark_eligibility(source):
    source['eligibleForSubscription'] = source['status'] == 'checked'
    if source['status'] != 'checked':
        return
    source.pop('reviewReason', None)
    previous = source.get('previousSupportedRules')
    current = source['dnsBlocks'] + source['dnsExceptions']
    if previous and current < previous * .7:
        source['eligibleForSubscription'] = False
        source['reviewReason'] = f'支持条目从此前 {previous} 降为 {current}，下降超过 30%，暂不进入分类候选。'
    if source.get('lifecycle') == 'discontinued_by_upstream':
        source['eligibleForSubscription'] = False
        source['reviewReason'] = '上游明确停止更新，保留历史整理，但默认不进入分类候选。'


def write_reports(sources, findings, skipped):
    OUTPUT.mkdir(exist_ok=True)
    for source in sources:
        mark_eligibility(source)
    groups = make_groups(sources)
    repositories = defaultdict(list)
    for source in sources:
        repositories[source['repository']].append(source)
    checked = [s for s in sources if s['status'] == 'checked']
    summary = dict(repositories=len(repositories), sources=len(sources), checked=len(checked),
                   failed=len(sources)-len(checked), independentAllowlists=sum(s['kind']=='independent_allowlist' for s in checked),
                   mixedFilters=sum(s['kind']=='mixed_filter' for s in checked),
                   blocklists=sum(s['kind']=='blocklist' for s in checked),
                   needsReview=sum(not s['eligibleForSubscription'] for s in checked),
                   sourceRuleTotals=dict(black=sum(s['dnsBlocks'] for s in checked),
                                         white=sum(s['dnsExceptions'] for s in checked)))
    repository_inventory = {}
    for repository, items in repositories.items():
        repository_inventory[repository] = dict(repository=repository, role='rule_source',
            sourceIds=[s['id'] for s in items], checkedSources=sum(s['status']=='checked' for s in items))
    for item in skipped:
        decoded = decode_github(item['url']) if item.get('url') else None
        if decoded:
            repository = 'https://github.com/' + decoded[0]
            repository_inventory.setdefault(repository, dict(repository=repository, role='unresolved_source',
                                                              sourceIds=[], checkedSources=0))
    reference_projects = read('catalog/sources.json')['referenceProjects']
    for reference in reference_projects:
        if reference['url'].startswith('https://github.com/'):
            repository_inventory.setdefault(reference['url'], dict(repository=reference['url'],
                role='reference_merger', sourceIds=[], checkedSources=0))
    summary['knownRepositoriesIncludingReferences'] = len(repository_inventory)
    manifest = dict(schemaVersion=1, generatedUtc=datetime.now(timezone.utc).isoformat(), summary=summary,
                    sources=sources, allowlistDiscovery=findings, excludedSources=skipped,
                    repositoryInventory=list(repository_inventory.values()),
                    countNote='规则数量为逐来源相加，含跨源重叠，不是全局去重计数。')
    atomic_write(OUTPUT / 'sources.json', json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    atomic_write(OUTPUT / 'groups.json', json.dumps(groups, ensure_ascii=False, indent=2)+'\n')
    for name, predicate in [('blacklist_links.txt', lambda s:s['role']=='filter'),
                            ('whitelist_links.txt', lambda s:s['role']=='independent_allowlist')]:
        atomic_write(OUTPUT / name, '\n'.join(s['url'] for s in checked if predicate(s))+'\n')
    rows = ['# 全部已整理仓库的黑白名单与分类目录', '',
            f"共 {summary['repositories']} 个已确认规则仓库、{summary['sources']} 个来源/版本，本次成功检查 {summary['checked']} 个，失败 {summary['failed']} 个。",
            f"成功来源包含 {summary['blocklists']} 个拦截列表、{summary['mixedFilters']} 个含放行例外的混合列表、{summary['independentAllowlists']} 个独立白名单。", '',
            f"另有 {summary['needsReview']} 个已下载来源因数量异常或停更标记需要复核，不进入 groups.json 的订阅候选。包含失效来源和参考合并项目，共登记 {len(repository_inventory)} 个已知仓库。", '',
            '范围为此前核验的 27 个订阅和新增的 21 个订阅，按 URL 去重，再补充本次从原仓库确认的独立白名单。不是穷举 GitHub 上全部规则项目。非 GitHub、失败和未支持来源另列于清单中。', '',
            '## 黑名单、白名单与例外', '',
            '- [拦截/混合订阅地址](blacklist_links.txt)：添加为 DNS 黑名单时应保留其原生例外。',
            '- [独立白名单订阅地址](whitelist_links.txt)：上游明确用于放行的文件，按用途选用。',
            '- 每个来源的 `blacklist.txt` 和 `whitelist.txt` 在下面的文件列；混合源的白名单是该来源的 DNS 放行例外。',
            '- 放行例外未转成域名，未删除修饰符，未统一附加 `$important`。不能将所有白名单合并后默认套用到每个档位。',
            '- 此目录保留来源调查快照；实际选源在 [profiles.json](../profiles.json)，分类生成结果见 [dist](../dist/README.md)。', '',
            '## 后续分类订阅', '',
            '[sources.json](sources.json) 是完整来源登记，包含强度、用途、地域、依据、仓库、URL、启用状态、版本族、格式组和调查时的黑白条目统计。[groups.json](groups.json) 是候选来源分组，不能直接合并全部成员；[profiles.json](../profiles.json) 决定实际选源，[build_filters.py](../build_filters.py) 生成分类订阅。组合边界见 [分类说明](CLASSIFICATION.md)。', '',
            '强度只采用已查看的上游档位说明；其余为“上游未明确分级”。用途若来自名称或文件名推断，在 JSON 的 categoryBasis 明确标记。', '',
            '同一来源的不同强度分别保存：HaGeZi Normal / Pro / Pro++ / Ultimate、1Hosts Lite / Xtra 应在对应档位择一。Pro Mini 是 Pro 的体积优化版本。Hosts 精确匹配与 Adblock 子域匹配的范围可能不同，格式差异不作语义去重。', '',
            '用途标签描述来源覆盖范围，不表示其中每条域名都属于该类。综合来源不能仅凭标签生成“纯广告”或“纯跟踪”规则。', '',
            '## 中国国内优化（黑名单）', '',
            '分组标识：`region-china-optimized`。地域维度独立于强度；只选上游明确说明面向中国环境、并提供 DNS 文件的已核验来源。中文名称、仓库语言和 .cn 域名数量不作为地域归类依据。', '',
            '本分类保留上游的广告、跟踪、恶意软件、HTTPDNS、PCDN 等覆盖范围，不按域名后缀或 IP 国家截断规则；强度未明确时仍记为 unknown。生成时携带所选来源的原生例外。', '',
            '| 来源 | 原始订阅 | 归类依据 | 支持的 DNS 拦截条目 |',
            '| --- | --- | --- | ---: |']
    china_group = next((g for g in groups['groups'] if g['id'] == 'region-china-optimized'), None)
    china_ids = set(china_group['sourceIds']) if china_group else set()
    for source in sources:
        if source['id'] in china_ids:
            rows.append(f"| [{source['name']}]({source['repository']}) | [订阅]({source['url']}) | [上游 README]({source['regionalFocus']['evidenceUrl']}) | {source['dnsBlocks']} |")
    if not china_ids:
        rows.append('| 本次没有通过核验的来源 | — | — | — |')
    rows += ['', '独立分类已接入构建程序，输出 [china.txt](../dist/china.txt)。此处计数沿用各来源 checkedUtc 对应的调查快照，最新构建数量见 [dist/manifest.json](../dist/manifest.json)。地域依据核实日期记录在 regionalFocus.evidenceReviewedOn。', '',
             '## 按仓库整理', '']
    for repository, items in sorted(repositories.items()):
        rows += [f'### [{repository.removeprefix("https://github.com/")}]({repository})', '',
                 '| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |',
                 '| --- | --- | --- | ---: | ---: | --- | --- | --- |']
        for s in items:
            category = '、'.join(CATEGORIES[c] for c in s['categories'])
            strength = STRENGTHS[s['strength']['value']]
            if s['status'] != 'checked':
                rows.append(f"| [{s['name']}]({s['url']}) | {category} | {strength} | 未验证 | 未验证 | 失败 | 否 | — |")
            else:
                outputs = s['outputs']
                fmt = '仅支持的 DNS 子集' if s['unsupported'] else '当前 DNS 语法可提取'
                candidate = '可选择，待组合验证' if s['eligibleForSubscription'] else '需复核'
                rows.append(f"| [{s['name']}]({s['url']}) | {category} | {strength} | {s['dnsBlocks']} | {s['dnsExceptions']} | {fmt} | {candidate} | [黑]({outputs['blacklist']}) / [白]({outputs['whitelist']}) |")
        rows.append('')
    rows += ['## 失效来源及参考仓库', '', '| 仓库 | 用途 |', '| --- | --- |']
    for repository, info in sorted(repository_inventory.items()):
        if info['role'] != 'rule_source':
            role = '参考合并项目，不作为原始规则订阅' if info['role']=='reference_merger' else '没有通过核验的可用来源；路径或格式问题见排除记录'
            rows.append(f"| [{repository.removeprefix('https://github.com/')}]({repository}) | {role} |")
    rows += ['', '## 白名单目录调查', '',
             '目录调查只记录实际发现的路径，文件名包含 whitelist 不足以证明它是可订阅白名单。StevenBlack 的 whitelist.example 是本地生成器示例；GoodbyeAds 的 Whitelist/Keep this 是目录占位文件。它们没有加入白名单订阅。', '',
             '| 仓库 | 调查状态 | 候选路径 |', '| --- | --- | --- |']
    for finding in findings:
        paths = '、'.join(finding.get('candidatePaths', [])) or '未发现相关命名文件'
        if finding['status']=='failed':
            paths = finding['error']
        state = '已检查' if finding['status']=='checked' else '未验证'
        if finding.get('complete') is False:
            state += '，目录截断'
        rows.append(f"| [仓库]({finding['repository']}) | {state} | {paths.replace('|', '/')[:800]} |")
    rows += ['', '这是目录与已知文件的检查，不能证明所有项目都不存在其他内部白名单。', '', '## 失败与排除', '']
    for s in sources:
        if s.get('reviewReason'):
            rows.append(f"- [{s['name']}]({s['url']}): {s['reviewReason']}")
    for s in sources:
        if s['status']=='failed':
            rows.append(f"- [{s['name']}]({s['url']}): {s['error']}")
    rows += ['','此前非 GitHub、404、超出大小上限等未通过来源，保留在 sources.json 的 excludedSources，未参与本次规则提取。', '',
             '## 重新整理', '', '```powershell', '.\\.venv\\Scripts\\python.exe -B organize_repository_rules.py', '```', '',
             '读取两份核验清单，重新下载规则并更新此目录；失败的来源不会被记为本次可用。旧快照可能仍在目录内，以 sources.json 的 status 与 outputs 为准。']
    atomic_write(OUTPUT / 'README.md', '\n'.join(rows)+'\n')
    print(json.dumps(summary, ensure_ascii=False), flush=True)


def main():
    if (ROOT / 'registry/reviewed_sources.json').exists():
        from refresh_source_registry import main as refresh_main
        refresh_main()
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-tree-scan', action='store_true', help='Reuse previous allowlist directory scan')
    args = parser.parse_args()
    sources, skipped = load_sources()
    if args.skip_tree_scan and (OUTPUT/'sources.json').exists():
        old = json.loads((OUTPUT/'sources.json').read_text(encoding='utf-8'))
        findings = old['allowlistDiscovery']
        extra = [s for s in old['sources'] if s['role']=='independent_allowlist']
    else:
        findings, extra = discover_allowlists(sources)
    sources.extend(extra)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(inspect_source, sources))
    write_reports(results, findings, skipped)


if __name__=='__main__':
    main()
