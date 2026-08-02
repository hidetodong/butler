from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


WORK_ROOT = Path(__file__).resolve().parents[1]
MAP_ROOT = WORK_ROOT.parent / "decision-map"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


work = load("decision_work_engine_tests", WORK_ROOT / "engine.py")
decision_map = load("decision_map_engine_work_tests", MAP_ROOT / "engine.py")


class Harness:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-decision-work-")
        self.root = Path(self.temp.name)
        (self.root / ".ai").mkdir()
        self.map_id = "DMAP-0001"
        self.map_counter = 0
        self.work_counter = 0
        self.map_commit("create_map", {"title": "Choose sync", "destination": "Resolve sync decisions"}, now="2026-08-01T00:00:00Z")

    def close(self) -> None:
        self.temp.cleanup()

    def map_spec(self, kind: str, fields: dict | None = None, operation_id: str | None = None) -> dict:
        self.map_counter += 1
        return {"schema_version": 1, "operation_id": operation_id or f"OP-map-{self.map_counter}", "operation": {"kind": kind, **(fields or {})}}

    def map_commit(self, kind: str, fields: dict | None = None, *, now: str = "2026-08-01T00:01:00Z", operation_id: str | None = None) -> dict:
        spec = self.map_spec(kind, fields, operation_id)
        return decision_map.apply(self.root, decision_map.plan(self.root, self.map_id, spec, now), now)

    def add_and_claim(self, decision_id: str, owner: str = "coordinator", *, depends_on: list[str] | None = None, now: str = "2026-08-01T01:00:00Z") -> dict:
        self.map_commit("add_decision", {"decision_id": decision_id, "question": f"Question {decision_id}?", "depends_on": depends_on or []}, now=now)
        operation_id = f"OP-claim-{decision_id}"
        claim = self.map_commit("claim", {"decision_id": decision_id, "owner": owner, "lease_seconds": 3600}, now=now, operation_id=operation_id)
        return {**claim, "operation_id": operation_id}

    def work_spec(self, kind: str, operation: dict, operation_id: str | None = None) -> dict:
        self.work_counter += 1
        return {"schema_version": 1, "operation_id": operation_id or f"OP-work-{self.work_counter}", "operation": {"kind": kind, "map_id": self.map_id, **operation}}

    def prepare(self, decision_id: str, attempt_id: str, claim: dict, *, work_type: str = "research", now: str = "2026-08-01T01:01:00Z", predecessor: str | None = None, mode: str = "serial") -> dict:
        request = {"decision_id": decision_id, "attempt_id": attempt_id, "confirmed_context": ["Confirmed"], "constraints": ["No project writes"], "expected_output": ["Candidate decision"], "claim_operation_id": claim["operation_id"], "claim_owner": claim["owner"], "claim_token": claim["token"], "requested_execution_mode": mode}
        if predecessor is not None:
            request["predecessor_attempt_id"] = predecessor
        spec = self.work_spec("prepare_attempts", {"work_type": work_type, "max_parallel": 1, "attempts": [request]})
        planned = work.plan(self.root, self.map_id, spec, now)
        return work.apply(self.root, planned, now)

    def task_digest(self, decision_id: str, attempt_id: str) -> str:
        view = work.inspect(self.root, self.map_id, decision_id, attempt_id, "2026-08-01T01:02:00Z")
        task = view["attempts"][0]["task"]
        return work._sha(work._canonical_json(task))

    @staticmethod
    def candidate(work_type: str = "research") -> dict:
        payloads = {
            "research": {"findings": ["Fact"], "sources": ["https://example.test"], "uncertainties": []},
            "prototype": {"artifacts": ["artifact:demo"], "observations": ["Works"], "human_evaluation": "Accept"},
            "grilling": {"questions": ["Why?"], "human_answers": ["Because"], "assumptions": [], "tradeoffs": ["Cost"], "self_answered": False},
            "task": {"action": "Check real path", "evidence": ["evidence:run"], "unblocked": True},
        }
        return {"status": "candidate", "actual_execution_mode": "serial", "fresh_context": work_type == "research", "outcome": "Choose A", "rationale": "Evidence supports A", "evidence": ["source:one"], "payload": payloads[work_type]}

    def record(self, decision_id: str, attempt_id: str, result: dict, *, now: str = "2026-08-01T01:02:00Z", operation_id: str | None = None) -> tuple[dict, dict]:
        spec = self.work_spec("record_result", {"decision_id": decision_id, "attempt_id": attempt_id, "task_sha256": self.task_digest(decision_id, attempt_id), "result": result}, operation_id)
        planned = work.plan(self.root, self.map_id, spec, now)
        return planned, work.apply(self.root, planned, now)

    @staticmethod
    def tree_bytes(root: Path) -> dict[str, bytes]:
        return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}
