# mihomo 分类规则

与 AdGuard Home 版使用同一批已验证分类；域名使用 MRS，通配符和正则使用 classical/text 配套规则集。
精确域名保持精确匹配；父域名及子域名范围、原生例外和 important 优先级保留。
规则由原作者维护，署名和许可见 [上游](../../upstream/README.md)；来源详情见 [统计](manifest.json)。

## 使用

1. 从下表选择一个配置片段，合并其中的 `rule-providers` 到现有配置。
2. 把片段的 `rules` 按原顺序放在现有分流规则之前。不要覆盖原来的节点、策略组或后续规则。
3. Boki / GHFast 片段中的所有规则集下载地址也使用对应加速源。每天更新一次（86400 秒）。

旧版用户需重新合并一次配置版本 2 的片段。新版固定声明八个 provider（四种动作/优先级 × 域名/正则），
即使暂无对应规则也保留不匹配任何域名的空规则集。以后出现新的例外、important 或正则时，无需再次修改配置。
这是配置片段，不是节点订阅；`interval` 只刷新规则文件，不刷新你合并过的配置。

放行例外只跳过本分类的 REJECT，继续执行后面的分流规则。不要单独使用拦截 MRS，否则会遗漏配套例外或正则。
独立白名单片段仅声明 provider，不自动强制 DIRECT；可用 NOT 条件排除拦截，或按你的用途指定策略。
多分类同时启用时，例外只对各自分类有效；需统一跨分类例外时，先合并来源生成同一分类。
这是域名流量拦截，不是 DNS 响应改写；仅 IP 连接且没有域名元数据时无法按域名过滤。
使用 mihomo v1.19.32 或更新版本。生成器用官方内核转换 MRS 并验证配置；每日发布按分类隔离失败，保留该分类旧版。
格式依据：[规则集合](https://wiki.metacubex.one/config/rule-providers/) / [路由规则](https://wiki.metacubex.one/config/rules/)。

## 配置片段

| 分类 | 拦截条目 | 例外条目 | 原始 | 加速1 | 加速2 |
| --- | ---: | ---: | --- | --- | --- |
| 综合 DNS 过滤（基础＋国内优化） | 307,309 | 123 | [combined.yaml](combined.yaml) | [Boki](combined-boki.yaml) | [GHFast](combined-ghfast.yaml) |
| 全量 DNS 黑名单（最高档＋全部可用专项） | 2,006,532 | 312 | [full.yaml](full.yaml) | [Boki](full-boki.yaml) | [GHFast](full-ghfast.yaml) |
| 均衡 DNS 过滤 | 199,122 | 0 | [balanced.yaml](balanced.yaml) | [Boki](balanced-boki.yaml) | [GHFast](balanced-ghfast.yaml) |
| 扩展 DNS 过滤 | 227,572 | 0 | [extended.yaml](extended.yaml) | [Boki](extended-boki.yaml) | [GHFast](extended-ghfast.yaml) |
| 激进 DNS 过滤 | 248,237 | 0 | [aggressive.yaml](aggressive.yaml) | [Boki](aggressive-boki.yaml) | [GHFast](aggressive-ghfast.yaml) |
| 最强 DNS 过滤 | 284,025 | 0 | [maximum.yaml](maximum.yaml) | [Boki](maximum-boki.yaml) | [GHFast](maximum-ghfast.yaml) |
| 1Hosts 均衡（替代基础） | 102,241 | 0 | [balanced-1hosts.yaml](balanced-1hosts.yaml) | [Boki](balanced-1hosts-boki.yaml) | [GHFast](balanced-1hosts-ghfast.yaml) |
| 1Hosts 激进（替代基础） | 786,132 | 0 | [aggressive-1hosts.yaml](aggressive-1hosts.yaml) | [Boki](aggressive-1hosts-boki.yaml) | [GHFast](aggressive-1hosts-ghfast.yaml) |
| 中国国内优化 DNS 黑名单 | 210,961 | 123 | [china.yaml](china.yaml) | [Boki](china-boki.yaml) | [GHFast](china-ghfast.yaml) |
| 广告分类 | 143,763 | 0 | [ads.yaml](ads.yaml) | [Boki](ads-boki.yaml) | [GHFast](ads-ghfast.yaml) |
| 跟踪与遥测分类 | 133,812 | 0 | [tracking.yaml](tracking.yaml) | [Boki](tracking-boki.yaml) | [GHFast](tracking-ghfast.yaml) |
| 安全分类（威胁与诈骗等） | 654,793 | 0 | [security.yaml](security.yaml) | [Boki](security-boki.yaml) | [GHFast](security-ghfast.yaml) |
| 被入侵网站补充列表（单一来源） | 9 | 0 | [malware.yaml](malware.yaml) | [Boki](malware-boki.yaml) | [GHFast](malware-ghfast.yaml) |
| 诈骗分类 | 157,602 | 0 | [scam.yaml](scam.yaml) | [Boki](scam-boki.yaml) | [GHFast](scam-ghfast.yaml) |
| 勒索软件分类 | 1,903 | 0 | [ransomware.yaml](ransomware.yaml) | [Boki](ransomware-boki.yaml) | [GHFast](ransomware-ghfast.yaml) |
| 挖矿分类 | 1,524 | 0 | [mining.yaml](mining.yaml) | [Boki](mining-boki.yaml) | [GHFast](mining-ghfast.yaml) |
| 电视分类 | 151 | 9 | [smart-tv.yaml](smart-tv.yaml) | [Boki](smart-tv-boki.yaml) | [GHFast](smart-tv-ghfast.yaml) |
| 游戏机分类 | 14 | 0 | [game-console.yaml](game-console.yaml) | [Boki](game-console-boki.yaml) | [GHFast](game-console-ghfast.yaml) |
| Windows 遥测组件 | 355 | 0 | [windows.yaml](windows.yaml) | [Boki](windows-boki.yaml) | [GHFast](windows-ghfast.yaml) |
| 小米组件 | 278 | 0 | [xiaomi.yaml](xiaomi.yaml) | [Boki](xiaomi-boki.yaml) | [GHFast](xiaomi-ghfast.yaml) |
| 三星组件 | 101 | 0 | [samsung.yaml](samsung.yaml) | [Boki](samsung-boki.yaml) | [GHFast](samsung-ghfast.yaml) |
| Spotify 域名拦截组件 | 3,780 | 0 | [spotify.yaml](spotify.yaml) | [Boki](spotify-boki.yaml) | [GHFast](spotify-ghfast.yaml) |
| YouTube 域名拦截组件 | 97,591 | 0 | [youtube.yaml](youtube.yaml) | [Boki](youtube-boki.yaml) | [GHFast](youtube-ghfast.yaml) |
| 社交平台限制组件 | 3,995 | 0 | [social.yaml](social.yaml) | [Boki](social-boki.yaml) | [GHFast](social-ghfast.yaml) |
| 短链接服务限制组件 | 9,935 | 0 | [shorteners.yaml](shorteners.yaml) | [Boki](shorteners-boki.yaml) | [GHFast](shorteners-ghfast.yaml) |
| 动态 DNS 服务限制组件 | 1,536 | 0 | [dyndns.yaml](dyndns.yaml) | [Boki](dyndns-boki.yaml) | [GHFast](dyndns-ghfast.yaml) |
| 托管服务限制组件 | 1,235 | 0 | [hosting.yaml](hosting.yaml) | [Boki](hosting-boki.yaml) | [GHFast](hosting-ghfast.yaml) |
| 推广跳转放行 | 0 | 930 | [allow-referral.yaml](allow-referral.yaml) | [Boki](allow-referral-boki.yaml) | [GHFast](allow-referral-ghfast.yaml) |
| 推广跳转放行（Native） | 0 | 1,613 | [allow-referral-native.yaml](allow-referral-native.yaml) | [Boki](allow-referral-native-boki.yaml) | [GHFast](allow-referral-native-ghfast.yaml) |
| 短链接放行 | 0 | 9,928 | [allow-shorteners.yaml](allow-shorteners.yaml) | [Boki](allow-shorteners-boki.yaml) | [GHFast](allow-shorteners-ghfast.yaml) |
| 设备原生遥测 | 98 | 0 | [native-tracking.yaml](native-tracking.yaml) | [Boki](native-tracking-boki.yaml) | [GHFast](native-tracking-ghfast.yaml) |
| 高滥用顶级域名限制 | 281 | 0 | [tld-restrictions.yaml](tld-restrictions.yaml) | [Boki](tld-restrictions-boki.yaml) | [GHFast](tld-restrictions-ghfast.yaml) |
| 钓鱼网站分类 | 118,066 | 0 | [phishing.yaml](phishing.yaml) | [Boki](phishing-boki.yaml) | [GHFast](phishing-ghfast.yaml) |
