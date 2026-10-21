#!/usr/bin/env python3
"""Classify Butler CLI entries into A/B/C/D from last-used timestamps."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SINCE_RE = re.compile(r"^([1-9][0-9]*)d$")
BUCKETS = ("A", "B", "C", "D")


class ReportError(ValueError):
    pass


def load_usage():
    path = Path(__file__).resolve().parents[1] / "usage" / "usage.py"
    spec = importlib.util.spec_from_file_location("butler_usage_for_report", path)
    if spec is None or spec.loader is None:
        raise ReportError("usage module is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


usage_mod = load_usage()


def parse_since(value: str) -> int:
    match = SINCE_RE.fullmatch(value.strip())
    if match is None:
        raise ReportError("since must be a positive integer followed by d, for example 90d")
    return int(match.group(1))


def valid_stamp(value: object) -> str | None:
    if isinstance(value, str) and usage_mod.TIMESTAMP_RE.fullmatch(value):
        return value
    return None


def last_used_of(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    return valid_stamp(value.get("last_used"))


def cutoff_stamp(now: str, since_days: int) -> str:
    if valid_stamp(now) is None:
        raise ReportError(f"invalid timestamp: {now}")
    moment = datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (moment - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_entries(root: Path) -> tuple[dict[str, Any], bool]:
    path = usage_mod.usage_path(root)
    if not path.is_file():
        return {}, True
    payload = usage_mod.load_payload(path)
    if payload is None:
        return {}, False
    entries = payload["entries"]
    if not isinstance(entries, dict):
        return {}, False
    return entries, True


def row(entry_id: str, bucket: str, stamp: str | None) -> dict[str, Any]:
    return {"id": entry_id, "bucket": bucket, "last_used": stamp}


def build_report(
    root: Path,
    since_days: int,
    now: str,
    *,
    allowed: set[str] | None = None,
) -> dict[str, Any]:
    allowed_ids = allowed if allowed is not None else usage_mod.allowed_ids()
    entries, trusted = read_entries(root)
    edge = cutoff_stamp(now, since_days)
    buckets: dict[str, list[dict[str, Any]]] = {name: [] for name in BUCKETS}
    for entry_id in sorted(allowed_ids):
        stamp = last_used_of(entries.get(entry_id)) if trusted else None
        if stamp is None:
            bucket = "C"
        elif stamp >= edge:
            bucket = "A"
        else:
            bucket = "B"
        buckets[bucket].append(row(entry_id, bucket, stamp))
    if trusted:
        for entry_id in sorted(set(entries) - allowed_ids):
            buckets["D"].append(row(entry_id, "D", last_used_of(entries.get(entry_id))))
    return {"since_days": since_days, "generated_at": now, "buckets": buckets}


def should_stamp(root: Path) -> bool:
    path = usage_mod.usage_path(root)
    if not path.exists():
        return True
    return usage_mod.load_payload(path) is not None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    report = sub.add_parser("report")
    report.add_argument("--project-root", required=True, type=Path)
    report.add_argument("--since", default="90d")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        since_days = parse_since(args.since)
        root = args.project_root.expanduser().resolve()
        payload = build_report(root, since_days, usage_mod.utc_now())
    except ReportError as error:
        print(f"usage-report: {error}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if should_stamp(root):
        usage_mod.stamp_tool(__file__, list(argv) if argv is not None else sys.argv[1:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
