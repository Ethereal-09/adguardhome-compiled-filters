"""Generate a compact subscription homepage from the published build metadata."""
from datetime import datetime, timedelta, timezone


SUMMARY = {
    "ads": ("纯广告（推荐）", "仅广告"),
    "china": ("国内广告＋隐私", "广告、隐私"),
    "ads-unwelcome": ("广告＋不受欢迎", "广告、功能拦截"),
    "awa-full": ("秋风完整", "广告、隐私、功能拦截"),
    "pcdn": ("PCDN（按需）", "两份 PCDN 源合并"),
    "oisd": ("oisd small", "原版 small 列表"),
    "combined": ("综合广告＋隐私", "秋风广告＋隐私、oisd"),
    "full": ("DNS 全量（按需）", "秋风完整、oisd、PCDN"),
}
SOURCE_TYPES = {
    "bili-pcdn": "PCDN", "anti-pcdn": "PCDN", "awa-full": "广告、隐私、不受欢迎",
    "awa-ads": "仅广告", "awa-unwelcome": "广告、不受欢迎", "awa-privacy": "广告、隐私",
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
    return f"[原始]({raw}) / [Boki](https://github.boki.moe/{boki}) / [GHFast](https://ghfast.top/{ghfast})"


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
        "仅合并、去重与格式转换。规则由上游作者维护。", "", "</div>", "",
        f"**订阅更新：{published}** · 每天 **04:23** 自动构建（北京时间）。",
        f"[自动构建：{state}]({workflow}) · [构建报告](dist/report.json)", "",
        "## 订阅", "",
        "优先选择 **纯广告**。AdGuard Home 添加到「DNS 黑名单」；mihomo 使用对应配置片段。",
        "", "| 订阅 | 条目数 | 主要内容 | AdGuard Home | mihomo |",
        "|---|---:|---|---|---|",
    ]
    for profile in catalog["profiles"]:
        pid = profile["id"]
        name, purpose = SUMMARY.get(pid, (profile["name"], profile.get("description", "")))
        output = profiles.get(pid)
        count = f"{output['rules']:,}" if output else "未发布"
        dns = subscription_links(repository, pid + ".txt") if output else "—"
        mihomo = subscription_links(repository, "mihomo/" + pid + ".yaml", True) if output else "—"
        lines.append(f"| {name} | {count} | {purpose} | {dns} | {mihomo} |")
    lines += [
        "", "数量为去重后的规则行，包含例外；通配符规则不等于一个域名。",
        "**PCDN、含「不受欢迎」及全量方案可能影响视频、更新或推送，按需使用。**", "",
        "<details>", "<summary>使用说明与合并方式</summary>", "",
        "- 每次选择一个主方案；PCDN 可单独加订。秋风的四个版本互不混用。",
        "- AdGuard Home 文件保留 `@@` 例外，无需另加同一份白名单。",
        "- mihomo 将 `rule-providers` 和 `rules` 合并到现有配置，拦截规则放在兜底规则前。例外继续后续分流，不强制 DIRECT。",
        "- 各订阅独立去重；不裁剪父子域名覆盖关系，不把 URL 路径扩大成整站拦截。",
        "- 下载或校验异常时使用 72 小时内的已校验缓存；缓存不可用则停止发布，保留上一版。",
        "- 语法和样例检查不能保证没有误拦截；加速线路异常时使用原始链接。", "", "</details>", "",
        "<details>", "<summary>浏览器专用规则</summary>", "",
        "仅供浏览器拦截器使用，**不能导入 AdGuard Home**。网页元素、路径、脚本和例外规则均保留。", "",
        "| 分类 | 条目数 | 订阅 |", "|---|---:|---|",
    ]
    for profile in catalog["browser_profiles"]:
        output = browsers.get(profile["id"])
        count = f"{output['rules']:,}" if output else "未发布"
        link = subscription_links(repository, "browser/" + profile["id"] + ".txt") if output else "—"
        lines.append(f"| {profile['name']} | {count} | {link} |")
    lines += ["", "</details>", "", "## 上游来源", "",
              f"共 **{len(catalog['sources'])} 个订阅地址**。本项目仅做合并，作者与许可说明保留在输出文件中。", "",
              "<details>", "<summary>查看全部来源、作者与分类</summary>", "",
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
              "修改来源或分类后，提交 `sources.json` 即可触发自动构建。", "", "</details>", ""]
    if attempt.get("errors"):
        lines += ["<details>", f"<summary>最近构建问题（{local_time(attempt['attempted_at'])}）</summary>", ""]
        lines += [f"- {sid}: {str(error).replace(chr(10), ' ')[:300]}" for sid, error in attempt["errors"].items()]
        lines += ["", "</details>", ""]
    return "\n".join(lines)
