<div align="center">

<h1>AdGuard Home 合并规则</h1>

仅合并、去重与格式转换。规则由上游作者维护。

</div>

**订阅更新：2026-10-03 21:04:52** · 每天 **04:23** 自动构建（北京时间）。
[自动构建：构建成功](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml) · [构建报告](dist/report.json)

## 订阅

优先选择 **纯广告**。AdGuard Home 添加到「DNS 黑名单」；mihomo 使用对应配置片段。

| 订阅 | 条目数 | 主要内容 | AdGuard Home | mihomo |
|---|---:|---|---|---|
| 纯广告（推荐） | 652 | 仅广告 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-ghfast.yaml) |
| 国内广告＋隐私 | 866 | 广告、隐私 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-ghfast.yaml) |
| 广告＋不受欢迎 | 748 | 广告、功能拦截 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-ghfast.yaml) |
| 秋风完整 | 962 | 广告、隐私、功能拦截 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-ghfast.yaml) |
| PCDN（按需） | 41 | 两份 PCDN 源合并 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-ghfast.yaml) |
| oisd small | 57,656 | 原版 small 列表 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-ghfast.yaml) |
| 综合广告＋隐私 | 57,919 | 秋风广告＋隐私、oisd | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-ghfast.yaml) |
| DNS 全量（按需） | 57,969 | 秋风完整、oisd、PCDN | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full.yaml) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-boki.yaml) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-ghfast.yaml) |

数量为去重后的规则行，包含例外；通配符规则不等于一个域名。
**PCDN、含「不受欢迎」及全量方案可能影响视频、更新或推送，按需使用。**

<details>
<summary>使用说明与合并方式</summary>

- 每次选择一个主方案；PCDN 可单独加订。秋风的四个版本互不混用。
- AdGuard Home 文件保留 `@@` 例外，无需另加同一份白名单。
- mihomo 将 `rule-providers` 和 `rules` 合并到现有配置，拦截规则放在兜底规则前。例外继续后续分流，不强制 DIRECT。
- 各订阅独立去重；不裁剪父子域名覆盖关系，不把 URL 路径扩大成整站拦截。
- 下载或校验异常时使用 72 小时内的已校验缓存；缓存不可用则停止发布，保留上一版。
- 语法和样例检查不能保证没有误拦截；加速线路异常时使用原始链接。

</details>

<details>
<summary>浏览器专用规则</summary>

仅供浏览器拦截器使用，**不能导入 AdGuard Home**。网页元素、路径、脚本和例外规则均保留。

| 分类 | 条目数 | 订阅 |
|---|---:|---|
| 去 App 下载提示 | 874 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) |
| 悬浮广告 | 5,892 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) |
| 乘风视频 | 134 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) |
| 乘风广告 | 1,168 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) |
| 浏览器合并 | 8,065 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) / [Boki](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) / [GHFast](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) |

</details>

## 上游来源

共 **11 个订阅地址**。本项目仅做合并，作者与许可说明保留在输出文件中。

<details>
<summary>查看全部来源、作者与分类</summary>

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
修改来源或分类后，提交 `sources.json` 即可触发自动构建。

</details>
