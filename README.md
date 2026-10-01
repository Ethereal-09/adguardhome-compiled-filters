<h1 align="center">AdGuard Home 规则订阅</h1>

<p align="center">adguardhome-compiled-filters · 自动合并 · 分类订阅 · 每日更新</p>

<p align="center">
  <a href="https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml"><img src="https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml/badge.svg" alt="每日自动构建"></a>
</p>

本项目仅获取、合并与去重上游规则，**规则由原作者及贡献者维护**。每天北京时间 **04:23** 自动构建，无需本机开机。

<!-- build-status:start -->
> 最近构建：**2026-10-01 09:23:28（北京时间）**
>
> 状态：**成功，已通过发布校验** · 分类 30/30 · 来源：新下载 41，缓存 0，失败 0
<!-- build-status:end -->

在 AdGuard Home 的 **过滤器** 中添加下方订阅。黑名单与白名单分别添加到对应页面；已有订阅会继续使用相同地址。

<!-- subscriptions:start -->
## 规则订阅

数量为最近一次通过发布校验的文件条目数，含原生放行例外；每个订阅独立去重，分类之间的数量不能直接相加。

### 基础订阅

添加到 **DNS 黑名单**。综合版与全量版选其一，国内优化可单独使用。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 综合版 | 299,283 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) |
| 国内优化 | 196,505 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 全量版 | 1,960,586 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |

全量版合并 34 个兼容来源，含最高档位、设备与服务限制；各来源原生例外和个人规则保留。

### 强度档位

按需求选一个档位；1Hosts 为替代基础。综合版采用 HaGeZi Normal，并叠加 AdRules DNS 与 AWAvenue。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| HaGeZi 均衡 · Normal | 200,319 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/balanced.txt) |
| HaGeZi 扩展 · Pro | 230,960 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/extended.txt) |
| HaGeZi 激进 · Pro++ | 251,638 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/aggressive.txt) |
| HaGeZi 最强 · Ultimate | 287,467 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/maximum.txt) |
| 1Hosts 均衡 · Lite | 102,241 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/balanced-1hosts.txt) |
| 1Hosts 激进 · Xtra | 786,132 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/aggressive-1hosts.txt) |

### 用途分类

添加到 **DNS 黑名单**，可按用途单独订阅或搭配基础订阅。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 广告分类 | 143,763 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) |
| 跟踪与遥测分类 | 133,806 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/tracking.txt) |
| 安全分类（威胁与诈骗等） | 654,793 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/security.txt) |
| 恶意网站分类 | 9 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/malware.txt) |
| 诈骗分类 | 157,602 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/scam.txt) |
| 勒索软件分类 | 1,903 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ransomware.txt) |
| 挖矿分类 | 1,268 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mining.txt) |
| 电视分类 | 160 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/smart-tv.txt) |
| 游戏机分类 | 14 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/game-console.txt) |
| Windows 遥测组件 | 347 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/windows.txt) |

### 设备与服务限制

添加到 **DNS 黑名单**，按需启用；整站或服务限制可能影响正常功能。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 小米组件 | 278 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/xiaomi.txt) |
| 三星组件 | 101 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/samsung.txt) |
| Spotify 域名拦截组件 | 3,780 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/spotify.txt) |
| YouTube 域名拦截组件 | 97,591 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/youtube.txt) |
| 社交平台限制组件 | 3,995 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/social.txt) |
| 短链接服务限制组件 | 9,982 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/shorteners.txt) |
| 动态 DNS 服务限制组件 | 1,538 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/dyndns.txt) |
| 托管服务限制组件 | 1,238 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/hosting.txt) |

### 独立白名单

添加到 **DNS 白名单**。各文件按用途选用，不自动并入黑名单。

| 规则 | 规则数 | 订阅 |
| --- | ---: | --- |
| 推广跳转放行 | 930 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral.txt) |
| 推广跳转放行（Native） | 1,609 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral-native.txt) |
| 短链接放行 | 9,975 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-shorteners.txt) |
<!-- subscriptions:end -->

DNS 过滤无法区分同一域名内的广告与正常内容，实际误杀需根据使用情况调整。

## 上游来源与署名

<!-- upstream:start -->
当前选用 **41 个来源文件**，来自 **17 个 GitHub 原仓库**。

<details>
<summary>查看来源维护账号、原始订阅与规则数量</summary>

下表使用本次发布所选来源的支持条目数，含来源自身的放行例外，尚未做跨来源合并。仓库所属账号不代表全部原创作者，原作者及间接来源以各上游说明为准。

