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
    from refresh_source_registry import main as current_main
    return current_main()


if __name__ == "__main__":
    main()
