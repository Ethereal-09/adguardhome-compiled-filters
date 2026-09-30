"""Resolve only explicit GitHub provenance and verify repository/file availability."""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from update_rules import ROOT, fetch, parse_line, UNSUPPORTED


def get_json(url):
    with urlopen(Request(url, headers={'User-Agent': 'PersonalDNSRules/2.0'}), timeout=25) as response:
        return json.load(response)


def decode_github(url):
    parsed = urlparse(url)
    parts = parsed.path.strip('/').split('/')
    if parsed.hostname == 'raw.githubusercontent.com' and len(parts) >= 4:
        return '/'.join(parts[:2]), parts[2], '/'.join(parts[3:])
    if parsed.hostname and parsed.hostname.endswith('jsdelivr.net') and len(parts) >= 4 and parts[0] == 'gh':
        repo, separator, ref = parts[2].partition('@')
        if separator:
            return parts[1] + '/' + repo, ref, '/'.join(parts[3:])
    return None


def main():
    catalog = json.loads((ROOT / 'catalog/sources.json').read_text(encoding='utf-8'))['sources']
    primary = [s for s in catalog if any(o['role'] in ('原始订阅', '订阅', '主订阅', '备用订阅') for o in s['occurrences'])]
    records, candidates = [], []
    for source in primary:
        record = dict(names=source['names'], suppliedUrl=source['url'], status='skipped', evidence=[])
        records.append(record)
        decoded = decode_github(source['url'])
        if not decoded:
            record['reason'] = '非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过'
            continue
        repo, ref, path = decoded
        if repo.lower() == 'adguardteam/hostlistsregistry':
            evidence = f'https://raw.githubusercontent.com/{repo}/{ref}/{path.rsplit("/", 1)[0]}/configuration.json'
            try:
                data = get_json(evidence)
                origins = data.get('sources', [])
                if len(origins) != 1:
                    raise ValueError('配置没有唯一直接上游，无法确定单一原仓库订阅')
                record['evidence'].append(dict(url=evidence, upstreamUrl=origins[0]['source']))
                decoded = decode_github(origins[0]['source'])
                if not decoded:
                    raise ValueError('仓库记录的上游不是 GitHub 原始链接，按要求跳过')
                repo, ref, path = decoded
            except Exception as error:
                record['reason'] = str(error)
                continue
        candidates.append((record, repo, ref, path))
    repositories = {}
    for repo in dict.fromkeys(c[1] for c in candidates):
        try:
            data = get_json(f'https://api.github.com/repos/{repo}')
            repositories[repo] = data
        except Exception as error:
            repositories[repo] = dict(error=str(error))
        print(f'Repository: {repo}', flush=True)

    def verify(candidate):
        record, repo, ref, path = candidate
        data = repositories[repo]
        try:
            if 'error' in data:
                raise ValueError('仓库核验失败：' + data['error'])
            if data.get('fork'):
                raise ValueError('该仓库为 fork，不当作原始仓库；未猜测父仓库中的对应规则')
            canonical = data['full_name']
            record['evidence'].append(dict(url=f'https://api.github.com/repos/{repo}', canonicalRepository=data['html_url'], fork=data['fork'], archived=data['archived']))
            if ref == 'latest':
                # latest is a jsDelivr selector, not a verified Git ref.
                ref = data['default_branch']
                record['evidence'].append(dict(resolution='使用 GitHub API 返回的默认分支，并验证相同文件路径', branch=ref))
            raw = f'https://raw.githubusercontent.com/{canonical}/{ref}/{path}'
            body = fetch(raw, 30, 1)
            supported = set()
            for line in body.splitlines():
                supported.update(rule for rule in parse_line(line) if rule != UNSUPPORTED)
            if not supported:
                raise ValueError('文件可下载，但没有当前程序支持的 DNS 规则')
            record.update(status='verified', repository=data['html_url'], subscriptionUrl=raw,
                          supportedRules=len(supported), archived=data['archived'])
        except Exception as error:
            record['reason'] = str(error)
        print(f"{record['names'][0]}: {record['status']}", flush=True)

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(verify, candidates))
    verified = {}
    for record in records:
        if record['status'] == 'verified':
            verified.setdefault(record['subscriptionUrl'], record)
    output = ROOT / 'github_sources'
    output.mkdir(exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(dict(checkedUtc=datetime.now(timezone.utc).isoformat(), records=records), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'subscription_links.txt').write_text('\n'.join(verified) + '\n', encoding='utf-8')
    config = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
    config['sources'] = [dict(name=r['names'][0], url=url, enabled=True,
                              minimumRules=max(1, int(r['supportedRules'] * .5)), repository=r['repository'])
                         for url, r in verified.items()]
    (output / 'config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = ['# GitHub 原仓库订阅核验', '',
            '仅从用户链接和仓库明确的配置解析地址。GitHub API 核验仓库，实际下载核验文件。fork、非 GitHub 来源和失败链接跳过；不猜替代路径。', '',
            '“原仓库”指直接规则项目，项目自身也可能整合其他上游；不声称仓库所属账号是全部规则的原创作者。', '',
            'CDN 的 latest 通过仓库默认分支解析，相同路径实际下载成功才接受。不同版本各自保留。', '',
            '配置与现有 config.json 分开，保留核验记录；运行：', '',
            '```powershell', '.\\.venv\\Scripts\\python.exe update_rules.py --config github_sources/config.json --output github_sources/dist', '```', '',
            f'确认后按订阅 URL 去重：{len(verified)} 个链接。', '',
            '| 名称 | 原仓库 | 已验证订阅 | 支持的 DNS 规则数 |', '| --- | --- | --- | ---: |']
    for url, r in verified.items():
        rows.append(f"| {r['names'][0]} | [仓库]({r['repository']}) | [订阅]({url}) | {r['supportedRules']} |")
    rows += ['', '## 跳过记录', '', '| 名称 | 用户链接 | 原因 |', '| --- | --- | --- |']
    for r in records:
        if r['status'] != 'verified':
            reason = r['reason'].replace('|', '\\|').replace('\n', ' ')
            rows.append(f"| {r['names'][0]} | [链接]({r['suppliedUrl']}) | {reason} |")
    (output / 'README.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    print(f'VERIFIED {len(verified)} unique subscriptions; SKIPPED {sum(r["status"] != "verified" for r in records)} inputs', flush=True)


if __name__ == '__main__':
    main()
