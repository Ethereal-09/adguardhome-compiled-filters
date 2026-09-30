"""Consolidate all user-provided source catalogs without enabling subscriptions."""
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def main():
    entries = {}
    references = [
        dict(name='217heidai/adblockfilters', url='https://github.com/217heidai/adblockfilters'),
        dict(name='zhuanshenlikaini/AdguardHome-Rules', url='https://github.com/zhuanshenlikaini/AdguardHome-Rules'),
        dict(name='hululu1068/AdGuard-Rule', url='https://github.com/hululu1068/AdGuard-Rule'),
        dict(name='广告过滤规则订阅中心（仅提取 DNS 段）', url='https://adguardfilters-chinese.pages.dev/'),
    ]

    def add(name, url, origin, **metadata):
        item = entries.setdefault(url, dict(names=[], url=url, occurrences=[], kind='未检查'))
        if name not in item['names']:
            item['names'].append(name)
        item['occurrences'].append(dict(origin=origin, name=name, **metadata))

    for source in read('upstream_sources.json'):
        add(source['name'], source['url'], '16 个来源表', role='原始订阅',
            suppliedType=source['type'], listedUpdateDate=source['listedUpdateDate'])
        for number, mirror in enumerate(source['mirrors'], 1):
            add(source['name'], mirror, '16 个来源表', role=f'加速链接{number}',
                originalUrl=source['url'])
    for source in read('organized/sources.json'):
        add(source['name'], source['url'], '30 条 AdGuard Home 配置', role='订阅',
            originallyEnabled=source['enabled'])
    for source in read('dns_section_sources.json')['sources']:
        add(source['name'], source['url'], '网页 DNS 过滤器段', role='主订阅')
        for backup in source['backupUrls']:
            add(source['name'], backup, '网页 DNS 过滤器段', role='备用订阅', originalUrl=source['url'])
    # These are previous inspection snapshots, not a fresh availability check.
    for audit_path in ('source_audit.json', 'organized/sources.json'):
        for audit in read(audit_path):
            item = entries.get(audit['url'])
            if not item:
                continue
            item['inspectionSnapshot'] = dict(auditFile=audit_path, **audit)
            if audit['status'] != 'checked':
                item['kind'] = '未验证成功'
            elif audit.get('exceptionRules', 0):
                item['kind'] = '拦截为主，含放行例外'
            else:
                item['kind'] = '拦截为主，未见放行例外'
    for item in entries.values():
        parsed = urlparse(item['url'])
        host = parsed.hostname or ''
        parts = parsed.path.strip('/').split('/')
        if host in ('raw.githubusercontent.com', 'gitee.com'):
            item['attribution'] = f'仓库所属账号：{parts[0]}'
        elif host.endswith('jsdelivr.net') and len(parts) >= 2 and parts[0] == 'gh':
            item['attribution'] = f'链接所指仓库账号：{parts[1]}'
        else:
            item['attribution'] = f'链接所在网站：{host}'
    output = ROOT / 'catalog'
    output.mkdir(exist_ok=True)
    primary = [item for item in entries.values() if any(o['role'] in ('原始订阅', '订阅', '主订阅') for o in item['occurrences'])]
    auxiliary = [item for item in entries.values() if item not in primary]
    (output / 'sources.json').write_text(json.dumps(dict(referenceProjects=references, sources=list(entries.values())), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, items in [('subscription_links.txt', primary), ('mirror_links.txt', auxiliary), ('all_links.txt', list(entries.values()))]:
        (output / name).write_text('\n'.join(item['url'] for item in items) + '\n', encoding='utf-8')
    lines = ['# 用户提供的全部规则来源', '',
             f'汇总 16 个来源表、30 条配置和网页 DNS 段的 14 个过滤器。按完整 URL 去重后，共 **{len(primary)} 个主订阅链接**、**{len(auxiliary)} 个仅作为加速/备用的链接**，合计 **{len(entries)} 个规则链接**。另列出 4 个参考项目/页面。', '',
             '去重只按完整 URL；同一规则的版本、格式、域名及分支不同，均分别保留。没有自动启用全部来源，也没有修改 config.json。', '',
             '黑白分类引用此前下载检查的快照，没有在本次重新下载。未检查不能当作黑名单或白名单已确认。含放行例外的过滤列表仍是混合过滤源，不能整体当白名单。', '',
             '署名字段只表示仓库归属或网站，不能证明原创作者。页面 CDN 地址保持原样，未臆造对应的“原始链接”。', '',
             '## 文件', '', '- [主订阅链接](subscription_links.txt)', '- [加速/备用链接](mirror_links.txt)', '- [全部规则链接](all_links.txt)', '- [完整结构化清单](sources.json)', '',
             '## 参考项目与页面', '']
    lines.extend(f"- [{r['name']}]({r['url']})" for r in references)
    lines += ['', '## 主订阅来源', '', '| 名称 | 仓库归属 / 网站 | 提供来源 | 原启用状态 | 此前检查结果 |', '| --- | --- | --- | --- | --- |']
    for item in primary:
        origins = '、'.join(dict.fromkeys(o['origin'] for o in item['occurrences']))
        flags = [o['originallyEnabled'] for o in item['occurrences'] if 'originallyEnabled' in o]
        enabled = ('启用' if flags[0] else '禁用') if flags else '未指定'
        lines.append(f"| [{' / '.join(item['names'])}]({item['url']}) | {item['attribution']} | {origins} | {enabled} | {item['kind']} |")
    lines += ['', '## 加速与备用链接', '', '这些链接可能指向第三方仓库保存的副本，链接所指账号不代表原规则作者。', '', '| 名称 | 链接 | 对应主订阅 |', '| --- | --- | --- |']
    for item in auxiliary:
        original = item['occurrences'][0]['originalUrl']
        lines.append(f"| {' / '.join(item['names'])} | [链接]({item['url']}) | [主订阅]({original}) |")
    (output / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(primary)} primary; {len(auxiliary)} auxiliary; {len(entries)} unique URLs; {len(references)} references')


if __name__ == '__main__':
    main()
