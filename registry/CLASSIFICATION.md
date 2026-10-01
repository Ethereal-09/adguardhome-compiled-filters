# 分类订阅与组合说明

每日分类构建和 GitHub 自动发布已启用。sources.json 记录来源与依据，groups.json 是候选目录；实际选源由 profiles.json 决定，build_filters.py 生成 dist 下的订阅。最新构建时间和状态见 [首页](../README.md)，真实应用的误杀仍需使用后验证。

## 分类维度

| 维度 | 字段 | 使用方式 |
| --- | --- | --- |
| 仓库与来源 | repository、url、path、ref | 保留原仓库、实际路径与版本分支 |
| 黑白性质 | role、kind | 区分拦截列表、混合过滤源和独立白名单 |
| 拦截强度 | strength.value、basis、evidenceUrl | 仅根据上游说明分级；未知强度单独保存 |
| 过滤用途 | categories、categoryBasis、categoryEvidence | 来源的覆盖范围；名称推断与上游说明分开 |
| 地域优化 | regionalFocus.value、basis、evidenceUrl、scope | 根据上游明确说明选择地区 DNS 来源；与强度独立 |
| 档位关系 | variantFamily | 同系列版本择一，避免高档位覆盖低档位 |
| 格式关系 | representationGroup、rawCounts | 同来源不同格式择一；不声称匹配语义相同 |
| 格式兼容 | compatibility、unsupported | 当前解析器是 DNS 子集，不是浏览器完整规则引擎 |
| 更新情况 | checkedUtc、lifecycle | 下载检查时间与停更标记；下载成功不代表活跃维护 |
| 历史启用 | enabledInCurrentConfig | 记录旧 config.json 的启用状态；当前选源以 profiles.json 为准 |

## 强度与用途分开

HaGeZi Normal、Pro、Pro++、Ultimate 可对应均衡、扩展、激进、最强档位。Pro Mini 与 Pro 属于同一强度系列，只是缩小体积。[上游说明](https://github.com/hagezi/dns-blocklists)

1Hosts Lite 与 Xtra 分别有上游的均衡、激进说明。[上游说明](https://github.com/badmojr/1Hosts)

其他来源没有核验到明确强度分级时保留 unknown，不按条目数量或名称自动归类。

短链接服务、动态 DNS 服务、社交平台整站拦截应作为独立组件，不能仅因包含大量域名就放进“加强广告”档位。Facebook 专项源会限制 Facebook 相关域名，其用途与纯广告过滤不同。[来源说明](https://github.com/anudeepND/blacklist)

## 中国国内优化黑名单

分组标识为 `region-china-optimized`，分类维度为 `region`。首版采用 [Cats-Team / AdRules](https://github.com/Cats-Team/AdRules) 的 [DNS 原始订阅](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt)。2026-10-01 核实其 README 明确说明面向中国地区，覆盖广告、跟踪、恶意软件、HTTPDNS、PCDN；上游同时单独列出了 DNS 规则，地域依据记录在 `regionalFocus`。

“国内优化”描述中国使用环境，不按 `.cn` 后缀筛选，也不按解析 IP 的国家归类；国内应用使用的 `.com` 等域名仍保留。仅有中文名称、中文 README 或中国账号的仓库不自动加入。浏览器中文过滤列表不能据此成为完整 DNS 订阅。

本分类仍保留来源原有强度信息；AdRules 未核验到明确强度档位，继续记为 `unknown`。地域标签不保证低误杀、低强度或具体应用去广告效果。选择来源时携带它自身的 DNS 放行例外，独立白名单仍为可选组件。

独立订阅已接入 profiles.json 的 china 分类，输出 [dist/china.txt](../dist/china.txt)。此目录统计沿用调查快照，最新构建见 [dist/manifest.json](../dist/manifest.json)。后续加入来源需同时核实原仓库、实际 DNS 文件及明确的中国地区用途说明；失败、数量异常或停更来源不进入分组。

## 黑名单与白名单的组合边界

选择一个混合过滤源时，同时带上它的 DNS 放行例外，保留原始匹配范围和修饰符。不要把弱档位的例外默认套到强档位，也不要统一添加 `$important`；否则会改变上游优先级。

独立白名单作为可选组件：例如推广跳转放行、短链接放行。需要由使用者明确选择用途，不自动合并进所有订阅。存在于文件中的 `@@` 不意味着来源整体属于白名单。

生成器的排除样例、占位文件、Python exceptions.py 与实际 DNS 白名单不同，不纳入白名单订阅。

调查时生成的每来源 whitelist.txt 仅包含当时解析器支持的放行例外，不作为每日构建的输入。每日构建重新下载上游，保留 DNS 通配符、正则和 important；遇到其他不支持的放行例外会拒绝该来源，避免丢失例外而扩大拦截。原始订阅可能具有更广的语法能力。

## 分类订阅候选

| 分类 | 选源方式 | 当前状态 |
| --- | --- | --- |
| 全量版 | 34 个可兼容 DNS 拦截来源；同系列最高强度、同源格式择一，原生例外及个人规则保留，独立白名单分开 | 已接入构建，full.txt |
| 均衡版 | HaGeZi Normal，1Hosts Lite 另作替代文件 | 已接入构建 |
| 扩展版 | HaGeZi Pro；不叠加所有系列版本 | 已接入构建 |
| 激进版 | HaGeZi Pro++，1Hosts Xtra 另作替代文件 | 已接入构建 |
| 最强版 | HaGeZi Ultimate，不默认加入专项服务限制 | 已接入构建 |
| 广告分类 | 广告用途来源；综合源不视为纯广告 | 已接入构建 |
| 跟踪分类 | 跟踪、遥测、Windows 等相应用途组件 | 已接入构建 |
| 安全分类 | 诈骗、钓鱼、恶意网站、勒索软件等来源 | 已接入构建 |
| 设备分类 | 电视、游戏机、小米、三星等 | 已接入构建，按需订阅 |
| 中国国内优化黑名单 | AdRules DNS，保留其原生放行例外 | 已接入构建 |
| 兼容性放行 | 三个独立白名单分开输出，按用途选择 | 已接入构建，可选组件 |

选源清单由 profiles.json 明确记录。同系列版本与格式组重复、地域或强度依据不匹配会在下载前报错。优化只在相同行为与优先级内删除被覆盖的简单条目，正则与通配符保持原样；来源或优化后分类比上一版减少超过 30% 时保留旧版。仍需检查真实应用误杀；下载、构建和程序测试不证明低误杀或应用去广告效果。

全量版的调查范围为 sources.json 中登记的全部来源，并非 GitHub 上全部项目。已排除独立白名单、停更/数量异常来源、被更高档位或另一格式替代的版本，以及含不支持的浏览器放行例外的来源。逐项依据见 [full_selection.json](full_selection.json)。每日构建按 profiles.json 的明确选源重下载，来源失败时保留全量版旧文件；新来源需核验后加入配置。
