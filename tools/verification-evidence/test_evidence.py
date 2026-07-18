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


if __name__ == "__main__":
    unittest.main()
