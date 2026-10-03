"""Bounded HTTPS download and checksum-verified, expiring source cache."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

LIMIT = 32 * 1024 * 1024


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic(path: Path, data: bytes | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def check_body(data: bytes) -> str:
    if not data or len(data) > LIMIT:
        raise ValueError("Empty or oversized download")
    body = data.decode("utf-8-sig")
    if "\x00" in body or re.search(r"<!doctype\s+html|<html\b|<body\b", body[:2000], re.I):
        raise ValueError("Download is not a text filter list")
    # Author-specified count is checked before parsing/duplicates are removed.
    expected = re.search(r"^!\s*(?:Entries|Total lines):\s*(\d+)", body, re.M | re.I)
    if expected:
        actual = sum(bool(line.strip()) and not line.lstrip().startswith(("!", "#", "[Adblock")) for line in body.splitlines())
        if actual != int(expected[1]):
            raise ValueError(f"Declared count {expected[1]} differs from received {actual}")
    return body


def download(url: str, github_api: bool = False) -> tuple[str, str]:
    if urlsplit(url).scheme != "https":
        raise ValueError("Only HTTPS source URLs are allowed")
    if github_api and urlsplit(url).hostname == "raw.githubusercontent.com":
        parts = urlsplit(url).path.strip("/").split("/")
        repository, tail = "/".join(parts[:2]), parts[2:]
        if tail[:2] == ["refs", "heads"]:
            tail = tail[2:]
        branch, path = tail[0], "/".join(tail[1:])
        route = f"repos/{repository}/contents/{quote(path)}?ref={quote(branch)}"
        result = subprocess.run(["gh", "api", route, "-H", "Accept: application/vnd.github.raw+json"],
                                capture_output=True, timeout=70)
        if result.returncode:
            raise ValueError(result.stderr.decode("utf-8", errors="replace")[:400])
        return check_body(result.stdout), "github-api"
    request = Request(url, headers={"User-Agent": "adguardhome-compiled-filters/2", "Accept-Encoding": "identity"})
    with urlopen(request, timeout=45) as response:
        if response.status != 200 or urlsplit(response.url).scheme != "https":
            raise ValueError("Unexpected response status or HTTPS downgrade")
        data = response.read(LIMIT + 1)
        length = response.headers.get("Content-Length")
        if length and int(length) != len(data):
            raise ValueError("Truncated HTTP response")
    return check_body(data), "https"


class Cache:
    def __init__(self, directory: Path, max_age_hours: int = 72):
        self.directory, self.max_age_hours = directory, max_age_hours

    def paths(self, source: dict) -> tuple[Path, Path]:
        key = hashlib.sha256(source["url"].encode()).hexdigest()
        return self.directory / (key + ".txt"), self.directory / (key + ".json")

    def load(self, source: dict, enforce_age: bool = True) -> tuple[str, dict]:
        path, info = self.paths(source)
        meta = json.loads(info.read_text(encoding="utf-8"))
        data = path.read_bytes()
        if meta["url"] != source["url"] or hashlib.sha256(data).hexdigest() != meta["sha256"]:
            raise ValueError("Cache identity/checksum mismatch")
        age = datetime.now(timezone.utc) - datetime.fromisoformat(meta["fetched_at"])
        if age.total_seconds() < -300 or (enforce_age and age.total_seconds() > self.max_age_hours * 3600):
            raise ValueError("Source cache expired or has future timestamp")
        return check_body(data), meta

    def store(self, source: dict, body: str, count: int, allow_count: int, transport: str) -> dict:
        path, info = self.paths(source)
        data = body.encode("utf-8")
        meta = {"url": source["url"], "fetched_at": timestamp(), "sha256": hashlib.sha256(data).hexdigest(),
                "active": count, "allow": allow_count, "transport": transport}
        atomic(path, data)
        atomic(info, json_text(meta))
        return meta


def count_guard(previous: dict | None, count: int, allow_count: int) -> None:
    if not previous:
        return
    old = previous["active"]
    if old >= 5 and count < old * .7:
        raise ValueError(f"Source count dropped more than 30% ({old} -> {count})")
    if old >= 100 and count > max(old * 2, old + 1000):
        raise ValueError(f"Source count grew unexpectedly ({old} -> {count})")
    old_allow = previous.get("allow", 0)
    if old_allow and allow_count < old_allow * .7:
        raise ValueError("Source exceptions disappeared or dropped more than 30%")


def retry_download(url: str, github_api: bool = False) -> tuple[str, str]:
    for attempt in range(3):
        try:
            return download(url, github_api)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
