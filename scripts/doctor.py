"""一致性自检：生成物是否漂移、加密 bundle 是否为真密文。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as common  # noqa: E402
import build  # noqa: E402
import sync_private  # noqa: E402


def main() -> int:
    issues: list[str] = []
    try:
        files = build.render()
    except Exception as exc:
        print(f"DRIFT: render failed ({type(exc).__name__})")
        return 1
    for name, data in files.items():
        path = common.ROOT / name
        if not path.is_file() or path.read_bytes() != data:
            issues.append(name)
    private = common.ROOT / "private"
    for bundle in sorted(private.glob("*.enc")):
        if not bundle.read_bytes().startswith(sync_private.MAGIC):
            issues.append(common.relative(bundle))
    if issues:
        print(f"DRIFT: {len(issues)} issues — run: python scripts/build.py")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
