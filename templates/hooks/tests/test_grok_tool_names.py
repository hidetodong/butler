"""Grok write names go through the same deny rule as Write and Edit."""
from __future__ import annotations

import subprocess
from pathlib import Path

from tests.test_integration import edit_payload, run_gate

MANAGED = "<!-- butler-managed:start -->\n"


def rule_id(stderr: str) -> str:
    for line in stderr.splitlines():
        if "denied:" in line:
            return line.split("denied:", 1)[1].strip()
    raise AssertionError(stderr)


def draft_project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    ai = root / ".ai"
    ai.mkdir(parents=True)
    (root / "CLAUDE.md").write_text(MANAGED + "rules\n", encoding="utf-8")
    (ai / "CONCEPT.md").write_text("c\n", encoding="utf-8")
    (ai / "TECH_PLAN.md").write_text("方案状态: draft\n", encoding="utf-8")
    (ai / "AC_LIST.md").write_text("---\n状态: draft\n---\n# Goal\nx\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def test_write_matches_write_rule(tmp_path: Path):
    root = draft_project(tmp_path)
    original = edit_payload(root, "src/auth.ts")
    original["tool_name"] = "Write"
    grok = edit_payload(root, "src/auth.ts")
    grok["tool_name"] = "write"
    first = run_gate(original, root)
    second = run_gate(grok, root)
    assert first.returncode == 2
    assert second.returncode == 2
    assert rule_id(first.stderr) == rule_id(second.stderr)


def test_search_replace_matches_edit_rule(tmp_path: Path):
    root = draft_project(tmp_path)
    original = edit_payload(root, "src/auth.ts")
    grok = edit_payload(root, "src/auth.ts")
    grok["tool_name"] = "search_replace"
    first = run_gate(original, root)
    second = run_gate(grok, root)
    assert first.returncode == 2
    assert second.returncode == 2
    assert rule_id(first.stderr) == rule_id(second.stderr)


def test_camel_case_write_is_gated(tmp_path: Path):
    root = draft_project(tmp_path)
    original = edit_payload(root, "src/auth.ts")
    grok = {
        "toolName": "search_replace",
        "toolInput": {"file_path": "src/auth.ts"},
        "cwd": str(root),
    }
    first = run_gate(original, root)
    second = run_gate(grok, root)
    assert first.returncode == 2
    assert second.returncode == 2
    assert rule_id(first.stderr) == rule_id(second.stderr)


def test_terminal_command_stays_allowed(tmp_path: Path):
    root = draft_project(tmp_path)
    result = run_gate(
        {
            "tool_name": "run_terminal_command",
            "tool_input": {"command": "printf x > src/auth.ts", "file_path": "src/auth.ts"},
            "cwd": str(root),
        },
        root,
    )
    assert result.returncode == 0
    assert "denied:" not in result.stderr
