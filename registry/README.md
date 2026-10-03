# AdGuard Home 来源登记

最近核验：2026-10-03T09:13:39+00:00（UTC）。共 8 个原始文件，8 个通过完整下载、保守解析和 AdGuard 引擎校验。

上游署名、用途、强度、地域和证据保存在 [reviewed_sources.json](reviewed_sources.json)；当前兼容结果见 [sources.json](sources.json)，实际组合见 [profiles.json](../profiles.json)。

对浏览器条件、URL 路径和脚本语法不做域名扩大转换。无法保留网络放行例外或 badfilter 的来源整份排除。DNS 黑名单保留其原生例外；独立白名单按用途另行订阅。

中文或中国地区依据保存在 selectionEvidence / regionalFocus；语言不等于域名地区，也不保证低误杀。当前订阅以 dist/ 和 manifest.json 为准。

| 原始来源 | 分类 | DNS 拦截 | DNS 例外 | 结果 |
| --- | --- | ---: | ---: | --- |
| [AdRules DNS List](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | ads, tracking, security | 197268 | 0 | 可选；fresh |
| [Anti-AD](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) | ads, tracking | 93798 | 110 | 可选；fresh |
| [ios_rule_script / rule/AdGuard/Advertising/Advertising.txt](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/AdGuard/Advertising/Advertising.txt) | ads, tracking | 280859 | 0 | 可选；fresh |
| [GOODBYEADS / data/rules/dns.txt](https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/dns.txt) | ads, tracking | 114252 | 0 | 可选；fresh |
| [adblockfilters / rules/adblockdns.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt) | ads, tracking | 219136 | 197 | 可选；fresh |
| [adblockfilters / rules/adblockdnslite.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt) | ads, tracking | 5372 | 16 | 可选；fresh |
| [秋风纯广告](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt) | ads | 652 | 0 | 可选；fresh |
| [秋风广告与隐私](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt) | ads, tracking | 866 | 0 | 可选；fresh |

## 重新核验

```powershell
.\.venv\Scripts\python.exe refresh_source_registry.py --validator .cache\dns-rule-validator.exe
```

每日构建直接读取已选来源，每次重新下载、检查例外、异常数量下降和引擎兼容性；不会自动启用新发现的订阅源。
