"""Compile one verified generation from the workbook catalog, then publish it."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from .engines import export_mihomo, match_dns, validate_dns
from .network import Cache, atomic, count_guard, json_text, retry_download, timestamp
from .rules import active_lines, merge, parse, stats

SERVICE_HOSTS = ("www.baidu.com", "www.bilibili.com", "api.bilibili.com", "www.qq.com", "wx.qq.com",
                 "weixin.qq.com", "www.taobao.com", "www.jd.com", "www.alipay.com", "www.zhihu.com",
                 "www.douyin.com", "music.163.com", "www.microsoft.com", "www.apple.com")
FUNCTION_HOSTS = ("httpdns.alicdn.com", "httpdns.baidu.com", "httpdns.bilivideo.com", "dns.weixin.qq.com",
                  "mtalk.google.com", "mcdn.bilivideo.com", "mcdn.bilivideo.cn", "p2pchunk-ws.douyucdn.cn")


def load_catalog(path: Path) -> dict:
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema") != 2:
        raise ValueError("Expected new workbook catalog schema 2")
    ids = [s["id"] for s in catalog["sources"]]
    urls = [s["url"] for s in catalog["sources"]]
    if len(set(ids)) != len(ids) or len(set(urls)) != len(urls):
        raise ValueError("Duplicate source ID or URL")
    by_id = {s["id"]: s for s in catalog["sources"]}
    for key in ("profiles", "browser_profiles"):
        names = [p["id"] for p in catalog[key]]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate subscription ID")
        for p in catalog[key]:
            if not re.fullmatch(r"[a-z][a-z0-9-]*", p["id"]):
                raise ValueError("Unsafe subscription ID")
            if not p["sources"]:
                raise ValueError("Empty subscription selection")
            for sid in p["sources"]:
                if sid not in by_id:
                    raise ValueError("Unknown source " + sid)
                if key == "profiles" and by_id[sid]["mode"] == "browser":
                    raise ValueError("Browser source cannot enter a DNS subscription")
            # AWA variants are mutually exclusive, not independent source families.
            if sum(sid.startswith("awa-") for sid in p["sources"]) > 1:
                raise ValueError("Multiple AWA variants in one subscription")
    workbook = path.parent / "sources.xlsx"
    if workbook.exists():
        from tools.import_excel import extract
        extracted = extract(workbook)
        if extracted["sha256"] != catalog["sha256"]:
            raise ValueError("Workbook changed: import and review the new source catalog first")
        original = {(s["sheet"], s["row"], s["url"]) for s in extracted["sources"]}
        selected = {(s["sheet"], s["row"], s["url"]) for s in catalog["sources"]}
        if original != selected:
            raise ValueError("Source catalog does not exactly match workbook URLs")
    return catalog


def source_result(source: dict, cache: Cache, offline: bool, github_api: bool) -> dict:
    previous = {"active": source["initial_active"], "allow": source.get("initial_allow", 0)} if source.get("initial_active") else None
    try:
        _, previous = cache.load(source, enforce_age=False)
    except (OSError, ValueError, KeyError):
        pass

    def inspect(body: str) -> tuple:
        if any(line.lstrip().startswith("!#") for line in body.splitlines()):
            raise ValueError("Upstream added conditional/include directives; source needs review before merging")
        parsed = parse(body, source["mode"])
        if source["mode"] != "browser":
            parsed.require_dns_safe()
            validate_dns(parsed.rules)
        if not parsed.active:
            raise ValueError("Empty source list")
        allow_count = sum(line.startswith("@@") for line in active_lines(body))
        return parsed, allow_count

    warning = None
    if offline:
        body, meta = cache.load(source)
        parsed, _ = inspect(body)
        state = "cache-offline"
    else:
        try:
            body, transport = retry_download(source["url"], github_api)
            parsed, allow_count = inspect(body)
            count_guard(previous, parsed.active, allow_count)
            meta = cache.store(source, body, parsed.active, allow_count, transport)
            state = "fresh"
        except Exception as error:
            warning = str(error)
            try:
                body, meta = cache.load(source)  # Verified cache expires after 72 h.
            except Exception as cache_error:
                reason = "not available" if isinstance(cache_error, OSError) else str(cache_error)
                raise ValueError(f"{warning}; verified cache {reason}") from cache_error
            parsed, _ = inspect(body)
            state = "cache-fallback"
    updated = re.search(r"^!\s*(?:Last modified|Update time|Update Time):\s*(.+)", body, re.M | re.I)
    record = {"id": source["id"], "name": source["name"], "mode": source["mode"], "url": source["url"],
              "repository": source["repository"], "author": source["author"], "license": source["license"],
              "license_url": source.get("license_url"), "state": state, "warning": warning,
              "fetched_at": meta["fetched_at"], "sha256": meta["sha256"], "active": parsed.active,
              "upstream_updated": updated[1].strip() if updated else None,
              "dns_candidate": len(parsed.rules), "dns_usable": len(parsed.rules) if source["mode"] != "browser" else 0,
              "unsafe_exceptions": parsed.unsafe_exceptions, "skipped": parsed.skipped, "examples": parsed.examples}
    return {"record": record, "dns": parsed.rules if source["mode"] != "browser" else [],
            "browser": sorted(set(active_lines(body))),
            "comments": [line for line in body.splitlines() if line.startswith("!") and
                         re.match(r"!\s*(?:copyright|license|maintainer|author|by|homepage)\b", line, re.I)]}


def header(profile: dict, source_ids: list[str], sources: dict, built: str, browser: bool = False) -> str:
    lines = (["[Adblock Plus 2.0]"] if browser else []) + [f"! Title: {profile['name']}", f"! Updated: {built}",
              "! Expires: 1 day", "! This project only merges upstream rules; original authors retain credit.",
              f"! Description: {profile.get('description', '浏览器专用，不能用于 AdGuard Home。')}"]
    for sid in source_ids:
        entry = sources[sid]
        record = entry["record"]
        lines.extend([f"! Source: {record['name']} | {record['url']}",
                      f"! Author/project: {record['author']} | {record['repository']}",
                      f"! License: {record['license']} | {record.get('license_url') or 'not declared by upstream'}"])
        lines.extend(entry["comments"])
    return "\n".join(lines) + "\n\n"


def verify_services(profile: dict, rules: list[str]) -> dict:
    service, function = match_dns([{"rules": rules, "hosts": SERVICE_HOSTS}, {"rules": rules, "hosts": FUNCTION_HOSTS}])
    blocked = [host for host, result in zip(SERVICE_HOSTS, service) if result]
    if blocked:
        raise ValueError("Core service probe blocked: " + ", ".join(blocked))
    return {"service_probes": len(service), "functional_blocks": [h for h, b in zip(FUNCTION_HOSTS, function) if b]}


def generated_files(stage: Path) -> dict:
    return {p.relative_to(stage).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(stage.rglob("*")) if p.is_file()}


def safe_target(dist: Path, relative: str) -> Path:
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Unsafe artifact path")
    target = (dist / relative).resolve()
    resolved = target.relative_to(dist.resolve())
    if any(part.startswith("health_") for part in resolved.parts):
        raise ValueError("Health scan artifacts belong to the user")
    return target


def publish(stage: Path, dist: Path, manifest: dict) -> None:
    previous = {}
    if (dist / "manifest.json").exists():
        previous = json.loads((dist / "manifest.json").read_text(encoding="utf-8"))
    # Validate every path before replacing any artifact. Only manifest-owned files are pruned.
    old_files = previous.get("files", {}) if previous.get("schema") == 2 else {}
    targets = {name: safe_target(dist, name) for name in manifest["files"]}
    retired = [safe_target(dist, name) for name in old_files if name not in targets]
    backup = {}
    paths = list(targets.values()) + retired + [dist / "manifest.json"]
    for path in paths:
        backup[path] = path.read_bytes() if path.exists() else None
    try:
        for name, target in targets.items():
            data = (stage / name).read_bytes()
            if hashlib.sha256(data).hexdigest() != manifest["files"][name]:
                raise ValueError("Staged artifact checksum mismatch")
            atomic(target, data)
        for target in retired:
            target.unlink(missing_ok=True)
        atomic(dist / "manifest.json", json_text(manifest))
    except BaseException:
        for path, data in backup.items():
            if data is None:
                path.unlink(missing_ok=True)
            else:
                atomic(path, data)
        raise


def links(repository: str, path: str) -> str:
    raw = f"https://raw.githubusercontent.com/{repository}/main/dist/{path}"
    return f"[原始]({raw}) · [加速 1](https://github.boki.moe/{raw}) · [加速 2](https://ghfast.top/{raw})"


def readme(catalog: dict, manifest: dict | None, attempt: dict) -> str:
    repository = catalog["repository"]
    local = lambda t: datetime.fromisoformat(t).astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S UTC+8")
    state = ("离线缓存构建" if attempt.get("offline") else "完成（部分源使用缓存，见构建报告）" if attempt.get("degraded_sources") else "成功") if attempt["status"] == "success" else "失败，订阅保留上次成功版本"
    lines = ["# AdGuard Home 合并规则", "", "按提供的 Excel 选源，仅合并与去重。规则由上游作者维护。",
             "", f"最近构建：**{local(attempt['attempted_at'])}** · {state}。每天北京时间 **04:23** 自动更新。",
             "", "优先使用「纯广告」；PCDN 和含「不受欢迎」的方案可能影响视频、更新或推送，请按需选用。",
             "同一份 DNS 全量只选秋风完整版本，四个秋风变体不会混用。", "",
             "## AdGuard Home", "", "添加到「DNS 黑名单」。文件中的 `@@` 例外已保留，无需另加白名单。",
             "", "| 订阅 | 拦截 / 例外 | 内容 | 链接 |", "|---|---:|---|---|"]
    profiles = {p["id"]: p for p in (manifest or {}).get("profiles", [])}
    for profile in catalog["profiles"]:
        output = profiles.get(profile["id"])
        number = f"{output['block']:,} / {output['allow']:,}" if output else "未发布"
        lines.append(f"| {profile['name']} | {number} | {profile['description']} | {links(repository, profile['id'] + '.txt') if output else '等待成功构建'} |")
    if manifest:
        lines += ["", f"订阅实际更新时间：{local(manifest['built_at'])}。数量按最终去重规则行统计，通配符不等于一个域名。"]
    lines += ["", "## mihomo", "", "使用对应配置片段，将 `rule-providers` 和 `rules` 合并到现有配置；拦截规则放在兜底规则前。",
              "例外跳过本订阅的拦截并继续后续分流，不强制 DIRECT。原始与两条加速配置均提供。",
              "", "| 订阅 | 配置片段 |", "|---|---|"]
    for profile in catalog["profiles"]:
        pid = profile["id"]
        raw = f"https://raw.githubusercontent.com/{repository}/main/dist/mihomo/"
        if pid in profiles:
            lines.append(f"| {profile['name']} | [原始]({raw}{pid}.yaml) · [加速 1](https://github.boki.moe/{raw}{pid}-boki.yaml) · [加速 2](https://ghfast.top/{raw}{pid}-ghfast.yaml) |")
    lines += ["", "## 浏览器规则", "", "以下文件保留网页元素、路径、脚本和例外规则，**仅供浏览器拦截器使用，不能导入 AdGuard Home**。",
              "", "| 分类 | 条目 | 链接 |", "|---|---:|---|"]
    browsers = {p["id"]: p for p in (manifest or {}).get("browser_profiles", [])}
    for profile in catalog["browser_profiles"]:
        output = browsers.get(profile["id"])
        lines.append(f"| {profile['name']} | {output['rules'] if output else '未发布'} | {links(repository, 'browser/' + profile['id'] + '.txt') if output else '等待成功构建'} |")
    lines += ["", "<details>", "<summary>上游来源与作者（Excel 中全部 11 个地址）</summary>", "",
              "| 作者 / 项目 | 规则文件 | 类型 | 有效行 / DNS 可用 |", "|---|---|---|---:|"]
    sources = {s["id"]: s for s in (manifest or {}).get("sources", [])}
    for source in catalog["sources"]:
        record = sources.get(source["id"], {})
        count = f"{record.get('active', '—')} / {record.get('dns_usable', '—')}"
        lines.append(f"| [{source['author']}]({source['repository']}) | [{source['name']}]({source['url']}) | {source['category'].replace('|', '/')} | {count} |")
    lines += ["", "完整来源、许可、跳过原因、缓存状态与功能域名检查见 [构建报告](dist/report.json)。",
              "上游许可证保存在 [licenses](licenses/)。未声明许可的源按原样注明，不替作者指定许可证。", "", "</details>", "",
              "## 运行与维护", "", "Python 3.12，合并程序使用标准库，无需 pip 依赖。GitHub Actions 自动安装固定版本的校验引擎并运行测试。",
              "", "```powershell", "python tools/install_engines.py", "python compile_rules.py", "```", "",
              "本地需要 Go 1.27.1；Windows 已登录 GitHub CLI 时可用 `python compile_rules.py --github-api` 从相同上游文件的 API 下载。",
              "[sources.xlsx](sources.xlsx) 保留原始表格，[sources.json](sources.json) 管理分类与组合。修改 Excel 后先提取并审核分类：",
              "", '```powershell', 'python tools/import_excel.py sources.xlsx --output .cache/new-sources.json', '```', "",
              "每个订阅独立合并，仅删除完全相同的规范化规则；不进行父子域名覆盖裁剪，不把 URL 路径扩大成整站拦截。",
              "下载、格式、规则数量突变或引擎校验失败时，优先使用 72 小时内的已校验缓存；缓存也不可用则整次构建停止，保留上一版订阅。",
              "核心网站样例检查和语法校验不能保证 App 无误拦截。加速线路是第三方服务，异常时请使用原始链接。",
              "", f"[自动构建记录](https://github.com/{repository}/actions/workflows/update.yml)", ""]
    if attempt.get("errors"):
        lines += ["最近构建问题："] + [f"- {sid}: {str(error).replace(chr(10), ' ')[:300]}" for sid, error in attempt["errors"].items()] + [""]
    return "\n".join(lines)


def run(root: Path, offline: bool = False, github_api: bool = False) -> dict:
    catalog = load_catalog(root / "sources.json")
    attempt = {"attempted_at": timestamp(), "status": "running", "errors": {}, "offline": offline}
    cache = Cache(root / ".cache/excel-sources")
    collected = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {pool.submit(source_result, s, cache, offline, github_api): s["id"] for s in catalog["sources"]}
        for job in as_completed(jobs):
            sid = jobs[job]
            try:
                collected[sid] = job.result()
                print(f"{sid}: {collected[sid]['record']['state']}, DNS {len(collected[sid]['dns'])}", flush=True)
            except Exception as error:
                attempt["errors"][sid] = str(error)
    stage_root = root / ".cache/staging"
    stage_root.mkdir(parents=True, exist_ok=True)
    manifest = None
    if not attempt["errors"]:
        with tempfile.TemporaryDirectory(prefix="generation-", dir=stage_root) as temp:
            stage = Path(temp)
            built = timestamp()
            outputs, browsers = [], []
            try:
                for profile in catalog["profiles"]:
                    rules = merge([collected[sid]["dns"] for sid in profile["sources"]])
                    validation = validate_dns(rules)
                    probes = verify_services(profile, rules)
                    pid = profile["id"]
                    notices = header(profile, profile["sources"], collected, built)
                    atomic(stage / (pid + ".txt"), notices + "\n".join(rules) + "\n")
                    mihomo = export_mihomo(stage / "mihomo", pid, rules, catalog["repository"], notices.splitlines())
                    outputs.append(dict(profile, **stats(rules), validation=validation, probes=probes, mihomo=mihomo))
                    print(f"{pid}: {len(rules)} rules, AdGuard and mihomo passed", flush=True)
                for profile in catalog["browser_profiles"]:
                    rules = merge([collected[sid]["browser"] for sid in profile["sources"]])
                    atomic(stage / "browser" / (profile["id"] + ".txt"), header(profile, profile["sources"], collected, built, True) + "\n".join(rules) + "\n")
                    browsers.append(dict(profile, **stats(rules)))
                source_records = [collected[s["id"]]["record"] for s in catalog["sources"]]
                report = {"schema": 2, "built_at": built, "workbook_sha256": catalog["sha256"],
                          "sources": source_records, "profiles": outputs, "browser_profiles": browsers,
                          "policy": {"dedup": "identical normalized lines within each output", "coverage_pruning": False,
                                     "browser_in_dns": False, "max_cache_hours": 72,
                                     "service_probe_limit": "sample hostname tests, not real App behavior"}}
                atomic(stage / "report.json", json_text(report))
                manifest = dict(report, files=generated_files(stage))
                publish(stage, root / "dist", manifest)
                attempt["status"] = "success"
                attempt["degraded_sources"] = [s["id"] for s in source_records if s["state"] == "cache-fallback"]
            except Exception as error:
                attempt["errors"]["publication"] = str(error)
    if attempt["errors"]:
        attempt["status"] = "failed"
        old = root / "dist/manifest.json"
        if old.exists():
            previous = json.loads(old.read_text(encoding="utf-8"))
            manifest = previous if previous.get("schema") == 2 else None
    atomic(root / ".cache/build-report.json", json_text(attempt))
    atomic(root / "README.md", readme(catalog, manifest, attempt))
    summary = Path(os.environ["GITHUB_STEP_SUMMARY"]) if os.environ.get("GITHUB_STEP_SUMMARY") else None
    if summary:
        atomic(summary, f"Build status: {attempt['status']}\n\n" + json_text(attempt))
    return attempt
