#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("iteration_intake", Path(__file__).with_name("intake.py"))
assert SPEC and SPEC.loader
intake = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(intake)


def valid_spec() -> dict:
    return {"title": "Semantic router", "summary": "Agreed to add one router.", "confirmed_decisions": ["Support Claude and Codex"], "model_recommendations": ["Use registry v2"], "open_questions": [], "in_scope": ["Add router"], "out_of_scope": ["Pi router"], "milestone_route": None}


class IntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-intake-")
        self.root = Path(self.temp.name) / "project"
        ai = self.root / ".ai"
        ai.mkdir(parents=True)
        (ai / "ITERATIONS.md").write_text("# 迭代台账\n\ncurrent: none\n\n| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n|---|---|---|---|---|---|---|\n| ITER-0042 | old | closed | 2026-01-01 | 2026-01-01 | — | x |\n", encoding="utf-8")
        (ai / "MILESTONES.md").write_text("# 里程碑台账\n\ncurrent: none\n", encoding="utf-8")
        for name in intake.LIVE:
            (ai / name).write_text(f"old {name}\n", encoding="utf-8")
        (ai / "task-state.md").write_text("old state\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_plan_is_zero_write_and_uses_composite_max(self) -> None:
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = intake.plan(self.root, valid_spec())
        self.assertEqual("ready", result["status"])
        self.assertEqual("ITER-0043", result["iteration"])
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_active_iteration_refuses_without_new_id(self) -> None:
        ledger = self.root / ".ai/ITERATIONS.md"
        ledger.write_text(ledger.read_text().replace("current: none", "current: ITER-0042").replace("| closed |", "| active |"), encoding="utf-8")
        result = intake.plan(self.root, valid_spec())
        self.assertEqual("active-exists", result["status"])
        self.assertEqual([], result["writes"])

    def test_active_milestone_requires_and_binds_a_planned_route(self) -> None:
        ai = self.root / ".ai"
        (ai / "MILESTONES.md").write_text("# 里程碑台账\n\ncurrent: MILE-0002\n\n| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n|---|---|---|---|---|---|---|\n| MILE-0002 | M | active | 2026-01-01 | — | — | — |\n", encoding="utf-8")
        (ai / "MILESTONE.md").write_text("| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |\n|---|---|---|---|\n| R1 | Router | — | planned |\n", encoding="utf-8")
        spec = valid_spec(); spec["milestone_route"] = None
        self.assertEqual("needs-milestone-route", intake.plan(self.root, spec)["status"])
        spec["milestone_route"] = "R1"
        with mock.patch.object(intake, "sync_state"):
            result = intake.apply(self.root, spec)
        self.assertEqual("MILE-0002", result["milestone"])
        self.assertIn("| R1 | Router | ITER-0043 | active |", (ai / "MILESTONE.md").read_text())
        self.assertIn("| MILE-0002 | M | active | 2026-01-01 | — | ITER-0043 | — |", (ai / "MILESTONES.md").read_text())

    def test_apply_rolls_back_every_ai_file_on_failure(self) -> None:
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with self.assertRaises(RuntimeError), mock.patch.object(intake, "sync_state"):
            intake.apply(self.root, valid_spec(), after_write=lambda: (_ for _ in ()).throw(RuntimeError("injected")))
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_apply_crystallizes_without_raw_transcript(self) -> None:
        with mock.patch.object(intake, "sync_state"):
            result = intake.apply(self.root, valid_spec())
        self.assertEqual("applied", result["status"])
        concept = (self.root / ".ai/CONCEPT.md").read_text(encoding="utf-8")
        self.assertIn("已确认：Support Claude and Codex", concept)
        self.assertIn("建议（未确认）：Use registry v2", concept)
        self.assertNotIn("transcript", concept.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
