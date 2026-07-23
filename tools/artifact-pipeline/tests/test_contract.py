import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("contract", ROOT / "contract.py")
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class ArtifactContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = contract.load_manifest(ROOT)

    def template(self, name):
        spec = self.manifest["artifacts"][name]
        return (ROOT / spec["template"]).read_text(encoding="utf-8")

    def test_all_five_templates_match_manifest(self):
        self.assertEqual({}, contract.validate_templates(ROOT))
        self.assertEqual(5, len(self.manifest["artifacts"]))

    def test_unknown_artifact_is_rejected(self):
        self.assertTrue(contract.validate_text("mystery", "# x\n", self.manifest))

    def test_missing_reordered_and_duplicate_sections_are_rejected(self):
        text = self.template("concept")
        self.assertTrue(contract.validate_text("concept", text.replace("## Scope\n", ""), self.manifest))
        swapped = text.replace("## Current Understanding", "## TEMP").replace("## Scope", "## Current Understanding").replace("## TEMP", "## Scope")
        self.assertTrue(contract.validate_text("concept", swapped, self.manifest))
        self.assertTrue(contract.validate_text("concept", text + "\n## Scope\n- x\n", self.manifest))

    def test_marker_version_and_identity_are_rejected(self):
        text = self.template("concept")
        self.assertTrue(contract.validate_text("concept", text.replace("1.0.0", "9.0.0"), self.manifest))
        self.assertTrue(contract.validate_text("concept", text.replace("artifact=concept", "artifact=changelog"), self.manifest))

    def test_frontmatter_and_field_enums_are_rejected(self):
        acceptance = self.template("acceptance").replace("状态: draft", "状态: closed")
        self.assertTrue(contract.validate_text("acceptance", acceptance, self.manifest))
        plan = self.template("tech_plan").replace("方案状态: draft", "方案状态: maybe")
        self.assertTrue(contract.validate_text("tech_plan", plan, self.manifest))

    def test_fixed_table_header_is_rejected(self):
        text = self.template("verify_report").replace("| Evidence ID | AC | 强度 | Outcome | Record |", "| ID | AC | Record |")
        self.assertTrue(contract.validate_text("verify_report", text, self.manifest))

    def test_manifest_has_unique_paths_templates_and_phases(self):
        specs = list(self.manifest["artifacts"].values())
        self.assertEqual(len(specs), len({item["path"] for item in specs}))
        self.assertEqual(len(specs), len({item["template"] for item in specs}))
        self.assertEqual({"P1", "P2", "P3", "P5", "close"}, {item["phase"] for item in specs})


if __name__ == "__main__":
    unittest.main()
