"""Update README subscriptions, build status and the Actions run summary."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re

from dns_utils import atomic_write

BUILD_START = '<!-- build-status:start -->'
BUILD_END = '<!-- build-status:end -->'
SUBSCRIPTIONS_START = '<!-- subscriptions:start -->'
SUBSCRIPTIONS_END = '<!-- subscriptions:end -->'
UPSTREAM_START = '<!-- upstream:start -->'
UPSTREAM_END = '<!-- upstream:end -->'
MIHOMO_START = '<!-- mihomo:start -->'
MIHOMO_END = '<!-- mihomo:end -->'
DEFAULT_REPOSITORY = 'Ethereal-09/adguardhome-compiled-filters'
SUBSCRIPTION_ACCELERATORS = (('Boki', 'https://github.boki.moe/'),
                            ('GHFast', 'https://ghfast.top/'))


def replace_block(text, start, end, content):
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f'README must contain exactly one ordered block: {start}')
    return re.sub(re.escape(start) + r'.*?' + re.escape(end),
                  lambda _: start + '\n' + content.rstrip() + '\n' + end, text, flags=re.DOTALL)


def publication_blocks(config, manifest, registry, repository, allow_retained=False):
    """Describe the validated output; never use historical registry rule counts."""
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Invalid README repository')
    profiles = [p for p in config['profiles'] if p.get('enabled', False)]
    sources = {s['id']: s for s in registry['sources']}
    selected = set()
    groups = {name: [] for name in ('基础订阅', '强度档位', '用途分类', '设备与服务限制', '独立白名单')}
    labels = {'combined': '国内精简（推荐）', 'full': '中文源全量（按需）', 'china': '国内增强',
              'balanced': 'HaGeZi 均衡 · Normal', 'extended': 'HaGeZi 扩展 · Pro',
              'aggressive': 'HaGeZi 激进 · Pro++', 'maximum': 'HaGeZi 最强 · Ultimate',
              'balanced-1hosts': '1Hosts 均衡 · Lite', 'aggressive-1hosts': '1Hosts 激进 · Xtra'}
    scopes = {'combined': '国内 Lite + 秋风纯广告', 'china': '增加隐私与国内 DNS 合集',
              'full': '当前入选中文/中国地区来源'}
    for profile in profiles:
        pid = profile['id']
        item = manifest['profiles'][pid]
        if not allow_retained and (item['status'] != 'ready' or item['sourceIds'] != profile['sourceIds']):
            raise ValueError('README counts require ready outputs with matching sources: ' + pid)
        if item['status'] == 'failed':
            continue
        count = item['totalRules']
        if type(count) is not int or count < 1 or count != item['blockingRules'] + item['exceptionRules']:
            raise ValueError('Invalid README rule count: ' + pid)
        selected.update(item['sourceIds'])
        if profile['kind'] == 'allowlist':
            group = '独立白名单'
        elif profile['axis'] in ('composition', 'region'):
            group = '基础订阅'
        elif profile['axis'] == 'strength':
            group = '强度档位'
        elif profile.get('optionalComponent'):
            group = '设备与服务限制'
        else:
            group = '用途分类'
        label = labels.get(pid, profile['name']).replace('|', r'\|').replace('\n', ' ')
        if item['status'] == 'retained':
            label += '（保留旧版）'
        filename = 'adguard.txt' if pid == config['defaultProfile'] else pid + '.txt'
        url = f'https://raw.githubusercontent.com/{repository}/main/dist/{filename}'
        links = ' | '.join([f'[原始]({url})',
                            *(f'[{name}]({prefix}{url})' for name, prefix in SUBSCRIPTION_ACCELERATORS)])
        scope = f" {scopes.get(pid, '按需选用')} |" if group == '基础订阅' else ''
        row = f'| {label} | {count:,} |{scope} {links} |'
        groups[group].append((pid, row))

    rows = ['## AdGuard Home 订阅', '',
            '在 AdGuard Home → **过滤器 → DNS 黑名单**添加，三档任选一个。日常推荐国内精简；增强与全量版覆盖更广，仍可能影响正常功能。', '']
    notes = {'强度档位': '任选一个档位；1Hosts 可作为替代。',
             '用途分类': '按用途单独使用或搭配基础订阅，添加到 DNS 黑名单。',
             '设备与服务限制': '添加到 DNS 黑名单；整站或服务限制可能影响正常功能。',
             '独立白名单': '添加到 **DNS 白名单**，按用途选择。'}
    extra_count = sum(len(entries) for group, entries in groups.items() if group != '基础订阅')
    folded = False
    for group, entries in groups.items():
        if not entries:
            continue
        if group == '基础订阅':
            order = {'combined': 0, 'china': 1, 'full': 2}
            entries.sort(key=lambda entry: order.get(entry[0], 3))
            rows += ['| 规则 | 规则数 | 适用范围 | 原始链接 | 加速1 | 加速2 |',
                     '| --- | ---: | --- | --- | --- | --- |',
                     *(row for _, row in entries), '']
            rows += ['每条规则的三个链接任选一个订阅。数量随成功构建更新，含原生放行例外；每个订阅独立去重。', '']
        else:
            if not folded:
                rows += ['<details>',
                         f'<summary>其他分类订阅（{extra_count} 项）：强度、用途、设备与白名单</summary>', '']
                folded = True
            rows += ['### ' + group, '', notes[group], '',
                     '| 规则 | 规则数 | 原始链接 | 加速1 | 加速2 |',
                     '| --- | ---: | --- | --- | --- |',
                     *(row for _, row in entries), '']
    if folded:
        rows += ['</details>', '']
    custom_profiles = [labels.get(p['id'], p['name']) for p in profiles if p.get('includeCustom')]
    rows += ['三档均保留原生放行例外并应用个人规则；中文文档不代表只包含中国域名。', '']

    repositories = {sources[sid]['repository'] for sid in selected}
    github = sum(repo.startswith('https://github.com/') for repo in repositories)
    external = len(repositories) - github
    origins = f'**{github} 个 GitHub 原仓库**' + (f'及 **{external} 个官方站点**' if external else '')
    upstream = [f'当前选用 **{len(selected)} 个来源文件**，来自 {origins}。', '',
                '<details>', '<summary>查看上游作者、原始订阅与规则数量</summary>', '',
                '数量为来源合并前的支持条目数。仓库账号不代表全部原创作者，完整署名以各上游说明为准。', '',
                '| 维护账号 / 原始项目 | 原始规则文件 | 支持规则数 |', '| --- | --- | ---: |']
    for sid in sorted(selected, key=lambda sid: (sources[sid]['repository'].lower(), sources[sid]['path'])):
        source, stats = sources[sid], manifest['sources'][sid]
        if not allow_retained and (stats.get('url') != source['url'] or type(stats.get('accepted')) is not int or stats['accepted'] < 1):
            raise ValueError('Invalid README upstream count or identity: ' + sid)
        repo = source['repository']
        name = repo.removeprefix('https://github.com/') if repo.startswith('https://github.com/') else source['repositoryAccount']
        filename = source['path'].replace('|', r'\|')
        count_text = f"{stats['accepted']:,}" if type(stats.get('accepted')) is int else '本次未获取'
        upstream.append(f"| [{name}]({repo}) | [{filename}]({source['url']}) | {count_text} |")
    upstream += ['', '</details>', '',
                 '[来源登记](registry/README.md) · [上游许可与署名](upstream/README.md)；合并产物遵循各上游许可。']
    return '\n'.join(rows), '\n'.join(upstream)


def update_readme(path, run, build_outcome=None, audit_outcome=None, *,
                  config=None, manifest=None, registry=None, repository=DEFAULT_REPOSITORY,
                  mihomo_manifest=None, publication=None):
    """Refresh counts only after successful publication validation; preserve them on failure."""
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    if publication is not None:
        checked = datetime.fromisoformat(publication['checkedUtc']).astimezone(timezone(timedelta(hours=8)))
        published = publication.get('publishedUtc')
        block = []
        if published:
            stamp = datetime.fromisoformat(published).astimezone(timezone(timedelta(hours=8)))
            block += [f'> 最近成功发布：**{stamp:%Y-%m-%d %H:%M:%S}（北京时间）**', '>']
        state = {'success': '全部通过校验', 'partial': '部分更新，失败分类保留旧版', 'failed': '本次失败，保留旧版'}[publication['status']]
        block += [f'> 最近检查：{checked:%Y-%m-%d %H:%M:%S} · **{state}**', '>',
                  f'> 本次通过：AdGuard Home {len(publication["dnsValidated"])} / mihomo {len(publication["mihomoValidated"])} · [变化与失败详情](dist/publication.json)']
        cached = len(run.get('cacheSources', []))
        if cached:
            block[-1] += f' · 缓存来源 {cached}'
        updated = replace_block(text, BUILD_START, BUILD_END, '\n'.join(block))
        subscriptions, upstream = publication_blocks(config, manifest, registry, repository, allow_retained=True)
        updated = replace_block(updated, SUBSCRIPTIONS_START, SUBSCRIPTIONS_END, subscriptions)
        updated = replace_block(updated, UPSTREAM_START, UPSTREAM_END, upstream)
        if MIHOMO_START in updated:
            updated = replace_block(updated, MIHOMO_START, MIHOMO_END,
                                    mihomo_content(manifest, mihomo_manifest, repository, allow_stale=True))
        if updated != text:
            atomic_write(path, updated)
        return
    stamp = datetime.fromisoformat(run['checkedUtc']).astimezone(timezone(timedelta(hours=8)))
    failed = run.get('status') == 'failed' or run.get('failedProfiles') or run.get('error')
    if build_outcome in ('failure', 'cancelled') or failed:
        state = '构建失败'
    elif audit_outcome == 'failure':
        state = '发布校验失败，订阅保留旧版'
    elif audit_outcome == 'success':
        state = '成功，已通过发布校验'
    else:
        state = '构建成功'
    details = []
    if run.get('profileCount'):
        ready = run['profileCount'] - len(run.get('failedProfiles', []))
        details.append(f"分类 {ready}/{run['profileCount']}")
    sources = run.get('sources', {})
    if sources:
        fresh = sum(item['status'] == 'fresh' for item in sources.values())
        cached = sum(item['status'] == 'cached' for item in sources.values())
        source_failed = sum(item['status'] == 'failed' for item in sources.values())
        details.append(f'来源：新下载 {fresh}，缓存 {cached}，失败 {source_failed}')
    block = [f"> 最近构建：**{stamp:%Y-%m-%d %H:%M:%S}（北京时间）**", '>',
             '> 状态：**' + state + '**' + (' · ' + ' · '.join(details) if details else '')]
    if failed or audit_outcome == 'failure' or build_outcome == 'failure':
        previous_publication = re.search(r'^> 最近成功发布：.*$', text, flags=re.MULTILINE)
        if previous_publication:
            block = [previous_publication[0], '>'] + block
    updated = replace_block(text, BUILD_START, BUILD_END, '\n'.join(block))
    if not failed and build_outcome == 'success' and audit_outcome == 'success' and manifest is not None:
        subscriptions, upstream = publication_blocks(config, manifest, registry, repository)
        updated = replace_block(updated, SUBSCRIPTIONS_START, SUBSCRIPTIONS_END, subscriptions)
        updated = replace_block(updated, UPSTREAM_START, UPSTREAM_END, upstream)
        if MIHOMO_START in updated and mihomo_manifest is not None:
            updated = replace_block(updated, MIHOMO_START, MIHOMO_END,
                                    mihomo_content(manifest, mihomo_manifest, repository))
    if updated != text:
        atomic_write(path, updated)


def mihomo_content(dns_manifest, manifest, repository, allow_stale=False):
    profiles = manifest['profiles']
    if not allow_stale and set(profiles) != set(dns_manifest['profiles']):
        raise ValueError('mihomo profiles differ from DNS publication')
    for pid, item in profiles.items():
        dns_item = dns_manifest['profiles'][pid]
        may_retain = allow_stale and item.get('status') == 'retained'
        if not may_retain and item['inputSha256'] != dns_item['fileSha256']:
            raise ValueError('mihomo input checksum differs from DNS publication: ' + pid)
        if not may_retain and any(item[field] != dns_item[field] for field in ('blockingRules', 'exceptionRules')):
            raise ValueError('mihomo counts differ from DNS publication: ' + pid)
    rows = ['## mihomo 订阅', '',
            '使用 **MRS 域名集 + 配套正则与例外**；[配置合并方法](dist/mihomo/README.md)。旧配置需重新合并一次新版片段，此后规则集按日刷新。', '',
            '| 分类 | 拦截条目 | 例外条目 | 原始配置 | Boki 配置 | GHFast 配置 |',
            '| --- | ---: | ---: | --- | --- | --- |']
    def row(pid, item):
        label = {'combined': '国内精简', 'china': '国内增强', 'full': '中文源全量'}.get(pid, item['name']).replace('|', r'\|')
        if item.get('status') == 'retained':
            label += '（保留旧版）'
        if item['inputSha256'] != dns_manifest['profiles'][pid].get('fileSha256'):
            label += '（与 DNS 版本不同）'
        base = f'https://raw.githubusercontent.com/{repository}/main/dist/mihomo/{pid}'
        return (f'| {label} | {item["blockingRules"]:,} | {item["exceptionRules"]:,} | [原始]({base}.yaml) | '
                f'[Boki](https://github.boki.moe/{base}-boki.yaml) | [GHFast](https://ghfast.top/{base}-ghfast.yaml) |')
    featured = [pid for pid in ('combined', 'china', 'full') if pid in profiles]
    rows += [row(pid, profiles[pid]) for pid in featured]
    others = [pid for pid in profiles if pid not in featured]
    if others:
        rows += ['', '<details>', f'<summary>其他 mihomo 分类（{len(others)} 项）</summary>', '',
                 '| 分类 | 拦截条目 | 例外条目 | 原始配置 | Boki 配置 | GHFast 配置 |',
                 '| --- | ---: | ---: | --- | --- | --- |',
                 *(row(pid, profiles[pid]) for pid in others), '', '</details>']
    return '\n'.join(rows)


def read_optional(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def heartbeat(path):
    today = datetime.now(timezone.utc)
    week = today.strftime('%G-W%V')
    if read_optional(path).get('week') == week:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(week=week, successfulRunUtc=today.isoformat(timespec='seconds')),
                               indent=2) + '\n', encoding='utf-8')


def summary(path, cache):
    run = read_optional(cache / 'last-run.json')
    audit = read_optional(cache / 'publish-audit.json')
    sources = run.get('sources', {})
    cached = run.get('cacheSources', [])
    lines = ['## DNS subscriptions update', '',
             f"Checked: {run.get('checkedUtc', 'Build did not complete')}", '',
             f"Sources: {len(sources)}; cache fallback: {len(cached)}; failed profiles: {len(run.get('failedProfiles', []))}",
             f"Publication audit: {audit.get('status', 'not run')}", '',
             'Each validated profile/platform can publish independently; failed outputs retain their previous version.', '']
    if cached:
        print(f'::warning::{len(cached)} upstream sources used validated cache (maximum age 72 hours); see run artifact.')
        lines += ['Cached sources (these were not freshly downloaded):', ''] + [f'- {sid}' for sid in cached]
    if audit.get('error'):
        lines += ['', audit['error']]
    for pid, errors in audit.get('failures', {}).items():
        lines += [f'- {pid}: {errors}']
    lines += ['', '| Profile | Rules | Engine |', '| --- | ---: | --- |']
    for pid, item in audit.get('profiles', {}).items():
        lines.append(f"| {pid} | {item['rules']} | {item['engine']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as handle:
        handle.write('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--heartbeat', type=Path)
    parser.add_argument('--summary', type=Path)
    parser.add_argument('--readme', type=Path)
    parser.add_argument('--build-outcome')
    parser.add_argument('--audit-outcome')
    parser.add_argument('--cache', type=Path, default=Path('.cache'))
    parser.add_argument('--config', type=Path, default=Path('profiles.json'))
    parser.add_argument('--manifest', type=Path, default=Path('dist/manifest.json'))
    parser.add_argument('--registry', type=Path, default=Path('registry/sources.json'))
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY', DEFAULT_REPOSITORY))
    args = parser.parse_args()
    if args.heartbeat:
        heartbeat(args.heartbeat)
    if args.summary:
        summary(args.summary, args.cache)
    if args.readme:
        run = read_optional(args.cache / 'last-run.json')
        if not run:
            run = dict(checkedUtc=datetime.now(timezone.utc).isoformat(timespec='seconds'), status='failed')
        publication = {}
        if args.build_outcome == 'success' and args.audit_outcome == 'success':
            publication = dict(config=read_optional(args.config), manifest=read_optional(args.manifest),
                               registry=read_optional(args.registry), repository=args.repository,
                               mihomo_manifest=read_optional(args.manifest.parent / 'mihomo/manifest.json') or None)
        update_readme(args.readme, run, args.build_outcome, args.audit_outcome, **publication)


if __name__ == '__main__':
    main()
