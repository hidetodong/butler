#!/usr/bin/env python3
"""Read-only CLI for Butler workspace discovery and write-scope checks."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_LIB = REPO_ROOT / "templates" / "hooks"
if str(HOOK_LIB) not in sys.path:
    sys.path.insert(0, str(HOOK_LIB))

from lib.workspace_scope import (  # noqa: E402
    ScopeError,
    authorize_paths,
    discover_workspaces,
    git_changed_paths,
    load_workspace_map,
    parse_prd_refs,
    parse_write_plan,
    resolve_effective_scope,
)


SCHEMA_VERSION = 1


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ScopeError(f"invalid arguments: {message}")


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items() if key != "root"}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def _emit(action: str, ok: bool, **fields: Any) -> None:
    payload = {"schema_version": SCHEMA_VERSION, "action": action, "ok": ok, **fields}
    print(json.dumps(_json_safe(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def build_parser() -> Parser:
    parser = Parser(description="Discover and enforce Butler workspace write scopes")
    sub = parser.add_subparsers(dest="action", required=True, parser_class=Parser)
    for action in ("discover", "validate", "check-plan"):
        item = sub.add_parser(action)
        item.add_argument("--project-root", required=True, type=Path)
    paths = sub.add_parser("check-paths")
    paths.add_argument("--project-root", required=True, type=Path)
    paths.add_argument("--path", action="append", required=True, dest="paths")
    diff = sub.add_parser("check-diff")
    diff.add_argument("--project-root", required=True, type=Path)
    diff.add_argument("--base", required=True)
    diff.add_argument("--head")
    diff.add_argument("--include-untracked", action="store_true")
    return parser


def run(args: argparse.Namespace) -> int:
    action = args.action
    root = args.project_root
    if action == "discover":
        _emit(action, True, discovery=discover_workspaces(root), zero_write=True)
        return 0
    if action == "validate":
        workspace_map = load_workspace_map(root)
        _emit(
            action,
            True,
            workspace_count=len(workspace_map["workspaces"]),
            active_workspaces=sorted(key for key, row in workspace_map["workspaces"].items() if row["status"] == "active"),
            ownership=workspace_map["ownership"],
            zero_write=True,
        )
        return 0
    if action == "check-plan":
        workspace_map = load_workspace_map(root)
        ac = (root.resolve(strict=True) / ".ai/AC_LIST.md").read_text(encoding="utf-8")
        refs = parse_prd_refs(ac)
        if not refs:
            _emit(action, True, applicable=False, reason="AC_LIST has no prd_refs", zero_write=True)
            return 0
        effective = resolve_effective_scope(root, refs, workspace_map)
        plan_text = (root.resolve(strict=True) / ".ai/TECH_PLAN.md").read_text(encoding="utf-8")
        plan = parse_write_plan(plan_text, effective, workspace_map)
        _emit(action, True, applicable=True, effective_scope=effective, write_plan=plan, zero_write=True)
        return 0
    if action == "check-paths":
        result = authorize_paths(root, args.paths)
        _emit(action, True, zero_write=True, **result)
        return 0
    if action == "check-diff":
        paths = git_changed_paths(root, args.base, args.head, args.include_untracked)
        result = authorize_paths(root, paths)
        _emit(action, True, git={"base": args.base, "head": args.head, "include_untracked": args.include_untracked}, zero_write=True, **result)
        return 0
    raise ScopeError(f"unsupported action: {action}")


def main(argv: list[str] | None = None) -> int:
    action = "unknown"
    try:
        args = build_parser().parse_args(argv)
        action = args.action
        return run(args)
    except (ScopeError, OSError, UnicodeError, json.JSONDecodeError) as error:
        _emit(action, False, error=str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
