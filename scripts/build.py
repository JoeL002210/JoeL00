"""确定性生成：内容层 -> dist/ 简报、切片索引与各工具入口。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as common  # noqa: E402

SECTION = re.compile(r"^##\s+(.+?)\s*$", re.M)


class BuildError(RuntimeError):
    pass


def collect(manifest: dict) -> list[dict]:
    cards: list[dict] = []
    seen: dict[str, str] = {}
    for path in common.iter_card_paths():
        meta, body = common.parse_card(path)
        errors = common.card_errors(meta, body, manifest)
        if errors:
            raise BuildError(f"{common.relative(path)}: {'; '.join(errors)}")
        if meta["status"] == "archived" or meta["load"] == "never":
            continue
        if meta["id"] in seen:
            raise BuildError(f"duplicate id {meta['id']}: {seen[meta['id']]} vs {common.relative(path)}")
        seen[meta["id"]] = common.relative(path)
        cards.append({"meta": meta, "body": body, "path": common.relative(path)})
    return cards


def split_sections(body: str) -> list[tuple[str, str]]:
    matches = list(SECTION.finditer(body))
    if not matches:
        return [("", body.strip())]
    out = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        out.append((match.group(1), body[match.start():end].strip()))
    return out


def make_brief(cards: list[dict], manifest: dict) -> str:
    parts = [
        common.GENERATED,
        f"# ai-brain · 共享简报 v{manifest['content_version']}\n",
        "本文件为生成物。修改请改 `core/`、`playbook/`、`context/` 后重跑 `scripts/build.py`。\n",
        "## 常驻规则\n",
    ]
    always = [c for c in cards if c["meta"]["load"] == "always"]
    on_demand = [c for c in cards if c["meta"]["load"] == "on-demand"]
    for card in always:
        meta = card["meta"]
        parts.append(f"\n### {meta['title']} · `{meta['id']}`\n\n{card['body'].strip()}\n")
    parts.append("\n## 按需索引\n\n")
    parts.append("| ID | 类型 | 摘要 | 路径 |\n|---|---|---|---|\n")
    for card in on_demand:
        meta = card["meta"]
        parts.append(f"| `{meta['id']}` | {meta['type']} | {meta['summary']} | `{card['path']}` |\n")
    parts.append("\n## 使用约束\n\n")
    parts.append("- 只按 ID 拉取本次任务需要的卡片，不整批注入（渐进式披露）。\n")
    parts.append("- 一个工具一个适配器，新增工具不动内容层。\n")
    parts.append("- 原文记忆需解密到 `local/` 后才可读；不得写回仓库。\n")
    parts.append("- 本仓库不含 PII；任何真实标识信息都属 `local/`。\n")
    return "".join(parts)


def make_index(cards: list[dict]) -> str:
    rows = []
    for card in sorted(cards, key=lambda c: c["path"]):
        meta = card["meta"]
        for heading, text in split_sections(card["body"]):
            rows.append({
                "id": meta["id"],
                "path": card["path"],
                "heading": heading,
                "text": text,
                "type": meta["type"],
                "load": meta["load"],
                "tags": meta["tags"],
                "summary": meta["summary"],
            })
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)


def render() -> dict[str, bytes]:
    manifest = common.load_manifest()
    cards = collect(manifest)
    brief = make_brief(cards, manifest)
    tokens = common.estimate_tokens(brief)
    budget = manifest["budgets"]["ai_brief_tokens"]
    if tokens > budget:
        raise BuildError(f"ai-brief.md exceeds budget: {tokens} > {budget} estimated tokens")

    files: dict[str, bytes] = {
        "dist/ai-brief.md": brief.encode("utf-8"),
        "dist/index.jsonl": make_index(cards).encode("utf-8"),
    }

    for name in manifest["adapters"]:
        cfg_path = common.ROOT / "adapters" / f"{name}.yaml"
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        mode = cfg["include_mode"]
        if mode == "link":
            continue
        if mode == "import":
            body = (
                "# ai-brain · 共享入口\n\n"
                "本文件为生成物，禁止手改。常驻规则由下列引用提供：\n\n"
                f"{cfg['import_line']}\n\n"
                "按需卡片见同目录 `index.jsonl` 与内容层 `context/INDEX.md`。\n"
            )
            content = common.GENERATED + body
        elif mode == "inline":
            content = brief
        else:
            raise BuildError(f"unknown include_mode: {mode}")
        frontmatter = cfg.get("frontmatter")
        if frontmatter:
            fm = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=True)
            content = f"---\n{fm}---\n" + content
        files[cfg["entry"]] = content.encode("utf-8")

    hashes = {name: common.sha256(data) for name, data in files.items()}
    build_manifest = {
        "schema_version": manifest["schema_version"],
        "content_version": manifest["content_version"],
        "files": hashes,
    }
    files["dist/BUILD.json"] = (
        json.dumps(build_manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    return files


def write(files: dict[str, bytes]) -> None:
    for name, data in files.items():
        path = common.ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def main(argv: list[str]) -> int:
    try:
        files = render()
    except (BuildError, ValueError) as exc:
        print(f"BUILD FAILED: {exc}")
        return 1
    if "--check" in argv:
        stale = [name for name, data in files.items()
                 if not (common.ROOT / name).is_file()
                 or (common.ROOT / name).read_bytes() != data]
        if stale:
            print(f"STALE: {len(stale)} files — run: python scripts/build.py")
            return 1
        print(f"GENERATED OK: {len(files)} files")
        return 0
    write(files)
    print(f"WROTE {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
