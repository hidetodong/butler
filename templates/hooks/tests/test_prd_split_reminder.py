"""Unit tests for rules.prd_split_reminder (PostToolUse advisory)."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.io import Advisory, Context
from rules import prd_split_reminder


def make_ctx(cwd: Path, target: str, tool_name: str = "Write") -> Context:
    return Context(
        cwd=str(cwd),
        tool_name=tool_name,
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


class TestPrdSplitReminder:
    def test_milestone_write_without_prd_dir_advises(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        adv = prd_split_reminder.evaluate(make_ctx(tmp_path, ".ai/MILESTONE.md"))
        assert isinstance(adv, Advisory)
        assert adv.rule_id == "prd_split_reminder"
        assert adv.message  # non-empty → will be injected
        assert "references/prd" in adv.message

    def test_milestone_write_with_prd_dir_is_silent(self, tmp_path):
        (tmp_path / ".ai" / "references" / "prd").mkdir(parents=True)
        adv = prd_split_reminder.evaluate(make_ctx(tmp_path, ".ai/MILESTONE.md"))
        assert adv.message == ""  # prd/ exists → no nudge

    def test_non_milestone_target_is_silent(self, tmp_path):
        adv = prd_split_reminder.evaluate(make_ctx(tmp_path, ".ai/CONCEPT.md"))
        assert adv.message == ""

    def test_source_file_target_is_silent(self, tmp_path):
        adv = prd_split_reminder.evaluate(make_ctx(tmp_path, "src/auth.ts"))
        assert adv.message == ""

    def test_edit_tool_on_milestone_also_advises(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        adv = prd_split_reminder.evaluate(
            make_ctx(tmp_path, ".ai/MILESTONE.md", tool_name="Edit")
        )
        assert adv.message

    def test_advisory_has_no_verdict_field(self):
        # Advisory 刻意不带 verdict——它绝不能进 deny 链。
        adv = Advisory(rule_id="x")
        assert not hasattr(adv, "verdict")
