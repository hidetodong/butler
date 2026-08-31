#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
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
        if f"v{released}" in available:
            self.assertEqual(
                self._historic_hook_digest(f"v{released}"),
                current,
                "工作区 templates/hooks 与已发布 tag 不一致，白名单对账结论不可信",
            )

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
