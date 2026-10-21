#!/usr/bin/env python3
"""Record last-used timestamps for Butler CLI entries. Fail-open on I/O."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
USAGE_REL = Path(".ai") / ".usage.json"
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ID_RE = re.compile(r"^(?:tool|workflow):[a-z0-9]+(?:-[a-z0-9]+)*$")

PRODUCT_TOOLS = frozenset({
    "artifact-pipeline",
    "butler-upgrade",
    "context-budget",
    "decision-map",
    "decision-promotion",
    "decision-work",
    "domain-contract",
    "goal-assurance",
    "handoff",
    "intake",
    "iteration-intake",
    "preference-experiment",
    "prd-migrate",
    "prd-status",
    "prd-update",
    "project-config",
    "state-ledger",
    "usage",
    "usage-report",
    "verification-evidence",
    "workspace-scope",
})
SKIP_TOOLS = frozenset({
    "codex-validators",
    "delivery-selftest",
    "explore-dogfood",
    "mile0009-e2e",
})
BUTLER_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = BUTLER_ROOT / "workflows" / "registry.json"


class UsageError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tool_dirs(tools_root: Path) -> set[str]:
    return {path.name for path in tools_root.iterdir() if path.is_dir() and not path.name.startswith(".")}


def workflow_ids(registry: dict[str, Any] | None = None) -> set[str]:
    data = registry if registry is not None else json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    ids = {str(item["id"]) for item in data.get("workflows", [])}
    ids.add("router")
    return ids


def allowed_ids(*, registry: dict[str, Any] | None = None) -> set[str]:
    ids = {f"tool:{name}" for name in PRODUCT_TOOLS}
    ids.update(f"workflow:{name}" for name in workflow_ids(registry))
    return ids


def infer_root(argv: list[str] | None) -> Path | None:
    args = list(argv or [])
    for index, arg in enumerate(args):
        if arg == "--project-root" and index + 1 < len(args):
            return Path(args[index + 1]).expanduser().resolve()
        if arg.startswith("--project-root="):
            return Path(arg.split("=", 1)[1]).expanduser().resolve()
    cwd = Path.cwd()
    if (cwd / ".ai").is_dir():
        return cwd
    return None


def usage_path(root: Path) -> Path:
    return root / USAGE_REL


def load_payload(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        return None
    entries = data.get("entries")
    if not isinstance(entries, dict):
        return None
    return data


def dump_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(prefix=".usage.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def record(root: Path, entry_id: str, *, allowed: set[str] | None = None, now: str | None = None) -> None:
    allowed_set = allowed if allowed is not None else allowed_ids()
    if not ID_RE.fullmatch(entry_id) or entry_id not in allowed_set:
        raise UsageError(f"unknown usage id: {entry_id}")
    ai = root / ".ai"
    if not ai.is_dir():
        return
    path = usage_path(root)
    payload = load_payload(path) if path.is_file() else None
    if payload is None:
        payload = {"schema_version": SCHEMA_VERSION, "entries": {}}
    stamp = now or utc_now()
    if not TIMESTAMP_RE.fullmatch(stamp):
        raise UsageError(f"invalid timestamp: {stamp}")
    entries = payload["entries"]
    current = entries.get(entry_id)
    if not isinstance(current, dict):
        current = {}
    current["last_used"] = stamp
    entries[entry_id] = {"last_used": current["last_used"]}
    dump_payload(path, payload)


def stamp_tool(script_file: str, argv: list[str] | None = None) -> None:
    try:
        name = Path(script_file).resolve().parent.name
        if name not in PRODUCT_TOOLS:
            return
        root = infer_root(list(argv) if argv is not None else sys.argv[1:])
        if root is None:
            return
        record(root, f"tool:{name}")
    except Exception:
        return


def show(root: Path) -> dict[str, Any]:
    path = usage_path(root)
    payload = load_payload(path) if path.is_file() else None
    if payload is None:
        return {"schema_version": SCHEMA_VERSION, "entries": {}}
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--project-root", required=True, type=Path)
    rec.add_argument("--id", required=True)
    query = sub.add_parser("show")
    query.add_argument("--project-root", required=True, type=Path)
    sub.add_parser("catalog")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "catalog":
            stamp_tool(__file__, argv)
            print(json.dumps(sorted(allowed_ids()), ensure_ascii=False, indent=2))
            return 0
        root = args.project_root.expanduser().resolve()
        if args.command == "show":
            stamp_tool(__file__, argv)
            print(json.dumps(show(root), ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        try:
            record(root, args.id)
        except UsageError as error:
            print(f"usage: {error}", file=sys.stderr)
            return 1
        except Exception:
            return 0
        stamp_tool(__file__, argv)
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
