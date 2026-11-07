"""提交前敏感信息扫描：只输出布尔结论与计数，绝不回显命中内容。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as common  # noqa: E402

SCAN_DIRS = ("core", "playbook", "context", "dist", "adapters", "inbox", "archive", "private")
SCAN_FILES = ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "MANIFEST.yaml")
TEXT_SUFFIXES = {".md", ".mdc", ".yaml", ".yml", ".jsonl", ".txt"}
EMAIL_ALLOWED_DOMAINS = {"example.invalid"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PATTERNS = (
    re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
    re.compile(r"[A-Za-z]:[\\/]Users[\\/][^\\\s/]+", re.I),
    re.compile(r"\\\\{2}[A-Za-z0-9._-]+[\\/]"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"[?&](?:sig|signature|X-Amz-Signature|X-Amz-Credential)=", re.I),
    EMAIL,
)


def extra_terms() -> list[str]:
    path = common.ROOT / "local" / "pii_terms.txt"
    if not path.is_file():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def text_has_findings(text: str, terms: list[str] | None = None) -> bool:
    for pattern in PATTERNS:
        for match in pattern.finditer(text):
            if pattern is EMAIL:
                domain = match.group(0).rsplit("@", 1)[-1].lower()
                if domain in EMAIL_ALLOWED_DOMAINS:
                    continue
            return True
    for term in (terms if terms is not None else extra_terms()):
        if term in text:
            return True
    return False


def scan() -> list[str]:
    """返回命中文件的相对路径（不含命中文本）。"""
    terms = extra_terms()
    findings: list[str] = []
    targets: list[Path] = []
    for folder in SCAN_DIRS:
        root = common.ROOT / folder
        if root.is_dir():
            targets.extend(p for p in sorted(root.rglob("*"))
                           if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES
                           and ".example." not in p.name)
    targets.extend(common.ROOT / name for name in SCAN_FILES
                   if (common.ROOT / name).is_file())
    seen: set[str] = set()
    for path in targets:
        rel = common.relative(path)
        if rel in seen:
            continue
        seen.add(rel)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(rel)
            continue
        if text_has_findings(text, terms):
            findings.append(rel)
    return findings


def report(findings_count: int) -> str:
    if findings_count:
        return f"FINDINGS: {findings_count} files"
    return "CLEAN"


def main() -> int:
    findings = scan()
    print(report(len(findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
