#!/usr/bin/env python3
"""Structural contract tests for Butler's derived Goal view."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "Coder/20_Workflow_Lifecycle/goal-contract.md"


class GoalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CONTRACT.read_text(encoding="utf-8")

    def test_required_sections(self) -> None:
        self.assertIn("audience: AI / 开发者", self.text)
        self.assertIn("scope:", self.text)
        for heading in (
            "## 2. 两层 Goal 视图",
            "## 3. 派生状态机",
            "## 4. 完成候选不是完成",
            "## 5. 允许与禁止跃迁",
            "## 6. 层级与宿主投影",
            "## 7. 极小任务降级",
        ):
            self.assertIn(heading, self.text)

    def test_closed_state_set(self) -> None:
        states = {"active", "at-risk", "blocked", "completion-candidate", "complete", "abandoned"}
        declared = self.text.split("封闭状态集合：", 1)[1].split("。", 1)[0]
        self.assertEqual(states, {state for state in states if f"`{state}`" in declared})

    def test_existing_sources_are_composed(self) -> None:
        for token in ("CONCEPT.md # Goal", "AC_LIST.md", "TECH_PLAN.md", "task-state.md", "VERIFY_REPORT.md", "review"):
            self.assertIn(token, self.text)

    def test_no_parallel_goal_ledger(self) -> None:
        self.assertIn("不新增 `.ai/GOAL.md`", self.text)
        self.assertIn("不创建 `.ai/GOAL.md`、`.ai/GOALS.md`", self.text)

    def test_completion_shortcuts_are_forbidden(self) -> None:
        for shortcut in ("`active → complete`", "`tasks done → complete`", "`host complete → project complete`"):
            self.assertIn(shortcut, self.text)

    def test_all_consumers_point_to_contract(self) -> None:
        consumers = (
            "Coder/README.md",
            "Coder/20_Workflow_Lifecycle/lifecycle.md",
            "Coder/20_Workflow_Lifecycle/concept-schema.md",
            "Coder/20_Workflow_Lifecycle/acceptance-schema.md",
            "Coder/20_Workflow_Lifecycle/milestone-schema.md",
            "Coder/40_Context_Management/context-persistence.md",
        )
        for relative in consumers:
            self.assertIn("goal-contract.md", (ROOT / relative).read_text(encoding="utf-8"), relative)
        readme = (ROOT / "Coder/README.md").read_text(encoding="utf-8")
        tree = readme.split("## 目录结构", 1)[1].split("```", 2)[1]
        self.assertIn("goal-contract.md", tree)

    def test_milestone_completion_candidate_is_explicit(self) -> None:
        self.assertIn("里程碑对应语义", self.text)
        self.assertIn("最后一个迭代 closed", self.text)


if __name__ == "__main__":
    unittest.main()
