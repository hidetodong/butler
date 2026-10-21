#!/usr/bin/env python3
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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
        if path.name == ".usage.json":
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

    def manifest_with_config_migration(self):
        manifest = self.manifest()
        current = (ROOT / "VERSION").read_text().strip()
        released = next(item for item in manifest["migrations"] if item["target"] == current)
        if any(
            action["type"] == "migrate_config"
            for item in manifest["migrations"]
            if UPGRADE.semver(item["target"]) <= UPGRADE.semver(current)
            for action in item["actions"]
        ):
            return manifest
        migration = released
        target = migration["target"]
        migration["actions"].insert(-1, {
            "id": f"{target}/test-migrate-config",
            "type": "migrate_config",
            "domain": "project",
            "preconditions": ["legacy-config-readable", "target-path-owned"],
        })
        return manifest

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

    def test_v330_registers_project_config_migration_before_entrypoints(self):
        migration = next(item for item in self.manifest()["migrations"] if item["target"] == "3.3.0")
        self.assertEqual(("3.2.0", "3.3.0", "v3.3.0.md"), (
            migration["source"], migration["target"], migration["recipe"]
        ))
        self.assertEqual(
            ["global_install", "migrate_config", "regen_entrypoints", "restamp"],
            [action["type"] for action in migration["actions"]],
        )

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

    def test_historical_split_no_longer_stops_for_project_md(self):
        project = self.project("1.7.0", agents=False)
        (project / ".ai/PROJECT.md").write_text("# Knowledge\nprivate prose\n")
        before = digest_tree(project)
        undecided = UPGRADE.build_plan(project, ROOT, None)
        self.assertNotIn(undecided["status"], {"needs-decision", "manual-split"})
        self.assertFalse(any(action["id"].startswith("4.0.0/") for action in undecided["actions"]))
        self.assertEqual(before, digest_tree(project))
        self.assertEqual("# Knowledge\nprivate prose\n", (project / ".ai/PROJECT.md").read_text())
        deferred = UPGRADE.build_plan(project, ROOT, "defer")
        now = UPGRADE.build_plan(project, ROOT, "now")
        self.assertEqual(deferred["status"], now["status"])
        self.assertEqual(deferred["status"], undecided["status"])

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
        planned = UPGRADE.build_plan(split, ROOT, None)
        self.assertNotIn(planned["status"], {"needs-decision", "manual-split"})
        self.assertTrue((split / ".ai/project/partial.md").is_file())
        self.assertFalse(any(action["id"].startswith("4.0.0/") for action in planned["actions"]))

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
        current = (ROOT / "VERSION").read_text().strip()
        migration = next(item for item in manifest["migrations"] if item["target"] == current)
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

    def test_config_migration_action_is_zero_write_transactional_and_idempotent(self):
        project = self.project("3.1.0")
        local = project / ".ai/local-constraints.md"
        local.write_text(
            "# Project Type\n- CLI\n\n"
            "# Active Profiles\n- `typescript-rules`\n\n"
            "# Local Constraints\n- preserve me\n\n"
            "# Butler 功能开关\n"
            "- dangerous: on\n"
            "- independent_review: off\n"
            "- preference: on\n",
            encoding="utf-8",
        )
        manifest = self.manifest_with_config_migration()
        original = UPGRADE.read_json

        def fake_read(path):
            return manifest if path.name == "manifest.json" else original(path)

        before = digest_tree(project)
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            plan = UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual(before, digest_tree(project))
        paths = {(item["operation"], item["path"]) for item in plan["changes"]}
        self.assertIn(("write", ".ai/butler.config.json"), paths)
        self.assertIn(("write", ".ai/local-constraints.md"), paths)

        applied = UPGRADE.apply_plan(plan, project)
        self.assertIn(applied["status"], {"applied", "applied-external-pending"})
        config = json.loads((project / ".ai/butler.config.json").read_text())
        self.assertTrue(config["dangerous"])
        self.assertEqual(["typescript-rules"], config["profiles"])
        narrowed = local.read_text()
        self.assertNotIn("# Active Profiles", narrowed)
        self.assertNotIn("# Butler 功能开关", narrowed)
        self.assertIn("# Local Constraints\n- preserve me", narrowed)

        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            again = UPGRADE.build_plan(project, ROOT, "defer")
        self.assertEqual("already-current", again["status"])

        (project / ".ai/butler.config.json").unlink()
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "configuration drift"):
                UPGRADE.build_plan(project, ROOT, "defer")

    def test_config_migration_conflict_and_failure_leave_no_half_state(self):
        conflict = self.project("3.1.0")
        local = conflict / ".ai/local-constraints.md"
        local.write_text("# Butler 功能开关\n- dangerous: on\n")
        config_tool = UPGRADE.load_project_config(ROOT)
        config_tool.initialize(conflict)
        manifest = self.manifest_with_config_migration()
        original = UPGRADE.read_json

        def fake_read(path):
            return manifest if path.name == "manifest.json" else original(path)

        before = digest_tree(conflict)
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "conflict"):
                UPGRADE.build_plan(conflict, ROOT, "defer")
        self.assertEqual(before, digest_tree(conflict))

        project = self.project("3.1.0")
        local = project / ".ai/local-constraints.md"
        local.write_text(
            "# Active Profiles\n- none\n\n"
            "# Local Constraints\n- preserve\n\n"
            "# Butler 功能开关\n- dangerous: off\n",
            encoding="utf-8",
        )
        before = digest_tree(project, ignore_runtime=True)
        with mock.patch.object(UPGRADE, "read_json", side_effect=fake_read):
            plan = UPGRADE.build_plan(project, ROOT, "defer")
        with mock.patch.dict(os.environ, {"BUTLER_UPGRADE_FAIL_AFTER": "2"}):
            with self.assertRaisesRegex(UPGRADE.UpgradeError, "all project files restored"):
                UPGRADE.apply_plan(plan, project)
        self.assertEqual(before, digest_tree(project, ignore_runtime=True))
        self.assertFalse((project / ".ai/butler.config.json").exists())
        self.assertIn("# Butler 功能开关", local.read_text())

    def test_manifest_rejects_protected_action_paths_and_bad_preconditions(self):
        data = self.manifest()
        add = next(
            action for migration in data["migrations"] for action in migration["actions"]
            if action["type"] == "add_field"
        )
        add["path"] = ".ai/references/raw/owner.md"
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

    def test_hook_filter_is_single_source_and_excludes_pytest_scaffold(self):
        """AC1 / AC2：源侧与目标侧共用同一过滤口径，且都不把 pytest 脚手架计入摘要。"""
        for name in UPGRADE.NON_DEPLOYED_HOOK_FILES:
            self.assertTrue(
                (ROOT / "templates" / "hooks" / name).is_file(),
                f"排除清单项在 templates/hooks 下不存在，排除会静默失效: {name}",
            )
        tree = self.base / "hooktree"
        (tree / "lib").mkdir(parents=True)
        (tree / "tests").mkdir()
        (tree / "__pycache__").mkdir()
        (tree / "butler_gate.py").write_text("gate\n")
        (tree / "lib" / "io.py").write_text("io\n")
        (tree / "lib" / "conftest.py").write_text("nested stays\n")
        (tree / "conftest.py").write_text("")
        (tree / "pytest.ini").write_text("[pytest]\n")
        (tree / "tests" / "test_gate.py").write_text("t\n")
        (tree / "__pycache__" / "gate.pyc").write_bytes(b"\x00")
        (tree / "stale.pyc").write_bytes(b"\x00")

        fake_butler = self.base / "fake-butler"
        (fake_butler / "templates").mkdir(parents=True)
        shutil.copytree(tree, fake_butler / "templates" / "hooks")
        fake_project = self.base / "fake-project"
        (fake_project / ".claude").mkdir(parents=True)
        shutil.copytree(tree, fake_project / ".claude" / "hooks")

        source = UPGRADE.hook_source_files(fake_butler)
        target = UPGRADE.target_hook_files(fake_project)
        self.assertEqual(source, target, "源侧与目标侧口径分叉会让树摘要永久错位")
        self.assertEqual(
            {"butler_gate.py", "lib/io.py", "lib/conftest.py"},
            {path.as_posix() for path in source},
        )
        self.assertEqual(UPGRADE.tree_digest(source), UPGRADE.tree_digest(target))

    def test_modified_hook_tree_is_still_refused(self):
        """AC6：内容被改或含项目独有文件的 hook 树仍须拒绝覆盖，且零写入。"""
        source = UPGRADE.hook_source_files(ROOT)

        def modify_existing(hooks: Path) -> None:
            victim = hooks / "rules" / "phase_gate.py"
            victim.write_bytes(victim.read_bytes() + b"\n# tampered\n")

        def add_owned_file(hooks: Path) -> None:
            (hooks / "rules" / "custom.py").write_text("owner rule\n")

        for label, mutate in (("modified-content", modify_existing), ("extra-file", add_owned_file)):
            with self.subTest(drift=label):
                project = self.project("2.14.0")
                hooks = project / ".claude" / "hooks"
                for rel, content in source.items():
                    target = hooks / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                mutate(hooks)
                before = digest_tree(project)
                with self.assertRaisesRegex(UPGRADE.UpgradeError, "hook tree"):
                    UPGRADE.build_plan(project, ROOT, "defer")
                self.assertEqual(before, digest_tree(project), "拒绝路径必须零写入")

    def test_whitelist_holds_only_recomputable_history_digests(self):
        """AC3：白名单每项都能被某个历史 tag 按当前口径复现，混口径值会被这条抓住。"""
        digests = self.manifest()["known_hook_tree_digests"]
        self.assertEqual(len(digests), len(set(digests)), "白名单不得有重复项")

        probe = subprocess.run(
            ["git", "-C", str(ROOT), "tag"], capture_output=True, text=True, check=False
        )
        if probe.returncode != 0 or not probe.stdout.strip():
            self.skipTest("git tag 不可用（浅克隆或无 tag），跳过历史复算对账")

        available = set(probe.stdout.split())
        checkpoints = [tag for tag in ("v1.0.0", "v2.18.0", "v3.1.0") if tag in available]
        if not checkpoints:
            self.skipTest("代表性 tag 均不存在，跳过历史复算对账")

        for tag in checkpoints:
            with self.subTest(tag=tag):
                self.assertIn(
                    self._historic_hook_digest(tag),
                    set(digests),
                    f"{tag} 的 hook 树摘要不在白名单里，该版本部署的项目将无法升级",
                )

        current = UPGRADE.tree_digest(UPGRADE.hook_source_files(ROOT))
        released = (ROOT / "VERSION").read_text().strip()
        tag_name = f"v{released}"
        if tag_name in available:
            historic = self._historic_hook_digest(tag_name)
            self.assertTrue(
                current == historic or current in set(digests),
                "工作区 hook 树摘要必须等于当前 VERSION 对应 tag，或已登记进 known_hook_tree_digests",
            )

    def entrypoints(self, project: Path, version: str = "0.0.0") -> None:
        text = f"<!-- user-managed -->\n规则源：butler v{version}\n<!-- /user-managed -->\n"
        (project / "CLAUDE.md").write_text(text)
        (project / "AGENTS.md").write_text(text)

    def deployed_project(self, name: str) -> Path:
        project = self.base / name
        project.mkdir()
        (project / ".ai").mkdir()
        self.entrypoints(project)
        return project

    def action_fixture(self, action: dict) -> Path:
        suffix = action["id"].split("/", 1)[1]
        root = self.base / f"butler-{len(list(self.base.iterdir()))}-{suffix}"
        (root / "migrations").mkdir(parents=True)
        (root / "VERSION").write_text("0.0.1\n")
        (root / "migrations" / "v0.0.1.md").write_text("# stub\n")
        manifest = {
            "schema_version": 1,
            "baseline_version": "0.0.0",
            "known_hook_tree_digests": [],
            "migrations": [{
                "source": "0.0.0",
                "target": "0.0.1",
                "recipe": "v0.0.1.md",
                "actions": [action],
            }],
        }
        (root / "migrations" / "manifest.json").write_text(json.dumps(manifest))
        return root

    def apply_action(self, project: Path, action: dict) -> int:
        butler = self.action_fixture(action)
        with redirect_stdout(io.StringIO()):
            return UPGRADE.main([
                "--butler-root", str(butler),
                "apply",
                "--project-root", str(project),
                "--split", "defer",
            ])

    def test_schema_defines_delete_and_move_and_keeps_split(self):
        text = (ROOT / "Coder/20_Workflow_Lifecycle/migration-schema.md").read_text()
        section = text.split("## 4. typed 操作标签", 1)[1].split("## 5.", 1)[0]
        self.assertLess(section.index("[delete]"), section.index("[split]"))
        self.assertLess(section.index("[move]"), section.index("[split]"))
        self.assertIn("知识文件夹", section)
        for tag in ("[delete]", "[move]"):
            body = section.split(tag, 1)[1].split("\n- `[", 1)[0]
            for phrase in ("起始态", "重复", "冲突", "不覆盖"):
                self.assertIn(phrase, body, tag)
        readme = (ROOT / "tools/butler-upgrade/README.md").read_text()
        self.assertIn("rename/add-field、delete/move、", readme)

    def test_v4_recipe_is_linked_and_not_selected_before_version_cut(self):
        self.assertTrue((ROOT / "migrations" / "v4.0.0.md").is_file())
        self.assertEqual("3.6.0", (ROOT / "VERSION").read_text().strip())
        data = self.manifest()
        UPGRADE.validate_manifest(data, ROOT)
        section = next(item for item in data["migrations"] if item["target"] == "4.0.0")
        self.assertEqual(("3.6.0", "v4.0.0.md"), (section["source"], section["recipe"]))
        self.assertEqual(
            [
                "global_install", "delete", "delete", "move", "migrate_config",
                "regen_entrypoints", "sync_hooks", "restamp",
            ],
            [action["type"] for action in section["actions"]],
        )
        by_id = {action["id"]: action for action in section["actions"]}
        self.assertEqual(".ai/project", by_id["4.0.0/02-delete-project-dir"]["path"])
        self.assertEqual(".ai/PROJECT.md", by_id["4.0.0/03-delete-project-md"]["path"])
        self.assertEqual("deliveries", by_id["4.0.0/04-move-deliveries"]["from"])
        self.assertEqual(".ai/deliveries", by_id["4.0.0/04-move-deliveries"]["to"])
        schema = (ROOT / "Coder/20_Workflow_Lifecycle/migration-schema.md").read_text()
        split = schema.split("- `[split]`：", 1)[1].split("\n- `", 1)[0]
        self.assertIn("知识文件夹", split)
        self.assertIn("退役", split)
        project = self.project("3.6.0")
        (project / ".ai" / "butler.config.json").write_text(
            json.dumps({
                "schema_version": 1,
                "dangerous": False,
                "independent_review": False,
                "profiles": [],
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        plan = UPGRADE.build_plan(project, ROOT, None)
        self.assertFalse(any(action["id"].startswith("4.0.0/") for action in plan["actions"]))

    def test_manifest_accepts_delete_and_move_and_rejects_illegal_paths(self):
        data = self.manifest()
        UPGRADE.validate_manifest(data, ROOT)
        migration = copy.deepcopy(data)
        target = migration["migrations"][0]["target"]
        migration["migrations"][0]["actions"][0] = {
            "id": f"{target}/delete-shape",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin",
        }
        UPGRADE.validate_manifest(migration, ROOT)
        moved = copy.deepcopy(data)
        moved["migrations"][0]["actions"][0] = {
            "id": f"{target}/move-shape",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        }
        UPGRADE.validate_manifest(moved, ROOT)
        illegal = [
            {"type": "delete", "path": ".."},
            {"type": "delete", "path": "/tmp/outside"},
            {"type": "delete", "path": ".ai"},
            {"type": "delete", "path": ".ai/iterations"},
            {"type": "delete", "path": ".ai/milestones/x"},
            {"type": "delete", "path": ".ai/references/x"},
            {"type": "delete", "path": ".ai/verification-evidence/x"},
            {"type": "delete", "path": ".ai/butler-upgrade/x"},
            {"type": "move", "from": "origin", "to": "other"},
            {"type": "move", "from": ".ai/notes", "to": ".ai/notes"},
            {"type": "move", "from": ".ai/box", "to": ".ai/box/nested"},
            {"type": "move", "from": "origin", "to": ".ai"},
            {"type": "move", "from": "origin", "to": ".ai/iterations/origin"},
        ]
        for fields in illegal:
            with self.subTest(fields=fields):
                bad = copy.deepcopy(data)
                action = {
                    "id": f"{target}/bad",
                    "domain": "project",
                    "preconditions": [
                        "delete-path-allowed" if fields["type"] == "delete" else "move-path-allowed"
                    ],
                }
                action.update(fields)
                bad["migrations"][0]["actions"][0] = action
                with self.assertRaises(UPGRADE.UpgradeError):
                    UPGRADE.validate_manifest(bad, ROOT)

    def test_apply_without_split_is_accepted(self):
        project = self.project("3.6.0")
        (project / ".ai" / "butler.config.json").write_text(
            json.dumps({
                "schema_version": 1,
                "dangerous": False,
                "independent_review": False,
                "profiles": [],
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        for extra in ([], ["--split", "defer"], ["--split", "now"]):
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--butler-root", str(ROOT),
                 "apply", "--project-root", str(project), *extra],
                capture_output=True, text=True,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)

    def test_delete_removes_file_or_directory_and_is_idempotent(self):
        project = self.deployed_project("delete-file")
        (project / "origin.txt").write_bytes(b"gone")
        (project / "stay.txt").write_bytes(b"stay")
        self.assertEqual(0, self.apply_action(project, {
            "id": "0.0.1/delete-file",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin.txt",
        }))
        self.assertFalse((project / "origin.txt").exists())
        self.assertEqual(b"stay", (project / "stay.txt").read_bytes())
        self.assertEqual(0, self.apply_action(project, {
            "id": "0.0.1/delete-file-again",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin.txt",
        }))

        directory = self.deployed_project("delete-dir")
        nested = directory / "origin" / "sub"
        nested.mkdir(parents=True)
        (nested / "a.txt").write_bytes(b"nested")
        (directory / "origin" / "b.txt").write_bytes(b"top")
        (directory / "origin" / "empty").mkdir()
        butler = self.action_fixture({
            "id": "0.0.1/delete-dir",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin",
        })
        plan = UPGRADE.build_plan(directory, butler, "defer")
        kinds = [change.operation for change in plan["_planned"]]
        self.assertEqual(["delete", "delete", "remove-dir", "remove-dir", "remove-dir"], kinds)
        remove_paths = [
            change.path.relative_to(directory.resolve()).as_posix()
            for change in plan["_planned"] if change.operation == "remove-dir"
        ]
        self.assertEqual(["origin/empty", "origin/sub", "origin"], remove_paths)
        applied = UPGRADE.apply_plan(plan, directory)
        self.assertEqual("applied", applied["status"])
        self.assertFalse((directory / "origin").exists())

        empty = self.deployed_project("delete-empty")
        (empty / "origin").mkdir()
        self.assertEqual(0, self.apply_action(empty, {
            "id": "0.0.1/delete-empty",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin",
        }))
        self.assertFalse((empty / "origin").exists())

    def test_delete_refuses_protected_paths_without_removing_files(self):
        project = self.deployed_project("delete-protected")
        kept = project / ".ai" / "iterations" / "keep.txt"
        kept.parent.mkdir(parents=True)
        kept.write_bytes(b"archive")
        (project / "stay.txt").write_bytes(b"stay")
        before = digest_tree(project)
        for path in ("../outside", "/tmp/outside", ".ai", ".ai/iterations", ".ai/butler-upgrade/run"):
            with self.subTest(path=path):
                code = self.apply_action(project, {
                    "id": "0.0.1/delete-protected",
                    "type": "delete",
                    "domain": "project",
                    "preconditions": ["delete-path-allowed"],
                    "path": path,
                })
                self.assertEqual(2, code)
                self.assertEqual(b"archive", kept.read_bytes())
                self.assertEqual(b"stay", (project / "stay.txt").read_bytes())
                self.assertEqual(before, digest_tree(project))

    def test_move_relocates_repo_root_into_ai_and_checks_start_state(self):
        project = self.deployed_project("move-file")
        (project / "origin.txt").write_bytes(b"abc")
        self.assertEqual(0, self.apply_action(project, {
            "id": "0.0.1/move-file",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin.txt",
            "to": ".ai/box/kept.txt",
        }))
        self.assertFalse((project / "origin.txt").exists())
        self.assertEqual(b"abc", (project / ".ai" / "box" / "kept.txt").read_bytes())
        self.assertEqual(0, self.apply_action(project, {
            "id": "0.0.1/move-file-again",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin.txt",
            "to": ".ai/box/kept.txt",
        }))
        self.assertEqual(b"abc", (project / ".ai" / "box" / "kept.txt").read_bytes())

        directory = self.deployed_project("move-dir")
        nested = directory / "origin" / "sub"
        nested.mkdir(parents=True)
        (nested / "a.txt").write_bytes(b"nested")
        (directory / "origin" / "b.txt").write_bytes(b"top")
        butler = self.action_fixture({
            "id": "0.0.1/move-dir",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        })
        plan = UPGRADE.build_plan(directory, butler, "defer")
        kinds = [change.operation for change in plan["_planned"]]
        self.assertEqual(kinds, sorted(kinds, key=lambda item: UPGRADE.OPERATION_RANK[item]))
        remove_paths = [
            change.path.relative_to(directory.resolve()).as_posix()
            for change in plan["_planned"] if change.operation == "remove-dir"
        ]
        self.assertEqual(remove_paths, sorted(remove_paths, key=lambda item: (-item.count("/"), item)))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(0, UPGRADE.main([
                "--butler-root", str(butler), "apply",
                "--project-root", str(directory), "--split", "defer",
            ]))
        self.assertFalse((directory / "origin").exists())
        self.assertEqual(b"nested", (directory / ".ai" / "origin" / "sub" / "a.txt").read_bytes())
        self.assertEqual(b"top", (directory / ".ai" / "origin" / "b.txt").read_bytes())

        both = self.deployed_project("move-both")
        (both / "origin").write_bytes(b"source")
        (both / ".ai" / "origin").write_bytes(b"dest")
        before = digest_tree(both)
        self.assertEqual(2, self.apply_action(both, {
            "id": "0.0.1/move-both",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        }))
        self.assertEqual(b"source", (both / "origin").read_bytes())
        self.assertEqual(b"dest", (both / ".ai" / "origin").read_bytes())
        self.assertEqual(before, digest_tree(both))

        neither = self.deployed_project("move-neither")
        before = digest_tree(neither)
        self.assertEqual(2, self.apply_action(neither, {
            "id": "0.0.1/move-neither",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        }))
        self.assertFalse((neither / "origin").exists())
        self.assertFalse((neither / ".ai" / "origin").exists())
        self.assertEqual(before, digest_tree(neither))

        done = self.deployed_project("move-done")
        (done / ".ai" / "origin").write_bytes(b"already")
        self.assertEqual(0, self.apply_action(done, {
            "id": "0.0.1/move-done",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        }))
        self.assertEqual(b"already", (done / ".ai" / "origin").read_bytes())
        self.assertFalse((done / "origin").exists())
        self.assertEqual(["origin"], [path.name for path in (done / ".ai").iterdir() if path.name == "origin"])

    def test_symlink_delete_and_move_are_refused(self):
        project = self.deployed_project("symlink-top")
        real = project / "real.txt"
        real.write_bytes(b"safe")
        (project / "origin").symlink_to(real)
        before = digest_tree(project)
        self.assertEqual(2, self.apply_action(project, {
            "id": "0.0.1/delete-link",
            "type": "delete",
            "domain": "project",
            "preconditions": ["delete-path-allowed"],
            "path": "origin",
        }))
        self.assertTrue((project / "origin").is_symlink())
        self.assertEqual(b"safe", real.read_bytes())
        self.assertEqual(before, digest_tree(project))

        nested = self.deployed_project("symlink-child")
        (nested / "origin").mkdir()
        (nested / "origin" / "keep.txt").write_bytes(b"keep")
        (nested / "origin" / "link").symlink_to(nested / "origin" / "keep.txt")
        before = digest_tree(nested)
        self.assertEqual(2, self.apply_action(nested, {
            "id": "0.0.1/move-link",
            "type": "move",
            "domain": "project",
            "preconditions": ["move-path-allowed"],
            "from": "origin",
            "to": ".ai/origin",
        }))
        self.assertTrue((nested / "origin" / "link").is_symlink())
        self.assertEqual(b"keep", (nested / "origin" / "keep.txt").read_bytes())
        self.assertFalse((nested / ".ai" / "origin").exists())
        self.assertEqual(before, digest_tree(nested))

    def test_directory_failure_restores_delete_and_move(self):
        cases = {
            "delete": {
                "id": "0.0.1/fail-delete",
                "type": "delete",
                "domain": "project",
                "preconditions": ["delete-path-allowed"],
                "path": "origin",
            },
            "move": {
                "id": "0.0.1/fail-move",
                "type": "move",
                "domain": "project",
                "preconditions": ["move-path-allowed"],
                "from": "origin",
                "to": ".ai/origin",
            },
        }
        for label, action in cases.items():
            with self.subTest(action=label):
                project = self.deployed_project(f"fail-{label}")
                nested = project / "origin" / "sub"
                nested.mkdir(parents=True)
                (nested / "a.txt").write_bytes(b"nested")
                (project / "origin" / "b.txt").write_bytes(b"top")
                butler = self.action_fixture(action)
                plan = UPGRADE.build_plan(project, butler, "defer")
                self.assertGreaterEqual(len(plan["_planned"]), 2)
                before = digest_tree(project, ignore_runtime=True)
                present = {
                    path.relative_to(project).as_posix(): path.read_bytes()
                    for path in project.rglob("*") if path.is_file() and not path.is_symlink()
                }
                dirs = {
                    path.relative_to(project).as_posix()
                    for path in project.rglob("*") if path.is_dir() and not path.is_symlink()
                }
                fail_at = len(plan["_planned"]) // 2
                with mock.patch.dict(os.environ, {"BUTLER_UPGRADE_FAIL_AFTER": str(fail_at)}):
                    with self.assertRaisesRegex(UPGRADE.UpgradeError, "all project files restored") as raised:
                        UPGRADE.apply_plan(plan, project)
                self.assertEqual(UPGRADE.EXIT_RESTORED, raised.exception.code)
                self.assertEqual(before, digest_tree(project, ignore_runtime=True))
                for rel, content in present.items():
                    self.assertEqual(content, (project / rel).read_bytes(), rel)
                for rel in dirs:
                    self.assertTrue((project / rel).is_dir(), rel)
                if label == "move":
                    self.assertFalse((project / ".ai" / "origin").exists())

    def v4_butler_root(self) -> Path:
        root = self.base / f"butler-v4-{len(list(self.base.iterdir()))}"
        shutil.copytree(ROOT / "migrations", root / "migrations")
        shutil.copytree(ROOT / "templates", root / "templates")
        (root / "scripts").mkdir()
        shutil.copy(
            ROOT / "scripts" / "render-project-entrypoints.py",
            root / "scripts" / "render-project-entrypoints.py",
        )
        config_dir = root / "tools" / "project-config"
        config_dir.mkdir(parents=True)
        shutil.copy(ROOT / "tools" / "project-config" / "config.py", config_dir / "config.py")
        (root / "VERSION").write_text("4.0.0\n")
        return root

    def apply_v4(self, project: Path, butler: Path) -> int:
        real_run = subprocess.run

        def guard(argv, *args, **kwargs):
            parts = argv if isinstance(argv, (list, tuple)) else [argv]
            if any("setup.sh" in str(part) for part in parts):
                raise AssertionError("setup.sh was invoked")
            return real_run(argv, *args, **kwargs)

        with mock.patch("subprocess.run", guard):
            with redirect_stdout(io.StringIO()):
                return UPGRADE.main([
                    "--butler-root", str(butler),
                    "apply",
                    "--project-root", str(project),
                ])

    def test_v4_recipe_cleans_a_temp_project_and_is_idempotent(self):
        butler = self.v4_butler_root()
        project = self.project("3.6.0", user="precious")
        self.assertFalse(butler in project.parents or project in butler.parents)
        nested = project / ".ai" / "project" / "notes"
        nested.mkdir(parents=True)
        (nested / "keep.txt").write_bytes(b"folder")
        (project / ".ai" / "PROJECT.md").write_text("# old\n")
        (project / "deliveries").mkdir()
        (project / "deliveries" / "note.txt").write_bytes(b"packet")
        (project / ".ai" / "butler.config.json").write_text(json.dumps({
            "schema_version": 1,
            "dangerous": True,
            "independent_review": False,
            "preference": True,
            "profiles": ["typescript-rules"],
        }, indent=2) + "\n")
        inbox = project / ".ai" / "INBOX.md"
        inbox.write_text("## 闪念\n\n| 闪念键 | 记于 | 一句话 | 状态 | 去向 |\n")
        inbox_bytes = inbox.read_bytes()

        plan = UPGRADE.build_plan(project, butler, None)
        self.assertTrue(all(action["id"].startswith("4.0.0/") for action in plan["actions"]))
        self.assertIn("4.0.0/01-global-install", plan["external_pending"])
        self.assertEqual(0, self.apply_v4(project, butler))
        self.assertFalse((project / ".ai" / "project").exists())
        self.assertFalse((project / ".ai" / "PROJECT.md").exists())
        self.assertFalse((project / "deliveries").exists())
        self.assertEqual(b"packet", (project / ".ai" / "deliveries" / "note.txt").read_bytes())
        for name in ("CLAUDE.md", "AGENTS.md"):
            text = (project / name).read_text()
            self.assertIn(f"precious-{name}", text)
            self.assertIn("butler v4.0.0", text)
        self.assertEqual(
            UPGRADE.tree_digest(UPGRADE.hook_source_files(butler)),
            UPGRADE.tree_digest(UPGRADE.target_hook_files(project)),
        )
        stored = json.loads((project / ".ai" / "butler.config.json").read_text())
        self.assertNotIn("preference", stored)
        self.assertTrue(stored["dangerous"])
        self.assertFalse(stored["independent_review"])
        self.assertEqual(["typescript-rules"], stored["profiles"])
        self.assertEqual(inbox_bytes, inbox.read_bytes())
        self.assertEqual(0, self.apply_v4(project, butler))
        self.assertEqual(b"packet", (project / ".ai" / "deliveries" / "note.txt").read_bytes())
        self.assertEqual(1, len(list((project / ".ai" / "deliveries").rglob("*"))))

    def test_legacy_inbox_or_origin_stops_before_any_write(self):
        butler = self.v4_butler_root()
        legacy = self.project("3.6.0")
        (legacy / ".ai" / "project").mkdir()
        (legacy / ".ai" / "project" / "a.txt").write_bytes(b"stay")
        (legacy / ".ai" / "PROJECT.md").write_text("stay\n")
        (legacy / "deliveries").mkdir()
        (legacy / "deliveries" / "a.txt").write_bytes(b"stay")
        inbox = legacy / ".ai" / "INBOX.md"
        inbox.write_bytes(b"<!-- butler-inbox:managed -->\n## Sources\n")
        before = digest_tree(legacy)
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "legacy inbox"):
            UPGRADE.build_plan(legacy, butler, None)
        self.assertEqual(before, digest_tree(legacy))

        origin_project = self.project("3.6.0")
        (origin_project / "origin").mkdir()
        (origin_project / "origin" / "mine.txt").write_bytes(b"mine")
        (origin_project / ".ai" / "PROJECT.md").write_text("stay\n")
        (origin_project / "deliveries").mkdir()
        (origin_project / "deliveries" / "a.txt").write_bytes(b"stay")
        before = digest_tree(origin_project)
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "origin is present"):
            UPGRADE.build_plan(origin_project, butler, None)
        self.assertEqual(before, digest_tree(origin_project))

        linked = self.project("3.6.0")
        outside = self.base / "outside-inbox"
        outside.write_bytes(b"secret")
        (linked / ".ai" / "INBOX.md").symlink_to(outside)
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "symlink"):
            UPGRADE.build_plan(linked, butler, None)
        self.assertEqual(b"secret", outside.read_bytes())

    def test_both_deliveries_stop_without_overwrite(self):
        butler = self.v4_butler_root()
        project = self.project("3.6.0")
        (project / "deliveries").mkdir()
        (project / "deliveries" / "src.txt").write_bytes(b"src")
        (project / ".ai" / "deliveries").mkdir()
        (project / ".ai" / "deliveries" / "dst.txt").write_bytes(b"dst")
        before = digest_tree(project)
        with self.assertRaisesRegex(UPGRADE.UpgradeError, "move conflict"):
            UPGRADE.build_plan(project, butler, None)
        self.assertEqual(before, digest_tree(project))
        self.assertEqual(b"src", (project / "deliveries" / "src.txt").read_bytes())
        self.assertEqual(b"dst", (project / ".ai" / "deliveries" / "dst.txt").read_bytes())

    def test_v4_chain_deletes_project_md_without_the_old_split_stop(self):
        butler = self.v4_butler_root()
        project = self.project("1.7.0")
        (project / ".ai" / "PROJECT.md").write_text("# Knowledge\nprivate prose\n")
        (project / ".ai" / "deliveries").mkdir()
        (project / ".ai" / "deliveries" / "kept.txt").write_bytes(b"kept")
        queued = UPGRADE.build_plan(project, butler, None)
        self.assertNotIn(queued["status"], {"needs-decision", "manual-split"})
        self.assertTrue(any(action["type"] == "split" for action in queued["actions"]))
        self.assertTrue(any(action["id"] == "4.0.0/03-delete-project-md" for action in queued["actions"]))
        self.assertEqual(0, self.apply_v4(project, butler))
        self.assertFalse((project / ".ai" / "PROJECT.md").exists())

    def test_retired_preference_docs_and_unpaid_debt_stay_honest(self):
        self.assertTrue((ROOT / "tools" / "preference-experiment").is_dir())
        self.assertTrue((ROOT / "templates" / "preference").is_dir())
        for path in ROOT.rglob("*.py"):
            if ".git" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            names = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            self.assertFalse(names & {"reorder_options", "reorder_by_profile"}, str(path))
        debt = (ROOT / ".ai" / "debt.md").read_text(encoding="utf-8")
        self.assertNotIn("还没有 `migrations/v4.0.0.md`", debt)
        self.assertNotIn("不会自动碰", debt)
        self.assertNotIn("也不会碰", debt)
        self.assertIn("仍要人自己处理", debt)
        self.assertIn("从未在真实已部署项目上跑过", debt)
        self.assertIn("这条账仍欠着", debt)

    def _historic_hook_digest(self, ref: str) -> str:
        """按 upgrade.py 当前口径复算某个 git ref 上的 templates/hooks 树摘要。"""
        listing = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", "-r", "-z", f"{ref}:templates/hooks"],
            capture_output=True, check=True,
        )
        files: dict[Path, bytes] = {}
        for entry in listing.stdout.split(b"\0"):
            if not entry:
                continue
            meta, path = entry.split(b"\t", 1)
            mode, _kind, oid = meta.split(b" ")
            if mode == b"120000":
                continue
            rel = Path(path.decode())
            if UPGRADE.skip_hook_file(rel):
                continue
            blob = subprocess.run(
                ["git", "-C", str(ROOT), "cat-file", "blob", oid.decode()],
                capture_output=True, check=True,
            )
            files[rel] = blob.stdout
        return UPGRADE.tree_digest(files)


if __name__ == "__main__":
    unittest.main()
