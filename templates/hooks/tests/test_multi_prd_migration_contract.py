from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_acceptance_uses_multi_prd_pin_and_keeps_legacy_read_only() -> None:
    text = read("Coder/20_Workflow_Lifecycle/acceptance-schema.md")
    for token in ("prd_refs", "prd_id", "prd_version", "module_slugs", "两字段禁止并存", "legacy", "migration receipt"):
        assert token in text
    assert "prd/<prd_id>/.archive/<prd_version>/<module_slug>.md" in text


def test_plan_and_verify_inherit_the_acceptance_pin() -> None:
    plan = read("Coder/20_Workflow_Lifecycle/tech-plan-schema.md")
    verify = read("Coder/20_Workflow_Lifecycle/verify-schema.md")
    assert "逐项继承 `AC_LIST.md` 的 `prd_refs`" in plan
    assert "不得跨需求借同名模块" in verify
    assert "migration receipt" in plan and "migration receipt" in verify


def test_reference_schema_registers_transaction_and_resolver() -> None:
    text = read("Coder/40_Context_Management/references-schema.md")
    for token in ("tools/prd-migrate/prd_migrate.py", "inspect/plan", "staging/backup/rename", ".butler-migration.json", "不回写"):
        assert token in text


def test_human_guide_is_complete_and_linked() -> None:
    guide = read("docs/prd-migration-guide.md")
    for heading in ("迁移前盘点", "确定日期化 `prd_id`", "MILESTONE 与 AC", "执行事务迁移", "迁移后验证", "失败恢复"):
        assert heading in guide
    for command in (" inspect ", " plan ", " apply ", " verify ", " resolve ", " rollback "):
        assert command in guide
    assert "docs/prd-migration-guide.md" in read("HUMAN_GUIDE.md")


def test_tool_and_behavior_tests_are_registered() -> None:
    assert (ROOT / "tools/prd-migrate/prd_migrate.py").is_file()
    assert (ROOT / "tools/prd-migrate/tests/test_prd_migrate.py").is_file()
