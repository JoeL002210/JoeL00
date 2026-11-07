"""ai-brain 公共工具：卡片解析、校验与哈希。"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "MANIFEST.yaml"
SOURCES = ("core", "playbook", "context")

REQUIRED = (
    "id", "title", "type", "scope", "status", "version", "updated",
    "review_by", "sensitivity", "load", "summary", "tags",
)
ENUMS = {
    "type": {"preference", "rule", "prompt", "context", "workflow", "index"},
    "status": {"active", "deprecated", "archived"},
    "sensitivity": {"public", "local"},
    "load": {"always", "on-demand", "never"},
}
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GENERATED = "<!-- GENERATED FROM MANIFEST by scripts/build.py — DO NOT EDIT -->\n"


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_card(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"frontmatter missing: {relative(path)}")
    meta = yaml.safe_load(match.group(1))
    if not isinstance(meta, dict):
        raise ValueError(f"frontmatter is not a mapping: {relative(path)}")
    return meta, text[match.end():]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_card_paths():
    for source in SOURCES:
        yield from sorted((ROOT / source).rglob("*.md"))


def card_errors(meta: dict, body: str, manifest: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in meta:
            errors.append(f"missing field: {key}")
    for key, allowed in ENUMS.items():
        if key in meta and meta[key] not in allowed:
            errors.append(f"invalid {key}: {meta[key]}")
    if "id" in meta and not re.fullmatch(r"[A-Za-z0-9._-]{3,}", str(meta["id"])):
        errors.append("invalid id format")
    for key in ("updated", "review_by"):
        if key in meta and not DATE.match(str(meta[key])):
            errors.append(f"invalid date: {key}")
    if "sensitivity" in meta and meta["sensitivity"] != "public":
        errors.append("content-layer card must be sensitivity: public")
    if "summary" in meta and len(str(meta["summary"])) > 150:
        errors.append("summary exceeds 150 characters")
    if "tags" in meta and (not isinstance(meta["tags"], list) or not meta["tags"]):
        errors.append("tags must be a non-empty list")
    max_lines = manifest["budgets"]["max_card_lines"]
    if body.count("\n") + 1 > max_lines:
        errors.append(f"body exceeds {max_lines} lines")
    return errors


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def estimate_tokens(text: str) -> int:
    """粗略估算：中日韩文本按 2 字符/token 保守计算。"""
    return len(text) // 2


def expand(value: str, extra: dict[str, str] | None = None) -> str:
    import os
    mapping = {
        "HOME": str(Path.home()),
        "AI_BRAIN": str(ROOT),
        "WORKSPACE": os.environ.get("AI_BRAIN_WORKSPACE", str(ROOT.parent)),
        "CODEBUDDY_HOME": str(Path.home() / ".codebuddy"),
    }
    if extra:
        mapping.update(extra)
    for key, val in mapping.items():
        value = value.replace("${" + key + "}", val)
    return value
