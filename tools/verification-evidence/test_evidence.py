#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).with_name("evidence.py")


class EvidenceCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        (self.root / ".ai").mkdir(parents=True)
        (self.root / ".ai" / "ITERATIONS.md").write_text(
            "# iterations\n\ncurrent: ITER-0099\n\n"
            "| id | title | status |\n|---|---|---|\n| ITER-0099 | test | active |\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @property
    def hot(self) -> Path:
        return self.root / ".ai" / "verification-evidence"

    def invoke(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def run_evidence(
        self,
        evidence_id: str,
        command: list[str],
        *options: str,
    ) -> subprocess.CompletedProcess[str]:
        return self.invoke(
            "run",
            "--project-root",
            str(self.root),
            "--iteration",
            "ITER-0099",
            "--id",
            evidence_id,
            "--ac",
            "AC1,AC3",
            *options,
            "--",
            *command,
        )

    def record(self, evidence_id: str) -> dict:
        return json.loads((self.hot / evidence_id / "record.json").read_text(encoding="utf-8"))

    def write_tdd_plan(
        self,
        command: list[str] | None = None,
        *,
        cycle: str = "sample",
        ac: str = "AC1,AC3",
        cwd: str = ".",
    ) -> list[str]:
        actual = command or [
            sys.executable,
            "-c",
            "from pathlib import Path; p=Path('tdd.flag'); seen=p.exists(); p.write_text('x'); raise SystemExit(0 if seen else 1)",
        ]
        argv_json = json.dumps(actual, ensure_ascii=False, separators=(",", ":"))
        (self.root / ".ai" / "TECH_PLAN.md").write_text(
            "# TECH_PLAN — ITER-0099\n\n"
            "## Test Strategy\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            f"| {cycle} | {ac} | `{argv_json}` | `{cwd}` |\n",
            encoding="utf-8",
        )
        return actual

    def run_tdd_pair(self, command: list[str]) -> None:
        red = self.run_evidence("tdd-sample-red", command)
        green = self.run_evidence("tdd-sample-green", command)
        self.assertEqual(1, red.returncode, red.stdout + red.stderr)
        self.assertEqual(0, green.returncode, green.stdout + green.stderr)

    def check_tdd(self, source: str = "hot") -> subprocess.CompletedProcess[str]:
        return self.invoke(
            "check-tdd",
            "--project-root",
            str(self.root),
            "--iteration",
            "ITER-0099",
            "--source",
            source,
        )

    def write_record(self, evidence_id: str, record: dict) -> None:
        (self.hot / evidence_id / "record.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_success_captures_exact_argv_streams_hashes_and_verifies(self) -> None:
        command = [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"]
        result = self.run_evidence("unit", command)
        self.assertEqual(0, result.returncode, result.stderr)
        record = self.record("unit")
        self.assertEqual(command, record["command"]["argv"])
        self.assertEqual(".", record["command"]["cwd"])
        self.assertEqual(["AC1", "AC3"], record["ac_ids"])
        self.assertEqual("passed", record["outcome"])
        for name, expected in (("stdout", b"out\n"), ("stderr", b"err\n")):
            self.assertEqual(expected, (self.hot / "unit" / f"{name}.log").read_bytes())
            self.assertEqual(hashlib.sha256(expected).hexdigest(), record[name]["sha256"])
        verified = self.invoke(
            "verify", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(0, verified.returncode, verified.stdout + verified.stderr)

    def test_nonzero_process_is_preserved_as_failed_evidence(self) -> None:
        result = self.run_evidence("failure", [sys.executable, "-c", "raise SystemExit(7)"])
        self.assertEqual(1, result.returncode)
        record = self.record("failure")
        self.assertEqual(7, record["process_exit_code"])
        self.assertEqual("failed", record["outcome"])

    def test_timeout_kills_process_and_preserves_timeout_evidence(self) -> None:
        result = self.run_evidence(
            "timeout",
            [sys.executable, "-c", "import time; time.sleep(5)"],
            "--timeout",
            "0.05",
        )
        self.assertEqual(124, result.returncode)
        self.assertEqual("timeout", self.record("timeout")["outcome"])

    def test_output_over_limit_is_incomplete_not_passed(self) -> None:
        result = self.run_evidence(
            "large",
            [sys.executable, "-c", "print('x' * 100)"],
            "--max-output-bytes",
            "16",
        )
        self.assertEqual(3, result.returncode)
        stream = self.record("large")["stdout"]
        self.assertEqual(101, stream["bytes"])
        self.assertEqual(16, stream["captured_bytes"])
        self.assertTrue(stream["truncated"])
        self.assertEqual("incomplete", self.record("large")["outcome"])

    def test_launch_error_is_recorded_and_returns_tool_error(self) -> None:
        result = self.run_evidence("missing", ["definitely-not-a-real-command-xyz"])
        self.assertEqual(2, result.returncode)
        record = self.record("missing")
        self.assertEqual("launch_error", record["outcome"])
        self.assertIsNone(record["process_exit_code"])
        self.assertIn("launch_error", record)

    def test_invalid_or_duplicate_id_and_cwd_escape_are_rejected(self) -> None:
        success = self.run_evidence("once", [sys.executable, "-c", "pass"])
        self.assertEqual(0, success.returncode)
        duplicate = self.run_evidence("once", [sys.executable, "-c", "pass"])
        self.assertEqual(2, duplicate.returncode)
        invalid = self.run_evidence("../escape", [sys.executable, "-c", "pass"])
        self.assertEqual(2, invalid.returncode)
        escaped = self.run_evidence(
            "cwd-escape", [sys.executable, "-c", "pass"], "--cwd", ".."
        )
        self.assertEqual(2, escaped.returncode)
        self.assertFalse((self.root.parent / "escape").exists())

    def test_concurrent_same_id_has_one_winner(self) -> None:
        base = [
            sys.executable,
            str(TOOL),
            "run",
            "--project-root",
            str(self.root),
            "--iteration",
            "ITER-0099",
            "--id",
            "race",
            "--ac",
            "AC1",
            "--",
            sys.executable,
            "-c",
            "import time; time.sleep(0.2)",
        ]
        first = subprocess.Popen(base, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        second = subprocess.run(base, text=True, capture_output=True, check=False)
        first_stdout, first_stderr = first.communicate(timeout=2)
        results = sorted([first.returncode, second.returncode])
        self.assertEqual([0, 2], results, first_stdout + first_stderr + second.stdout + second.stderr)
        self.assertTrue((self.hot / "race" / "record.json").is_file())

    def test_tampering_is_detected(self) -> None:
        self.assertEqual(0, self.run_evidence("tamper", [sys.executable, "-c", "print('ok')"]).returncode)
        (self.hot / "tamper" / "stdout.log").write_text("no\n", encoding="utf-8")
        result = self.invoke(
            "verify", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("SHA-256", result.stdout)

    def test_boolean_exit_code_tampering_is_rejected(self) -> None:
        self.assertEqual(0, self.run_evidence("typed", [sys.executable, "-c", "pass"]).returncode)
        record_path = self.hot / "typed" / "record.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["outcome"] = "failed"
        record["process_exit_code"] = True
        record_path.write_text(json.dumps(record), encoding="utf-8")
        result = self.invoke(
            "verify", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("outcome", result.stdout)

    def test_symlinked_hot_root_and_extra_record_file_are_rejected(self) -> None:
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        self.hot.symlink_to(outside, target_is_directory=True)
        rejected = self.run_evidence("linked", [sys.executable, "-c", "pass"])
        self.assertEqual(2, rejected.returncode)
        self.hot.unlink()
        self.assertEqual(0, self.run_evidence("extra", [sys.executable, "-c", "pass"]).returncode)
        (self.hot / "extra" / "unexpected.txt").write_text("x")
        verified = self.invoke(
            "verify", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(1, verified.returncode)
        self.assertIn("文件集不符", verified.stdout)

    def test_archive_and_reopen_keep_exactly_one_source(self) -> None:
        self.assertEqual(0, self.run_evidence("archive", [sys.executable, "-c", "pass"]).returncode)
        archived = self.invoke(
            "archive", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(0, archived.returncode, archived.stdout + archived.stderr)
        archive_root = self.root / ".ai" / "iterations" / "ITER-0099" / "evidence"
        self.assertFalse(self.hot.exists())
        self.assertTrue((archive_root / "archive" / "record.json").is_file())
        verified = self.invoke(
            "verify",
            "--project-root",
            str(self.root),
            "--iteration",
            "ITER-0099",
            "--source",
            "archive",
        )
        self.assertEqual(0, verified.returncode)
        reopened = self.invoke(
            "reopen", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(0, reopened.returncode, reopened.stdout + reopened.stderr)
        self.assertTrue((self.hot / "archive" / "record.json").is_file())
        self.assertFalse(archive_root.exists())

    def test_closed_iteration_requires_explicit_allow_closed(self) -> None:
        ledger = self.root / ".ai/ITERATIONS.md"
        ledger.write_text(
            "# iterations\n\ncurrent: none\n\n"
            "| id | title | status |\n|---|---|---|\n| ITER-0099 | test | closed |\n",
            encoding="utf-8",
        )
        rejected = self.run_evidence("closed-denied", [sys.executable, "-c", "pass"])
        self.assertEqual(2, rejected.returncode)
        allowed = self.run_evidence(
            "closed-allowed", [sys.executable, "-c", "print('closed')"], "--allow-closed"
        )
        self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)
        archived = self.invoke(
            "archive", "--project-root", str(self.root), "--iteration", "ITER-0099", "--allow-closed"
        )
        self.assertEqual(0, archived.returncode, archived.stdout + archived.stderr)
        reopened = self.invoke(
            "reopen", "--project-root", str(self.root), "--iteration", "ITER-0099", "--allow-closed"
        )
        self.assertEqual(0, reopened.returncode, reopened.stdout + reopened.stderr)

    def test_tdd_pair_accepts_same_failed_then_passed_command(self) -> None:
        command = self.write_tdd_plan()
        self.run_tdd_pair(command)
        result = self.check_tdd()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("[OK] sample", result.stdout)

    def test_tdd_check_is_noop_without_declaration(self) -> None:
        (self.root / ".ai" / "TECH_PLAN.md").write_text(
            "# TECH_PLAN — ITER-0099\n\n## Test Strategy\n\n"
            "- 普通测试；文档可写 `<!-- butler-tdd-cycles: v1 -->` 说明格式，但这不算声明。\n",
            encoding="utf-8",
        )
        result = self.check_tdd()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("未声明 TDD cycle", result.stdout)
        self.assertFalse(self.hot.exists())

    def test_tdd_pair_rejects_missing_green(self) -> None:
        command = self.write_tdd_plan()
        red = self.run_evidence("tdd-sample-red", command)
        self.assertEqual(1, red.returncode)
        result = self.check_tdd()
        self.assertEqual(1, result.returncode)
        self.assertIn("缺少 Green evidence", result.stdout)

    def test_tdd_pair_rejects_missing_red_and_failed_green(self) -> None:
        command = self.write_tdd_plan()
        green = self.run_evidence("tdd-sample-green", command)
        self.assertEqual(1, green.returncode)
        result = self.check_tdd()
        self.assertEqual(1, result.returncode)
        self.assertIn("缺少 Red evidence", result.stdout)
        self.assertIn("Green outcome 必须是 passed", result.stdout)

    def test_tdd_pair_rejects_outcome_and_order_drift(self) -> None:
        command = self.write_tdd_plan()
        self.run_tdd_pair(command)

        red = self.record("tdd-sample-red")
        red["outcome"] = "passed"
        red["process_exit_code"] = 0
        self.write_record("tdd-sample-red", red)
        wrong_outcome = self.check_tdd()
        self.assertEqual(1, wrong_outcome.returncode)
        self.assertIn("Red outcome 必须是 failed", wrong_outcome.stdout)

        red["outcome"] = "failed"
        red["process_exit_code"] = 1
        green = self.record("tdd-sample-green")
        red["finished_at"] = green["started_at"]
        green["started_at"] = red["started_at"]
        self.write_record("tdd-sample-red", red)
        self.write_record("tdd-sample-green", green)
        wrong_order = self.check_tdd()
        self.assertEqual(1, wrong_order.returncode)
        self.assertIn("Red 必须完整结束后才开始 Green", wrong_order.stdout)

    def test_tdd_pair_rejects_command_cwd_and_ac_drift(self) -> None:
        command = self.write_tdd_plan()
        self.run_tdd_pair(command)
        green_path = self.hot / "tdd-sample-green" / "record.json"
        original = green_path.read_text(encoding="utf-8")

        mutations = (
            ("argv", "argv 与声明不一致", lambda record: record["command"].__setitem__("argv", ["false"])),
            ("cwd", "cwd 与声明不一致", lambda record: record["command"].__setitem__("cwd", "other")),
            ("ac", "AC 与声明不一致", lambda record: record.__setitem__("ac_ids", ["AC1"])),
        )
        for label, expected, mutate in mutations:
            with self.subTest(label=label):
                green_path.write_text(original, encoding="utf-8")
                record = json.loads(original)
                mutate(record)
                self.write_record("tdd-sample-green", record)
                result = self.check_tdd()
                self.assertEqual(1, result.returncode)
                self.assertIn(expected, result.stdout)

    def test_tdd_declaration_rejects_bad_rows_and_duplicate_cycles(self) -> None:
        command = self.write_tdd_plan(cycle="Bad_Name")
        invalid_name = self.check_tdd()
        self.assertEqual(1, invalid_name.returncode)
        self.assertIn("cycle 名非法", invalid_name.stdout)

        argv_json = json.dumps(command, separators=(",", ":"))
        plan = self.root / ".ai" / "TECH_PLAN.md"
        plan.write_text(
            "# TECH_PLAN — ITER-0099\n\n## Test Strategy\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            f"| sample | AC1,AC3 | `{argv_json}` | `.` |\n"
            f"| sample | AC1,AC3 | `{argv_json}` | `.` |\n",
            encoding="utf-8",
        )
        duplicate = self.check_tdd()
        self.assertEqual(1, duplicate.returncode)
        self.assertIn("cycle 重复", duplicate.stdout)

        plan.write_text(
            "# TECH_PLAN — ITER-0099\n\n## Test Strategy\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            "| sample | AC1 | `[not-json]` | `../escape` |\n",
            encoding="utf-8",
        )
        invalid_fields = self.check_tdd()
        self.assertEqual(1, invalid_fields.returncode)
        self.assertIn("argv_json 非法", invalid_fields.stdout)
        self.assertIn("cwd 越出项目根", invalid_fields.stdout)

    def test_tdd_declaration_must_live_in_test_strategy_and_fit_evidence_ids(self) -> None:
        command = self.write_tdd_plan()
        argv_json = json.dumps(command, separators=(",", ":"))
        plan = self.root / ".ai" / "TECH_PLAN.md"
        plan.write_text(
            "# TECH_PLAN — ITER-0099\n\n## Design Decisions\n\n"
            "<!-- butler-tdd-cycles: v1 -->\n"
            "| Cycle | AC | argv_json | cwd |\n"
            "|---|---|---|---|\n"
            f"| sample | AC1,AC3 | `{argv_json}` | `.` |\n\n"
            "## Test Strategy\n\n- 普通测试。\n",
            encoding="utf-8",
        )
        wrong_section = self.check_tdd()
        self.assertEqual(1, wrong_section.returncode)
        self.assertIn("必须位于 Test Strategy 段", wrong_section.stdout)

        self.write_tdd_plan(cycle="a" * 60)
        too_long = self.check_tdd()
        self.assertEqual(1, too_long.returncode)
        self.assertIn("生成的 evidence ID 非法", too_long.stdout)

    def test_tdd_pair_supports_archived_evidence(self) -> None:
        command = self.write_tdd_plan()
        self.run_tdd_pair(command)
        archived = self.invoke(
            "archive", "--project-root", str(self.root), "--iteration", "ITER-0099"
        )
        self.assertEqual(0, archived.returncode, archived.stdout + archived.stderr)
        result = self.check_tdd("archive")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("[OK] sample", result.stdout)


if __name__ == "__main__":
    unittest.main()
