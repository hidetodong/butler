from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "Coder/40_Context_Management/workspace-scope-schema.md"
REFERENCES = ROOT / "Coder/40_Context_Management/references-schema.md"
README = ROOT / "Coder/README.md"


class WorkspaceScopeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCHEMA.read_text(encoding="utf-8")

    def test_project_map_fields_and_stable_key(self) -> None:
        for marker in (".ai/project/workspaces.md", "workspace_key | package_identity | path | kind | status | evidence", "优先直接用它作 `workspace_key`", "目录移动只更新 `path`"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)
        self.assertIn("状态保持 `active`", self.text)
        self.assertNotIn("`active` / `moved` / `retired`", self.text)

    def test_map_failures_are_fail_closed(self) -> None:
        for marker in ("相同 `workspace_key`", "同一规范化路径", "逃出 `PROJECT_ROOT`", "地图不存在或 `retired`", "fail-closed"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_four_scopes_and_write_equation(self) -> None:
        for scope in ("primary_write", "supporting_write", "read_only", "excluded"):
            self.assertIn(scope, self.text)
        self.assertIn("allowed_write = primary_write ∪ supporting_write", self.text)
        self.assertIn("四个集合必须两两互斥", self.text)
        self.assertIn("未声明不是默许", self.text)

    def test_module_scope_can_only_narrow(self) -> None:
        self.assertIn("module.allowed_write    ⊆ requirement.allowed_write", self.text)
        self.assertIn("module.excluded         ⊇ requirement.excluded", self.text)
        self.assertIn("不得把需求级 read-only 提升为 supporting write", self.text)
        self.assertIn("模块四类集合也必须两两互斥", self.text)

    def test_expansion_precedes_write(self) -> None:
        self.assertIn("先停止该越界分支并产出扩张提案", self.text)
        self.assertIn("先更新需求 `Workspace Scope`", self.text)
        self.assertIn("不得先改代码再补范围", self.text)

    def test_single_package_and_permission_layers(self) -> None:
        self.assertIn("`root → .`", self.text)
        self.assertIn("三层取交集", self.text)
        self.assertIn("危险模式冻结的授权上限不会因 `supporting_write` 增加而扩大", self.text)

    def test_registered_and_referenced(self) -> None:
        self.assertIn("workspace-scope-schema.md", README.read_text(encoding="utf-8"))
        references = REFERENCES.read_text(encoding="utf-8")
        self.assertIn("`Workspace Scope`", references)
        self.assertIn("`workspace-scope-schema.md`", references)


if __name__ == "__main__":
    unittest.main()
