# 分类订阅与组合说明

每日分类构建和 GitHub 自动发布已启用。sources.json 记录来源与依据，groups.json 是候选目录；实际选源由 profiles.json 决定，publish_filters.py 在临时目录构建并逐分类验证后更新 dist。首页显示最近成功发布与本次检查状态，真实应用的误拦截仍需使用后验证。

个人规则默认用于综合版、国内优化版和全量版；其他黑名单由 `includeCustom` 控制，独立白名单不能开启此选项。个人放行使用 important，修改后应检查实际效果。

发布按分类和格式隔离：下载或 DNS 校验失败保留该分类旧版；mihomo 转换失败只保留相应 mihomo 旧版，不阻止已通过校验的 DNS 文件更新。两种格式输入版本不同时首页明确标注。完整状态、每分类新增/删除数量及来源计数变化见 [publication.json](../dist/publication.json)。失败或部分成功的 Actions 会标为失败，但正常产物已提交。

默认拒绝数量下降超过 30%、数量翻倍且净增至少 1000 条，以及基线至少 20 条的放行规则下降超过 30%。阈值在 `changeChecks` 中配置；核实上游调整后可手动运行 `publish_filters.py --allow-reviewed-changes`，此参数不会绕过格式或引擎验证。

mihomo 配置版本 2 固定八个 provider 和拦截表达式，空规则集不匹配任何域名，避免首次出现例外或正则时旧客户端遗漏更新。旧用户需重新合并一次片段。

实际使用回归清单：国内常用应用登录与验证码、支付、视频播放、应用及系统更新。测试时记录客户端、分类、命中域名和结果；失败先核对过滤日志，再调整个人放行，不预先扩大白名单。引擎测试通过不代表这些场景已通过实机验证。

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

分组标识为 `region-china-optimized`，分类维度为 `region`。当前独立合并以下三个来源，地域依据和原始文件记录在 `regionalFocus`：

| 来源 | 上游依据 | DNS 原始文件 |
| --- | --- | --- |
| [AdRules](https://github.com/Cats-Team/AdRules) | 明确面向中国使用环境 | [dns.txt](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) |
| [anti-AD](https://github.com/privacy-protection-tools/anti-AD) | 明确面向中文区，提供 AdGuard Home 格式 | [anti-ad-easylist.txt](https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt) |
| [217heidai Lite](https://github.com/217heidai/adblockfilters) | README 声明 Lite 版本针对国内域名 | [adblockdnslite.txt](https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt) |

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
| 全量版 | 52 个可兼容 DNS 拦截来源；同系列最高强度、同源格式择一，原生例外及个人规则保留，独立白名单分开 | 已接入构建，full.txt |
| 均衡版 | HaGeZi Normal，1Hosts Lite 另作替代文件 | 已接入构建 |
| 扩展版 | HaGeZi Pro；不叠加所有系列版本 | 已接入构建 |
| 激进版 | HaGeZi Pro++，1Hosts Xtra 另作替代文件 | 已接入构建 |
| 最强版 | HaGeZi Ultimate，不默认加入专项服务限制 | 已接入构建 |
| 广告分类 | 广告用途来源；综合源不视为纯广告 | 已接入构建 |
| 跟踪分类 | 跟踪、遥测、Windows 等相应用途组件 | 已接入构建 |
| 安全分类 | 诈骗、钓鱼、恶意网站、勒索软件等来源 | 已接入构建 |
| 设备分类 | 电视、游戏机、小米、三星等 | 已接入构建，按需订阅 |
| 中国国内优化黑名单 | AdRules DNS、anti-AD、217heidai 国内 Lite，保留各自原生放行例外 | 已接入构建 |
| 设备原生遥测 | NextDNS 已迁移的 8 个设备原始列表；保留其历史更新时间事实 | 已接入构建，native-tracking.txt |
| 顶级域名限制 | HaGeZi 高滥用 TLD 列表，作为服务限制组件 | 已接入构建，tld-restrictions.txt |
| 钓鱼网站 | Blocklist Project 的 phishing 原始分类 | 已接入构建，phishing.txt |
| 兼容性放行 | 三个独立白名单分开输出，按用途选择 | 已接入构建，可选组件 |

选源清单由 profiles.json 明确记录。同系列版本与格式组重复、地域或强度依据不匹配会在下载前报错。优化只在相同行为与优先级内删除被覆盖的简单条目，正则与通配符保持原样；来源或优化后分类比上一版减少超过 30% 时保留旧版。仍需检查真实应用误杀；下载、构建和程序测试不证明低误杀或应用去广告效果。

全量版的调查范围为 sources.json 中登记的全部来源，并非 GitHub 上全部项目。已排除独立白名单、停更/数量异常来源、被更高档位或另一格式替代的版本，以及含不支持的浏览器放行例外的来源。逐项依据见 [full_selection.json](full_selection.json)。每日构建按 profiles.json 的明确选源重下载，来源失败时保留全量版旧文件；新来源需核验后加入配置。

## 来源重整与兼容性边界

2026-10-01 根据用户提供的链接、已核实原仓库 DNS 发布文件和此前维护来源，共完整检查 93 个候选文件。65 个通过当前解析器及 AdGuard 官方 DNS 引擎检查；最终选用 60 个来源生成 33 个独立订阅。代理地址与原地址不重复入源，Dan Pollock 的两种 hosts 版本择一。

`reviewed_sources.json` 保存人工核实的来源与用途，`refresh_source_registry.py` 使用与每日构建相同的下载完整性检查、例外处理与官方引擎重新核验，避免调查目录与实际构建采用不同的兼容标准。

乘风、ADgk、EasyList 等浏览器列表含无法在 DNS 中保留的网络放行条件，整份排除；AdGuard DNS 源的 badfilter 暂未实现安全组合，也保留排除记录。HaGeZi TIF 超过当前单来源 32 MiB 上限。完整失败原因见 [来源登记](README.md)，这些排除不表示上游规则本身无效。

GOODBYEADS DNS 和 blackmatrix7 Advertising 等来源纳入全量版；中文 README 本身不作为国内优化依据。hululu1068 的 mylist 虽可解析，但属于内部混合修正组件，没有作为通用黑名单或纯白名单自动叠加。
