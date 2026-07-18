#!/usr/bin/env python3
"""Structural contract tests for TECH_PLAN admission and its consumers."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "Coder/20_Workflow_Lifecycle/tech-plan-schema.md"


class PlanAdmissionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCHEMA.read_text(encoding="utf-8")

    def test_frontmatter_and_closed_states(self) -> None:
        for field in ("方案状态", "方案审查日期", "方案审查方式"):
            self.assertIn(field, self.text)
        declared = self.text.split("`方案状态` 是封闭枚举：", 1)[1].split("。", 1)[0]
        for state in ("draft", "pass", "revise", "blocked"):
            self.assertIn(f"`{state}`", declared)

    def test_all_challenge_dimensions(self) -> None:
        for dimension in (
            "AC Coverage",
            "Assumptions",
            "Alternatives / Trade-offs",
            "Failure Modes",
            "Impact / Scope Challenge",
            "Verification Blind Spots",
            "Verdict",
        ):
            self.assertIn(dimension, self.text)

    def test_pass_is_only_execute_state(self) -> None:
        self.assertIn("进入 P4 的唯一合法状态", self.text)
        self.assertIn("实质修改", self.text)
        self.assertIn("退回 `draft`", self.text)

    def test_legacy_is_not_new_contract(self) -> None:
        self.assertIn("旧版部署兼容", self.text)
        self.assertIn("不是**新方案的合法省略方式", self.text)

    def test_consumers_point_to_single_contract(self) -> None:
        consumers = (
            "Coder/20_Workflow_Lifecycle/lifecycle.md",
            "Coder/20_Workflow_Lifecycle/goal-contract.md",
            "Coder/65_Extension_Dangerous/dangerous-engine.md",
            "templates/rule-card.md",
        )
        for relative in consumers:
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("tech-plan-schema.md", text, relative)

    def test_shared_hook_has_plan_gate(self) -> None:
        hook = (ROOT / "templates/hooks/rules/phase_gate.py").read_text(encoding="utf-8")
        self.assertIn("方案状态|plan_status", hook)
        self.assertIn("PASSED_PLAN_STATE = \"pass\"", hook)
        self.assertIn("legacy allow", hook)

    def test_codex_wrapper_exercises_deny_then_allow(self) -> None:
        wrapper_test = (ROOT / "scripts/verify-codex-hooks.sh").read_text(encoding="utf-8")
        self.assertIn("方案状态: draft", wrapper_test)
        self.assertIn("P3 方案未通过", wrapper_test)
        self.assertIn("方案状态: pass", wrapper_test)


if __name__ == "__main__":
    unittest.main()
