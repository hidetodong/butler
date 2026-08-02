from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from common import Harness, promotion


NOW = "2026-08-02T01:00:00Z"
CLI = Path(__file__).resolve().parents[1] / "decision_promotion.py"


class DecisionPromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.h = Harness()
        self.h.source_chain()

    def tearDown(self) -> None:
        self.h.close()

    def test_source_closure_allows_partial_map_and_empty_evidence(self) -> None:
        self.h.map_apply("add_decision", operation_id="OP-add-3", decision_id="DEC-0003", question="Unrelated", depends_on=[])
        before = self.h.tree_bytes(self.h.root)
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        self.assertEqual("DEC-0002", planned["request"]["source"]["decision_ids"][0])
        self.assertEqual(["DEC-0001", "DEC-0002"], planned["effect"]["source"]["closure"])
        source = promotion._source_slice(self.h.root, planned["request"]["source"])
        self.assertEqual(["DEC-0001", "DEC-0002"], source["closure"])
        self.assertEqual(before, self.h.tree_bytes(self.h.root))

    def test_unresolved_or_unknown_source_fails_without_writes(self) -> None:
        self.h.map_apply("add_decision", operation_id="OP-add-3", decision_id="DEC-0003", question="Open", depends_on=[])
        for identity in ("DEC-0003", "DEC-9999"):
            before = self.h.tree_bytes(self.h.root)
            with self.assertRaises(promotion.DecisionPromotionError):
                promotion.plan(self.h.root, self.h.route_request(roots=[identity]), NOW)
            self.assertEqual(before, self.h.tree_bytes(self.h.root))

    def test_route_reference_only_adds_receipt_semantic_state_and_is_inspectable(self) -> None:
        map_before = (self.h.ai / "decision-maps/DMAP-0001/state.json").read_bytes()
        milestone_before = (self.h.ai / "MILESTONE.md").read_bytes()
        iterations_before = (self.h.ai / "ITERATIONS.md").read_bytes()
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        result = promotion.apply(self.h.root, planned, NOW)
        self.assertFalse(result["idempotent"])
        self.assertTrue((self.h.ai / "decision-promotions/PROM-0001/receipt.json").is_file())
        self.assertEqual(map_before, (self.h.ai / "decision-maps/DMAP-0001/state.json").read_bytes())
        self.assertEqual(milestone_before, (self.h.ai / "MILESTONE.md").read_bytes())
        self.assertEqual(iterations_before, (self.h.ai / "ITERATIONS.md").read_bytes())
        viewed = promotion.inspect(self.h.root, milestone_id="MILE-0002", route_id="R1", now=NOW)
        self.assertEqual(["PROM-0001"], [item["promotion_id"] for item in viewed["receipts"]])
        self.assertEqual("ok", promotion.verify(self.h.root, now=NOW)["status"])

    def test_receipt_replay_is_idempotent_and_id_conflict_fails(self) -> None:
        request = self.h.route_request()
        planned = promotion.plan(self.h.root, request, NOW)
        promotion.apply(self.h.root, planned, NOW)
        before = self.h.tree_bytes(self.h.root)
        self.assertTrue(promotion.apply(self.h.root, planned, NOW)["idempotent"])
        self.assertTrue(promotion.plan(self.h.root, request, NOW)["effect"]["idempotent"])
        changed = self.h.route_request(route_id="R2")
        with self.assertRaises(promotion.DecisionPromotionError) as error:
            promotion.plan(self.h.root, changed, NOW)
        self.assertEqual("promotion_id_conflict", error.exception.code)
        self.assertEqual(before, self.h.tree_bytes(self.h.root))

    def test_receipt_publish_failure_leaves_no_visible_or_staged_promotion(self) -> None:
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        with mock.patch.object(promotion.os, "rename", side_effect=OSError("injected rename failure")):
            with self.assertRaises(OSError):
                promotion.apply(self.h.root, planned, NOW)
        base = self.h.ai / "decision-promotions"
        self.assertFalse((base / "PROM-0001").exists())
        self.assertEqual([], list(base.iterdir()))

    def test_route_state_change_makes_plan_stale_but_unrelated_map_change_does_not(self) -> None:
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        self.h.map_apply("add_fog", operation_id="OP-unrelated-fog", fog_id="FOG-0001", description="Unrelated")
        promotion.apply(self.h.root, planned, NOW)

        other = promotion.plan(self.h.root, self.h.route_request("PROM-0002", route_id="R2"), NOW)
        milestone = self.h.ai / "MILESTONE.md"
        milestone.write_text(milestone.read_text().replace("| R2 | Future | — | planned |", "| R2 | Future | ITER-0043 | active |"), encoding="utf-8")
        before = self.h.tree_bytes(self.h.root, semantic=True)
        with self.assertRaises(promotion.DecisionPromotionError) as error:
            promotion.apply(self.h.root, other, NOW)
        self.assertEqual("stale_plan", error.exception.code)
        self.assertEqual(before, self.h.tree_bytes(self.h.root, semantic=True))

    def test_invalid_route_states_and_standalone_under_active_milestone_fail(self) -> None:
        for status, iteration in (("active", "ITER-0043"), ("closed", "ITER-0043"), ("abandoned", "—")):
            self.h.set_milestone(True, route_status=status, iteration=iteration)
            with self.assertRaises(promotion.DecisionPromotionError):
                promotion.plan(self.h.root, self.h.route_request(), NOW)
        self.h.set_milestone(True)
        with self.assertRaises(promotion.DecisionPromotionError) as error:
            promotion.plan(self.h.root, self.h.iteration_request(milestone=False), NOW)
        self.assertEqual("milestone_mismatch", error.exception.code)

    def test_nonblocking_global_lock_conflict_is_zero_semantic_write(self) -> None:
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        lock = self.h.ai / ".decision-promotion.lock"
        descriptor = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        before = self.h.tree_bytes(self.h.root, semantic=True)
        try:
            with self.assertRaises(promotion.DecisionPromotionError) as error:
                promotion.apply(self.h.root, planned, NOW)
            self.assertEqual("promotion_busy", error.exception.code)
            self.assertEqual(before, self.h.tree_bytes(self.h.root, semantic=True))
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def test_project_root_guard_blocks_even_if_ai_lock_inode_can_change(self) -> None:
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        descriptor = os.open(self.h.root, os.O_RDONLY)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            with self.assertRaises(promotion.DecisionPromotionError) as error:
                promotion.apply(self.h.root, planned, NOW)
            self.assertEqual("promotion_busy", error.exception.code)
            self.assertFalse((self.h.ai / "decision-promotions").exists())
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def test_two_processes_commit_one_receipt_for_same_plan(self) -> None:
        planned = promotion.plan(self.h.root, self.h.route_request(), NOW)
        path = self.h.root / "promotion-plan.json"
        path.write_text(json.dumps(planned), encoding="utf-8")
        processes = [
            subprocess.Popen(
                [sys.executable, str(CLI), "apply", "--project-root", str(self.h.root), "--plan", str(path), "--now", NOW],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for _ in range(2)
        ]
        results = [process.communicate() + (process.returncode,) for process in processes]
        self.assertTrue(all(item[2] in {0, 1} for item in results))
        self.assertIn(0, [item[2] for item in results])
        self.assertEqual(["PROM-0001"], [path.name for path in (self.h.ai / "decision-promotions").iterdir() if not path.name.startswith(".tmp-")])
        self.assertEqual("ok", promotion.verify(self.h.root, now=NOW)["status"])

    def test_iteration_start_reuses_intake_and_writes_source_reference(self) -> None:
        request = self.h.iteration_request()
        planned = promotion.plan(self.h.root, request, NOW)

        def sync_state(root) -> None:
            promotion.STATE_LEDGER.migrate(root, 20, 50)

        with mock.patch.object(promotion.ITERATION_INTAKE, "sync_state", side_effect=sync_state):
            result = promotion.apply(self.h.root, planned, NOW)
        self.assertEqual("ITER-0043", result["iteration_id"])
        concept = (self.h.ai / "CONCEPT.md").read_text(encoding="utf-8")
        self.assertIn("Promotion Source：`PROM-0001`", concept)
        self.assertIn("已确认：DEC-0001 — Choose 1", concept)
        self.assertIn("已确认：DEC-0002 — Choose 2", concept)
        self.assertIn("current: ITER-0043", (self.h.ai / "ITERATIONS.md").read_text())
        self.assertIn("| R1 | Router | ITER-0043 | active |", (self.h.ai / "MILESTONE.md").read_text())
        self.assertFalse((self.h.ai / ".decision-promotion-pending").exists())
        self.assertEqual("ok", promotion.verify(self.h.root, now=NOW)["status"])

    def test_standalone_iteration_only_when_no_active_milestone(self) -> None:
        self.h.set_milestone(False)
        planned = promotion.plan(self.h.root, self.h.iteration_request(milestone=False), NOW)
        with mock.patch.object(promotion.ITERATION_INTAKE, "sync_state", side_effect=lambda root: promotion.STATE_LEDGER.migrate(root, 20, 50)):
            result = promotion.apply(self.h.root, planned, NOW)
        self.assertIsNone(result["milestone_id"])
        self.assertIn("| ITER-0043 | Promoted slice | active", (self.h.ai / "ITERATIONS.md").read_text())

    def test_intake_callback_or_sync_failure_rolls_back_all_ai_state(self) -> None:
        planned = promotion.plan(self.h.root, self.h.iteration_request(), NOW)
        before = self.h.tree_bytes(self.h.root, semantic=True)
        with mock.patch.object(promotion.ITERATION_INTAKE, "sync_state", side_effect=RuntimeError("sync failed")):
            with self.assertRaises(RuntimeError):
                promotion.apply(self.h.root, planned, NOW)
        self.assertEqual(before, self.h.tree_bytes(self.h.root, semantic=True))
        self.assertFalse((self.h.ai / "decision-promotions/PROM-0001").exists())
        self.assertFalse((self.h.ai / ".decision-promotion-pending").exists())

    def test_pending_journal_makes_pre_callback_crash_detectable_and_blocks_retry(self) -> None:
        request = self.h.iteration_request()
        planned = promotion.plan(self.h.root, request, NOW)
        source = promotion._source_slice(self.h.root, planned["request"]["source"])
        result = {key: planned["effect"][key] for key in ("kind", "milestone_id", "route_id", "iteration_id")}
        pending = promotion._make_pending(planned["request"], planned["request_sha256"], source, result, NOW)
        promotion._publish_pending(self.h.root, pending)
        report = promotion.verify(self.h.root, now=NOW)
        self.assertTrue(any(item["code"] == "incomplete_promotion" for item in report["errors"]))
        with self.assertRaises(promotion.DecisionPromotionError) as error:
            promotion.plan(self.h.root, request, NOW)
        self.assertEqual("incomplete_promotion", error.exception.code)

    def test_verify_reports_incomplete_marker_tampering_and_symlink(self) -> None:
        concept = self.h.ai / "CONCEPT.md"
        concept.write_text("## Current Understanding\n\n- Promotion Source：`PROM-0009` missing\n", encoding="utf-8")
        report = promotion.verify(self.h.root, now=NOW)
        self.assertTrue(any(item["code"] == "incomplete_promotion" for item in report["errors"]))

        promotion.apply(self.h.root, promotion.plan(self.h.root, self.h.route_request(), NOW), NOW)
        receipt = self.h.ai / "decision-promotions/PROM-0001/receipt.json"
        value = json.loads(receipt.read_text(encoding="utf-8"))
        value["source"]["slice_sha256"] = "sha256:" + "0" * 64
        receipt.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        report = promotion.verify(self.h.root, now=NOW)
        self.assertEqual("error", report["status"])
        self.assertTrue(any(item["code"] == "source_slice_mismatch" for item in report["errors"]))

        receipt.unlink()
        receipt.symlink_to("/tmp/missing")
        report = promotion.verify(self.h.root, now=NOW)
        self.assertTrue(any(item["code"] in {"unsafe_path", "missing_state"} for item in report["errors"]))

    def test_unknown_fields_duplicate_roots_and_bad_ids_fail_closed(self) -> None:
        cases = []
        unknown = self.h.route_request(); unknown["extra"] = True; cases.append(unknown)
        duplicate = self.h.route_request(); duplicate["source"]["decision_ids"] = ["DEC-0002", "DEC-0002"]; cases.append(duplicate)
        bad = self.h.route_request(); bad["promotion_id"] = "PROM-0000"; cases.append(bad)
        for request in cases:
            before = self.h.tree_bytes(self.h.root)
            with self.assertRaises(promotion.DecisionPromotionError):
                promotion.plan(self.h.root, request, NOW)
            self.assertEqual(before, self.h.tree_bytes(self.h.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
