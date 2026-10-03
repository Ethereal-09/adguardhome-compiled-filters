# AdGuard Home 合并规则

按提供的 Excel 选源，仅合并与去重。规则由上游作者维护。

最近构建：**2026-10-03 20:55:08 UTC+8** · 成功。每天北京时间 **04:23** 自动更新。

优先使用「纯广告」；PCDN 和含「不受欢迎」的方案可能影响视频、更新或推送，请按需选用。
同一份 DNS 全量只选秋风完整版本，四个秋风变体不会混用。

## AdGuard Home

添加到「DNS 黑名单」。文件中的 `@@` 例外已保留，无需另加白名单。

| 订阅 | 拦截 / 例外 | 内容 | 链接 |
|---|---:|---|---|
| 纯广告（最小干预） | 652 / 0 | 国内广告；优先从此版本开始使用。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads.txt) |
| 国内广告＋隐私 | 866 / 0 | 国内广告、隐私；采用上游 No.Unwelcome 版本。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/china.txt) |
| 广告＋不受欢迎 | 748 / 0 | 保留统计与遥测；可能限制更新、推送、PCDN 等功能。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/ads-unwelcome.txt) |
| 秋风完整 | 962 / 0 | 采用表格中的秋风完整方案，包含广告、隐私和不受欢迎规则。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/awa-full.txt) |
| PCDN（单独可选） | 38 / 3 | 两份 PCDN 源合并；可能影响视频加载与节点选择。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/pcdn.txt) |
| oisd small（单独可选） | 57,656 / 0 | 原始 oisd small 列表；不按完整 oisd 的描述推断 small 的覆盖范围。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/oisd.txt) |
| 综合广告＋隐私 | 57,919 / 0 | 秋风广告＋隐私合并 oisd small；不额外加入两份 PCDN 源。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/combined.txt) |
| DNS 全量（按需） | 57,966 / 3 | 表格中可安全转换的 DNS 源全量；包含功能拦截，浏览器专用源不计入。 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/full.txt) |

订阅实际更新时间：2026-10-03 20:55:21 UTC+8。数量按最终去重规则行统计，通配符不等于一个域名。

## mihomo

使用对应配置片段，将 `rule-providers` 和 `rules` 合并到现有配置；拦截规则放在兜底规则前。
例外跳过本订阅的拦截并继续后续分流，不强制 DIRECT。原始与两条加速配置均提供。

| 订阅 | 配置片段 |
|---|---|
| 纯广告（最小干预） | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-ghfast.yaml) |
| 国内广告＋隐私 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/china-ghfast.yaml) |
| 广告＋不受欢迎 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/ads-unwelcome-ghfast.yaml) |
| 秋风完整 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/awa-full-ghfast.yaml) |
| PCDN（单独可选） | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/pcdn-ghfast.yaml) |
| oisd small（单独可选） | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/oisd-ghfast.yaml) |
| 综合广告＋隐私 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/combined-ghfast.yaml) |
| DNS 全量（按需） | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full.yaml) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-boki.yaml) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/mihomo/full-ghfast.yaml) |

## 浏览器规则

以下文件保留网页元素、路径、脚本和例外规则，**仅供浏览器拦截器使用，不能导入 AdGuard Home**。

