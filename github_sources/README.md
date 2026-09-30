# GitHub 原仓库订阅核验

仅从用户链接和仓库明确的配置解析地址。GitHub API 核验仓库，实际下载核验文件。fork、非 GitHub 来源和失败链接跳过；不猜替代路径。

“原仓库”指直接规则项目，项目自身也可能整合其他上游；不声称仓库所属账号是全部规则的原创作者。

CDN 的 latest 通过仓库默认分支解析，相同路径实际下载成功才接受。不同版本各自保留。

核验配置已同步到项目根目录 config.json；此处保留核验快照。运行：

```powershell
.\.venv\Scripts\python.exe update_rules.py
```

确认后按订阅 URL 去重：27 个链接。

| 名称 | 原仓库 | 已验证订阅 | 支持的 DNS 规则数 |
| --- | --- | --- | ---: |
| AdGuard Chinese filter | [仓库](https://github.com/AdguardTeam/FiltersRegistry) | [订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | 5905 |
| AdGuard Mobile Ads filter | [仓库](https://github.com/AdguardTeam/AdguardFilters) | [订阅](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | 899 |
| AdRules DNS List | [仓库](https://github.com/Cats-Team/AdRules) | [订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 195932 |
| CJX's Annoyance List | [仓库](https://github.com/cjx82630/cjxlist) | [订阅](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | 115 |
| xinggsf mv | [仓库](https://github.com/xinggsf/Adblock-Plus-Rule) | [订阅](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | 27 |
| jiekouAD | [仓库](https://github.com/damengzhu/banad) | [订阅](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | 4512 |
| AWAvenue Ads Rule | [仓库](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [订阅](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 958 |
| DNS-Blocklists PRO mini | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) | 59779 |
| StevenBlack hosts | [仓库](https://github.com/StevenBlack/hosts) | [订阅](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | 74759 |
| ADgk | [仓库](https://github.com/banbendalao/ADgk) | [订阅](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt) | 3059 |
| 大圣净化 | [仓库](https://github.com/jdlingyu/ad-wars) | [订阅](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 1645 |
| AdAway default blocklist | [仓库](https://github.com/AdAway/adaway.github.io) | [订阅](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 6540 |
| Perflyst and Dandelion Sprout's Smart-TV Blocklist | [仓库](https://github.com/Perflyst/PiHoleBlocklist) | [订阅](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 149 |
| Scam Blocklist by DurableNapkin | [仓库](https://github.com/durablenapkin/scamblocklist) | [订阅](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 941 |
| Game Console Adblock List | [仓库](https://github.com/DandelionSprout/adfilt) | [订阅](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 9 |
| NoCoin Filter List | [仓库](https://github.com/hoshsadiq/adblock-nocoin-list) | [订阅](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt) | 47 |
| Spam404 | [仓库](https://github.com/Spam404/lists) | [订阅](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 8140 |
| The Big List of Hacked Malware Web Sites | [仓库](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) | [订阅](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 9 |
| HaGeZi Ultimate | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) | 287467 |
| HaGeZi Pro++ | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) | 251638 |
| HaGeZi Pro | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | 230960 |
| HaGeZi Normal | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) | 200319 |
| HaGeZi Badware Hoster | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | 1238 |
| HaGeZi DynDNS | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | 1538 |
| HaGeZi URL Shortener | [仓库](https://github.com/hagezi/dns-blocklists) | [订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) | 9982 |
| 1Hosts Lite | [仓库](https://github.com/badmojr/1Hosts) | [订阅](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | 102241 |
| 1Hosts Xtra | [仓库](https://github.com/badmojr/1Hosts) | [订阅](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) | 786132 |

## 跳过记录

| 名称 | 用户链接 | 原因 |
| --- | --- | --- |
| AdGuard Base filter | [链接](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) | Empty response or HTML instead of rules |
| AdGuard DNS filter | [链接](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| EasyList | [链接](https://easylist-downloads.adblockplus.org/easylist.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| EasyList China | [链接](https://easylist-downloads.adblockplus.org/easylistchina.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| EasyPrivacy | [链接](https://easylist-downloads.adblockplus.org/easyprivacy.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| OISD Basic | [链接](https://abp.oisd.nl/basic/) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| Pollock hosts | [链接](https://someonewhocares.org/hosts/hosts) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| Connershua | [链接](https://raw.githubusercontent.com/DivineEngine/AdGuardFilter/master/filter.txt) | 仓库核验失败：HTTP Error 404: Not Found |
| 乘风广告过滤规则 | [链接](https://gitee.com/xinggsf/Adblock-Rule/raw/master/rule.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| 乘风视频广告过滤 | [链接](https://gitee.com/xinggsf/Adblock-Rule/raw/master/mv.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| easylist | [链接](https://easylist.to/easylist/easylist.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| easyprivacy | [链接](https://easylist.to/easylist/easyprivacy.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| fanboy-annoyance | [链接](https://easylist.to/easylist/fanboy-annoyance.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| alexa | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/alexa) | HTTP Error 404: Not Found |
| apple | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/apple) | HTTP Error 404: Not Found |
| huawei | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/huawei) | HTTP Error 404: Not Found |
| roku | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/roku) | HTTP Error 404: Not Found |
| samsung | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/samsung) | HTTP Error 404: Not Found |
| sonos | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/sonos) | HTTP Error 404: Not Found |
| windows | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/windows) | HTTP Error 404: Not Found |
| xiaomi | [链接](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/xiaomi) | HTTP Error 404: Not Found |
| Adblock Warning Removal List | [链接](https://easylist-downloads.adblockplus.org/antiadblockfilters.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| I don't care about cookies | [链接](https://www.i-dont-care-about-cookies.eu/abp/) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| Dan Pollock's List | [链接](https://someonewhocares.org/hosts/zero/hosts) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| Peter Lowe's List | [链接](https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| AdGuard DNS | [链接](https://filters.adtidy.org/android/filters/15_optimized.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| AdGuard DNS | [链接](https://cdn.jsdelivr.net/gh/AdguardTeam/HostlistsRegistry@main/filters/general/filter_1_DnsFilter/filter.txt) | 仓库记录的上游不是 GitHub 原始链接，按要求跳过 |
| Anti-AD | [链接](https://anti-ad.net/easylist.txt) | 非 GitHub 原始链接或明确的 GitHub CDN 链接，按要求跳过 |
| HaGeZi Threat Intelligence Feeds | [链接](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/tif.txt) | Source exceeds 32 MiB limit |
| HaGeZi Most Abused TLDs | [链接](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/spam-tlds.txt) | 文件可下载，但没有当前程序支持的 DNS 规则 |
