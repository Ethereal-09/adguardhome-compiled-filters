"""Build a DNS-only AdGuard subscription using Python's standard library."""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
UNSUPPORTED = '__UNSUPPORTED__'


def domain(value: str) -> str | None:
    try:
        value = value.strip().rstrip('.').encode('idna').decode('ascii').lower()
    except UnicodeError:
        return None
    if len(value) > 253 or '.' not in value:
        return None
    try:
        ipaddress.ip_address(value)
        return None
    except ValueError:
        pass
    if any(len(label) > 63 or not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', label)
           for label in value.split('.')):
        return None
    return value


def parse_line(line: str) -> list[str]:
    line = line.strip()
    if not line or line.startswith(('!', '#', '[Adblock')):
        return []
    match = re.fullmatch(r'(@@)?\|\|([^\^$\s]+)\^(\$important)?', line)
    if match:
        name = domain(match[2])
        return [(match[1] or '') + '||' + name + '^' + (match[3] or '')] if name else [UNSUPPORTED]
    match = re.fullmatch(r'(?:0\.0\.0\.0|127\.0\.0\.1|::|::1)\s+(.+)', line)
    if match:
        result = []
        for host in match[1].split('#', 1)[0].split():
            if host.lower() in ('localhost', 'localhost.localdomain'):
                continue
            name = domain(host)
            result.append(f'|{name}|' if name else UNSUPPORTED)
        return result
    # Only whitespace-delimited inline comments; ## is a cosmetic rule.
    name = domain(re.sub(r'\s+#.*$', '', line))
    return [f'|{name}|'] if name else [UNSUPPORTED]


def custom_rules(path: Path, allow: bool) -> set[str]:
    rules = set()
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        for rule in parse_line(line):
            if rule == UNSUPPORTED:
                raise ValueError(f'Unsupported personal rule at {path}:{number}: {line}')
            if allow:
                rule = re.sub(r'^@@', '', rule).removesuffix('$important')
                rule = '@@' + rule + '$important'
            elif rule.startswith('@@'):
                raise ValueError(f'Put exceptions in allow.txt: {path}:{number}')
            rules.add(rule)
    return rules


def fetch(url: str, timeout: int, retries: int) -> str:
    if not url.startswith('https://'):
        raise ValueError(f'HTTPS required: {url}')
    for attempt in range(1, retries + 1):
        try:
            request = Request(url, headers={'User-Agent': 'PersonalDNSRules/2.0'})
            with urlopen(request, timeout=timeout) as response:
                if not response.url.startswith('https://'):
                    raise ValueError('Redirect to non-HTTPS URL')
                status = response.getcode()
                if isinstance(status, int) and status != 200:
                    raise ValueError(f'Incomplete or unexpected HTTP response: {status}')
                length = response.headers.get('Content-Length')
                expected = int(length) if isinstance(length, str) and length.isdigit() else None
                if expected is not None and expected > 32 * 1024 * 1024:
                    raise ValueError('Source exceeds 32 MiB limit')
                raw = response.read(32 * 1024 * 1024 + 1)
                if len(raw) > 32 * 1024 * 1024:
                    raise ValueError('Source exceeds 32 MiB limit')
                if expected is not None and len(raw) != expected:
                    raise ValueError(f'Truncated response: expected {expected} bytes, received {len(raw)}')
                body = raw.decode('utf-8-sig')
            if not body.strip() or re.search(r'<\s*(?:!doctype\s+html|html|head|body)\b', body, re.I):
                raise ValueError('Empty response or HTML instead of rules')
            count = re.search(r'(?im)^![^\n]*\bCount:\s*([\d,]+)\s+rules!?', body[:4096])
            if count:
                declared = int(count[1].replace(',', ''))
                active = sum(bool(line.strip()) and not line.strip().startswith(('!', '#', '[Adblock'))
                             for line in body.splitlines())
                if active < declared * .98:
                    raise ValueError(f'Truncated rule source: header declares {declared}, received {active} lines')
            return body
        except Exception:
            if attempt == retries:
                raise
            print(f'Download failed, retry {attempt}/{retries}: {url}', file=sys.stderr)
            time.sleep(min(10, 2 * attempt))
    raise RuntimeError('No download attempts')


