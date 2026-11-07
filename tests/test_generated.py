import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import _common as common  # noqa: E402
import build  # noqa: E402


class GenerationTests(unittest.TestCase):
    def test_render_is_deterministic(self):
        first = build.render()
        second = build.render()
        self.assertEqual(set(first), set(second))
        for key in first:
            self.assertEqual(first[key], second[key], f"non-deterministic: {key}")

    def test_generated_files_carry_the_marker(self):
        files = build.render()
        for name, data in files.items():
            if name.endswith((".md", ".mdc")):
                self.assertIn(b"GENERATED", data, f"missing marker: {name}")

    def test_build_manifest_matches_rendered_hashes(self):
        files = build.render()
        manifest = json.loads(files["dist/BUILD.json"].decode("utf-8"))
        self.assertEqual(set(manifest["files"]), set(files) - {"dist/BUILD.json"})
        for name, digest in manifest["files"].items():
            self.assertEqual(common.sha256(files[name]), digest, f"hash mismatch: {name}")

    def test_disk_matches_render(self):
        files = build.render()
        stale = [name for name, data in files.items()
                 if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        self.assertEqual([], stale, "run: python scripts/build.py")

    def test_brief_stays_within_budget(self):
        files = build.render()
        brief = files["dist/ai-brief.md"].decode("utf-8")
        budget = common.load_manifest()["budgets"]["ai_brief_tokens"]
        self.assertLessEqual(common.estimate_tokens(brief), budget)
        self.assertIn("按需索引", brief)

    def test_index_jsonl_is_parseable_and_sorted(self):
        files = build.render()
        lines = files["dist/index.jsonl"].decode("utf-8").splitlines()
        self.assertGreater(len(lines), 10)
        ids = []
        for line in lines:
            row = json.loads(line)
            self.assertIn("text", row)
            self.assertIn("id", row)
            ids.append((row["path"], row["id"]))
        self.assertEqual(sorted(ids), ids, "index.jsonl must be deterministically ordered")


if __name__ == "__main__":
    unittest.main()
