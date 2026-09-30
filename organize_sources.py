"""Inspect supplied subscriptions and separate supported DNS block/exception rules."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
from urllib.parse import urlparse

from update_rules import fetch, parse_line, UNSUPPORTED, atomic_write, ROOT

# Original enabled flags are preserved. Names are display names, not author claims.
DATA = '''0|Connershua|https://raw.githubusercontent.com/DivineEngine/AdGuardFilter/master/filter.txt
0|ADgk|https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt
0|大圣净化|https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts
0|乘风广告过滤规则|https://gitee.com/xinggsf/Adblock-Rule/raw/master/rule.txt
0|乘风视频广告过滤|https://gitee.com/xinggsf/Adblock-Rule/raw/master/mv.txt
0|CJX’s Annoyance List|https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt
0|AdAway default blocklist|https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt
1|AdGuard DNS filter|https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt
0|easylist|https://easylist.to/easylist/easylist.txt
0|easylistchina|https://easylist-downloads.adblockplus.org/easylistchina.txt
0|easyprivacy|https://easylist.to/easylist/easyprivacy.txt
0|fanboy-annoyance|https://easylist.to/easylist/fanboy-annoyance.txt
1|alexa|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/alexa
1|apple|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/apple
1|huawei|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/huawei
1|roku|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/roku
1|samsung|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/samsung
1|sonos|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/sonos
1|windows|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/windows
1|xiaomi|https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/xiaomi
0|Adblock Warning Removal List|https://easylist-downloads.adblockplus.org/antiadblockfilters.txt
0|I don't care about cookies|https://www.i-dont-care-about-cookies.eu/abp/
0|Perflyst and Dandelion Sprout's Smart-TV Blocklist|https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt
0|Dan Pollock's List|https://someonewhocares.org/hosts/zero/hosts
0|Scam Blocklist by DurableNapkin|https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt
0|Game Console Adblock List|https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt
0|Peter Lowe's List|https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext
0|NoCoin Filter List|https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt
0|Spam404|https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt
0|The Big List of Hacked Malware Web Sites|https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list'''


def inspect(source):
    blocks, allows = set(), set()
    stats = dict(source, status='checked', blockingRules=0, exceptionRules=0,
                 supportedBlocks=0, supportedAllows=0, unsupported=0)
    try:
        text = fetch(source['url'], 25, 1)
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith(('!', '#', '[')):
                continue
            exception = line.startswith('@@') or any(token in line for token in ('#@#', '#@?#', '#@$#'))
            stats['exceptionRules' if exception else 'blockingRules'] += 1
            for rule in parse_line(line):
                if rule == UNSUPPORTED:
                    stats['unsupported'] += 1
                elif rule.startswith('@@'):
                    allows.add(rule)
                else:
                    blocks.add(rule)
        stats['supportedBlocks'], stats['supportedAllows'] = len(blocks), len(allows)
    except Exception as error:
        stats['status'], stats['error'] = 'unverified', str(error)
    print(f"{source['name']}: {stats['status']} blocks={len(blocks)} allows={len(allows)}", flush=True)
    return stats, blocks, allows


def main():
    sources = []
    for line in DATA.splitlines():
        enabled, name, url = line.split('|', 2)
        host = urlparse(url).hostname
        owner = urlparse(url).path.strip('/').split('/')[0] if host in ('raw.githubusercontent.com', 'gitee.com') else host
        sources.append(dict(name=name, url=url, enabled=enabled == '1', repositoryOwnerOrHost=owner))
    output = ROOT / 'organized'
    output.mkdir(exist_ok=True)
    results = list(ThreadPoolExecutor(max_workers=4).map(inspect, sources))
    report = [item[0] for item in results]
    atomic_write(output / 'sources.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    rows = ['# 来源黑白名单整理', '', '按用户提供的 30 个来源检查，保留原启用状态；不改变 config.json。', '',
            '这些订阅用于过滤；其中的放行例外不是独立白名单订阅。仓库所属账号或网站不等于原创作者。', '',
            '| 来源 | 原状态 | 检查结果 | 拦截/其他规则行 | 放行例外行 | 支持的 DNS 拦截 | 支持的 DNS 放行 |',
            '| --- | --- | --- | ---: | ---: | ---: | ---: |']
    for s in report:
        status = '未验证' if s['status'] != 'checked' else ('拦截与例外混合' if s['exceptionRules'] else '拦截为主，未见例外')
        rows.append(f"| [{s['name']}]({s['url']}) | {'启用' if s['enabled'] else '禁用'} | {status} | {s['blockingRules']} | {s['exceptionRules']} | {s['supportedBlocks']} | {s['supportedAllows']} |")
    rows += ['', '## 输出文件', '',
             '- `all_blacklist.txt` / `all_whitelist.txt`：所有成功检查来源中支持的 DNS 拦截和放行条目，仅供整理参考。',
             '- `enabled_blacklist.txt` / `enabled_whitelist.txt`：仅原配置启用来源。',
             '- `enabled_adguard.txt`：原启用来源的拦截与放行合并结果。',
             '', '原始放行修饰符保持不变。浏览器规则、正则及其他不支持语法不导入 DNS 输出，数量见 sources.json。',
             '精确域名匹配保持精确，不扩大到子域名。不要将整个混合源加入 DNS 白名单。',
             '拦截/其他规则行的计数是语法初筛，不等于全部都适用于 DNS。未验证来源的零值表示未读取，不能视为无规则。']
    enabled_failed = [s['name'] for s in report if s['enabled'] and s['status'] != 'checked']
    for scope in ('all', 'enabled'):
        if scope == 'enabled' and enabled_failed:
            rows += ['', '启用来源下载失败，保留已有 enabled 输出，不发布缺失来源的结果：' + ', '.join(enabled_failed)]
            continue
        blocks, allows = set(), set()
        for stats, block, allow in results:
            if stats['status'] == 'checked' and (scope == 'all' or stats['enabled']):
                blocks.update(block)
                allows.update(allow)
        for label, rules in [('blacklist', blocks), ('whitelist', allows)]:
            atomic_write(output / f'{scope}_{label}.txt', '! Supported DNS rules extracted from supplied sources\n' + '\n'.join(sorted(rules)) + '\n')
        if scope == 'enabled':
            atomic_write(output / 'enabled_adguard.txt', '! Enabled supplied sources, with original exceptions\n' + '\n'.join(sorted(blocks | allows)) + '\n')
        print(f'{scope}: {len(blocks)} block rules, {len(allows)} exception rules')
    atomic_write(output / 'README.md', '\n'.join(rows) + '\n')


if __name__ == '__main__':
    main()
