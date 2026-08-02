from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from common import Harness, decision_map, work


CLI = Path(__file__).resolve().parents[1] / "decision_work.py"


class DecisionWorkStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.h = Harness()

    def tearDown(self) -> None:
        self.h.close()

    def test_inspect_plan_verify_are_zero_write(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        before = self.h.tree_bytes(self.h.root)
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "attempts": [{"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "serial"}]})
        work.inspect(self.h.root, now="2026-08-01T01:01:00Z")
        work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z")
        self.assertEqual("ok", work.verify(self.h.root, now="2026-08-01T01:01:00Z")["status"])
        self.assertEqual(before, self.h.tree_bytes(self.h.root))

    def test_prepare_and_record_are_immutable_and_idempotent(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        request = {"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "serial"}
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "attempts": [request]}, "OP-stable-prepare")
        planned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z")
        self.assertFalse(work.apply(self.h.root, planned, "2026-08-01T01:01:00Z")["idempotent"])
        self.assertTrue(work.apply(self.h.root, planned, "2026-08-01T01:02:00Z")["idempotent"])
        replanned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T03:00:00Z")
        self.assertTrue(replanned["effect"]["idempotent"])
        self.assertTrue(work.apply(self.h.root, replanned, "2026-08-01T03:00:00Z")["idempotent"])
        result_plan, first = self.h.record("DEC-0001", "ATT-0001", self.h.candidate(), operation_id="OP-stable-record")
        self.assertFalse(first["idempotent"])
        self.assertTrue(work.apply(self.h.root, result_plan, "2026-08-01T01:03:00Z")["idempotent"])

    def test_two_processes_publish_one_immutable_attempt(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        request = {"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "serial"}
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "attempts": [request]}, "OP-concurrent-prepare")
        planned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z")
        plan_path = self.h.root / "concurrent-plan.json"
        plan_path.write_text(json.dumps(planned), encoding="utf-8")
        processes = [
            subprocess.Popen(
                [sys.executable, str(CLI), "apply", "--project-root", str(self.h.root), "--plan", str(plan_path), "--now", "2026-08-01T01:01:01Z"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for _ in range(2)
        ]
        results = [process.communicate() + (process.returncode,) for process in processes]
        self.assertIn(0, [item[2] for item in results])
        self.assertTrue(all(item[2] in {0, 1} for item in results))
        for stdout, stderr, _ in results:
            self.assertEqual("", stderr)
            self.assertIsInstance(json.loads(stdout), dict)
        attempt = self.h.root / ".ai/decision-work/DMAP-0001/DEC-0001/ATT-0001"
        self.assertEqual(["task.json"], sorted(path.name for path in attempt.iterdir()))
        self.assertEqual("ok", work.verify(self.h.root, self.h.map_id, "2026-08-01T01:02:00Z")["status"])

    def test_bad_batch_is_zero_write_and_limits_are_strict(self) -> None:
        claims = {decision: self.h.add_and_claim(decision) for decision in ("DEC-0001", "DEC-0002")}
        before = self.h.tree_bytes(self.h.root)
        requests = []
        for index, decision in enumerate(claims, 1):
            claim = claims[decision]
            requests.append({"decision_id": decision, "attempt_id": f"ATT-{index:04d}", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": "wrong" if index == 2 else claim["token"], "requested_execution_mode": "parallel"})
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "max_parallel": 2, "attempts": requests})
        with self.assertRaises(work.DecisionWorkError):
            work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z")
        self.assertEqual(before, self.h.tree_bytes(self.h.root))
        for value in (0, 9, True):
            invalid = self.h.work_spec("prepare_attempts", {"work_type": "research", "max_parallel": value, "attempts": [requests[0]]})
            with self.assertRaises(work.DecisionWorkError):
                work.plan(self.h.root, self.h.map_id, invalid)

    def test_batch_publish_failure_rolls_back_attempt_tree(self) -> None:
        claims = {decision: self.h.add_and_claim(decision) for decision in ("DEC-0001", "DEC-0002")}
        requests = []
        for index, decision in enumerate(claims, 1):
            claim = claims[decision]
            requests.append({"decision_id": decision, "attempt_id": f"ATT-{index:04d}", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "parallel"})
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "max_parallel": 2, "attempts": requests})
        planned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z")
        original_rename = work.os.rename
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected publish failure")
            return original_rename(source, target)

        with mock.patch.object(work.os, "rename", side_effect=fail_second):
            with self.assertRaises(OSError):
                work.apply(self.h.root, planned, "2026-08-01T01:01:00Z")
        self.assertFalse((self.h.root / ".ai/decision-work").exists())

    def test_claim_replacement_makes_result_stale_but_recordable(self) -> None:
        claim = self.h.add_and_claim("DEC-0001", now="2026-08-01T01:00:00Z")
        self.h.prepare("DEC-0001", "ATT-0001", claim, now="2026-08-01T01:01:00Z")
        replacement = self.h.map_commit("claim", {"decision_id": "DEC-0001", "owner": "other", "lease_seconds": 3600}, now="2026-08-01T02:00:00Z", operation_id="OP-reclaim")
        self.h.record("DEC-0001", "ATT-0001", self.h.candidate(), now="2026-08-01T02:01:00Z")
        derived = work.inspect(self.h.root, self.h.map_id, "DEC-0001", "ATT-0001", "2026-08-01T02:02:00Z")["attempts"][0]["derived"]
        self.assertEqual("stale", derived["relation"])
        self.assertFalse(derived["absorbable"])

    def test_verify_reports_symlink_and_tampering(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        self.h.prepare("DEC-0001", "ATT-0001", claim)
        task = self.h.root / ".ai/decision-work/DMAP-0001/DEC-0001/ATT-0001/task.json"
        task.write_text(task.read_text().replace("Question", "Changed"))
        report = work.verify(self.h.root, self.h.map_id)
        self.assertEqual("error", report["status"])
        self.assertTrue(any(item["code"] in {"noncanonical_document", "task_digest_mismatch", "task_binding_mismatch"} for item in report["errors"]))

        task.unlink()
        os.symlink("/tmp", task)
        report = work.verify(self.h.root, self.h.map_id)
        self.assertEqual("error", report["status"])
        self.assertTrue(any(item["code"] == "unsafe_path" for item in report["errors"]))

    def test_verify_reports_absorbed_result_deleted_after_commit(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        self.h.prepare("DEC-0001", "ATT-0001", claim)
        self.h.record("DEC-0001", "ATT-0001", self.h.candidate())
        absorb = self.h.work_spec("absorb_result", {"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "owner": claim["owner"], "token": claim["token"], "resolve_operation_id": "OP-resolve-for-missing-result"})
        work.apply(self.h.root, work.plan(self.h.root, self.h.map_id, absorb, "2026-08-01T01:03:00Z"), "2026-08-01T01:03:00Z")
        result = self.h.root / ".ai/decision-work/DMAP-0001/DEC-0001/ATT-0001/result.json"
        result.unlink()
        report = work.verify(self.h.root, self.h.map_id, "2026-08-01T01:04:00Z")
        self.assertEqual("error", report["status"])
        self.assertTrue(any(item["code"] == "missing_result" for item in report["errors"]))

    def test_verify_reports_result_content_tampering_before_absorb(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        self.h.prepare("DEC-0001", "ATT-0001", claim)
        self.h.record("DEC-0001", "ATT-0001", self.h.candidate())
        result = self.h.root / ".ai/decision-work/DMAP-0001/DEC-0001/ATT-0001/result.json"
        result.write_text(result.read_text().replace("Choose A", "Choose B"))
        report = work.verify(self.h.root, self.h.map_id, "2026-08-01T01:04:00Z")
        self.assertEqual("error", report["status"])
        self.assertTrue(any(item["code"] == "result_request_mismatch" for item in report["errors"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
