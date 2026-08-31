"""inbox 工作流的双宿主接线测试。

两个用例描述的都是当前活着的接线：注册表条目与两份宿主薄壳，一律指向 R7 起生效的
新契约与新工具。R8 之前这里还有第三个用例，断言的是上一代规则文件自身的内容，
已随那份文件一起退役。
"""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[3]


def test_inbox_is_registered_for_both_hosts() -> None:
    data = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
    matches = [item for item in data["workflows"] if item["id"] == "inbox"]
    assert len(matches) == 1
    item = matches[0]
    assert item["rule_source"] == "Coder/40_Context_Management/intake-workflow.md"
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
        assert "intake-schema.md" in text
        assert "intake-workflow.md" in text
        assert "tools/intake/" in text
