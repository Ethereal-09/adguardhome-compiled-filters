"""Update README subscriptions, build status and the Actions run summary."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re

from update_rules import atomic_write

BUILD_START = '<!-- build-status:start -->'
BUILD_END = '<!-- build-status:end -->'
SUBSCRIPTIONS_START = '<!-- subscriptions:start -->'
SUBSCRIPTIONS_END = '<!-- subscriptions:end -->'
UPSTREAM_START = '<!-- upstream:start -->'
UPSTREAM_END = '<!-- upstream:end -->'
DEFAULT_REPOSITORY = 'Ethereal-09/adguardhome-compiled-filters'


def replace_block(text, start, end, content):
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f'README must contain exactly one ordered block: {start}')
    return re.sub(re.escape(start) + r'.*?' + re.escape(end),
                  lambda _: start + '\n' + content.rstrip() + '\n' + end, text, flags=re.DOTALL)


def publication_blocks(config, manifest, registry, repository):
    """Describe the validated output; never use historical registry rule counts."""
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Invalid README repository')
    profiles = [p for p in config['profiles'] if p.get('enabled', False)]
    sources = {s['id']: s for s in registry['sources']}
    selected = set()
    groups = {name: [] for name in ('基础订阅', '强度档位', '用途分类', '设备与服务限制', '独立白名单')}
    labels = {'combined': '综合版', 'full': '全量版', 'china': '国内优化',
              'balanced': 'HaGeZi 均衡 · Normal', 'extended': 'HaGeZi 扩展 · Pro',
              'aggressive': 'HaGeZi 激进 · Pro++', 'maximum': 'HaGeZi 最强 · Ultimate',
              'balanced-1hosts': '1Hosts 均衡 · Lite', 'aggressive-1hosts': '1Hosts 激进 · Xtra'}
    for profile in profiles:
        pid = profile['id']
        item = manifest['profiles'][pid]
        if item['status'] != 'ready' or item['sourceIds'] != profile['sourceIds']:
            raise ValueError('README counts require ready outputs with matching sources: ' + pid)
        count = item['totalRules']
        if type(count) is not int or count < 1 or count != item['blockingRules'] + item['exceptionRules']:
            raise ValueError('Invalid README rule count: ' + pid)
        selected.update(profile['sourceIds'])
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
        filename = 'adguard.txt' if pid == config['defaultProfile'] else pid + '.txt'
        url = f'https://raw.githubusercontent.com/{repository}/main/dist/{filename}'
        row = f'| {label} | {count:,} | [订阅]({url}) |'
        groups[group].append((pid, row))

    rows = ['## 规则订阅', '',
            '数量为最近一次通过发布校验的文件条目数，含原生放行例外；每个订阅独立去重，分类之间的数量不能直接相加。', '']
    notes = {'基础订阅': '添加到 **DNS 黑名单**。综合版与全量版选其一，国内优化可单独使用。',
             '强度档位': '按需求选一个档位；1Hosts 为替代基础。综合版以 HaGeZi Normal 为基础，叠加已核验的通用与国内 DNS 来源。',
             '用途分类': '添加到 **DNS 黑名单**，可按用途单独订阅或搭配基础订阅。',
             '设备与服务限制': '添加到 **DNS 黑名单**，按需启用；整站或服务限制可能影响正常功能。',
             '独立白名单': '添加到 **DNS 白名单**。各文件按用途选用，不自动并入黑名单。'}
    for group, entries in groups.items():
        if not entries:
            continue
        if group == '基础订阅':
            order = {'combined': 0, 'china': 1, 'full': 2}
            entries.sort(key=lambda entry: order.get(entry[0], 3))
        rows += ['### ' + group, '', notes[group], '',
                 '| 规则 | 规则数 | 订阅 |', '| --- | ---: | --- |',
                 *(row for _, row in entries), '']
        if group == '基础订阅' and any(pid == 'full' for pid, _ in entries):
            rows += [f"全量版合并 {len(manifest['profiles']['full']['sourceIds'])} 个兼容来源，含最高档位、设备与服务限制；各来源原生例外和个人规则保留。", '']
        if group == '基础订阅' and any(pid == 'china' for pid, _ in entries):
            names = '、'.join(sources[sid]['name'] for sid in manifest['profiles']['china']['sourceIds'])
            rows += ['国内优化来源：' + names + '。地域依据上游说明，规则文件独立合并与去重。', '']

    repositories = {sources[sid]['repository'] for sid in selected}
    github = sum(repo.startswith('https://github.com/') for repo in repositories)
    external = len(repositories) - github
    origins = f'**{github} 个 GitHub 原仓库**' + (f'及 **{external} 个官方站点**' if external else '')
    upstream = [f'当前选用 **{len(selected)} 个来源文件**，来自 {origins}。', '',
                '<details>', '<summary>查看来源维护账号、原始订阅与规则数量</summary>', '',
                '下表使用本次发布所选来源的支持条目数，含来源自身的放行例外，尚未做跨来源合并。仓库所属账号不代表全部原创作者，原作者及间接来源以各上游说明为准。', '',
                '| 维护账号 / 原始项目 | 原始规则文件 | 支持规则数 |', '| --- | --- | ---: |']
    for sid in sorted(selected, key=lambda sid: (sources[sid]['repository'].lower(), sources[sid]['path'])):
        source, stats = sources[sid], manifest['sources'][sid]
        if stats.get('url') != source['url'] or type(stats.get('accepted')) is not int or stats['accepted'] < 1:
            raise ValueError('Invalid README upstream count or identity: ' + sid)
        repo = source['repository']
        name = repo.removeprefix('https://github.com/') if repo.startswith('https://github.com/') else source['repositoryAccount']
        filename = source['path'].replace('|', r'\|')
        upstream.append(f"| [{name}]({repo}) | [{filename}]({source['url']}) | {stats['accepted']:,} |")
    upstream += ['', '</details>', '',
                 '完整来源与归类依据见 [来源登记](registry/sources.json)，各上游的许可及署名要求见 [许可原文](upstream/README.md)。合并产物保留各上游的权利和许可，不另行声明统一许可。']
    return '\n'.join(rows), '\n'.join(upstream)


def update_readme(path, run, build_outcome=None, audit_outcome=None, *,
                  config=None, manifest=None, registry=None, repository=DEFAULT_REPOSITORY):
    """Refresh counts only after successful publication validation; preserve them on failure."""
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
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
    updated = replace_block(text, BUILD_START, BUILD_END, '\n'.join(block))
    if not failed and build_outcome == 'success' and audit_outcome == 'success' and manifest is not None:
        subscriptions, upstream = publication_blocks(config, manifest, registry, repository)
        updated = replace_block(updated, SUBSCRIPTIONS_START, SUBSCRIPTIONS_END, subscriptions)
        updated = replace_block(updated, UPSTREAM_START, UPSTREAM_END, upstream)
    if updated != text:
        atomic_write(path, updated)


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
             'Subscriptions are committed only after build and publication audit both succeed.', '']
    if cached:
        print(f'::warning::{len(cached)} upstream sources used validated cache (maximum age 72 hours); see run artifact.')
        lines += ['Cached sources (these were not freshly downloaded):', ''] + [f'- {sid}' for sid in cached]
    if audit.get('error'):
        lines += ['', audit['error']]
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
                               registry=read_optional(args.registry), repository=args.repository)
        update_readme(args.readme, run, args.build_outcome, args.audit_outcome, **publication)


if __name__ == '__main__':
    main()
