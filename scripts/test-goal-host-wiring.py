#!/usr/bin/env python3
"""End-to-end structural checks for shared Goal host wiring."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GoalHostWiringTests(unittest.TestCase):
    def test_both_entrypoints_receive_same_goal_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            subprocess.run(["python3", str(ROOT / "scripts/render-project-entrypoints.py"), "--target", str(target), "--butler-root", str(ROOT)], check=True, capture_output=True)
            claude = (target / "CLAUDE.md").read_text(encoding="utf-8")
            codex = (target / "AGENTS.md").read_text(encoding="utf-8")
            for token in ("$BUTLER_PATH/tools/goal-assurance/goal.py", "goal-calibration.md", "宿主 complete 不反写"):
                self.assertIn(token, claude)
                self.assertIn(token, codex)

    def test_projection_is_thin_and_one_way(self) -> None:
        contract = (ROOT / "Coder/20_Workflow_Lifecycle/goal-contract.md").read_text(encoding="utf-8")
        for token in ("objective", "state", "blocking reason", "next step", "project `.ai/` → host"):
            self.assertIn(token, contract)

    def test_capability_absence_has_honest_degradation(self) -> None:
        contract = (ROOT / "Coder/20_Workflow_Lifecycle/goal-contract.md").read_text(encoding="utf-8")
        self.assertIn("capability-detect", contract)
        self.assertIn("不建宿主替代文件", contract)
        self.assertIn("task-state.md", contract)

    def test_cold_start_restores_goal_inputs(self) -> None:
        context = (ROOT / "Coder/40_Context_Management/context-persistence.md").read_text(encoding="utf-8")
        for token in ("方案 verdict", "Goal Calibration", "Completion Inputs"):
            self.assertIn(token, context)

    def test_resident_tool_is_documented_for_target_projects(self) -> None:
        deployment = (ROOT / "Coder/20_Workflow_Lifecycle/mcv-deployment.md").read_text(encoding="utf-8")
        self.assertIn("$BUTLER/tools/goal-assurance/goal.py", deployment)
        self.assertTrue((ROOT / "tools/goal-assurance/goal.py").is_file())
        self.assertIn("不得从目标项目 cwd", (ROOT / "Coder/20_Workflow_Lifecycle/lifecycle.md").read_text(encoding="utf-8"))

    def test_registry_workflow_count_and_no_parallel_goal_file(self) -> None:
        registry = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
        self.assertEqual(11, len(registry["workflows"]))
        self.assertFalse((ROOT / ".ai/GOAL.md").exists())
        self.assertFalse((ROOT / ".ai/GOALS.md").exists())

    def test_deployment_status_is_honest(self) -> None:
        compatibility = (ROOT / "docs/codex-compatibility.md").read_text(encoding="utf-8")
        self.assertIn("新部署或显式重渲染", compatibility)
        self.assertIn("当前未发布状态不得称已普遍升级", compatibility)


if __name__ == "__main__":
    unittest.main()
