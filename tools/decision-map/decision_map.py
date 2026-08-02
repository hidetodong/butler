#!/usr/bin/env python3
"""JSON CLI Adapter for the Decision Map engine."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, NoReturn

from engine import DecisionMapError, apply, inspect, plan, verify


class JsonParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise DecisionMapError("invalid_arguments", message, 2)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _document(path: str) -> dict[str, Any]:
    target = Path(path)
    if target.is_symlink() or not target.is_file():
        raise DecisionMapError("invalid_document", f"JSON document must be a regular file: {path}", 2)
    try:
        value = json.loads(target.read_text(encoding="utf-8"), object_pairs_hook=_pairs)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise DecisionMapError("invalid_document", f"cannot read JSON document {path}: {error}", 2) from error
    if not isinstance(value, dict):
        raise DecisionMapError("invalid_document", f"JSON document must contain an object: {path}", 2)
    return value


def parser() -> argparse.ArgumentParser:
    root = JsonParser(description=__doc__)
    actions = root.add_subparsers(dest="action", required=True)
    inspect_parser = actions.add_parser("inspect")
    inspect_parser.add_argument("--project-root", required=True)
    inspect_parser.add_argument("--map-id")
    inspect_parser.add_argument("--now", help=argparse.SUPPRESS)
    plan_parser = actions.add_parser("plan")
    plan_parser.add_argument("--project-root", required=True)
    plan_parser.add_argument("--map-id", required=True)
    plan_parser.add_argument("--spec", required=True)
    plan_parser.add_argument("--now", help=argparse.SUPPRESS)
    apply_parser = actions.add_parser("apply")
    apply_parser.add_argument("--project-root", required=True)
    apply_parser.add_argument("--plan", required=True)
    apply_parser.add_argument("--now", help=argparse.SUPPRESS)
    verify_parser = actions.add_parser("verify")
    verify_parser.add_argument("--project-root", required=True)
    verify_parser.add_argument("--map-id")
    verify_parser.add_argument("--now", help=argparse.SUPPRESS)
    return root


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if args.action == "inspect":
            result = inspect(args.project_root, args.map_id, args.now)
        elif args.action == "plan":
            result = plan(args.project_root, args.map_id, _document(args.spec), args.now)
        elif args.action == "apply":
            result = apply(args.project_root, _document(args.plan), args.now)
        else:
            result = verify(args.project_root, args.map_id, args.now)
        emit(result)
        return 0 if result.get("status") == "ok" else 2
    except DecisionMapError as error:
        emit({"schema_version": 1, "status": "error", "code": error.code, "message": error.message})
        return error.exit_code
    except OSError as error:
        emit({"schema_version": 1, "status": "error", "code": "io_error", "message": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
