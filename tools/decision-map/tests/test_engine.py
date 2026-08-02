from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "engine.py"
SPEC = importlib.util.spec_from_file_location("decision_map_engine", MODULE)
assert SPEC and SPEC.loader
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)


class DecisionMapEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-decision-map-")
        self.root = Path(self.temp.name)
        (self.root / ".ai").mkdir()
        self.map_id = "DMAP-0001"
        self.counter = 0
        self.commit(
            "create_map",
            {"title": "Choose sync", "destination": "Select a safe sync strategy"},
            now="2026-08-01T00:00:00Z",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def spec(self, kind: str, fields: dict | None = None, operation_id: str | None = None) -> dict:
        self.counter += 1
        return {
            "schema_version": 1,
            "operation_id": operation_id or f"OP-test-{self.counter}",
            "operation": {"kind": kind, **(fields or {})},
        }

    def commit(self, kind: str, fields: dict | None = None, *, now: str = "2026-08-01T00:01:00Z", operation_id: str | None = None) -> dict:
        spec = self.spec(kind, fields, operation_id)
        planned = engine.plan(self.root, self.map_id, spec, now)
        return engine.apply(self.root, planned, now)

    def add_decision(self, identity: str, depends_on: list[str] | None = None) -> None:
        self.commit("add_decision", {"decision_id": identity, "question": f"Question {identity}?", "depends_on": depends_on or []})

    def resolve(self, identity: str, **credentials: str) -> dict:
        return self.commit("resolve", {"decision_id": identity, "outcome": f"Resolved {identity}", "rationale": "Evidence supports it", "evidence": ["ref:local"], **credentials})

    @staticmethod
    def tree_bytes(root: Path) -> dict[str, bytes]:
        return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}

    def test_dependency_frontier_abandon_and_close_lifecycle(self) -> None:
        self.add_decision("DEC-0001")
        self.add_decision("DEC-0002", ["DEC-0001"])
        view = engine.inspect(self.root, self.map_id, "2026-08-01T00:02:00Z")
        self.assertEqual(["DEC-0001"], view["frontier"])

        self.resolve("DEC-0001")
        self.assertEqual(["DEC-0002"], engine.inspect(self.root, self.map_id, "2026-08-01T00:02:00Z")["frontier"])
        self.commit("abandon", {"decision_id": "DEC-0002", "reason": "No longer needed"})
        closed = self.commit("close_map")
        self.assertEqual(6, closed["revision"])
        self.assertEqual("closed", engine.inspect(self.root, self.map_id)["state"]["status"])
        with self.assertRaisesRegex(engine.DecisionMapError, "read-only") as captured:
            engine.plan(self.root, self.map_id, self.spec("add_fog", {"fog_id": "FOG-0001", "description": "Late fog"}))
        self.assertEqual("map_closed", captured.exception.code)

    def test_dag_and_abandoned_dependency_fail_closed(self) -> None:
        self.add_decision("DEC-0001")
        self.add_decision("DEC-0002", ["DEC-0001"])
        before = self.tree_bytes(self.root)
        with self.assertRaises(engine.DecisionMapError) as cycle:
            engine.plan(self.root, self.map_id, self.spec("link_dependency", {"decision_id": "DEC-0001", "dependency_id": "DEC-0002"}))
        self.assertEqual("dependency_cycle", cycle.exception.code)
        self.assertEqual(before, self.tree_bytes(self.root))
        with self.assertRaises(engine.DecisionMapError) as open_dependents:
            engine.plan(self.root, self.map_id, self.spec("abandon", {"decision_id": "DEC-0001", "reason": "Drop it"}))
        self.assertEqual("open_dependents", open_dependents.exception.code)
        self.assertEqual(before, self.tree_bytes(self.root))

    def test_missing_cross_map_and_unknown_contract_fields_are_rejected(self) -> None:
        before = self.tree_bytes(self.root)
        invalid_specs = [
            self.spec("add_decision", {"decision_id": "DEC-0001", "question": "Q", "depends_on": ["DEC-9999"]}),
            {"schema_version": 1, "operation_id": "OP-extra", "operation": {"kind": "close_map"}, "extra": True},
            {"schema_version": True, "operation_id": "OP-bool-schema", "operation": {"kind": "close_map"}},
            self.spec("add_fog", {"fog_id": "FOG-00001", "description": "Bad identity"}),
            self.spec("claim", {"decision_id": "DEC-0001", "owner": "worker", "lease_seconds": 86401}),
        ]
        for invalid in invalid_specs:
            with self.subTest(invalid=invalid), self.assertRaises(engine.DecisionMapError):
                engine.plan(self.root, self.map_id, invalid)
        self.assertEqual(before, self.tree_bytes(self.root))

    def test_fog_graduation_is_atomic_and_can_create_an_internal_dag(self) -> None:
        self.commit("add_fog", {"fog_id": "FOG-0001", "description": "Unknown rollout shape"})
        before = self.tree_bytes(self.root)
        bad = self.spec("graduate_fog", {"fog_id": "FOG-0001", "decisions": [{"decision_id": "DEC-0001", "question": "Q", "depends_on": ["DEC-9999"]}]})
        with self.assertRaises(engine.DecisionMapError):
            engine.plan(self.root, self.map_id, bad)
        self.assertEqual(before, self.tree_bytes(self.root))

        result = self.commit("graduate_fog", {"fog_id": "FOG-0001", "decisions": [
            {"decision_id": "DEC-0001", "question": "Pick transport?", "depends_on": []},
            {"decision_id": "DEC-0002", "question": "Pick retry policy?", "depends_on": ["DEC-0001"]},
        ]})
        self.assertEqual(["DEC-0001", "DEC-0002"], result["decision_ids"])
        view = engine.inspect(self.root, self.map_id, "2026-08-01T00:02:00Z")
        self.assertEqual("graduated", view["state"]["fog"]["FOG-0001"]["status"])
        self.assertEqual(["DEC-0001"], view["frontier"])
        with self.assertRaises(engine.DecisionMapError) as repeated:
            engine.plan(self.root, self.map_id, self.spec("graduate_fog", {"fog_id": "FOG-0001", "decisions": [{"decision_id": "DEC-0003", "question": "Again?", "depends_on": []}]}))
        self.assertEqual("fog_not_open", repeated.exception.code)

    def test_lease_expiry_reclaim_and_stale_worker_are_deterministic(self) -> None:
        self.add_decision("DEC-0001")
        first = self.commit("claim", {"decision_id": "DEC-0001", "owner": "worker-a", "lease_seconds": 60}, now="2026-08-01T01:00:00Z")
        token_a = first["token"]
        self.assertGreaterEqual(len(token_a), 32)
        self.assertEqual([], engine.inspect(self.root, self.map_id, "2026-08-01T01:00:59Z")["frontier"])
        self.assertEqual(["DEC-0001"], engine.inspect(self.root, self.map_id, "2026-08-01T01:01:00Z")["frontier"])

        second = self.commit("claim", {"decision_id": "DEC-0001", "owner": "worker-b", "lease_seconds": 60}, now="2026-08-01T01:01:00Z")
        self.assertNotEqual(token_a, second["token"])
        stale = self.spec("resolve", {"decision_id": "DEC-0001", "owner": "worker-a", "token": token_a, "outcome": "Old", "rationale": "Stale", "evidence": []})
        with self.assertRaises(engine.DecisionMapError) as error:
            engine.plan(self.root, self.map_id, stale, "2026-08-01T01:01:01Z")
        self.assertEqual("claim_mismatch", error.exception.code)
        self.commit("resolve", {"decision_id": "DEC-0001", "owner": "worker-b", "token": second["token"], "outcome": "New", "rationale": "Fresh", "evidence": []}, now="2026-08-01T01:01:01Z")
        self.assertEqual("resolved", engine.inspect(self.root, self.map_id)["state"]["decisions"]["DEC-0001"]["status"])

    def test_renew_release_and_direct_resolve(self) -> None:
        self.add_decision("DEC-0001")
        claimed = self.commit("claim", {"decision_id": "DEC-0001", "owner": "worker", "lease_seconds": 10}, now="2026-08-01T02:00:00Z")
        renewed = self.commit("renew", {"decision_id": "DEC-0001", "owner": "worker", "token": claimed["token"], "lease_seconds": 20}, now="2026-08-01T02:00:05Z")
        self.assertEqual("2026-08-01T02:00:30Z", renewed["expires_at"])
        self.commit("release", {"decision_id": "DEC-0001", "owner": "worker", "token": claimed["token"]}, now="2026-08-01T02:00:06Z")
        self.resolve("DEC-0001")
        self.assertEqual("resolved", engine.inspect(self.root, self.map_id)["state"]["decisions"]["DEC-0001"]["status"])

    def test_idempotent_retry_returns_original_claim_and_conflicting_id_fails(self) -> None:
        self.add_decision("DEC-0001")
        operation = self.spec("claim", {"decision_id": "DEC-0001", "owner": "worker", "lease_seconds": 30}, "OP-stable-claim")
        planned = engine.plan(self.root, self.map_id, operation, "2026-08-01T03:00:00Z")
        first = engine.apply(self.root, planned, "2026-08-01T03:00:01Z")
        second = engine.apply(self.root, planned, "2026-08-01T04:00:00Z")
        self.assertFalse(first["idempotent"])
        self.assertTrue(second["idempotent"])
        self.assertEqual(first["token"], second["token"])
        self.assertEqual(first["revision"], second["revision"])
        conflict = self.spec("release", {"decision_id": "DEC-0001", "owner": "worker", "token": first["token"]}, "OP-stable-claim")
        with self.assertRaises(engine.DecisionMapError) as error:
            engine.plan(self.root, self.map_id, conflict, "2026-08-01T03:00:02Z")
        self.assertEqual("operation_id_conflict", error.exception.code)
        self.assertEqual(3, engine.inspect(self.root, self.map_id)["state"]["revision"])

    def test_inspect_plan_verify_are_zero_write(self) -> None:
        before = self.tree_bytes(self.root)
        engine.inspect(self.root, now="2026-08-01T00:00:01Z")
        engine.inspect(self.root, self.map_id, "2026-08-01T00:00:01Z")
        engine.plan(self.root, self.map_id, self.spec("add_fog", {"fog_id": "FOG-0001", "description": "Fog"}), "2026-08-01T00:00:01Z")
        report = engine.verify(self.root, self.map_id, "2026-08-01T00:00:01Z")
        self.assertEqual("ok", report["status"])
        self.assertEqual(before, self.tree_bytes(self.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
