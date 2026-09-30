"""Write an Actions run summary and a weekly repository maintenance record."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


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
    parser.add_argument('--cache', type=Path, default=Path('.cache'))
    args = parser.parse_args()
    if args.heartbeat:
        heartbeat(args.heartbeat)
    if args.summary:
        summary(args.summary, args.cache)


if __name__ == '__main__':
    main()
