from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_workspace_scope_execution_contract_is_registered():
    schema = (ROOT / "Coder/40_Context_Management/workspace-scope-schema.md").read_text(encoding="utf-8")
    tech = (ROOT / "Coder/20_Workflow_Lifecycle/tech-plan-schema.md").read_text(encoding="utf-8")
    verify = (ROOT / "Coder/20_Workflow_Lifecycle/verify-schema.md").read_text(encoding="utf-8")
    readme = (ROOT / "Coder/README.md").read_text(encoding="utf-8")
    for marker in ("## Path Ownership", "## Module Workspace Scope", "# Workspace Write Plan", "check-plan", "check-paths", "check-diff", "PreToolUse"):
        assert marker in schema
    assert "# Workspace Write Plan" in tech
    assert "check-diff" in verify
    assert "workspace-scope-schema.md" in readme and "实际发现和 diff/hook 门禁留 R8" not in readme
    assert "属于 MILE-0009 R8" not in schema
