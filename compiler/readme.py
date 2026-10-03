"""Generate a compact subscription homepage from the published build metadata."""
from datetime import datetime, timedelta, timezone


SOURCE_TYPES = {
    "bili-pcdn": "PCDN", "anti-pcdn": "PCDN", "awa-full": "广告、隐私、不受欢迎",
    "noapp": "去 App 下载提示", "adult-ads": "悬浮广告", "video": "视频广告",
    "browser-ads": "网页广告", "oisd-small": "oisd small",
}


def local_time(value: str) -> str:
    return datetime.fromisoformat(value).astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")


def subscription_links(repository: str, path: str, mihomo: bool = False) -> str:
    root = f"https://raw.githubusercontent.com/{repository}/main/dist/"
    raw = root + path
    boki = root + path.removesuffix(".yaml") + "-boki.yaml" if mihomo else raw
    ghfast = root + path.removesuffix(".yaml") + "-ghfast.yaml" if mihomo else raw
    return f"[订阅]({raw}) | [Boki](https://github.boki.moe/{boki}) | [GHFast](https://ghfast.top/{ghfast})"


def readme(catalog: dict, manifest: dict | None, attempt: dict) -> str:
    repository = catalog["repository"]
    workflow = f"https://github.com/{repository}/actions/workflows/update.yml"
    profiles = {p["id"]: p for p in (manifest or {}).get("profiles", [])}
    sources = {s["id"]: s for s in (manifest or {}).get("sources", [])}
    browsers = {p["id"]: p for p in (manifest or {}).get("browser_profiles", [])}
    published = local_time(manifest["built_at"]) if manifest else "尚未发布"
    state = "构建成功" if attempt["status"] == "success" else "构建失败，保留上一版订阅"
    if attempt["status"] == "success" and attempt.get("offline"):
        state = "离线缓存构建"
    elif attempt["status"] == "success" and attempt.get("degraded_sources"):
        state = "已构建，部分源使用缓存"
    lines = [
        '<div align="center">', "", "<h1>AdGuard Home 合并规则</h1>", "",
        "一个 DNS 合并订阅，每日自动更新。", "", "</div>", "",
        f"更新：**{published}**（北京时间） · [构建状态：{state}]({workflow})", "",
        "## AdGuard Home", "",
        "添加下方合并订阅到「DNS 黑名单」，文件内已保留上游放行例外。",
        "", "| 订阅 | 规则数 | 原始链接 | 加速 1 | 加速 2 |",
        "|---|---:|---|---|---|",
    ]
    for profile in catalog["profiles"]:
        pid = profile["id"]
        name = profile["name"]
        output = profiles.get(pid)
        count = f"{output['rules']:,}" if output else "未发布"
        dns = subscription_links(repository, pid + ".txt") if output else "— | — | —"
        lines.append(f"| {name} | {count} | {dns} |")
    lines += [
        "", "包含秋风完整、oisd small 与两份 PCDN 规则，可能影响视频、更新或推送。", "",
        "原分类订阅已整合，请将旧分类地址替换为上方 `full.txt`。", "",
        "<details>", "<summary>mihomo 订阅</summary>", "",
        "将配置片段中的 `rule-providers` 和 `rules` 合并到现有配置，放在兜底规则前。",
        "例外继续后续分流，不强制 DIRECT。", "",
        "| 订阅 | 原始配置 | 加速 1 | 加速 2 |", "|---|---|---|---|",
    ]
    for profile in catalog["profiles"]:
        pid = profile["id"]
        name = profile["name"]
        link = subscription_links(repository, "mihomo/" + pid + ".yaml", True) if pid in profiles else "— | — | —"
        lines.append(f"| {name} | {link} |")
    lines += ["", "</details>", "",
        "<details>", "<summary>使用说明与合并方式</summary>", "",
        "- AdGuard Home 只需添加一个 `full.txt` 合并订阅，PCDN 已包含在内。",
        "- AdGuard Home 文件保留 `@@` 例外，无需另加同一份白名单。",
        "- 规则数包含拦截与例外，按去重后的有效行统计，不等于覆盖的域名总数。",
        "- 仅去除标准化后完全相同的规则；不裁剪父子域名覆盖关系，不把 URL 路径扩大成整站拦截。",
        "- 下载或校验异常时使用 72 小时内的已校验缓存；缓存不可用则停止发布，保留上一版。",
        "- 语法和样例检查不能保证没有误拦截；加速线路异常时使用原始链接。", "", "</details>", "",
        "<details>", "<summary>浏览器专用规则</summary>", "",
        "仅供浏览器拦截器使用，**不能导入 AdGuard Home**。网页元素、路径、脚本和例外规则均保留。", "",
        "| 订阅 | 规则数 | 原始链接 | 加速 1 | 加速 2 |", "|---|---:|---|---|---|",
    ]
    for profile in catalog["browser_profiles"]:
        output = browsers.get(profile["id"])
        count = f"{output['rules']:,}" if output else "未发布"
        link = subscription_links(repository, "browser/" + profile["id"] + ".txt") if output else "— | — | —"
        lines.append(f"| {profile['name']} | {count} | {link} |")
    lines += ["", "</details>", "", "<details>", "<summary>上游来源与作者</summary>", "",
              f"共 **{len(catalog['sources'])} 个订阅地址**。本项目仅做合并，规则由下列上游作者维护。", "",
              "| 作者 / 项目 | 原始规则 | 分类 | DNS 可用条目 |", "|---|---|---|---:|"]
    for source in catalog["sources"]:
        count = sources.get(source["id"], {}).get("dns_usable")
        usable = "浏览器专用" if source["mode"] == "browser" else f"{count:,}" if count is not None else "—"
        kind = SOURCE_TYPES.get(source["id"], source["category"].replace("|", "/"))
        lines.append(f"| [{source['author']}]({source['repository']}) | [{source['name']}]({source['url']}) | {kind} | {usable} |")
    lines += ["", "[上游许可证](licenses/) · [完整统计与跳过原因](dist/report.json)",
              "未声明许可的来源按原样注明，不替作者指定许可证。", "", "</details>", "",
              "<details>", "<summary>运行与维护</summary>", "",
              "自动构建使用 [sources.json](sources.json) 管理来源和组合，无需 Excel 文件。", "",
              "本地使用 Python 3.12、Go 1.27.1；Python 合并程序无需 pip 依赖。", "",
              "```powershell", "python tools/install_engines.py", "python compile_rules.py", "```", "",
              "已登录 GitHub CLI 时，可使用 `python compile_rules.py --github-api` 下载相同上游文件。",
              "修改来源后，提交 `sources.json` 即可触发自动构建。每天北京时间 **04:23** 自动更新。",
              "", "</details>", ""]
    if attempt.get("errors"):
        lines += ["<details>", f"<summary>最近构建问题（{local_time(attempt['attempted_at'])}）</summary>", ""]
        lines += [f"- {sid}: {str(error).replace(chr(10), ' ')[:300]}" for sid, error in attempt["errors"].items()]
        lines += ["", "</details>", ""]
    return "\n".join(lines)
