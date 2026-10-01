# AdGuard Home 规则订阅

[![自动构建](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml/badge.svg)](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)

合并、去重并分类上游 DNS 规则，**规则由上游原作者及贡献者维护**。每天北京时间 **04:23** 自动更新。

<!-- build-status:start -->
> 最近构建：**2026-10-01 22:47:47（北京时间）**
>
> 状态：**成功，已通过发布校验** · 分类 33/33 · 来源：新下载 60，缓存 0，失败 0
<!-- build-status:end -->

<!-- subscriptions:start -->
## 订阅

在 AdGuard Home → **过滤器 → DNS 黑名单**添加。日常使用选综合版；国内优化可单独使用；全量版按需选择。

| 规则 | 规则数 | 适用范围 | 订阅 |
| --- | ---: | --- | --- |
| 综合版 | 308,701 | 通用过滤 + 国内优化 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) |
| 国内优化 | 210,674 | 中国使用环境 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 全量版 | 2,005,873 | 最高档位 + 全部兼容专项（含服务限制） | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |

数量随成功构建更新，含原生放行例外；每个订阅独立去重。

<details>
<summary>其他分类订阅（30 项）：强度、用途、设备与白名单</summary>

### 强度档位

任选一个档位；1Hosts 可作为替代。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| HaGeZi 均衡 · Normal | 200,656 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/balanced.txt) |
| HaGeZi 扩展 · Pro | 231,053 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/extended.txt) |
| HaGeZi 激进 · Pro++ | 251,762 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/aggressive.txt) |
| HaGeZi 最强 · Ultimate | 287,640 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/maximum.txt) |
| 1Hosts 均衡 · Lite | 102,241 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/balanced-1hosts.txt) |
| 1Hosts 激进 · Xtra | 786,132 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/aggressive-1hosts.txt) |

### 用途分类

按用途单独使用或搭配基础订阅，添加到 DNS 黑名单。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 广告分类 | 143,763 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) |
| 跟踪与遥测分类 | 133,812 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/tracking.txt) |
| 安全分类（威胁与诈骗等） | 654,800 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/security.txt) |
| 恶意网站分类 | 9 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/malware.txt) |
| 诈骗分类 | 157,609 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/scam.txt) |
| 勒索软件分类 | 1,903 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ransomware.txt) |
| 挖矿分类 | 1,524 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mining.txt) |
| 电视分类 | 160 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/smart-tv.txt) |
| 游戏机分类 | 14 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/game-console.txt) |
| Windows 遥测组件 | 355 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/windows.txt) |
| 设备原生遥测 | 98 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/native-tracking.txt) |
| 钓鱼网站分类 | 118,066 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/phishing.txt) |

### 设备与服务限制

添加到 DNS 黑名单；整站或服务限制可能影响正常功能。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 小米组件 | 278 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/xiaomi.txt) |
| 三星组件 | 101 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/samsung.txt) |
| Spotify 域名拦截组件 | 3,780 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/spotify.txt) |
| YouTube 域名拦截组件 | 97,591 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/youtube.txt) |
| 社交平台限制组件 | 3,995 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/social.txt) |
| 短链接服务限制组件 | 9,981 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/shorteners.txt) |
| 动态 DNS 服务限制组件 | 1,538 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/dyndns.txt) |
| 托管服务限制组件 | 1,238 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/hosting.txt) |
| 高滥用顶级域名限制 | 281 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/tld-restrictions.txt) |

### 独立白名单

添加到 **DNS 白名单**，按用途选择。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 推广跳转放行 | 930 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral.txt) |
| 推广跳转放行（Native） | 1,611 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral-native.txt) |
| 短链接放行 | 9,974 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-shorteners.txt) |

</details>
<!-- subscriptions:end -->

## 来源与署名

<!-- upstream:start -->
当前选用 **60 个来源文件**，来自 **25 个 GitHub 原仓库**及 **2 个官方站点**。

<details>
<summary>查看上游作者、原始订阅与规则数量</summary>

数量为来源合并前的支持条目数。仓库账号不代表全部原创作者，完整署名以各上游说明为准。

