"""pytest fixtures shared across hook tests."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def tmp_project(tmp_path: Path):
    """Copy a named fixture tree into tmp_path. Returns the project root."""

    def _make(fixture_name: str) -> Path:
        src = FIXTURES_DIR / fixture_name
        if not src.exists():
            raise FileNotFoundError(f"fixture not found: {fixture_name}")
        for item in src.rglob("*"):
            rel = item.relative_to(src)
            dst = tmp_path / rel
            if item.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst)
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        return tmp_path

    return _make
