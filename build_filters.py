"""Download verified original sources, build DNS subscriptions, and preserve failed outputs."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

from update_rules import ROOT, UNSUPPORTED, atomic_write, domain, fetch, parse_line
from verify_github_sources import decode_github
from workflow_status import update_readme


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_if_changed(path, content):
    if path.exists() and path.read_text(encoding='utf-8') == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, content)
    return True


def json_text(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def validate_engine(rules, validator):
    """Fail before publication if the pinned AdGuard DNS engine rejects a rule."""
    if validator is None:
        return None
    result = subprocess.run([str(Path(validator).resolve())], input='\n'.join(rules) + '\n',
                            text=True, encoding='utf-8', capture_output=True, timeout=180)
    try:
        report = json.loads(result.stdout)
    except (ValueError, TypeError) as error:
        raise ValueError('AdGuard validator returned no valid report: ' + result.stderr[:300]) from error
    if result.returncode or report.get('invalid') or report.get('checked') != len(rules):
        raise ValueError('AdGuard engine validation failed: ' + '; '.join(report.get('errors', []))[:1000])
    if report.get('engine') != 'AdguardTeam/urlfilter v0.23.4':
        raise ValueError('Unexpected AdGuard validator version')
    return report['engine']


@contextmanager
def build_lock(cache):
    cache.mkdir(parents=True, exist_ok=True)
    with (cache / 'build.lock').open('a+b') as handle:
        if handle.tell() == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise RuntimeError('Another filter build is running in this cache directory') from error
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def parse_dns_line(line):
    """Normalize simple rules; retain supported DNS masks/regex without rewriting them."""
    line = line.strip()
    if not line or line.startswith(('!', '#', '[Adblock')):
        return []
    exact = re.fullmatch(r'(@@)?\|([^|\s]+)\|(\$important)?', line)
    if exact:
        name = domain(exact[2])
        return [(exact[1] or '') + '|' + name + '|' + (exact[3] or '')] if name else [UNSUPPORTED]
    parsed = parse_line(line)
    if parsed != [UNSUPPORTED]:
        return parsed
    # Only important is supported as a modifier. Never strip domain/client/badfilter.
    pattern = line.removeprefix('@@')
    if pattern.endswith('$important'):
        pattern = pattern[:-10]
    if len(pattern) > 2 and pattern.startswith('/') and pattern.endswith('/'):
        return [line]  # opaque: no hostname coverage optimization for regular expressions
    if '$' not in pattern and '.' in pattern and re.fullmatch(r'[a-zA-Z0-9_.|^*\-]+', pattern):
        # A mask is admitted only if it actually uses a wildcard, or is an anchored
        # partial hostname. Invalid plain domain/Hosts entries are still skipped.
        if '*' in pattern or (pattern.startswith(('||', '|')) and not pattern.endswith(('^', '|'))):
            return [line]
    return [UNSUPPORTED]


def parse_source(body, role):
    rules, unsupported, entries, examples = set(), 0, 0, []
    if '\x00' in body:
        raise ValueError('NUL byte in rule source')
    for raw in body.splitlines():
        line = raw.strip()
        parsed = parse_dns_line(line)
        if not parsed:
            continue
        if '$badfilter' in line or ',badfilter' in line:
            raise ValueError('badfilter requires disabling rules before optimization; source rejected')
        if role == 'independent_allowlist' and not line.startswith('@@'):
            raise ValueError('Independent allowlist contains a non-exception rule')
        for rule in parsed:
            if rule == UNSUPPORTED:
                # Losing an exception would enlarge the upstream blocking scope.
                if line.startswith('@@'):
                    raise ValueError('Unsupported exception; source rejected instead of dropping it: ' + line[:160])
                unsupported += 1
                if len(examples) < 5:
                    examples.append(line[:160])
            else:
                entries += 1
                rules.add(rule)
    if not rules:
        raise ValueError('No supported DNS rules')
    return rules, dict(accepted=len(rules), parsedEntries=entries,
                      duplicates=entries-len(rules), unsupported=unsupported, unsupportedExamples=examples)


def simple_rule(rule):
    match = re.fullmatch(r'(@@)?(\|\||\|)([^|^$]+)(\^|\|)(\$important)?', rule)
    if not match or not domain(match[3]):
        return None
    scope = 'suffix' if match[2] == '||' and match[4] == '^' else 'exact'
    if (match[2], match[4]) not in (('||', '^'), ('|', '|')):
        return None
    return bool(match[1]), bool(match[5]), scope, match[3]


def optimize_rules(rules):
    """Remove covered domains only within identical action and priority buckets."""
    unique = set(rules)
    suffixes = {}
    for rule in unique:
        info = simple_rule(rule)
        if info and info[2] == 'suffix':
            suffixes.setdefault(info[:2], set()).add(info[3])
    kept = set()
    for rule in unique:
        info = simple_rule(rule)
        if not info:
            kept.add(rule)
            continue
        allow, important, scope, name = info
        candidates = suffixes.get((allow, important), set())
        labels = name.split('.')
        first = 1 if scope == 'suffix' else 0
        if not any('.'.join(labels[i:]) in candidates for i in range(first, len(labels))):
            kept.add(rule)
    return kept, len(unique)-len(kept)


def validate_source_origin(source):
    """Accept original GitHub files or an explicitly reviewed official website URL."""
    url = source['url']
    decoded = decode_github(url)
    if url.startswith('https://raw.githubusercontent.com/'):
        if not decoded or source['repository'] != 'https://github.com/' + decoded[0]:
            raise ValueError('Unverified raw GitHub provenance: ' + source['id'])
        return
    proof = source.get('provenance', {})
    website, evidence, subscription = (urlsplit(value) for value in
        (source['repository'], proof.get('evidenceUrl', ''), url))
    if (proof.get('kind') != 'official_website' or proof.get('status') != 'verified'
            or proof.get('subscriptionUrl') != url or not proof.get('checkedUtc')
            or any(p.scheme != 'https' or not p.hostname or p.username or p.password
                   for p in (website, evidence, subscription))
            or website.hostname != subscription.hostname or evidence.hostname != website.hostname):
        raise ValueError('Unverified official website provenance: ' + source['id'])


def load_plan(config_path, registry_path):
    config, registry = read_json(config_path), read_json(registry_path)
    if config.get('schemaVersion') != 1:
        raise ValueError('Unsupported profile configuration schema')
    sources = {s['id']: s for s in registry['sources']}
    limits = config['download']
    for key in ('timeoutSeconds', 'retries', 'workers'):
        if type(limits[key]) is not int or limits[key] < 1:
            raise ValueError('Invalid download setting: ' + key)
    if limits['workers'] > 8 or not 0 <= limits['cacheMaxAgeHours'] <= 168:
        raise ValueError('Workers must be <= 8 and cache expiry <= 168 hours')
    if not 0 <= config['maxDropFraction'] < 1:
        raise ValueError('Invalid maxDropFraction')
    profiles = [p for p in config['profiles'] if p.get('enabled', True)]
    ids = set()
    for profile in profiles:
        pid = profile['id']
        if not re.fullmatch(r'[a-z][a-z0-9-]*', pid) or pid in ids or pid in ('adguard', 'report', 'manifest'):
            raise ValueError('Invalid or duplicate profile id: ' + pid)
        ids.add(pid)
        if profile['kind'] not in ('blocklist', 'allowlist') or not profile['sourceIds']:
            raise ValueError('Invalid profile kind or empty source list: ' + pid)
        if type(profile.get('coverageOptimization', True)) is not bool:
            raise ValueError('coverageOptimization must be a boolean: ' + pid)
        families, representations = set(), set()
        if len(profile['sourceIds']) != len(set(profile['sourceIds'])):
            raise ValueError('Duplicate source in profile: ' + pid)
        for sid in profile['sourceIds']:
            if sid not in sources:
                raise ValueError('Unknown source: ' + sid)
            source = sources[sid]
            validate_source_origin(source)
            if not source.get('eligibleForSubscription') or source['status'] != 'checked':
                raise ValueError('Source needs review before selection: ' + sid)
            if (source['role'] == 'independent_allowlist') != (profile['kind'] == 'allowlist'):
                raise ValueError('Allowlist and blocking sources must be separate: ' + pid)
            for key, seen in [('variantFamily', families), ('representationGroup', representations)]:
                value = source.get(key)
                if value and value in seen:
                    raise ValueError(f'{pid}: multiple versions of {key} {value}')
                if value:
                    seen.add(value)
            if profile.get('axis') == 'strength' and source['strength']['value'] != profile['value']:
                raise ValueError('Upstream strength mismatch: ' + pid)
            if profile.get('axis') == 'region':
                focus = source.get('regionalFocus', {})
                if (focus.get('value') != profile['value'] or focus.get('basis') != 'repository_documentation'
                        or focus.get('scope') != 'dns'):
                    raise ValueError('Unverified DNS region classification: ' + pid)
    if config['defaultProfile'] not in ids or next(p for p in profiles if p['id'] == config['defaultProfile'])['kind'] != 'blocklist':
        raise ValueError('Default profile must be an enabled blocklist')
    return config, profiles, sources


def download_source(source, limits, cache, previous, max_drop, allow_large_drop, validator=None):
    key = hashlib.sha256(source['url'].encode()).hexdigest()
    raw_path, meta_path = cache / (key + '.txt'), cache / (key + '.json')
    state, cached_meta = 'fresh', None
    try:
        body = fetch(source['url'], limits['timeoutSeconds'], limits['retries'])
        downloaded = utcnow()
    except OSError as error:
        if not meta_path.exists() or not raw_path.exists():
            raise
        cached_meta = read_json(meta_path)
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(cached_meta['downloadedUtc'])).total_seconds()/3600
        if age < 0 or age > limits['cacheMaxAgeHours']:
            raise ValueError('Download failed and cache expired: ' + str(error)) from error
        body = raw_path.read_text(encoding='utf-8')
        if (cached_meta['url'] != source['url'] or
                hashlib.sha256(body.encode()).hexdigest() != cached_meta['bodySha256']):
            raise ValueError('Cache identity or checksum mismatch') from error
        downloaded, state = cached_meta['downloadedUtc'], 'cached'
        print(f"WARNING: validated cache fallback for {source['name']} ({age:.1f} hours old)", flush=True)
    rules, stats = parse_source(body, source['role'])
    minimum = max(1, int((source['dnsBlocks'] + source['dnsExceptions']) * .5))
    if stats['accepted'] < minimum:
        raise ValueError(f"Source below minimum {minimum}: {stats['accepted']}")
    if previous and previous.get('accepted') and not allow_large_drop and stats['accepted'] < previous['accepted'] * (1-max_drop):
        raise ValueError(f"Source decreased over {max_drop:.0%}: {source['name']}")
    engine = validate_engine(rules, validator)
    if engine:
        stats['validatedEngine'] = engine
    if state == 'fresh':
        cache.mkdir(parents=True, exist_ok=True)
        atomic_write(raw_path, body)
        atomic_write(meta_path, json_text(dict(url=source['url'], downloadedUtc=downloaded,
                                              bodySha256=hashlib.sha256(body.encode()).hexdigest())))
    return dict(rules=rules, stats=dict(id=source['id'], name=source['name'], url=source['url'],
        repository=source['repository'], repositoryAccount=source['repositoryAccount'],
        downloadState=state, **stats), downloadedUtc=downloaded)


def personal_rules(custom):
    result = set()
    for filename, allow in [('block.txt', False), ('allow.txt', True)]:
        path = custom / filename
        for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            for rule in parse_dns_line(line):
                if rule == UNSUPPORTED:
                    raise ValueError(f'Unsupported personal rule: {path}:{number}')
                if allow:
                    rule = '@@' + rule.removeprefix('@@').removesuffix('$important') + '$important'
                elif rule.startswith('@@'):
                    raise ValueError(f'Put personal exceptions in allow.txt: {path}:{number}')
                result.add(rule)
    return result


def profile_content(profile, rules, sources, stamp):
    clean = lambda text: str(text).replace('\r', ' ').replace('\n', ' ')
    header = [f"! Title: {clean(profile['name'])}", f'! Updated: {stamp}', '! Expires: 1 day',
              f'! Rules: {len(rules)}', '! Maintainer merges only; upstream rules belong to their authors.',
              '! DNS masks/regex preserved; exact Hosts scope and source exception priority retained.',
              '! Upstream licenses and notices: ../upstream/README.md (in the original repository).']
    for sid in profile['sourceIds']:
        source = sources[sid]
        header += [f"! Source: {clean(source['name'])} | {source['url']}",
                   f"! Repository: {source['repository']} | Account: {clean(source['repositoryAccount'])}"]
        if source.get('licenseEvidenceUrl'):
            header.append('! Upstream license: ' + source['licenseEvidenceUrl'])
    return '\n'.join(header + sorted(rules)) + '\n'


def index_content(profiles, published, default):
    rows = ['# 自动生成的 DNS 分类订阅', '',
            '本项目仅获取、合并与去重，上游规则由各原作者及贡献者维护；所属仓库账号不等于全部原创作者。原始订阅和仓库链接在每个规则文件头部及 manifest.json 中。', '',
            f'默认入口 [adguard.txt](adguard.txt) 对应 `{default}`。四个强度档位任选一个；国内优化及设备/用途组件按需搭配。综合版的来源含未分级组件，不宣称属于均衡或低误杀档位。', '',
            '独立白名单保持独立，在 AdGuard Home 的 DNS 白名单按需订阅；不默认加入全部黑名单。设备及服务限制组件不保证去广告效果，可能影响服务功能。', '',
            '| 分类 | 类型 | 条目 | 去除重复 | 去除覆盖条目 | 文件 | 状态 |',
            '| --- | --- | ---: | ---: | ---: | --- | --- |']
    for profile in profiles:
        item = published[profile['id']]
        kind = '白名单' if profile['kind'] == 'allowlist' else '黑名单（含原生放行例外）'
        status = {'ready': '可用', 'retained': '本次失败，保留旧版', 'failed': '未生成'}[item['status']]
        if item.get('usesCache'):
            status += '，使用缓存来源'
        file_link = f"[订阅]({profile['id']}.txt)" if item.get('totalRules') else '—'
        rows.append(f"| {profile['name']} | {kind} | {item.get('totalRules', '—')} | {item.get('duplicatesRemoved', '—')} | {item.get('coveredRemoved', '—')} | {file_link} | {status} |")
    if any(p['id'] == 'full' for p in profiles):
        rows += ['', '全量版 [full.txt](full.txt) 合并已核验、可兼容的 DNS 拦截来源，同系列强度取最高档、同一来源格式择一，并保留所选来源的原生放行例外和个人规则。包含设备及服务限制组件，独立白名单不并入；选源与排除依据见 [核验清单](../registry/full_selection.json)。']
    rows += ['', '条目数含拦截规则和原生放行例外，不是实际命中次数；统计不证明真实应用的低误杀或去广告效果。', '',
             '优化仅在同一拦截/放行动作、同一 important 优先级内移除被父域覆盖的简单条目；通配符和正则保持原样。Hosts 和纯域名保留精确匹配。', '',
             '完整构建统计与选源见 [manifest.json](manifest.json)。下载检查时间与缓存年龄记录在本地 .cache/last-run.json，不因检查时间变化重复提交相同订阅。']
    return '\n'.join(rows) + '\n'


def build(config_path, registry_path, output, custom, cache, allow_large_drop=False, validator=None, readme=None):
    with build_lock(cache):
        try:
            result = _build(config_path, registry_path, output, custom, cache, allow_large_drop, validator)
        except Exception as error:
            run = dict(checkedUtc=utcnow(), status='failed', error=str(error), sources={},
                       changedProfiles=[], failedProfiles=[], cacheSources=[])
            write_if_changed(cache / 'last-run.json', json_text(run))
            if readme is not None:
                update_readme(readme, run)
            raise
        if readme is not None:
            update_readme(readme, read_json(cache / 'last-run.json'))
        return result


def _build(config_path, registry_path, output, custom, cache, allow_large_drop, validator):
    config, profiles, sources = load_plan(config_path, registry_path)
    custom_rules = personal_rules(custom)  # validate before downloading anything
    validate_engine(custom_rules, validator)
    old = read_json(output / 'manifest.json') if (output / 'manifest.json').exists() else {}
    old_sources, old_profiles = old.get('sources', {}), old.get('profiles', {})
    selected = sorted({sid for p in profiles for sid in p['sourceIds']})
    fetched, errors, runtime = {}, {}, {}
    print(f'Building {len(profiles)} profiles from {len(selected)} unique sources', flush=True)
    with ThreadPoolExecutor(max_workers=config['download']['workers']) as pool:
        futures = {pool.submit(download_source, sources[sid], config['download'], cache / 'sources',
            old_sources.get(sid), config['maxDropFraction'], allow_large_drop, validator): sid for sid in selected}
        for future in as_completed(futures):
            sid = futures[future]
            try:
                fetched[sid] = future.result()
                item = fetched[sid]
                runtime[sid] = dict(status=item['stats']['downloadState'], downloadedUtc=item['downloadedUtc'],
                                    accepted=item['stats']['accepted'])
                print(f"OK {sources[sid]['name']}: {item['stats']['accepted']} ({item['stats']['downloadState']})", flush=True)
            except Exception as error:
                errors[sid] = str(error)
                runtime[sid] = dict(status='failed', error=str(error))
                print(f"FAILED {sources[sid]['name']}: {error}", file=sys.stderr, flush=True)
    output.mkdir(parents=True, exist_ok=True)
    published, changed, failed, new_contents = {}, [], [], {}
    for profile in profiles:
        pid = profile['id']
        try:
            missing = [sid for sid in profile['sourceIds'] if sid in errors]
            if missing:
                raise ValueError('; '.join(f'{sources[sid]["name"]}: {errors[sid]}' for sid in missing))
            merged, entries = set(), 0
            for sid in profile['sourceIds']:
                source_rules = fetched[sid]['rules']
                merged.update(source_rules)
                entries += fetched[sid]['stats']['parsedEntries']
            if profile.get('includeCustom', False):
                if profile['kind'] != 'blocklist':
                    raise ValueError('Personal blocking rules cannot be added to an allowlist')
                merged.update(custom_rules)
                entries += len(custom_rules)
            unique_count = len(merged)
            optimized, covered = optimize_rules(merged) if profile.get('coverageOptimization', True) else (merged, 0)
            previous = old_profiles.get(pid, {})
            if (previous.get('totalRules') and not allow_large_drop
                    and len(optimized) < previous['totalRules'] * (1-config['maxDropFraction'])):
                raise ValueError('Profile rule count decreased over configured limit')
            identity = json_text(dict(formatVersion=2, profile=profile, sources=[dict(id=sid, url=sources[sid]['url'],
                name=sources[sid]['name'], repository=sources[sid]['repository'],
                account=sources[sid]['repositoryAccount'], licenseEvidenceUrl=sources[sid].get('licenseEvidenceUrl'))
                for sid in profile['sourceIds']]))
            digest = hashlib.sha256((identity + '\n'.join(sorted(optimized))).encode()).hexdigest()
            stamp = previous.get('updatedUtc') if previous.get('contentDigest') == digest else utcnow()
            stamp = stamp or utcnow()
            content = profile_content(profile, optimized, sources, stamp)
            new_contents[pid] = content
            published[pid] = dict(name=profile['name'], kind=profile['kind'], axis=profile['axis'],
                value=profile.get('value'), sourceIds=profile['sourceIds'], status='ready',
                updatedUtc=stamp, contentDigest=digest, totalRules=len(optimized),
                blockingRules=sum(not rule.startswith('@@') for rule in optimized),
                exceptionRules=sum(rule.startswith('@@') for rule in optimized),
                duplicatesRemoved=entries-unique_count, coveredRemoved=covered,
                fileSha256=hashlib.sha256(content.encode('utf-8')).hexdigest(),
                validatedEngine='AdguardTeam/urlfilter v0.23.4' if validator else None,
                usesCache=any(fetched[sid]['stats']['downloadState'] == 'cached' for sid in profile['sourceIds']))
            print(f'PROFILE {pid}: {len(optimized)} rules; duplicates={entries-unique_count}, covered={covered}', flush=True)
        except Exception as error:
            failed.append(pid)
            retained = old_profiles.get(pid, {}) if (output / (pid + '.txt')).exists() else {}
            published[pid] = dict(retained, name=retained.get('name', profile['name']),
                                  kind=retained.get('kind', profile['kind']),
                                  sourceIds=retained.get('sourceIds', []), requestedSourceIds=profile['sourceIds'],
                                  status='retained' if retained else 'failed', error=str(error))
            print(f'RETAIN {pid}: {error}', file=sys.stderr, flush=True)
    # Validate/prepare every profile before replacing any subscription file.
    for pid, content in new_contents.items():
        if write_if_changed(output / (pid + '.txt'), content):
            changed.append(pid)
    public_sources = {sid: fetched[sid]['stats'] if sid in fetched else
                      dict(old_sources.get(sid, {}), status='failed', error=errors[sid]) for sid in selected}
    manifest = dict(schemaVersion=1, defaultProfile=config['defaultProfile'], sources=public_sources, profiles=published)
    write_if_changed(output / 'manifest.json', json_text(manifest))
    write_if_changed(output / 'README.md', index_content(profiles, published, config['defaultProfile']))
    default = config['defaultProfile']
    if default in new_contents:
        write_if_changed(output / 'adguard.txt', new_contents[default])
        summary = dict(updatedUtc=published[default]['updatedUtc'], totalRules=published[default]['totalRules'],
                       defaultProfile=default, sources=[public_sources[sid] for sid in published[default]['sourceIds']])
        write_if_changed(output / 'report.json', json_text(summary))
    run = dict(checkedUtc=utcnow(), status='failed' if failed else 'success', profileCount=len(profiles),
               sources=runtime, changedProfiles=changed, failedProfiles=failed,
               cacheSources=[sid for sid, item in runtime.items() if item['status'] == 'cached'])
    write_if_changed(cache / 'last-run.json', json_text(run))
    print(f'Completed: {len(profiles)-len(failed)} ready, {len(failed)} failed/retained, {len(changed)} changed', flush=True)
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'profiles.json')
    parser.add_argument('--registry', type=Path, default=ROOT / 'registry/sources.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--custom', type=Path, default=ROOT / 'custom')
    parser.add_argument('--cache', type=Path, default=ROOT / '.cache')
    parser.add_argument('--readme', type=Path, default=ROOT / 'README.md', help='Update the marked README build-status block')
    parser.add_argument('--allow-large-drop', action='store_true', help='Use only after reviewing an upstream count decrease')
    parser.add_argument('--validator', type=Path, default=os.environ.get('DNS_RULE_VALIDATOR'),
                        help='Path to the pinned AdGuard DNS rule validator (mandatory in CI)')
    args = parser.parse_args()
    try:
        return build(args.config, args.registry, args.output, args.custom, args.cache,
                     args.allow_large_drop, args.validator, args.readme)
    except KeyboardInterrupt:
        print('Stopped by user; completed outputs remain available.', file=sys.stderr)
        return 130
    except Exception as error:
        print(f'Build failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
