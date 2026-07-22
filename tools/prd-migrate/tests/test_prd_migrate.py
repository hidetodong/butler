from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "prd_migrate.py"
SPEC = importlib.util.spec_from_file_location("prd_migrate", MODULE_PATH)
assert SPEC and SPEC.loader
prd_migrate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prd_migrate)

PRD_ID = "2026-07-22-user-login"
NOW = "2026-07-22T12:00:00+08:00"


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_symlink(): digest.update(b"L" + str(path.readlink()).encode())
        elif path.is_file(): digest.update(b"F" + path.read_bytes())
    return digest.hexdigest()


class PrdMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.prd = self.root / ".ai/references/prd"
        self.prd.mkdir(parents=True)
        (self.prd / "00_INDEX.md").write_text("# Login PRD\n\n当前版本: v1.1\n", encoding="utf-8")
        (self.prd / "login-flow.md").write_bytes(b"live login\r\n")
        archive = self.prd / ".archive/v1.0"
        archive.mkdir(parents=True)
        (archive / "00_INDEX.md").write_text("当前版本: v1.0\n", encoding="utf-8")
        (archive / "login-flow.md").write_bytes(b"old login\n")
        (self.root / ".ai/iterations/ITER-0001").mkdir(parents=True)
        (self.root / ".ai/iterations/ITER-0001/AC_LIST.md").write_text(
            "---\nprd_version: v1.0\n---\n.ai/references/prd/login-flow.md\n", encoding="utf-8"
        )
        (self.root / ".ai/MILESTONE.md").write_text("| R1 | 登录 → prd: login-flow |\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, dict]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = prd_migrate.main(list(args))
        return code, json.loads(output.getvalue())

    def apply(self) -> dict:
        code, result = self.run_cli("apply", "--project-root", str(self.root), "--prd-id", PRD_ID, "--title", "用户登录", "--now", NOW)
        self.assertEqual(0, code, result)
        return result

    def test_inspect_and_plan_are_zero_write(self) -> None:
        before = tree_digest(self.root)
        code, inspected = self.run_cli("inspect", "--project-root", str(self.root))
        self.assertEqual(0, code); self.assertEqual("legacy", inspected["state"])
        code, plan = self.run_cli("plan", "--project-root", str(self.root), "--prd-id", PRD_ID, "--title", "用户登录")
        self.assertEqual(0, code); self.assertEqual("v1.1", plan["current_version"])
        self.assertEqual("milestone", plan["impact"][0]["group"])
        self.assertEqual(["login-flow"], plan["impact"][0]["route_slugs"])
        self.assertEqual("closed-history", plan["impact"][1]["group"])
        self.assertEqual(before, tree_digest(self.root))

    def test_bold_and_table_index_versions_are_supported(self) -> None:
        index = self.prd / "00_INDEX.md"
        index.write_text("**当前版本**：**v1.1**\n", encoding="utf-8")
        self.assertEqual("v1.1", prd_migrate.index_version(index))
        index.write_text("| Current Version | v1.1 |\n", encoding="utf-8")
        self.assertEqual("v1.1", prd_migrate.index_version(index))
        index.write_text("# PRD 知识文件夹索引 · AI信控助手 V1.1.0\n\n| slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |\n", encoding="utf-8")
        self.assertEqual("v1.1.0", prd_migrate.index_version(index))
        index.write_text("# PRD 知识文件夹索引 · AI信控助手 V1.1.0\n\n- **源**：doc version **28**，产品版本 V1.1.0\n- 改版：doc version 20 → 28\n", encoding="utf-8")
        self.assertEqual("v28", prd_migrate.index_version(index))

    def test_legacy_doc_revision_pin_without_dot_is_supported(self) -> None:
        ac = self.root / ".ai/iterations/ITER-0001/AC_LIST.md"
        ac.write_text("---\nprd_version: v28\n---\n.ai/references/prd/login-flow.md\n", encoding="utf-8")
        (self.prd / "00_INDEX.md").write_text("# Login V28\n", encoding="utf-8")
        code, result = self.run_cli("resolve", "--project-root", str(self.root), "--ac-file", ".ai/iterations/ITER-0001/AC_LIST.md", "--ref", "prd/login-flow.md")
        self.assertEqual(0, code, result)
        self.assertEqual("v28", result["prd_version"])

    def test_apply_verify_idempotent_and_history_zero_write(self) -> None:
        history = self.root / ".ai/iterations/ITER-0001/AC_LIST.md"
        before = history.read_bytes()
        result = self.apply()
        self.assertTrue(result["changed"])
        self.assertTrue((self.prd / PRD_ID / "login-flow.md").is_file())
        self.assertEqual(b"live login\r\n", (self.prd / PRD_ID / "login-flow.md").read_bytes())
        self.assertEqual(before, history.read_bytes())
        code, verified = self.run_cli("verify", "--project-root", str(self.root))
        self.assertEqual(0, code); self.assertTrue(verified["verified"])
        repeated = self.apply()
        self.assertFalse(repeated["changed"])

    def test_legacy_reference_resolves_before_and_after_migration(self) -> None:
        ac = ".ai/iterations/ITER-0001/AC_LIST.md"
        args = ("resolve", "--project-root", str(self.root), "--ac-file", ac, "--ref", "prd/login-flow.md")
        code, old = self.run_cli(*args)
        self.assertEqual(0, code); self.assertEqual(".ai/references/prd/.archive/v1.0/login-flow.md", old["path"])
        self.apply()
        code, migrated = self.run_cli(*args)
        self.assertEqual(0, code); self.assertEqual(f".ai/references/prd/{PRD_ID}/.archive/v1.0/login-flow.md", migrated["path"])

    def test_collection_prd_refs_resolve_independent_versions(self) -> None:
        self.apply()
        second = self.prd / "2026-07-23-batch-import"
        second.mkdir()
        (second / "00_INDEX.md").write_text("当前版本: v2.0\n", encoding="utf-8")
        (second / "import-rules.md").write_text("rules", encoding="utf-8")
        ac = self.root / ".ai/AC_LIST.md"
        ac.write_text(
            "---\nprd_refs:\n"
            f"  - prd_id: {PRD_ID}\n    prd_version: v1.1\n    module_slugs: [login-flow]\n"
            "  - prd_id: 2026-07-23-batch-import\n    prd_version: v2.0\n    module_slugs: [import-rules]\n"
            "---\n", encoding="utf-8",
        )
        code, result = self.run_cli("resolve", "--project-root", str(self.root), "--ac-file", ".ai/AC_LIST.md", "--ref", "prd/2026-07-23-batch-import/import-rules.md")
        self.assertEqual(0, code); self.assertEqual("v2.0", result["prd_version"])

    def test_invalid_identity_mixed_layout_and_symlink_reject(self) -> None:
        code, result = self.run_cli("plan", "--project-root", str(self.root), "--prd-id", "2026-02-30-bad", "--title", "Bad")
        self.assertEqual(2, code); self.assertIn("calendar", result["error"])
        (self.prd / PRD_ID).mkdir()
        code, result = self.run_cli("plan", "--project-root", str(self.root), "--prd-id", PRD_ID, "--title", "Bad")
        self.assertEqual(2, code); self.assertIn("mixed", result["error"])
        (self.prd / PRD_ID).rmdir()
        outside = self.root / "outside"; outside.write_text("x", encoding="utf-8")
        (self.prd / "link.md").symlink_to(outside)
        code, result = self.run_cli("inspect", "--project-root", str(self.root))
        self.assertEqual(2, code); self.assertIn("symlink", result["error"])

    def test_apply_failure_after_backup_restores_legacy(self) -> None:
        real_replace = prd_migrate.os.replace
        calls = 0

        def fail_stage(source, target):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("injected switch failure")
            return real_replace(source, target)

        with mock.patch.object(prd_migrate.os, "replace", side_effect=fail_stage):
            code, result = self.run_cli("apply", "--project-root", str(self.root), "--prd-id", PRD_ID, "--title", "用户登录", "--now", NOW)
        self.assertEqual(2, code); self.assertIn("injected", result["error"])
        self.assertEqual("legacy", prd_migrate.layout(self.root)["state"])
        self.assertTrue((self.prd / "login-flow.md").is_file())

    def test_rollback_refuses_drift_then_restores_exact_legacy(self) -> None:
        before = tree_digest(self.prd)
        self.apply()
        target = self.prd / PRD_ID / "login-flow.md"
        target.write_text("drift", encoding="utf-8")
        code, result = self.run_cli("rollback", "--project-root", str(self.root))
        self.assertEqual(2, code); self.assertIn("drift", result["error"])
        target.write_bytes(b"live login\r\n")
        code, result = self.run_cli("rollback", "--project-root", str(self.root))
        self.assertEqual(0, code); self.assertEqual("legacy", result["state"])
        self.assertEqual(before, tree_digest(self.prd))

    def test_malformed_or_unpinned_prd_refs_fail_closed(self) -> None:
        self.apply()
        ac = self.root / ".ai/AC_LIST.md"
        ac.write_text(f"---\nprd_refs:\n  - prd_id: {PRD_ID}\n    prd_version: v1.1\n    module_slugs: []\n---\n", encoding="utf-8")
        code, result = self.run_cli("resolve", "--project-root", str(self.root), "--ac-file", ".ai/AC_LIST.md", "--ref", f"prd/{PRD_ID}/login-flow.md")
        self.assertEqual(2, code); self.assertIn("module_slugs", result["error"])
        ac.write_text(
            f"---\nprd_refs:\n  - prd_id: {PRD_ID}\n    prd_version: v1.1\n    unexpected: yes\n    module_slugs: [login-flow]\n---\n",
            encoding="utf-8",
        )
        code, result = self.run_cli("resolve", "--project-root", str(self.root), "--ac-file", ".ai/AC_LIST.md", "--ref", f"prd/{PRD_ID}/login-flow.md")
        self.assertEqual(2, code); self.assertIn("prd_refs", result["error"])

    def test_tampered_receipt_paths_cannot_escape_project(self) -> None:
        self.apply()
        receipt_path = self.prd / prd_migrate.RECEIPT
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["backup"] = "../../outside"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        code, result = self.run_cli("rollback", "--project-root", str(self.root))
        self.assertEqual(2, code); self.assertIn("unsafe", result["error"])
        self.assertTrue(self.prd.is_dir())

    def test_post_switch_verification_failure_restores_legacy(self) -> None:
        with mock.patch.object(prd_migrate, "verify", side_effect=prd_migrate.MigrationError("injected verify failure")):
            code, result = self.run_cli("apply", "--project-root", str(self.root), "--prd-id", PRD_ID, "--title", "用户登录", "--now", NOW)
        self.assertEqual(2, code); self.assertIn("injected", result["error"])
        self.assertEqual("legacy", prd_migrate.layout(self.root)["state"])
        self.assertTrue((self.prd / "login-flow.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
