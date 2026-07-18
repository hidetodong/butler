"""Integration tests: run butler_gate.py as subprocess with real stdin/env."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

GATE = Path(__file__).resolve().parent.parent / "butler_gate.py"


def run_gate(payload: dict, cwd: Path, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.pop("BUTLER_BYPASS", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd),
    )


def edit_payload(cwd: Path, target: str) -> dict:
    return {
        "tool_name": "Edit",
        "tool_input": {"file_path": target, "old_string": "a", "new_string": "b"},
        "cwd": str(cwd),
    }


def patch_payload(cwd: Path, command: str) -> dict:
    return {
        "tool_name": "apply_patch",
        "tool_input": {"command": command},
        "cwd": str(cwd),
    }


class TestAllowPaths:
    def test_allow_when_all_artifacts_present(self, tmp_project):
        proj = tmp_project("full-artifacts")
        r = run_gate(edit_payload(proj, "src/auth.ts"), proj)
        assert r.returncode == 0, r.stderr

    def test_non_gated_tool_passes_through(self, tmp_project):
        proj = tmp_project("empty-project")
        payload = {
            "tool_name": "Read",
            "tool_input": {"file_path": "src/foo.ts"},
            "cwd": str(proj),
        }
        r = run_gate(payload, proj)
        assert r.returncode == 0

    def test_edit_inside_blacklist_allowed_even_without_artifacts(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, ".ai/CONCEPT.md"), proj)
        assert r.returncode == 0

    def test_absolute_path_outside_project_is_left_to_host_permissions(self, tmp_project, tmp_path):
        proj = tmp_project("empty-project")
        external = tmp_path.parent / "user-config" / "config.toml"
        r = run_gate(edit_payload(proj, str(external)), proj)
        assert r.returncode == 0, r.stderr

    def test_edit_from_project_subdir_still_uses_project_root_gate(self, tmp_project):
        proj = tmp_project("full-artifacts")
        subdir = proj / "packages" / "app"
        subdir.mkdir(parents=True)
        target = proj / "shared" / "config.py"
        r = run_gate(edit_payload(subdir, str(target)), subdir)
        assert r.returncode == 0, r.stderr

    def test_patch_across_two_valid_projects_allows_when_each_gate_passes(self, tmp_path):
        session = tmp_path / "aggregate"
        session.mkdir()
        roots = []
        for name in ("one", "two"):
            root = tmp_path / name
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            ai = root / ".ai"
            ai.mkdir()
            (ai / "CONCEPT.md").write_text("c")
            (ai / "AC_LIST.md").write_text("状态: ack-frozen\n")
            (ai / "TECH_PLAN.md").write_text("方案状态: pass\n")
            roots.append(root)
        command = (
            "*** Begin Patch\n"
            f"*** Add File: {roots[0] / 'a.py'}\n+a\n"
            f"*** Add File: {roots[1] / 'b.py'}\n+b\n"
            "*** End Patch"
        )
        r = run_gate(patch_payload(session, command), session)
        assert r.returncode == 0, r.stderr


class TestDenyPaths:
    def test_missing_file_path_fails_closed(self, tmp_project):
        proj = tmp_project("full-artifacts")
        payload = {"tool_name": "Edit", "tool_input": {}, "cwd": str(proj)}
        r = run_gate(payload, proj)
        assert r.returncode == 2
        assert "无法解析" in r.stderr

    def test_phase_gate_denies_when_concept_missing(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, "src/auth.ts"), proj)
        assert r.returncode == 2
        assert "phase_gate" in r.stderr
        assert "CONCEPT.md" in r.stderr

    def test_absolute_target_in_another_project_uses_that_projects_gate(self, tmp_path):
        session = tmp_path / "session"
        target_project = tmp_path / "target"
        session.mkdir()
        target_project.mkdir()
        subprocess.run(["git", "init", "-q", str(target_project)], check=True)
        r = run_gate(
            edit_payload(session, str(target_project / "src" / "x.py")),
            session,
        )
        assert r.returncode == 2
        assert "CONCEPT.md" in r.stderr

    def test_edit_from_subdir_cannot_bypass_project_phase_gate(self, tmp_project):
        proj = tmp_project("empty-project")
        subdir = proj / "packages" / "app"
        subdir.mkdir(parents=True)
        target = proj / "shared" / "config.py"
        r = run_gate(edit_payload(subdir, str(target)), subdir)
        assert r.returncode == 2
        assert "CONCEPT.md" in r.stderr

    def test_phase_gate_denies_when_ac_not_frozen(self, tmp_path):
        ai = tmp_path / ".ai"
        ai.mkdir()
        (ai / "CONCEPT.md").write_text("c")
        (ai / "TECH_PLAN.md").write_text("t")
        (ai / "AC_LIST.md").write_text("---\n状态: draft\n---\n# Goal\nx")
        r = run_gate(edit_payload(tmp_path, "src/auth.ts"), tmp_path)
        assert r.returncode == 2
        assert "phase_gate" in r.stderr
        assert "ack-frozen" in r.stderr

    def test_phase_gate_denies_when_plan_not_passed(self, tmp_path):
        ai = tmp_path / ".ai"
        ai.mkdir()
        (ai / "CONCEPT.md").write_text("c")
        (ai / "AC_LIST.md").write_text("---\n状态: ack-frozen\n---\n")
        (ai / "TECH_PLAN.md").write_text("---\n方案状态: revise\n---\n")
        r = run_gate(edit_payload(tmp_path, "src/auth.ts"), tmp_path)
        assert r.returncode == 2
        assert "phase_gate" in r.stderr
        assert "P3 方案未通过" in r.stderr

    def test_protected_paths_denies_business_extension(self, tmp_project):
        proj = tmp_project("full-artifacts")
        r = run_gate(edit_payload(proj, "99_Business_Extension/policy.md"), proj)
        assert r.returncode == 2
        assert "protected_paths" in r.stderr

    def test_stderr_format_contains_all_fields(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(edit_payload(proj, "src/x.ts"), proj)
        assert r.returncode == 2
        assert "denied:" in r.stderr
        assert "tool:" in r.stderr
        assert "target:" in r.stderr
        assert "reason:" in r.stderr
        assert "bypass:" in r.stderr

    def test_apply_patch_denies_when_any_target_is_protected(self, tmp_project):
        proj = tmp_project("full-artifacts")
        command = """*** Begin Patch
