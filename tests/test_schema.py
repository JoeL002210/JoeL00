import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import _common as common  # noqa: E402


class CardSchemaTests(unittest.TestCase):
    def test_all_content_cards_are_valid_public_cards(self):
        manifest = common.load_manifest()
        seen = set()
        count = 0
        for path in common.iter_card_paths():
            meta, body = common.parse_card(path)
            errors = common.card_errors(meta, body, manifest)
            self.assertEqual([], errors, f"{common.relative(path)}: {errors}")
            self.assertNotIn(meta["id"], seen, f"duplicate id: {meta['id']}")
            seen.add(meta["id"])
            count += 1
        self.assertGreaterEqual(count, 10, "content layer is unexpectedly small")

    def test_manifest_contract(self):
        manifest = common.load_manifest()
        self.assertEqual("local", manifest["sensitivity_default"])
        self.assertTrue(manifest["private_bundle"]["encrypted"])
        self.assertGreater(manifest["budgets"]["ai_brief_tokens"], 0)
        for source in manifest["sources"]:
            self.assertTrue((ROOT / source).is_dir(), f"missing source dir: {source}")

    def test_every_adapter_has_a_file_and_entry(self):
        manifest = common.load_manifest()
        import yaml
        for name in manifest["adapters"]:
            path = ROOT / "adapters" / f"{name}.yaml"
            self.assertTrue(path.is_file(), f"missing adapter: {name}")
            cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(name, cfg["tool"])
            self.assertTrue(cfg["entry"].startswith("dist/"))
            self.assertIn(cfg["include_mode"], {"inline", "import", "link"})

    def test_generated_header_is_declared_in_docs(self):
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("禁止手改", contributing)


if __name__ == "__main__":
    unittest.main()
