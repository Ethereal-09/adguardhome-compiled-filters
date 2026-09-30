# 来源黑白名单整理

按用户提供的 30 个来源检查，保留原启用状态；不改变 config.json。

这些订阅用于过滤；其中的放行例外不是独立白名单订阅。仓库所属账号或网站不等于原创作者。

| 来源 | 原状态 | 检查结果 | 拦截/其他规则行 | 放行例外行 | 支持的 DNS 拦截 | 支持的 DNS 放行 |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| [Connershua](https://raw.githubusercontent.com/DivineEngine/AdGuardFilter/master/filter.txt) | 禁用 | 未验证 | 0 | 0 | 0 | 0 |
| [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt) | 禁用 | 拦截与例外混合 | 8944 | 172 | 3030 | 29 |
| [大圣净化](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 禁用 | 拦截为主，未见例外 | 1709 | 0 | 1645 | 0 |
| [乘风广告过滤规则](https://gitee.com/xinggsf/Adblock-Rule/raw/master/rule.txt) | 禁用 | 未验证 | 0 | 0 | 0 | 0 |
| [乘风视频广告过滤](https://gitee.com/xinggsf/Adblock-Rule/raw/master/mv.txt) | 禁用 | 未验证 | 0 | 0 | 0 | 0 |
| [CJX’s Annoyance List](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | 禁用 | 拦截与例外混合 | 1812 | 6 | 115 | 0 |
| [AdAway default blocklist](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 禁用 | 拦截为主，未见例外 | 6542 | 0 | 6540 | 0 |
| [AdGuard DNS filter](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | 启用 | 拦截与例外混合 | 176771 | 210 | 176018 | 11 |
| [easylist](https://easylist.to/easylist/easylist.txt) | 禁用 | 拦截与例外混合 | 63226 | 1097 | 44125 | 0 |
| [easylistchina](https://easylist-downloads.adblockplus.org/easylistchina.txt) | 禁用 | 拦截与例外混合 | 16954 | 1159 | 5746 | 11 |
| [easyprivacy](https://easylist.to/easylist/easyprivacy.txt) | 禁用 | 拦截与例外混合 | 55376 | 846 | 43155 | 4 |
| [fanboy-annoyance](https://easylist.to/easylist/fanboy-annoyance.txt) | 禁用 | 拦截与例外混合 | 20938 | 1025 | 235 | 1 |
| [alexa](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/alexa) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [apple](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/apple) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [huawei](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/huawei) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [roku](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/roku) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [samsung](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/samsung) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [sonos](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/sonos) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [windows](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/windows) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [xiaomi](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/xiaomi) | 启用 | 未验证 | 0 | 0 | 0 | 0 |
| [Adblock Warning Removal List](https://easylist-downloads.adblockplus.org/antiadblockfilters.txt) | 禁用 | 拦截与例外混合 | 2732 | 92 | 2334 | 0 |
| [I don't care about cookies](https://www.i-dont-care-about-cookies.eu/abp/) | 禁用 | 拦截与例外混合 | 11070 | 1 | 80 | 0 |
| [Perflyst and Dandelion Sprout's Smart-TV Blocklist](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 禁用 | 拦截与例外混合 | 154 | 9 | 140 | 9 |
| [Dan Pollock's List](https://someonewhocares.org/hosts/zero/hosts) | 禁用 | 拦截为主，未见例外 | 13095 | 0 | 13082 | 0 |
| [Scam Blocklist by DurableNapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 禁用 | 拦截为主，未见例外 | 951 | 0 | 941 | 0 |
| [Game Console Adblock List](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 禁用 | 拦截为主，未见例外 | 15 | 0 | 9 | 0 |
| [Peter Lowe's List](https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext) | 禁用 | 拦截为主，未见例外 | 3552 | 0 | 3552 | 0 |
| [NoCoin Filter List](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt) | 禁用 | 拦截与例外混合 | 308 | 8 | 47 | 0 |
| [Spam404](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 禁用 | 拦截为主，未见例外 | 8140 | 0 | 8140 | 0 |
| [The Big List of Hacked Malware Web Sites](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 禁用 | 拦截为主，未见例外 | 9 | 0 | 9 | 0 |

## 输出文件

- `all_blacklist.txt` / `all_whitelist.txt`：所有成功检查来源中支持的 DNS 拦截和放行条目，仅供整理参考。
- `enabled_blacklist.txt` / `enabled_whitelist.txt`：仅原配置启用来源。
- `enabled_adguard.txt`：原启用来源的拦截与放行合并结果。

原始放行修饰符保持不变。浏览器规则、正则及其他不支持语法不导入 DNS 输出，数量见 sources.json。
精确域名匹配保持精确，不扩大到子域名。不要将整个混合源加入 DNS 白名单。
拦截/其他规则行的计数是语法初筛，不等于全部都适用于 DNS。未验证来源的零值表示未读取，不能视为无规则。

启用来源下载失败，保留已有 enabled 输出，不发布缺失来源的结果：alexa, apple, huawei, roku, samsung, sonos, windows, xiaomi
