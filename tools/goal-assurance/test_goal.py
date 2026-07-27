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
EVIDENCE_TOOL = MODULE_PATH.parent.parent / "verification-evidence" / "evidence.py"
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

    def add_evidence(self, evidence_id: str, outcome: str, ac_ids: list[str]) -> None:
        directory = self.root / ".ai" / "verification-evidence" / evidence_id
        out, err = b"diagnostic\n", b""
        write(directory / "stdout.log", out.decode())
        write(directory / "stderr.log", "")
        record = {
            "schema_version": 1, "evidence_id": evidence_id, "iteration": "ITER-0001",
            "outcome": outcome, "ac_ids": ac_ids,
            "stdout": {"path": "stdout.log", "bytes": len(out), "captured_bytes": len(out), "sha256": hashlib.sha256(out).hexdigest(), "truncated": False},
            "stderr": {"path": "stderr.log", "bytes": len(err), "captured_bytes": len(err), "sha256": hashlib.sha256(err).hexdigest(), "truncated": False},
        }
        write(directory / "record.json", json.dumps(record))
        verify = self.root / ".ai" / "VERIFY_REPORT.md"
        write(
            verify,
            verify.read_text().replace(
                "# Completion Inputs",
                f"| `{evidence_id}` | diagnostic | captured | {outcome} | `.ai/iterations/ITER-0001/evidence/{evidence_id}/record.json` |\n# Completion Inputs",
            ),
        )

    def add_tdd_pair(self) -> None:
        command = [
            sys.executable,
            "-c",
            "from pathlib import Path; p=Path('tdd.flag'); seen=p.exists(); p.write_text('x'); raise SystemExit(0 if seen else 1)",
        ]
        argv_json = json.dumps(command, separators=(",", ":"))
        write(
            self.root / ".ai/TECH_PLAN.md",
            "---\n方案状态: pass\n---\n\n## Test Strategy\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            f"| goal-gate | AC1,AC2 | `{argv_json}` | `.` |\n",
        )
        for phase, expected in (("red", 1), ("green", 0)):
            result = subprocess.run(
                [
                    sys.executable,
                    str(EVIDENCE_TOOL),
                    "run",
                    "--project-root",
                    str(self.root),
                    "--iteration",
                    "ITER-0001",
                    "--id",
                    f"tdd-goal-gate-{phase}",
                    "--ac",
                    "AC1,AC2",
                    "--",
                    *command,
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        verify = self.root / ".ai/VERIFY_REPORT.md"
        rows = (
            "| `tdd-goal-gate-red` | AC1–AC2 | captured | failed | "
            "`.ai/iterations/ITER-0001/evidence/tdd-goal-gate-red/record.json` |\n"
            "| `tdd-goal-gate-green` | AC1–AC2 | captured | passed | "
            "`.ai/iterations/ITER-0001/evidence/tdd-goal-gate-green/record.json` |\n"
        )
        write(verify, verify.read_text().replace("# Completion Inputs", rows + "# Completion Inputs"))

    def test_positive_eligible(self) -> None:
        self.assertEqual("eligible", goal.evaluate(self.root)["verdict"])

    def test_declared_tdd_without_pair_is_ineligible(self) -> None:
        write(
            self.root / ".ai/TECH_PLAN.md",
            "---\n方案状态: pass\n---\n\n## Test Strategy\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            "| goal-gate | AC1,AC2 | `[\"python3\",\"-m\",\"pytest\"]` | `.` |\n",
        )
        self.assert_ineligible("tdd_pairs_valid")

    def test_declared_tdd_with_valid_pair_is_eligible(self) -> None:
        self.add_tdd_pair()
        result = goal.evaluate(self.root)
        self.assertEqual("eligible", result["verdict"], result)
        check = next(item for item in result["checks"] if item["id"] == "tdd_pairs_valid")
        self.assertTrue(check["passed"])
        self.assertIn("[OK] goal-gate", check["detail"])

    def test_declared_tdd_with_drifted_pair_is_ineligible(self) -> None:
        self.add_tdd_pair()
        (self.root / ".ai/verification-evidence/tdd-goal-gate-green").rename(
            self.root / ".ai/verification-evidence/tdd-goal-gate-green-missing"
        )
        self.assert_ineligible("tdd_pairs_valid")

    def test_failed_diagnostic_is_retained_but_later_passed_proof_still_closes(self) -> None:
        self.add_evidence("failed-first", "failed", ["AC1", "AC2"])
        result = goal.evaluate(self.root)
        self.assertEqual("eligible", result["verdict"], result)
        evidence = next(item for item in result["checks"] if item["id"] == "evidence_valid")
        self.assertIn("failed-first", evidence["detail"])

    def test_failed_diagnostic_never_contributes_ac_coverage(self) -> None:
        record = self.root / ".ai" / "verification-evidence" / "proof" / "record.json"
        data = json.loads(record.read_text())
        data["outcome"] = "failed"
        write(record, json.dumps(data))
        result = goal.evaluate(self.root)
        self.assertEqual("ineligible", result["verdict"])
        evidence_valid = next(item for item in result["checks"] if item["id"] == "evidence_valid")
        coverage = next(item for item in result["checks"] if item["id"] == "evidence_covers_ac")
        self.assertTrue(evidence_valid["passed"])
        self.assertFalse(coverage["passed"])

    def test_unknown_evidence_outcome_fails_closed(self) -> None:
        record = self.root / ".ai" / "verification-evidence" / "proof" / "record.json"
        data = json.loads(record.read_text())
        data["outcome"] = "maybe"
        write(record, json.dumps(data))
        self.assert_ineligible("evidence_valid")

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
