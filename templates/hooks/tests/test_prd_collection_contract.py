from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "Coder/40_Context_Management/references-schema.md"


class PrdCollectionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCHEMA.read_text(encoding="utf-8")

    def test_two_level_indexes_and_per_requirement_history(self) -> None:
        required = (
            ".ai/references/prd/",
            "prd/00_INDEX.md",
            "<prd_id>/00_INDEX.md",
            "<prd_id>/.archive/vN/",
            "项目级需求总索引",
            "单需求索引",
            "版本序列互不相干",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_prd_id_format_and_stability_are_explicit(self) -> None:
        self.assertIn("YYYY-MM-DD-<requirement-slug>", self.text)
        self.assertIn("首次进入当前项目 Butler 体系", self.text)
        self.assertIn("一次分配、终身不变", self.text)
        for forbidden_change in ("PRD 从 v1.0 升到 v1.1", "标题、章节号", "实现代码所在目录移动"):
            with self.subTest(forbidden_change=forbidden_change):
                self.assertIn(forbidden_change, self.text)

    def test_identity_decision_is_closed_and_fail_closed(self) -> None:
        outcomes = re.findall(r"\| `(new-requirement|new-version|duplicate|ambiguous)` \|", self.text)
        self.assertEqual(outcomes, ["new-requirement", "new-version", "duplicate", "ambiguous"])
        self.assertIn("任何动作层都不得用“默认新建”绕过 `ambiguous`", self.text)
        self.assertIn("弱信号不得单独定案", self.text)

    def test_requirement_and_module_identity_are_distinct(self) -> None:
        self.assertIn("prd_id + prd_version + module_slug", self.text)
        self.assertIn("不得把其中一个当另一个使用", self.text)
        self.assertIn("`module_slug` 只在所属 `prd_id` 内唯一", self.text)

    def test_legacy_is_readable_but_not_silently_migrated(self) -> None:
        for marker in ("legacy 单 PRD 结构", "它仍可读", "不得静默创建日期", "MILE-0009 R5"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_non_prd_paths_remain_optional(self) -> None:
        self.assertIn("PRD 需求集合是可选加层", self.text)
        self.assertIn("扁平资料流不变", self.text)
        self.assertIn("`origin/` 用户原稿不因 PRD 集合而被改写、移动或删除", self.text)


if __name__ == "__main__":
    unittest.main()
