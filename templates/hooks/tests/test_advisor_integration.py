"""Integration tests: run butler_advisor.py as subprocess with real stdin.

核心断言：advisor 永远 exit 0（PostToolUse advisory 绝不阻塞），
有提醒时 stdout 是合法的 additionalContext JSON，无提醒 / 坏输入时静默放行。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ADVISOR = Path(__file__).resolve().parent.parent / "butler_advisor.py"


def run_advisor(payload, cwd: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    return subprocess.run(
        [sys.executable, str(ADVISOR)],
        input=payload if isinstance(payload, str) else json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd),
    )


def write_payload(cwd: Path, target: str) -> dict:
    return {
        "tool_name": "Write",
        "tool_input": {"file_path": target, "content": "x"},
        "cwd": str(cwd),
        "tool_response": {"success": True},
    }


class TestAdvisorEmits:
    def test_milestone_without_prd_emits_additional_context(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        r = run_advisor(write_payload(tmp_path, ".ai/MILESTONE.md"), tmp_path)
        assert r.returncode == 0
        out = json.loads(r.stdout)
        hso = out["hookSpecificOutput"]
        assert hso["hookEventName"] == "PostToolUse"
        assert "references/prd" in hso["additionalContext"]

    def test_milestone_with_prd_dir_is_silent(self, tmp_path):
        (tmp_path / ".ai" / "references" / "prd").mkdir(parents=True)
        r = run_advisor(write_payload(tmp_path, ".ai/MILESTONE.md"), tmp_path)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "PRD 先行自检" not in context
        assert "handoff 新鲜度" in context

    def test_apply_patch_milestone_emits_json_once(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        payload = {
            "tool_name": "apply_patch",
            "tool_input": {"command": """*** Begin Patch
*** Update File: .ai/MILESTONE.md
+brief
*** Update File: .ai/MILESTONE.md
+more
*** End Patch"""},
            "cwd": str(tmp_path),
        }
        r = run_advisor(payload, tmp_path)
        assert r.returncode == 0
        out = json.loads(r.stdout)
        assert "references/prd" in out["hookSpecificOutput"]["additionalContext"]


class TestAdvisorNeverBlocks:
    def test_non_milestone_target_exit0_silent(self, tmp_path):
        r = run_advisor(write_payload(tmp_path, "src/auth.ts"), tmp_path)
        assert r.returncode == 0
        assert r.stdout.strip() == ""

    def test_non_gated_tool_exit0(self, tmp_path):
        payload = {"tool_name": "Read", "tool_input": {}, "cwd": str(tmp_path)}
        r = run_advisor(payload, tmp_path)
        assert r.returncode == 0

    def test_malformed_stdin_fails_open_exit0(self, tmp_path):
        # 与 butler_gate 的 fail-closed 相反：advisory 坏输入静默放行。
        r = run_advisor("this is not json", tmp_path)
        assert r.returncode == 0
        assert r.stdout.strip() == ""

    def test_missing_tool_name_exit0(self, tmp_path):
        r = run_advisor({"tool_input": {}}, tmp_path)
        assert r.returncode == 0

    def test_malformed_apply_patch_fails_open(self, tmp_path):
        payload = {
            "tool_name": "apply_patch",
            "tool_input": {"command": "not a patch"},
            "cwd": str(tmp_path),
        }
        r = run_advisor(payload, tmp_path)
        assert r.returncode == 0
        assert r.stdout.strip() == ""
