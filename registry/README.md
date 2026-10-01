# AdGuard Home 来源登记

最近核验：2026-10-01T13:58:28+00:00（UTC）。共 93 个原始文件，65 个通过完整下载、保守解析和 AdGuard 引擎校验。

上游署名、用途、强度、地域和证据保存在 [reviewed_sources.json](reviewed_sources.json)；当前兼容结果见 [sources.json](sources.json)，实际组合见 [profiles.json](../profiles.json)。

对浏览器条件、URL 路径和脚本语法不做域名扩大转换。无法保留网络放行例外或 badfilter 的来源整份排除。DNS 黑名单保留其原生例外；独立白名单按用途另行订阅。

旧的 registry/sources/ 是历史拆分快照，本次发布以 dist/ 和 manifest.json 为准。

| 原始来源 | 分类 | DNS 拦截 | DNS 例外 | 结果 |
| --- | --- | ---: | ---: | --- |
| [AdGuard Chinese filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|pagead2.googlesyndication.com/pagead/js/adsbygoogle.js$domain=soft8ware.com |
| [AdGuard Mobile Ads filter](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | ads | 951 | 0 | 可选；fresh |
| [AdRules DNS List](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | ads, tracking, security | 196737 | 0 | 可选；fresh |
| [CJX's Annoyance List](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | annoyance | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|th7.cn/sanda2015/css/ads.js |
| [xinggsf mv](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | video | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|log.mmstat.com/eg.js^$script |
| [jiekouAD](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|themoviedb.org/assets/ |
| [AWAvenue Ads Rule](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | ads, tracking | 962 | 0 | 可选；fresh |
| [DNS-Blocklists PRO mini](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) | ads, tracking, security | 60007 | 0 | 可选；fresh |
| [StevenBlack hosts](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | ads, tracking, security | 74759 | 0 | 可选；fresh |
| [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|mirror*.mangafunc.fun/comic/ |
| [大圣净化](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | ads | 1645 | 0 | 可选；fresh |
| [AdAway default blocklist](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | ads | 6540 | 0 | 可选；fresh |
| [Perflyst and Dandelion Sprout's Smart-TV Blocklist](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | smart_tv | 145 | 9 | 可选；fresh |
| [Scam Blocklist by DurableNapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | scam | 957 | 0 | 可选；fresh |
| [Game Console Adblock List](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | game_console | 14 | 0 | 可选；fresh |
| [NoCoin Filter List](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt) | mining | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|api.nyda.pro^$websocket |
| [Spam404](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | security | 8140 | 0 | 可选；fresh |
| [The Big List of Hacked Malware Web Sites](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | security | 9 | 0 | 可选；fresh |
| [HaGeZi Ultimate](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) | ads, tracking, security | 287640 | 0 | 可选；fresh |
| [HaGeZi Pro++](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) | ads, tracking, security | 251762 | 0 | 可选；fresh |
| [HaGeZi Pro](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | ads, tracking, security | 231053 | 0 | 可选；fresh |
| [HaGeZi Normal](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) | ads, tracking, security | 200656 | 0 | 可选；fresh |
| [HaGeZi Badware Hoster](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | hosting_blocking | 1238 | 0 | 可选；fresh |
| [HaGeZi DynDNS](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | dyndns_blocking | 1538 | 0 | 可选；fresh |
| [HaGeZi URL Shortener](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) | shortener_blocking | 9981 | 0 | 可选；fresh |
| [1Hosts Lite](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | ads, tracking, security | 102241 | 0 | 可选；fresh |
| [1Hosts Xtra](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) | ads, tracking, security | 786132 | 0 | 可选；fresh |
| [blocklistproject/Lists / abuse-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/abuse-ags.txt) | security | 435051 | 0 | 可选；fresh |
| [blocklistproject/Lists / ads-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ads-ags.txt) | ads | 233991 | 0 | 可选；fresh |
| [blocklistproject/Lists / crypto-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/crypto-ags.txt) | mining | 1272 | 0 | 可选；fresh |
| [blocklistproject/Lists / fraud-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/fraud-ags.txt) | scam | 256184 | 0 | 可选；fresh |
| [blocklistproject/Lists / phishing-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/phishing-ags.txt) | phishing | 190191 | 0 | 可选；fresh |
| [blocklistproject/Lists / ransomware-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ransomware-ags.txt) | ransomware | 1904 | 0 | 可选；fresh |
| [blocklistproject/Lists / redirect-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/redirect-ags.txt) | security | 108682 | 0 | 可选；fresh |
| [blocklistproject/Lists / scam-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/scam-ags.txt) | scam | 8527 | 0 | 可选；fresh |
| [blocklistproject/Lists / smart-tv-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/smart-tv-ags.txt) | smart_tv | 77 | 0 | 可选；fresh |
| [blocklistproject/Lists / tracking-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/tracking-ags.txt) | tracking | 143866 | 0 | 可选；fresh |
| [anudeepND/blacklist / adservers.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) | ads, tracking, security | 42343 | 0 | 可选；fresh |
| [anudeepND/blacklist / facebook.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) | social_blocking | 3995 | 0 | 可选；fresh |
| [anudeepND/blacklist / CoinMiner.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt) | mining | — | — | 上游明确停止更新，保留登记，不进入订阅。 |
| [crazy-max/WindowsSpyBlocker / spy.txt](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) | tracking | 347 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt) | ads, tracking, security | 277744 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) | ads, tracking, security | 277714 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-Xiaomi-Extension.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) | xiaomi | 278 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-Samsung-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) | samsung | 101 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-Spotify-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) | spotify | 3780 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-YouTube-AdBlock.txt) | youtube | 97645 | 0 | 可选；fresh |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) | youtube | 97645 | 0 | 可选；fresh |
| [HaGeZi / whitelist-referral.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt) | referral_allow | 0 | 936 | 可选；fresh |
| [HaGeZi / whitelist-referral-native.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral-native.txt) | referral_allow | 0 | 1611 | 可选；fresh |
| [HaGeZi / whitelist-urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-urlshortener.txt) | shortener_allow | 0 | 9974 | 可选；fresh |
| [AdGuard Base filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) | ads | — | — | Empty response or HTML instead of rules |
| [AdGuard DNS filter](https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/gh-pages/Filters/filter.txt) | ads, tracking | — | — | badfilter requires disabling rules before optimization; source rejected |
| [OISD Basic](https://raw.githubusercontent.com/sjhgvr/oisd/main/abp_small.txt) | ads, tracking | 57297 | 0 | 可选；fresh |
| [alexa](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/alexa) | tracking, native_tracking | 3 | 0 | 可选；fresh |
| [apple](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/apple) | tracking, native_tracking | 19 | 0 | 可选；fresh |
| [huawei](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/huawei) | tracking, native_tracking | 37 | 0 | 可选；fresh |
| [roku](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/roku) | tracking, native_tracking | 1 | 0 | 可选；fresh |
| [samsung](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/samsung) | tracking, native_tracking | 4 | 0 | 可选；fresh |
| [sonos](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/sonos) | tracking, native_tracking | 2 | 0 | 可选；fresh |
| [windows](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/windows) | tracking, native_tracking | 23 | 0 | 可选；fresh |
| [xiaomi](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/xiaomi) | tracking, native_tracking | 9 | 0 | 可选；fresh |
| [Anti-AD](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) | ads, tracking | 93120 | 110 | 可选；fresh |
| [HaGeZi Threat Intelligence Feeds](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/tif.txt) | security, malware, phishing, scam | — | — | Source exceeds 32 MiB limit |
| [HaGeZi Most Abused TLDs](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/spam-tlds.txt) | tld_blocking | 281 | 0 | 可选；fresh |
| [adblock-nocoin-list / hosts.txt](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt) | mining | 312 | 0 | 可选；fresh |
| [AdditionalFiltersCN / CN.txt](https://raw.githubusercontent.com/Crystal-RainSlide/AdditionalFiltersCN/master/CN.txt) | ads | — | — | badfilter requires disabling rules before optimization; source rejected |
| [Adblock-Plus-Rule / rule.txt](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|bdstatic.com/static/common/widget/ui/admanager/$script,domain=image.baidu.com |
| [ios_rule_script / rule/AdGuard/Advertising/Advertising.txt](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/AdGuard/Advertising/Advertising.txt) | ads, tracking | 280210 | 0 | 可选；fresh |
| [AdGuard-Custom-Rule / rule/zhihu.txt](https://raw.githubusercontent.com/zsakvo/AdGuard-Custom-Rule/master/rule/zhihu.txt) | unknown | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|www.zhihu.com/api/v4/search_v3* |
| [koolproxy / rules/daily.txt](https://raw.githubusercontent.com/ilxp/koolproxy/main/rules/daily.txt) | unknown | — | — | Empty response or HTML instead of rules |
| [uAssets / filters/badware.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/badware.txt) | security | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|onelink.me/*://app/$doc |
| [uAssets / filters/privacy.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt) | tracking | — | — | badfilter requires disabling rules before optimization; source rejected |
| [uAssets / filters/quick-fixes.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/quick-fixes.txt) | compatibility | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|hb.vntsm.com/v4/live/vms/sites/aternos.org/index.js$script,domain=aternos.org |
| [uAssets / filters/resource-abuse.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/resource-abuse.txt) | mining | 1 | 0 | 可选；fresh |
| [uAssets / filters/unbreak.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/unbreak.txt) | compatibility | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|awstrack.me/*auth.coindesk.com$doc,popup |
| [GOODBYEADS / data/rules/dns.txt](https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt) | ads, tracking | 113593 | 0 | 可选；fresh |
| [adblockfilters / rules/adblockdns.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt) | ads, tracking | 215870 | 197 | 可选；fresh |
| [adblockfilters / rules/adblockdnslite.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt) | ads, tracking | 5360 | 16 | 可选；fresh |
| [AdGuard-Rule / rule/adgh.txt](https://raw.githubusercontent.com/hululu1068/AdGuard-Rule/main/rule/adgh.txt) | ads, tracking | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|emails.educause.edu^\| |
| [AdGuard-Rule / rule/mylist.txt](https://raw.githubusercontent.com/hululu1068/AdGuard-Rule/main/rule/mylist.txt) | ads, tracking | 4 | 100 | 可选；fresh |
| [GOODBYEADS / data/rules/allow.txt](https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/allow.txt) | compatibility_allow | — | — | Unsupported exception; source rejected instead of dropping it: @@#.banner%20ad.$image,domain=dokuo666.blog98.fc2.com |
| [EasyList](https://easylist-downloads.adblockplus.org/easylist.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|youtube.com/get_video_info?$xmlhttprequest,domain=music.youtube.com\|tv.youtube.com |
| [EasyList China](https://easylist-downloads.adblockplus.org/easylistchina.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@.adserver.$domain=litv.tv |
| [EasyPrivacy](https://easylist-downloads.adblockplus.org/easyprivacy.txt) | tracking | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|bam.nr-data.net^$xmlhttprequest,domain=abema.tv |
| [Pollock hosts](https://someonewhocares.org/hosts/hosts) | ads, tracking, security | 13082 | 0 | 可选；fresh |
| [easylist](https://easylist.to/easylist/easylist.txt) | ads | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|youtube.com/get_video_info?$xmlhttprequest,domain=music.youtube.com\|tv.youtube.com |
| [easyprivacy](https://easylist.to/easylist/easyprivacy.txt) | tracking | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|bam.nr-data.net^$xmlhttprequest,domain=abema.tv |
| [fanboy-annoyance](https://easylist.to/easylist/fanboy-annoyance.txt) | annoyance | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|assets.mailerlite.com/js/universal.js$script,domain=real.gr |
| [Adblock Warning Removal List](https://easylist-downloads.adblockplus.org/antiadblockfilters.txt) | annoyance | — | — | Unsupported exception; source rejected instead of dropping it: @@/adsbygoogle.js$script,domain=arabiaweather.com |
| [I don't care about cookies](https://www.i-dont-care-about-cookies.eu/abp/) | annoyance | — | — | Unsupported exception; source rejected instead of dropping it: @@\|\|nf.pl/js/libs/cookiesDirective.js$script |
| [Dan Pollock's List](https://someonewhocares.org/hosts/zero/hosts) | ads, tracking, security | 13082 | 0 | 可选；fresh |
| [Peter Lowe's List](https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext) | ads, tracking | 3552 | 0 | 可选；fresh |

## 重新核验

```powershell
.\.venv\Scripts\python.exe refresh_source_registry.py --validator .cache\dns-rule-validator.exe
```

每日构建直接读取已选来源，每次重新下载、检查例外、异常数量下降和引擎兼容性；不会自动启用新发现的订阅源。
