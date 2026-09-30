<h1 align="center">AdBlock DNS Filters</h1>

<p align="center">使用 Python 每天自动获取、分类、合并和优化上游 DNS 规则</p>

[![每日更新](https://github.com/Ethereal-09/AdBlock-DNS-Filters/actions/workflows/update.yml/badge.svg)](https://github.com/Ethereal-09/AdBlock-DNS-Filters/actions/workflows/update.yml)

## 📔 说明

**本人仅维护合并程序与订阅配置。上游规则由各原作者及其贡献者编写和维护，规则成果归原作者所有。** 本项目做来源选择、格式处理、去重与覆盖优化。

适用于 AdGuard Home DNS 过滤，合并程序使用 Python 标准库。GitHub Actions 另外编译固定版本的 AdGuard 官方过滤引擎验证器，发布前验证 DNS 语法和正则。每天北京时间 **04:23** 自动更新，不依赖本机持续开机。实际启动可能延迟，公开仓库 60 天没有活动也可能暂停定时任务，见 [GitHub 官方说明](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)。工作流每周维护一次成功记录，保持仓库有更新活动。

## 🎯 分类订阅

配置选择 **39 个来源文件、17 个 GitHub 仓库**，构建 **27 个黑名单分类和 3 个独立白名单**。完整文件与状态见 [分类订阅索引](dist/README.md)，统计见 [manifest.json](dist/manifest.json)。

| 文件 | 内容 |
| --- | --- |
| [adguard.txt](dist/adguard.txt) / [combined.txt](dist/combined.txt) | 综合版：HaGeZi Normal ＋ AdRules DNS ＋ AWAvenue，加个人规则 |
| [full.txt](dist/full.txt) | 全量版：32 个已核验、可兼容的 DNS 拦截来源；最高强度＋全部可用专项，加个人规则 |
| [balanced.txt](dist/balanced.txt) | 均衡：HaGeZi Normal |
| [extended.txt](dist/extended.txt) | 扩展：HaGeZi Pro |
| [aggressive.txt](dist/aggressive.txt) | 激进：HaGeZi Pro++ |
| [maximum.txt](dist/maximum.txt) | 最强：HaGeZi Ultimate |
| [balanced-1hosts.txt](dist/balanced-1hosts.txt) / [aggressive-1hosts.txt](dist/aggressive-1hosts.txt) | 1Hosts Lite / Xtra，作为对应基础档位的替代选择 |
| [china.txt](dist/china.txt) | 中国国内优化：上游明确面向中国环境的 AdRules DNS |
| [ads.txt](dist/ads.txt) / [tracking.txt](dist/tracking.txt) | 广告、跟踪与遥测分类 |
| [security.txt](dist/security.txt) | 安全分类：威胁、重定向、诈骗、勒索软件等来源 |
| [malware.txt](dist/malware.txt) / [scam.txt](dist/scam.txt) / [mining.txt](dist/mining.txt) / [ransomware.txt](dist/ransomware.txt) | 分用途的安全组件 |
| [smart-tv.txt](dist/smart-tv.txt) / [game-console.txt](dist/game-console.txt) | 电视、游戏机分类 |
| [分类订阅索引](dist/README.md) | Windows、小米、三星、Spotify、YouTube、社交平台、短链接、动态 DNS、托管服务等可选组件 |
| [allow-referral.txt](dist/allow-referral.txt) / [allow-referral-native.txt](dist/allow-referral-native.txt) / [allow-shorteners.txt](dist/allow-shorteners.txt) | 按需使用的推广跳转、短链接独立放行 |

强度档位任选一个；同系列多个版本不叠加。综合版含未明确分级的国内组件，不能等同于上游的均衡档位。分类按上游来源的用途选源，不凭域名名称猜测每条规则的类别；不承诺单一用途或实际应用低误杀。

全量版单独订阅，默认入口仍为综合版。全量覆盖本项目登记的可用 DNS 来源，包含最高档位和社交平台、短链接、动态 DNS、托管服务等限制组件，并携带所选来源的原生放行例外；独立白名单不合入。它不代表 GitHub 所有规则，也不包含无法保留浏览器例外的来源。全部选择、替代与排除原因见 [全量选源核验](registry/full_selection.json)，该清单为新增全量版时的核验快照。

国内优化描述中国使用环境，保留相关的 `.com` 等域名，不按 `.cn` 或解析 IP 国家筛选。设备及服务限制组件按需选择；DNS 域名拦截无法区分同一域名的广告与正常内容，也不保证去除视频内嵌广告。

在 AdGuard Home **过滤器 → DNS 黑名单** 添加以下订阅地址，按需选用：

```text
https://raw.githubusercontent.com/Ethereal-09/AdBlock-DNS-Filters/main/dist/adguard.txt
https://raw.githubusercontent.com/Ethereal-09/AdBlock-DNS-Filters/main/dist/china.txt
https://raw.githubusercontent.com/Ethereal-09/AdBlock-DNS-Filters/main/dist/full.txt
```

独立放行组件添加到 **DNS 白名单**，不自动并入黑名单。黑名单文件已经携带所选来源自身的原生放行例外。

其他分类使用同一地址下的对应文件名，见 [分类订阅索引](dist/README.md)。例如短链接白名单为 `https://raw.githubusercontent.com/Ethereal-09/AdBlock-DNS-Filters/main/dist/allow-shorteners.txt`。

## 🛠️ 运行与每日自动更新

本机已有环境，可直接运行：

```powershell
.\.venv\Scripts\python.exe -X utf8 -B build_filters.py
```

新电脑需要 Python 3.11+，推荐 3.12，先创建环境：

```powershell
py -3.12 -m venv .venv
```

GitHub Actions 工作流在 [.github/workflows/update.yml](.github/workflows/update.yml)：

1. 上传全部项目文件到自己的公开仓库，默认分支为 `main`；包括配置、来源登记、catalog/、github_sources/、new_sources/ 等核验资料以及程序、测试、工作流和生成文件。不要上传 `.venv/`、`.cache/`。
2. 在 Actions 页面启用 `Update DNS rules`，点击 `Run workflow` 验证首次构建和提交。
3. 工作流每天运行，程序、选源配置或本地规则变更也会触发。自动测试、下载、构建和验证全部订阅；仅在全部通过后提交 `dist/`，有变化才提交，每周附带一次维护记录。
4. 仓库需要允许 Actions 的写入权限；分支保护若阻止直接提交，需配置允许的提交方式。Actions 成功状态确认远程更新已接通。

每轮结果、缓存使用情况和失败原因在 Actions 的运行摘要中；下载日志与发布审核报告保存为 30 天的运行附件。缓存替代会显示警告，不冒充本次成功下载。构建或发布审核失败时，不提交本轮订阅。

本次代码和产物审计记录见 [AUDIT.md](AUDIT.md)。源配置不会每天自动发现新仓库或重新分级，新增来源仍需核验并修改配置。

[首次云端自动运行](https://github.com/Ethereal-09/AdBlock-DNS-Filters/actions/runs/36777499627) 已通过测试、下载、30 个分类构建、全部产物审核、缓存保存及机器人自动提交。工作流处于启用状态，默认分支为 `main`。

## 上游规则与署名

<details>
<summary>点击查看分类程序选择的 GitHub 原仓库订阅</summary>

账号表示仓库所属组织或维护账号，不代表所有规则的原创作者。合并型上游的间接来源和许可，以原仓库说明为准；本项目不为合并规则另行声明统一许可。已保存所选 17 个原仓库的[许可证与许可说明](upstream/README.md)，规则文件头部也链接原始许可。规则经过格式规范、合并和去重，修改由本项目完成。

| 来源文件 | 仓库所属账号 / 组织 | 原仓库 | 订阅 |
| --- | --- | --- | --- |
| AdGuard Mobile Ads filter | AdguardTeam | [仓库](https://github.com/AdguardTeam/AdguardFilters) | [原始订阅](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) |
| AdRules DNS List | Cats-Team | [仓库](https://github.com/Cats-Team/AdRules) | [原始订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) |
| AWAvenue Ads Rule | TG-Twilight | [仓库](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [原始订阅](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) |
| StevenBlack hosts | StevenBlack | [仓库](https://github.com/StevenBlack/hosts) | [原始订阅](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) |
| 大圣净化 | jdlingyu | [仓库](https://github.com/jdlingyu/ad-wars) | [原始订阅](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) |
| AdAway default blocklist | AdAway | [仓库](https://github.com/AdAway/adaway.github.io) | [原始订阅](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) |
| Perflyst and Dandelion Sprout's Smart-TV Blocklist | Perflyst | [仓库](https://github.com/Perflyst/PiHoleBlocklist) | [原始订阅](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) |
| Scam Blocklist by DurableNapkin | durablenapkin | [仓库](https://github.com/durablenapkin/scamblocklist) | [原始订阅](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) |
| Game Console Adblock List | DandelionSprout | [仓库](https://github.com/DandelionSprout/adfilt) | [原始订阅](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) |
| Spam404 | Spam404 | [仓库](https://github.com/Spam404/lists) | [原始订阅](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) |
| The Big List of Hacked Malware Web Sites | mitchellkrogza | [仓库](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) | [原始订阅](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) |
| HaGeZi Ultimate | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) |
| HaGeZi Pro++ | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) |
| HaGeZi Pro | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) |
| HaGeZi Normal | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) |
| HaGeZi Badware Hoster | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) |
| HaGeZi DynDNS | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) |
| HaGeZi URL Shortener | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) |
| 1Hosts Lite | badmojr | [仓库](https://github.com/badmojr/1Hosts) | [原始订阅](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) |
| 1Hosts Xtra | badmojr | [仓库](https://github.com/badmojr/1Hosts) | [原始订阅](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) |
| blocklistproject/Lists / abuse-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/abuse-ags.txt) |
| blocklistproject/Lists / ads-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ads-ags.txt) |
| blocklistproject/Lists / crypto-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/crypto-ags.txt) |
| blocklistproject/Lists / ransomware-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ransomware-ags.txt) |
| blocklistproject/Lists / redirect-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/redirect-ags.txt) |
| blocklistproject/Lists / scam-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/scam-ags.txt) |
| blocklistproject/Lists / smart-tv-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/smart-tv-ags.txt) |
| blocklistproject/Lists / tracking-ags.txt | blocklistproject | [仓库](https://github.com/blocklistproject/Lists) | [原始订阅](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/tracking-ags.txt) |
| anudeepND/blacklist / adservers.txt | anudeepND | [仓库](https://github.com/anudeepND/blacklist) | [原始订阅](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) |
| anudeepND/blacklist / facebook.txt | anudeepND | [仓库](https://github.com/anudeepND/blacklist) | [原始订阅](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) |
| crazy-max/WindowsSpyBlocker / spy.txt | crazy-max | [仓库](https://github.com/crazy-max/WindowsSpyBlocker) | [原始订阅](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) |
| jerryn70/GoodbyeAds / GoodbyeAds-AdBlock-Filter.txt | jerryn70 | [仓库](https://github.com/jerryn70/GoodbyeAds) | [原始订阅](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) |
| jerryn70/GoodbyeAds / GoodbyeAds-Xiaomi-Extension.txt | jerryn70 | [仓库](https://github.com/jerryn70/GoodbyeAds) | [原始订阅](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) |
| jerryn70/GoodbyeAds / GoodbyeAds-Samsung-AdBlock.txt | jerryn70 | [仓库](https://github.com/jerryn70/GoodbyeAds) | [原始订阅](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) |
| jerryn70/GoodbyeAds / GoodbyeAds-Spotify-AdBlock.txt | jerryn70 | [仓库](https://github.com/jerryn70/GoodbyeAds) | [原始订阅](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) |
| jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock-Filter.txt | jerryn70 | [仓库](https://github.com/jerryn70/GoodbyeAds) | [原始订阅](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) |
| HaGeZi / whitelist-referral.txt | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt) |
| HaGeZi / whitelist-referral-native.txt | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral-native.txt) |
| HaGeZi / whitelist-urlshortener.txt | hagezi | [仓库](https://github.com/hagezi/dns-blocklists) | [原始订阅](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-urlshortener.txt) |

</details>

全部已知来源、黑白性质、强度、地域与依据见 [来源分类目录](registry/README.md)。停更、数量异常及未选用的浏览器来源不会自动启用。组合边界见 [分类说明](registry/CLASSIFICATION.md)。

## 优化与异常处理

- 同一来源每轮只下载一次，多个分类共享下载结果；4 个并发，超时 45 秒，失败重试 3 次。
- 删除空行、注释和重复条目；规范域名大小写、IDN、Hosts 及纯域名。Hosts 和纯域名转为精确匹配 `|domain|`，不扩大到子域名。
- **每个订阅文件内部独立去重**，不同订阅之间允许重复。同一来源只下载一次不意味着它的规则只保留在一个分类中。
- 仅在相同拦截/放行动作、相同 important 优先级内，删除被已存在的父域规则覆盖的简单条目。只有子域名时不会生成父域规则。`||example.com^` 已经覆盖父域及子域；精确父域规则 `|example.com|` 不覆盖子域。每个分类可设置 `coverageOptimization: false` 仅做相同规则去重；此选项不会删除上游原有的广泛父域规则。通配符、正则及上游例外保留，不将全部例外提升为 important。语法见 [AdGuard DNS 官方文档](https://adguard-dns.io/kb/general/dns-filtering-syntax/)。
- 支持域名、Hosts、简单 Adblock 域名规则、DNS 掩码、正则及 important。其他修饰符及浏览器语法不在支持范围；不支持的拦截条目记入统计。不支持的放行例外或 badfilter 会导致整个来源拒绝，防止丢失例外扩大拦截。
- 校验完整 HTTP 响应、Content-Length、大小上限、空响应及 HTML。网络失败可使用 **72 小时内**已校验缓存；缓存有地址与校验和验证。内容异常不使用缓存掩盖。
- 无有效缓存或数量异常时，保留受影响分类的旧文件，其他分类继续更新。来源最低数量为登记支持条目数的 50%；来源或优化后分类比上一版减少超过 **30%** 时触发保护。
- 每个订阅文件采用临时文件替换，跨文件不是一个原子事务；本地中断后重新运行可修复索引和统计。GitHub 发布以一次 Git 提交为单位，全部分类构建和发布审核通过才提交；失败时远程订阅保留上一次版本。
- 发布审核核对全部分类的排序、重复、黑白性质、来源署名、条目数、文件校验和、默认入口一致性，并用 `AdguardTeam/urlfilter v0.23.4` 验证每一条输出规则。正则额外使用与引擎相同的 Go regexp 实现提前编译，避免无效正则被静默忽略。验证器版本对应 AdGuard Home v0.107.79 的依赖，来源和编译配置见 [tools/engine](tools/engine)。
- 文件锁阻止同一缓存目录的并发构建。`.cache/` 保存缓存与本次日志，不上传仓库；订阅无变化时保留原更新时间。

确认上游数量下降正常后才使用以下选项；该选项不绕过最低数量或下载校验：

```powershell
.\.venv\Scripts\python.exe -X utf8 -B build_filters.py --allow-large-drop
```

## 后续维护与验证

修改 [profiles.json](profiles.json) 调整来源 id、启用状态与组合。id、实际地址与依据在 [registry/sources.json](registry/sources.json)；程序在下载前校验版本族、格式组、强度和地域。禁用分类会停止更新，已生成的旧文件保留，需按实际订阅情况清理。新增来源须先核验原仓库、真实路径、DNS 格式与用途，每天的构建不会猜测地址或自动启用未知来源。

个人规则在 [custom/block.txt](custom/block.txt) 和 [custom/allow.txt](custom/allow.txt)。默认作用于综合版和全量版；个人放行附加 important。其他黑名单可设置 `includeCustom: true`。默认本地文件仅有说明和示例，没有实际生效的个人规则。

`update_rules.py`、`config.json` 保留用于旧版单文件构建。日常入口已切换为 `build_filters.py`，新 `adguard.txt` 对应明确选源的综合版。

```powershell
.\.venv\Scripts\python.exe -X utf8 -B -m unittest discover -s tests -p 'test_*.py'
```

测试覆盖规则优先级与优化前后的拦截决定、匹配范围、分类间独立去重、共享下载、缓存过期、失败保留、恢复、数量保护、配置约束及重复运行。Actions 强制运行真实 AdGuard DNSEngine 的父子域名、精确匹配、例外优先级及 100 组覆盖优化前后比较；本地未设置 `DNS_RULE_VALIDATOR` 时会明确跳过这部分测试。

本地使用已编译验证器运行完整构建和发布审核：

```powershell
.\.venv\Scripts\python.exe -X utf8 build_filters.py --validator .cache/dns-rule-validator.exe
.\.venv\Scripts\python.exe -X utf8 validate_subscriptions.py --validator .cache/dns-rule-validator.exe
```

引擎语法及匹配测试通过不代表真实设备与应用没有误杀。上游原生放行例外在合并后也会影响其他来源的拦截；当前尚未提供逐条规则来源追踪与误杀反馈处理。全量版包含最高强度和服务限制规则，按使用需求选择。
