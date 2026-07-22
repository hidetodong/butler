from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
INBOX = REPO / "tools/inbox/inbox.py"
MIGRATE = REPO / "tools/prd-migrate/prd_migrate.py"
STATUS = REPO / "tools/prd-status/prd_status.py"
UPDATE = REPO / "tools/prd-update/prd_update.py"
SCOPE = REPO / "tools/workspace-scope/workspace_scope.py"
PRD_A = "2026-07-22-login"
PRD_B = "2026-07-23-admin-login"


def run_json(tool: Path, *args: str, expected: int = 0) -> dict:
    result = subprocess.run([sys.executable, str(tool), *args], text=True, capture_output=True, check=False)
    if result.returncode != expected:
        raise AssertionError(f"{tool.name} exit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
    return json.loads(result.stdout)


def scope_block() -> str:
    return """
## Workspace Scope

- primary_write: [@acme/web]
- supporting_write: [@acme/ui]
- read_only: [@acme/api]
- excluded: []
"""


class Mile0009E2E(unittest.TestCase):
    def test_full_resident_tool_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            prd = root / ".ai/references/prd"
            archive = prd / ".archive/v1.0"
            archive.mkdir(parents=True)
            (root / "origin").mkdir()
            source = root / "origin/login-requirement.md"
            source.write_bytes(b"incoming requirement\r\n")
            (prd / "00_INDEX.md").write_text("# Login\n\n当前版本: v1.1\n", encoding="utf-8")
            (prd / "login-flow.md").write_bytes(b"live v1.1\r\n")
            (archive / "00_INDEX.md").write_text("当前版本: v1.0\n", encoding="utf-8")
            (archive / "login-flow.md").write_bytes(b"legacy v1.0\n")
            history = root / ".ai/iterations/ITER-0001/AC_LIST.md"
            history.parent.mkdir(parents=True)
            history.write_text("---\nprd_version: v1.0\n---\n.ai/references/prd/login-flow.md\n", encoding="utf-8")
            (root / ".ai/ITERATIONS.md").write_text(
                "current: none\n\n| 迭代号 | 标题 | 状态 |\n|---|---|---|\n| ITER-0001 | Legacy | closed |\n",
                encoding="utf-8",
            )
            (root / ".ai/MILESTONE.md").write_text("| R1 | Login → prd: login-flow | — | planned |\n", encoding="utf-8")

            first = run_json(INBOX, "scan", "--project-root", str(root), "--apply")
            inbox_bytes = (root / ".ai/INBOX.md").read_bytes()
            second = run_json(INBOX, "scan", "--project-root", str(root), "--apply")
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(inbox_bytes, (root / ".ai/INBOX.md").read_bytes())
            self.assertEqual(b"incoming requirement\r\n", source.read_bytes())

            before = run_json(MIGRATE, "resolve", "--project-root", str(root), "--ac-file", ".ai/iterations/ITER-0001/AC_LIST.md", "--ref", "prd/login-flow.md")
            self.assertEqual(".ai/references/prd/.archive/v1.0/login-flow.md", before["path"])
            migrated = run_json(MIGRATE, "apply", "--project-root", str(root), "--prd-id", PRD_A, "--title", "Login", "--now", "2026-07-22T09:00:00+08:00")
            self.assertTrue(migrated["changed"])
            self.assertTrue(run_json(MIGRATE, "verify", "--project-root", str(root))["verified"])
            after = run_json(MIGRATE, "resolve", "--project-root", str(root), "--ac-file", ".ai/iterations/ITER-0001/AC_LIST.md", "--ref", "prd/login-flow.md")
            self.assertEqual(f".ai/references/prd/{PRD_A}/.archive/v1.0/login-flow.md", after["path"])
            self.assertEqual(b"legacy v1.0\n", (root / after["path"]).read_bytes())

            for relative, name in (("apps/web", "@acme/web"), ("packages/ui", "@acme/ui"), ("packages/api", "@acme/api")):
                path = root / relative
                path.mkdir(parents=True)
                (path / "package.json").write_text(json.dumps({"name": name}) + "\n", encoding="utf-8")
            project = root / ".ai/project"
            project.mkdir()
            (project / "workspaces.md").write_text("""# Workspaces

| workspace_key | package_identity | path | kind | status | evidence |
|---|---|---|---|---|---|
| @acme/web | @acme/web | apps/web | app | active | manifest |
| @acme/ui | @acme/ui | packages/ui | library | active | manifest |
| @acme/api | @acme/api | packages/api | library | active | manifest |
""", encoding="utf-8")
            live_index = prd / PRD_A / "00_INDEX.md"
            live_index.write_text(f"""# Login

## Requirement Identity

- prd_id: {PRD_A}
- current_version: v1.1
- status: active

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
| login-flow | login-flow | v1.0 | v1.1 | active |
{scope_block()}""", encoding="utf-8")
            incoming = root / "incoming"
            incoming.mkdir()
            (incoming / "login-flow.md").write_bytes(b"live v1.2 exact\n")
            spec = root / "update.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "prd_id": PRD_A,
                "expected_old_version": "v1.1",
                "new_version": "v1.2",
                "confirmed": True,
                "confirmation": {"mode": "dangerous-self-review", "at": "2026-07-22T09:05:00+08:00"},
                "active_modules": [{"module_slug": "login-flow", "title": "login-flow", "source": "incoming/login-flow.md", "origins": ["login-flow"]}],
                "removed_slugs": [],
                "dispositions": []
            }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            planned = run_json(UPDATE, "plan", "--project-root", str(root), "--spec", str(spec))
            self.assertTrue(planned["apply_ready"])
            applied = run_json(UPDATE, "apply", "--project-root", str(root), "--spec", str(spec), "--now", "2026-07-22T09:06:00+08:00")
            self.assertTrue(applied["changed"])
            self.assertTrue(run_json(UPDATE, "verify", "--project-root", str(root), "--prd-id", PRD_A)["verified"])

            second_prd = prd / PRD_B
            second_prd.mkdir()
            (second_prd / "login-flow.md").write_bytes(b"independent same slug\n")
            (second_prd / "00_INDEX.md").write_text(f"""# Admin Login

- prd_id: {PRD_B}
- current_version: v2.0
- status: active

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
| login-flow | Admin Login | v2.0 | v2.0 | active |
{scope_block()}""", encoding="utf-8")
            collection = prd / "00_INDEX.md"
            collection.write_text(collection.read_text(encoding="utf-8") + f"| {PRD_B} | Admin Login | v2.0 | active | SRC-2 | {PRD_B}/00_INDEX.md |\n", encoding="utf-8")

            (root / ".ai/AC_LIST.md").write_text(f"""---
prd_refs:
  - prd_id: {PRD_A}
    prd_version: v1.1
    module_slugs: [login-flow]
  - prd_id: {PRD_B}
    prd_version: v2.0
    module_slugs: [login-flow]
---
""", encoding="utf-8")
            (root / ".ai/TECH_PLAN.md").write_text("""# Workspace Write Plan

| workspace_key | access | path_patterns | rationale |
|---|---|---|---|
| @acme/web | primary_write | [apps/web/**] | implementation |
| @acme/ui | supporting_write | [packages/ui/**] | shared UI |
""", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "e2e@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "E2E"], check=True)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)

            status = run_json(STATUS, "status", "--project-root", str(root), "--prd-id", PRD_A)
            self.assertEqual(applied["update_id"], status["requirements"][0]["latest_update"]["update_id"])
            self.assertTrue(run_json(SCOPE, "check-plan", "--project-root", str(root))["applicable"])
            allowed = run_json(SCOPE, "check-paths", "--project-root", str(root), "--path", "apps/web/src/main.ts", "--path", "packages/ui/src/button.ts")
            self.assertEqual(2, len(allowed["results"]))
            denied = run_json(SCOPE, "check-paths", "--project-root", str(root), "--path", "packages/api/src/client.ts", expected=2)
            self.assertIn("write denied", denied["error"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
