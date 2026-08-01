#!/usr/bin/env python3
"""Regression tests for the Butler workflow registry synchronizer."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts/sync-workflow-registry.py"
SPEC = importlib.util.spec_from_file_location("workflow_registry", MODULE_PATH)
assert SPEC and SPEC.loader
registry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = registry
SPEC.loader.exec_module(registry)


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(relative)
        if path.is_symlink():
            digest.update(b"L" + os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
    return digest.hexdigest()


class WorkflowRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="butler-workflows-")
        self.root = Path(self.temp.name)
        data = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
        copy_paths = {
            "workflows/registry.json", "README.md", "HUMAN_GUIDE.md", "Coder/README.md",
            "workflows/router-examples.json",
            "docs/codex-compatibility.md", "docs/workflows.md", "scripts/setup.sh",
            "scripts/install-codex-plugin.sh", "plugins/butler/.codex-plugin/plugin.json",
            "plugins/butler/hooks/hooks.json",
        }
        router = data["router"]
        copy_paths.update({router["rule_source"], router["claude"]["path"], router["codex"]["path"]})
        copy_paths.add(str(Path(router["codex"]["path"]).parent / "agents/openai.yaml"))
        for item in data["workflows"]:
            copy_paths.update({item["rule_source"], item["claude"]["path"], item["codex"]["path"]})
            copy_paths.add(str(Path(item["codex"]["path"]).parent / "agents/openai.yaml"))
        for name in ("butler-gate.sh", "butler-advisor.sh"):
            copy_paths.add(f"plugins/butler/hooks/{name}")
        for relative in copy_paths:
            source = ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        for item in [router, *data["workflows"]]:
            name = item["codex"]["name"].removeprefix("$")
            link = self.root / ".agents/skills" / name
            link.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(f"../../plugins/butler/skills/{name}", link)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def read(self) -> dict:
        return json.loads((self.root / "workflows/registry.json").read_text(encoding="utf-8"))

    def test_registry_is_exact_and_high_risk_is_explicit_only(self) -> None:
        data = registry.read_registry(self.root)
        self.assertEqual(2, data["schema_version"])
        self.assertEqual("/butler", data["router"]["claude"]["name"])
        self.assertEqual("$butler-router", data["router"]["codex"]["name"])
        self.assertEqual(registry.EXPECTED_IDS, {item["id"] for item in data["workflows"]})
        policies = {item["id"]: item["allow_implicit_invocation"] for item in data["workflows"]}
        self.assertFalse(policies["loop"])
        self.assertFalse(policies["dangerous"])
        self.assertTrue(all(policies[name] for name in registry.EXPECTED_IDS - registry.HIGH_RISK))

    def test_routing_metadata_rejects_unknown_asymmetric_self_and_cycles(self) -> None:
        cases = []
        unknown = self.read(); unknown["workflows"][0]["routing"]["prerequisites"] = ["ghost"]; cases.append(unknown)
        asymmetric = self.read(); asymmetric["workflows"][0]["routing"]["conflicts_with"] = ["prd"]; cases.append(asymmetric)
        self_route = self.read(); self_route["workflows"][0]["routing"]["prerequisites"] = ["inbox"]; cases.append(self_route)
        cycle = self.read()
        cycle["workflows"][0]["routing"]["prerequisites"] = ["prd"]
        cycle["workflows"][1]["routing"]["prerequisites"] = ["inbox"]
        cases.append(cycle)
        for case in cases:
            with self.assertRaises(registry.RegistryError):
                registry.validate_registry(case, self.root)

    def test_shared_router_examples_cover_all_workflows_and_statuses(self) -> None:
        data = registry.read_registry(self.root)
        examples = json.loads((self.root / "workflows/router-examples.json").read_text())["examples"]
        self.assertEqual(registry.EXPECTED_IDS, {item["expected_primary"] for item in examples if item["expected_primary"]})
        self.assertEqual(set(data["router"]["statuses"]), {item["expected_status"] for item in examples})

    def test_setup_is_a_thin_machine_install_router(self) -> None:
        data = registry.read_registry(self.root)
        setup = next(item for item in data["workflows"] if item["id"] == "setup")
        self.assertEqual("Coder/20_Workflow_Lifecycle/butler-setup.md", setup["rule_source"])
        command = (self.root / setup["claude"]["path"]).read_text(encoding="utf-8")
        skill = (self.root / setup["codex"]["path"]).read_text(encoding="utf-8")
        contract = (self.root / setup["rule_source"]).read_text(encoding="utf-8")
        for text in (command, skill, contract):
            self.assertIn("scripts/setup.sh", text)
        self.assertIn("显式", contract)
        self.assertIn("不初始化当前项目", contract)
        self.assertNotIn("configure-global-install.py", command)
        self.assertNotIn("install-codex-plugin.sh", skill)

    def test_write_is_idempotent_and_check_is_zero_write(self) -> None:
        data = registry.read_registry(self.root)
        projections = registry.build_projections(data, self.root)
        command = self.root / ".claude/commands/butler/prd.md"
        command.write_text(command.read_text(encoding="utf-8").replace("description:", "description: stale ", 1), encoding="utf-8")
        self.assertEqual(0, registry.main(["--write", "--root", str(self.root)]))
        after_write = digest_tree(self.root)
        self.assertEqual(0, registry.main(["--write", "--root", str(self.root)]))
        self.assertEqual(after_write, digest_tree(self.root))
        self.assertEqual(0, registry.main(["--check", "--root", str(self.root)]))
        self.assertEqual(after_write, digest_tree(self.root))
        self.assertTrue(all(registry.projection_drift(item) is None for item in projections))

    def test_frontmatter_projection_preserves_workflow_bodies(self) -> None:
        command = self.root / ".claude/commands/butler/review.md"
        skill = self.root / "plugins/butler/skills/butler-review/SKILL.md"
        command.write_text(command.read_text(encoding="utf-8") + "\nregistry-body-sentinel\n", encoding="utf-8")
        skill.write_text(skill.read_text(encoding="utf-8") + "\nregistry-skill-sentinel\n", encoding="utf-8")
        self.assertEqual(0, registry.main(["--write", "--root", str(self.root)]))
        self.assertTrue(command.read_text(encoding="utf-8").endswith("registry-body-sentinel\n"))
        self.assertTrue(skill.read_text(encoding="utf-8").endswith("registry-skill-sentinel\n"))

    def test_check_detects_file_and_symlink_drift_without_writing(self) -> None:
        yaml = self.root / "plugins/butler/skills/butler-loop/agents/openai.yaml"
        yaml.write_text(yaml.read_text(encoding="utf-8").replace("false", "true"), encoding="utf-8")
        link = self.root / ".agents/skills/butler-prd"
        link.unlink()
        os.symlink("/tmp/not-butler", link)
        before = digest_tree(self.root)
        self.assertEqual(1, registry.main(["--check", "--root", str(self.root)]))
        self.assertEqual(before, digest_tree(self.root))

    def test_managed_projection_drift_matrix(self) -> None:
        data = registry.read_registry(self.root)
        projections = {item.path.relative_to(self.root).as_posix(): item for item in registry.build_projections(data, self.root)}
        file_cases = {
            ".claude/commands/butler/prd.md": lambda text: text.replace("description:", "description: stale ", 1),
            "plugins/butler/skills/butler-prd/SKILL.md": lambda text: text.replace("name: butler-prd", "name: stale-prd", 1),
            "plugins/butler/skills/butler-prd/agents/openai.yaml": lambda text: text.replace("allow_implicit_invocation: true", "allow_implicit_invocation: false"),
            "docs/workflows.md": lambda text: text + "\nstale\n",
        }
        for relative, mutate in file_cases.items():
            path = self.root / relative
            original = path.read_text(encoding="utf-8")
            path.write_text(mutate(original), encoding="utf-8")
            self.assertIsNotNone(registry.projection_drift(projections[relative]), relative)
            path.write_text(original, encoding="utf-8")
        link = self.root / ".agents/skills/butler-prd"
        expected = projections[".agents/skills/butler-prd"]
        link.unlink(); os.symlink("../../plugins/butler/skills/missing", link)
        self.assertIsNotNone(registry.projection_drift(expected))
        link.unlink(); os.symlink("/tmp/absolute", link)
        self.assertIsNotNone(registry.projection_drift(expected))
        link.unlink(); link.mkdir()
        self.assertIsNotNone(registry.projection_drift(expected))

    def test_schema_rejects_missing_extra_duplicate_unsafe_and_policy_drift(self) -> None:
        labelled_cases: list[tuple[str, dict]] = []
        missing = self.read(); missing["workflows"].pop(); labelled_cases.append(("missing", missing))
        extra = self.read(); extra["workflows"].append(extra["workflows"][0].copy()); labelled_cases.append(("extra", extra))
        duplicate = self.read(); duplicate["workflows"][1]["id"] = duplicate["workflows"][0]["id"]; labelled_cases.append(("duplicate", duplicate))
        unsafe = self.read(); unsafe["workflows"][0]["rule_source"] = "../escape.md"; labelled_cases.append(("unsafe", unsafe))
        high = self.read()
        for w in high["workflows"]:
            if w["id"] == "dangerous":
                w["allow_implicit_invocation"] = True
                break
        labelled_cases.append(("high_risk_implicit", high))
        normal = self.read(); normal["workflows"][0]["allow_implicit_invocation"] = False; labelled_cases.append(("normal_explicit_false", normal))
        unknown = self.read(); unknown["unexpected"] = True; labelled_cases.append(("unknown_key", unknown))
        for label, case in labelled_cases:
            with self.subTest(case=label):
                with self.assertRaises(registry.RegistryError):
                    registry.validate_registry(case, self.root)

    def test_repository_sets_and_plugin_contract_are_closed(self) -> None:
        data = self.read()
        extra = self.root / ".agents/skills/butler-ghost"
        os.symlink("../../plugins/butler/skills/butler-prd", extra)
        with self.assertRaisesRegex(registry.RegistryError, "discovery set drift"):
            registry.validate_registry(data, self.root)
        extra.unlink()
        hooks_path = self.root / "plugins/butler/hooks/hooks.json"
        hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
        hooks["hooks"]["PreToolUse"][0]["matcher"] = "Write"
        hooks_path.write_text(json.dumps(hooks), encoding="utf-8")
        with self.assertRaisesRegex(registry.RegistryError, "hook matcher drift"):
            registry.validate_registry(data, self.root)
        shutil.copy2(ROOT / "plugins/butler/hooks/hooks.json", hooks_path)
        manifest_path = self.root / "plugins/butler/.codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["name"] = "not-butler"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(registry.RegistryError, "manifest name/skills"):
            registry.validate_registry(data, self.root)
        shutil.copy2(ROOT / "plugins/butler/.codex-plugin/plugin.json", manifest_path)
        wrapper = self.root / "plugins/butler/hooks/butler-gate.sh"
        wrapper.chmod(0o644)
        with self.assertRaisesRegex(registry.RegistryError, "not executable"):
            registry.validate_registry(data, self.root)
        wrapper.chmod(0o755)
        installer = self.root / "scripts/install-codex-plugin.sh"
        installer.write_text(installer.read_text(encoding="utf-8").replace("marketplace.json", "marketplace-disabled"), encoding="utf-8")
        with self.assertRaisesRegex(registry.RegistryError, "installer contract"):
            registry.validate_registry(data, self.root)
        shutil.copy2(ROOT / "scripts/install-codex-plugin.sh", installer)
        distribution = self.read()
        distribution["plugin"]["team_distribution"] = "available"
        with self.assertRaisesRegex(registry.RegistryError, "supported boundary"):
            registry.validate_registry(distribution, self.root)
        legacy = self.root / ".claude/commands/loop.md"
        legacy.write_text("forbidden\n", encoding="utf-8")
        with self.assertRaisesRegex(registry.RegistryError, "legacy aliases"):
            registry.validate_registry(data, self.root)

    def test_failed_write_rolls_back_applied_files(self) -> None:
        data = registry.read_registry(self.root)
        docs = self.root / "docs/workflows.md"
        yaml = self.root / "plugins/butler/skills/butler-prd/agents/openai.yaml"
        docs.write_text("stale docs\n", encoding="utf-8")
        yaml.write_text("stale yaml\n", encoding="utf-8")
        before = digest_tree(self.root)
        real_atomic = registry.atomic_write
        calls = 0

        def fail_once(path: Path, content: bytes, mode: int) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected failure")
            real_atomic(path, content, mode)

        with mock.patch.object(registry, "atomic_write", side_effect=fail_once):
            with self.assertRaises(OSError):
                registry.apply_projections(registry.build_projections(data, self.root))
        self.assertEqual(before, digest_tree(self.root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
