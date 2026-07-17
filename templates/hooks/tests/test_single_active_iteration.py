"""Unit tests for rules.single_active_iteration."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.io import Context
from rules import single_active_iteration as sai

LEDGER = ".ai/ITERATIONS.md"
SEP = "|---|---|---|---|---|---|---|\n"
HEADER = (
    "# 迭代台账\n\n"
    "current: {cur}\n\n"
    "| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |\n"
) + SEP

ROW_ACTIVE_1 = "| ITER-0001 | t | active | 2026-01-01 | — | — | — |"
ROW_CLOSED_1 = "| ITER-0001 | t | closed | 2026-01-01 | 2026-01-02 | — | deliveries/ITER-0001-x.md |"
ROW_ACTIVE_2 = "| ITER-0002 | t | active | 2026-01-03 | — | — | — |"
ROW_CLOSED_2 = "| ITER-0002 | t | closed | 2026-01-03 | 2026-01-04 | — | deliveries/ITER-0002-x.md |"
ROW_ACTIVE_3 = "| ITER-0003 | t | active | 2026-01-05 | — | — | — |"


def _table(cur: str, *rows: str) -> str:
    return HEADER.format(cur=cur) + "".join(r + "\n" for r in rows)


def write_ctx(content: str, target: str = LEDGER) -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="Write",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target, "content": content},
    )


def edit_ctx(old: str, new: str, cwd: str, target: str = LEDGER) -> Context:
    return Context(
        cwd=cwd,
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target, "old_string": old, "new_string": new},
    )


def multiedit_ctx(pairs: list[tuple[str, str]], cwd: str, target: str = LEDGER) -> Context:
    return Context(
        cwd=cwd,
        tool_name="MultiEdit",
        target_path=PurePosixPath(target),
        tool_input={
            "file_path": target,
            "edits": [{"old_string": o, "new_string": n} for o, n in pairs],
        },
    )


def patch_ctx(removed: list[str], added: list[str], cwd: str) -> Context:
    return Context(
        cwd=cwd,
        tool_name="apply_patch",
        target_path=PurePosixPath(LEDGER),
        tool_input={
            "file_path": LEDGER,
            "butler_patch_removed": removed,
            "butler_patch_added": added,
        },
    )


def _seed(tmp_path: Path, content: str) -> str:
    ledger = tmp_path / ".ai" / "ITERATIONS.md"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(content, encoding="utf-8")
    return str(tmp_path)


class TestWrite:
    def test_single_active_allows(self):
        d = sai.evaluate(write_ctx(_table("ITER-0002", ROW_ACTIVE_2, ROW_CLOSED_1)))
        assert d.verdict == "allow"
        assert d.rule_id == "single_active_iteration"

    def test_two_active_denies(self):
        d = sai.evaluate(write_ctx(_table("ITER-0002", ROW_ACTIVE_2, ROW_ACTIVE_1)))
        assert d.verdict == "deny"
        assert "ITER-0001" in d.reason and "ITER-0002" in d.reason
        assert "iteration-schema" in d.remediation

    def test_zero_active_allows(self):
        d = sai.evaluate(write_ctx(_table("none", ROW_CLOSED_1, ROW_CLOSED_2)))
        assert d.verdict == "allow"

    def test_header_only_allows(self):
        assert sai.evaluate(write_ctx(HEADER.format(cur="none"))).verdict == "allow"

    def test_empty_allows(self):
        assert sai.evaluate(write_ctx("")).verdict == "allow"

    def test_non_ledger_path_allows(self):
        # 同样含双 active，但目标不是迭代台账 → 不校验。
        content = _table("ITER-0002", ROW_ACTIVE_2, ROW_ACTIVE_1)
        assert sai.evaluate(write_ctx(content, target=".ai/CONCEPT.md")).verdict == "allow"

    def test_uppercase_active_counts(self):
        row = "| ITER-0002 | t | Active | 2026-01-03 | — | — | — |"
        d = sai.evaluate(write_ctx(_table("ITER-0002", row, ROW_ACTIVE_1)))
        assert d.verdict == "deny"


class TestEdit:
    def test_open_after_close_allows(self, tmp_path):
        cwd = _seed(tmp_path, _table("none", ROW_CLOSED_1))
        d = sai.evaluate(edit_ctx(SEP, SEP + ROW_ACTIVE_2 + "\n", cwd))
        assert d.verdict == "allow"

    def test_open_without_close_denies(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(edit_ctx(SEP, SEP + ROW_ACTIVE_2 + "\n", cwd))
        assert d.verdict == "deny"
        assert "ITER-0001" in d.reason and "ITER-0002" in d.reason

    def test_close_active_allows(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(edit_ctx(ROW_ACTIVE_1, ROW_CLOSED_1, cwd))
        assert d.verdict == "allow"

    def test_uncertainty_old_not_found_allows(self, tmp_path):
        # old_string 未命中 → 退化为片段（1 active）→ 放行，不误杀。
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(edit_ctx("NONEXISTENT", ROW_ACTIVE_2, cwd))
        assert d.verdict == "allow"

    def test_fragment_two_active_denies(self, tmp_path):
        # 即便退化，片段自身含双 active 也拒。
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        frag = ROW_ACTIVE_2 + "\n" + ROW_ACTIVE_3
        d = sai.evaluate(edit_ctx("NONEXISTENT", frag, cwd))
        assert d.verdict == "deny"

    def test_missing_ledger_file_fallback_allows(self, tmp_path):
        # 无 .ai/ITERATIONS.md（读失败）→ 退化片段（1 active）→ 放行。
        d = sai.evaluate(edit_ctx("x", ROW_ACTIVE_2, str(tmp_path)))
        assert d.verdict == "allow"


class TestMultiEdit:
    def test_close_then_open_allows(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(
            multiedit_ctx(
                [(ROW_ACTIVE_1, ROW_CLOSED_1), (SEP, SEP + ROW_ACTIVE_2 + "\n")], cwd
            )
        )
        assert d.verdict == "allow"

    def test_open_only_denies(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(multiedit_ctx([(SEP, SEP + ROW_ACTIVE_2 + "\n")], cwd))
        assert d.verdict == "deny"
        assert "ITER-0002" in d.reason


class TestApplyPatch:
    def test_open_without_close_denies(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(patch_ctx([], [ROW_ACTIVE_2], cwd))
        assert d.verdict == "deny"

    def test_close_old_and_open_new_same_patch_allows(self, tmp_path):
        cwd = _seed(tmp_path, _table("ITER-0001", ROW_ACTIVE_1))
        d = sai.evaluate(
            patch_ctx([ROW_ACTIVE_1], [ROW_CLOSED_1, ROW_ACTIVE_2], cwd)
        )
        assert d.verdict == "allow"
