#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tools" / "butler-upgrade" / "upgrade.py"
SPEC = importlib.util.spec_from_file_location("butler_upgrade", SCRIPT)
assert SPEC and SPEC.loader
UPGRADE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = UPGRADE
SPEC.loader.exec_module(UPGRADE)

RENDER_SPEC = importlib.util.spec_from_file_location(
    "fixture_renderer", ROOT / "scripts" / "render-project-entrypoints.py"
)
assert RENDER_SPEC and RENDER_SPEC.loader
RENDER = importlib.util.module_from_spec(RENDER_SPEC)
sys.modules[RENDER_SPEC.name] = RENDER
RENDER_SPEC.loader.exec_module(RENDER)


def digest_tree(root: Path, *, ignore_runtime: bool = False) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if ignore_runtime and rel.parts[:2] == (".ai", "butler-upgrade"):
            continue
        if path.is_file() and not path.is_symlink():
            digest.update(rel.as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
    return digest.hexdigest()


class UpgradeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def project(self, version: str, *, agents: bool = True, user: str = "owner bytes") -> Path:
        project = self.base / f"project-{version.replace('.', '-')}-{len(list(self.base.iterdir()))}"
        project.mkdir()
        (project / ".ai").mkdir()
        RENDER.apply(RENDER.plan(project, ROOT))
        current = (ROOT / "VERSION").read_text().strip()
        for name in ("CLAUDE.md", "AGENTS.md"):
            path = project / name
            text = path.read_text().replace(f"butler v{current}", f"butler v{version}")
            text = text.replace(RENDER.USER_START + "\n", RENDER.USER_START + f"\n{user}-{name}\n", 1)
            path.write_text(text)
        if not agents:
            (project / "AGENTS.md").unlink()
        return project

    def manifest(self):
        return json.loads((ROOT / "migrations" / "manifest.json").read_text())

    def test_manifest_covers_every_recipe_and_rejects_bad_contracts(self):
        data = self.manifest()
        UPGRADE.validate_manifest(data, ROOT)
        recipes = {item["recipe"] for item in data["migrations"]}
        self.assertEqual(recipes, {p.name for p in (ROOT / "migrations").glob("v*.md")})
        mutations = []
        bad = copy.deepcopy(data); bad["migrations"][2]["source"] = "9.9.9"; mutations.append(bad)
        bad = copy.deepcopy(data); bad["migrations"][0]["actions"][0]["id"] = bad["migrations"][1]["actions"][0]["id"]; mutations.append(bad)
        bad = copy.deepcopy(data); bad["migrations"][0]["actions"][0]["type"] = "shell"; mutations.append(bad)
        bad = copy.deepcopy(data); bad["migrations"][0]["actions"][0]["domain"] = "machine"; mutations.append(bad)
        bad = copy.deepcopy(data); bad["migrations"][0]["actions"][0]["extra"] = "x"; mutations.append(bad)
        for value in mutations:
            with self.subTest(value=value["migrations"][0]):
                with self.assertRaises(UPGRADE.UpgradeError):
                    UPGRADE.validate_manifest(value, ROOT)

    def test_plan_is_zero_write_and_reports_machine_actions(self):
        project = self.project("2.14.0", agents=False)
        before = digest_tree(project)
        result = UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual(before, digest_tree(project))
        self.assertEqual("ready-with-external-pending", result["status"])
        self.assertTrue(result["changes"])
        self.assertTrue(result["external_pending"])
        self.assertEqual("2.14.0", result["from_version"])

    def test_cli_json_plan_is_zero_write_for_project_home_and_butler_inputs(self):
        project = self.project("2.14.0", agents=False)
        home = self.base / "home"; home.mkdir()
        tracked_inputs = [
            ROOT / "VERSION", ROOT / "migrations/manifest.json",
            ROOT / "templates/CLAUDE.md.template", ROOT / "templates/AGENTS.md.template",
            ROOT / "templates/rule-card.md", ROOT / "templates/settings.hooks-snippet.json",
        ]
        def inputs_digest():
            return hashlib.sha256(b"".join(path.read_bytes() for path in tracked_inputs)).hexdigest()
        before = (digest_tree(project), digest_tree(home), inputs_digest())
        env = dict(os.environ, HOME=str(home), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--butler-root", str(ROOT), "plan",
             "--project-root", str(project), "--split", "defer", "--json"],
            text=True, capture_output=True, env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("ready-with-external-pending", payload["status"])
        self.assertTrue(payload["actions"])
        self.assertTrue(payload["changes"])
        self.assertEqual(before, (digest_tree(project), digest_tree(home), inputs_digest()))

    def test_cross_version_apply_preserves_user_regions_and_is_idempotent(self):
        project = self.project("1.1.0", agents=False, user="precious")
        first = UPGRADE.build_plan(project, ROOT, "defer")
        applied = UPGRADE.apply_plan(first, project)
        self.assertIn(applied["status"], {"applied", "applied-external-pending"})
        current = (ROOT / "VERSION").read_text().strip()
        for name in ("CLAUDE.md", "AGENTS.md"):
            text = (project / name).read_text()
            self.assertIn(f"butler v{current}", text)
            if name == "CLAUDE.md":
                self.assertIn("precious-CLAUDE.md", text)
        self.assertTrue((project / ".claude/hooks/butler_gate.py").is_file())
        settings = json.loads((project / ".claude/settings.json").read_text())
        self.assertIn("PreToolUse", settings["hooks"])
        self.assertIn("PostToolUse", settings["hooks"])
        before = digest_tree(project, ignore_runtime=True)
        again = UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual("already-current", again["status"])
        self.assertEqual(before, digest_tree(project, ignore_runtime=True))

    def test_split_requires_explicit_decision_and_never_guesses_semantics(self):
        project = self.project("1.7.0", agents=False)
        (project / ".ai/PROJECT.md").write_text("# Knowledge\nprivate prose\n")
        before = digest_tree(project)
        undecided = UPGRADE.build_plan(project, ROOT, None)
        self.assertEqual("needs-decision", undecided["status"])
        self.assertEqual(before, digest_tree(project))
        now = UPGRADE.build_plan(project, ROOT, "now")
        self.assertEqual("manual-split", now["status"])
        self.assertEqual(before, digest_tree(project))
        deferred = UPGRADE.build_plan(project, ROOT, "defer")
        UPGRADE.apply_plan(deferred, project)
        self.assertEqual("# Knowledge\nprivate prose\n", (project / ".ai/PROJECT.md").read_text())

    def test_manual_bootstrap_and_entrypoint_drift_fail_closed(self):
        project = self.base / "unversioned"
        project.mkdir(); (project / ".ai").mkdir(); (project / "CLAUDE.md").write_text("owner\n")
        result = UPGRADE.build_plan(project, ROOT, None)
        self.assertEqual("manual-bootstrap", result["status"])
        drift = self.project("2.14.0")
        agents = drift / "AGENTS.md"
        agents.write_text(agents.read_text().replace("butler v2.14.0", "butler v2.15.0"))
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "version drift"):
            UPGRADE.build_plan(drift, ROOT, "defer")

    def test_marker_hook_and_split_drift_stop_before_writes(self):
        marker = self.project("2.15.0")
        (marker / "CLAUDE.md").write_text((marker / "CLAUDE.md").read_text() + RENDER.MANAGED_START)
        before = digest_tree(marker)
        with self.assertRaises(UPGRADE.UpgradeError):
            UPGRADE.build_plan(marker, ROOT, "defer")
        self.assertEqual(before, digest_tree(marker))
        hook = self.project("2.15.0")
        (hook / ".claude/hooks").mkdir(parents=True)
        (hook / ".claude/hooks/owner.py").write_text("custom\n")
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "recognized"):
            UPGRADE.build_plan(hook, ROOT, "defer")
        split = self.project("1.7.0", agents=False)
        (split / ".ai/project").mkdir()
        (split / ".ai/project/partial.md").write_text("x")
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "partially"):
            UPGRADE.build_plan(split, ROOT, "defer")

    def test_symlink_escape_and_self_target_are_rejected(self):
        project = self.project("2.15.0")
        outside = self.base / "outside"; outside.mkdir()
        (project / ".claude").symlink_to(outside, target_is_directory=True)
        before = digest_tree(outside)
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "symlink"):
            UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual(before, digest_tree(outside))
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "Butler itself"):
            UPGRADE.resolve_roots(str(ROOT), ROOT)

    def test_injected_failure_restores_every_project_file(self):
        project = self.project("2.15.0")
        before = digest_tree(project, ignore_runtime=True)
        plan = UPGRADE.build_plan(project, ROOT, "defer")
        with mock.patch.dict(os.environ, {"BUTLER_UPGRADE_FAIL_AFTER": "2"}):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "all project files restored") as raised:
                UPGRADE.apply_plan(plan, project)
        self.assertEqual(UPGRADE.EXIT_RESTORED, raised.exception.code)
        self.assertEqual(before, digest_tree(project, ignore_runtime=True))
        journals = list((project / ".ai/butler-upgrade/runs").glob("*/journal.json"))
        self.assertEqual(1, len(journals))
        self.assertEqual("failed-restored", json.loads(journals[0].read_text())["status"])

    def test_lock_is_fail_closed_and_not_removed(self):
        project = self.project("2.15.0")
        plan = UPGRADE.build_plan(project, ROOT, "defer")
        lock = project / ".ai/butler-upgrade/apply.lock"
        lock.parent.mkdir(parents=True); lock.write_text('{"pid": 1}\n')
        with self.assertRaises(UPGRADE.UpgradeError) as raised:
            UPGRADE.apply_plan(plan, project)
        self.assertEqual(UPGRADE.EXIT_LOCKED, raised.exception.code)
        self.assertTrue(lock.exists())
        with self.assertRaises(UPGRADE.UpgradeError) as planned:
            UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual(UPGRADE.EXIT_LOCKED, planned.exception.code)

    def test_change_after_plan_is_rejected_before_runtime_writes(self):
        project = self.project("2.15.0")
        plan = UPGRADE.build_plan(project, ROOT, "defer")
        claude = project / "CLAUDE.md"
        claude.write_text(claude.read_text() + "late owner edit\n")
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "changed after planning"):
            UPGRADE.apply_plan(plan, project)
        self.assertFalse((project / ".ai/butler-upgrade").exists())

    def test_transaction_preparation_failure_changes_no_target_and_releases_lock(self):
        project = self.project("2.15.0")
        before = digest_tree(project, ignore_runtime=True)
        plan = UPGRADE.build_plan(project, ROOT, "defer")
        original = UPGRADE.atomic_write
        def fail_runtime(path, content, mode):
            if ".ai/butler-upgrade" in path.as_posix():
                raise OSError("injected preparation failure")
            return original(path, content, mode)
        with mock.patch.object(UPGRADE, "atomic_write", side_effect=fail_runtime):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "no target files changed") as raised:
                UPGRADE.apply_plan(plan, project)
        self.assertEqual(UPGRADE.EXIT_RESTORED, raised.exception.code)
        self.assertEqual(before, digest_tree(project, ignore_runtime=True))
        self.assertFalse((project / ".ai/butler-upgrade/apply.lock").exists())

    def test_parameterized_rename_is_planned_without_overwriting_destination(self):
        project = self.project("2.15.0")
        old = project / ".ai/SESSION_HANDOFF.md"
        old.write_text("history\n")
        manifest = self.manifest()
        migration = manifest["migrations"][-1]
        target = migration["target"]
        migration["actions"].insert(0, {
            "id": f"{target}/00-rename-handoff", "type": "rename", "domain": "project",
            "preconditions": ["source-destination-shape-valid", "target-path-owned"],
            "from": ".ai/SESSION_HANDOFF.md", "to": ".ai/02_SESSION_HANDOFF.md",
        })
        original = UPGRADE.read_json
        def fake_read(path):
            return manifest if path.name == "manifest.json" else original(path)
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            plan = UPGRADE.build_plan(project, ROOT, "defer")
        paths = {(item["operation"], item["path"]) for item in plan["changes"]}
        self.assertIn(("delete", ".ai/SESSION_HANDOFF.md"), paths)
        self.assertIn(("write", ".ai/02_SESSION_HANDOFF.md"), paths)
        (project / ".ai/02_SESSION_HANDOFF.md").write_text("owner\n")
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "rename conflict"):
                UPGRADE.build_plan(project, ROOT, "defer")

    def test_global_install_needs_separate_confirmation(self):
        with self.assertRaises(UPGRADE.UpgradeError) as raised:
            UPGRADE.global_install(ROOT, False)
        self.assertEqual(UPGRADE.EXIT_DECISION, raised.exception.code)

    def test_manifest_rejects_protected_action_paths_and_bad_preconditions(self):
        data = self.manifest()
        add = next(
            action for migration in data["migrations"] for action in migration["actions"]
            if action["type"] == "add_field"
        )
        add["path"] = "origin/owner.md"
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "not owned"):
            UPGRADE.validate_manifest(data, ROOT)
        data = self.manifest()
        data["migrations"][0]["actions"][0]["preconditions"] = []
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "preconditions"):
            UPGRADE.validate_manifest(data, ROOT)

    def test_current_stamp_does_not_hide_content_drift(self):
        current = (ROOT / "VERSION").read_text().strip()
        project = self.project(current)
        claude = project / "CLAUDE.md"
        claude.write_text(claude.read_text().replace("# 项目工程协作规则", "# drifted rules", 1))
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "content drift"):
            UPGRADE.build_plan(project, ROOT, "defer")
        ambiguous = self.base / "ambiguous"
        ambiguous.mkdir(); (ambiguous / ".ai").mkdir()
        (ambiguous / "CLAUDE.md").write_text(f"> 规则源：butler v{current}\nowner\n")
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "ambiguous"):
            UPGRADE.build_plan(ambiguous, ROOT, "defer")


if __name__ == "__main__":
    unittest.main()
