#!/usr/bin/env python3
"""Verify pinned Codex validator integrity and run them in an empty HOME."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATORS = ROOT / "tools" / "codex-validators"
PROVENANCE = VALIDATORS / "PROVENANCE.json"
PLUGIN = ROOT / "plugins" / "butler"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_and_verify_provenance(root: Path = VALIDATORS) -> dict[str, object]:
    provenance_path = root / "PROVENANCE.json"
    payload = json.loads(provenance_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported provenance schema")
    source = payload.get("source")
    if not isinstance(source, dict) or source.get("repository") != "https://github.com/openai/codex":
        raise ValueError("unexpected validator source")
    commit = source.get("commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise ValueError("source commit must be a full SHA")
    entries = payload.get("files")
    if not isinstance(entries, list) or len(entries) != 2:
        raise ValueError("provenance must list exactly two validators")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("invalid provenance file entry")
        relative = entry.get("path")
        expected = entry.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError("provenance path/hash must be strings")
        path = (root / relative).resolve()
        if root.resolve() not in path.parents or not path.is_file():
            raise ValueError(f"missing or unsafe validator path: {relative}")
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"validator hash mismatch: {relative}: {actual}")
    license_path = root / "LICENSE"
    if not license_path.is_file() or "Apache License" not in license_path.read_text(encoding="utf-8"):
        raise ValueError("missing upstream Apache license")
    return payload


def run(command: list[str], home: Path) -> subprocess.CompletedProcess[str]:
    env = {"HOME": str(home), "PATH": os.environ.get("PATH", "")}
    return subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)


class VendoredValidatorTests(unittest.TestCase):
    def test_integrity_and_empty_home_validation(self) -> None:
        load_and_verify_provenance()
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp) / "empty-home"
            home.mkdir()
            plugin_validator = VALIDATORS / "plugin-creator" / "validate_plugin.py"
            result = run([sys.executable, str(plugin_validator), str(PLUGIN)], home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            skill_validator = VALIDATORS / "skill-creator" / "quick_validate.py"
            skills = sorted((PLUGIN / "skills").iterdir())
            self.assertEqual(len(skills), 13)
            for skill in skills:
                result = run([sys.executable, str(skill_validator), str(skill)], home)
                self.assertEqual(result.returncode, 0, f"{skill.name}: {result.stdout}{result.stderr}")

    def test_modified_or_missing_snapshot_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "validators"
            shutil.copytree(VALIDATORS, copy)
            target = copy / "skill-creator" / "quick_validate.py"
            target.write_text(target.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_and_verify_provenance(copy)
            target.unlink()
            with self.assertRaisesRegex(ValueError, "missing or unsafe"):
                load_and_verify_provenance(copy)

    def test_bad_plugin_and_skill_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            bad_plugin = temp_root / "butler"
            shutil.copytree(PLUGIN, bad_plugin, symlinks=True)
            manifest = bad_plugin / ".codex-plugin" / "plugin.json"
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["version"] = "floating"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            home = temp_root / "home"
            home.mkdir()
            result = run(
                [sys.executable, str(VALIDATORS / "plugin-creator" / "validate_plugin.py"), str(bad_plugin)],
                home,
            )
            self.assertNotEqual(result.returncode, 0)

            bad_skill = bad_plugin / "skills" / "butler-prd"
            skill_md = bad_skill / "SKILL.md"
            skill_md.write_text(skill_md.read_text(encoding="utf-8").replace("name: butler-prd", "name: Butler PRD", 1), encoding="utf-8")
            result = run(
                [sys.executable, str(VALIDATORS / "skill-creator" / "quick_validate.py"), str(bad_skill)],
                home,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
