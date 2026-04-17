"""Unit tests for rules.protected_paths."""
from __future__ import annotations

from pathlib import PurePosixPath

from lib.io import Context
from rules import protected_paths


def make_ctx(target: str) -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


class TestProtectedPaths:
    def test_business_extension_denies(self):
        d = protected_paths.evaluate(make_ctx("99_Business_Extension/policy.md"))
        assert d.verdict == "deny"
        assert d.rule_id == "protected_paths"
        assert "99_Business_Extension" in d.reason
        assert d.remediation

    def test_business_extension_nested_denies(self):
        d = protected_paths.evaluate(
            make_ctx("99_Business_Extension/nested/deep/file.md")
        )
        assert d.verdict == "deny"

    def test_normal_source_allows(self):
        d = protected_paths.evaluate(make_ctx("src/auth.ts"))
        assert d.verdict == "allow"
        assert d.rule_id == "protected_paths"

    def test_ai_directory_allows(self):
        d = protected_paths.evaluate(make_ctx(".ai/CONCEPT.md"))
        assert d.verdict == "allow"

    def test_similar_name_not_false_positive(self):
        # "99_business_extension_notes.md" should NOT match the protected prefix
        d = protected_paths.evaluate(make_ctx("99_business_extension_notes.md"))
        assert d.verdict == "allow"

    def test_path_at_root_matching_prefix(self):
        # The bare name "99_Business_Extension" (no trailing /) is not under the protected
        # directory; treat as allow (rule matches `prefix + "/"` only).
        d = protected_paths.evaluate(make_ctx("99_Business_Extension"))
        assert d.verdict == "allow"
