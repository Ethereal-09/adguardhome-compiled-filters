"""Find additional subscriptions from repository-published links and GitHub directories."""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import quote, unquote

from update_rules import ROOT, fetch, parse_line, UNSUPPORTED
from verify_github_sources import get_json

REPOSITORIES = ['blocklistproject/Lists', 'anudeepND/blacklist', 'crazy-max/WindowsSpyBlocker',
                'jerryn70/GoodbyeAds', 'Perflyst/PiHoleBlocklist', 'DandelionSprout/adfilt']


def main():
    existing = {s['url'] for s in json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))['sources']}
    candidates, skipped = {}, []
    for repo in REPOSITORIES:
        try:
            info = get_json(f'https://api.github.com/repos/{repo}')
            if info['fork'] or info['archived']:
                skipped.append(dict(repository=repo, reason='Fork or archived repository'))
                continue
            branch, canonical = info['default_branch'], info['full_name']
            directory = {'blocklistproject/Lists': 'adguard', 'crazy-max/WindowsSpyBlocker': 'data/hosts'}.get(repo)
            if directory:
                evidence = f'https://api.github.com/repos/{canonical}/contents/{directory}?ref={branch}'
                listing = get_json(evidence)
                wanted = {'ads', 'tracking', 'malware', 'phishing', 'ransomware', 'scam', 'fraud', 'redirect', 'crypto', 'abuse', 'smart-tv'} if repo.startswith('blocklistproject/') else {'spy'}
                urls = [item['download_url'] for item in listing if item['type'] == 'file' and item['name'].removesuffix('.txt').removesuffix('-ags') in wanted]
            else:
                # GitHub API returns actual README path/branch, no guessed rule path.
                meta = get_json(f'https://api.github.com/repos/{canonical}/readme')
                evidence = meta['html_url']
                text = fetch(meta['download_url'], 25, 1)
                urls = re.findall(r'https://raw\.githubusercontent\.com/[^\s<>"\)\]]+', text)
                urls = [u.rstrip('.,;') for u in urls if u.lower().startswith(f'https://raw.githubusercontent.com/{canonical}/'.lower())]
                # Dandelion publishes many browser lists; only explicit DNS/hosts links.
                if repo.startswith('DandelionSprout/'):
                    urls = [u for u in urls if any(key in unquote(u).lower() for key in ('adguardhome', 'dns', 'hosts'))]
            for url in dict.fromkeys(urls):
                if url in existing or len(candidates) >= 40:
                    continue
                candidates[url] = dict(name=canonical + ' / ' + unquote(url.rsplit('/', 1)[-1]),
                                       url=url, repository=info['html_url'], evidence=evidence,
                                       repositoryUpdated=info['pushed_at'])
            print(f'{repo}: {len(urls)} published candidates', flush=True)
        except Exception as error:
            skipped.append(dict(repository=repo, reason=str(error)))

    def inspect(item):
        try:
            body = fetch(item['url'], 30, 1)
            rules, unsupported = set(), 0
            for line in body.splitlines():
                for rule in parse_line(line):
                    if rule == UNSUPPORTED:
                        unsupported += 1
                    else:
                        rules.add(rule)
            if not rules:
                raise ValueError('No supported DNS rules')
            allows = sum(r.startswith('@@') for r in rules)
            return dict(item, status='verified', supportedRules=len(rules), exceptionRules=allows,
                        unsupported=unsupported)
        except Exception as error:
            return dict(item, status='skipped', reason=str(error))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(inspect, candidates.values()))
    verified = [r for r in results if r['status'] == 'verified']
    output = ROOT / 'new_sources'
    output.mkdir(exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(dict(checkedUtc=datetime.now(timezone.utc).isoformat(), results=results, skippedRepositories=skipped), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'subscription_links.txt').write_text('\n'.join(r['url'] for r in verified) + '\n', encoding='utf-8')
    (output / 'config_candidates.json').write_text(json.dumps([dict(name=r['name'], url=r['url'], enabled=False,
        minimumRules=max(1, r['supportedRules']//2), repository=r['repository']) for r in verified], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = ['# 新发现的 GitHub 订阅源', '', f'本次新增验证 {len(verified)} 个订阅地址。按 URL 排除了当前 config.json 中的订阅。', '',
            '只接受仓库 README 明确发布的 Raw 链接或 GitHub API 返回的规则目录文件；跳过 fork 和归档仓库。下载成功及存在支持规则不等于已经验证无误杀；仓库更新时间不等于规则文件更新时间。', '',
            '新增候选配置默认禁用，没有改动现有 config.json。没有把整个含例外的过滤列表当作白名单。', '',
            '| 名称 / 文件 | 订阅 | 仓库证据 | 支持的 DNS 规则 | 放行例外 | 跳过条目 |', '| --- | --- | --- | ---: | ---: | ---: |']
    for r in verified:
        rows.append(f"| [{r['name']}]({r['repository']}) | [Raw]({r['url']}) | [证据]({r['evidence']}) | {r['supportedRules']} | {r['exceptionRules']} | {r['unsupported']} |")
    rows += ['', '## 文件', '', '- [新增订阅地址](subscription_links.txt)', '- [候选配置条目](config_candidates.json)', '- [核验与跳过记录](audit.json)', '',
             '不同分类列表可能相互重叠；例如 crypto 主要针对加密挖矿，smart-tv 针对电视设备。使用前按需求选择分类。上游许可及贡献者信息以各仓库说明为准。', '', '## 跳过记录', '']
    for r in results:
        if r['status'] == 'skipped':
            rows.append(f"- [{r['name']}]({r['url']}): {r['reason']}")
    for r in skipped:
        rows.append(f"- {r['repository']}: {r['reason']}")
    (output / 'README.md').write_text('\n'.join(rows)+'\n', encoding='utf-8')
    print(f'VERIFIED {len(verified)} new subscriptions', flush=True)


if __name__ == '__main__':
    main()