| 维护账号 / 原仓库 | 原始规则文件 | 支持规则数 |
| --- | --- | ---: |
| [AdAway/adaway.github.io](https://github.com/AdAway/adaway.github.io) | [hosts.txt](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 6,540 |
| [AdguardTeam/AdguardFilters](https://github.com/AdguardTeam/AdguardFilters) | [MobileFilter/sections/adservers.txt](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | 951 |
| [anudeepND/blacklist](https://github.com/anudeepND/blacklist) | [adservers.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) | 42,343 |
| [anudeepND/blacklist](https://github.com/anudeepND/blacklist) | [facebook.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) | 3,995 |
| [badmojr/1Hosts](https://github.com/badmojr/1Hosts) | [Lite/adblock.txt](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | 102,241 |
| [badmojr/1Hosts](https://github.com/badmojr/1Hosts) | [Xtra/adblock.txt](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) | 786,132 |
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
| [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | [dns.txt](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 196,505 |
| [crazy-max/WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker) | [data/hosts/spy.txt](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) | 347 |
| [DandelionSprout/adfilt](https://github.com/DandelionSprout/adfilt) | [GameConsoleAdblockList.txt](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 14 |
| [durablenapkin/scamblocklist](https://github.com/durablenapkin/scamblocklist) | [adguard.txt](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 950 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/dyndns.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | 1,538 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/hoster.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | 1,238 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/multi.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) | 200,319 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/pro.plus.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) | 251,638 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/pro.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | 230,960 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/ultimate.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) | 287,467 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) | 9,982 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-referral-native.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral-native.txt) | 1,609 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-referral.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt) | 936 |
| [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists) | [adblock/whitelist-urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-urlshortener.txt) | 9,975 |
| [jdlingyu/ad-wars](https://github.com/jdlingyu/ad-wars) | [hosts](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 1,645 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Samsung-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) | 101 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Spotify-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) | 3,780 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Extension/GoodbyeAds-Xiaomi-Extension.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) | 278 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Formats/GoodbyeAds-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) | 277,714 |
| [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) | [Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) | 97,645 |
| [mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) | [hacked-domains.list](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 9 |
| [Perflyst/PiHoleBlocklist](https://github.com/Perflyst/PiHoleBlocklist) | [SmartTV-AGH.txt](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 154 |
| [Spam404/lists](https://github.com/Spam404/lists) | [main-blacklist.txt](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 8,140 |
| [StevenBlack/hosts](https://github.com/StevenBlack/hosts) | [hosts](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | 74,759 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [AWAvenue-Ads-Rule.txt](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 962 |

</details>

完整来源与归类依据见 [来源登记](registry/sources.json)，各上游的许可及署名要求见 [许可原文](upstream/README.md)。合并产物保留各上游的权利和许可，不另行声明统一许可。
<!-- upstream:end -->

## 项目维护

每日自动构建后，首页同步更新**构建时间、状态、各订阅数量与所选上游数量**。数量来自构建结果；发布校验失败时保留上次发布的订阅数量，并显示失败状态。

<details>
<summary>配置、个人规则与本地运行</summary>

- **选源与分类**：[profiles.json](profiles.json)；依据见 [分类说明](registry/CLASSIFICATION.md) 和 [全量选源清单](registry/full_selection.json)。新增来源须核实原仓库及真实文件路径。
- **个人规则**：[block.txt](custom/block.txt) / [allow.txt](custom/allow.txt)，默认作用于综合版、全量版；个人放行附加 `important`。
- **合并与去重**：每个订阅独立处理，分类之间允许重复。只拦截子域名不会扩大到父域名；覆盖优化仅移除已被现有同动作、同优先级规则覆盖的条目，可用 `coverageOptimization: false` 关闭。
- **原生例外**：黑名单携带所选上游自身的放行例外；合并后的例外可能影响其他来源。独立白名单仍按用途单独订阅。
- **发布校验**：使用 AdGuard 官方引擎验证产物。网络异常可使用 72 小时内有效缓存；数量异常或校验失败时保留上次发布的订阅。

Python 3.12 本地运行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -X utf8 build_filters.py
```

GitHub Actions 自动编译官方引擎验证器并执行完整校验。本地完整校验需使用 `--validator` 指定验证器，再执行 `validate_subscriptions.py`。构建时间记录最近一次执行完成；规则文件的更新时间仅在内容变化时改变。

</details>

[自动构建记录](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml) · [构建统计](dist/manifest.json) · [来源分类目录](registry/README.md)
