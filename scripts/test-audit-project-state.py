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

AUDITOR = Path(__file__).with_name("audit-project-state.py")
SPEC = importlib.util.spec_from_file_location("audit_project_state", AUDITOR)
assert SPEC and SPEC.loader
AUDIT_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT_MODULE
SPEC.loader.exec_module(AUDIT_MODULE)


class StateAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        (self.root / ".ai").mkdir(parents=True)
        self.write_active_state()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_active_state(self) -> None:
        (self.root / ".ai" / "ITERATIONS.md").write_text(
            "# iterations\n\ncurrent: ITER-0002\n\n"
            "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            "| ITER-0002 | current | active | 2026-01-02 | — | MILE-0001 | — |\n"
            "| ITER-0001 | old | closed | 2026-01-01 | 2026-01-01 | MILE-0001 | deliveries/ITER-0001-old.md |\n",
            encoding="utf-8",
        )
        (self.root / ".ai" / "MILESTONES.md").write_text(
            "# milestones\n\ncurrent: MILE-0001\n\n"
            "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n"
            "|---|---|---|---|---|---|---|\n"
            "| MILE-0001 | m | active | 2026-01-01 | — | ITER-0001, ITER-0002 | — |\n",
            encoding="utf-8",
        )
        (self.root / ".ai" / "MILESTONE.md").write_text(
            "| 路线项 | 主题 | 实际 ITER | 状态 |\n|---|---|---|---|\n"
            "| R1 | old | ITER-0001 | closed |\n| R2 | current | ITER-0002 | active |\n",
            encoding="utf-8",
        )
        for name in ("task-state.md", "02_SESSION_HANDOFF.md"):
            (self.root / ".ai" / name).write_text("ITER-0002 active\n", encoding="utf-8")
        archive = self.root / ".ai" / "iterations" / "ITER-0001"
        archive.mkdir(parents=True)
        for name in ("CONCEPT.md", "AC_LIST.md", "TECH_PLAN.md", "VERIFY_REPORT.md", "CHANGELOG.md"):
            (archive / name).write_text(f"# {name}\n", encoding="utf-8")
        deliveries = self.root / "deliveries"
        deliveries.mkdir()
        (deliveries / "ITER-0001-old.md").write_text("# delivery\n", encoding="utf-8")

    def invoke(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(AUDITOR), "--project-root", str(self.root), *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_active_project_is_read_only_and_passes(self) -> None:
        ledger = self.root / ".ai" / "ITERATIONS.md"
        ledger.write_text(ledger.read_text().replace("| current |", "| on|off contract |"))
        before = self.snapshot()
        result = self.invoke()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_current_and_multiple_active_drift_are_reported(self) -> None:
        path = self.root / ".ai" / "ITERATIONS.md"
        text = path.read_text(encoding="utf-8").replace(
            "| ITER-0001 | old | closed |", "| ITER-0001 | old | active |"
        )
        path.write_text(text, encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("iterations.single_active", result.stdout)
        self.assertIn("iterations.current", result.stdout)

    def test_missing_closed_delivery_and_archive_are_reported(self) -> None:
        (self.root / "deliveries" / "ITER-0001-old.md").unlink()
        (self.root / ".ai" / "iterations" / "ITER-0001" / "AC_LIST.md").unlink()
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("ITER-0001.delivery", result.stdout)
        self.assertIn("ITER-0001.archive", result.stdout)

    def test_milestone_route_status_drift_is_reported(self) -> None:
        path = self.root / ".ai" / "MILESTONE.md"
        path.write_text(path.read_text().replace("ITER-0002 | active", "ITER-0002 | closed"))
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("route.R2", result.stdout)

    def test_active_milestone_requires_workspace(self) -> None:
        (self.root / ".ai" / "MILESTONE.md").unlink()
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("milestones.workspace", result.stdout)

    def test_runtime_pointer_drift_is_reported(self) -> None:
        (self.root / ".ai" / "task-state.md").write_text("ITER-9999 active\n")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn(".ai/task-state.md", result.stdout)

    def test_release_metadata_and_unreleased_state_are_explicit(self) -> None:
        (self.root / "plugins" / "butler" / ".codex-plugin").mkdir(parents=True)
        (self.root / "migrations").mkdir()
        (self.root / "VERSION").write_text("1.2.3\n")
        (self.root / "plugins" / "butler" / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"version": "1.2.3"}), encoding="utf-8"
        )
        (self.root / "CHANGELOG.md").write_text("## [1.2.3] - today\n")
        (self.root / "migrations" / "v1.2.3.md").write_text("# migration\n")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "initial"], cwd=self.root, check=True)
        subprocess.run(["git", "tag", "v1.2.3"], cwd=self.root, check=True)
        self.assertEqual(0, self.invoke().returncode)
        (self.root / "unreleased.txt").write_text("x")
        blocked = self.invoke()
        self.assertEqual(1, blocked.returncode)
        allowed = self.invoke("--allow-unreleased")
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        self.assertIn("UNRELEASED", allowed.stdout)

    def test_evidence_index_requires_valid_archive_and_fold_receipt(self) -> None:
        archive = self.root / ".ai" / "iterations" / "ITER-0001"
        (archive / "VERIFY_REPORT.md").write_text(
            "# Evidence Index\n\n"
            "| ID | Record |\n|---|---|\n"
            "| proof | `.ai/iterations/ITER-0001/evidence/proof/record.json` |\n",
            encoding="utf-8",
        )
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("ITER-0001.evidence_hashes", result.stdout)
        self.assertIn("ITER-0001.fold_receipt", result.stdout)

    def test_evidence_pointer_outside_index_does_not_count(self) -> None:
        archive = self.root / ".ai" / "iterations" / "ITER-0001"
        (archive / "VERIFY_REPORT.md").write_text(
            "# Verification Results\n\n"
            "`.ai/iterations/ITER-0001/evidence/proof/record.json`\n\n"
            "# Evidence Index\n\n| ID | Record |\n|---|---|\n",
            encoding="utf-8",
        )
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("Evidence Index 无 record 指针", result.stdout)

    def test_fold_receipt_schema_version_is_checked(self) -> None:
        archive = self.root / ".ai" / "iterations" / "ITER-0001"
        (archive / "VERIFY_REPORT.md").write_text("# Evidence Index\n", encoding="utf-8")
        project = self.root / ".ai" / "project"
        project.mkdir()
        (project / "fold-state.json").write_text(
            json.dumps({"schema_version": 2, "receipts": {"ITER-0001": {}}}),
            encoding="utf-8",
        )
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("fold-state schema_version 必须为 1", result.stdout)

    def test_only_latest_receipt_topic_hash_tracks_current_file(self) -> None:
        project = self.root / ".ai" / "project"
        project.mkdir()
        topic = project / "capabilities.md"
        topic.write_text("# current\n", encoding="utf-8")
        archive1 = self.root / ".ai" / "iterations" / "ITER-0001"
        archive2 = self.root / ".ai" / "iterations" / "ITER-0002"
        archive2.mkdir()
        changelog1 = archive1 / "CHANGELOG.md"
        changelog2 = archive2 / "CHANGELOG.md"
        changelog2.write_text("# second\n", encoding="utf-8")
        fold = {
            "schema_version": 1,
            "receipts": {
                "ITER-0001": {
                    "changelog": {"path": ".ai/iterations/ITER-0001/CHANGELOG.md", "sha256": hashlib.sha256(changelog1.read_bytes()).hexdigest()},
                    "topics": [{"path": ".ai/project/capabilities.md", "sha256": hashlib.sha256(b"# old\n").hexdigest()}],
                },
                "ITER-0002": {
                    "changelog": {"path": ".ai/iterations/ITER-0002/CHANGELOG.md", "sha256": hashlib.sha256(changelog2.read_bytes()).hexdigest()},
                    "topics": [{"path": ".ai/project/capabilities.md", "sha256": hashlib.sha256(topic.read_bytes()).hexdigest()}],
                },
            },
        }
        (project / "fold-state.json").write_text(json.dumps(fold), encoding="utf-8")

        audit = AUDIT_MODULE.Audit(self.root, False)
        audit.audit_fold_receipt("ITER-0001", archive1)
        self.assertTrue(audit.findings[-1].ok)
        self.assertIn("historical-snapshot", audit.findings[-1].detail)

        topic.write_text("# drift\n", encoding="utf-8")
        audit.audit_fold_receipt("ITER-0002", archive2)
        self.assertFalse(audit.findings[-1].ok)
        self.assertIn("topic SHA-256 不符", audit.findings[-1].detail)

    def test_valid_evidence_index_and_fold_receipt_pass(self) -> None:
        archive = self.root / ".ai" / "iterations" / "ITER-0001"
        evidence = archive / "evidence" / "proof"
        evidence.mkdir(parents=True)
        stdout = b"ok\n"
        stderr = b""
        (evidence / "stdout.log").write_bytes(stdout)
        (evidence / "stderr.log").write_bytes(stderr)
        record = {
            "schema_version": 1,
            "evidence_id": "proof",
            "iteration": "ITER-0001",
            "ac_ids": ["AC1"],
            "command": {"argv": ["python3", "-m", "unittest"], "cwd": "."},
            "started_at": "2026-01-01T00:00:00.000Z",
            "finished_at": "2026-01-01T00:00:01.000Z",
            "duration_ms": 1000,
            "process_exit_code": 0,
            "outcome": "passed",
            "stdout": {"path": "stdout.log", "bytes": 3, "captured_bytes": 3, "sha256": hashlib.sha256(stdout).hexdigest(), "truncated": False},
            "stderr": {"path": "stderr.log", "bytes": 0, "captured_bytes": 0, "sha256": hashlib.sha256(stderr).hexdigest(), "truncated": False},
        }
        (evidence / "record.json").write_text(json.dumps(record), encoding="utf-8")
        diagnostic = archive / "evidence" / "diagnostic"
        diagnostic.mkdir()
        (diagnostic / "stdout.log").write_bytes(stdout)
        (diagnostic / "stderr.log").write_bytes(stderr)
        failed_record = dict(record)
        failed_record.update(
            {"evidence_id": "diagnostic", "process_exit_code": 7, "outcome": "failed"}
        )
        (diagnostic / "record.json").write_text(json.dumps(failed_record), encoding="utf-8")
        (archive / "VERIFY_REPORT.md").write_text(
            "# AC Status\n- [x] AC1 (auto·可靠) ✓\n\n# Evidence Index\n"
            "| ID | AC | Record |\n|---|---|---|\n"
            "| proof | AC1 | `.ai/iterations/ITER-0001/evidence/proof/record.json` |\n"
            "| diagnostic | AC1 | `.ai/iterations/ITER-0001/evidence/diagnostic/record.json` |\n",
            encoding="utf-8",
        )
        project = self.root / ".ai" / "project"
        project.mkdir()
        topic = project / "capabilities.md"
        topic.write_text("# capabilities\n", encoding="utf-8")
        changelog = archive / "CHANGELOG.md"
        fold = {
            "schema_version": 1,
            "receipts": {
                "ITER-0001": {
                    "changelog": {"path": ".ai/iterations/ITER-0001/CHANGELOG.md", "sha256": hashlib.sha256(changelog.read_bytes()).hexdigest()},
                    "topics": [{"path": ".ai/project/capabilities.md", "sha256": hashlib.sha256(topic.read_bytes()).hexdigest()}],
                }
            },
        }
        (project / "fold-state.json").write_text(json.dumps(fold), encoding="utf-8")
        result = self.invoke()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("保留非通过记录=['diagnostic']", result.stdout)

    def snapshot(self) -> dict[str, str]:
        return {
            str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.root.rglob("*")
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
