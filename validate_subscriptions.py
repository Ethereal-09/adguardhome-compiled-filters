"""Check every subscription and its manifest before publishing a Git commit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from build_filters import ROOT, load_plan, parse_dns_line, read_json


def audit(output, config_path, registry_path, validator, profile_ids=None, check_alias=True):
    config, profiles, sources = load_plan(config_path, registry_path)
    manifest = read_json(output / 'manifest.json')
    if manifest.get('defaultProfile') != config['defaultProfile']:
        raise ValueError('Manifest default profile differs from configuration')
    results = {}
    for profile in profiles:
        pid = profile['id']
        if profile_ids is not None and pid not in profile_ids:
            continue
        item = manifest['profiles'][pid]
        if item['status'] != 'ready' or item['sourceIds'] != profile['sourceIds']:
            raise ValueError('Profile is failed/retained or has different sources: ' + pid)
        path = output / (pid + '.txt')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item.get('fileSha256'):
            raise ValueError('Subscription checksum differs from manifest: ' + pid)
        previous, count, exceptions, headers = None, 0, 0, set()
        with path.open(encoding='utf-8') as handle:
            for number, raw in enumerate(handle, 1):
                line = raw.rstrip('\n')
                if line.startswith('!'):
                    headers.add(line)
                    continue
                if not line or parse_dns_line(line) != [line]:
                    raise ValueError(f'{pid}:{number}: noncanonical/unsupported rule')
                if previous is not None and line <= previous:
                    raise ValueError(f'{pid}:{number}: duplicate or unsorted rule')
                previous, count = line, count + 1
                exceptions += line.startswith('@@')
                if profile['kind'] == 'allowlist' and not line.startswith('@@'):
                    raise ValueError('Blocking rule in an independent allowlist: ' + pid)
        if (count != item['totalRules'] or exceptions != item['exceptionRules']
                or count - exceptions != item['blockingRules']):
            raise ValueError('Manifest counts differ from file: ' + pid)
        for sid in profile['sourceIds']:
            source = sources[sid]
            if f"! Source: {source['name']} | {source['url']}" not in headers:
                raise ValueError('Missing upstream attribution: ' + sid)
        with path.open(encoding='utf-8') as handle:
            checked = subprocess.run([str(Path(validator).resolve())], stdin=handle,
                                     text=True, encoding='utf-8', capture_output=True, timeout=180)
        report = json.loads(checked.stdout)
        if (checked.returncode or report.get('invalid') or report.get('checked') != count
                or report.get('engine') != 'AdguardTeam/urlfilter v0.23.4'):
            raise ValueError(f'{pid}: AdGuard engine rejected output: {report}')
        results[pid] = dict(rules=count, sha256=digest, engine=report['engine'], usesCache=item['usesCache'])
        print(f'VALID {pid}: {count} rules', flush=True)
    default = output / (config['defaultProfile'] + '.txt')
    if check_alias and (output / 'adguard.txt').read_bytes() != default.read_bytes():
        raise ValueError('Default subscription alias differs from configured profile')
    return dict(status='passed', profiles=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--config', type=Path, default=ROOT / 'profiles.json')
    parser.add_argument('--registry', type=Path, default=ROOT / 'registry/sources.json')
    parser.add_argument('--validator', type=Path, required=True)
    parser.add_argument('--report', type=Path, default=ROOT / '.cache/publish-audit.json')
    args = parser.parse_args()
    try:
        report = audit(args.output, args.config, args.registry, args.validator)
    except Exception as error:
        report = dict(status='failed', error=str(error))
        print(str(error), file=sys.stderr)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
