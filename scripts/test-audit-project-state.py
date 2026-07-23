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

    def test_v2_index_routes_audit_across_cold_shards(self) -> None:
        hot = self.root / ".ai" / "ITERATIONS.md"
        text = hot.read_text(encoding="utf-8")
        old_row = "| ITER-0001 | old | closed | 2026-01-01 | 2026-01-01 | MILE-0001 | deliveries/ITER-0001-old.md |"
        hot.write_text(text.replace(old_row + "\n", ""), encoding="utf-8")
        shard = self.root / ".ai/history/iterations/ITER-000001-000050.md"
        shard.parent.mkdir(parents=True)
        shard.write_text(
            "# ITER cold ledger · 1–50\n\n"
            "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
            "|---|---|---|---|---|---|---|\n" + old_row + "\n",
            encoding="utf-8",
        )
        (self.root / ".ai/state-index.json").write_text(
            json.dumps({
                "schema_version": 2,
                "shard_size": 50,
                "ledgers": {
                    "iterations": {"routing": {
                        "scheme": "fixed-range-v1", "directory": ".ai/history/iterations",
                        "prefix": "ITER", "minimum_width": 6, "receipt_suffix": ".json",
                    }},
                    "milestones": {"routing": {
                        "scheme": "fixed-range-v1", "directory": ".ai/history/milestones",
                        "prefix": "MILE", "minimum_width": 6, "receipt_suffix": ".json",
                    }},
                },
            }),
            encoding="utf-8",
        )
        audit = AUDIT_MODULE.Audit(self.root, False)
        combined = audit.ledger_text(".ai/ITERATIONS.md", ".ai/history/ITERATIONS.cold.md")
        self.assertIn(old_row, combined)

    def test_v2_index_rejects_shard_path_escape(self) -> None:
        (self.root / ".ai/state-index.json").write_text(
            json.dumps({
                "schema_version": 2,
                "shard_size": 50,
                "ledgers": {
                    "iterations": {"routing": {
                        "scheme": "fixed-range-v1", "directory": ".ai/history/escape",
                        "prefix": "ITER", "minimum_width": 6, "receipt_suffix": ".json",
                    }},
                    "milestones": {"routing": {}},
                },
            }),
            encoding="utf-8",
        )
        audit = AUDIT_MODULE.Audit(self.root, False)
        with self.assertRaises(AUDIT_MODULE.AuditError):
            audit.ledger_text(".ai/ITERATIONS.md", ".ai/history/ITERATIONS.cold.md")

    def test_current_and_multiple_active_drift_are_reported(self) -> None:
        path = self.root / ".ai" / "ITERATIONS.md"
        text = path.read_text(encoding="utf-8").replace(
            "| ITER-0001 | old | closed |", "| ITER-0001 | old | active |"
        )
        path.write_text(text, encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)

    def test_noncanonical_zero_identity_is_reported(self) -> None:
        path = self.root / ".ai" / "ITERATIONS.md"
        path.write_text(path.read_text().replace("ITER-0001", "ITER-0000"), encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("iterations.ids", result.stdout)
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

    def test_milestone_numbers_must_be_contiguous(self) -> None:
        path = self.root / ".ai" / "MILESTONES.md"
        path.write_text(path.read_text().replace("MILE-0001", "MILE-0002"), encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("milestones.sequence", result.stdout)

    def test_malformed_formal_milestone_id_is_reported_without_crashing(self) -> None:
        milestone = self.root / ".ai" / "MILESTONES.md"
        milestone.write_text(milestone.read_text().replace("MILE-0001", "MILE-draft"), encoding="utf-8")
        iterations = self.root / ".ai" / "ITERATIONS.md"
        iterations.write_text(iterations.read_text().replace("MILE-0001", "MILE-draft"), encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("milestones.ids", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_valid_unnumbered_milestone_backlog_passes(self) -> None:
        ledger = self.root / ".ai" / "MILESTONES.md"
        ledger.write_text(
            ledger.read_text()
            + "\n## 待办区（未编号）\n\n"
            + "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n"
            + "|---|---|---|---|---|\n"
            + "| future-goal | later | 2026-01-02 | .ai/milestone-backlog/future-goal.md | defer |\n",
            encoding="utf-8",
        )
        backlog = self.root / ".ai" / "milestone-backlog"
        backlog.mkdir()
        (backlog / "future-goal.md").write_text(
            "---\n候办键: future-goal\n候办状态: deferred\n---\n", encoding="utf-8"
        )
        result = self.invoke()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_multiple_backlog_directions_use_separate_rows_and_files(self) -> None:
        ledger = self.root / ".ai" / "MILESTONES.md"
        ledger.write_text(
            ledger.read_text()
            + "\n## 待办区（未编号）\n\n"
            + "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n"
            + "|---|---|---|---|---|\n"
            + "| search-redesign | search | 2026-01-02 | .ai/milestone-backlog/search-redesign.md | defer |\n"
            + "| billing-cleanup | billing | 2026-01-02 | .ai/milestone-backlog/billing-cleanup.md | defer |\n",
            encoding="utf-8",
        )
        backlog = self.root / ".ai" / "milestone-backlog"
        backlog.mkdir()
        for slug in ("search-redesign", "billing-cleanup"):
            (backlog / f"{slug}.md").write_text(
                f"---\n候办键: {slug}\n候办状态: deferred\n---\n# {slug}\n", encoding="utf-8"
            )
        result = self.invoke()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_backlog_draft_identity_must_be_unique_and_match_filename(self) -> None:
        ledger = self.root / ".ai" / "MILESTONES.md"
        ledger.write_text(
            ledger.read_text()
            + "\n## 待办区（未编号）\n\n"
            + "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n"
            + "|---|---|---|---|---|\n"
            + "| search-redesign | search | 2026-01-02 | .ai/milestone-backlog/search-redesign.md | defer |\n",
            encoding="utf-8",
        )
        backlog = self.root / ".ai" / "milestone-backlog"
        backlog.mkdir()
        draft = backlog / "search-redesign.md"
        invalid_bodies = (
            "---\n候办键: search-redesign\n候办键: billing-cleanup\n候办状态: deferred\n---\n",
            "---\n候办键: billing-cleanup\n候办状态: deferred\n---\n",
            "---\n候办键: search-redesign\n候办状态: deferred\n候办状态: deferred\n---\n",
        )
        for body in invalid_bodies:
            with self.subTest(body=body):
                draft.write_text(body, encoding="utf-8")
                result = self.invoke()
                self.assertEqual(1, result.returncode)
                self.assertIn("backlog.search-redesign.markers", result.stdout)

    def test_milestone_backlog_missing_and_orphan_drafts_are_reported(self) -> None:
        ledger = self.root / ".ai" / "MILESTONES.md"
        ledger.write_text(
            ledger.read_text()
            + "\n## 待办区（未编号）\n\n"
            + "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n"
            + "|---|---|---|---|---|\n"
            + "| missing | later | 2026-01-02 | .ai/milestone-backlog/missing.md | defer |\n",
            encoding="utf-8",
        )
        backlog = self.root / ".ai" / "milestone-backlog"
        backlog.mkdir()
        (backlog / "orphan.md").write_text("---\n候办键: orphan\n候办状态: deferred\n---\n", encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("backlog.missing.draft", result.stdout)
        self.assertIn("milestones.backlog_set", result.stdout)

    def test_milestone_backlog_cannot_masquerade_as_formal_number(self) -> None:
        ledger = self.root / ".ai" / "MILESTONES.md"
        ledger.write_text(
            ledger.read_text()
            + "\n## 待办区（未编号）\n\n"
            + "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |\n"
            + "|---|---|---|---|---|\n"
            + "| mile-0002 | later | 2026-01-02 | .ai/milestone-backlog/mile-0002.md | defer |\n",
            encoding="utf-8",
        )
        backlog = self.root / ".ai" / "milestone-backlog"
        backlog.mkdir()
        (backlog / "mile-0002.md").write_text(
            "---\n候办键: mile-0002\n候办状态: deferred\n---\n", encoding="utf-8"
        )
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("backlog.mile-0002.slug", result.stdout)

    def test_milestone_backlog_contract_is_wired_to_both_hosts(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        schema = (repo / "Coder/20_Workflow_Lifecycle/milestone-schema.md").read_text(encoding="utf-8")
        command = (repo / ".claude/commands/butler/milestone.md").read_text(encoding="utf-8")
        skill = (repo / "plugins/butler/skills/butler-milestone/SKILL.md").read_text(encoding="utf-8")
        for text in (schema, command, skill):
            self.assertIn(".ai/milestone-backlog/", text)
            self.assertIn("start <候办键>", text)
        self.assertIn("一方向一文件", schema)
        self.assertIn("一方向一个候办键", command)
        self.assertIn("exactly one direction", skill)
        self.assertIn("开启前退回", schema)
        self.assertIn("no linked iteration, archive, or delivery", skill)

    def test_runtime_pointer_drift_is_reported(self) -> None:
        (self.root / ".ai" / "task-state.md").write_text("ITER-9999 active\n")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn(".ai/task-state.md", result.stdout)

    def test_handoff_receipt_is_checked_when_present(self) -> None:
        task = self.root / ".ai" / "task-state.md"
        task.write_text(
            "- 当前迭代：ITER-0002\n- 当前里程碑：MILE-0001\n- 阶段：P1 Analysis\n"
            "- 状态：active\n- 下一动作：继续。\n",
            encoding="utf-8",
        )
        (self.root / ".ai" / "CONCEPT.md").write_text("# Current Understanding\n- x\n", encoding="utf-8")
        tool = AUDITOR.parent.parent / "tools" / "handoff" / "handoff.py"
        synced = subprocess.run(
            [sys.executable, str(tool), "sync", "--project-root", str(self.root)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, synced.returncode, synced.stdout + synced.stderr)
        self.assertEqual(0, self.invoke().returncode)
        task.write_text(task.read_text().replace("继续", "改变"), encoding="utf-8")
        result = self.invoke()
        self.assertEqual(1, result.returncode)
        self.assertIn("handoff.freshness", result.stdout)

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
        subprocess.run(["git", "add", "unreleased.txt"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "after release"], cwd=self.root, check=True)
        clean_but_ahead = self.invoke()
        self.assertEqual(1, clean_but_ahead.returncode)
        self.assertIn("不指向 HEAD", clean_but_ahead.stdout)
        allowed_ahead = self.invoke("--allow-unreleased")
        self.assertEqual(0, allowed_ahead.returncode, allowed_ahead.stdout + allowed_ahead.stderr)
        self.assertIn("UNRELEASED", allowed_ahead.stdout)

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
            "## AC Status\n- [x] AC1 (auto·可靠) ✓\n\n## Evidence Index\n"
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
