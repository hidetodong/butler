"""Unit tests for lib.io."""
from __future__ import annotations

import io as stdio
import json
import sys
from pathlib import PurePosixPath

import pytest

from lib.io import (
    Context,
    Decision,
    GATED_BLACKLIST,
    OUT_OF_CWD,
    is_gated,
    parse_stdin,
    resolve_target,
)


class TestResolveTarget:
    def test_relative_path_preserved(self):
        result = resolve_target({"file_path": "src/auth.ts"}, cwd="/tmp/proj")
        assert result == PurePosixPath("src/auth.ts")

    def test_missing_file_path_returns_out_of_cwd(self):
        result = resolve_target({}, cwd="/tmp/proj")
        assert result == OUT_OF_CWD

    def test_empty_file_path_returns_out_of_cwd(self):
        result = resolve_target({"file_path": ""}, cwd="/tmp/proj")
        assert result == OUT_OF_CWD

    def test_parent_reference_resolves_within_cwd(self, tmp_path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "a.ts").write_text("x")
        result = resolve_target(
            {"file_path": "src/../src/a.ts"}, cwd=str(tmp_path)
        )
        assert result == PurePosixPath("src/a.ts")

    def test_parent_reference_escapes_cwd_returns_sentinel(self, tmp_path):
        result = resolve_target(
            {"file_path": "../escape.ts"}, cwd=str(tmp_path)
        )
        assert result == OUT_OF_CWD

    def test_absolute_path_inside_cwd_resolved_to_relative(self, tmp_path):
        target = tmp_path / "src" / "a.ts"
        target.parent.mkdir(parents=True)
        target.write_text("x")
        result = resolve_target({"file_path": str(target)}, cwd=str(tmp_path))
        assert result == PurePosixPath("src/a.ts")

    def test_absolute_path_outside_cwd_returns_sentinel(self, tmp_path):
        other = tmp_path.parent / "other_dir"
        result = resolve_target({"file_path": str(other / "x.ts")}, cwd=str(tmp_path))
        assert result == OUT_OF_CWD

    def test_symlink_cwd_and_target_normalized_consistently(self, tmp_path):
        """cwd and file_path may arrive with different symlink forms (e.g. macOS /tmp)."""
        real_dir = tmp_path / "real"
        real_dir.mkdir()
        (real_dir / "src").mkdir()
        (real_dir / "src" / "a.ts").write_text("x")

        link_dir = tmp_path / "via_link"
        link_dir.symlink_to(real_dir, target_is_directory=True)

        # cwd points through the symlink; file_path is absolute via the real path
        result = resolve_target(
            {"file_path": str(real_dir / "src" / "a.ts")},
            cwd=str(link_dir),
        )
        assert result == PurePosixPath("src/a.ts")


class TestIsGated:
    def test_source_path_is_gated(self):
        assert is_gated(PurePosixPath("src/auth.ts")) is True

    def test_ai_directory_exempt(self):
        assert is_gated(PurePosixPath(".ai/CONCEPT.md")) is False

    def test_deliveries_exempt(self):
        assert is_gated(PurePosixPath("deliveries/x.md")) is False

    def test_claude_dir_exempt(self):
        assert is_gated(PurePosixPath(".claude/settings.json")) is False

    def test_node_modules_exempt(self):
        assert is_gated(PurePosixPath("node_modules/foo/index.js")) is False

    def test_out_of_cwd_is_gated_conservative(self):
        assert is_gated(OUT_OF_CWD) is True

    def test_root_of_blacklisted_dir_exempt(self):
        assert is_gated(PurePosixPath(".ai")) is False

    def test_prefix_collision_not_false_positive(self):
        # ".github" must NOT match ".git" prefix
        assert is_gated(PurePosixPath(".github/workflows/ci.yml")) is True


class TestParseStdin:
    def test_parse_valid_json(self, monkeypatch):
        payload = {"tool_name": "Edit", "tool_input": {"file_path": "x"}, "cwd": "/tmp"}
        monkeypatch.setattr(sys, "stdin", stdio.StringIO(json.dumps(payload)))
        assert parse_stdin() == payload

    def test_parse_invalid_json_raises(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", stdio.StringIO("not json"))
        with pytest.raises(json.JSONDecodeError):
            parse_stdin()


class TestDecision:
    def test_decision_defaults(self):
        d = Decision(verdict="allow", rule_id="x")
        assert d.verdict == "allow"
        assert d.rule_id == "x"
        assert d.reason == ""
        assert d.remediation == ""


class TestBlacklistContents:
    def test_expected_entries(self):
        assert ".ai/" in GATED_BLACKLIST
        assert "deliveries/" in GATED_BLACKLIST
        assert ".claude/" in GATED_BLACKLIST
        assert ".git/" in GATED_BLACKLIST
        assert "node_modules/" in GATED_BLACKLIST
        assert ".vscode/" in GATED_BLACKLIST
        assert ".idea/" in GATED_BLACKLIST
