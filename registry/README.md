# 全部已整理仓库的黑白名单与分类目录

共 23 个已确认规则仓库、51 个来源/版本，本次成功检查 51 个，失败 0 个。
成功来源包含 41 个拦截列表、7 个含放行例外的混合列表、3 个独立白名单。

另有 1 个已下载来源因数量异常或停更标记需要复核，不进入 groups.json 的订阅候选。包含失效来源和参考合并项目，共登记 29 个已知仓库。

范围为此前核验的 27 个订阅和新增的 21 个订阅，按 URL 去重，再补充本次从原仓库确认的独立白名单。不是穷举 GitHub 上全部规则项目。非 GitHub、失败和未支持来源另列于清单中。

## 黑名单、白名单与例外

- [拦截/混合订阅地址](blacklist_links.txt)：添加为 DNS 黑名单时应保留其原生例外。
- [独立白名单订阅地址](whitelist_links.txt)：上游明确用于放行的文件，按用途选用。
- 每个来源的 `blacklist.txt` 和 `whitelist.txt` 在下面的文件列；混合源的白名单是该来源的 DNS 放行例外。
- 放行例外未转成域名，未删除修饰符，未统一附加 `$important`。不能将所有白名单合并后默认套用到每个档位。
- 此目录保留来源调查快照；实际选源在 [profiles.json](../profiles.json)，分类生成结果见 [dist](../dist/README.md)。

## 后续分类订阅

[sources.json](sources.json) 是完整来源登记，包含强度、用途、地域、依据、仓库、URL、启用状态、版本族、格式组和调查时的黑白条目统计。[groups.json](groups.json) 是候选来源分组，不能直接合并全部成员；[profiles.json](../profiles.json) 决定实际选源，[build_filters.py](../build_filters.py) 生成分类订阅。组合边界见 [分类说明](CLASSIFICATION.md)。

强度只采用已查看的上游档位说明；其余为“上游未明确分级”。用途若来自名称或文件名推断，在 JSON 的 categoryBasis 明确标记。

同一来源的不同强度分别保存：HaGeZi Normal / Pro / Pro++ / Ultimate、1Hosts Lite / Xtra 应在对应档位择一。Pro Mini 是 Pro 的体积优化版本。Hosts 精确匹配与 Adblock 子域匹配的范围可能不同，格式差异不作语义去重。

用途标签描述来源覆盖范围，不表示其中每条域名都属于该类。综合来源不能仅凭标签生成“纯广告”或“纯跟踪”规则。

## 中国国内优化（黑名单）

分组标识：`region-china-optimized`。地域维度独立于强度；只选上游明确说明面向中国环境、并提供 DNS 文件的已核验来源。中文名称、仓库语言和 .cn 域名数量不作为地域归类依据。

本分类保留上游的广告、跟踪、恶意软件、HTTPDNS、PCDN 等覆盖范围，不按域名后缀或 IP 国家截断规则；强度未明确时仍记为 unknown。生成时携带所选来源的原生例外。

