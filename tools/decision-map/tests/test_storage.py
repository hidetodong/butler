from __future__ import annotations

import fcntl
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE = Path(__file__).resolve().parents[1] / "engine.py"
CLI = MODULE.with_name("decision_map.py")
SPEC = importlib.util.spec_from_file_location("decision_map_storage", MODULE)
assert SPEC and SPEC.loader
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)


class DecisionMapStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-decision-storage-")
        self.root = Path(self.temp.name)
        (self.root / ".ai").mkdir()
        self.map_id = "DMAP-0001"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def spec(self, operation_id: str, kind: str, **fields) -> dict:
        return {"schema_version": 1, "operation_id": operation_id, "operation": {"kind": kind, **fields}}

    def create(self) -> None:
        spec = self.spec("OP-create", "create_map", title="Map", destination="Destination")
        engine.apply(self.root, engine.plan(self.root, self.map_id, spec, "2026-08-01T00:00:00Z"), "2026-08-01T00:00:00Z")

    @staticmethod
    def tree_bytes(root: Path) -> dict[str, bytes]:
        return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}

    def test_stale_plan_is_rejected_without_state_change(self) -> None:
        self.create()
        one = engine.plan(self.root, self.map_id, self.spec("OP-one", "add_fog", fog_id="FOG-0001", description="One"))
        two = engine.plan(self.root, self.map_id, self.spec("OP-two", "add_fog", fog_id="FOG-0002", description="Two"))
        engine.apply(self.root, one)
        before = self.tree_bytes(self.root)
        with self.assertRaises(engine.DecisionMapError) as error:
            engine.apply(self.root, two)
        self.assertEqual("stale_plan", error.exception.code)
        self.assertEqual(1, error.exception.exit_code)
        self.assertEqual(before, self.tree_bytes(self.root))

    def test_nonblocking_lock_conflict_is_safe(self) -> None:
        self.create()
        planned = engine.plan(self.root, self.map_id, self.spec("OP-fog", "add_fog", fog_id="FOG-0001", description="Fog"))
        lock = self.root / ".ai/.decision-map-locks/DMAP-0001.lock"
        descriptor = os.open(lock, os.O_RDWR)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        before = self.tree_bytes(self.root)
        try:
            with self.assertRaises(engine.DecisionMapError) as error:
                engine.apply(self.root, planned)
            self.assertEqual("map_locked", error.exception.code)
            self.assertEqual(before, self.tree_bytes(self.root))
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def test_two_processes_from_one_base_commit_at_most_once(self) -> None:
        self.create()
        plans = []
        for number in (1, 2):
            spec = self.spec(f"OP-concurrent-{number}", "add_fog", fog_id=f"FOG-000{number}", description=f"Fog {number}")
            planned = engine.plan(self.root, self.map_id, spec, "2026-08-01T00:01:00Z")
            path = self.root / f"plan-{number}.json"
            path.write_text(json.dumps(planned), encoding="utf-8")
            plans.append(path)
        processes = [subprocess.Popen([sys.executable, str(CLI), "apply", "--project-root", str(self.root), "--plan", str(path), "--now", "2026-08-01T00:01:01Z"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for path in plans]
        results = [process.communicate() + (process.returncode,) for process in processes]
        self.assertEqual([0, 1], sorted(item[2] for item in results))
        for stdout, stderr, _ in results:
            self.assertEqual("", stderr)
            self.assertIsInstance(json.loads(stdout), dict)
        state = engine.inspect(self.root, self.map_id)["state"]
        self.assertEqual(2, state["revision"])
        self.assertEqual(1, len(state["fog"]))

    def test_update_replace_failure_preserves_original_and_cleans_temp(self) -> None:
        self.create()
        planned = engine.plan(self.root, self.map_id, self.spec("OP-fog", "add_fog", fog_id="FOG-0001", description="Fog"))
        before = self.tree_bytes(self.root)
        with mock.patch.object(engine.os, "replace", side_effect=OSError("injected replace failure")):
            with self.assertRaises(OSError):
                engine.apply(self.root, planned)
        self.assertEqual(before, self.tree_bytes(self.root))
        self.assertEqual(["state.json"], [path.name for path in (self.root / ".ai/decision-maps/DMAP-0001").iterdir()])

    def test_create_rename_failure_leaves_no_visible_or_staged_map(self) -> None:
        planned = engine.plan(self.root, self.map_id, self.spec("OP-create", "create_map", title="Map", destination="Destination"))
        with mock.patch.object(engine.os, "rename", side_effect=OSError("injected rename failure")):
            with self.assertRaises(OSError):
                engine.apply(self.root, planned)
        base = self.root / ".ai/decision-maps"
        self.assertFalse((base / self.map_id).exists())
        self.assertEqual([], list(base.iterdir()))
        self.assertEqual([], engine.inspect(self.root)["maps"])

    def test_symlink_state_and_map_root_fail_closed(self) -> None:
        self.create()
        state = self.root / ".ai/decision-maps/DMAP-0001/state.json"
        real = self.root / "outside.json"
        real.write_bytes(state.read_bytes())
        state.unlink()
        state.symlink_to(real)
        with self.assertRaises(engine.DecisionMapError) as error:
            engine.inspect(self.root, self.map_id)
        self.assertEqual("unsafe_state_path", error.exception.code)

        maps = self.root / ".ai/decision-maps"
        state.unlink()
        (maps / self.map_id).rmdir()
        maps.rmdir()
        maps.symlink_to(self.root)
        with self.assertRaises(engine.DecisionMapError) as root_error:
            engine.inspect(self.root)
        self.assertEqual("unsafe_path", root_error.exception.code)

    def test_verify_reports_staging_and_noncanonical_state_without_writing(self) -> None:
        self.create()
        base = self.root / ".ai/decision-maps"
        (base / ".tmp-DMAP-0002-crash").mkdir()
        state = base / self.map_id / "state.json"
        value = state.read_text(encoding="utf-8")
        state.write_text(value.replace("  \"applied_operations\"", "    \"applied_operations\""), encoding="utf-8")
        before = self.tree_bytes(self.root)
        report = engine.verify(self.root)
        self.assertEqual("error", report["status"])
        self.assertEqual({"stale_staging", "noncanonical_state"}, {item["code"] for item in report["errors"]})
        self.assertEqual(before, self.tree_bytes(self.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
