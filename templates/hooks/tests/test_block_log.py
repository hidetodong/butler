"""Unit tests for intercept log formatting, rotation, and fail-closed writes."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

import pytest

from lib.block_log import MAX_BYTES, append_block_log, format_line, trim_to_budget
from lib.io import Context, Decision


def make_ctx(cwd: Path, target: str = "src/auth.ts") -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


DENY = Decision(verdict="deny", rule_id="phase_gate", reason="缺 .ai/CONCEPT.md\n第二行")


def test_format_line_uses_reason_first_line_and_sanitizes():
    ctx = make_ctx(Path("/tmp"))
    line = format_line(ctx, Decision(verdict="deny", rule_id="phase_gate", reason="a | b\nx"))
    assert line.endswith("\n")
    assert line.count("|") == 4
    assert "a / b" in line
    assert "x" not in line.split(" | ")[-1]


def test_trim_drops_oldest_complete_lines():
    old = b"old-1\nold-2\n"
    incoming = b"new\n"
    result = trim_to_budget(old, incoming, max_bytes=len(b"old-2\nnew\n"))
    assert result == b"old-2\nnew\n"


def test_append_writes_one_line(tmp_path: Path):
    ctx = make_ctx(tmp_path)
    append_block_log(ctx, DENY)
    log = tmp_path / ".ai" / ".hook-blocks.log"
    text = log.read_text(encoding="utf-8")
    assert text.count("\n") == 1
    assert "phase_gate" in text
    assert "src/auth.ts" in text
    assert "缺 .ai/CONCEPT.md" in text
    assert "第二行" not in text


def test_append_rotates_when_over_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("lib.block_log.MAX_BYTES", 40)
    ctx = make_ctx(tmp_path)
    path = tmp_path / ".ai" / ".hook-blocks.log"
    path.parent.mkdir()
    path.write_bytes(b"aaaaaaaaaaaaaaaaaaaa\nbbbbbbbbbbbbbbbbbbbb\n")
    append_block_log(ctx, DENY, log_path=path)
    data = path.read_bytes()
    assert len(data) <= 40 or data.endswith(format_line(ctx, DENY).encode())
    assert b"aaaaaaaaaaaaaaaaaaaa" not in data


def test_append_write_failure_propagates(tmp_path: Path):
    ctx = make_ctx(tmp_path)
    blocker = tmp_path / ".ai"
    blocker.write_text("not-a-directory", encoding="utf-8")
    with pytest.raises(OSError):
        append_block_log(ctx, DENY)
