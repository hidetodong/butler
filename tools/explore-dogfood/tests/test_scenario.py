from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("explore_dogfood_scenario_tests", TOOL / "scenario.py")
assert SPEC and SPEC.loader
scenario = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scenario)


class ExploreDogfoodScenarioTests(unittest.TestCase):
    def test_end_to_end_report_is_honest_and_recoverable(self) -> None:
        report = scenario.run_scenario()
        self.assertEqual("ok", report["status"])
        self.assertEqual(["DEC-0001", "DEC-0002"], report["map"]["initial_frontier"])
        self.assertEqual([], report["map"]["final_frontier"])
        self.assertEqual(3, report["map"]["decision_count"])
        self.assertEqual("ok", report["map"]["verify_status"])
        self.assertEqual("parallel", report["work"]["requested_mode"])
        self.assertEqual(["serial", "serial"], report["work"]["actual_modes"])
        self.assertEqual([False, False], report["work"]["fresh_context"])
        self.assertEqual([True, True], report["work"]["absorbable_before_absorb"])
        self.assertFalse(report["work"]["record_changed_map"])
        self.assertEqual(
            {"code": "invalid_digest", "exit_code": 2, "zero_writes": True},
            report["work"]["invalid_digest_probe"],
        )
        self.assertEqual("ok", report["work"]["verify_status"])
        self.assertEqual(0, report["recovery"]["transcript_reads"])
        self.assertEqual(1, report["recovery"]["command_count"])
        self.assertEqual(2, report["recovery"]["attempt_count"])
        self.assertEqual({"DEC-0001": "resolved", "DEC-0002": "resolved", "DEC-0003": "resolved"}, report["recovery"]["decision_statuses"])
        self.assertFalse(report["promotion"]["first_idempotent"])
        self.assertTrue(report["promotion"]["replay_idempotent"])
        self.assertEqual("ok", report["promotion"]["verify_status"])
        self.assertEqual(1, report["promotion"]["receipt_count"])
        self.assertGreaterEqual(report["maintenance"]["persistent_json_files"], 6)

    def test_cli_emits_one_json_document(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOL / "scenario.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(completed.stdout)
        self.assertEqual("ok", report["status"])
        self.assertEqual("PROM-0001", report["promotion"]["promotion_id"])

    def test_live_verifier_proves_refusal_without_semantic_writes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="butler-explore-live-verifier-") as directory:
            root = Path(directory) / "project"
            exercise = scenario.Scenario(root)
            initialized = exercise.initialize_map()
            exercise.research_and_absorb(initialized["claims"])
            (root / ".ai/ITERATIONS.md").write_text(
                "# 迭代台账\n\ncurrent: ITER-0106\n\n"
                "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
                "|---|---|---|---|---|---|---|\n"
                "| ITER-0106 | dogfood | active | 2026-08-02 | — | MILE-0014 | — |\n",
                encoding="utf-8",
            )
            (root / ".ai/MILESTONES.md").write_text(
                "# 里程碑台账\n\ncurrent: MILE-0014\n\n"
                "| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |\n"
                "|---|---|---|---|---|---|---|\n"
                "| MILE-0014 | Explore | active | 2026-08-01 | — | ITER-0106 | — |\n",
                encoding="utf-8",
            )
            (root / ".ai/MILESTONE.md").write_text(
                "# MILESTONE\n\n"
                "| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |\n"
                "|---|---|---|---|\n"
                "| R5 | Router dogfood | ITER-0106 | active |\n",
                encoding="utf-8",
            )
            backlog = root / ".ai/milestone-backlog/codex-structured-question-cards.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text("候办状态: deferred\n", encoding="utf-8")
            report = scenario.verify_persisted(root, "DMAP-0001", "MILE-0014", "R5")
            self.assertEqual("ok", report["status"], report["errors"])
            self.assertEqual({"code": "route_unavailable", "exit_code": 1}, report["promotion_refusal"])
            self.assertTrue(report["zero_semantic_writes"])
            self.assertFalse(report["promotion_receipt_exists"])

    def test_dogfood_report_has_four_complete_observations_and_one_verdict(self) -> None:
        root = TOOL.parents[1]
        report = (root / "docs/explore-dogfood-r5.md").read_text(encoding="utf-8")
        for title in (
            "观测一：跨会话恢复成本",
            "观测二：错误路线与误写",
            "观测三：Research 并行效果",
            "观测四：Map 维护开销",
        ):
            section = report.split(f"## {title}", 1)[1].split("\n## ", 1)[0]
            for field in ("### 口径", "### 原始观测", "### 结论", "### 局限"):
                self.assertIn(field, section)
        self.assertEqual(1, report.count("最终裁决: `defer`"))
        backlog = (root / ".ai/milestone-backlog/codex-structured-question-cards.md").read_text(encoding="utf-8")
        self.assertIn("候办状态: deferred", backlog)


if __name__ == "__main__":
    unittest.main(verbosity=2)