| 来源 | 原始订阅 | 归类依据 | 支持的 DNS 拦截条目 |
| --- | --- | --- | ---: |
| [AdRules DNS List](https://github.com/Cats-Team/AdRules) | [订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | [上游 README](https://github.com/Cats-Team/AdRules#readme) | 195932 |

独立分类已接入构建程序，输出 [china.txt](../dist/china.txt)。此处计数沿用各来源 checkedUtc 对应的调查快照，最新构建数量见 [dist/manifest.json](../dist/manifest.json)。地域依据核实日期记录在 regionalFocus.evidenceReviewedOn。

## 按仓库整理

### [AdAway/adaway.github.io](https://github.com/AdAway/adaway.github.io)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [AdAway default blocklist](https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt) | 广告 | 上游未明确分级 | 6540 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/adaway-adaway-github-io-hosts-txt-66566edd/blacklist.txt) / [白](sources/adaway-adaway-github-io-hosts-txt-66566edd/whitelist.txt) |

### [AdguardTeam/AdguardFilters](https://github.com/AdguardTeam/AdguardFilters)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [AdGuard Mobile Ads filter](https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt) | 广告 | 上游未明确分级 | 899 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/adguardteam-adguardfilters-mobilefilter-sections-adservers-txt-81ac67be/blacklist.txt) / [白](sources/adguardteam-adguardfilters-mobilefilter-sections-adservers-txt-81ac67be/whitelist.txt) |

### [AdguardTeam/FiltersRegistry](https://github.com/AdguardTeam/FiltersRegistry)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [AdGuard Chinese filter](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | 广告 | 上游未明确分级 | 5894 | 11 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/adguardteam-filtersregistry-filters-filter-224-chinese-filter-txt-4987b98a/blacklist.txt) / [白](sources/adguardteam-filtersregistry-filters-filter-224-chinese-filter-txt-4987b98a/whitelist.txt) |

### [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [AdRules DNS List](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 广告、跟踪/遥测、安全综合 | 上游未明确分级 | 195932 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/cats-team-adrules-dns-txt-35998f0f/blacklist.txt) / [白](sources/cats-team-adrules-dns-txt-35998f0f/whitelist.txt) |

### [DandelionSprout/adfilt](https://github.com/DandelionSprout/adfilt)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [Game Console Adblock List](https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt) | 游戏机 | 上游未明确分级 | 9 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/dandelionsprout-adfilt-gameconsoleadblocklist-txt-2fd8cf2e/blacklist.txt) / [白](sources/dandelionsprout-adfilt-gameconsoleadblocklist-txt-2fd8cf2e/whitelist.txt) |

### [Perflyst/PiHoleBlocklist](https://github.com/Perflyst/PiHoleBlocklist)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [Perflyst and Dandelion Sprout's Smart-TV Blocklist](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | 电视 | 上游未明确分级 | 140 | 9 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/perflyst-piholeblocklist-smarttv-agh-txt-f3772bac/blacklist.txt) / [白](sources/perflyst-piholeblocklist-smarttv-agh-txt-f3772bac/whitelist.txt) |

### [Spam404/lists](https://github.com/Spam404/lists)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [Spam404](https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt) | 安全综合 | 上游未明确分级 | 8140 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/spam404-lists-main-blacklist-txt-694a44a4/blacklist.txt) / [白](sources/spam404-lists-main-blacklist-txt-694a44a4/whitelist.txt) |

### [StevenBlack/hosts](https://github.com/StevenBlack/hosts)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [StevenBlack hosts](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | 广告、跟踪/遥测、安全综合 | 上游未明确分级 | 74759 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/stevenblack-hosts-hosts-603e776c/blacklist.txt) / [白](sources/stevenblack-hosts-hosts-603e776c/whitelist.txt) |

### [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [AWAvenue Ads Rule](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 广告、跟踪/遥测 | 上游未明确分级 | 958 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/tg-twilight-awavenue-ads-rule-awavenue-ads-rule-txt-594187e3/blacklist.txt) / [白](sources/tg-twilight-awavenue-ads-rule-awavenue-ads-rule-txt-594187e3/whitelist.txt) |

### [anudeepND/blacklist](https://github.com/anudeepND/blacklist)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [anudeepND/blacklist / adservers.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt) | 广告、跟踪/遥测、安全综合 | 上游未明确分级 | 42343 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/anudeepnd-blacklist-adservers-txt-e413d034/blacklist.txt) / [白](sources/anudeepnd-blacklist-adservers-txt-e413d034/whitelist.txt) |
| [anudeepND/blacklist / facebook.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt) | 社交平台整站限制 | 上游未明确分级 | 3995 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/anudeepnd-blacklist-facebook-txt-32006df0/blacklist.txt) / [白](sources/anudeepnd-blacklist-facebook-txt-32006df0/whitelist.txt) |
| [anudeepND/blacklist / CoinMiner.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt) | 挖矿 | 上游未明确分级 | 5830 | 0 | 当前 DNS 语法可提取 | 需复核 | [黑](sources/anudeepnd-blacklist-coinminer-txt-61cc5905/blacklist.txt) / [白](sources/anudeepnd-blacklist-coinminer-txt-61cc5905/whitelist.txt) |

