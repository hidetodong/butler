#!/usr/bin/env python3
"""Structural contract tests for runtime Goal calibration."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "Coder/20_Workflow_Lifecycle/goal-calibration.md"


class GoalCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CONTRACT.read_text(encoding="utf-8")

    def test_six_signal_classes(self) -> None:
        signals = (
            "implementation-deviation", "assumption-invalidated", "scope-drift",
            "verification-failure", "review-finding", "external-blocker",
        )
        declared = self.text.split("## 2. 六类校准信号", 1)[1].split("## 3.", 1)[0]
        for signal in signals:
            self.assertIn(f"`{signal}`", declared)

    def test_projection_fields_and_states(self) -> None:
        for field in ("ID", "Signal", "Fact Source", "Goal Impact", "Route", "Status"):
            self.assertIn(field, self.text)
        for state in ("open / blocked / resolved", "可重算"):
            self.assertIn(state, self.text)
        self.assertIn("不造占位数据行", self.text)
        self.assertIn("不能冒充 Signal/Status 枚举值", self.text)

    def test_routes_cover_all_phases_and_stop(self) -> None:
        routing = self.text.split("## 4. 按事实性质回流", 1)[1].split("## 5.", 1)[0]
        for route in ("P1", "P2", "P3", "P4", "P5", "honest stop"):
            self.assertIn(route, routing)

    def test_goal_impact_and_resolution_evidence(self) -> None:
        self.assertIn("Goal 至少 `at-risk`", self.text)
        self.assertIn("→ `blocked`", self.text)
        self.assertIn("新 passed evidence", self.text)
        self.assertIn("定点复查", self.text)

    def test_shortcuts_are_forbidden(self) -> None:
        for shortcut in (
            "`tasks done → ignore signal`", "`risk noted → continue old plan`",
            "`delete row → resolved`", "`closed history → reopen`",
        ):
            self.assertIn(shortcut, self.text)

    def test_consumers_point_to_contract(self) -> None:
        consumers = (
            "Coder/README.md",
            "Coder/20_Workflow_Lifecycle/lifecycle.md",
            "Coder/20_Workflow_Lifecycle/goal-contract.md",
            "Coder/30_Quality_Gate/correction-contract.md",
            "Coder/40_Context_Management/context-persistence.md",
            "Coder/20_Workflow_Lifecycle/verify-schema.md",
            "Coder/60_Extension_CodeReview/review-engine.md",
            "Coder/65_Extension_Dangerous/dangerous-engine.md",
            "templates/rule-card.md",
        )
        for relative in consumers:
            self.assertIn("goal-calibration.md", (ROOT / relative).read_text(encoding="utf-8"), relative)

    def test_readme_tree_registers_contract(self) -> None:
        readme = (ROOT / "Coder/README.md").read_text(encoding="utf-8")
        tree = readme.split("## 目录结构", 1)[1].split("```", 2)[1]
        self.assertIn("goal-calibration.md", tree)

    def test_current_empty_projection_has_no_fake_signal_row(self) -> None:
        task_state = (ROOT / ".ai/task-state.md").read_text(encoding="utf-8")
        section = task_state.split("# Goal Calibration", 1)[1]
        self.assertIn("当前无未闭合运行时信号（N/A）", section)
        self.assertNotIn("| — | 当前无", section)


if __name__ == "__main__":
    unittest.main()