| 分类 | 条目 | 链接 |
|---|---:|---|
| 去 App 下载提示 | 874 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/noapp.txt) |
| 悬浮广告 | 5892 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/adult-ads.txt) |
| 乘风视频 | 134 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/video.txt) |
| 乘风广告 | 1168 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/browser-ads.txt) |
| 浏览器合并 | 8065 | [原始](https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) · [加速 1](https://github.boki.moe/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) · [加速 2](https://ghfast.top/https://raw.githubusercontent.com/Ethereal-09/adguardhome-compiled-filters/main/dist/browser/combined.txt) |

<details>
<summary>上游来源与作者（Excel 中全部 11 个地址）</summary>

| 作者 / 项目 | 规则文件 | 类型 | 有效行 / DNS 可用 |
|---|---|---|---:|
| [Li-Dong-Don/AdGuard-BiliCDN-Rules](https://github.com/Li-Dong-Don/AdGuard-BiliCDN-Rules) | [BiliCDN PCDN](https://raw.githubusercontent.com/tonydongguwpi/AdGuard-BiliCDN-Rules/refs/heads/main/adguard.txt) | PCDN | 11 / 9 |
| [xianhongtao/AdGuard-AntiPCDN-Rules](https://github.com/xianhongtao/AdGuard-AntiPCDN-Rules) | [AntiPCDN](https://raw.githubusercontent.com/xianhongtao/AdGuard-AntiPCDN-Rules/refs/heads/main/adguard.txt) | PCDN | 34 / 34 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风完整](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | 广告＋隐私＋不受欢迎 （不受欢迎指强制更新、P2P/PCDN、推送、云控下发一类） | 965 / 962 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风纯广告](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt) | 仅广告 | 655 / 652 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风广告＋不受欢迎](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Privacy.txt) | 广告＋不受欢迎+不包含隐私规则 | 751 / 748 |
| [TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) | [秋风广告＋隐私](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt) | 广告＋隐私+不包含不受欢迎规则 | 869 / 866 |
| [Noyllopa/NoAppDownload](https://github.com/Noyllopa/NoAppDownload) | [NoAppDownload](https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt) | 去 App 下载提示广告过滤规则 | 877 / 0 |
| [damengzhu/banad](https://github.com/damengzhu/banad) | [大萌主悬浮广告](https://raw.githubusercontent.com/damengzhu/banad/refs/heads/main/jiekouAD.txt) | 去除色情悬浮广告 | 5894 / 0 |
| [xinggsf/Adblock-Plus-Rule](https://github.com/xinggsf/Adblock-Plus-Rule) | [乘风视频](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | 视频过滤规则 | 134 / 0 |
| [xinggsf/Adblock-Plus-Rule](https://github.com/xinggsf/Adblock-Plus-Rule) | [乘风广告](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt) | 广告过滤规则 | 1169 / 0 |
| [Stephan van Ruth (sjhgvr)](https://oisd.nl/) | [oisd small](https://small.oisd.nl/) | 完整的列表阻止了广告、（移动）应用程序广告、网络钓鱼、恶意广告、恶意软件、间谍软件、勒索软件、加密货币劫持、诈骗 ... 遥测/分析/跟踪（在不需要正常功能的地方） | 57656 / 57656 |

完整来源、许可、跳过原因、缓存状态与功能域名检查见 [构建报告](dist/report.json)。
上游许可证保存在 [licenses](licenses/)。未声明许可的源按原样注明，不替作者指定许可证。

</details>

## 运行与维护

Python 3.12，合并程序使用标准库，无需 pip 依赖。GitHub Actions 自动安装固定版本的校验引擎并运行测试。

```powershell
python tools/install_engines.py
python compile_rules.py
```

本地需要 Go 1.27.1；Windows 已登录 GitHub CLI 时可用 `python compile_rules.py --github-api` 从相同上游文件的 API 下载。
[sources.xlsx](sources.xlsx) 保留原始表格，[sources.json](sources.json) 管理分类与组合。修改 Excel 后先提取并审核分类：

```powershell
python tools/import_excel.py sources.xlsx --output .cache/new-sources.json
```

每个订阅独立合并，仅删除完全相同的规范化规则；不进行父子域名覆盖裁剪，不把 URL 路径扩大成整站拦截。
下载、格式、规则数量突变或引擎校验失败时，优先使用 72 小时内的已校验缓存；缓存也不可用则整次构建停止，保留上一版订阅。
核心网站样例检查和语法校验不能保证 App 无误拦截。加速线路是第三方服务，异常时请使用原始链接。

[自动构建记录](https://github.com/Ethereal-09/adguardhome-compiled-filters/actions/workflows/update.yml)
