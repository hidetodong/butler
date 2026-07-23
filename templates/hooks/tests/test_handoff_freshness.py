from pathlib import Path, PurePosixPath

from lib.io import Context
from rules import handoff_freshness


def ctx(tmp_path: Path, target: str) -> Context:
    return Context(str(tmp_path), "Write", PurePosixPath(target), {"file_path": target})


def test_authoritative_sources_advise(tmp_path):
    for target in sorted(handoff_freshness.EXACT):
        message = handoff_freshness.evaluate(ctx(tmp_path, target)).message
        assert "handoff" in message
        assert "sync" in message


def test_handoff_and_unrelated_files_are_silent(tmp_path):
    for target in (".ai/02_SESSION_HANDOFF.md", ".ai/handoff-state.json", "src/app.py"):
        assert handoff_freshness.evaluate(ctx(tmp_path, target)).message == ""
