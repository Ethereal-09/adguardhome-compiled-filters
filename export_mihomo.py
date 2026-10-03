"""Export verified AdGuard DNS subscriptions as mihomo MRS and regex providers."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import struct
import subprocess
import sys
import tempfile
import time
from urllib.request import ProxyHandler, build_opener

from build_filters import ROOT, json_text, read_json
from workflow_status import DEFAULT_REPOSITORY, SUBSCRIPTION_ACCELERATORS

MIHOMO_VERSION = 'v1.19.32'
SIMPLE = re.compile(r'(@@)?(\|\||\|)([a-zA-Z0-9.-]+)(\^|\|)(\$important)?')
BUCKETS = ('block', 'allow', 'block-important', 'allow-important')


def empty_domain_mrs():
    """MRSv1 with zero rules and a nonterminal root; it matches no hostname.

    The official converter rejects zero input. Encode its documented reader
    layout instead: root bitmap terminates before its unreachable label.
    See v1.19.32 rules/provider/mrs_reader.go and component/trie/domain_set_bin.go.
    A single raw Zstandard block avoids a compression library dependency.
    Every generated file is still loaded and counted by the official kernel.
    """
    payload = b'MRS\x01\x00' + struct.pack('>qq', 0, 0)
    payload += b'\x01' + struct.pack('>qqqqq', 1, 0, 1, 1, 1) + b'\x00'
    return b'\x28\xb5\x2f\xfd\x20' + bytes([len(payload)]) + ((len(payload) << 3) | 1).to_bytes(3, 'little') + payload


def yaml_config(config):
    """Readable YAML using JSON-quoted scalars (no optional YAML dependency)."""
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    lines = ['# Merge these providers and rules into your existing mihomo configuration.', 'rule-providers:']
    for name, provider in config['rule-providers'].items():
        lines.append('  ' + name + ':')
        lines.extend('    ' + key + ': ' + quote(value) for key, value in provider.items())
    lines.append('rules:' if config['rules'] else 'rules: []')
    lines.extend('  - ' + quote(rule) for rule in config['rules'])
    return '\n'.join(lines) + '\n'


def convert_rule(line):
    """Return priority/action, provider format and payload; never widen an exact host."""
    allow, important = line.startswith('@@'), line.endswith('$important')
    bucket = ('allow' if allow else 'block') + ('-important' if important else '')
    match = SIMPLE.fullmatch(line)
    if match and (match[2], match[4]) in (('||', '^'), ('|', '|')):
        return bucket, 'domain', ('+.' if match[2] == '||' else '') + match[3]
    pattern = line.removeprefix('@@')
    if important:
        pattern = pattern[:-10]
    if len(pattern) > 2 and pattern.startswith('/') and pattern.endswith('/'):
        expression = pattern[1:-1]
        if any(token in expression for token in (r'\Q', r'\E', '[[:')):
            raise ValueError('Regex uses nonportable Go/.NET syntax: ' + line)
    else:
        if not re.fullmatch(r'[a-zA-Z0-9_.|^*\-]+', pattern) or '.' not in pattern:
            raise ValueError('Cannot safely export rule: ' + line)
        # Mirrors urlfilter's mask grammar on DNS hostnames. A || rule matches
        # the synthetic http://hostname request, so retain the label boundary.
        prefix = ''
        if pattern.startswith('||'):
            prefix, pattern = r'^(?:[a-z0-9-_.]+\.)?', pattern[2:]
        elif pattern.startswith('|'):
            prefix, pattern = '^', pattern[1:]
        end = '$' if pattern.endswith('|') else ''
        if end:
            pattern = pattern[:-1]
        expression = prefix + ''.join('.*' if char == '*' else
            r'([^ a-zA-Z0-9.%_-]|$)' if char == '^' else re.escape(char)
            for char in pattern) + end
    if '\n' in expression or '\r' in expression:
        raise ValueError('Multiline regex cannot be exported')
    return bucket, 'classical', 'DOMAIN-REGEX,' + expression


def bucket_expression(providers, bucket):
    names = [name for name, info in providers.items() if info['bucket'] == bucket]
    parts = ['(RULE-SET,' + name + ')' for name in names]
    return parts[0] if len(parts) == 1 else '(OR,(' + ','.join(parts) + '))' if parts else None


def reject_rules(providers):
    """Exceptions skip rejection and fall through to the user's remaining routing rules."""
    rules = []
    for bucket in ('block-important', 'block'):
        expression = bucket_expression(providers, bucket)
        if not expression:
            continue
        terms = [expression]
        exceptions = ('allow-important',) if bucket == 'block-important' else ('allow', 'allow-important')
        for exception in exceptions:
            allowed = bucket_expression(providers, exception)
            if allowed:
                terms.append('(NOT,(' + allowed + '))')
        rule = 'AND,(' + ','.join(terms) + '),REJECT' if len(terms) > 1 else expression[1:-1] + ',REJECT'
        rules.append(rule)
    return rules


