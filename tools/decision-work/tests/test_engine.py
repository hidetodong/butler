from __future__ import annotations

import unittest

from common import Harness, decision_map, work


class DecisionWorkEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.h = Harness()

    def tearDown(self) -> None:
        self.h.close()

    def test_research_candidate_requires_explicit_absorb(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        self.h.prepare("DEC-0001", "ATT-0001", claim)
        before = decision_map.inspect(self.h.root, self.h.map_id)["state"]["revision"]
        self.h.record("DEC-0001", "ATT-0001", self.h.candidate())
        view = work.inspect(self.h.root, self.h.map_id, "DEC-0001", "ATT-0001", "2026-08-01T01:03:00Z")
        self.assertTrue(view["attempts"][0]["derived"]["absorbable"])
        self.assertEqual(before, decision_map.inspect(self.h.root, self.h.map_id)["state"]["revision"])

        spec = self.h.work_spec("absorb_result", {"decision_id": "DEC-0001", "attempt_id": "ATT-0001", "owner": claim["owner"], "token": claim["token"], "resolve_operation_id": "OP-resolve-from-work"})
        planned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:04:00Z")
        applied = work.apply(self.h.root, planned, "2026-08-01T01:04:00Z")
        self.assertFalse(applied["idempotent"])
        state = decision_map.inspect(self.h.root, self.h.map_id)["state"]
        self.assertEqual("resolved", state["decisions"]["DEC-0001"]["status"])
        self.assertIn("decision-work:.ai/decision-work/DMAP-0001/DEC-0001/ATT-0001/result.json#sha256:", state["decisions"]["DEC-0001"]["resolution"]["evidence"][-1])
        self.assertTrue(work.apply(self.h.root, planned, "2026-08-01T02:00:00Z")["idempotent"])
        replanned = work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T02:01:00Z")
        self.assertTrue(replanned["effect"]["idempotent"])
        self.assertTrue(work.apply(self.h.root, replanned, "2026-08-01T02:01:00Z")["idempotent"])

    def test_four_work_type_candidate_contracts(self) -> None:
        for index, work_type in enumerate(("research", "prototype", "grilling", "task"), 1):
            with self.subTest(work_type=work_type):
                decision = f"DEC-{index:04d}"
                attempt = f"ATT-{index:04d}"
                claim = self.h.add_and_claim(decision)
                self.h.prepare(decision, attempt, claim, work_type=work_type, mode="serial")
                self.h.record(decision, attempt, self.h.candidate(work_type))
                result = work.inspect(self.h.root, self.h.map_id, decision, attempt)["attempts"][0]["result"]
                self.assertEqual("candidate", result["status"])

    def test_needs_input_requires_new_predecessor_attempt(self) -> None:
        claim = self.h.add_and_claim("DEC-0001")
        self.h.prepare("DEC-0001", "ATT-0001", claim, work_type="prototype", mode="hitl")
        self.h.record("DEC-0001", "ATT-0001", {"status": "needs_input", "actual_execution_mode": "hitl", "fresh_context": False, "questions": ["Approve prototype?"], "artifact_pointers": ["artifact:demo"]})
        self.h.prepare("DEC-0001", "ATT-0002", claim, work_type="prototype", predecessor="ATT-0001", mode="hitl")
        with self.assertRaises(work.DecisionWorkError) as duplicate:
            self.h.prepare("DEC-0001", "ATT-0003", claim, work_type="prototype", predecessor="ATT-0001", mode="hitl")
        self.assertEqual("predecessor_already_continued", duplicate.exception.code)

    def test_invalid_human_and_task_candidates_fail_closed(self) -> None:
        cases = [
            ("prototype", {"artifacts": ["a"], "observations": ["o"], "human_evaluation": ""}),
            ("grilling", {"questions": ["q"], "human_answers": ["invented"], "assumptions": [], "tradeoffs": ["t"], "self_answered": True}),
            ("task", {"action": "a", "evidence": ["e"], "unblocked": True, "delivery_completed": True}),
        ]
        for index, (work_type, payload) in enumerate(cases, 1):
            decision = f"DEC-{index:04d}"
            attempt = f"ATT-{index:04d}"
            claim = self.h.add_and_claim(decision)
            self.h.prepare(decision, attempt, claim, work_type=work_type, mode="serial")
            result = self.h.candidate(work_type)
            result["payload"] = payload
            before = self.h.tree_bytes(self.h.root)
            with self.subTest(work_type=work_type), self.assertRaises(work.DecisionWorkError):
                self.h.record(decision, attempt, result)
            self.assertEqual(before, self.h.tree_bytes(self.h.root))

    def test_failed_cancelled_and_late_never_resolve(self) -> None:
        results = [
            {"status": "failed", "actual_execution_mode": "serial", "fresh_context": True, "error_code": "network", "error_summary": "offline"},
            {"status": "cancelled", "actual_execution_mode": "serial", "fresh_context": True, "reason": "user stopped"},
        ]
        for index, result in enumerate(results, 1):
            decision = f"DEC-{index:04d}"
            attempt = f"ATT-{index:04d}"
            claim = self.h.add_and_claim(decision, now="2026-08-01T01:00:00Z")
            self.h.prepare(decision, attempt, claim, now="2026-08-01T01:01:00Z")
            self.h.record(decision, attempt, result, now="2026-08-01T02:30:00Z")
            item = work.inspect(self.h.root, self.h.map_id, decision, attempt, "2026-08-01T02:31:00Z")["attempts"][0]
            self.assertEqual("late", item["derived"]["timeliness"])
            self.assertFalse(item["derived"]["absorbable"])
            self.assertEqual("open", decision_map.inspect(self.h.root, self.h.map_id)["state"]["decisions"][decision]["status"])

    def test_absorb_uses_fresh_map_base_for_parallel_results(self) -> None:
        claims = {decision: self.h.add_and_claim(decision) for decision in ("DEC-0001", "DEC-0002")}
        requests = []
        for index, decision in enumerate(claims, 1):
            claim = claims[decision]
            requests.append({"decision_id": decision, "attempt_id": f"ATT-{index:04d}", "confirmed_context": [], "constraints": [], "expected_output": ["answer"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": "parallel"})
        spec = self.h.work_spec("prepare_attempts", {"work_type": "research", "max_parallel": 2, "attempts": requests})
        work.apply(self.h.root, work.plan(self.h.root, self.h.map_id, spec, "2026-08-01T01:01:00Z"), "2026-08-01T01:01:00Z")
        for index, decision in enumerate(claims, 1):
            attempt = f"ATT-{index:04d}"
            self.h.record(decision, attempt, self.h.candidate())
            absorb = self.h.work_spec("absorb_result", {"decision_id": decision, "attempt_id": attempt, "owner": claims[decision]["owner"], "token": claims[decision]["token"], "resolve_operation_id": f"OP-resolve-{index}"})
            work.apply(self.h.root, work.plan(self.h.root, self.h.map_id, absorb, "2026-08-01T01:04:00Z"), "2026-08-01T01:04:00Z")
        state = decision_map.inspect(self.h.root, self.h.map_id)["state"]
        self.assertEqual(["resolved", "resolved"], [state["decisions"][item]["status"] for item in claims])


if __name__ == "__main__":
    unittest.main(verbosity=2)
