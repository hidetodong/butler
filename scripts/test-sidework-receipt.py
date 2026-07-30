#!/usr/bin/env python3
"""Structural contract tests for Butler sidework receipts."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "Coder/40_Context_Management/sidework-receipt.md"
TEMPLATE = ROOT / "templates/sidework-receipt.md"


class SideworkReceiptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rule = RULE.read_text(encoding="utf-8")
        cls.template = TEMPLATE.read_text(encoding="utf-8")

    def test_rule_is_registered_context_contract(self) -> None:
        self.assertIn("audience: AI / 开发者", self.rule)
        self.assertIn("scope:", self.rule)
        readme = (ROOT / "Coder/README.md").read_text(encoding="utf-8")
        self.assertIn("sidework-receipt.md", readme)
        self.assertIn("触发式读取", readme)
        self.assertIn("不扫描目录猜待办", readme)

    def test_template_has_fixed_sections_and_table(self) -> None:
        expected = [
            "用户发起的目标",
            "成果结论",
            "成果与改动位置",
            "验证事实",
            "对主线的影响",
            "主 Agent 续接入口",
        ]
        self.assertEqual(expected, re.findall(r"^## (.+)$", self.template, re.MULTILINE))
        self.assertIn("| 类型 | 路径 / 提交 / 补丁 | 说明 |", self.template)
        self.assertIn("{{标题}}", self.template)
        self.assertIn("{{项目内路径或稳定指针}}", self.template)

    def test_mixed_outputs_and_pointer_only_rule_are_explicit(self) -> None:
        for token in (
            "代码改动、调研、方案、实验结论和验证证据",
            "同一份回执可以混装",
            "不复制正文",
            "共享工作区",
            "不能冒称作者归属或独立提交",
        ):
            self.assertIn(token, self.rule)

    def test_producer_cannot_write_mainline_state(self) -> None:
        for protected in (
            ".ai/CONCEPT.md",
            ".ai/AC_LIST.md",
            ".ai/TECH_PLAN.md",
            ".ai/VERIFY_REPORT.md",
            ".ai/task-state.md",
            ".ai/02_SESSION_HANDOFF.md",
        ):
            self.assertIn(f"`{protected}`", self.rule)
        self.assertIn("不自行写入主线状态文件", self.rule)

    def test_receipt_is_not_write_authorization(self) -> None:
        for token in (
            "不是代码写入授权或流程绕过",
            "当前 Butler 阶段门禁和项目范围约束",
            "不得设置 `BUTLER_BYPASS`",
            "回执本身不提供额外写权限",
        ):
            self.assertIn(token, self.rule)

    def test_user_keeps_decision_and_controls_consumption(self) -> None:
        for token in (
            "模型不建立“接受 / 拒绝”状态",
            "用户显式给出回执路径",
            "不在冷启动或每轮对话自动扫描",
            "需要用户决定的问题",
        ):
            self.assertIn(token, self.rule)

    def test_path_collision_and_escape_rules_are_explicit(self) -> None:
        for token in (
            "$PROJECT_ROOT/.ai/sidework/<YYYY-MM-DD>-<slug>.md",
            "只新建，绝不覆盖",
            "依次尝试 `-2`、`-3`",
            "create-only（只创建）",
            "并发创建返回“已存在”",
            "符号链接",
            "路径逃出项目根",
        ):
            self.assertIn(token, self.rule)

    def test_human_guide_has_both_user_actions(self) -> None:
        guide = (ROOT / "HUMAN_GUIDE.md").read_text(encoding="utf-8")
        for token in (
            "把旁路 Agent 的成果钩回主线",
            ".ai/sidework/",
            "这是一项旁路工作",
            "接回这份旁路工作",
            "templates/sidework-receipt.md",
        ):
            self.assertIn(token, guide)

    def test_full_ci_runs_contract_test(self) -> None:
        ci = (ROOT / "scripts/verify-ci.sh").read_text(encoding="utf-8")
        self.assertIn('python "$ROOT/scripts/test-sidework-receipt.py"', ci)


if __name__ == "__main__":
    unittest.main()
