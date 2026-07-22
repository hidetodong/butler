from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
CLI = REPO / "tools" / "prd-update" / "prd_update.py"
STATUS = REPO / "tools" / "prd-status" / "prd_status.py"
TARGET_ID = "2026-07-22-alpha"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_symlink():
            digest.update(b"L" + os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
        else:
            digest.update(b"D")
    return digest.hexdigest()


def requirement_index(prd_id: str, version: str, modules: list[tuple[str, str]]) -> str:
    rows = "\n".join(f"| {slug} | {title} | {version} | {version} | active |" for slug, title in modules)
    return f"""# {prd_id}

## Requirement Identity

- prd_id: {prd_id}
- current_version: {version}
- status: active

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
{rows}

## Workspace Scope

- primary_write: [web]
- supporting_write: []
- read_only: [contracts]
- excluded: [admin]
"""


def ac_ref(prd_id: str, version: str, modules: str) -> str:
    return f"""---
状态: ack-frozen
ACK 日期: 2026-07-22
prd_refs:
  - prd_id: {prd_id}
    prd_version: {version}
    module_slugs: [{modules}]
---
# AC
"""


def make_project(base: Path) -> tuple[Path, Path]:
    root = base / "project"
    prd = root / ".ai" / "references" / "prd"
    target = prd / TARGET_ID
    other_id = "2026-07-23-beta"
    other = prd / other_id
    target.mkdir(parents=True)
    other.mkdir()
    project = root / ".ai" / "project"
    project.mkdir()
    (project / "workspaces.md").write_text(
        "# Workspaces\n\n| workspace_key | package_identity | path | kind | status | evidence |\n|---|---|---|---|---|---|\n"
        "| web | web | apps/web | app | active | manifest |\n"
        "| contracts | contracts | packages/contracts | library | active | manifest |\n"
        "| admin | admin | apps/admin | app | active | manifest |\n",
        encoding="utf-8",
    )
    (prd / "00_INDEX.md").write_text(
        "# PRD Collection\n\n| prd_id | 标题 | 当前版本 | 状态 | 来源线索 | 入口 |\n|---|---|---|---|---|---|\n"
        f"| {TARGET_ID} | Alpha | v1.0 | active | SRC-1 | {TARGET_ID}/00_INDEX.md |\n"
        f"| {other_id} | Beta | v3.0 | active | SRC-2 | {other_id}/00_INDEX.md |\n",
        encoding="utf-8",
    )
    (target / "00_INDEX.md").write_text(requirement_index(TARGET_ID, "v1.0", [("flow", "Flow"), ("old-only", "Old only")]), encoding="utf-8")
    (target / "flow.md").write_bytes(b"old flow\n")
    (target / "old-only.md").write_bytes(b"old only\n")
    (other / "00_INDEX.md").write_text(requirement_index(other_id, "v3.0", [("flow", "Other flow")]), encoding="utf-8")
    (other / "flow.md").write_bytes(b"other untouched\n")
    (root / ".ai" / "AC_LIST.md").write_text(ac_ref(TARGET_ID, "v1.0", "flow"), encoding="utf-8")
    (root / ".ai" / "ITERATIONS.md").write_text(
        "current: ITER-0099\n\n| 迭代号 | 标题 | 状态 |\n|---|---|---|\n| ITER-0001 | Closed | closed |\n| ITER-0099 | Active | active |\n",
        encoding="utf-8",
    )
    closed = root / ".ai" / "iterations" / "ITER-0001"
    closed.mkdir(parents=True)
    (closed / "AC_LIST.md").write_text(ac_ref(TARGET_ID, "v1.0", "old-only"), encoding="utf-8")
    (root / ".ai" / "MILESTONE.md").write_text(f"| R1 | Future → prd: {TARGET_ID}#flow | — | planned |\n", encoding="utf-8")
    incoming = root / "incoming"
    incoming.mkdir()
    (incoming / "flow.md").write_bytes(b"new flow exact\n")
    (incoming / "extra.md").write_bytes(b"new extra exact\n")
    spec = root / "update.json"
    write_spec(spec, confirmed=True, complete_dispositions=True)
    return root, spec


def write_spec(path: Path, *, confirmed: bool, complete_dispositions: bool, mutate: dict | None = None) -> None:
    dispositions = []
    if complete_dispositions:
        dispositions = [
            {"path": ".ai/MILESTONE.md#R1", "decision": "use-new-on-start", "note": "future adopts v1.1"},
            {"path": ".ai/AC_LIST.md", "decision": "keep-pinned", "note": "active remains pinned until amend"},
            {"path": ".ai/iterations/ITER-0001/AC_LIST.md", "decision": "keep-pinned-history", "note": "closed stays v1.0"},
        ]
    value = {
        "schema_version": 1,
        "prd_id": TARGET_ID,
        "expected_old_version": "v1.0",
        "new_version": "v1.1",
        "confirmed": confirmed,
        "confirmation": {"mode": "user-ack" if confirmed else "pending", "at": "2026-07-22T10:00:00+08:00" if confirmed else None},
        "active_modules": [
            {"module_slug": "flow", "title": "Flow renamed", "source": "incoming/flow.md", "origins": ["flow"]},
            {"module_slug": "extra", "title": "Extra", "source": "incoming/extra.md", "origins": []},
        ],
        "removed_slugs": ["old-only"],
        "dispositions": dispositions,
    }
    if mutate:
        value.update(mutate)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PrdUpdateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root, self.spec = make_project(Path(self.temp.name))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, action: str, *args: str, env: dict[str, str] | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
        command = [sys.executable, str(CLI), action, "--project-root", str(self.root), *args]
        merged = os.environ.copy()
        if env:
            merged.update(env)
        result = subprocess.run(command, text=True, capture_output=True, check=False, env=merged)
        return result, json.loads(result.stdout)

    def apply(self, env: dict[str, str] | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
        return self.run_cli("apply", "--spec", str(self.spec), "--now", "2026-07-22T10:01:00+08:00", env=env)

    def test_plan_is_zero_write_and_reports_changes_impacts_and_dispositions(self) -> None:
        before = tree_hash(self.root)
        result, payload = self.run_cli("plan", "--spec", str(self.spec))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(payload["apply_ready"])
        self.assertEqual({item["kind"] for item in payload["module_changes"]}, {"updated", "added", "removed"})
        self.assertEqual({item["state"] for item in payload["impact"]}, {"future", "active", "closed"})
        self.assertEqual(payload["missing_dispositions"], [])
        self.assertEqual(before, tree_hash(self.root))

    def test_pending_plan_is_exit_one_and_apply_rejects_without_writes(self) -> None:
        write_spec(self.spec, confirmed=False, complete_dispositions=False)
        before = tree_hash(self.root)
        result, payload = self.run_cli("plan", "--spec", str(self.spec))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["apply_ready"])
        self.assertEqual(len(payload["missing_dispositions"]), 3)
        result, payload = self.apply()
        self.assertEqual(result.returncode, 2)
        self.assertIn("not apply-ready", payload["error"])
        self.assertEqual(before, tree_hash(self.root))

    def test_apply_archives_then_updates_indexes_receipt_and_leaves_other_prd_untouched(self) -> None:
        other = self.root / ".ai/references/prd/2026-07-23-beta"
        other_before = tree_hash(other)
        result, payload = self.apply()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(payload["changed"])
        target = self.root / ".ai/references/prd" / TARGET_ID
        self.assertEqual((target / ".archive/v1.0/flow.md").read_bytes(), b"old flow\n")
        self.assertEqual((target / ".archive/v1.0/old-only.md").read_bytes(), b"old only\n")
        self.assertEqual((target / "flow.md").read_bytes(), b"new flow exact\n")
        self.assertEqual((target / "extra.md").read_bytes(), b"new extra exact\n")
        self.assertIn("| old-only | Old only | v1.0 | v1.1 | removed |", (target / "00_INDEX.md").read_text(encoding="utf-8"))
        self.assertIn(f"| {TARGET_ID} | Alpha | v1.1 |", (self.root / ".ai/references/prd/00_INDEX.md").read_text(encoding="utf-8"))
        self.assertEqual(other_before, tree_hash(other))
        receipt = json.loads((self.root / payload["receipt"]).read_text(encoding="utf-8"))
        self.assertEqual(receipt["dispositions"][0]["state"], "active")
        self.assertEqual({item["state"] for item in receipt["impact"]}, {"future", "active", "closed"})

    def test_status_projects_latest_receipt_read_only(self) -> None:
        result, applied = self.apply()
        self.assertEqual(result.returncode, 0)
        before = tree_hash(self.root)
        status = subprocess.run([sys.executable, str(STATUS), "status", "--project-root", str(self.root), "--prd-id", TARGET_ID], text=True, capture_output=True, check=False)
        self.assertEqual(status.returncode, 0, status.stdout)
        latest = json.loads(status.stdout)["requirements"][0]["latest_update"]
        self.assertEqual(latest["update_id"], applied["update_id"])
        self.assertEqual(latest["new_version"], "v1.1")
        self.assertEqual(before, tree_hash(self.root))

    def test_repeat_apply_is_idempotent_and_verify_passes(self) -> None:
        first_result, first = self.apply()
        self.assertEqual(first_result.returncode, 0)
        before = tree_hash(self.root)
        second_result, second = self.apply()
        self.assertEqual(second_result.returncode, 0, second_result.stdout)
        self.assertFalse(second["changed"])
        self.assertEqual(first["update_id"], second["update_id"])
        self.assertEqual(before, tree_hash(self.root))
        verified, payload = self.run_cli("verify", "--prd-id", TARGET_ID)
        self.assertEqual(verified.returncode, 0)
        self.assertTrue(payload["verified"])

    def test_rollback_restores_exact_collection_and_rejects_post_update_drift(self) -> None:
        prd = self.root / ".ai/references/prd"
        before = tree_hash(prd)
        result, _ = self.apply()
        self.assertEqual(result.returncode, 0)
        (prd / TARGET_ID / "flow.md").write_text("drift\n", encoding="utf-8")
        result, payload = self.run_cli("rollback", "--prd-id", TARGET_ID)
        self.assertEqual(result.returncode, 2)
        self.assertIn("post hash", payload["error"])
        (prd / TARGET_ID / "flow.md").write_bytes(b"new flow exact\n")
        result, payload = self.run_cli("rollback", "--prd-id", TARGET_ID)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["restored_version"], "v1.0")
        self.assertEqual(before, tree_hash(prd))

    def test_all_transaction_failure_points_restore_exact_collection(self) -> None:
        for point in ("after_archive", "after_live", "after_index", "after_receipt", "after_first_rename", "after_second_rename"):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as temp:
                root, spec = make_project(Path(temp))
                before = tree_hash(root / ".ai/references/prd")
                result = subprocess.run(
                    [sys.executable, str(CLI), "apply", "--project-root", str(root), "--spec", str(spec), "--now", "2026-07-22T10:01:00+08:00"],
                    text=True, capture_output=True, check=False,
                    env={**os.environ, "BUTLER_PRD_UPDATE_FAIL_AT": point},
                )
                self.assertEqual(result.returncode, 2, (point, result.stdout))
                self.assertEqual(before, tree_hash(root / ".ai/references/prd"), point)
                references = root / ".ai/references"
                self.assertFalse((references / ".prd-update.lock").exists())
                self.assertEqual(list(references.glob(".prd-update-stage-*")), [])
                backups = references / ".prd-update-backups"
                self.assertFalse(backups.exists() and any(backups.iterdir()))

    def test_lock_conflict_and_tampered_receipt_backup_fail_closed(self) -> None:
        lock = self.root / ".ai/references/.prd-update.lock"
        lock.write_text("held\n", encoding="utf-8")
        before = tree_hash(self.root / ".ai/references/prd")
        result, payload = self.apply()
        self.assertEqual(result.returncode, 2)
        self.assertIn("holds the lock", payload["error"])
        self.assertEqual(before, tree_hash(self.root / ".ai/references/prd"))
        lock.unlink()
        result, applied = self.apply()
        self.assertEqual(result.returncode, 0)
        receipt_path = self.root / applied["receipt"]
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["backup"] = "../../outside"
        hash_input = dict(receipt)
        hash_input.pop("receipt_payload_sha256")
        receipt["receipt_payload_sha256"] = "sha256:" + hashlib.sha256(json.dumps(hash_input, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result, payload = self.run_cli("verify", "--prd-id", TARGET_ID)
        self.assertEqual(result.returncode, 2)
        self.assertIn("backup", payload["error"])

    def test_receipt_payload_tamper_and_invalid_now_fail_closed(self) -> None:
        result, applied = self.apply()
        self.assertEqual(result.returncode, 0)
        receipt_path = self.root / applied["receipt"]
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["new_version"] = "v9.9"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        result, payload = self.run_cli("verify", "--prd-id", TARGET_ID)
        self.assertEqual(result.returncode, 2)
        self.assertIn("payload hash", payload["error"])

        with tempfile.TemporaryDirectory() as temp:
            root, spec = make_project(Path(temp))
            before = tree_hash(root / ".ai/references/prd")
            invalid = subprocess.run(
                [sys.executable, str(CLI), "apply", "--project-root", str(root), "--spec", str(spec), "--now", "not-a-time"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("ISO-8601", json.loads(invalid.stdout)["error"])
            self.assertEqual(before, tree_hash(root / ".ai/references/prd"))

    def test_milestone_impacts_are_classified_per_route(self) -> None:
        (self.root / ".ai/MILESTONE.md").write_text(
            f"| R1 | Future → prd: {TARGET_ID}#flow | — | planned |\n"
            f"| R2 | Finished → prd: {TARGET_ID}#flow | — | closed |\n",
            encoding="utf-8",
        )
        value = json.loads(self.spec.read_text(encoding="utf-8"))
        value["dispositions"].append(
            {"path": ".ai/MILESTONE.md#R2", "decision": "keep-pinned-history", "note": "closed route stays v1.0"}
        )
        self.spec.write_text(json.dumps(value), encoding="utf-8")
        result, payload = self.run_cli("plan", "--spec", str(self.spec))
        self.assertEqual(result.returncode, 0, result.stdout)
        routes = {item["path"]: item["state"] for item in payload["impact"] if "MILESTONE.md#" in item["path"]}
        self.assertEqual(routes, {".ai/MILESTONE.md#R1": "future", ".ai/MILESTONE.md#R2": "closed"})

    def test_rollback_failure_restores_updated_collection_exactly(self) -> None:
        result, _ = self.apply()
        self.assertEqual(result.returncode, 0)
        prd = self.root / ".ai/references/prd"
        updated = tree_hash(prd)
        result, payload = self.run_cli(
            "rollback", "--prd-id", TARGET_ID,
            env={"BUTLER_PRD_UPDATE_FAIL_AT": "rollback_after_first_rename"},
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("injected failure", payload["error"])
        self.assertEqual(updated, tree_hash(prd))

    def test_invalid_one_to_one_new_slug_rename_is_rejected(self) -> None:
        value = json.loads(self.spec.read_text(encoding="utf-8"))
        value["active_modules"] = [
            {"module_slug": "flow", "title": "Flow", "source": "incoming/flow.md", "origins": ["flow"]},
            {"module_slug": "new-name", "title": "Renamed old", "source": "incoming/extra.md", "origins": ["old-only"]},
        ]
        value["removed_slugs"] = []
        self.spec.write_text(json.dumps(value), encoding="utf-8")
        before = tree_hash(self.root)
        result, payload = self.run_cli("plan", "--spec", str(self.spec))
        self.assertEqual(result.returncode, 2)
        self.assertIn("rename must preserve", payload["error"])
        self.assertEqual(before, tree_hash(self.root))


if __name__ == "__main__":
    unittest.main()
