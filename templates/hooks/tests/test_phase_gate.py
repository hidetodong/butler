"""Unit tests for rules.phase_gate."""
from __future__ import annotations

from pathlib import Path, PurePosixPath

from lib.io import Context, OUTSIDE_PROJECT, UNKNOWN_TARGET
from rules import phase_gate


def make_ctx(cwd: Path, target: str) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


def make_special_ctx(cwd: Path, target: PurePosixPath) -> Context:
    return Context(
        cwd=str(cwd),
        tool_name="Edit",
        target_path=target,
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

    def test_outside_project_allows_host_permission_to_decide(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_special_ctx(proj, OUTSIDE_PROJECT))
        assert d.verdict == "allow"

    def test_unknown_target_denies(self, tmp_project):
        proj = tmp_project("full-artifacts")
        d = phase_gate.evaluate(make_special_ctx(proj, UNKNOWN_TARGET))
        assert d.verdict == "deny"
        assert "无法解析" in d.reason

    def test_reason_includes_remediation(self, tmp_project):
        proj = tmp_project("empty-project")
        d = phase_gate.evaluate(make_ctx(proj, "src/x.ts"))
        assert d.remediation
        assert "P1" in d.remediation


class TestAcFreezeGate:
    """D1: AC_LIST 冻结门——状态须为 ack-frozen 才放行源码写。"""

    def _seed_full_ai(self, root: Path, ac_body: str) -> None:
        ai = root / ".ai"
        ai.mkdir(parents=True, exist_ok=True)
        (ai / "CONCEPT.md").write_text("c", encoding="utf-8")
        (ai / "TECH_PLAN.md").write_text("t", encoding="utf-8")
        (ai / "AC_LIST.md").write_text(ac_body, encoding="utf-8")

    def test_draft_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "---\n状态: draft\nACK 日期: —\n---\n# Goal\nx")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"
        assert "ack-frozen" in d.reason

    def test_frozen_allows(self, tmp_path):
        self._seed_full_ai(
            tmp_path, "---\n状态: ack-frozen\nACK 日期: 2026-06-15\n---\n# Goal\nx"
        )
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "allow"

    def test_legacy_no_status_field_allows(self, tmp_path):
        self._seed_full_ai(tmp_path, "# Goal\n旧版 AC_LIST，无状态字段")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "allow"

    def test_unknown_status_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "---\n状态: 进行中\n---\n# Goal\nx")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "deny"

    def test_english_status_key_allows(self, tmp_path):
        self._seed_full_ai(tmp_path, "---\nstatus: ack-frozen\n---\n# Goal\nx")
        d = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert d.verdict == "allow"


class TestPlanAdmissionGate:
    """P3: 显式 TECH_PLAN 状态只有 pass 可进入源码执行。"""

    def _seed_full_ai(self, root: Path, plan_body: str) -> None:
        ai = root / ".ai"
        ai.mkdir(parents=True, exist_ok=True)
        (ai / "CONCEPT.md").write_text("c", encoding="utf-8")
        (ai / "AC_LIST.md").write_text("---\n状态: ack-frozen\n---\n", encoding="utf-8")
        (ai / "TECH_PLAN.md").write_text(plan_body, encoding="utf-8")

    def test_pass_allows(self, tmp_path):
        self._seed_full_ai(tmp_path, "---\n方案状态: pass\n---\n# Goal\nx")
        assert phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts")).verdict == "allow"

    def test_draft_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "---\n方案状态: draft\n---\n# Goal\nx")
        decision = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert decision.verdict == "deny"
        assert "只有 pass" in decision.reason

    def test_revise_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "方案状态: revise\n# Goal\nx")
        assert phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts")).verdict == "deny"

    def test_blocked_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "方案状态: blocked\n# Goal\nx")
        decision = phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts"))
        assert decision.verdict == "deny"
        assert "解除阻塞" in decision.remediation

    def test_unknown_status_denies(self, tmp_path):
        self._seed_full_ai(tmp_path, "方案状态: approved\n# Goal\nx")
        assert phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts")).verdict == "deny"

    def test_english_key_and_case_allows(self, tmp_path):
        self._seed_full_ai(tmp_path, "plan_status: PASS\n# Goal\nx")
        assert phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts")).verdict == "allow"

    def test_legacy_no_status_field_allows(self, tmp_path):
        self._seed_full_ai(tmp_path, "# Goal\n旧版方案，无准入字段")
        assert phase_gate.evaluate(make_ctx(tmp_path, "src/x.ts")).verdict == "allow"
