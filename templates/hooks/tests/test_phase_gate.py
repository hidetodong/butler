"""Unit tests for rules.phase_gate."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.io import Context, OUT_OF_CWD
from rules import phase_gate


def make_ctx(cwd: Path, target: str) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


def make_ctx_oocwd(cwd: Path) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=OUT_OF_CWD,
        tool_input={},
    )


class TestPhaseGate:
    def test_blacklist_path_allows(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, ".ai/CONCEPT.md"))
        assert d.verdict == "allow"
        assert d.rule_id == "phase_gate"

    def test_all_artifacts_present_allows(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "allow"

    def test_concept_missing_denies(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert d.rule_id == "phase_gate"
        assert "CONCEPT.md" in d.reason

    def test_ac_list_missing_denies(self, tmp_project):
        proj = tmp_project("p1-done")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert "AC_LIST.md" in d.reason

    def test_tech_plan_missing_denies(self, tmp_project):
        proj = tmp_project("p1p2-done")
        d = phase_gate.evaluate(make_ctx(proj, "src/auth.ts"))
        assert d.verdict == "deny"
        assert "TECH_PLAN.md" in d.reason

    def test_empty_file_denies(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "CONCEPT.md").write_text("")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"
        assert "CONCEPT.md" in d.reason

    def test_whitespace_only_file_denies(self, tmp_path):
        (tmp_path / ".ai").mkdir()
        (tmp_path / ".ai" / "CONCEPT.md").write_text("   \n\n")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"

    def test_out_of_cwd_denies(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_ctx_oocwd(proj))
        assert d.verdict == "deny"

    def test_reason_includes_remediation(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, "src/x.ts"))
        assert d.remediation
        assert "P1" in d.remediation
