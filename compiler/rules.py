"""Conservative host-level conversion. No parent expansion or coverage pruning."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import ipaddress
import re


def domain(value: str) -> str | None:
    try:
        value = value.rstrip(".").encode("idna").decode("ascii").lower()
        ipaddress.ip_address(value)
        return None
    except ValueError:
        pass
    except UnicodeError:
        return None
    if len(value) > 253 or "." not in value:
        return None
    if any(not re.fullmatch(r"[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?", p) for p in value.split(".")):
        return None
    if value in {"localhost.localdomain", "broadcasthost.localdomain"}:
        return None
    return value


def active_lines(body: str) -> list[str]:
    return [line.strip() for line in body.splitlines()
            if line.strip() and not line.lstrip().startswith(("!", "# ", "#\t", "[Adblock", "#屏蔽"))
            and line.strip() != "#"]


def dns_line(line: str) -> tuple[list[str], str | None]:
    """Accept only patterns whose complete scope fits a DNS hostname."""
    if any(marker in line for marker in ("##", "#@#", "#?#", "#$#", "#%#", "#@$#", "#@?#")):
        return [], "cosmetic"
    if line.startswith("#"):
        return [], "comment"
    hosts = line.split("#", 1)[0].split()
    if len(hosts) > 1:
        try:
            address = ipaddress.ip_address(hosts[0])
        except ValueError:
            return [], "unsupported"
        if not (address.is_unspecified or address.is_loopback):
            return [], "dns-rewrite"
        names = [domain(x) for x in hosts[1:]]
        if not all(names):
            return [], "invalid-hosts"
        return [f"|{name}|" for name in names], None
    name = domain(line)
    if name:
        return [f"|{name}|"], None
    allow = line.startswith("@@")
    pattern = line[2:] if allow else line
    important = pattern.endswith("$important")
    if important:
        pattern = pattern[:-10]
    if "$" in pattern and not (pattern.startswith("/") and pattern.endswith("/")):
        return [], "browser-modifier"
    if pattern.startswith("/") and pattern.endswith("/"):
        # URL/resource regex cannot be stripped to a host without widening it.
        if any(t in pattern for t in (":", "/", "\\/")) and "/" in pattern[1:-1]:
            return [], "url-regex"
        if any(t in pattern[1:-1] for t in ("http", ":", "\\Q", "\\E", "[[:")):
            return [], "nonportable-regex"
        if not pattern[1:-1] or any(c.isspace() for c in pattern):
            return [], "invalid-regex"
        return [line], None  # Compile with the actual Go engine before publication.
    if "/" in pattern or ":" in pattern or "?" in pattern or "=" in pattern:
        return [], "url-path"
    simple = re.fullmatch(r"(\|\||\|)([^|^*]+)(\^|\|)", pattern)
    if simple and (simple[1], simple[3]) in (("||", "^"), ("|", "|")):
        name = domain(simple[2])
        if not name:
            return [], "invalid-domain"
        rule = simple[1] + name + simple[3]
    elif re.fullmatch(r"[a-zA-Z0-9_.|^*\-]+", pattern) and "." in pattern and "*" in pattern:
        rule = pattern.lower()
        if ".." in rule or rule.replace("*", "").strip("|^") in {"", ".", "com", "cn", "net", "org"}:
            return [], "overbroad"
    else:
        return [], "unsupported"
    return [("@@" if allow else "") + rule + ("$important" if important else "")], None


@dataclass
class Parsed:
    rules: list[str]
    skipped: dict[str, int]
    examples: list[dict]
    unsafe_exceptions: int
    active: int

    def require_dns_safe(self) -> None:
        if self.unsafe_exceptions:
            raise ValueError(f"{self.unsafe_exceptions} unsupported exception/disable rules: cannot safely extract DNS subset")
        if not self.rules:
            raise ValueError("No host-level DNS rules")


def parse(body: str, mode: str) -> Parsed:
    counts, examples, collected, unsafe = Counter(), [], [], 0
    lines = active_lines(body)
    for number, line in enumerate(lines, 1):
        result, reason = dns_line(line)
        if reason:
            counts[reason] += 1
            if len(examples) < 12:
                examples.append({"active_line": number, "reason": reason, "rule": line})
            if line.startswith("@@") or "$badfilter" in line or ",badfilter" in line:
                unsafe += 1
        collected.extend(result)
    parsed = Parsed(sorted(set(collected)), dict(counts), examples, unsafe, len(lines))
    if mode == "dns" and counts:
        raise ValueError(f"DNS source changed format; rejected lines: {dict(counts)}")
    if mode not in {"dns", "mixed", "browser"}:
        raise ValueError(f"Unknown source mode {mode}")
    return parsed


def merge(groups: list[list[str]]) -> list[str]:
    # Each output receives its own complete set. Different outputs never share ownership.
    return sorted({rule for group in groups for rule in group})


def stats(rules: list[str]) -> dict:
    return {"rules": len(rules), "block": sum(not r.startswith("@@") for r in rules),
            "allow": sum(r.startswith("@@") for r in rules),
            "important": sum(r.endswith("$important") for r in rules)}
