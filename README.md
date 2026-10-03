# AdGuard Home / mihomo 国内规则订阅

[![每日构建](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml/badge.svg)](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)

仅合并、去重上游规则，原作者及贡献者保留署名与许可。每天北京时间 **04:23** 自动检查、构建。

<!-- build-status:start -->
> 最近成功发布：**2026-10-03 17:17:15（北京时间）**
>
> 最近检查：2026-10-03 17:17:15 · **全部通过校验**
>
> 本次通过：AdGuard Home 3 / mihomo 3 · [变化与失败详情](dist/publication.json)
<!-- build-status:end -->

<!-- subscriptions:start -->
## AdGuard Home 订阅

在 AdGuard Home → **过滤器 → DNS 黑名单**添加，三档任选一个。日常推荐国内精简；增强与全量版覆盖更广，仍可能影响正常功能。

| 规则 | 规则数 | 适用范围 | 原始链接 | 加速1 | 加速2 |
| --- | ---: | --- | --- | --- | --- |
| 国内精简（推荐） | 5,585 | 国内 Lite + 秋风纯广告 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/adguard.txt) |
| 国内增强 | 211,238 | 增加隐私与国内 DNS 合集 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 中文源全量（按需） | 341,316 | 当前入选中文/中国地区来源 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |

每条规则的三个链接任选一个订阅。数量随成功构建更新，含原生放行例外；每个订阅独立去重。

三档均保留原生放行例外并应用个人规则；中文文档不代表只包含中国域名。
<!-- subscriptions:end -->

<!-- mihomo:start -->
## mihomo 订阅

使用 **MRS 域名集 + 配套正则与例外**；[配置合并方法](dist/mihomo/README.md)。旧配置需重新合并一次新版片段，此后规则集按日刷新。

| 分类 | 拦截条目 | 例外条目 | 原始配置 | Boki 配置 | GHFast 配置 |
| --- | ---: | ---: | --- | --- | --- |
| 国内精简 | 5,569 | 16 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-ghfast.yaml) |
| 国内增强 | 211,115 | 123 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-ghfast.yaml) |
| 中文源全量 | 341,013 | 303 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-ghfast.yaml) |
<!-- mihomo:end -->

<!-- upstream:start -->
当前选用 **8 个来源文件**，来自 **6 个 GitHub 原仓库**。

<details>
<summary>查看上游作者、原始订阅与规则数量</summary>

数量为来源合并前的支持条目数。仓库账号不代表全部原创作者，完整署名以各上游说明为准。

| 维护账号 / 原始项目 | 原始规则文件 | 支持规则数 |
| --- | --- | ---: |
| [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) | [rules/adblockdns.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt) | 219,333 |
| [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters) | [rules/adblockdnslite.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt) | 5,388 |
| [8680/GOODBYEADS](https://github.com/8680/GOODBYEADS) | [data/rules/dns.txt](https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt) | 114,252 |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | [rule/AdGuard/Advertising/Advertising.txt](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/AdGuard/Advertising/Advertising.txt) | 280,859 |
| [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | [dns.txt](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | 197,268 |
| [privacy-protection-tools/anti-AD](https://github.com/privacy-protection-tools/anti-AD) | [anti-ad-easylist.txt](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) | 93,908 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt) | 866 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt) | 652 |

</details>

[来源登记](registry/README.md) · [上游许可与署名](upstream/README.md)；合并产物遵循各上游许可。
<!-- upstream:end -->

## 选源与迁移

只选已核实中文仓库文档或明确面向中国 DNS 环境的原始 GitHub 来源。日常版采用国内 Lite 与秋风纯广告，增强版加入隐私与国内合集；全量版限于当前入选项目，同系列只保留一个版本。中文合集可能包含全球规则及 HTTPDNS/PCDN 等限制，全量不保证低误杀。

**旧用户：**原有 `adguard.txt`、`combined.txt`、`china.txt`、`full.txt` 地址继续有效，请强制更新。原先其他 30 个分类已撤下，请删除对应订阅；mihomo 用户同时删除那些分类的规则与 provider。三档任选一个即可。

<details>
<summary>维护与本地运行</summary>

- [选源配置](profiles.json) · [分类依据](registry/CLASSIFICATION.md) · [构建统计](dist/manifest.json)。
- 个人规则：[拦截](custom/block.txt) / [放行](custom/allow.txt)，三档均应用。
- 各档独立去重，保留精确/子域匹配、优先级与原生例外。只删除语义已被覆盖的规则，不扩大域名匹配。
- 下载异常、数量骤变、放行例外骤减、常用服务样本被拦截或引擎验证失败，暂停对应发布并保留旧版。样本验证无法覆盖所有 App。

Python 3.12 创建环境后执行完整发布（GitHub Actions 已自动配置验证器）：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe publish_filters.py --validator .cache/dns-rule-validator.exe --mihomo .cache/mihomo/mihomo.exe
```

新增来源先登记到 `registry/reviewed_sources.json`，用 `refresh_source_registry.py --validator <验证器路径>` 核验，再修改选源配置；程序不会自动启用发现的新源。

</details>
