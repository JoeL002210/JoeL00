"""新设备接入：生成入口、（可选）安装到工具用户级位置、（可选）解密私有层、自检。

默认只做 dry-run 与生成，不改动任何工具配置；加 --install 才会写入，
且写入前把已存在的目标文件备份到 local/backups/（该目录被 gitignore）。
"""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as common  # noqa: E402
import build  # noqa: E402
import sync_private  # noqa: E402


def adapter_configs(manifest: dict):
    for name in manifest["adapters"]:
        path = common.ROOT / "adapters" / f"{name}.yaml"
        yield yaml.safe_load(path.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    install = "--install" in argv
    manifest = common.load_manifest()
    try:
        build.write(build.render())
    except Exception as exc:
        print(f"BOOTSTRAP FAILED: {type(exc).__name__}: {exc}")
        return 1

    installed = 0
    manual: list[str] = []
    for cfg in adapter_configs(manifest):
        if cfg["install_mode"] != "copy":
            manual.append(cfg["tool"])
            continue
        source = common.ROOT / cfg["entry"]
        destination = Path(common.expand(cfg["install_to"]))
        if install:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists() or destination.is_symlink():
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                backup = common.ROOT / "local" / "backups" / f"{cfg['tool']}-{stamp}.bak"
                backup.parent.mkdir(parents=True, exist_ok=True)
                if destination.is_file():
                    shutil.copy2(destination, backup)
            shutil.copy2(source, destination)
        installed += 1
        print(f"  {cfg['tool']}: {cfg['install_to']}" + (" (installed)" if install else " (dry-run)"))

    bundle_path = common.ROOT / manifest["private_bundle"]["path"]
    env_name = manifest["private_bundle"]["passphrase_env"]
    passphrase_ready = bool(os.environ.get(env_name)) or sync_private.PASSPHRASE_FILE.is_file()
    if bundle_path.is_file() and passphrase_ready:
        sync_private.decrypt(bundle_path, common.ROOT / manifest["private_bundle"]["restore_to"])
        print("  private bundle: decrypted to local/")
    elif bundle_path.is_file():
        print("  private bundle: present, skipped (no passphrase available)")

    if manual:
        print(f"  manual: {', '.join(manual)}")
    print(f"BOOTSTRAP {'OK' if install else 'DRY-RUN OK'}: {installed} copy targets, {len(manual)} manual")
    if not install:
        print("  to write tool configs: python scripts/bootstrap.py --install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
