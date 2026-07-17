#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("resolve-project-root.py")
SPEC = importlib.util.spec_from_file_location("resolve_project_root", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProjectRootTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def git_init(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", str(root)], check=True)

    def test_explicit_target_wins_outside_start(self):
        start = self.base / "session"
        target = self.base / "actual-project"
        start.mkdir()
        target.mkdir()
        result = MODULE.resolve_project_root(user_target=target, start=start)
        self.assertEqual(target.resolve(), result.root)
        self.assertEqual("user-target", result.evidence)

    def test_explicit_non_git_directory_is_valid(self):
        target = self.base / "new-project"
        target.mkdir()
        result = MODULE.resolve_project_root(user_target=target)
        self.assertEqual(target.resolve(), result.root)

    def test_missing_or_file_target_is_rejected(self):
        with self.assertRaises(MODULE.RootResolutionError):
            MODULE.resolve_project_root(user_target=self.base / "missing")
        file_target = self.base / "file"
        file_target.write_text("x")
        with self.assertRaises(MODULE.RootResolutionError):
            MODULE.resolve_project_root(user_target=file_target)

    def test_nested_git_directory_resolves_top_level(self):
        repo = self.base / "repo"
        nested = repo / "packages" / "app"
        self.git_init(repo)
        nested.mkdir(parents=True)
        result = MODULE.resolve_project_root(start=nested)
        self.assertEqual(repo.resolve(), result.root)
        self.assertEqual("vcs-root", result.evidence)

    def test_nearest_existing_butler_root_wins_without_git(self):
        project = self.base / "project"
        nested = project / "src" / "feature"
        (project / ".ai").mkdir(parents=True)
        nested.mkdir(parents=True)
        (project / "AGENTS.md").write_text(
            "<!-- butler-managed:start -->\nmanaged\n<!-- butler-managed:end -->\n"
        )
        result = MODULE.resolve_project_root(start=nested)
        self.assertEqual(project.resolve(), result.root)
        self.assertEqual("butler-root", result.evidence)

    def test_multi_repo_parent_is_rejected_without_writes(self):
        aggregate = self.base / "aggregate"
        self.git_init(aggregate / "one")
        self.git_init(aggregate / "two")
        before = sorted(path.relative_to(aggregate) for path in aggregate.rglob("*"))
        with self.assertRaises(MODULE.RootResolutionError):
            MODULE.resolve_project_root(start=aggregate)
        after = sorted(path.relative_to(aggregate) for path in aggregate.rglob("*"))
        self.assertEqual(before, after)
        self.assertFalse((aggregate / ".ai").exists())

    def test_symlink_resolves_to_real_absolute_path(self):
        target = self.base / "real"
        link = self.base / "linked"
        target.mkdir()
        link.symlink_to(target, target_is_directory=True)
        result = MODULE.resolve_project_root(user_target=link)
        self.assertEqual(target.resolve(), result.root)


if __name__ == "__main__":
    unittest.main()
