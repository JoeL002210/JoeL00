import os
import secrets
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import audit  # noqa: E402
import sync_private  # noqa: E402


class PrivacyTests(unittest.TestCase):
    def test_repository_content_is_clean(self):
        findings = audit.scan()
        self.assertEqual([], findings, "run: python scripts/audit.py")

    def test_scanner_detects_pii_without_echoing_it(self):
        samples = [
            "contact: person@example.org",
            "mobile: 13800138000",
            r"path: C:\Users\someone\notes.md",
            "token: ghp_" + "A" * 36,
        ]
        for sample in samples:
            self.assertTrue(audit.text_has_findings(sample), "scanner missed a PII pattern")
        self.assertNotIn("13800138000", audit.report(findings_count=1))

    def test_private_bundle_roundtrip_never_writes_plaintext(self):
        passphrase = secrets.token_hex(16)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source" / "note.md"
            source.parent.mkdir(parents=True)
            secret_line = "private marker " + secrets.token_hex(8)
            source.write_text(secret_line, encoding="utf-8")
            bundle = tmp_path / "bundle.enc"
            os.environ["AI_BRAIN_PASSPHRASE"] = passphrase
            try:
                count = sync_private.encrypt([source], tmp_path / "source", bundle)
                self.assertEqual(1, count)
                blob = bundle.read_bytes()
                self.assertTrue(blob.startswith(sync_private.MAGIC))
                self.assertNotIn(secret_line.encode("utf-8"), blob)
                self.assertNotIn(b"note.md", blob)
                self.assertTrue(sync_private.verify(bundle))
                restored = sync_private.decrypt(bundle, tmp_path / "restored")
                self.assertEqual(secret_line, (restored / "note.md").read_text(encoding="utf-8"))
            finally:
                os.environ.pop("AI_BRAIN_PASSPHRASE", None)

    def test_wrong_passphrase_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "s" / "a.md"
            source.parent.mkdir(parents=True)
            source.write_text("x", encoding="utf-8")
            bundle = tmp_path / "b.enc"
            os.environ["AI_BRAIN_PASSPHRASE"] = secrets.token_hex(8)
            try:
                sync_private.encrypt([source], tmp_path / "s", bundle)
                os.environ["AI_BRAIN_PASSPHRASE"] = secrets.token_hex(8)
                self.assertFalse(sync_private.verify(bundle))
            finally:
                os.environ.pop("AI_BRAIN_PASSPHRASE", None)


    def test_init_passphrase_never_prints_the_value(self):
        import contextlib
        import io
        original = sync_private.PASSPHRASE_FILE
        with tempfile.TemporaryDirectory() as tmp:
            sync_private.PASSPHRASE_FILE = Path(tmp) / "passphrase.txt"
            try:
                captured = io.StringIO()
                with contextlib.redirect_stdout(captured):
                    path = sync_private.init_passphrase()
                value = path.read_text(encoding="utf-8").strip()
                self.assertGreaterEqual(len(value), 32)
                self.assertNotIn(value, captured.getvalue())
                self.assertIn("not shown", captured.getvalue())
            finally:
                sync_private.PASSPHRASE_FILE = original

    def test_encrypt_works_with_local_passphrase_file_only(self):
        original = sync_private.PASSPHRASE_FILE
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sync_private.PASSPHRASE_FILE = tmp_path / "passphrase.txt"
            sync_private.PASSPHRASE_FILE.write_text(secrets.token_hex(16), encoding="utf-8")
            os.environ.pop("AI_BRAIN_PASSPHRASE", None)
            source = tmp_path / "s" / "a.md"
            source.parent.mkdir(parents=True)
            source.write_text("x", encoding="utf-8")
            try:
                self.assertEqual(1, sync_private.encrypt([source], tmp_path / "s", tmp_path / "b.enc"))
                self.assertTrue(sync_private.verify(tmp_path / "b.enc"))
            finally:
                sync_private.PASSPHRASE_FILE = original


if __name__ == "__main__":
    unittest.main()
