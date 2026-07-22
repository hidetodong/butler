from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_rule_requires_explicit_identity_confirmed_spec_and_dispositions() -> None:
    text = read("Coder/40_Context_Management/prd-update.md")
    for token in (
        "显式给出已登记 `prd_id`", '"confirmed": true', '"origins"', '"removed_slugs"',
        "amend-and-refreeze", "keep-pinned-history", "每个影响 path",
    ):
        assert token in text


def test_rule_defines_zero_write_plan_and_whole_collection_transaction() -> None:
    text = read("Coder/40_Context_Management/prd-update.md")
    for token in (
        "零写 plan", ".prd-update.lock", ".archive/<old_version>",
        ".prd-update-backups/<update_id>", "整 collection 切换", "立即反切换",
    ):
        assert token in text


def test_receipt_verify_rollback_and_idempotence_are_persistent() -> None:
    text = read("Coder/40_Context_Management/prd-update.md")
    for token in (
        ".butler-updates/<update_id>.json", "spec/source/pre/post/archive hashes",
        "changed:false", "rollback", "任何后续 PRD 更新", "路径篡改",
    ):
        assert token in text


def test_update_tool_reuses_status_parser_and_exposes_four_actions() -> None:
    tool = read("tools/prd-update/prd_update.py")
    assert "import prd_status as status_contract" in tool
    for token in ('("plan", "apply")', '("verify", "rollback")', "build_staged_tree", "verify_update", "rollback_update"):
        assert token in tool
    assert (ROOT / "tools/prd-update/tests/test_prd_update.py").is_file()


def test_status_projects_latest_receipt_without_writes() -> None:
    rule = read("Coder/40_Context_Management/prd-status.md")
    tool = read("tools/prd-status/prd_status.py")
    assert "latest_update" in rule and "receipt 畸形即 fail-closed" in rule
    assert "def latest_update" in tool and "UPDATE_RECEIPT_KEYS" in tool


def test_both_hosts_delegate_update_to_same_transaction_tool() -> None:
    claude = read(".claude/commands/butler/prd.md")
    codex = read("plugins/butler/skills/butler-prd/SKILL.md")
    for text in (claude, codex):
        assert "tools/prd-update/prd_update.py" in text
        assert "apply_ready" in text
        assert "plan" in text and "apply" in text


def test_reference_route_coder_index_and_ci_register_update() -> None:
    references = read("Coder/40_Context_Management/references-schema.md")
    coder = read("Coder/README.md")
    ci = read("scripts/verify-ci.sh")
    assert "`tools/prd-update/`" in references
    assert "`tools/prd-update/`" in coder
    assert "tools/prd-update/tests" in ci
