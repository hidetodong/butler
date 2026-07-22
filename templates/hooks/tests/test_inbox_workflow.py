from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[3]


def test_inbox_workflow_route_and_safety_contract() -> None:
    text = (ROOT / "Coder/40_Context_Management/inbox-workflow.md").read_text(encoding="utf-8")
    required = (
        "new-requirement", "existing-requirement-version", "supplemental-material",
        "fuzzy-idea", "milestone-direction", "record-only", "duplicate-candidate", "ambiguous",
        "awaiting-confirmation", "dangerous", ".ai/RUN_LOG.md", "processed_sha256",
        "活工作区保护", "一个冲突或失败项不能阻塞无依赖 sibling",
    )
    for token in required:
        assert token in text


def test_inbox_is_registered_for_both_hosts() -> None:
    data = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
    matches = [item for item in data["workflows"] if item["id"] == "inbox"]
    assert len(matches) == 1
    item = matches[0]
    assert item["rule_source"] == "Coder/40_Context_Management/inbox-workflow.md"
    assert item["claude"]["name"] == "/butler:inbox"
    assert item["codex"]["name"] == "$butler-inbox"
    assert item["allow_implicit_invocation"] is True


def test_host_entries_are_thin_and_resolve_project_root() -> None:
    paths = (
        ROOT / ".claude/commands/butler/inbox.md",
        ROOT / "plugins/butler/skills/butler-inbox/SKILL.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "BUTLER_PATH" in text
        assert "mcv-deployment.md §0.1" in text
        assert "inbox-workflow.md" in text
        assert "origin/" in text
