from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


READERS = (
    "Coder/00_System_Prompt/logic-protocol.md",
    "Coder/65_Extension_Dangerous/dangerous-engine.md",
    "Coder/62_Extension_Agents/independent-review.md",
    "Coder/70_Extension_Preference/preference-probe-engine.md",
    ".claude/commands/butler/dangerous.md",
    ".claude/commands/butler/preference.md",
    ".claude/commands/butler/progress.md",
    "plugins/butler/skills/butler-dangerous/SKILL.md",
    "plugins/butler/skills/butler-preference/SKILL.md",
    "plugins/butler/skills/butler-progress/SKILL.md",
    "plugins/butler/skills/butler-review/SKILL.md",
    "templates/rule-card.md",
)

WRITERS = {
    "Coder/65_Extension_Dangerous/dangerous-engine.md": "set dangerous true|false",
    "Coder/62_Extension_Agents/independent-review.md": "set independent_review true|false",
    "Coder/70_Extension_Preference/preference-probe-engine.md": "set preference true|false",
    ".claude/commands/butler/dangerous.md": "set dangerous true",
    ".claude/commands/butler/preference.md": "set preference true|false",
    "plugins/butler/skills/butler-dangerous/SKILL.md": "set dangerous true|false",
    "plugins/butler/skills/butler-preference/SKILL.md": "set preference true|false",
    "plugins/butler/skills/butler-review/SKILL.md": "set independent_review true|false",
}


class ConsumerContractTests(unittest.TestCase):
    def text(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_every_live_consumer_delegates_reads_to_resolve(self):
        for relative in READERS:
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn("project-config", text)
                self.assertIn("resolve", text)

    def test_writers_delegate_to_json_only_set_contract(self):
        for relative, invocation in WRITERS.items():
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn(invocation, text)
                self.assertNotIn("回写 `.ai/local-constraints.md`", text)
                self.assertNotIn("回写为 `on`", text)
                self.assertNotIn("回写为 `off`", text)

    def test_commands_surface_source_conflicts_and_legacy_write_boundary(self):
        for relative in (
            ".claude/commands/butler/dangerous.md",
            ".claude/commands/butler/preference.md",
            ".claude/commands/butler/progress.md",
        ):
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn("source", text)
                self.assertIn("legacy_conflicts", text)
        for relative in (
            ".claude/commands/butler/dangerous.md",
            ".claude/commands/butler/preference.md",
        ):
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn("source=legacy", text)
                self.assertIn("source=missing", text)
                self.assertIn("不得直接改 Markdown", text)

    def test_progress_version_does_not_come_from_project_config(self):
        for relative in (
            ".claude/commands/butler/progress.md",
            "plugins/butler/skills/butler-progress/SKILL.md",
        ):
            with self.subTest(relative=relative):
                text = self.text(relative)
                self.assertIn("AGENTS.md", text)
                self.assertIn("VERSION", text)
                self.assertNotIn("version from `.ai/local-constraints.md`", text)

    def test_current_repository_is_migrated_without_changing_switch_values(self):
        config = self.text(".ai/butler.config.json")
        self.assertIn('"dangerous": true', config)
        self.assertIn('"independent_review": false', config)
        self.assertIn('"preference": true', config)
        legacy = self.text(".ai/local-constraints.md")
        self.assertNotIn("# Active Profiles", legacy)
        self.assertNotIn("# Butler 功能开关", legacy)
        self.assertNotIn("# Review Policy", legacy)
        self.assertIn("# Local Constraints", legacy)


if __name__ == "__main__":
    unittest.main()
