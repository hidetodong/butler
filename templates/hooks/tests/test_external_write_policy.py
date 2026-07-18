"""Contract tests for external-write ownership and dangerous-mode scope."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_dangerous_mode_freezes_host_authorized_ceiling() -> None:
    text = _read("Coder/65_Extension_Dangerous/dangerous-engine.md")
    required = [
        "授权上限",
        "启动时冻结",
        "宿主",
        "动态发现并追加实际施工项目",
        "不得在运行中自行扩大授权上限",
        "不依赖它的工作",
        "回到第 4 步连续推进",
    ]
    for phrase in required:
        assert phrase in text


def test_public_rule_surfaces_assign_external_permissions_to_host() -> None:
    for relative in (
        "Coder/README.md",
        "Coder/20_Workflow_Lifecycle/mcv-deployment.md",
        "templates/rule-card.md",
        "templates/hooks/README.md",
    ):
        text = _read(relative)
        assert "宿主" in text, relative
        assert "项目外" in text, relative


def test_normal_external_authorization_is_not_a_bypass() -> None:
    assert "正常项目外授权不走 bypass" in _read(
        "Coder/20_Workflow_Lifecycle/mcv-deployment.md"
    )