| 维护账号 / 原始项目 | 原始规则文件 | 支持规则数 |
| --- | --- | ---: |
| [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) | [rules/adblockdns.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt) | 216,067 |
| [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) | [rules/adblockdnslite.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt) | 5,376 |
| [8680/GOODBYEADS](https://github.com/8680/GOODBYEADS) | [data/rules/dns.txt](https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt) | 113,593 |
| [AdAway/adaway.github.io](https://github.com/AdAway/adaway.github.io) | [hosts.txt](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 6,540 |
| [AdguardTeam/AdguardFilters](https://github.com/AdguardTeam/AdguardFilters) | [MobileFilter/sections/adservers.txt](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | 951 |
| [anudeepND/blacklist](https://github.com/anudeepND/blacklist) | [adservers.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) | 42,343 |
| [anudeepND/blacklist](https://github.com/anudeepND/blacklist) | [facebook.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) | 3,995 |
| [badmojr/1Hosts](https://github.com/badmojr/1Hosts) | [Lite/adblock.txt](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | 102,241 |
| [badmojr/1Hosts](https://github.com/badmojr/1Hosts) | [Xtra/adblock.txt](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) | 786,132 |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [rule/AdGuard/Advertising/Advertising.txt](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/AdGuard/Advertising/Advertising.txt) | 280,210 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/abuse-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/abuse-ags.txt) | 435,051 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/ads-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ads-ags.txt) | 233,991 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/crypto-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/crypto-ags.txt) | 1,272 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/fraud-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/fraud-ags.txt) | 256,184 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/phishing-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/phishing-ags.txt) | 190,191 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/ransomware-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ransomware-ags.txt) | 1,904 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/redirect-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/redirect-ags.txt) | 108,682 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/scam-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/scam-ags.txt) | 8,527 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/smart-tv-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/smart-tv-ags.txt) | 77 |
| [blocklistproject/Lists](https://github.com/blocklistproject/Lists) | [adguard/tracking-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/tracking-ags.txt) | 143,866 |
| [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | [dns.txt](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 196,737 |
| [crazy-max/WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker) | [data/hosts/spy.txt](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) | 347 |
| [DandelionSprout/adfilt](https://github.com/DandelionSprout/adfilt) | [GameConsoleAdblockList.txt](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 14 |
| [durablenapkin/scamblocklist](https://github.com/durablenapkin/scamblocklist) | [adguard.txt](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 957 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/dyndns.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | 1,538 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/hoster.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | 1,238 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/multi.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) | 200,656 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/pro.plus.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) | 251,762 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/pro.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | 231,053 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/spam-tlds.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/spam-tlds.txt) | 281 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/ultimate.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) | 287,640 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) | 9,981 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-referral-native.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral-native.txt) | 1,611 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-referral.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt) | 936 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-urlshortener.txt) | 9,974 |
| [hoshsadiq/adblock-nocoin-list](https://github.com/hoshsadiq/adblock-nocoin-list) | [hosts.txt](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt) | 312 |
| [jdlingyu/ad-wars](https://github.com/jdlingyu/ad-wars) | [hosts](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 1,645 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Samsung-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) | 101 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Spotify-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) | 3,780 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Xiaomi-Extension.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) | 278 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Formats/GoodbyeAds-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) | 277,714 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) | 97,645 |
| [mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) | [hacked-domains.list](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 9 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/alexa](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/alexa) | 3 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/apple](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/apple) | 19 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/huawei](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/huawei) | 37 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/roku](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/roku) | 1 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/samsung](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/samsung) | 4 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/sonos](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/sonos) | 2 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/windows](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/windows) | 23 |
| [nextdns/native-tracking-domains](https://github.com/nextdns/native-tracking-domains) | [domains/xiaomi](https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/xiaomi) | 9 |
| [Perflyst/PiHoleBlocklist](https://github.com/Perflyst/PiHoleBlocklist) | [SmartTV-AGH.txt](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 154 |
| [privacy-protection-tools/anti-AD](https://github.com/privacy-protection-tools/anti-AD) | [anti-ad-easylist.txt](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) | 93,230 |
| [sjhgvr/oisd](https://github.com/sjhgvr/oisd) | [abp_small.txt](https://raw.githubusercontent.com/sjhgvr/oisd/main/abp_small.txt) | 57,297 |
| [Spam404/lists](https://github.com/Spam404/lists) | [main-blacklist.txt](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 8,140 |
| [StevenBlack/hosts](https://github.com/StevenBlack/hosts) | [hosts](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | 74,759 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [AWAvenue-Ads-Rule.txt](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 962 |
| [uBlockOrigin/uAssets](https://github.com/uBlockOrigin/uAssets) | [filters/resource-abuse.txt](https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/resource-abuse.txt) | 1 |
| [Peter Lowe](https://pgl.yoyo.org/adservers/) | [adservers/serverlist.php](https://pgl.yoyo.org/adservers/serverlist.php?hostformat=adblockplus&showintro=1&mimetype=plaintext) | 3,552 |
| [Dan Pollock](https://someonewhocares.org/hosts/) | [hosts/zero/hosts](https://someonewhocares.org/hosts/zero/hosts) | 13,082 |

</details>

[来源登记](registry/README.md) · [上游许可与署名](upstream/README.md)；合并产物遵循各上游许可。
<!-- upstream:end -->

## 维护

[分类与合并说明](registry/CLASSIFICATION.md) · [构建统计](dist/manifest.json) · [自动构建记录](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)

<details>
<summary>修改规则与本地运行</summary>

- 选源与分类：[profiles.json](profiles.json)。新增来源先登记到 [核实来源](registry/reviewed_sources.json)，再用 `refresh_source_registry.py --validator <验证器路径>` 检查。
- 个人规则：[拦截](custom/block.txt) / [放行](custom/allow.txt)，默认用于综合版、全量版。
- 自动构建通过发布校验后更新规则及数量；失败时保留上次发布版本。

Python 3.12 本地构建：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -X utf8 build_filters.py
```

完整发布校验需使用 `--validator` 指定官方引擎验证器，并运行 `validate_subscriptions.py`；GitHub Actions 自动完成这些步骤。

</details>
