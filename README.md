<div align="center">

<h1>AdGuard Home 合并规则</h1>

合并上游规则，独立去重，每日自动更新。

</div>

更新：**2026-10-03 21:27:41**（北京时间） · [构建状态：构建成功](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)

## AdGuard Home

推荐从 **纯广告** 开始，添加到「DNS 黑名单」。每个方案已保留上游例外。

| 订阅 | 规则数 | 原始链接 | 加速 1 | 加速 2 |
|---|---:|---|---|---|
| 纯广告（推荐） | 652 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) |
| 国内广告＋隐私 | 866 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 广告＋不受欢迎 | 748 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) |
| 秋风完整 | 962 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) |
| PCDN（按需） | 41 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) |
| oisd small | 57,656 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) |
| 综合广告＋隐私 | 57,919 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) |
| DNS 全量（按需） | 57,969 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |

规则数包含拦截与例外。PCDN、含「不受欢迎」及全量方案按需使用，可能影响视频、更新或推送。

<details>
<summary>mihomo 订阅</summary>

将配置片段中的 `rule-providers` 和 `rules` 合并到现有配置，放在兜底规则前。
例外继续后续分流，不强制 DIRECT。

| 订阅 | 原始配置 | 加速 1 | 加速 2 |
|---|---|---|---|
| 纯广告（推荐） | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-ghfast.yaml) |
| 国内广告＋隐私 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-ghfast.yaml) |
| 广告＋不受欢迎 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-ghfast.yaml) |
| 秋风完整 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-ghfast.yaml) |
| PCDN（按需） | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-ghfast.yaml) |
| oisd small | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-ghfast.yaml) |
| 综合广告＋隐私 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-ghfast.yaml) |
| DNS 全量（按需） | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full.yaml) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-boki.yaml) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-ghfast.yaml) |

</details>

<details>
<summary>规则数量怎么算？</summary>

DNS 全量 **57,969 条**，包含 **57,966 条拦截**和 **3 条例外**。

| 全量使用的来源 | 原始有效行 | 源内去重后的 DNS 规则 |
|---|---:|---:|
| 秋风完整 | 965 | 962 |
| oisd small | 57,656 | 57,656 |
| BiliCDN PCDN | 11 | 9 |
| AntiPCDN | 34 | 34 |

源内去重后共 **58,661 条**，再去除 **692 条跨源重复**，发布 **57,969 条**。

浏览器合并版 **8,065 条**单独统计，保留网页元素、路径、脚本和例外规则。

秋风四种方案存在重叠，全量选用完整版本；各订阅之间也有重叠，不能将表中数量直接相加。
浏览器规则含无法在 DNS 层保留原范围的条件与例外，因此单独输出。
另外跳过了 **2 条带 URL 路径的规则**，保留其原始范围，没有扩大为整站拦截。

[完整构建报告](dist/report.json)

</details>

<details>
<summary>使用说明与合并方式</summary>

- 每次选择一个主方案；PCDN 可单独加订。秋风的四个版本互不混用。
- AdGuard Home 文件保留 `@@` 例外，无需另加同一份白名单。
- 各订阅独立去重；不裁剪父子域名覆盖关系，不把 URL 路径扩大成整站拦截。
- 下载或校验异常时使用 72 小时内的已校验缓存；缓存不可用则停止发布，保留上一版。
- 语法和样例检查不能保证没有误拦截；加速线路异常时使用原始链接。

</details>

<details>
<summary>浏览器专用规则</summary>

仅供浏览器拦截器使用，**不能导入 AdGuard Home**。网页元素、路径、脚本和例外规则均保留。

| 分类 | 规则数 | 原始链接 | 加速 1 | 加速 2 |
|---|---:|---|---|---|
| 去 App 下载提示 | 874 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) |
| 悬浮广告 | 5,892 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) |
| 乘风视频 | 134 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) |
| 乘风广告 | 1,168 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) |
| 浏览器合并 | 8,065 | [订阅](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) | [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) | [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) |

</details>

<details>
<summary>上游来源与作者</summary>

共 **11 个订阅地址**。本项目仅做合并，规则由下列上游作者维护。

| 作者 / 项目 | 原始规则 | 分类 | DNS 可用条目 |
|---|---|---|---:|
| [Li-Dong-Don/AdGuard-BiliCDN-Rules](https://github.com/Li-Dong-Don/AdGuard-BiliCDN-Rules) | [BiliCDN PCDN](https://raw.githubusercontent.com/tonydongguwpi/AdGuard-BiliCDN-Rules/refs/heads/main/adguard.txt) | PCDN | 9 |
| [xianhongtao/AdGuard-AntiPCDN-Rules](https://github.com/xianhongtao/AdGuard-AntiPCDN-Rules) | [AntiPCDN](https://raw.githubusercontent.com/xianhongtao/AdGuard-AntiPCDN-Rules/refs/heads/main/adguard.txt) | PCDN | 34 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风完整](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 广告、隐私、不受欢迎 | 962 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风纯广告](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt) | 仅广告 | 652 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风广告＋不受欢迎](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Privacy.txt) | 广告、不受欢迎 | 748 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风广告＋隐私](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt) | 广告、隐私 | 866 |
| [Noyllopa/NoAppDownload](https://github.com/Noyllopa/NoAppDownload) | [NoAppDownload](https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt) | 去 App 下载提示 | 浏览器专用 |
| [damengzhu/banad](https://github.com/damengzhu/banad) | [大萌主悬浮广告](https://raw.githubusercontent.com/damengzhu/banad/refs/heads/main/jiekouAD.txt) | 悬浮广告 | 浏览器专用 |
| [xinggsf/Adblock-Plus-Rule](https://github.com/xinggsf/Adblock-Plus-Rule) | [乘风视频](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | 视频广告 | 浏览器专用 |
| [xinggsf/Adblock-Plus-Rule](https://github.com/xinggsf/Adblock-Plus-Rule) | [乘风广告](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt) | 网页广告 | 浏览器专用 |
| [Stephan van Ruth (sjhgvr)](https://oisd.nl/) | [oisd small](https://small.oisd.nl/) | oisd small | 57,656 |

[上游许可证](licenses/) · [完整统计与跳过原因](dist/report.json)
未声明许可的来源按原样注明，不替作者指定许可证。

</details>

<details>
<summary>运行与维护</summary>

自动构建使用 [sources.json](sources.json) 管理来源和组合，无需 Excel 文件。

本地使用 Python 3.12、Go 1.27.1；Python 合并程序无需 pip 依赖。

```powershell
python tools/install_engines.py
python compile_rules.py
```

已登录 GitHub CLI 时，可使用 `python compile_rules.py --github-api` 下载相同上游文件。
修改来源或分类后，提交 `sources.json` 即可触发自动构建。每天北京时间 **04:23** 自动更新。

</details>
