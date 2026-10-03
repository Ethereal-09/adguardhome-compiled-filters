"""Stage, audit and publish each DNS/mihomo profile independently."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from build_filters import (ROOT, build, build_lock, index_content, json_text, load_plan,
                           read_json, utcnow, write_if_changed)
from export_mihomo import MIHOMO_VERSION, export, index_content as mihomo_index
from validate_subscriptions import audit
from workflow_status import DEFAULT_REPOSITORY, read_optional, update_readme


def retain_profile(old, target, pid, error):
    item = old.get('profiles', {}).get(pid, {})
    path = target / (pid + '.txt')
    if item and path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == item.get('fileSha256'):
        return dict(item, status='retained', error=error)
    return dict(name=item.get('name', pid), kind=item.get('kind', 'blocklist'),
                sourceIds=[], status='failed', error=error)


def changes(before, after):
    def rules(path):
        return {line for line in path.read_text(encoding='utf-8').splitlines() if line and not line.startswith('!')} if path.exists() else set()
    previous, current = rules(before), rules(after)
    return dict(added=len(current-previous), removed=len(previous-current))


def check_compatibility(path, validator, hosts):
    """Check configured service samples with the real engine before publication."""
    if not hosts:
        return
    rules = [line for line in path.read_text(encoding='utf-8').splitlines()
             if line and not line.startswith('!')]
    result = subprocess.run([str(validator), '-match'],
        input=json_text([dict(rules=rules, hosts=hosts)]), text=True, encoding='utf-8',
        capture_output=True, check=True, timeout=120)
    decisions = json.loads(result.stdout)[0]
    blocked = [host for host, decision in zip(hosts, decisions, strict=True) if decision]
    if blocked:
        raise ValueError('Compatibility samples blocked: ' + ', '.join(blocked))


def prune_retired(output, old, old_mihomo, active):
    """Only remove retired manifest-owned files; preserve unknown user artifacts."""
    root = output.resolve()
    retired = set(old.get('profiles', {})) - set(active)
    for pid in retired:
        paths = [output / (pid + '.txt')]
        previous = old_mihomo.get('profiles', {}).get(pid, {})
        paths += [output / 'mihomo' / p['file'] for p in previous.get('providers', {}).values()]
        paths += [output / 'mihomo' / (pid + suffix + '.yaml') for suffix in ('', '-boki', '-ghfast')]
        for path in paths:
            if not path.resolve().is_relative_to(root):
                raise ValueError('Retired output escapes publication directory')
            path.unlink(missing_ok=True)
    return sorted(retired)


def publish(config_path, registry_path, output, custom, cache, validator, binary,
            readme=None, repository=DEFAULT_REPOSITORY, allow_reviewed_changes=False):
    config, profiles, _ = load_plan(config_path, registry_path)
    with build_lock(cache / 'publication'), tempfile.TemporaryDirectory(dir=cache, prefix='publication-') as folder:
        stage = Path(folder) / 'dns'
        if output.exists():
            stage.mkdir()
            for path in output.iterdir():
                if path.is_file() and path.suffix in ('.txt', '.json', '.md'):
                    shutil.copy2(path, stage / path.name)
        else:
            stage.mkdir()
        old = read_optional(output / 'manifest.json')
        old_mihomo = read_optional(output / 'mihomo/manifest.json')
        failures, dns_ok, mi_ok, deltas = {}, {}, {}, {}
        build(config_path, registry_path, stage, custom, cache, allow_reviewed_changes, validator)
        manifest = read_json(stage / 'manifest.json')
        run = read_json(cache / 'last-run.json')
        for profile in profiles:
            pid = profile['id']
            try:
                item = manifest['profiles'][pid]
                if item['status'] != 'ready':
                    raise ValueError(item.get('error', 'Profile is not ready'))
                result = audit(stage, config_path, registry_path, validator, {pid}, check_alias=False)
                check_compatibility(stage / (pid + '.txt'), validator, config.get('compatibilityHosts', []))
                result['profiles'][pid]['compatibilityHosts'] = config.get('compatibilityHosts', [])
                dns_ok[pid] = result['profiles'][pid]
                deltas[pid] = changes(output / (pid + '.txt'), stage / (pid + '.txt'))
            except Exception as error:
                failures[pid] = dict(dns=str(error))
                manifest['profiles'][pid] = retain_profile(old, output, pid, str(error))
                if manifest['profiles'][pid]['status'] == 'retained':
                    shutil.copy2(output / (pid + '.txt'), stage / (pid + '.txt'))
                else:
                    (stage / (pid + '.txt')).unlink(missing_ok=True)
        write_if_changed(stage / 'manifest.json', json_text(manifest))
        mi_stage = Path(folder) / 'mihomo'

        def convert(selected, destination):
            subset = dict(config, profiles=[p for p in profiles if p['id'] in selected])
            subset_path = Path(folder) / 'selected.json'
            subset_path.write_text(json_text(subset), encoding='utf-8')
            return export(stage, destination, subset_path, binary, repository)

        # Normally validate the whole successful batch once. A conversion failure
        # falls back to individual profiles, so one regex cannot stop all exports.
        if dns_ok:
            try:
                converted = convert(set(dns_ok), mi_stage)
                mi_ok.update(converted['profiles'])
            except Exception as error:
                print('Batch mihomo validation failed; isolating profiles: ' + str(error), flush=True)
                for pid in dns_ok:
                    destination = Path(folder) / ('mi-' + pid)
                    try:
                        converted = convert({pid}, destination)
                        mi_ok[pid] = converted['profiles'][pid]
                        mi_stage.mkdir(exist_ok=True)
                        for path in destination.iterdir():
                            if path.name not in ('manifest.json', 'README.md'):
                                shutil.copy2(path, mi_stage / path.name)
                    except Exception as profile_error:
                        failures.setdefault(pid, {})['mihomo'] = str(profile_error)
        # Preserve previously validated mihomo data independently of the DNS
        # platform. Explicitly identify mismatched/retained inputs in metadata.
        mi_profiles = {}
        for profile in profiles:
            pid = profile['id']
            if pid in mi_ok:
                mi_profiles[pid] = dict(mi_ok[pid], status='ready')
            elif pid in old_mihomo.get('profiles', {}):
                previous = old_mihomo['profiles'][pid]
                try:
                    for provider in previous['providers'].values():
                        path = output / 'mihomo' / provider['file']
                        if hashlib.sha256(path.read_bytes()).hexdigest() != provider['sha256']:
                            raise ValueError('Retained mihomo checksum mismatch')
                    for suffix in ('', '-boki', '-ghfast'):
                        if not (output / 'mihomo' / (pid + suffix + '.yaml')).is_file():
                            raise ValueError('Retained mihomo configuration is missing')
                    mi_profiles[pid] = dict(previous, status='retained',
                        error=failures.get(pid, {}).get('mihomo', 'DNS input retained'))
                except Exception as error:
                    failures.setdefault(pid, {})['mihomo'] = str(error)
            else:
                failures.setdefault(pid, {})['mihomo'] = 'No validated version available'

        # No output is touched until its engine validation is finished.
        output.mkdir(parents=True, exist_ok=True)
        for pid in dns_ok:
            shutil.copy2(stage / (pid + '.txt'), output / (pid + '.txt'))
        default = config['defaultProfile']
        if default in dns_ok:
            shutil.copy2(stage / (default + '.txt'), output / 'adguard.txt')
        write_if_changed(output / 'manifest.json', json_text(manifest))
        write_if_changed(output / 'README.md', index_content(profiles, manifest['profiles'], default))
        mi_output = output / 'mihomo'
        mi_output.mkdir(exist_ok=True)
        if mi_stage.exists():
            for path in mi_stage.iterdir():
                if path.name not in ('manifest.json', 'README.md'):
                    shutil.copy2(path, mi_output / path.name)
        mi_manifest = dict(schemaVersion=2, configVersion=2, profiles=mi_profiles,
            engine='mihomo ' + MIHOMO_VERSION, validatedProviders=sum(len(p['providers']) for p in mi_ok.values()),
            sourceManifestSha256=hashlib.sha256((output / 'manifest.json').read_bytes()).hexdigest())
        write_if_changed(mi_output / 'manifest.json', json_text(mi_manifest))
        write_if_changed(mi_output / 'README.md', mihomo_index(mi_profiles))
        report = dict(status='partial' if failures and (dns_ok or mi_ok) else 'failed' if failures else 'success',
            checkedUtc=utcnow(), dnsValidated=list(dns_ok), mihomoValidated=list(mi_ok),
            compatibilityHosts=config.get('compatibilityHosts', []),
            failures=failures, changes=deltas, sourceChanges={sid: {
                key: dict(previous=old.get('sources', {}).get(sid, {}).get(key), current=stats.get(key))
                for key in ('accepted', 'blockingRules', 'exceptionRules')}
                for sid, stats in manifest['sources'].items()})
        old_publication = read_optional(output / 'publication.json')
        if len(dns_ok) == len(profiles) and len(mi_ok) == len(profiles):
            report['retiredProfiles'] = prune_retired(output, old, old_mihomo, manifest['profiles'])
        if dns_ok or mi_ok:
            report['publishedUtc'] = report['checkedUtc']
        elif old_publication.get('publishedUtc'):
            report['publishedUtc'] = old_publication['publishedUtc']
        write_if_changed(output / 'publication.json', json_text(report))
        write_if_changed(cache / 'publish-audit.json', json_text(dict(status=report['status'], profiles=dns_ok, failures=failures)))
        if readme is not None:
            update_readme(readme, run, config=config, manifest=manifest, registry=read_json(registry_path),
                          repository=repository, mihomo_manifest=mi_manifest, publication=report)
        print(f"PUBLICATION {report['status']}: DNS {len(dns_ok)}/{len(profiles)}, mihomo {len(mi_ok)}/{len(profiles)}", flush=True)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'profiles.json')
    parser.add_argument('--registry', type=Path, default=ROOT / 'registry/sources.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--custom', type=Path, default=ROOT / 'custom')
    parser.add_argument('--cache', type=Path, default=ROOT / '.cache')
    parser.add_argument('--readme', type=Path, default=ROOT / 'README.md')
    parser.add_argument('--validator', type=Path, default=os.environ.get('DNS_RULE_VALIDATOR'), required=not os.environ.get('DNS_RULE_VALIDATOR'))
    parser.add_argument('--mihomo', type=Path, default=os.environ.get('MIHOMO_BINARY'), required=not os.environ.get('MIHOMO_BINARY'))
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY', DEFAULT_REPOSITORY))
    parser.add_argument('--allow-reviewed-changes', action='store_true', help='Bypass count guards only after reviewing upstream changes')
    args = parser.parse_args()
    try:
        report = publish(args.config, args.registry, args.output, args.custom, args.cache,
            args.validator, args.mihomo, args.readme, args.repository, args.allow_reviewed_changes)
        # Partial updates are committed first; Actions reports them as a failure
        # in its final step so the maintainer still receives a failure signal.
        return 0 if report['dnsValidated'] or report['mihomoValidated'] else 1
    except Exception as error:
        report = dict(status='failed', checkedUtc=utcnow(), error=str(error), dnsValidated=[], mihomoValidated=[])
        write_if_changed(args.cache / 'publish-audit.json', json_text(report))
        update_readme(args.readme, report, 'failure', 'failure')
        print('Publication failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
