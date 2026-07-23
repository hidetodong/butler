import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("contract_generator", ROOT / "contract.py")
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class ArtifactGeneratorTests(unittest.TestCase):
    def project(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".ai").mkdir()
        return temporary, root

    def test_render_replaces_slots(self):
        text = contract.render(ROOT, "concept", "ITER-1234", "Title")
        self.assertIn("ITER-1234 · Title", text)
        self.assertNotIn("{{", text)

    def test_init_is_idempotent_and_never_overwrites(self):
        temporary, root = self.project()
        first = contract.generate(root, ROOT, "concept", "ITER-1234", "T", "init", "P1", False, False)
        before = (root / ".ai/CONCEPT.md").read_bytes()
        second = contract.generate(root, ROOT, "concept", "ITER-1234", "changed", "init", "P1", False, False)
        self.assertTrue(first["changed"])
        self.assertFalse(second["changed"])
        self.assertEqual(before, (root / ".ai/CONCEPT.md").read_bytes())
        temporary.cleanup()

    def test_dry_run_is_zero_write(self):
        temporary, root = self.project()
        result = contract.generate(root, ROOT, "acceptance", "ITER-1234", "", "init", "P2", True, False)
        self.assertTrue(result["changed"])
        self.assertFalse((root / ".ai/AC_LIST.md").exists())
        temporary.cleanup()

    def test_reset_requires_force(self):
        temporary, root = self.project()
        target = root / ".ai/CONCEPT.md"
        target.write_text("user content", encoding="utf-8")
        with self.assertRaises(contract.ContractError):
            contract.generate(root, ROOT, "concept", "ITER-1234", "", "reset", "P1", False, False)
        self.assertEqual("user content", target.read_text())
        result = contract.generate(root, ROOT, "concept", "ITER-1234", "", "reset", "P1", False, True)
        self.assertTrue(result["changed"])
        temporary.cleanup()

    def test_downstream_generation_is_rejected(self):
        temporary, root = self.project()
        with self.assertRaises(contract.ContractError):
            contract.generate(root, ROOT, "verify_report", "ITER-1234", "", "init", "P3", False, False)
        temporary.cleanup()

    def test_atomic_write_failure_leaves_original(self):
        temporary, root = self.project()
        target = root / ".ai/x.md"
        target.write_text("old", encoding="utf-8")
        def fail(source, destination):
            raise OSError("injected")
        with self.assertRaises(OSError):
            contract.atomic_write(target, "new", replace=fail)
        self.assertEqual("old", target.read_text())
        self.assertEqual(["x.md"], [path.name for path in target.parent.iterdir()])
        temporary.cleanup()

    def test_check_skips_legacy_and_rejects_strict_drift(self):
        temporary, root = self.project()
        target = root / ".ai/CONCEPT.md"
        target.write_text("# legacy\n", encoding="utf-8")
        self.assertEqual("legacy", contract.check_artifact(root, ROOT, "concept")["status"])
        target.write_text(contract.render(ROOT, "concept", "ITER-1234", "T").replace("## Scope", "## Changed"), encoding="utf-8")
        self.assertEqual("drift", contract.check_artifact(root, ROOT, "concept")["status"])
        temporary.cleanup()

    def test_project_check_reports_missing_and_valid_files(self):
        temporary, root = self.project()
        result = contract.check_project(root, ROOT)
        self.assertEqual("drift", result["status"])
        for name, spec in contract.load_manifest(ROOT)["artifacts"].items():
            target = root / spec["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(contract.render(ROOT, name, "ITER-1234", "T"), encoding="utf-8")
        self.assertEqual("ok", contract.check_project(root, ROOT)["status"])
        temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
