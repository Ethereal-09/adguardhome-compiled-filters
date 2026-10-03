"""Recheck reviewed original subscriptions with the same parser and engine used to build."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os

from build_filters import (ROOT, build_lock, download_source, json_text, read_json,
                           utcnow, validate_source_origin, write_if_changed)


def refresh(catalog, registry, cache, validator):
    reviewed = read_json(catalog)
    entries = reviewed['sources']
    if len(entries) != len({s['url'] for s in entries}) or len(entries) != len({s['id'] for s in entries}):
        raise ValueError('Duplicate reviewed source URL or ID')
    previous = {s['id']: s for s in read_json(registry)['sources']} if registry.exists() else {}
    limits = dict(timeoutSeconds=45, retries=3, workers=4, cacheMaxAgeHours=72)

    def inspect(entry):
        source = dict(entry)
        old = previous.get(source['id'], {})
        source.update(dnsBlocks=old.get('dnsBlocks', 0), dnsExceptions=old.get('dnsExceptions', 0))
        try:
            validate_source_origin(source)
            if source.get('lifecycle') == 'discontinued_by_upstream':
                raise ValueError('上游明确停止更新，保留登记，不进入订阅。')
            baseline = {'accepted': source['dnsBlocks'] + source['dnsExceptions']} if old.get('status') == 'checked' else None
            fetched = download_source(source, limits, cache / 'sources', baseline, .3, False, validator)
            rules, stats = fetched['rules'], fetched['stats']
            exceptions = sum(rule.startswith('@@') for rule in rules)
            source.update(status='checked', eligibleForSubscription=True, checkedUtc=utcnow(),
                dnsBlocks=len(rules)-exceptions, dnsExceptions=exceptions,
                unsupported=stats['unsupported'], unsupportedExamples=stats['unsupportedExamples'],
                compatibility='dns_subset' if stats['unsupported'] else 'supported_dns_syntax',
                kind='independent_allowlist' if source['role']=='independent_allowlist' else
                    'mixed_filter' if exceptions else 'blocklist',
                downloadState=stats['downloadState'], downloadedUtc=fetched['downloadedUtc'],
                validatedEngine=stats.get('validatedEngine'), outputs={})
            print(f"CHECKED {source['name']}: {len(rules)} ({stats['downloadState']})", flush=True)
        except Exception as error:
            source.update(status='failed', eligibleForSubscription=False, checkedUtc=utcnow(),
                          error=str(error), reviewReason=str(error), outputs={})
            print(f"EXCLUDED {source['name']}: {error}", flush=True)
        return source

    with build_lock(cache), ThreadPoolExecutor(max_workers=4) as pool:
        sources = list(pool.map(inspect, entries))
        accepted = [s for s in sources if s['eligibleForSubscription']]
        summary = dict(sources=len(sources), checked=len(accepted), failed=len(sources)-len(accepted),
                       originalProjects=len({s['repository'] for s in sources}),
                       kinds=dict(Counter(s['kind'] for s in accepted)))
        data = dict(schemaVersion=1, generatedUtc=utcnow(), summary=summary, sources=sources,
                    excludedSources=reviewed.get('unresolvedLinks', []),
                    countNote='逐来源计数，跨来源重叠；生成订阅由 profiles.json 明确选择。')
        write_if_changed(registry, json_text(data))
        rows = ['# AdGuard Home 来源登记', '',
            f"最近核验：{data['generatedUtc']}（UTC）。共 {len(sources)} 个原始文件，{len(accepted)} 个通过完整下载、保守解析和 AdGuard 引擎校验。", '',
            '上游署名、用途、强度、地域和证据保存在 [reviewed_sources.json](reviewed_sources.json)；当前兼容结果见 [sources.json](sources.json)，实际组合见 [profiles.json](../profiles.json)。', '',
            '对浏览器条件、URL 路径和脚本语法不做域名扩大转换。无法保留网络放行例外或 badfilter 的来源整份排除。DNS 黑名单保留其原生例外；独立白名单按用途另行订阅。', '',
            '中文或中国地区依据保存在 selectionEvidence / regionalFocus；语言不等于域名地区，也不保证低误杀。当前订阅以 dist/ 和 manifest.json 为准。', '',
            '| 原始来源 | 分类 | DNS 拦截 | DNS 例外 | 结果 |', '| --- | --- | ---: | ---: | --- |']
        for source in sources:
            state = ('可选；'+source['downloadState']) if source['eligibleForSubscription'] else source['error']
            state = state.replace('|', '\\|').replace('\n', ' ')
            rows.append(f"| [{source['name']}]({source['url']}) | {', '.join(source['categories'])} | {source.get('dnsBlocks', 0) if source['eligibleForSubscription'] else '—'} | {source.get('dnsExceptions', 0) if source['eligibleForSubscription'] else '—'} | {state} |")
        rows += ['', '## 重新核验', '', '```powershell',
            '.\\.venv\\Scripts\\python.exe refresh_source_registry.py --validator .cache\\dns-rule-validator.exe', '```', '',
            '每日构建直接读取已选来源，每次重新下载、检查例外、异常数量下降和引擎兼容性；不会自动启用新发现的订阅源。', '']
        write_if_changed(registry.parent/'README.md', '\n'.join(rows))
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=ROOT/'registry/reviewed_sources.json')
    parser.add_argument('--registry', type=Path, default=ROOT/'registry/sources.json')
    parser.add_argument('--cache', type=Path, default=ROOT/'.cache')
    parser.add_argument('--validator', type=Path, default=os.environ.get('DNS_RULE_VALIDATOR'))
    args = parser.parse_args()
    if not args.validator:
        parser.error('--validator or DNS_RULE_VALIDATOR is required')
    refresh(args.catalog, args.registry, args.cache, args.validator)


if __name__ == '__main__':
    main()
