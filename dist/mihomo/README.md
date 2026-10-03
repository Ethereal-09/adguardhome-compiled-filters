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
| 国内精简（推荐） | 5,569 | 16 | [combined.yaml](combined.yaml) | [Boki](combined-boki.yaml) | [GHFast](combined-ghfast.yaml) |
| 国内增强 | 211,115 | 123 | [china.yaml](china.yaml) | [Boki](china-boki.yaml) | [GHFast](china-ghfast.yaml) |
| 中文源全量（按需） | 341,013 | 303 | [full.yaml](full.yaml) | [Boki](full-boki.yaml) | [GHFast](full-ghfast.yaml) |