### [badmojr/1Hosts](https://github.com/badmojr/1Hosts)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [1Hosts Lite](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | 广告、跟踪/遥测、安全综合 | 均衡 | 102241 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/badmojr-1hosts-lite-adblock-txt-6a71fde5/blacklist.txt) / [白](sources/badmojr-1hosts-lite-adblock-txt-6a71fde5/whitelist.txt) |
| [1Hosts Xtra](https://raw.githubusercontent.com/badmojr/1Hosts/master/Xtra/adblock.txt) | 广告、跟踪/遥测、安全综合 | 激进 | 786132 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/badmojr-1hosts-xtra-adblock-txt-ec275c9c/blacklist.txt) / [白](sources/badmojr-1hosts-xtra-adblock-txt-ec275c9c/whitelist.txt) |

### [banbendalao/ADgk](https://github.com/banbendalao/ADgk)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt) | 广告 | 上游未明确分级 | 3030 | 29 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/banbendalao-adgk-adgk-txt-c99347f4/blacklist.txt) / [白](sources/banbendalao-adgk-adgk-txt-c99347f4/whitelist.txt) |

### [blocklistproject/Lists](https://github.com/blocklistproject/Lists)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [blocklistproject/Lists / abuse-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/abuse-ags.txt) | 安全综合 | 上游未明确分级 | 435051 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-abuse-ags-txt-69397c3c/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-abuse-ags-txt-69397c3c/whitelist.txt) |
| [blocklistproject/Lists / ads-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ads-ags.txt) | 广告 | 上游未明确分级 | 233991 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-ads-ags-txt-21a38910/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-ads-ags-txt-21a38910/whitelist.txt) |
| [blocklistproject/Lists / crypto-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/crypto-ags.txt) | 挖矿 | 上游未明确分级 | 1272 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-crypto-ags-txt-722f85ae/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-crypto-ags-txt-722f85ae/whitelist.txt) |
| [blocklistproject/Lists / fraud-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/fraud-ags.txt) | 诈骗 | 上游未明确分级 | 256184 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-fraud-ags-txt-859f4062/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-fraud-ags-txt-859f4062/whitelist.txt) |
| [blocklistproject/Lists / phishing-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/phishing-ags.txt) | 钓鱼 | 上游未明确分级 | 190191 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-phishing-ags-txt-6ab23539/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-phishing-ags-txt-6ab23539/whitelist.txt) |
| [blocklistproject/Lists / ransomware-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/ransomware-ags.txt) | 勒索软件 | 上游未明确分级 | 1904 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-ransomware-ags-txt-8f253932/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-ransomware-ags-txt-8f253932/whitelist.txt) |
| [blocklistproject/Lists / redirect-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/redirect-ags.txt) | 安全综合 | 上游未明确分级 | 108682 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-redirect-ags-txt-6ece472c/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-redirect-ags-txt-6ece472c/whitelist.txt) |
| [blocklistproject/Lists / scam-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/scam-ags.txt) | 诈骗 | 上游未明确分级 | 8527 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-scam-ags-txt-521f7b7c/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-scam-ags-txt-521f7b7c/whitelist.txt) |
| [blocklistproject/Lists / smart-tv-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/smart-tv-ags.txt) | 电视 | 上游未明确分级 | 77 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-smart-tv-ags-txt-92f6ccb6/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-smart-tv-ags-txt-92f6ccb6/whitelist.txt) |
| [blocklistproject/Lists / tracking-ags.txt](https://raw.githubusercontent.com/blocklistproject/Lists/main/adguard/tracking-ags.txt) | 跟踪/遥测 | 上游未明确分级 | 143866 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/blocklistproject-lists-adguard-tracking-ags-txt-06c487dc/blacklist.txt) / [白](sources/blocklistproject-lists-adguard-tracking-ags-txt-06c487dc/whitelist.txt) |

### [cjx82630/cjxlist](https://github.com/cjx82630/cjxlist)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [CJX's Annoyance List](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | 网页干扰 | 上游未明确分级 | 115 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/cjx82630-cjxlist-cjx-annoyance-txt-d2386b6d/blacklist.txt) / [白](sources/cjx82630-cjxlist-cjx-annoyance-txt-d2386b6d/whitelist.txt) |

### [crazy-max/WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [crazy-max/WindowsSpyBlocker / spy.txt](https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt) | Windows、跟踪/遥测 | 上游未明确分级 | 347 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/crazy-max-windowsspyblocker-data-hosts-spy-txt-a41d8da9/blacklist.txt) / [白](sources/crazy-max-windowsspyblocker-data-hosts-spy-txt-a41d8da9/whitelist.txt) |

### [damengzhu/banad](https://github.com/damengzhu/banad)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [jiekouAD](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | 广告 | 上游未明确分级 | 4508 | 4 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/damengzhu-banad-jiekouad-txt-91a5eb50/blacklist.txt) / [白](sources/damengzhu-banad-jiekouad-txt-91a5eb50/whitelist.txt) |

### [durablenapkin/scamblocklist](https://github.com/durablenapkin/scamblocklist)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [Scam Blocklist by DurableNapkin](https://raw.githubusercontent.com/durablenapkin/scamblocklist/master/adguard.txt) | 诈骗 | 上游未明确分级 | 941 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/durablenapkin-scamblocklist-adguard-txt-f27041d5/blacklist.txt) / [白](sources/durablenapkin-scamblocklist-adguard-txt-f27041d5/whitelist.txt) |

### [hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [DNS-Blocklists PRO mini](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.mini.txt) | 广告、跟踪/遥测、安全综合 | 扩展 | 59779 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-pro-mini-txt-20bb6b45/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-pro-mini-txt-20bb6b45/whitelist.txt) |
| [HaGeZi Ultimate](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/ultimate.txt) | 广告、跟踪/遥测、安全综合 | 最强 | 287467 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-ultimate-txt-bc290ebd/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-ultimate-txt-bc290ebd/whitelist.txt) |
| [HaGeZi Pro++](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.plus.txt) | 广告、跟踪/遥测、安全综合 | 激进 | 251638 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-pro-plus-txt-7a87ce26/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-pro-plus-txt-7a87ce26/whitelist.txt) |
| [HaGeZi Pro](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | 广告、跟踪/遥测、安全综合 | 扩展 | 230960 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-pro-txt-65c8e043/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-pro-txt-65c8e043/whitelist.txt) |
| [HaGeZi Normal](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt) | 广告、跟踪/遥测、安全综合 | 均衡 | 200319 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-multi-txt-ce9f678a/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-multi-txt-ce9f678a/whitelist.txt) |
| [HaGeZi Badware Hoster](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | 托管服务限制 | 专项，不按通用强度排序 | 1238 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-hoster-txt-15f0d4a7/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-hoster-txt-15f0d4a7/whitelist.txt) |
| [HaGeZi DynDNS](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | 动态 DNS 服务限制 | 专项，不按通用强度排序 | 1538 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-dyndns-txt-1d5b17bf/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-dyndns-txt-1d5b17bf/whitelist.txt) |
| [HaGeZi URL Shortener](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/urlshortener.txt) | 短链接服务限制 | 专项，不按通用强度排序 | 9982 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-urlshortener-txt-25500e57/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-urlshortener-txt-25500e57/whitelist.txt) |
| [HaGeZi / whitelist-referral.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt) | 推广/跳转链接放行 | 放行，不适用拦截强度 | 0 | 867 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-whitelist-referral-txt-da8500f6/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-whitelist-referral-txt-da8500f6/whitelist.txt) |
| [HaGeZi / whitelist-referral-native.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral-native.txt) | 推广/跳转链接放行 | 放行，不适用拦截强度 | 0 | 1609 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-whitelist-referral-native-txt-69481aca/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-whitelist-referral-native-txt-69481aca/whitelist.txt) |
| [HaGeZi / whitelist-urlshortener.txt](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-urlshortener.txt) | 短链接放行 | 放行，不适用拦截强度 | 0 | 9975 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/hagezi-dns-blocklists-adblock-whitelist-urlshortener-txt-c2ee3e5c/blacklist.txt) / [白](sources/hagezi-dns-blocklists-adblock-whitelist-urlshortener-txt-c2ee3e5c/whitelist.txt) |

