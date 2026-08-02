from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).resolve().parents[1] / "decision_map.py"


class DecisionMapCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-decision-cli-")
        self.root = Path(self.temp.name)
        (self.root / ".ai").mkdir()
        self.documents = self.root / "documents"
        self.documents.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def document(self, name: str, value: dict) -> Path:
        path = self.documents / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def run_cli(self, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run([sys.executable, str(CLI), *args], text=True, capture_output=True)
        self.assertEqual("", result.stderr)
        lines = result.stdout.splitlines()
        self.assertEqual(1, len(lines), result.stdout)
        return result, json.loads(lines[0])

    @staticmethod
    def tree_digest(root: Path) -> str:
        digest = hashlib.sha256()
        for path in sorted(root.rglob("*")):
            digest.update(path.relative_to(root).as_posix().encode())
            if path.is_file():
                digest.update(path.read_bytes())
        return digest.hexdigest()

    def test_four_action_cli_and_cross_process_recovery(self) -> None:
        spec = self.document("create.json", {"schema_version": 1, "operation_id": "OP-create", "operation": {"kind": "create_map", "title": "Map", "destination": "Destination"}})
        before = self.tree_digest(self.root)
        plan_result, planned = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(spec), "--now", "2026-08-01T00:00:00Z")
        self.assertEqual(0, plan_result.returncode)
        self.assertEqual(before, self.tree_digest(self.root))
        plan_path = self.document("plan.json", planned)
        applied_result, applied = self.run_cli("apply", "--project-root", str(self.root), "--plan", str(plan_path), "--now", "2026-08-01T00:00:01Z")
        self.assertEqual(0, applied_result.returncode)
        self.assertEqual(1, applied["revision"])

        inspect_result, inspected = self.run_cli("inspect", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--now", "2026-08-01T00:00:02Z")
        self.assertEqual(0, inspect_result.returncode)
        self.assertEqual("DMAP-0001", inspected["state"]["map_id"])
        verify_result, verified = self.run_cli("verify", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--now", "2026-08-01T00:00:02Z")
        self.assertEqual(0, verify_result.returncode)
        self.assertEqual("ok", verified["status"])

    def test_conflict_and_bad_input_have_stable_exit_codes(self) -> None:
        create = self.document("create.json", {"schema_version": 1, "operation_id": "OP-create", "operation": {"kind": "create_map", "title": "Map", "destination": "Destination"}})
        _, planned = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(create))
        plan_path = self.document("create-plan.json", planned)
        self.run_cli("apply", "--project-root", str(self.root), "--plan", str(plan_path))

        other = self.document("other.json", {"schema_version": 1, "operation_id": "OP-create-2", "operation": {"kind": "create_map", "title": "Other", "destination": "Other"}})
        conflict_result, conflict = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(other))
        self.assertEqual(1, conflict_result.returncode)
        self.assertEqual("map_exists", conflict["code"])

        bad = self.document("bad.json", {"schema_version": 1, "operation_id": "OP-bad", "operation": {"kind": "unknown"}})
        bad_result, bad_output = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(bad))
        self.assertEqual(2, bad_result.returncode)
        self.assertEqual("invalid_operation", bad_output["code"])

    def test_apply_stale_plan_and_idempotent_retry(self) -> None:
        create = self.document("create.json", {"schema_version": 1, "operation_id": "OP-create", "operation": {"kind": "create_map", "title": "Map", "destination": "Destination"}})
        _, created_plan = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(create))
        created_plan_path = self.document("created-plan.json", created_plan)
        self.run_cli("apply", "--project-root", str(self.root), "--plan", str(created_plan_path))

        first = self.document("first.json", {"schema_version": 1, "operation_id": "OP-first", "operation": {"kind": "add_fog", "fog_id": "FOG-0001", "description": "First"}})
        second = self.document("second.json", {"schema_version": 1, "operation_id": "OP-second", "operation": {"kind": "add_fog", "fog_id": "FOG-0002", "description": "Second"}})
        _, first_plan = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(first))
        _, second_plan = self.run_cli("plan", "--project-root", str(self.root), "--map-id", "DMAP-0001", "--spec", str(second))
        first_path = self.document("first-plan.json", first_plan)
        second_path = self.document("second-plan.json", second_plan)
        _, first_apply = self.run_cli("apply", "--project-root", str(self.root), "--plan", str(first_path))
        _, retry = self.run_cli("apply", "--project-root", str(self.root), "--plan", str(first_path))
        self.assertEqual(first_apply["revision"], retry["revision"])
        self.assertTrue(retry["idempotent"])
        stale_result, stale = self.run_cli("apply", "--project-root", str(self.root), "--plan", str(second_path))
        self.assertEqual(1, stale_result.returncode)
        self.assertEqual("stale_plan", stale["code"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
