#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import io
import os
import shlex
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).with_name("configure-global-install.py")
SPEC = importlib.util.spec_from_file_location("configure_global_install", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class GlobalInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = SCRIPT.parent.parent.resolve()
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name) / "home"
        self.home.mkdir()
        self.zshrc = self.home / ".zshrc"
        self.zshrc.write_text("", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    @property
    def claude_md(self) -> Path:
        return self.home / ".claude" / "CLAUDE.md"

    @property
    def command_link(self) -> Path:
        return self.home / ".claude" / "commands" / "butler"

    def plan(self):
        return MODULE.plan_global_install(self.home, self.repo)

    def apply(self) -> None:
        with redirect_stdout(io.StringIO()):
            MODULE.apply_global_install(self.plan())

    def test_first_install_and_second_run_are_idempotent(self) -> None:
        self.apply()
        first = {
            "zshrc": self.zshrc.read_bytes(),
            "claude": self.claude_md.read_bytes(),
            "link": os.readlink(self.command_link),
        }
        self.apply()
        self.assertEqual(first["zshrc"], self.zshrc.read_bytes())
        self.assertEqual(first["claude"], self.claude_md.read_bytes())
        self.assertEqual(first["link"], os.readlink(self.command_link))
        self.assertEqual(1, self.zshrc.read_text().count("export BUTLER_PATH="))
        self.assertEqual(2, self.claude_md.read_text().count(MODULE.GLOBAL_MARKER))

    def test_orphan_marker_rejects_all_writes_and_preserves_mode(self) -> None:
        self.claude_md.parent.mkdir(parents=True)
        original = b"before\n<!-- butler-global-config -->\nUSER DATA AFTER\n"
        self.claude_md.write_bytes(original)
        self.claude_md.chmod(0o600)
        self.zshrc.write_text("# untouched\n", encoding="utf-8")
        before_shell = self.zshrc.read_bytes()
        with self.assertRaises(MODULE.ConfigError):
            self.plan()
        self.assertEqual(original, self.claude_md.read_bytes())
        self.assertEqual(0o600, stat.S_IMODE(self.claude_md.stat().st_mode))
        self.assertEqual(before_shell, self.zshrc.read_bytes())
        self.assertFalse(self.command_link.exists())

    def test_duplicate_or_inline_markers_reject_without_writes(self) -> None:
        self.claude_md.parent.mkdir(parents=True)
        for text in (
            "\n".join([MODULE.GLOBAL_MARKER] * 4) + "\n",
            f"prefix {MODULE.GLOBAL_MARKER} suffix\n",
        ):
            with self.subTest(text=text):
                self.claude_md.write_text(text, encoding="utf-8")
                before = self.claude_md.read_bytes()
                with self.assertRaises(MODULE.ConfigError):
                    self.plan()
                self.assertEqual(before, self.claude_md.read_bytes())

    def test_valid_managed_pair_preserves_prefix_suffix_mode_and_is_idempotent(self) -> None:
        self.claude_md.parent.mkdir(parents=True)
        self.claude_md.write_text(
            "owner prefix  \n"
            f"{MODULE.GLOBAL_MARKER}\nold managed\n{MODULE.GLOBAL_MARKER}\n"
            "owner suffix\n",
            encoding="utf-8",
        )
        self.claude_md.chmod(0o640)
        self.apply()
        text = self.claude_md.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("owner prefix  \n"))
        self.assertTrue(text.endswith("owner suffix\n"))
        self.assertNotIn("old managed", text)
        self.assertEqual(2, text.count(MODULE.GLOBAL_MARKER))
        self.assertEqual(0o640, stat.S_IMODE(self.claude_md.stat().st_mode))
        before = self.claude_md.read_bytes()
        self.apply()
        self.assertEqual(before, self.claude_md.read_bytes())

    def test_managed_pair_preserves_crlf_user_bytes(self) -> None:
        self.claude_md.parent.mkdir(parents=True)
        prefix = b"owner prefix  \r\nsecond\r\n"
        suffix = b"owner suffix\r\nlast-without-newline"
        self.claude_md.write_bytes(
            prefix
            + MODULE.GLOBAL_MARKER.encode()
            + b"\r\nold managed\r\n"
            + MODULE.GLOBAL_MARKER.encode()
            + b"\r\n"
            + suffix
        )
        self.apply()
        updated = self.claude_md.read_bytes()
        self.assertTrue(updated.startswith(prefix))
        self.assertTrue(updated.endswith(suffix))

    def test_comment_or_plain_text_does_not_fake_existing_export(self) -> None:
        self.zshrc.write_text(
            "# tool reads BUTLER_PATH here\nOTHER_BUTLER_PATH=value\n",
            encoding="utf-8",
        )
        self.apply()
        text = self.zshrc.read_text(encoding="utf-8")
        self.assertIn("# tool reads BUTLER_PATH here", text)
        self.assertIn("OTHER_BUTLER_PATH=value", text)
        self.assertEqual(1, text.count("export BUTLER_PATH="))

    def test_one_export_updates_in_place_and_preserves_mode(self) -> None:
        self.zshrc.write_text(
            "before\n  export   BUTLER_PATH = '/old/path'\nafter\n",
            encoding="utf-8",
        )
        self.zshrc.chmod(0o600)
        self.apply()
        lines = self.zshrc.read_text(encoding="utf-8").splitlines()
        self.assertEqual("before", lines[0])
        self.assertEqual(f"export BUTLER_PATH={shlex.quote(str(self.repo))}", lines[1])
        self.assertEqual("after", lines[2])
        self.assertEqual(0o600, stat.S_IMODE(self.zshrc.stat().st_mode))

    def test_multiple_exports_reject_before_any_write(self) -> None:
        original = "export BUTLER_PATH=/one\n export BUTLER_PATH=/two\n"
        self.zshrc.write_text(original, encoding="utf-8")
        with self.assertRaises(MODULE.ConfigError):
            self.plan()
        self.assertEqual(original, self.zshrc.read_text(encoding="utf-8"))
        self.assertFalse(self.claude_md.exists())

    def test_shell_path_is_quoted_as_data_not_code(self) -> None:
        root = Path("/tmp/butler $(touch should-not-run) 'quoted'")
        merged = MODULE.merge_shell_rc("", root)
        self.assertIn(f"export BUTLER_PATH={shlex.quote(str(root))}", merged)
        self.assertNotIn('BUTLER_PATH="/tmp/butler $(', merged)

    def test_real_command_directory_rejects_without_internal_link(self) -> None:
        self.command_link.mkdir(parents=True)
        owner_file = self.command_link / "user.md"
        owner_file.write_text("mine", encoding="utf-8")
        with self.assertRaises(MODULE.ConfigError):
            self.plan()
        self.assertEqual("mine", owner_file.read_text(encoding="utf-8"))
        self.assertEqual([owner_file], list(self.command_link.iterdir()))

    def test_unrelated_or_unowned_broken_symlink_rejects(self) -> None:
        self.command_link.parent.mkdir(parents=True)
        targets = (Path("/tmp/not-butler"), Path(self.temp.name) / "gone" / "commands")
        for target in targets:
            with self.subTest(target=target):
                if os.path.lexists(self.command_link):
                    self.command_link.unlink()
                self.command_link.symlink_to(target)
                with self.assertRaises(MODULE.ConfigError):
                    self.plan()
                self.assertEqual(str(target), os.readlink(self.command_link))

    def test_current_link_is_kept_and_recognizable_old_checkout_is_migrated(self) -> None:
        self.command_link.parent.mkdir(parents=True)
        self.command_link.symlink_to(self.repo / ".claude" / "commands" / "butler")
        self.apply()
        self.assertEqual(
            str(self.repo / ".claude" / "commands" / "butler"),
            os.readlink(self.command_link),
        )

        self.command_link.unlink()
        old_root = Path(self.temp.name) / "old-butler"
        (old_root / "Coder").mkdir(parents=True)
        (old_root / "scripts").mkdir()
        (old_root / ".claude" / "commands" / "butler").mkdir(parents=True)
        (old_root / "Coder" / "README.md").write_text("old", encoding="utf-8")
        (old_root / "scripts" / "setup.sh").write_text("old", encoding="utf-8")
        self.command_link.symlink_to(old_root / ".claude" / "commands" / "butler")
        self.apply()
        self.assertEqual(
            str(self.repo / ".claude" / "commands" / "butler"),
            os.readlink(self.command_link),
        )

    def test_owned_legacy_flat_link_is_removed_but_unrelated_link_is_preserved(self) -> None:
        commands = self.home / ".claude" / "commands"
        commands.mkdir(parents=True)
        legacy = commands / "butler-prd.md"
        legacy.symlink_to(self.repo / ".claude" / "commands" / "butler-prd.md")
        self.apply()
        self.assertFalse(os.path.lexists(legacy))

        legacy.symlink_to("/tmp/user-command.md")
        plan = self.plan()
        with redirect_stdout(io.StringIO()):
            MODULE.apply_global_install(plan)
        self.assertTrue(legacy.is_symlink())
        self.assertEqual("/tmp/user-command.md", os.readlink(legacy))

    def test_symlinked_user_config_is_rejected_instead_of_replaced(self) -> None:
        real = Path(self.temp.name) / "real-zshrc"
        real.write_text("owner\n", encoding="utf-8")
        self.zshrc.unlink()
        self.zshrc.symlink_to(real)
        with self.assertRaises(MODULE.ConfigError):
            self.plan()
        self.assertTrue(self.zshrc.is_symlink())
        self.assertEqual("owner\n", real.read_text(encoding="utf-8"))

    def test_apply_rejects_user_file_change_after_plan_before_any_commit(self) -> None:
        plan = self.plan()
        self.zshrc.write_text("user changed this after plan\n", encoding="utf-8")
        with self.assertRaises(MODULE.ConfigError):
            with redirect_stdout(io.StringIO()):
                MODULE.apply_global_install(plan)
        self.assertEqual("user changed this after plan\n", self.zshrc.read_text(encoding="utf-8"))
        self.assertFalse(self.claude_md.exists())
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse(os.path.lexists(self.command_link))

    def test_apply_rejects_command_target_change_after_plan_before_any_commit(self) -> None:
        plan = self.plan()
        self.command_link.mkdir(parents=True)
        (self.command_link / "owner.md").write_text("mine", encoding="utf-8")
        with self.assertRaises(MODULE.ConfigError):
            with redirect_stdout(io.StringIO()):
                MODULE.apply_global_install(plan)
        self.assertEqual("", self.zshrc.read_text(encoding="utf-8"))
        self.assertFalse(self.claude_md.exists())
        self.assertEqual("mine", (self.command_link / "owner.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
