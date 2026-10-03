"""Shared DNS rule parsing, verified downloads and atomic file writes."""
from __future__ import annotations

import ipaddress
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.parse import urlparse
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
            headers = body[:4096]
            counts = re.findall(r'(?im)^![^\n]*\bCount:\s*([\d,]+)\s+rules!?', headers)
            counts += re.findall(r'(?im)^![ \t]*Entries:[ \t]*([\d,]+)[ \t]*\r?$', headers)
            if counts:
                active = sum(bool(line.strip()) and not line.strip().startswith(('!', '#', '[Adblock'))
                             for line in body.splitlines())
                for count in counts:
                    declared = int(count.replace(',', ''))
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
