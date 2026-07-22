from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_split_runs_identity_gate_before_any_write() -> None:
    text = read("Coder/40_Context_Management/prd-split.md")
    for token in ("new-requirement", "new-version", "duplicate", "ambiguous", "零写", "只有 `new-requirement`"):
        assert token in text
    for forbidden_date_source in ("当前日期", "文件 mtime", "PRD 发布日", "改版日"):
        assert forbidden_date_source in text


def test_split_writes_two_level_collection_and_combines_alignment() -> None:
    text = read("Coder/40_Context_Management/prd-split.md")
    for token in ("<prd_id>/<module_slug>.md", "Workspace Scope", "一次 soft 对齐", "项目级 `prd/00_INDEX.md`", "其他 PRD"):
        assert token in text
    assert "首切不创建 `.archive/`" in text


def test_requirement_index_exposes_machine_readable_identity() -> None:
    text = read("Coder/40_Context_Management/references-schema.md")
    for token in ("## Requirement Identity", "- prd_id:", "- current_version:", "- status:"):
        assert token in text


def test_status_has_read_only_cli_and_filters() -> None:
    rule = read("Coder/40_Context_Management/prd-status.md")
    for token in ("tools/prd-status/prd_status.py", "--prd-id", "--workspace", "零写", "layout: legacy", "exit 2"):
        assert token in rule
    assert (ROOT / "tools/prd-status/tests/test_prd_status.py").is_file()
    assert ".ai/project/workspaces.md" in rule and "retired/未知键" in rule


def test_milestone_pointer_is_prd_qualified_and_legacy_is_read_only() -> None:
    text = read("Coder/20_Workflow_Lifecycle/milestone-schema.md")
    assert "<prd_id>#<module_slug>" in text
    assert "旧的 slug-only 标注仅作历史兼容读取" in text
    assert "references/prd/<prd_id>/<module_slug>.md" in text


def test_both_hosts_route_status_to_same_tool_and_require_update_identity() -> None:
    claude = read(".claude/commands/butler/prd.md")
    codex = read("plugins/butler/skills/butler-prd/SKILL.md")
    for text in (claude, codex):
        assert "prd-status" in text
        assert "--prd-id" in text
        assert "--workspace" in text
        assert "update" in text and "prd_id" in text


def test_coder_directory_and_ci_register_status() -> None:
    readme = read("Coder/README.md")
    ci = read("scripts/verify-ci.sh")
    assert "prd-status.md" in readme
    assert "tools/prd-status/tests" in ci
