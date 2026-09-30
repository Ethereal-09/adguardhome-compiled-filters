# 用户提供的全部规则来源

汇总 16 个来源表、30 条配置和网页 DNS 段的 14 个过滤器。按完整 URL 去重后，共 **57 个主订阅链接**、**49 个仅作为加速/备用的链接**，合计 **106 个规则链接**。另列出 4 个参考项目/页面。

去重只按完整 URL；同一规则的版本、格式、域名及分支不同，均分别保留。没有自动启用全部来源，也没有修改 config.json。

黑白分类引用此前下载检查的快照，没有在本次重新下载。未检查不能当作黑名单或白名单已确认。含放行例外的过滤列表仍是混合过滤源，不能整体当白名单。

署名字段只表示仓库归属或网站，不能证明原创作者。页面 CDN 地址保持原样，未臆造对应的“原始链接”。

## 文件

- [主订阅链接](subscription_links.txt)
- [加速/备用链接](mirror_links.txt)
- [全部规则链接](all_links.txt)
- [完整结构化清单](sources.json)

## 参考项目与页面

- [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)
- [zhuanshenlikaini/AdguardHome-Rules](https://github.com/zhuanshenlikaini/AdguardHome-Rules)
- [hululu1068/AdGuard-Rule](https://github.com/hululu1068/AdGuard-Rule)
- [广告过滤规则订阅中心（仅提取 DNS 段）](https://adguardfilters-chinese.pages.dev/)

## 主订阅来源

| 名称 | 仓库归属 / 网站 | 提供来源 | 原启用状态 | 此前检查结果 |
| --- | --- | --- | --- | --- |
| [AdGuard Base filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) | 仓库所属账号：AdguardTeam | 16 个来源表 | 未指定 | 未验证成功 |
| [AdGuard Chinese filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | 仓库所属账号：AdguardTeam | 16 个来源表 | 未指定 | 拦截为主，含放行例外 |
| [AdGuard Mobile Ads filter](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | 仓库所属账号：AdguardTeam | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [AdGuard DNS filter](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | 链接所在网站：adguardteam.github.io | 16 个来源表、30 条 AdGuard Home 配置 | 启用 | 拦截为主，含放行例外 |
| [AdRules DNS List](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 仓库所属账号：Cats-Team | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [CJX's Annoyance List / CJX’s Annoyance List](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | 仓库所属账号：cjx82630 | 16 个来源表、30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [EasyList](https://easylist-downloads.adblockplus.org/easylist.txt) | 链接所在网站：easylist-downloads.adblockplus.org | 16 个来源表 | 未指定 | 拦截为主，含放行例外 |
| [EasyList China / easylistchina](https://easylist-downloads.adblockplus.org/easylistchina.txt) | 链接所在网站：easylist-downloads.adblockplus.org | 16 个来源表、30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [EasyPrivacy](https://easylist-downloads.adblockplus.org/easyprivacy.txt) | 链接所在网站：easylist-downloads.adblockplus.org | 16 个来源表 | 未指定 | 拦截为主，含放行例外 |
| [xinggsf mv](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | 仓库所属账号：xinggsf | 16 个来源表 | 未指定 | 拦截为主，含放行例外 |
| [jiekouAD](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | 仓库所属账号：damengzhu | 16 个来源表 | 未指定 | 拦截为主，含放行例外 |
| [AWAvenue Ads Rule](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 仓库所属账号：TG-Twilight | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [DNS-Blocklists PRO mini](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) | 仓库所属账号：hagezi | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [OISD Basic](https://abp.oisd.nl/basic/) | 链接所在网站：abp.oisd.nl | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [StevenBlack hosts](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | 仓库所属账号：StevenBlack | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [Pollock hosts](https://someonewhocares.org/hosts/hosts) | 链接所在网站：someonewhocares.org | 16 个来源表 | 未指定 | 拦截为主，未见放行例外 |
| [Connershua](https://raw.githubusercontent.com/DivineEngine/AdGuardFilter/master/filter.txt) | 仓库所属账号：DivineEngine | 30 条 AdGuard Home 配置 | 禁用 | 未验证成功 |
| [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt) | 仓库所属账号：banbendalao | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [大圣净化](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 仓库所属账号：jdlingyu | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [乘风广告过滤规则](https://gitee.com/xinggsf/Adblock-Rule/raw/master/rule.txt) | 仓库所属账号：xinggsf | 30 条 AdGuard Home 配置 | 禁用 | 未验证成功 |
| [乘风视频广告过滤](https://gitee.com/xinggsf/Adblock-Rule/raw/master/mv.txt) | 仓库所属账号：xinggsf | 30 条 AdGuard Home 配置 | 禁用 | 未验证成功 |
| [AdAway default blocklist](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 仓库所属账号：AdAway | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [easylist](https://easylist.to/easylist/easylist.txt) | 链接所在网站：easylist.to | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [easyprivacy](https://easylist.to/easylist/easyprivacy.txt) | 链接所在网站：easylist.to | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [fanboy-annoyance](https://easylist.to/easylist/fanboy-annoyance.txt) | 链接所在网站：easylist.to | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [alexa](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/alexa) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [apple](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/apple) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [huawei](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/huawei) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [roku](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/roku) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [samsung](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/samsung) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [sonos](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/sonos) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [windows](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/windows) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [xiaomi](https://raw.githubusercontent.com/nextdns/metadata/master/privacy/native/xiaomi) | 仓库所属账号：nextdns | 30 条 AdGuard Home 配置 | 启用 | 未验证成功 |
| [Adblock Warning Removal List](https://easylist-downloads.adblockplus.org/antiadblockfilters.txt) | 链接所在网站：easylist-downloads.adblockplus.org | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [I don't care about cookies](https://www.i-dont-care-about-cookies.eu/abp/) | 链接所在网站：www.i-dont-care-about-cookies.eu | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [Perflyst and Dandelion Sprout's Smart-TV Blocklist](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 仓库所属账号：Perflyst | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [Dan Pollock's List](https://someonewhocares.org/hosts/zero/hosts) | 链接所在网站：someonewhocares.org | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [Scam Blocklist by DurableNapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 仓库所属账号：durablenapkin | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [Game Console Adblock List](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 仓库所属账号：DandelionSprout | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [Peter Lowe's List](https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext) | 链接所在网站：pgl.yoyo.org | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [NoCoin Filter List](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt) | 仓库所属账号：hoshsadiq | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，含放行例外 |
| [Spam404](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 仓库所属账号：Spam404 | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [The Big List of Hacked Malware Web Sites](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 仓库所属账号：mitchellkrogza | 30 条 AdGuard Home 配置 | 禁用 | 拦截为主，未见放行例外 |
| [HaGeZi Ultimate](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/ultimate.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [AdGuard DNS](https://filters.adtidy.org/android/filters/15_optimized.txt) | 链接所在网站：filters.adtidy.org | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Pro++](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.plus.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Pro](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Normal](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/multi.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [Anti-AD](https://anti-ad.net/easylist.txt) | 链接所在网站：anti-ad.net | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [AWAvenue Ads Rule](https://cdn.jsdelivr.net/gh/AdguardTeam/HostlistsRegistry@main/filters/general/filter_53_AWAvenueAdsRule/filter.txt) | 链接所指仓库账号：AdguardTeam | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Threat Intelligence Feeds](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/tif.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Badware Hoster](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/hoster.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi DynDNS](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/dyndns.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi URL Shortener](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/urlshortener.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [HaGeZi Most Abused TLDs](https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/spam-tlds.txt) | 链接所指仓库账号：hagezi | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [1Hosts Lite](https://cdn.jsdelivr.net/gh/AdguardTeam/HostlistsRegistry@main/filters/general/filter_24_1Hosts_Lite/filter.txt) | 链接所指仓库账号：AdguardTeam | 网页 DNS 过滤器段 | 未指定 | 未检查 |
| [1Hosts Xtra](https://cdn.jsdelivr.net/gh/AdguardTeam/HostlistsRegistry@main/filters/general/filter_70_1Hosts_Xtra/filter.txt) | 链接所指仓库账号：AdguardTeam | 网页 DNS 过滤器段 | 未指定 | 未检查 |

## 加速与备用链接

这些链接可能指向第三方仓库保存的副本，链接所指账号不代表原规则作者。

| 名称 | 链接 | 对应主订阅 |
| --- | --- | --- |
| AdGuard Base filter | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AdGuard_Base_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) |
| AdGuard Base filter | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Base_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) |
| AdGuard Base filter | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Base_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) |
| AdGuard Chinese filter | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AdGuard_Chinese_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) |
| AdGuard Chinese filter | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Chinese_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) |
| AdGuard Chinese filter | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Chinese_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) |
| AdGuard Mobile Ads filter | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AdGuard_Mobile_Ads_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) |
| AdGuard Mobile Ads filter | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Mobile_Ads_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) |
| AdGuard Mobile Ads filter | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Mobile_Ads_filter.txt) | [主订阅](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) |
| AdGuard DNS filter | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AdGuard_DNS_filter.txt) | [主订阅](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) |
| AdGuard DNS filter | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_DNS_filter.txt) | [主订阅](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) |
| AdGuard DNS filter | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_DNS_filter.txt) | [主订阅](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) |
| AdRules DNS List | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AdRules_DNS_List.txt) | [主订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) |
| AdRules DNS List | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdRules_DNS_List.txt) | [主订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) |
| AdRules DNS List | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdRules_DNS_List.txt) | [主订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) |
| CJX's Annoyance List | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/CJX's_Annoyance_List.txt) | [主订阅](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) |
| CJX's Annoyance List | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/CJX's_Annoyance_List.txt) | [主订阅](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) |
| CJX's Annoyance List | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/CJX's_Annoyance_List.txt) | [主订阅](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) |
| EasyList | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/EasyList.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylist.txt) |
| EasyList | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyList.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylist.txt) |
| EasyList | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyList.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylist.txt) |
| EasyList China | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/EasyList_China.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylistchina.txt) |
| EasyList China | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyList_China.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylistchina.txt) |
| EasyList China | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyList_China.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easylistchina.txt) |
| EasyPrivacy | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/EasyPrivacy.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easyprivacy.txt) |
| EasyPrivacy | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyPrivacy.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easyprivacy.txt) |
| EasyPrivacy | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/EasyPrivacy.txt) | [主订阅](https://easylist-downloads.adblockplus.org/easyprivacy.txt) |
| xinggsf mv | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/xinggsf_mv.txt) | [主订阅](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) |
| xinggsf mv | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/xinggsf_mv.txt) | [主订阅](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) |
| xinggsf mv | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/xinggsf_mv.txt) | [主订阅](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) |
| jiekouAD | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/jiekouAD.txt) | [主订阅](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) |
| jiekouAD | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/jiekouAD.txt) | [主订阅](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) |
| jiekouAD | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/jiekouAD.txt) | [主订阅](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) |
| AWAvenue Ads Rule | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/AWAvenue_Ads_Rule.txt) | [主订阅](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) |
| AWAvenue Ads Rule | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AWAvenue_Ads_Rule.txt) | [主订阅](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) |
| AWAvenue Ads Rule | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AWAvenue_Ads_Rule.txt) | [主订阅](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) |
| DNS-Blocklists PRO mini | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/DNS-Blocklists_PRO_mini.txt) | [主订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) |
| DNS-Blocklists PRO mini | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/DNS-Blocklists_PRO_mini.txt) | [主订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) |
| DNS-Blocklists PRO mini | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/DNS-Blocklists_PRO_mini.txt) | [主订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) |
| OISD Basic | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/OISD_Basic.txt) | [主订阅](https://abp.oisd.nl/basic/) |
| OISD Basic | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/OISD_Basic.txt) | [主订阅](https://abp.oisd.nl/basic/) |
| OISD Basic | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/OISD_Basic.txt) | [主订阅](https://abp.oisd.nl/basic/) |
| StevenBlack hosts | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/StevenBlack_hosts.txt) | [主订阅](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) |
| StevenBlack hosts | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/StevenBlack_hosts.txt) | [主订阅](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) |
| StevenBlack hosts | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/StevenBlack_hosts.txt) | [主订阅](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) |
| Pollock hosts | [链接](https://gcore.jsdelivr.net/gh/217heidai/adblockfilters@main/rules/Pollock_hosts.txt) | [主订阅](https://someonewhocares.org/hosts/hosts) |
| Pollock hosts | [链接](https://github.boki.moe/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/Pollock_hosts.txt) | [主订阅](https://someonewhocares.org/hosts/hosts) |
| Pollock hosts | [链接](https://ghfast.top/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/Pollock_hosts.txt) | [主订阅](https://someonewhocares.org/hosts/hosts) |
| AdGuard DNS | [链接](https://cdn.jsdelivr.net/gh/AdguardTeam/HostlistsRegistry@main/filters/general/filter_1_DnsFilter/filter.txt) | [主订阅](https://filters.adtidy.org/android/filters/15_optimized.txt) |
