"""Unit tests for rules.ledger_status."""
from __future__ import annotations

from pathlib import PurePosixPath

from lib.io import Context
from rules import ledger_status

LEDGER = ".ai/ITERATIONS.md"


def make_ctx(target: str, content: str, tool: str = "Write") -> Context:
    key = "content" if tool == "Write" else "new_string"
    return Context(
        cwd="/tmp/proj",
        tool_name=tool,
        target_path=PurePosixPath(target),
        tool_input={"file_path": target, key: content},
    )


def make_multiedit_ctx(target: str, new_strings: list[str]) -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="MultiEdit",
        target_path=PurePosixPath(target),
        tool_input={
            "file_path": target,
            "edits": [{"old_string": "x", "new_string": ns} for ns in new_strings],
        },
    )


HEADER = (
    "# 迭代台账\n\n"
    "current: ITER-0002\n\n"
    "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
    "|---|---|---|---|---|---|---|\n"
)


def _table(*rows: str) -> str:
    return HEADER + "".join(r + "\n" for r in rows)


class TestLedgerStatus:
    def test_valid_states_allow(self):
        content = _table(
            "| ITER-0002 | t | active | 2026-01-01 | — | — | — |",
            "| ITER-0001 | t | closed | 2026-01-01 | 2026-01-02 | — | deliveries/ITER-0001-x.md |",
        )
        d = ledger_status.evaluate(make_ctx(LEDGER, content))
        assert d.verdict == "allow"
        assert d.rule_id == "ledger_status"

    def test_abandoned_allows(self):
        content = _table("| ITER-0003 | t | abandoned | 2026-01-01 | — | — | — |")
        assert ledger_status.evaluate(make_ctx(LEDGER, content)).verdict == "allow"

    def test_planned_denies(self):
        content = _table("| ITER-0004 | t | planned | 2026-01-01 | — | — | — |")
        d = ledger_status.evaluate(make_ctx(LEDGER, content))
        assert d.verdict == "deny"
        assert d.rule_id == "ledger_status"
        assert "ITER-0004" in d.reason
        assert "planned" in d.reason
        assert "milestone-schema" in d.remediation

    def test_draft_denies(self):
        # draft 是 AC_LIST 的状态，对迭代行非法。
        content = _table("| ITER-0005 | t | draft | 2026-01-01 | — | — | — |")
        assert ledger_status.evaluate(make_ctx(LEDGER, content)).verdict == "deny"

    def test_non_ledger_path_allows(self):
        # 同样含 planned 文本，但目标不是迭代台账 → 不校验。
        content = "| ITER-0004 | t | planned | x | x | x | x |"
        d = ledger_status.evaluate(make_ctx(".ai/CONCEPT.md", content))
        assert d.verdict == "allow"

    def test_edit_new_string_planned_denies(self):
        row = "| ITER-0006 | t | planned | 2026-01-01 | — | — | — |"
        d = ledger_status.evaluate(make_ctx(LEDGER, row, tool="Edit"))
        assert d.verdict == "deny"

    def test_edit_new_string_valid_allows(self):
        row = "| ITER-0006 | t | active | 2026-01-01 | — | — | — |"
        d = ledger_status.evaluate(make_ctx(LEDGER, row, tool="Edit"))
        assert d.verdict == "allow"

    def test_multiedit_planned_denies(self):
        d = ledger_status.evaluate(
            make_multiedit_ctx(
                LEDGER,
                [
                    "| ITER-0007 | t | closed | 2026-01-01 | 2026-01-02 | — | d.md |",
                    "| ITER-0008 | t | planned | 2026-01-03 | — | — | — |",
                ],
            )
        )
        assert d.verdict == "deny"
        assert "ITER-0008" in d.reason

    def test_header_and_separator_only_allows(self):
        # 仅表头 + 分隔行，无数据行 → 不应误杀。
        assert ledger_status.evaluate(make_ctx(LEDGER, HEADER)).verdict == "allow"

    def test_empty_status_cell_allows(self):
        # 半写行：状态列空 → 放行。
        content = _table("| ITER-0009 | t |  | 2026-01-01 | — | — | — |")
        assert ledger_status.evaluate(make_ctx(LEDGER, content)).verdict == "allow"

    def test_uppercase_status_allows(self):
        content = _table("| ITER-0010 | t | Active | 2026-01-01 | — | — | — |")
        assert ledger_status.evaluate(make_ctx(LEDGER, content)).verdict == "allow"

    def test_non_iter_row_skipped(self):
        # 第一单元格不是 ITER-NNNN（如说明性行）→ 跳过，不校验其第三列。
        content = HEADER + "| 备注 | 说明 | planned 只是举例 | x | x | x | x |\n"
        assert ledger_status.evaluate(make_ctx(LEDGER, content)).verdict == "allow"

    def test_empty_content_allows(self):
        assert ledger_status.evaluate(make_ctx(LEDGER, "")).verdict == "allow"

    def test_apply_patch_added_invalid_status_denies(self):
        ctx = Context(
            cwd="/tmp/proj",
            tool_name="apply_patch",
            target_path=PurePosixPath(LEDGER),
            tool_input={
                "butler_patch_added": [
                    "| ITER-0011 | t | planned | 2026-01-01 | — | — | — |"
                ]
            },
        )
        assert ledger_status.evaluate(ctx).verdict == "deny"