### [hoshsadiq/adblock-nocoin-list](https://github.com/hoshsadiq/adblock-nocoin-list)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [NoCoin Filter List](https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt) | 挖矿 | 上游未明确分级 | 47 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/hoshsadiq-adblock-nocoin-list-nocoin-txt-1aa9d130/blacklist.txt) / [白](sources/hoshsadiq-adblock-nocoin-list-nocoin-txt-1aa9d130/whitelist.txt) |

### [jdlingyu/ad-wars](https://github.com/jdlingyu/ad-wars)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [大圣净化](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | 广告 | 上游未明确分级 | 1645 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/jdlingyu-ad-wars-hosts-eb100586/blacklist.txt) / [白](sources/jdlingyu-ad-wars-hosts-eb100586/whitelist.txt) |

### [jerryn70/GoodbyeAds](https://github.com/jerryn70/GoodbyeAds)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [jerryn70/GoodbyeAds / GoodbyeAds.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Hosts/GoodbyeAds.txt) | 广告、跟踪/遥测、安全综合 | 上游未明确分级 | 277744 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-hosts-goodbyeads-txt-882683a5/blacklist.txt) / [白](sources/jerryn70-goodbyeads-hosts-goodbyeads-txt-882683a5/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-AdBlock-Filter.txt) | 广告、跟踪/遥测、安全综合 | 上游未明确分级 | 277714 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-formats-goodbyeads-adblock-filter-txt-d11c0acd/blacklist.txt) / [白](sources/jerryn70-goodbyeads-formats-goodbyeads-adblock-filter-txt-d11c0acd/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-Xiaomi-Extension.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Xiaomi-Extension.txt) | 小米 | 上游未明确分级 | 278 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-extension-goodbyeads-xiaomi-extension-txt-2ab84d66/blacklist.txt) / [白](sources/jerryn70-goodbyeads-extension-goodbyeads-xiaomi-extension-txt-2ab84d66/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-Samsung-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Samsung-AdBlock.txt) | 三星 | 上游未明确分级 | 101 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-extension-goodbyeads-samsung-adblock-txt-10d171b5/blacklist.txt) / [白](sources/jerryn70-goodbyeads-extension-goodbyeads-samsung-adblock-txt-10d171b5/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-Spotify-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-Spotify-AdBlock.txt) | Spotify | 上游未明确分级 | 3780 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-extension-goodbyeads-spotify-adblock-txt-4a00db86/blacklist.txt) / [白](sources/jerryn70-goodbyeads-extension-goodbyeads-spotify-adblock-txt-4a00db86/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Extension/GoodbyeAds-YouTube-AdBlock.txt) | YouTube | 上游未明确分级 | 97645 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-extension-goodbyeads-youtube-adblock-txt-84c5ae17/blacklist.txt) / [白](sources/jerryn70-goodbyeads-extension-goodbyeads-youtube-adblock-txt-84c5ae17/whitelist.txt) |
| [jerryn70/GoodbyeAds / GoodbyeAds-YouTube-AdBlock-Filter.txt](https://raw.githubusercontent.com/jerryn70/GoodbyeAds/master/Formats/GoodbyeAds-YouTube-AdBlock-Filter.txt) | YouTube | 上游未明确分级 | 97645 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/jerryn70-goodbyeads-formats-goodbyeads-youtube-adblock-filter-txt-992d6a26/blacklist.txt) / [白](sources/jerryn70-goodbyeads-formats-goodbyeads-youtube-adblock-filter-txt-992d6a26/whitelist.txt) |

### [mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [The Big List of Hacked Malware Web Sites](https://raw.githubusercontent.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites/master/hacked-domains.list) | 恶意软件 | 上游未明确分级 | 9 | 0 | 当前 DNS 语法可提取 | 可选择，待组合验证 | [黑](sources/mitchellkrogza-the-big-list-of-hacked-malware-web-sites-hacked-domains-list-5df168a2/blacklist.txt) / [白](sources/mitchellkrogza-the-big-list-of-hacked-malware-web-sites-hacked-domains-list-5df168a2/whitelist.txt) |

### [xinggsf/Adblock-Plus-Rule](https://github.com/xinggsf/Adblock-Plus-Rule)

| 来源 / 版本 | 用途 | 强度 | 黑名单条目 | DNS 放行例外 | 格式支持 | 分类候选 | 文件 |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| [xinggsf mv](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | 视频场景 | 上游未明确分级 | 27 | 0 | 仅支持的 DNS 子集 | 可选择，待组合验证 | [黑](sources/xinggsf-adblock-plus-rule-mv-txt-b8142164/blacklist.txt) / [白](sources/xinggsf-adblock-plus-rule-mv-txt-b8142164/whitelist.txt) |

## 失效来源及参考仓库

| 仓库 | 用途 |
| --- | --- |
| [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) | 参考合并项目，不作为原始规则订阅 |
| [AdguardTeam/HostlistsRegistry](https://github.com/AdguardTeam/HostlistsRegistry) | 没有通过核验的可用来源；路径或格式问题见排除记录 |
| [DivineEngine/AdGuardFilter](https://github.com/DivineEngine/AdGuardFilter) | 没有通过核验的可用来源；路径或格式问题见排除记录 |
| [hululu1068/AdGuard-Rule](https://github.com/hululu1068/AdGuard-Rule) | 参考合并项目，不作为原始规则订阅 |
| [nextdns/metadata](https://github.com/nextdns/metadata) | 没有通过核验的可用来源；路径或格式问题见排除记录 |
| [zhuanshenlikaini/AdguardHome-Rules](https://github.com/zhuanshenlikaini/AdguardHome-Rules) | 参考合并项目，不作为原始规则订阅 |

## 白名单目录调查

目录调查只记录实际发现的路径，文件名包含 whitelist 不足以证明它是可订阅白名单。StevenBlack 的 whitelist.example 是本地生成器示例；GoodbyeAds 的 Whitelist/Keep this 是目录占位文件。它们没有加入白名单订阅。

| 仓库 | 调查状态 | 候选路径 |
| --- | --- | --- |
| [仓库](https://github.com/AdguardTeam/FiltersRegistry) | 已检查，目录截断 | 未发现相关命名文件 |
| [仓库](https://github.com/AdguardTeam/AdguardFilters) | 已检查 | AnnoyancesFilter/Cookies/sections/cookies_allowlist.txt、AnnoyancesFilter/MobileApp/sections/mobile-app_allowlist.txt、AnnoyancesFilter/Popups/sections/popups_allowlist.txt、AnnoyancesFilter/Popups/sections/push-notifications_allowlist.txt、AnnoyancesFilter/Popups/sections/subscriptions_allowlist.txt、BaseFilter/sections/allowlist.txt、BaseFilter/sections/allowlist_stealth.txt、ChineseFilter/sections/allowlist.txt、CyrillicFilters/RussianFilter/sections/allowlist.txt、CyrillicFilters/UkrainianFilter/sections/allowlist.txt、CyrillicFilters/common-sections/allowlist.txt、DutchFilter/sections/allowlist.txt、ExperimentalFilter/sections/English/allowlist.txt、ExperimentalFilter/sections/Russian/allowlist.txt、FrenchFilter/sections/allowlist.txt、GermanFilter/sections/allowlist.txt、ItalianFilter/sections/allow |
| [仓库](https://github.com/Cats-Team/AdRules) | 已检查 | mod/rules/dns-allowlist.txt |
| [仓库](https://github.com/cjx82630/cjxlist) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/xinggsf/Adblock-Plus-Rule) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/damengzhu/banad) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/hagezi/dns-blocklists) | 已检查 | adblock/whitelist-referral-native.txt、adblock/whitelist-referral.txt、adblock/whitelist-urlshortener.txt、wildcard/whitelist-referral-onlydomains.txt |
| [仓库](https://github.com/StevenBlack/hosts) | 已检查 | whitelist.example |
| [仓库](https://github.com/banbendalao/ADgk) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/jdlingyu/ad-wars) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/AdAway/adaway.github.io) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/Perflyst/PiHoleBlocklist) | 已检查 | 未发现相关命名文件 |
| [仓库](https://github.com/durablenapkin/scamblocklist) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/DandelionSprout/adfilt) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/hoshsadiq/adblock-nocoin-list) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/Spam404/lists) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/badmojr/1Hosts) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/blocklistproject/Lists) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/anudeepND/blacklist) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/crazy-max/WindowsSpyBlocker) | 未验证 | HTTP Error 403: rate limit exceeded |
| [仓库](https://github.com/jerryn70/GoodbyeAds) | 未验证 | HTTP Error 403: rate limit exceeded |

这是目录与已知文件的检查，不能证明所有项目都不存在其他内部白名单。

## 失败与排除

- [anudeepND/blacklist / CoinMiner.txt](https://raw.githubusercontent.com/anudeepND/blacklist/master/CoinMiner.txt): 上游明确停止更新，保留历史整理，但默认不进入分类候选。

此前非 GitHub、404、超出大小上限等未通过来源，保留在 sources.json 的 excludedSources，未参与本次规则提取。

## 重新整理

```powershell
.\.venv\Scripts\python.exe -B organize_repository_rules.py
```

读取两份核验清单，重新下载规则并更新此目录；失败的来源不会被记为本次可用。旧快照可能仍在目录内，以 sources.json 的 status 与 outputs 为准。
