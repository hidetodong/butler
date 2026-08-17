import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("migration", ROOT / "migration.py")
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


class MigrationTests(unittest.TestCase):
    def project(self):
        temporary = tempfile.TemporaryDirectory(); root = Path(temporary.name); (root / ".ai").mkdir()
        (root / ".ai/ITERATIONS.md").write_text("current: ITER-1234\n")
        manifest = migration.contract.load_manifest(ROOT)
        for name, spec in manifest["artifacts"].items():
            text = migration.contract.render(ROOT, name, "ITER-1234", "T")
            text = migration.contract.MARKER_RE.sub("", text).replace("N/A", f"preserved-{name}", 1)
            (root / spec["path"]).write_text(text)
        return temporary, root

    def legacy_h1_project(self):
        temporary, root = self.project()
        manifest = migration.contract.load_manifest(ROOT)
        for name, spec in manifest["artifacts"].items():
            path = root / spec["path"]
            text = path.read_text()
            text = text.replace("## ", "# ")
            path.write_text(text)
        return temporary, root

    def test_plan_is_zero_write_and_apply_preserves_content(self):
        temporary, root = self.project(); before = {p.name:p.read_bytes() for p in (root/".ai").glob("*.md")}
        planned = migration.plan(root)[0]
        self.assertTrue(planned["apply_ready"]); self.assertEqual(before, {p.name:p.read_bytes() for p in (root/".ai").glob("*.md")})
        receipt = migration.apply(root)
        self.assertTrue(receipt["changed"])
        for item in receipt["items"]:
            text = (root / item["path"]).read_text(); self.assertIn("preserved-", text); self.assertIn("butler-artifact-template", text)
        self.assertEqual("ok", migration.verify(root, receipt["migration_id"])["status"])
        temporary.cleanup()

    def test_second_apply_is_idempotent(self):
        temporary, root = self.project(); migration.apply(root); result = migration.apply(root)
        self.assertFalse(result["changed"]); temporary.cleanup()

    def test_legacy_h1_sections_preserve_every_body(self):
        temporary, root = self.legacy_h1_project()
        before = {path.name: path.read_text() for path in (root / ".ai").glob("*.md")}
        receipt = migration.apply(root)
        for item in receipt["items"]:
            old = before[Path(item["path"]).name]
            new = (root / item["path"]).read_text()
            for token in re.findall(r"preserved-[a-z_]+", old):
                self.assertIn(token, new)
        temporary.cleanup()

    def test_rollback_can_be_reapplied_from_same_verified_backup(self):
        temporary, root = self.project(); receipt = migration.apply(root); mid = receipt["migration_id"]
        migration.rollback(root, mid)
        reapplied = migration.apply(root)
        self.assertEqual(mid, reapplied["migration_id"])
        self.assertEqual("ok", migration.verify(root, mid)["status"])
        temporary.cleanup()

    def test_unknown_and_duplicate_sections_fail_closed(self):
        for extra in ("\n## Unknown\n- x\n", "\n## Scope\n- duplicate\n"):
            temporary, root = self.project(); path = root/".ai/CONCEPT.md"; path.write_text(path.read_text()+extra)
            with self.assertRaises(migration.MigrationError): migration.plan(root)
            temporary.cleanup()

    def test_rollback_and_post_drift_gate(self):
        temporary, root = self.project(); original=(root/".ai/CONCEPT.md").read_bytes(); receipt=migration.apply(root); mid=receipt["migration_id"]
        migration.rollback(root, mid); self.assertEqual(original,(root/".ai/CONCEPT.md").read_bytes()); temporary.cleanup()
        temporary, root = self.project(); receipt=migration.apply(root); mid=receipt["migration_id"]; path=root/".ai/CONCEPT.md"; path.write_text(path.read_text()+"drift")
        with self.assertRaises(migration.MigrationError): migration.rollback(root, mid)
        temporary.cleanup()

    def test_strict_verify_missing_human_section_is_migrated(self):
        manifest = migration.contract.load_manifest(ROOT)
        text = migration.contract.render(ROOT, "verify_report", "ITER-1234", "T")
        old = text.replace(migration.HUMAN_TEST_SECTION, "")
        self.assertNotIn("## 人测道小结", old)
        migrated = migration.migrate_strict_verify(old, manifest)
        self.assertIn("## 人测道小结", migrated)
        self.assertEqual([], migration.contract.validate_text("verify_report", migrated, manifest))
        self.assertIn("## Verification Summary", migrated)
        self.assertIn("## Handoff / Next Step", migrated)

    def test_strict_verify_already_migrated_is_idempotent(self):
        manifest = migration.contract.load_manifest(ROOT)
        text = migration.contract.render(ROOT, "verify_report", "ITER-1234", "T")
        self.assertEqual(text, migration.migrate_strict_verify(text, manifest))

    def test_strict_verify_misplaced_human_section_is_rejected(self):
        manifest = migration.contract.load_manifest(ROOT)
        text = migration.contract.render(ROOT, "verify_report", "ITER-1234", "T")
        misplaced = text.replace(migration.HUMAN_TEST_SECTION, "") + "## 人测道小结\n\n- misplaced\n\n"
        with self.assertRaises(migration.MigrationError) as ctx:
            migration.migrate_strict_verify(misplaced, manifest)
        self.assertIn("misplaced or duplicate", str(ctx.exception))

    def test_strict_verify_duplicate_human_section_is_rejected(self):
        manifest = migration.contract.load_manifest(ROOT)
        text = migration.contract.render(ROOT, "verify_report", "ITER-1234", "T")
        duplicate = text + "## 人测道小结\n\n- duplicate\n\n"
        with self.assertRaises(migration.MigrationError) as ctx:
            migration.migrate_strict_verify(duplicate, manifest)
        self.assertIn("misplaced or duplicate", str(ctx.exception))

    def test_strict_verify_unknown_marker_is_rejected(self):
        manifest = migration.contract.load_manifest(ROOT)
        text = migration.contract.render(ROOT, "verify_report", "ITER-1234", "T")
        bad = text.replace("1.0.0", "9.0.0")
        with self.assertRaises(migration.MigrationError) as ctx:
            migration.migrate_strict_verify(bad, manifest)
        self.assertIn("marker", str(ctx.exception))


if __name__ == "__main__": unittest.main()
