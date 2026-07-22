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
CLI = REPO / "tools/workspace-scope/workspace_scope.py"
PRD_A = "2026-07-22-alpha"
PRD_B = "2026-07-23-beta"


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode())
        if path.is_symlink():
            digest.update(b"L" + os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
        else:
            digest.update(b"D")
    return digest.hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def map_text(*, overlap: bool = False) -> str:
    extra = "| tooling/generated/** | @acme/api | generated | bad |\n" if overlap else ""
    return """# Workspaces

| workspace_key | package_identity | path | kind | status | evidence |
|---|---|---|---|---|---|
| @acme/web | @acme/web | apps/web | app | active | apps/web/package.json:name |
| @acme/ui | @acme/ui | packages/ui | library | active | packages/ui/package.json:name |
| @acme/api | @acme/api | packages/api | library | active | packages/api/package.json:name |
| @acme/admin | @acme/admin | apps/admin | app | active | apps/admin/package.json:name |
| old | — | retired/old | other | retired | retired-by-user |

## Path Ownership

| path_pattern | workspace_key | path_kind | evidence |
|---|---|---|---|
| package-lock.json | @acme/web | generated | npm-root-lock |
| tooling/** | @acme/ui | shared | explicit-owner |
""" + extra


def requirement_index(prd_id: str, version: str, *, web_category: str = "primary_write", module_scope: bool = False) -> str:
    scope = {
        "primary_write": ["@acme/web"] if web_category == "primary_write" else [],
        "supporting_write": ["@acme/ui"] if web_category != "supporting_write" else ["@acme/web", "@acme/ui"],
        "read_only": ["@acme/api"] if web_category != "read_only" else ["@acme/web", "@acme/api"],
        "excluded": ["@acme/admin"] if web_category != "excluded" else ["@acme/web", "@acme/admin"],
    }
    module = """
## Module Workspace Scope

| module_slug | primary_write | supporting_write | read_only | excluded |
|---|---|---|---|---|
| flow | [@acme/web] | [] | [@acme/ui, @acme/api] | [@acme/admin] |
""" if module_scope else ""
    return f"""# {prd_id}

## Requirement Identity

- prd_id: {prd_id}
- current_version: {version}
- status: active

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
| flow | Flow | v1.0 | {version} | active |

## Workspace Scope

- primary_write: [{', '.join(scope['primary_write'])}]
- supporting_write: [{', '.join(scope['supporting_write'])}]
- read_only: [{', '.join(scope['read_only'])}]
- excluded: [{', '.join(scope['excluded'])}]
{module}"""


def ac_text(refs: list[tuple[str, str, list[str]]]) -> str:
    rows = "\n".join(
        f"  - prd_id: {prd_id}\n    prd_version: {version}\n    module_slugs: [{', '.join(modules)}]"
        for prd_id, version, modules in refs
    )
    return f"""---
状态: ack-frozen
prd_refs:
{rows}
---
# AC
"""


def plan_text(*, web_pattern: str = "apps/web/**", include_ui: bool = False, access: str = "primary_write") -> str:
    ui = "| @acme/ui | supporting_write | [packages/ui/**, tooling/**] | shared UI |\n" if include_ui else ""
    return f"""---
方案状态: pass
---
# Workspace Write Plan

| workspace_key | access | path_patterns | rationale |
|---|---|---|---|
| @acme/web | {access} | [{web_pattern}, package-lock.json] | primary implementation |
{ui}"""


def make_project(base: Path) -> Path:
    root = base / "project"
    for relative, name in (
        ("apps/web", "@acme/web"), ("packages/ui", "@acme/ui"),
        ("packages/api", "@acme/api"), ("apps/admin", "@acme/admin"),
    ):
        write_json(root / relative / "package.json", {"name": name})
    write_json(root / "package.json", {"name": "root", "private": True, "workspaces": ["apps/*", "packages/*"]})
    (root / "package-lock.json").write_text("{}\n", encoding="utf-8")
    (root / "tooling").mkdir()
    project = root / ".ai/project"
    project.mkdir(parents=True)
    (project / "workspaces.md").write_text(map_text(), encoding="utf-8")
    prd_root = root / ".ai/references/prd"
    target = prd_root / PRD_A
    archive = target / ".archive/v1.0"
    target.mkdir(parents=True)
    archive.mkdir(parents=True)
    (target / "00_INDEX.md").write_text(requirement_index(PRD_A, "v1.1"), encoding="utf-8")
    (archive / "00_INDEX.md").write_text(requirement_index(PRD_A, "v1.0", module_scope=True), encoding="utf-8")
    (root / ".ai/AC_LIST.md").write_text(ac_text([(PRD_A, "v1.0", ["flow"])]), encoding="utf-8")
    (root / ".ai/TECH_PLAN.md").write_text(plan_text(include_ui=False), encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Fixture"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)
    return root


class WorkspaceScopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = make_project(Path(self.temp.name))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, action: str, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(CLI), action, "--project-root", str(self.root), *args],
            text=True, capture_output=True, check=False,
        )
        return result, json.loads(result.stdout)

    def test_discover_npm_array_and_object_is_zero_write(self) -> None:
        (self.root / "apps" / ".claude").mkdir()
        (self.root / "apps" / "prototype-without-manifest").mkdir()
        before = tree_hash(self.root)
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["discovery"]["layout"], "monorepo")
        self.assertEqual({item["workspace_key"] for item in payload["discovery"]["candidates"]}, {"@acme/web", "@acme/admin", "@acme/ui", "@acme/api"})
        self.assertEqual(before, tree_hash(self.root))
        package = json.loads((self.root / "package.json").read_text())
        package["workspaces"] = {"packages": package["workspaces"]}
        write_json(self.root / "package.json", package)
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(len(payload["discovery"]["candidates"]), 4)

    def test_discover_pnpm_and_single_package(self) -> None:
        (self.root / "package.json").write_text(json.dumps({"name": "root"}), encoding="utf-8")
        (self.root / "pnpm-workspace.yaml").write_text("packages:\n  - 'apps/*'\n  - 'packages/*'\n", encoding="utf-8")
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["discovery"]["patterns"], ["apps/*", "packages/*"])
        (self.root / "pnpm-workspace.yaml").unlink()
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["discovery"]["candidates"][0]["workspace_key"], "root")

    def test_discover_rejects_unsafe_duplicate_and_symlink(self) -> None:
        package = json.loads((self.root / "package.json").read_text())
        package["workspaces"] = ["../outside/*"]
        write_json(self.root / "package.json", package)
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsafe", payload["error"])
        package["workspaces"] = ["apps/*", "packages/*"]
        write_json(self.root / "package.json", package)
        write_json(self.root / "apps/admin/package.json", {"name": "@acme/web"})
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate package identity", payload["error"])
        write_json(self.root / "apps/admin/package.json", {"name": "@acme/admin"})
        target = self.root / "symlink-target"
        target.mkdir()
        (self.root / "apps/link-without-manifest").symlink_to(target, target_is_directory=True)
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", payload["error"])
        (self.root / "apps/link-without-manifest").unlink()
        package["workspaces"] = ["apps/missing-exact", "packages/*"]
        write_json(self.root / "package.json", package)
        result, payload = self.run_cli("discover")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no package.json", payload["error"])

    def test_validate_map_and_ownership_fail_closed(self) -> None:
        result, payload = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["workspace_count"], 5)
        path = self.root / ".ai/project/workspaces.md"
        path.write_text(map_text(overlap=True), encoding="utf-8")
        result, payload = self.run_cli("validate")
        self.assertEqual(result.returncode, 2)
        self.assertIn("overlap", payload["error"])

    def test_check_plan_uses_archived_pinned_scope_and_module_narrowing(self) -> None:
        before = tree_hash(self.root)
        result, payload = self.run_cli("check-plan")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload["effective_scope"]["sources"][0]["index"], f".ai/references/prd/{PRD_A}/.archive/v1.0/00_INDEX.md")
        self.assertEqual(payload["effective_scope"]["categories"]["supporting_write"], [])
        self.assertEqual(before, tree_hash(self.root))

    def test_check_paths_allows_plan_and_denies_scope_or_plan_escape(self) -> None:
        result, payload = self.run_cli("check-paths", "--path", "apps/web/src/main.ts", "--path", "package-lock.json")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual({item["workspace_key"] for item in payload["results"]}, {"@acme/web"})
        result, payload = self.run_cli("check-paths", "--path", "packages/api/client.ts")
        self.assertEqual(result.returncode, 2)
        self.assertIn("write denied", payload["error"])
        result, payload = self.run_cli("check-paths", "--path", "apps/web-test/file.ts")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no workspace owner", payload["error"])

    def test_missing_refs_is_controlled_na_but_legacy_is_rejected(self) -> None:
        (self.root / ".ai/AC_LIST.md").write_text("状态: ack-frozen\n", encoding="utf-8")
        result, payload = self.run_cli("check-paths", "--path", "apps/admin/x.ts")
        self.assertEqual(result.returncode, 0)
        self.assertFalse(payload["applicable"])
        (self.root / ".ai/AC_LIST.md").write_text("---\nprd_version: v1.0\n---\n", encoding="utf-8")
        result, payload = self.run_cli("check-plan")
        self.assertEqual(result.returncode, 2)
        self.assertIn("legacy", payload["error"])

    def test_cross_prd_explicit_permission_conflict_is_rejected(self) -> None:
        beta = self.root / ".ai/references/prd" / PRD_B
        beta.mkdir()
        beta_text = requirement_index(PRD_B, "v1.0", web_category="read_only")
        beta_text = beta_text.replace("- primary_write: []", "- primary_write: [@acme/admin]").replace("- excluded: [@acme/admin]", "- excluded: []")
        (beta / "00_INDEX.md").write_text(beta_text, encoding="utf-8")
        (self.root / ".ai/AC_LIST.md").write_text(ac_text([(PRD_A, "v1.0", ["flow"]), (PRD_B, "v1.0", ["flow"])]), encoding="utf-8")
        result, payload = self.run_cli("check-plan")
        self.assertEqual(result.returncode, 2)
        self.assertIn("permission conflict", payload["error"])

    def test_bad_plan_access_and_owner_are_rejected(self) -> None:
        (self.root / ".ai/TECH_PLAN.md").write_text(plan_text(access="supporting_write"), encoding="utf-8")
        result, payload = self.run_cli("check-plan")
        self.assertEqual(result.returncode, 2)
        self.assertIn("disagrees", payload["error"])
        (self.root / ".ai/TECH_PLAN.md").write_text(plan_text(web_pattern="packages/ui/**"), encoding="utf-8")
        result, payload = self.run_cli("check-plan")
        self.assertEqual(result.returncode, 2)
        self.assertIn("owned by", payload["error"])

    def test_check_diff_covers_rename_delete_and_untracked(self) -> None:
        source = self.root / "apps/web/old.ts"
        source.write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "old"], check=True)
        source.rename(self.root / "apps/web/new.ts")
        (self.root / "apps/web/untracked.ts").write_text("new\n", encoding="utf-8")
        result, payload = self.run_cli("check-diff", "--base", "HEAD", "--include-untracked")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(set(payload["paths"]), {"apps/web/old.ts", "apps/web/new.ts", "apps/web/untracked.ts"})
        (self.root / "apps/admin/out.ts").write_text("bad\n", encoding="utf-8")
        result, payload = self.run_cli("check-diff", "--base", "HEAD", "--include-untracked")
        self.assertEqual(result.returncode, 2)
        self.assertIn("write denied", payload["error"])


if __name__ == "__main__":
    unittest.main()
