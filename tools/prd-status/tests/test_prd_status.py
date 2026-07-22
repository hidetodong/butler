from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
CLI = REPO / "tools" / "prd-status" / "prd_status.py"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix().encode()
        digest.update(rel)
        if path.is_symlink():
            digest.update(b"L" + os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
        else:
            digest.update(b"D")
    return digest.hexdigest()


def requirement_index(prd_id: str, version: str, workspace: str) -> str:
    return f"""# Requirement

## Requirement Identity

- prd_id: {prd_id}
- current_version: {version}
- status: active

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
| shared-flow | Shared flow | {version} | {version} | active |

## Workspace Scope

- primary_write: [{workspace}]
- supporting_write: []
- read_only: [contracts]
- excluded: [admin]
"""


class PrdStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.prd = self.root / ".ai" / "references" / "prd"
        self.prd.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(CLI), "status", "--project-root", str(self.root), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        return result, json.loads(result.stdout)

    def make_collection(self) -> None:
        project = self.root / ".ai" / "project"
        project.mkdir(parents=True, exist_ok=True)
        (project / "workspaces.md").write_text(
            "# Workspaces\n\n| workspace_key | package_identity | path | kind | status | evidence |\n|---|---|---|---|---|---|\n"
            "| web | web | apps/web | app | active | package.json:name |\n"
            "| api | api | services/api | service | active | package.json:name |\n"
            "| contracts | contracts | packages/contracts | library | active | package.json:name |\n"
            "| admin | admin | apps/admin | app | active | package.json:name |\n",
            encoding="utf-8",
        )
        ids = [("2026-07-22-alpha", "Alpha", "v1.0", "web"), ("2026-07-23-beta", "Beta", "v2.1", "api")]
        rows = []
        for prd_id, title, version, workspace in ids:
            directory = self.prd / prd_id
            directory.mkdir()
            (directory / "00_INDEX.md").write_text(requirement_index(prd_id, version, workspace), encoding="utf-8")
            (directory / "shared-flow.md").write_text(f"exact {title}\n", encoding="utf-8")
            rows.append(f"| {prd_id} | {title} | {version} | active | SRC-{title} | {prd_id}/00_INDEX.md |")
        (self.prd / "00_INDEX.md").write_text(
            "# PRD Collection\n\n| prd_id | 标题 | 当前版本 | 状态 | 来源线索 | 入口 |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
            encoding="utf-8",
        )

    def test_lists_multiple_prds_and_keeps_same_module_slugs_independent(self) -> None:
        self.make_collection()
        before = tree_hash(self.root)
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual([item["prd_id"] for item in payload["requirements"]], ["2026-07-22-alpha", "2026-07-23-beta"])
        self.assertEqual([item["modules"][0]["module_slug"] for item in payload["requirements"]], ["shared-flow", "shared-flow"])
        self.assertEqual(before, tree_hash(self.root))

    def test_prd_id_detail_filter(self) -> None:
        self.make_collection()
        result, payload = self.run_cli("--prd-id", "2026-07-23-beta")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(payload["requirements"]), 1)
        self.assertEqual(payload["requirements"][0]["current_version"], "v2.1")

    def test_workspace_filter_and_match_category(self) -> None:
        self.make_collection()
        result, payload = self.run_cli("--workspace", "web")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["requirements"][0]["prd_id"], "2026-07-22-alpha")
        self.assertEqual(payload["requirements"][0]["workspace_matches"], ["primary_write"])

    def test_valid_filter_without_match_is_exit_one_and_read_only(self) -> None:
        self.make_collection()
        before = tree_hash(self.root)
        result, payload = self.run_cli("--workspace", "missing")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["requirements"], [])
        self.assertEqual(before, tree_hash(self.root))

    def test_legacy_is_readable_without_inventing_identity(self) -> None:
        (self.prd / "00_INDEX.md").write_text("# Legacy\n\n当前版本: v1.4\n", encoding="utf-8")
        (self.prd / "login.md").write_text("verbatim\n", encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 0)
        item = payload["requirements"][0]
        self.assertEqual(payload["layout"], "legacy")
        self.assertIsNone(item["prd_id"])
        self.assertTrue(item["migration_required"])

    def test_legacy_rejects_prd_id_lookup(self) -> None:
        (self.prd / "00_INDEX.md").write_text("当前版本: v1.0\n", encoding="utf-8")
        (self.prd / "one.md").write_text("one\n", encoding="utf-8")
        result, payload = self.run_cli("--prd-id", "2026-07-22-alpha")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no explicit prd_id", payload["error"])

    def test_rejects_mixed_collection_and_root_module(self) -> None:
        self.make_collection()
        (self.prd / "legacy.md").write_text("legacy\n", encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("mixed", payload["error"])

    def test_rejects_unindexed_requirement_directory(self) -> None:
        self.make_collection()
        extra = self.prd / "2026-07-24-ghost"
        extra.mkdir()
        (extra / "00_INDEX.md").write_text("ghost\n", encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("mismatch", payload["error"])

    def test_rejects_duplicate_prd_id(self) -> None:
        self.make_collection()
        index = self.prd / "00_INDEX.md"
        content = index.read_text(encoding="utf-8")
        duplicate = next(line for line in content.splitlines() if line.startswith("| 2026-07-22-alpha"))
        index.write_text(content + duplicate + "\n", encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate prd_id", payload["error"])

    @unittest.skipIf(os.name == "nt", "symlink semantics differ on Windows")
    def test_rejects_symlink_anywhere_in_prd_tree(self) -> None:
        self.make_collection()
        os.symlink(self.prd / "2026-07-22-alpha" / "shared-flow.md", self.prd / "2026-07-22-alpha" / "alias.md")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", payload["error"])

    def test_rejects_index_identity_drift_and_invalid_date(self) -> None:
        self.make_collection()
        child = self.prd / "2026-07-22-alpha" / "00_INDEX.md"
        child.write_text(child.read_text(encoding="utf-8").replace("current_version: v1.0", "current_version: v9.0"), encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("mismatch", payload["error"])

    def test_rejects_scope_key_missing_or_retired_in_project_map(self) -> None:
        self.make_collection()
        workspaces = self.root / ".ai" / "project" / "workspaces.md"
        workspaces.write_text(workspaces.read_text(encoding="utf-8").replace("| web | web | apps/web | app | active |", "| web | web | apps/web | app | retired |"), encoding="utf-8")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("not active", payload["error"])

    def test_invalid_cli_arguments_still_return_stable_json(self) -> None:
        result = subprocess.run([sys.executable, str(CLI), "status", "--unknown"], text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertIn("invalid arguments", payload["error"])

    @unittest.skipIf(os.name == "nt", "symlink semantics differ on Windows")
    def test_rejects_symlinked_project_state_ancestor(self) -> None:
        external = self.root / "external"
        external.mkdir()
        self.prd.rmdir()
        self.prd.parent.rmdir()
        (self.root / ".ai").rmdir()
        os.symlink(external, self.root / ".ai")
        result, payload = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", payload["error"])


if __name__ == "__main__":
    unittest.main()
