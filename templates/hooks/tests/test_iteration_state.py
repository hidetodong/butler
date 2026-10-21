"""Unit tests for active-iteration detection and root meta names."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.iteration_state import has_active_iteration, is_root_meta, meta_escape_applies


def test_root_meta_only_single_segment_names():
    assert is_root_meta(PurePosixPath("README.md"))
    assert is_root_meta(PurePosixPath("LICENSE"))
    assert not is_root_meta(PurePosixPath("docs/README.md"))
    assert not is_root_meta(PurePosixPath("src/auth.ts"))


def test_missing_ledger_is_not_active(tmp_path: Path):
    assert has_active_iteration(str(tmp_path)) is False


def test_current_none_is_not_active(tmp_path: Path):
    ledger = tmp_path / ".ai" / "ITERATIONS.md"
    ledger.parent.mkdir()
    ledger.write_text("current: none\n", encoding="utf-8")
    assert has_active_iteration(str(tmp_path)) is False
    assert meta_escape_applies(str(tmp_path), PurePosixPath("README.md"))


def test_current_active_blocks_escape(tmp_path: Path):
    ledger = tmp_path / ".ai" / "ITERATIONS.md"
    ledger.parent.mkdir()
    ledger.write_text("current: ITER-0121\n", encoding="utf-8")
    assert has_active_iteration(str(tmp_path)) is True
    assert meta_escape_applies(str(tmp_path), PurePosixPath("README.md")) is False


def test_unparseable_ledger_fails_closed(tmp_path: Path):
    ledger = tmp_path / ".ai" / "ITERATIONS.md"
    ledger.parent.mkdir()
    ledger.write_text("no current marker\n", encoding="utf-8")
    assert has_active_iteration(str(tmp_path)) is True
