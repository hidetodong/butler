"""End-to-end PreToolUse coverage for PRD-backed workspace scope."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tests.test_integration import edit_payload, patch_payload, run_gate


PRD_ID = "2026-07-22-workspace-gate"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scoped_project(tmp_path: Path) -> Path:
    root = tmp_path / "scoped"
    for relative, name in (("apps/web", "@acme/web"), ("packages/ui", "@acme/ui"), ("packages/api", "@acme/api")):
        _write(root / relative / "package.json", json.dumps({"name": name}) + "\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    _write(root / ".ai/CONCEPT.md", "concept\n")
    _write(root / ".ai/AC_LIST.md", f"""---
状态: ack-frozen
prd_refs:
  - prd_id: {PRD_ID}
    prd_version: v1.0
    module_slugs: [flow]
---
""")
    _write(root / ".ai/TECH_PLAN.md", """---
方案状态: pass
---
# Workspace Write Plan

| workspace_key | access | path_patterns | rationale |
|---|---|---|---|
| @acme/web | primary_write | [apps/web/**] | implementation |
| @acme/ui | supporting_write | [packages/ui/**] | shared component |
""")
    _write(root / ".ai/project/workspaces.md", """# Workspaces

| workspace_key | package_identity | path | kind | status | evidence |
|---|---|---|---|---|---|
| @acme/web | @acme/web | apps/web | app | active | manifest |
| @acme/ui | @acme/ui | packages/ui | library | active | manifest |
| @acme/api | @acme/api | packages/api | library | active | manifest |
""")
    _write(root / f".ai/references/prd/{PRD_ID}/00_INDEX.md", f"""# Requirement

- current_version: v1.0

## Modules

| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |
|---|---|---|---|---|
| flow | Flow | v1.0 | v1.0 | active |

## Workspace Scope

- primary_write: [@acme/web]
- supporting_write: [@acme/ui]
- read_only: [@acme/api]
- excluded: []
""")
    return root


def test_edit_and_multiedit_obey_plan(tmp_path):
    root = scoped_project(tmp_path)
    assert run_gate(edit_payload(root, "apps/web/src/main.ts"), root).returncode == 0
    multi = edit_payload(root, "packages/ui/src/button.ts")
    multi["tool_name"] = "MultiEdit"
    assert run_gate(multi, root).returncode == 0


def test_read_only_and_unplanned_paths_fail_closed(tmp_path):
    root = scoped_project(tmp_path)
    denied = run_gate(edit_payload(root, "packages/api/src/client.ts"), root)
    assert denied.returncode == 2 and "workspace_scope" in denied.stderr
    unplanned = run_gate(edit_payload(root, "apps/web-other/x.ts"), root)
    assert unplanned.returncode == 2 and "workspace" in unplanned.stderr


def test_apply_patch_checks_every_target_and_reports_denied_path(tmp_path):
    root = scoped_project(tmp_path)
    command = """*** Begin Patch
*** Add File: apps/web/src/ok.ts
+ok
*** Add File: packages/api/src/no.ts
+no
*** End Patch"""
    denied = run_gate(patch_payload(root, command), root)
    assert denied.returncode == 2
    assert "packages/api/src/no.ts" in denied.stderr


def test_no_prd_refs_is_explicit_not_applicable(tmp_project):
    root = tmp_project("full-artifacts")
    assert run_gate(edit_payload(root, "src/auth.ts"), root).returncode == 0


def test_legacy_prd_version_fails_closed(tmp_path):
    root = scoped_project(tmp_path)
    _write(root / ".ai/AC_LIST.md", "状态: ack-frozen\nprd_version: v1.0\n")
    denied = run_gate(edit_payload(root, "apps/web/src/main.ts"), root)
    assert denied.returncode == 2
    assert "migrate before workspace gating" in denied.stderr
