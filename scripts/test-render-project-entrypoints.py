#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("render-project-entrypoints.py")
SPEC = importlib.util.spec_from_file_location("render_project_entrypoints", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.root = SCRIPT.parent.parent
        self.temp = tempfile.TemporaryDirectory()
        self.target = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_render(self):
        MODULE.apply(MODULE.plan(self.target, self.root))

    def test_first_render_resolves_both_files(self):
        self.run_render()
        version = (self.root / "VERSION").read_text().strip()
        for name in ("CLAUDE.md", "AGENTS.md"):
            text = (self.target / name).read_text()
            self.assertIn(MODULE.MANAGED_START, text)
            self.assertIn(f"butler v{version}", text)
            self.assertIn(str(self.root), text)
            self.assertNotIn("{{", text)
            self.assertEqual(0o644, (self.target / name).stat().st_mode & 0o777)

    def test_second_render_is_byte_idempotent(self):
        self.run_render()
        before = {name: (self.target / name).read_bytes() for name in ("CLAUDE.md", "AGENTS.md")}
        self.run_render()
        self.assertEqual(before, {name: (self.target / name).read_bytes() for name in before})

    def test_existing_unmanaged_content_is_preserved(self):
        (self.target / "CLAUDE.md").write_text("owner claude  \n\n")
        (self.target / "AGENTS.md").write_text("owner agents\n")
        self.run_render()
        self.assertTrue((self.target / "CLAUDE.md").read_text().startswith("owner claude  \n\n"))
        self.assertTrue((self.target / "AGENTS.md").read_text().startswith("owner agents\n"))

    def test_each_user_region_is_preserved_on_update(self):
        self.run_render()
        values = {"CLAUDE.md": "\nclaude owner bytes\n", "AGENTS.md": "\nagents owner bytes\n"}
        for name, value in values.items():
            path = self.target / name
            text = path.read_text()
            left, right = text.split(MODULE.USER_START, 1)
            _, tail = right.split(MODULE.USER_END, 1)
            old_version = (self.root / "VERSION").read_text().strip()
            path.write_text(
                (left + MODULE.USER_START + value + MODULE.USER_END + tail).replace(
                    f"butler v{old_version}", "butler v0.0.0"
                )
            )
        self.run_render()
        for name, value in values.items():
            text = (self.target / name).read_text()
            inner = text.split(MODULE.USER_START, 1)[1].split(MODULE.USER_END, 1)[0]
            self.assertEqual(value, inner)
            self.assertIn(f"butler v{(self.root / 'VERSION').read_text().strip()}", text)

    def test_legacy_butler_file_is_migrated_without_duplicate_user_markers(self):
        template = (self.root / "templates/CLAUDE.md.template").read_text()
        rendered = MODULE.render_template(
            template,
            self.root,
            "0.0.0",
            MODULE.rule_card_content((self.root / "templates/rule-card.md").read_text()),
        )
        legacy = "owner prefix\n\n" + rendered.replace(
            "<!-- user-managed -->\n", "<!-- user-managed -->\nlegacy owner\n", 1
        ) + "\nowner suffix\n"
        (self.target / "CLAUDE.md").write_text(legacy)
        self.run_render()
        text = (self.target / "CLAUDE.md").read_text()
        self.assertEqual(1, text.count(MODULE.MANAGED_START))
        self.assertEqual(1, text.count(MODULE.USER_START))
        self.assertIn("legacy owner", text)
        self.assertTrue(text.startswith("owner prefix\n"))
        self.assertTrue(text.endswith("owner suffix\n"))

    def test_duplicate_marker_rejects_both_writes(self):
        self.run_render()
        agents_before = (self.target / "AGENTS.md").read_bytes()
        claude = self.target / "CLAUDE.md"
        claude.write_text(claude.read_text() + MODULE.MANAGED_START)
        claude_before = claude.read_bytes()
        with self.assertRaises(MODULE.RenderError):
            MODULE.plan(self.target, self.root)
        self.assertEqual(claude_before, claude.read_bytes())
        self.assertEqual(agents_before, (self.target / "AGENTS.md").read_bytes())

    def test_missing_template_fails_before_writes(self):
        bad_root = self.target / "bad-butler"
        bad_root.mkdir()
        (bad_root / "VERSION").write_text("9.9.9\n")
        with self.assertRaises(OSError):
            MODULE.plan(self.target / "project", bad_root)
        self.assertFalse((self.target / "project" / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
