<h1 align="center">adguardhome-compiled-filters</h1>

<p align="center">AdGuard Home DNS 规则 · 自动合并 · 独立分类 · 每日更新</p>

[![自动更新](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml/badge.svg)](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)

<!-- build-status:start -->
> 最近构建：**2026-10-01 09:10:59（北京时间）**
>
> 状态：**成功，已通过发布校验** · 分类 30/30 · 来源：新下载 41，缓存 0，失败 0
<!-- build-status:end -->

本项目仅获取、合并和去重上游规则，**规则由原作者及贡献者维护**。每天北京时间 **04:23** 由 GitHub Actions 自动构建，无需本机开机。

## 订阅

在 AdGuard Home **过滤器 → DNS 黑名单** 添加订阅。综合版或全量版选其一，其他分类按需使用。

| 分类 | 内容 | 订阅 |
| --- | --- | --- |
| 综合版 | HaGeZi Normal ＋ AdRules DNS ＋ AWAvenue | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) |
| 国内优化 | 面向中国使用环境的 AdRules DNS | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 全量版 | 34 个已核验兼容来源，含最高档位及专项限制规则 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |
| 均衡 | HaGeZi Normal | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/balanced.txt) |
| 扩展 | HaGeZi Pro | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/extended.txt) |
| 激进 | HaGeZi Pro++ | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/aggressive.txt) |
| 最强 | HaGeZi Ultimate | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/maximum.txt) |

强度档位任选一个。广告、跟踪、安全、电视、游戏机、Windows、小米、三星等专项与 1Hosts 替代版本见 **[全部分类订阅](dist/README.md)**。

独立白名单添加到 **DNS 白名单**：[跳转放行](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral.txt) · [referral-native](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-referral-native.txt) · [短链接放行](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/allow-shorteners.txt)。它们不会自动并入黑名单。

全量版含社交平台、短链接、动态 DNS 等服务限制，可能影响正常功能。DNS 过滤无法区分同一域名内的广告与正常内容；实际误杀需根据使用情况调整。

## 上游与署名

当前选用 41 个来源文件，来自 17 个 GitHub 原仓库。原始订阅地址写在每个规则文件头部，完整登记见 [sources.json](registry/sources.json)，[许可原文](upstream/README.md) 保留各上游的许可与署名要求。

<details>
<summary>查看上游仓库与维护账号</summary>

仓库所属账号不代表全部原创作者，原作者及间接来源以各上游说明为准。合并产物经过格式处理和去重，本项目不为上游规则另行声明统一许可。

| 维护账号 / 组织 | 原始仓库 |
| --- | --- |
| AdguardTeam | [AdguardFilters](https://github.com/AdguardTeam/AdguardFilters) |
| Cats-Team | [AdRules](https://github.com/Cats-Team/AdRules) |
| TG-Twilight | [AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) |
| hagezi | [dns-blocklists](https://github.com/hagezi/dns-blocklists) |
| badmojr | [1Hosts](https://github.com/badmojr/1Hosts) |
| AdAway | [adaway.github.io](https://github.com/AdAway/adaway.github.io) |
| StevenBlack | [hosts](https://github.com/StevenBlack/hosts) |
| jdlingyu | [ad-wars](https://github.com/jdlingyu/ad-wars) |
| Perflyst | [PiHoleBlocklist](https://github.com/Perflyst/PiHoleBlocklist) |
| DandelionSprout | [adfilt](https://github.com/DandelionSprout/adfilt) |
| durablenapkin | [scamblocklist](https://github.com/durablenapkin/scamblocklist) |
| Spam404 | [lists](https://github.com/Spam404/lists) |
| mitchellkrogza | [The-Big-List-of-Hacked-Malware-Web-Sites](https://github.com/mitchellkrogza/The-Big-List-of-Hacked-Malware-Web-Sites) |
| blocklistproject | [Lists](https://github.com/blocklistproject/Lists) |
| anudeepND | [blacklist](https://github.com/anudeepND/blacklist) |
| crazy-max | [WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker) |
| jerryn70 | [GoodbyeAds](https://github.com/jerryn70/GoodbyeAds) |

</details>

## 维护

- 分类与选源：[profiles.json](profiles.json)。分类依据：[分类说明](registry/CLASSIFICATION.md)；全量选源：[核验清单](registry/full_selection.json)。新增来源须核实真实 GitHub 仓库与文件，程序不猜测地址。
- 个人规则：[block.txt](custom/block.txt) / [allow.txt](custom/allow.txt)，默认作用于综合版和全量版。个人放行附加 `important`。
- 去重在每个订阅内部独立进行，分类之间允许重复；只拦截子域名不会扩大到父域名。覆盖优化只删除已被现有同动作、同优先级父域规则覆盖的条目，可用 `coverageOptimization: false` 关闭。
- 黑名单保留上游原生例外；合并后的例外可能影响其他来源。强度、用途和国内优化按来源证据选取，分类不保证每条域名只属于单一用途。
- 发布前用 AdGuard 官方引擎验证全部产物。网络异常可使用 72 小时内有效缓存；数量异常或校验失败时保留上次发布的订阅，仅更新首页的构建状态。

Python 3.12 本地运行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -X utf8 build_filters.py
```

GitHub Actions 自动编译官方引擎验证器并执行完整校验，本地完整校验需使用 `--validator` 指定验证器。构建时间表示最近一次执行完成；规则文件的更新时间仅在规则内容变化时改变。

[运行记录与日志](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml) · [构建统计](dist/manifest.json) · [来源分类目录](registry/README.md)
