#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("goal.py")
spec = importlib.util.spec_from_file_location("goal_assurance", MODULE_PATH)
goal = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(goal)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fixture(root: Path) -> None:
    write(root / ".ai/ITERATIONS.md", "current: ITER-0001\n| ITER-0001 | x | active | 2026-01-01 | — | — | — |\n")
    write(root / ".ai/AC_LIST.md", "---\n状态: ack-frozen\n---\n- [ ] AC1：one\n- [ ] AC2：two\n")
    write(root / ".ai/TECH_PLAN.md", "---\n方案状态: pass\n---\n")
    write(root / ".ai/task-state.md", "# Goal Calibration\n| ID | Signal | Fact Source | Goal Impact | Route | Status |\n|---|---|---|---|---|---|\n\nN/A\n")
    verify = """# AC Status
- [x] AC1 (auto·可靠) ✓ ok
- [x] AC2 (auto·可靠) ✓ ok
# Evidence Index
| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| `proof` | AC1–AC2 | captured | passed | `.ai/iterations/ITER-0001/evidence/proof/record.json` |
# Completion Inputs
- Review Verdict: pass
- Completion Blockers: none
"""
    write(root / ".ai/VERIFY_REPORT.md", verify)
    directory = root / ".ai/verification-evidence/proof"
    out, err = b"ok\n", b""
    write(directory / "stdout.log", out.decode())
    write(directory / "stderr.log", "")
    record = {
        "schema_version": 1, "evidence_id": "proof", "iteration": "ITER-0001",
        "outcome": "passed", "ac_ids": ["AC1", "AC2"],
        "stdout": {"path": "stdout.log", "bytes": len(out), "captured_bytes": len(out), "sha256": hashlib.sha256(out).hexdigest(), "truncated": False},
        "stderr": {"path": "stderr.log", "bytes": len(err), "captured_bytes": len(err), "sha256": hashlib.sha256(err).hexdigest(), "truncated": False},
    }
    write(directory / "record.json", json.dumps(record))


class GoalAdjudicatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        fixture(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_ineligible(self, check: str) -> None:
        result = goal.evaluate(self.root)
        self.assertEqual("ineligible", result["verdict"])
        self.assertTrue(any(reason.startswith(check + ":") for reason in result["reasons"]))

    def test_positive_eligible(self) -> None:
        self.assertEqual("eligible", goal.evaluate(self.root)["verdict"])

    def test_gfc_001_plan_revise(self) -> None:
        write(self.root / ".ai/TECH_PLAN.md", "方案状态: revise\n")
        self.assert_ineligible("plan_passed")

    def test_gfc_002_goal_outcome_missing_ac(self) -> None:
        write(self.root / ".ai/AC_LIST.md", "状态: ack-frozen\n- [ ] AC1：one\n- [ ] AC2：two\n- [ ] AC3：missing\n")
        self.assert_ineligible("acceptance_passed")

    def test_gfc_003_reported_without_evidence(self) -> None:
        (self.root / ".ai/verification-evidence/proof/record.json").unlink()
        self.assert_ineligible("evidence_valid")

    def test_gfc_004_review_must_fix(self) -> None:
        path = self.root / ".ai/VERIFY_REPORT.md"
        write(path, path.read_text().replace("Review Verdict: pass", "Review Verdict: must-fix"))
        self.assert_ineligible("review_passed")

    def test_gfc_005_blocking_risk(self) -> None:
        path = self.root / ".ai/VERIFY_REPORT.md"
        write(path, path.read_text().replace("Completion Blockers: none", "Completion Blockers: present"))
        self.assert_ineligible("completion_blockers_clear")

    def test_gfc_006_scope_drift_open(self) -> None:
        path = self.root / ".ai/task-state.md"
        write(path, path.read_text() + "| CAL-001 | scope-drift | diff | at-risk | P2 | open |\n")
        self.assert_ineligible("calibration_clear")

    def test_gfc_007_host_complete_cannot_override_failed_ac(self) -> None:
        path = self.root / ".ai/VERIFY_REPORT.md"
        write(path, path.read_text().replace("- [x] AC2", "- [ ] AC2"))
        self.assert_ineligible("acceptance_passed")

    def test_gfc_008_tasks_done_cannot_override_pending_ac(self) -> None:
        path = self.root / ".ai/VERIFY_REPORT.md"
        write(path, path.read_text().replace("- [x] AC1", "- [ ] AC1"))
        self.assert_ineligible("acceptance_passed")

    def test_unknown_review_fails_closed(self) -> None:
        path = self.root / ".ai/VERIFY_REPORT.md"
        write(path, path.read_text().replace("Review Verdict: pass", "Review Verdict: maybe"))
        self.assert_ineligible("review_passed")

    def test_cli_exit_codes_and_json(self) -> None:
        result = subprocess.run([sys.executable, str(MODULE_PATH), "evaluate", "--project-root", str(self.root)], text=True, capture_output=True)
        self.assertEqual(0, result.returncode)
        self.assertEqual("eligible", json.loads(result.stdout)["verdict"])

    def test_read_only(self) -> None:
        before = {p.relative_to(self.root): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob("*") if p.is_file()}
        goal.evaluate(self.root)
        after = {p.relative_to(self.root): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_fixture_matches_real_evidence_v1_shape(self) -> None:
        record = json.loads((self.root / ".ai/verification-evidence/proof/record.json").read_text())
        self.assertIn("stdout", record)
        self.assertIn("stderr", record)
        self.assertNotIn("streams", record)


if __name__ == "__main__":
    unittest.main()
