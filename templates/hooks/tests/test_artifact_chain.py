"""Unit tests for rules.artifact_chain (stub placeholder rule)."""
from __future__ import annotations

from pathlib import PurePosixPath

from lib.io import Context
from rules import artifact_chain


def make_ctx(target: str = "src/x.ts") -> Context:
    return Context(
        cwd="/tmp/proj",
        tool_name="Edit",
        target_path=PurePosixPath(target),
        tool_input={"file_path": target},
    )


class TestArtifactChainStub:
    def test_always_allows_source_path(self):
        d = artifact_chain.evaluate(make_ctx("src/auth.ts"))
        assert d.verdict == "allow"
        assert d.rule_id == "artifact_chain"

    def test_always_allows_protected_path(self):
        # Even paths that other rules deny must be allowed by the stub.
        d = artifact_chain.evaluate(make_ctx("99_Business_Extension/x.md"))
        assert d.verdict == "allow"

    def test_rule_id_stable(self):
        assert artifact_chain.RULE_ID == "artifact_chain"