def profile_config(pid, providers, rules, repository, accelerator='original'):
    prefix = dict(SUBSCRIPTION_ACCELERATORS).get(accelerator, '')
    mapping = {}
    for name, info in providers.items():
        raw = f'https://raw.githubusercontent.com/{repository}/main/dist/mihomo/{info["file"]}'
        mapping[name] = dict(type='http', behavior=info['behavior'], format=info['format'],
                             url=prefix + raw, path='./rule_provider/compiled/' + info['file'], interval=86400)
    return dict(**{'rule-providers': mapping}, rules=rules)


def binary_version(binary):
    result = subprocess.run([str(binary), '-v'], capture_output=True, text=True, encoding='utf-8', timeout=20)
    if result.returncode or not re.search(r'\b' + re.escape(MIHOMO_VERSION) + r'\b', result.stdout):
        raise ValueError('Expected official mihomo ' + MIHOMO_VERSION + ': ' + result.stdout[:200])


def kernel_errors(text):
    return [line for line in text.splitlines()
            if re.search(r'\blevel=(warning|error|fatal)\b', line)
            and 'msg="Mihomo shutting down"' not in line]


def validate_kernel(binary, stage, offline, providers):
    """Initialize providers in the actual kernel: -t alone does not check every payload."""
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        port = listener.getsockname()[1]
    offline['external-controller'] = f'127.0.0.1:{port}'
    path = stage / 'test.json'
    path.write_text(json_text(offline), encoding='utf-8')
    log_path = stage / 'kernel.log'
    with log_path.open('w', encoding='utf-8') as log:
        process = subprocess.Popen([str(binary), '-d', str(stage), '-f', str(path)], stdout=log, stderr=log,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        try:
            opener = build_opener(ProxyHandler({}))
            deadline = time.monotonic() + 60
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise ValueError('mihomo exited during provider validation')
                try:
                    with opener.open(f'http://127.0.0.1:{port}/providers/rules', timeout=2) as response:
                        # During bulk initialization the controller may return
                        # {"providers": null} before registration completes.
                        loaded = json.load(response).get('providers') or {}
                    if all(name in loaded and loaded[name]['ruleCount'] == info['rules']
                           for name, info in providers.items()):
                        break
                except (OSError, ValueError, KeyError):
                    pass
                time.sleep(.2)
            else:
                raise ValueError('mihomo did not load every expected provider/rule count: ' + log_path.read_text(encoding='utf-8')[-1000:])
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
    if kernel_errors(log_path.read_text(encoding='utf-8')):
        raise ValueError('mihomo reported invalid provider content: ' + log_path.read_text(encoding='utf-8')[-1000:])


def export(source, output, config_path, binary, repository=DEFAULT_REPOSITORY):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Invalid repository')
    binary = Path(binary).resolve()
    binary_version(binary)
    config, manifest = read_json(config_path), read_json(source / 'manifest.json')
    profiles = [p for p in config['profiles'] if p.get('enabled')]
    contents, exported, all_providers = {}, {}, {}
    with tempfile.TemporaryDirectory(prefix='mihomo-export-') as temp:
        stage = Path(temp)
        for profile in profiles:
            pid, item = profile['id'], manifest['profiles'][profile['id']]
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', pid):
                raise ValueError('Invalid profile ID: ' + pid)
            if item['status'] != 'ready' or item['sourceIds'] != profile['sourceIds']:
                raise ValueError('Export requires a verified, ready profile: ' + pid)
            body = (source / (pid + '.txt')).read_bytes()
            if hashlib.sha256(body).hexdigest() != item['fileSha256']:
                raise ValueError('Input checksum differs from manifest: ' + pid)
            data = {(bucket, behavior): set() for bucket in BUCKETS for behavior in ('domain', 'classical')}
            headers, count, exceptions = [], 0, 0
            for line in body.decode('utf-8').splitlines():
                if line.startswith('!'):
                    headers.append('#' + line[1:])
                elif line:
                    bucket, behavior, payload = convert_rule(line)
                    data[bucket, behavior].add(payload)
                    count += 1
                    exceptions += line.startswith('@@')
            if (count != item['totalRules'] or exceptions != item['exceptionRules']
                    or count - exceptions != item['blockingRules']):
                raise ValueError('Input rule counts differ from manifest: ' + pid)
            if profile['kind'] == 'allowlist' and count != exceptions:
                raise ValueError('Blocking rule in allowlist: ' + pid)
            providers = {}
            for (bucket, behavior), payloads in data.items():
                primary = bucket == ('allow' if profile['kind'] == 'allowlist' else 'block')
                stem = pid if primary else pid + '-' + bucket
                name = 'compiled-' + pid + '-' + bucket + ('-regex' if behavior == 'classical' else '')
                filename = stem + ('-regex.txt' if behavior == 'classical' else '.mrs')
                text = '\n'.join(headers + ['# mihomo ' + behavior + ' provider; preserve companion exception providers.']
                                 + sorted(payloads)) + '\n'
                if behavior == 'domain':
                    plain, mrs = stage / (name + '.txt'), stage / filename
                    plain.write_text(text, encoding='utf-8', newline='\n')
                    if not payloads:
                        mrs.write_bytes(empty_domain_mrs())
                    else:
                        result = subprocess.run([str(binary), 'convert-ruleset', 'domain', 'text', str(plain), str(mrs)],
                                            capture_output=True, text=True, encoding='utf-8', timeout=180)
                        if result.returncode or 'skip invalid' in (result.stdout + result.stderr).lower():
                            raise ValueError('MRS conversion failed: ' + pid + ': ' + result.stdout + result.stderr)
                    contents[filename] = mrs.read_bytes()
                else:
                    contents[filename] = text.encode('utf-8')
                providers[name] = dict(file=filename, bucket=bucket, behavior=behavior,
                    format='mrs' if behavior == 'domain' else 'text', rules=len(payloads),
                    sha256=hashlib.sha256(contents[filename]).hexdigest())
            routing = [] if profile['kind'] == 'allowlist' else reject_rules(providers)
            for accelerator in ('original', 'Boki', 'GHFast'):
                suffix = '' if accelerator == 'original' else '-' + accelerator.lower()
                contents[pid + suffix + '.yaml'] = yaml_config(profile_config(pid, providers, routing, repository, accelerator)).encode('utf-8')
            exported[pid] = dict(name=profile['name'], kind=profile['kind'], sourceIds=item['sourceIds'],
                configVersion=2,
                updatedUtc=item['updatedUtc'], inputSha256=item['fileSha256'], inputRules=count,
                blockingRules=count-exceptions, exceptionRules=exceptions,
                convertedRules=sum(len(r) for r in data.values()), upstreamNotices=headers,
                providers=providers, rules=routing)
            all_providers.update(providers)
            print(f'MIHOMO {pid}: {count} input rules, {len(providers)} providers', flush=True)

        # A real kernel parses all providers and the generated logical routes.
        for filename, content in contents.items():
            (stage / filename).write_bytes(content)
        offline = {'mode': 'rule', 'log-level': 'warning', 'rule-providers': {
            name: dict(type='file', behavior=info['behavior'], format=info['format'], path=info['file'])
            for name, info in all_providers.items()},
            'rules': [rule for item in exported.values() for rule in item['rules']] + ['MATCH,DIRECT']}
        (stage / 'test.yaml').write_text(yaml_config(offline), encoding='utf-8')
        result = subprocess.run([str(binary), '-t', '-d', str(stage), '-f', str(stage / 'test.yaml')],
                                capture_output=True, text=True, encoding='utf-8', timeout=240)
        if result.returncode or any(word in (result.stdout + result.stderr).lower()
                                  for word in ('error', 'invalid', 'warn')):
            raise ValueError('mihomo configuration validation failed: ' + result.stdout + result.stderr)
        validate_kernel(binary, stage, offline, all_providers)
    report = dict(schemaVersion=2, configVersion=2, engine='mihomo ' + MIHOMO_VERSION, profiles=exported,
                  validatedProviders=len(all_providers),
                  sourceManifestSha256=hashlib.sha256((source / 'manifest.json').read_bytes()).hexdigest())
    contents['manifest.json'] = json_text(report).encode('utf-8')
    contents['README.md'] = index_content(exported).encode('utf-8')
    # Publish nothing until all profiles and routes passed conversion/validation.
    output.mkdir(parents=True, exist_ok=True)
    for filename, content in contents.items():
        path = output / filename
        if not path.exists() or path.read_bytes() != content:
            from dns_utils import atomic_write
            if filename.endswith('.mrs'):
                temporary = path.with_suffix(path.suffix + '.tmp')
                temporary.write_bytes(content)
                temporary.replace(path)
            else:
                atomic_write(path, content.decode('utf-8'))
    print(f'VALID MIHOMO: {len(exported)} profiles, {len(all_providers)} providers loaded with exact rule counts.', flush=True)
    return report


def index_content(profiles):
    return '''# mihomo 分类规则

与 AdGuard Home 版使用同一批已验证分类；域名使用 MRS，通配符和正则使用 classical/text 配套规则集。
精确域名保持精确匹配；父域名及子域名范围、原生例外和 important 优先级保留。
规则由原作者维护，署名和许可见 [上游](../../upstream/README.md)；来源详情见 [统计](manifest.json)。

## 使用

1. 从下表选择一个配置片段，合并其中的 `rule-providers` 到现有配置。
2. 把片段的 `rules` 按原顺序放在现有分流规则之前。不要覆盖原来的节点、策略组或后续规则。
3. Boki / GHFast 片段中的所有规则集下载地址也使用对应加速源。每天更新一次（86400 秒）。

旧版用户需重新合并一次配置版本 2 的片段。新版固定声明八个 provider（四种动作/优先级 × 域名/正则），
即使暂无对应规则也保留不匹配任何域名的空规则集。以后出现新的例外、important 或正则时，无需再次修改配置。
这是配置片段，不是节点订阅；`interval` 只刷新规则文件，不刷新你合并过的配置。

放行例外只跳过本分类的 REJECT，继续执行后面的分流规则。不要单独使用拦截 MRS，否则会遗漏配套例外或正则。
独立白名单片段仅声明 provider，不自动强制 DIRECT；可用 NOT 条件排除拦截，或按你的用途指定策略。
多分类同时启用时，例外只对各自分类有效；需统一跨分类例外时，先合并来源生成同一分类。
这是域名流量拦截，不是 DNS 响应改写；仅 IP 连接且没有域名元数据时无法按域名过滤。
使用 mihomo ''' + MIHOMO_VERSION + ''' 或更新版本。生成器用官方内核转换 MRS 并验证配置；每日发布按分类隔离失败，保留该分类旧版。
格式依据：[规则集合](https://wiki.metacubex.one/config/rule-providers/) / [路由规则](https://wiki.metacubex.one/config/rules/)。

## 配置片段

| 分类 | 拦截条目 | 例外条目 | 原始 | 加速1 | 加速2 |
| --- | ---: | ---: | --- | --- | --- |
''' + '\n'.join(f'| {item["name"]} | {item["blockingRules"]:,} | {item["exceptionRules"]:,} | [{pid}.yaml]({pid}.yaml) | [Boki]({pid}-boki.yaml) | [GHFast]({pid}-ghfast.yaml) |'
               for pid, item in profiles.items()) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'dist')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/mihomo')
    parser.add_argument('--config', type=Path, default=ROOT / 'profiles.json')
    parser.add_argument('--mihomo', type=Path, default=os.environ.get('MIHOMO_BINARY'), required=not os.environ.get('MIHOMO_BINARY'))
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY', DEFAULT_REPOSITORY))
    args = parser.parse_args()
    try:
        export(args.source, args.output, args.config, args.mihomo, args.repository)
        return 0
    except Exception as error:
        print('mihomo export failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
