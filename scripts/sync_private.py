"""WorkBuddy 原文记忆/内容的加密同步：单一密文 blob。

口令来源优先级：AI_BRAIN_PASSPHRASE 环境变量 > 本机一次性文件 local/passphrase.txt。
口令值永不进入命令行、命令输出、日志或仓库。原文只在内存中打包，不落盘明文。
"""
from __future__ import annotations

import base64
import fnmatch
import hashlib
import io
import os
import secrets
import sys
import zipfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as common  # noqa: E402

MAGIC = b"AIBRAIN1"
SALT_SIZE = 16
SCRYPT_N = 1 << 15
PASSPHRASE_ENV = "AI_BRAIN_PASSPHRASE"
PASSPHRASE_FILE = common.ROOT / "local" / "passphrase.txt"


def _fernet(passphrase: str, salt: bytes):
    from cryptography.fernet import Fernet
    key = hashlib.scrypt(
        passphrase.encode("utf-8"), salt=salt,
        n=SCRYPT_N, r=8, p=1, dklen=32, maxmem=128 * 1024 * 1024,
    )
    return Fernet(base64.urlsafe_b64encode(key))


def _passphrase() -> str:
    value = os.environ.get(PASSPHRASE_ENV)
    if value:
        return value
    if PASSPHRASE_FILE.is_file():
        value = PASSPHRASE_FILE.read_text(encoding="utf-8").strip()
        if value:
            return value
    raise RuntimeError("no passphrase: set the env var or run init-passphrase")


def init_passphrase() -> Path:
    """生成高熵口令并存入被 gitignore 的一次性文件；值绝不回显。"""
    if PASSPHRASE_FILE.is_file() and PASSPHRASE_FILE.read_text(encoding="utf-8").strip():
        print("PASSPHRASE EXISTS (value not shown)")
        return PASSPHRASE_FILE
    PASSPHRASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PASSPHRASE_FILE.write_text(secrets.token_urlsafe(32), encoding="utf-8")
    print("PASSPHRASE SAVED (value not shown): local/passphrase.txt")
    return PASSPHRASE_FILE


def forget_passphrase() -> None:
    """口令转移到口令管理器后，删除本机一次性文件。"""
    if PASSPHRASE_FILE.is_file():
        PASSPHRASE_FILE.unlink()
    print("PASSPHRASE FILE REMOVED")


def encrypt(files, base: Path, out: Path) -> int:
    """files: Path 列表，或 (arcname, Path) 元组列表。"""
    entries: list[tuple[str, Path]] = []
    for item in files:
        if isinstance(item, tuple):
            arc, path = item
        else:
            arc, path = item.relative_to(base).as_posix(), item
        entries.append((arc.replace("\\", "/"), Path(path)))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for arc, path in sorted(entries):
            archive.write(path, arcname=arc)
    salt = os.urandom(SALT_SIZE)
    token = _fernet(_passphrase(), salt).encrypt(buffer.getvalue())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(MAGIC + salt + token)
    return len(entries)


def _open(bundle: Path) -> bytes:
    blob = bundle.read_bytes()
    if not blob.startswith(MAGIC):
        raise ValueError("not an encrypted ai-brain bundle")
    salt = blob[len(MAGIC):len(MAGIC) + SALT_SIZE]
    token = blob[len(MAGIC) + SALT_SIZE:]
    return _fernet(_passphrase(), salt).decrypt(token)


def decrypt(bundle: Path, dest: Path) -> Path:
    raw = _open(bundle)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for info in archive.infolist():
            name = Path(info.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError("unsafe path inside bundle")
            target = dest / name
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
    return dest


def verify(bundle: Path) -> bool:
    try:
        with zipfile.ZipFile(io.BytesIO(_open(bundle))) as archive:
            return len(archive.namelist()) > 0
    except Exception:
        return False


def collect_sources() -> list[tuple[str, Path]]:
    cfg = yaml.safe_load((common.ROOT / "private" / "sources.yaml").read_text(encoding="utf-8"))
    excludes = cfg.get("exclude", [])
    collected: dict[str, tuple[str, Path]] = {}
    for source in cfg["sources"]:
        base = Path(common.expand(source["base"]))
        if not base.is_dir():
            continue
        for pattern in source["include"]:
            for path in sorted(base.glob(pattern)):
                if not path.is_file():
                    continue
                rel = path.relative_to(base).as_posix()
                if any(fnmatch.fnmatch(rel, rule.lstrip("/")) for rule in excludes):
                    continue
                arc = f"{source['id']}/{rel}"
                collected[arc] = (arc, path)
    return [collected[key] for key in sorted(collected)]


def main(argv: list[str]) -> int:
    command = argv[0] if argv else ""
    bundle = common.ROOT / common.load_manifest()["private_bundle"]["path"]
    if command == "init-passphrase":
        init_passphrase()
        return 0
    if command == "forget":
        forget_passphrase()
        return 0
    if command == "encrypt":
        entries = collect_sources()
        if not entries:
            print("NO SOURCES")
            return 1
        count = encrypt(entries, common.ROOT, bundle)
        print(f"ENCRYPTED: {count} files")
        return 0
    if command == "decrypt":
        if not bundle.is_file():
            print("NO BUNDLE")
            return 1
        decrypt(bundle, common.ROOT / common.load_manifest()["private_bundle"]["restore_to"])
        print("DECRYPTED")
        return 0
    if command == "verify":
        if not bundle.is_file():
            print("NO BUNDLE")
            return 0
        ok = verify(bundle)
        print("BUNDLE OK" if ok else "BUNDLE FAILED")
        return 0 if ok else 1
    print("usage: sync_private.py init-passphrase|encrypt|verify|decrypt|forget")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
