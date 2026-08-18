from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tools/context-budget/context_budget.py"
SPEC = importlib.util.spec_from_file_location("context_budget", MODULE_PATH)
assert SPEC and SPEC.loader
context_budget = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = context_budget
SPEC.loader.exec_module(context_budget)


class ContextBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in (
            "Coder/README.md",
            "AGENTS.md",
            "templates/rule-card.md",
            "Coder/domain-model.md",
            "Coder/domain-glossary.md",
            "Coder/context-map.md",
            "Coder/architecture-overview.md",
            ".ai/project/invariants.md",
            ".ai/debt.md",
            ".ai/iterations/ITER-0107/AC_LIST.md",
            "deliveries/ITER-0107-domain-model-boundaries.md",
        ):
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        pointer_text = "\n".join(
            (self.root / relative).read_text(encoding="utf-8")
            for relative in ("Coder/domain-glossary.md", "Coder/context-map.md")
        )
        for raw in context_budget.MD_POINTER_RE.findall(pointer_text):
            target = self.root / raw.split("#", 1)[0]
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# fixture\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _replace(self, relative: str, old: str, new: str) -> None:
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_repository_baseline_passes(self) -> None:
        result = context_budget.check_project(self.root)
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.metrics["contexts"], 5)
        self.assertEqual(result.metrics["terms"], 19)
        self.assertEqual(result.metrics["routes"], 4)
        self.assertEqual(result.metrics["fact_classes"], 4)
        self.assertEqual(result.metrics["transitions"], 5)

    def test_l0_budget_and_markers_fail_closed(self) -> None:
        self._replace(
            "Coder/README.md",
            context_budget.L0_END,
            ("扩张" * 900) + "\\n" + context_budget.L0_END,
        )
        result = context_budget.check_project(self.root)
        self.assertIn("L0 bytes=", "\n".join(result.errors))

        self._replace("Coder/README.md", context_budget.L0_BEGIN, "")
        with self.assertRaisesRegex(ValueError, "markers"):
            context_budget.check_project(self.root)

    def test_l0_projection_mismatch_names_the_file(self) -> None:
        for relative in context_budget.L0_PROJECTIONS:
            with self.subTest(relative=relative):
                self.tearDown()
                self.setUp()
                self._replace(relative, "停在本入口", "停在别的入口")
                result = context_budget.check_project(self.root)
                joined = "\n".join(result.errors)
                self.assertIn("L0 projection mismatch", joined)
                self.assertIn(relative, joined)

    def test_l0_source_edit_breaks_both_projections(self) -> None:
        self._replace(context_budget.L0_SOURCE, "停在本入口", "停在别的入口")
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        for relative in context_budget.L0_PROJECTIONS:
            self.assertIn(relative, joined)

    def test_l0_projection_missing_markers_fail_closed(self) -> None:
        self._replace("AGENTS.md", context_budget.L0_END, "")
        with self.assertRaisesRegex(ValueError, "AGENTS.md"):
            context_budget.check_project(self.root)

    def test_l1_context_pointer_and_recursion_guards(self) -> None:
        self._replace("Coder/domain-model.md", "| 知识连续性 |", "| 错误上下文 |")
        result = context_budget.check_project(self.root)
        self.assertIn("L1 contexts mismatch", "\n".join(result.errors))

        self._replace("Coder/domain-model.md", "禁止递归追随引用", "允许递归")
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden pattern", joined)
        self.assertIn("no-recursion guard", joined)

    def test_l2_count_empty_cell_and_bad_source_fail(self) -> None:
        glossary = self.root / "Coder/domain-glossary.md"
        lines = glossary.read_text(encoding="utf-8").splitlines()
        row_index = next(i for i, line in enumerate(lines) if line.startswith("| Handoff |"))
        lines.pop(row_index)
        glossary.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = context_budget.check_project(self.root)
        self.assertIn("L2 term count=18", "\n".join(result.errors))

        self._replace("Coder/domain-glossary.md", "| PRD | 需求与范围 |", "| PRD |  |")
        self._replace(
            "Coder/domain-glossary.md",
            "`Coder/40_Context_Management/workspace-scope-schema.md`",
            "`Coder/missing-source.md`",
        )
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        self.assertIn("empty required cell", joined)
        self.assertIn("invalid definition source", joined)

    def test_missing_receipt_field_and_duplicate_table_fail(self) -> None:
        self._replace("Coder/domain-model.md", "- 选择理由", "- 其他说明")
        architecture = self.root / "Coder/architecture-overview.md"
        architecture.write_text(
            architecture.read_text(encoding="utf-8")
            + "\n| 概念 | 上下文限定 | 白话定义 |\n",
            encoding="utf-8",
        )
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        self.assertIn("fan-out receipt", joined)
        self.assertIn("duplicate glossary table", joined)

    def test_definition_source_symlink_cannot_escape_project(self) -> None:
        outside = Path(self.temp.name).parent / "outside-context-source.md"
        outside.write_text("# outside\n", encoding="utf-8")
        escaped = self.root / "Coder/escaped-source.md"
        escaped.symlink_to(outside)
        self.addCleanup(outside.unlink, missing_ok=True)
        self._replace(
            "Coder/domain-glossary.md",
            "`Coder/40_Context_Management/references-schema.md`",
            "`Coder/escaped-source.md`",
        )
        result = context_budget.check_project(self.root)
        self.assertIn("invalid definition source", "\n".join(result.errors))

    def test_context_map_transition_and_fields_fail_closed(self) -> None:
        self._replace("Coder/context-map.md", "### PRD→AC", "### 未知转换")
        result = context_budget.check_project(self.root)
        self.assertIn("transitions mismatch", "\n".join(result.errors))

        self._replace("Coder/context-map.md", "### 未知转换", "### PRD→AC")
        self._replace("Coder/context-map.md", "- 最小保真：", "- 其他字段：")
        result = context_budget.check_project(self.root)
        self.assertIn("fields mismatch", "\n".join(result.errors))

    def test_context_map_authority_repair_and_source_guards(self) -> None:
        self._replace(
            "Coder/context-map.md",
            "受控投影 → 权威事实；AC 钉版后不被 PRD live 反向改写",
            "未知事实 + 受控投影 → 权威事实；混入未知分类",
        )
        self._replace(
            "Coder/context-map.md",
            "→ 修复：`Coder/20_Workflow_Lifecycle/acceptance-schema.md`",
            "→ 处理：`Coder/20_Workflow_Lifecycle/acceptance-schema.md`",
        )
        self._replace(
            "Coder/context-map.md",
            "`Coder/40_Context_Management/references-schema.md`；`Coder/20_Workflow_Lifecycle/acceptance-schema.md`",
            "`Coder/missing-context-source.md`；`Coder/20_Workflow_Lifecycle/acceptance-schema.md`",
        )
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        self.assertIn("invalid authority relation", joined)
        self.assertIn("exactly one repair source", joined)
        self.assertIn("invalid direct source", joined)

        architecture = self.root / "Coder/architecture-overview.md"
        architecture.write_text(
            architecture.read_text(encoding="utf-8")
            + "\n### PRD→AC\n- 源上下文：需求与范围\n",
            encoding="utf-8",
        )
        result = context_budget.check_project(self.root)
        self.assertIn("duplicate context-map block", "\n".join(result.errors))

    def test_context_map_duplicate_recursion_and_budget_fail_closed(self) -> None:
        self._replace("Coder/context-map.md", "### AC→TECH_PLAN", "### PRD→AC")
        with self.assertRaisesRegex(ValueError, "duplicate transition"):
            context_budget.check_project(self.root)

        self._replace("Coder/context-map.md", "### PRD→AC", "### AC→TECH_PLAN")
        self._replace("Coder/context-map.md", "禁止递归追随引用", "允许递归追随引用")
        context_map = self.root / "Coder/context-map.md"
        context_map.write_text(
            context_map.read_text(encoding="utf-8") + ("膨胀" * 1600),
            encoding="utf-8",
        )
        result = context_budget.check_project(self.root)
        joined = "\n".join(result.errors)
        self.assertIn("context-map bytes=", joined)
        self.assertIn("missing progressive-loading guards", joined)
        self.assertIn("forbidden pattern", joined)


if __name__ == "__main__":
    unittest.main()