def atomic_write(path: Path, text: str) -> None:
    fd, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def build(config_path: Path, output: Path, custom: Path, allow_large_drop: bool = False) -> int:
    config = json.loads(config_path.read_text(encoding='utf-8-sig'))
    timeout, retries, drop = config['timeoutSeconds'], config['retries'], config['maxDropFraction']
    if not isinstance(timeout, int) or timeout < 1 or not isinstance(retries, int) or retries < 1 or not 0 <= drop < 1:
        raise ValueError('Invalid configuration limits')
    previous_path = output / 'report.json'
    previous = json.loads(previous_path.read_text(encoding='utf-8-sig')) if previous_path.exists() else {}
    old_sources = {item['url']: item for item in previous.get('sources', [])}
    sources = [item for item in config['sources'] if item.get('enabled', False)]
    if not sources:
        raise ValueError('No enabled sources')
    # Validate personal rules before doing any network requests.
    rules = custom_rules(custom / 'block.txt', False) | custom_rules(custom / 'allow.txt', True)
    stats = []
    for source in sources:
        print(f"Downloading {source['name']}", flush=True)
        body = fetch(source['url'], timeout, retries)
        accepted, unsupported = set(), 0
        for line in body.splitlines():
            for rule in parse_line(line):
                if rule == UNSUPPORTED:
                    unsupported += 1
                else:
                    accepted.add(rule)
        minimum = source['minimumRules']
        if not isinstance(minimum, int) or minimum < 1 or len(accepted) < minimum:
            raise ValueError(f"Too few supported rules from {source['name']}: {len(accepted)}")
        old = old_sources.get(source['url'])
        if not allow_large_drop and old and len(accepted) < old['accepted'] * (1 - drop):
            raise ValueError(f"Abnormal decrease from {source['name']}; review before --allow-large-drop")
        rules.update(accepted)
        stats.append(dict(name=source['name'], url=source['url'], accepted=len(accepted), unsupported=unsupported))
        print(f'  Accepted {len(accepted)}, unsupported {unsupported}', flush=True)
    if not allow_large_drop and previous and len(rules) < previous['totalRules'] * (1 - drop):
        raise ValueError('Abnormal total decrease; review before --allow-large-drop')
    target = output / 'adguard.txt'
    old_rules = {line for line in target.read_text(encoding='utf-8-sig').splitlines() if line and not line.startswith('!')} if target.exists() else None
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    report = dict(updatedUtc=now, totalRules=len(rules), sources=stats)
    output.mkdir(parents=True, exist_ok=True)
    if old_rules == rules:
        # Update report only when source statistics changed; no timestamp-only commits.
        if previous.get('sources') != stats or previous.get('totalRules') != len(rules):
            atomic_write(previous_path, json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(f'No rule changes ({len(rules)} rules).')
        return len(rules)
    title = re.sub(r'[\r\n]', ' ', str(config['title']))
    content = [f'! Title: {title}', f'! Updated: {now}', f'! Rules: {len(rules)}',
               '! Generated file. Edit custom files or config.json.', *sorted(rules)]
    atomic_write(target, '\n'.join(content) + '\n')
    atomic_write(previous_path, json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'Published {len(rules)} rules to {target}')
    return len(rules)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'config.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--custom', type=Path, default=ROOT / 'custom')
    parser.add_argument('--allow-large-drop', action='store_true')
    args = parser.parse_args()
    try:
        build(args.config, args.output, args.custom, args.allow_large_drop)
        return 0
    except KeyboardInterrupt:
        print('Stopped by user.', file=sys.stderr)
        return 130
    except Exception as error:
        print(f'Update failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
