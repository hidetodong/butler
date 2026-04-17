"""Unit tests for lib.bypass."""
from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

import pytest

from lib.bypass import evaluate_bypass
from lib.io import Context, Decision


def make_ctx(cwd: Path, target: str = "src/auth.ts") -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


DENY = Decision(
    verdict="deny",
    rule_id="phase_gate",
    reason="缺 .ai/CONCEPT.md",
    remediation="先完成 P1",
)

ALLOW = Decision(verdict="allow", rule_id="phase_gate")


class TestBypassEnvUnset:
    def test_returns_original_decision(self, tmp_path, monkeypatch):
        monkeypatch.delenv("BUTLER_BYPASS", raising=False)
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"
        assert result.rule_id == "phase_gate"

    def test_pass_through_allow_unchanged(self, tmp_path, monkeypatch):
        monkeypatch.delenv("BUTLER_BYPASS", raising=False)
        result = evaluate_bypass(make_ctx(tmp_path), ALLOW)
        assert result.verdict == "allow"


class TestBypassEnvSetButNoReason:
    def test_missing_reason_file_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        # no .ai/bypass-reason.md
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"
        assert "bypass-reason.md" in result.reason

    def test_empty_reason_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"

    def test_whitespace_only_reason_stays_deny(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("   \n\t\n")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "deny"


class TestBypassSuccess:
    def test_valid_reason_allows(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("hotfix\ndetails")
        result = evaluate_bypass(make_ctx(tmp_path), DENY)
        assert result.verdict == "allow"
        assert result.rule_id == "phase_gate"

    def test_run_log_appended(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("hotfix for prod")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert "phase_gate" in log
        assert "Edit" in log
        assert "src/auth.ts" in log
        assert "hotfix for prod" in log

    def test_run_log_line_format(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("x")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text().strip()
        # <ISO-UTC> | <rule_id> | <tool_name> | <relative_target> | <reason_first_line>
        pattern = (
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \| phase_gate \| Edit \| src/auth\.ts \| x$"
        )
        assert re.match(pattern, log), f"actual: {log!r}"

    def test_run_log_only_first_line_of_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text(
            "hotfix first line\nsecond line\nthird"
        )
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert "hotfix first line" in log
        assert "second line" not in log

    def test_run_log_appends_not_overwrites(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "RUN_LOG.md").write_text("existing line\n")
        (tmp_path / ".ai" / "bypass-reason.md").write_text("new reason")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert log.startswith("existing line\n")
        assert "new reason" in log

    def test_run_log_creates_ai_dir_if_missing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("r")
        log_path = tmp_path / ".ai" / "RUN_LOG.md"
        assert not log_path.exists()
        evaluate_bypass(make_ctx(tmp_path), DENY)
        assert log_path.exists()

    def test_run_log_pipe_char_sanitized(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("a | b | c")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        # The reason column itself should not contain raw |
        # Count of | separators should still be exactly 4 (five columns)
        last_line = log.strip().splitlines()[-1]
        assert last_line.count("|") == 4
        assert "a / b / c" in last_line

    def test_run_log_control_chars_sanitized(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "bypass-reason.md").write_text("hot\x01fix\x02done")
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        assert "\x01" not in log
        assert "\x02" not in log
        assert "hot fix done" in log

    def test_run_log_long_reason_truncated(self, tmp_path, monkeypatch):
        monkeypatch.setenv("BUTLER_BYPASS", "1")
        (tmp_path / ".ai").mkdir()
        long_reason = "x" * 500
        (tmp_path / ".ai" / "bypass-reason.md").write_text(long_reason)
        evaluate_bypass(make_ctx(tmp_path), DENY)
        log = (tmp_path / ".ai" / "RUN_LOG.md").read_text()
        last_line = log.strip().splitlines()[-1]
        # reason col: 200 chars of x plus ellipsis
        reason_col = last_line.split(" | ")[-1]
        assert len(reason_col) == 201  # 200 + ellipsis
        assert reason_col.endswith("…")
