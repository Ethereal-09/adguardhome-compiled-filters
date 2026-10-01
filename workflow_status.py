"""Write an Actions run summary and a weekly repository maintenance record."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re

from update_rules import atomic_write

BUILD_START = '<!-- build-status:start -->'
BUILD_END = '<!-- build-status:end -->'


def update_readme(path, run, build_outcome=None, audit_outcome=None):
    """Replace only the build-status block; never claim cached sources are fresh."""
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    if text.count(BUILD_START) != 1 or text.count(BUILD_END) != 1:
        raise ValueError('README must contain exactly one build-status block')
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
    block = [BUILD_START, f"> 最近构建：**{stamp:%Y-%m-%d %H:%M:%S}（北京时间）**", '>',
             '> 状态：**' + state + '**' + (' · ' + ' · '.join(details) if details else ''), BUILD_END]
    updated = re.sub(re.escape(BUILD_START) + r'.*?' + re.escape(BUILD_END),
                     lambda _: '\n'.join(block), text, flags=re.DOTALL)
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
    args = parser.parse_args()
    if args.heartbeat:
        heartbeat(args.heartbeat)
    if args.summary:
        summary(args.summary, args.cache)
    if args.readme:
        run = read_optional(args.cache / 'last-run.json')
        if not run:
            run = dict(checkedUtc=datetime.now(timezone.utc).isoformat(timespec='seconds'), status='failed')
        update_readme(args.readme, run, args.build_outcome, args.audit_outcome)


if __name__ == '__main__':
    main()