*** Add File: src/ok.py
+ok
*** Add File: 99_Business_Extension/policy.md
+blocked
*** End Patch"""
        r = run_gate(patch_payload(proj, command), proj)
        assert r.returncode == 2
        assert "protected_paths" in r.stderr
        assert "99_Business_Extension/policy.md" in r.stderr

    def test_patch_across_projects_denies_when_one_project_gate_fails(self, tmp_path):
        session = tmp_path / "aggregate"
        allowed = tmp_path / "allowed"
        denied = tmp_path / "denied"
        for root in (session, allowed, denied):
            root.mkdir()
        for root in (allowed, denied):
            subprocess.run(["git", "init", "-q", str(root)], check=True)
        ai = allowed / ".ai"
        ai.mkdir()
        (ai / "CONCEPT.md").write_text("c")
        (ai / "AC_LIST.md").write_text("状态: ack-frozen\n")
        (ai / "TECH_PLAN.md").write_text("方案状态: pass\n")
        command = (
            "*** Begin Patch\n"
            f"*** Add File: {allowed / 'a.py'}\n+a\n"
            f"*** Add File: {denied / 'b.py'}\n+b\n"
            "*** End Patch"
        )
        r = run_gate(patch_payload(session, command), session)
        assert r.returncode == 2
        assert "CONCEPT.md" in r.stderr


class TestBypassFlow:
    def test_bypass_without_reason_still_denies(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate(
            edit_payload(proj, "src/x.ts"), proj, env_extra={"BUTLER_BYPASS": "1"}
        )
        assert r.returncode == 2
        assert "bypass-reason.md" in r.stderr

    def test_bypass_with_reason_allows(self, tmp_project):
        proj = tmp_project("with-bypass-reason")
        # with-bypass-reason fixture has all three artifacts too; to actually
        # exercise bypass we write to a protected path instead.
        r = run_gate(
            edit_payload(proj, "99_Business_Extension/policy.md"),
            proj,
            env_extra={"BUTLER_BYPASS": "1"},
        )
        assert r.returncode == 0, r.stderr
        log = (proj / ".ai" / "RUN_LOG.md").read_text()
        assert "protected_paths" in log

    def test_bypass_with_empty_reason_denies(self, tmp_project):
        proj = tmp_project("with-bypass-reason")
        (proj / ".ai" / "bypass-reason.md").write_text("")
        r = run_gate(
            edit_payload(proj, "99_Business_Extension/policy.md"),
            proj,
            env_extra={"BUTLER_BYPASS": "1"},
        )
        assert r.returncode == 2


class TestFailClosed:
    def test_malformed_stdin_fails_closed(self, tmp_project):
        proj = tmp_project("full-artifacts")
        env = os.environ.copy()
        env.pop("BUTLER_BYPASS", None)
        r = subprocess.run(
            [sys.executable, str(GATE)],
            input="this is not json",
            capture_output=True,
            text=True,
            env=env,
            cwd=str(proj),
        )
        assert r.returncode == 2
        assert "internal error" in r.stderr

    def test_missing_tool_name_passes_through(self, tmp_project):
        proj = tmp_project("empty-project")
        r = run_gate({"tool_input": {}}, proj)
        # No tool_name → not in GATED_TOOLS → exit 0
        assert r.returncode == 0

    def test_malformed_apply_patch_fails_closed(self, tmp_project):
        proj = tmp_project("full-artifacts")
        r = run_gate(patch_payload(proj, "not a patch"), proj)
        assert r.returncode == 2
        assert "internal error" in r.stderr
