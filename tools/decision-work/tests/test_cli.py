from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from common import Harness


CLI = Path(__file__).resolve().parents[1] / "decision_work.py"


class DecisionWorkCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.h = Harness()
        self.docs = tempfile.TemporaryDirectory(prefix="butler-decision-work-cli-")
        self.doc_root = Path(self.docs.name)

    def tearDown(self) -> None:
        self.docs.cleanup()
        self.h.close()

    def run_cli(self, *args: str, expected: int = 0) -> dict:
        result = subprocess.run(["python3", str(CLI), *args], text=True, capture_output=True, check=False)
        self.assertEqual(expected, result.returncode, result.stderr or result.stdout)
        value = json.loads(result.stdout)
        self.assertIsInstance(value, dict)
        return value

    def write(self, name: str, value: dict) -> Path:
        path = self.doc_root / name
        path.write_text(json.dumps(value))
        return path

    def test_cross_process_prepare_record_inspect_verify(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        prepare = self.h.work_spec("prepare_attempts", {"work_type": "research", "attempts": [{"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "serial"}]})
        planned = self.run_cli("plan", "--project-root", str(self.h.root), "--map-id", self.h.map_id, "--spec", str(self.write("prepare.json", prepare)), "--now", "2026-08-01T01:01:00Z")
        self.run_cli("apply", "--project-root", str(self.h.root), "--plan", str(self.write("prepare-plan.json", planned)), "--now", "2026-08-01T01:01:00Z")
        inspected = self.run_cli("inspect", "--project-root", str(self.h.root), "--map-id", self.h.map_id, "--decision-id", "DEC-0001", "--attempt-id", "ATT-0001", "--now", "2026-08-01T01:02:00Z")
        task = inspected["attempts"][0]["task"]
        import hashlib
        task_sha = "sha256:" + hashlib.sha256((json.dumps(task, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()).hexdigest()
        record = self.h.work_spec("record_result", {"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "task_sha256": task_sha, "result": self.h.candidate()})
        record_plan = self.run_cli("plan", "--project-root", str(self.h.root), "--map-id", self.h.map_id, "--spec", str(self.write("record.json", record)), "--now", "2026-08-01T01:02:00Z")
        self.run_cli("apply", "--project-root", str(self.h.root), "--plan", str(self.write("record-plan.json", record_plan)), "--now", "2026-08-01T01:02:00Z")
        verified = self.run_cli("verify", "--project-root", str(self.h.root), "--map-id", self.h.map_id, "--now", "2026-08-01T01:03:00Z")
        self.assertEqual("ok", verified["status"])
        self.assertEqual("candidate", verified["checked"][0]["derived"]["result_status"])

    def test_cli_reports_bad_input_as_single_json(self) -> None:
        bad = self.write("bad.json", {"schema_version": 1})
        result = self.run_cli("plan", "--project-root", str(self.h.root), "--map-id", self.h.map_id, "--spec", str(bad), expected=2)
        self.assertEqual("error", result["status"])
        self.assertIn("code", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
