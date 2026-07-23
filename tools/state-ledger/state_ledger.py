#!/usr/bin/env python3
"""Deterministic bounded hot ledgers with fixed-range cold shards."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable

ID_RE = {
    "iterations": re.compile(r"^ITER-[0-9]{4,}$", re.ASCII),
    "milestones": re.compile(r"^MILE-[0-9]{4,}$", re.ASCII),
}
SPEC = {
    "iterations": {
        "hot": ".ai/ITERATIONS.md",
        "legacy": ".ai/history/ITERATIONS.cold.md",
        "directory": ".ai/history/iterations",
        "prefix": "ITER",
        "columns": 7,
        "header": "迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付",
    },
    "milestones": {
        "hot": ".ai/MILESTONES.md",
        "legacy": ".ai/history/MILESTONES.cold.md",
        "directory": ".ai/history/milestones",
        "prefix": "MILE",
        "columns": 7,
        "header": "里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付",
    },
}
INDEX = ".ai/state-index.json"
SCHEMA_VERSION = 2
SHARD_RECEIPT_SCHEMA = 1
DEFAULT_HOT_LIMIT = 20
DEFAULT_SHARD_SIZE = 50
SHARD_FILE_RE = re.compile(r"^(ITER|MILE)-([0-9]{6,})-([0-9]{6,})\.(md|json)$", re.ASCII)


class Error(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def number(value: str) -> int:
    return int(value.split("-", 1)[1])


def valid_identity(kind: str, value: str) -> bool:
    if not ID_RE[kind].fullmatch(value):
        return False
    numeric = number(value)
    prefix = str(SPEC[kind]["prefix"])
    return numeric >= 1 and value == f"{prefix}-{numeric:04d}"


def row_line(row: list[str]) -> str:
    return "| " + " | ".join(row) + " |"


def parse_rows(text: str, prefix: str, columns: int) -> list[list[str]]:
    found: list[list[str]] = []
    marker = f"| {prefix}-"
    for raw in text.splitlines():
        if not raw.startswith(marker):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if len(cells) > columns:
            tail_count = columns - 2
            cells = [cells[0], "|".join(cells[1:-tail_count]).strip(), *cells[-tail_count:]]
        if len(cells) != columns:
            raise Error(f"{cells[0] if cells else prefix}: expected {columns} columns")
        found.append(cells)
    return found


rows = parse_rows


def regular_bytes(root: Path, relative: str, required: bool = True) -> bytes | None:
    path = root / relative
    if path.is_symlink():
        raise Error(f"refuse symlink: {relative}")
    if not path.exists():
        if required:
            raise Error(f"missing file: {relative}")
        return None
    if not path.is_file():
        raise Error(f"not a regular file: {relative}")
    return path.read_bytes()


def decode(data: bytes, relative: str) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Error(f"invalid UTF-8: {relative}") from exc


def shard_bounds(value: int, shard_size: int) -> tuple[int, int]:
    if shard_size < 1:
        raise Error("shard_size must be positive")
    start = ((value - 1) // shard_size) * shard_size + 1
    return start, start + shard_size - 1


def shard_relative(kind: str, start: int, end: int, suffix: str = "md") -> str:
    spec = SPEC[kind]
    width = max(6, len(str(end)))
    name = f"{spec['prefix']}-{start:0{width}d}-{end:0{width}d}.{suffix}"
    return f"{spec['directory']}/{name}"


def render_shard(kind: str, start: int, end: int, shard_rows: list[list[str]]) -> str:
    spec = SPEC[kind]
    lines = [
        f"# {spec['prefix']} cold ledger · {start}–{end}",
        "",
        f"| {spec['header']} |",
        "|---|---|---|---|---|---|---|",
        *[row_line(row) for row in sorted(shard_rows, key=lambda item: number(item[0]), reverse=True)],
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_hot(original: str, kind: str, hot_rows: list[list[str]]) -> str:
    prefix = SPEC[kind]["prefix"]
    marker = f"| {prefix}-"
    output: list[str] = []
    inserted = False
    for raw in original.splitlines():
        if raw.startswith(marker):
            if not inserted:
                output.extend(row_line(row) for row in hot_rows)
                inserted = True
            continue
        output.append(raw)
    if not inserted:
        raise Error(f"{prefix} hot ledger has no data row insertion point")
    return "\n".join(output).rstrip() + "\n"


def discover_managed(root: Path, kind: str) -> set[str]:
    directory = root / str(SPEC[kind]["directory"])
    if not directory.exists():
        return set()
    if directory.is_symlink() or not directory.is_dir():
        raise Error(f"invalid shard directory: {SPEC[kind]['directory']}")
    found: set[str] = set()
    prefix = str(SPEC[kind]["prefix"])
    for path in directory.iterdir():
        relative = str(path.relative_to(root))
        if path.is_symlink() or not path.is_file():
            raise Error(f"invalid shard entry: {relative}")
        match = SHARD_FILE_RE.fullmatch(path.name)
        if match is None or match.group(1) != prefix:
            raise Error(f"orphan shard entry: {relative}")
        start, end = int(match.group(2)), int(match.group(3))
        if start > end or shard_relative(kind, start, end, match.group(4)) != relative:
            raise Error(f"non-canonical shard entry: {relative}")
        found.add(relative)
    return found


def load_sources(root: Path, kind: str) -> tuple[str, list[list[str]], set[str]]:
    spec = SPEC[kind]
    hot_data = regular_bytes(root, str(spec["hot"]))
    assert hot_data is not None
    hot_text = decode(hot_data, str(spec["hot"]))
    sources: list[tuple[str, str]] = [(str(spec["hot"]), hot_text)]
    legacy_data = regular_bytes(root, str(spec["legacy"]), required=False)
    managed = discover_managed(root, kind)
    if legacy_data is not None:
        sources.append((str(spec["legacy"]), decode(legacy_data, str(spec["legacy"]))))
    for relative in sorted(path for path in managed if path.endswith(".md")):
        data = regular_bytes(root, relative)
        assert data is not None
        sources.append((relative, decode(data, relative)))

    all_rows: list[list[str]] = []
    owners: dict[str, str] = {}
    for relative, text in sources:
        for row in parse_rows(text, str(spec["prefix"]), int(spec["columns"])):
            identifier = row[0]
            if not valid_identity(kind, identifier):
                raise Error(f"invalid id: {identifier}")
            if identifier in owners:
                raise Error(f"duplicate id across {owners[identifier]} and {relative}: {identifier}")
            owners[identifier] = relative
            all_rows.append(row)
    if not all_rows:
        raise Error(f"{spec['prefix']} ledger has no rows")
    return hot_text, all_rows, managed


def shard_receipt(kind: str, start: int, end: int, relative: str, rendered: str, count: int) -> str:
    receipt = {
        "schema_version": SHARD_RECEIPT_SCHEMA,
        "kind": kind,
        "start": start,
        "end": end,
        "path": relative,
        "count": count,
        "sha256": digest(rendered.encode("utf-8")),
    }
    return json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def routing_meta(kind: str) -> dict[str, object]:
    spec = SPEC[kind]
    return {
        "scheme": "fixed-range-v1",
        "directory": spec["directory"],
        "prefix": spec["prefix"],
        "minimum_width": 6,
        "receipt_suffix": ".json",
    }


def build(root: Path, hot_limit: int, shard_size: int) -> tuple[dict[str, object], dict[str, str], set[str]]:
    if hot_limit < 1 or shard_size < 1:
        raise Error("hot_limit and shard_size must be positive")
    payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "hot_limit": hot_limit,
        "shard_size": shard_size,
        "ledgers": {},
    }
    writes: dict[str, str] = {}
    deletes: set[str] = set()

    for kind, spec in SPEC.items():
        hot_text, all_rows, discovered = load_sources(root, kind)
        ordered = sorted(all_rows, key=lambda row: number(row[0]), reverse=True)
        hot_rows = ordered[:hot_limit]
        cold_rows = ordered[hot_limit:]
        hot_rendered = render_hot(hot_text, kind, hot_rows)
        writes[str(spec["hot"])] = hot_rendered

        buckets: dict[tuple[int, int], list[list[str]]] = {}
        for row in cold_rows:
            bounds = shard_bounds(number(row[0]), shard_size)
            buckets.setdefault(bounds, []).append(row)

        target_files: set[str] = set()
        for start, end in sorted(buckets):
            relative = shard_relative(kind, start, end)
            receipt_path = shard_relative(kind, start, end, "json")
            rendered = render_shard(kind, start, end, buckets[(start, end)])
            writes[relative] = rendered
            writes[receipt_path] = shard_receipt(kind, start, end, relative, rendered, len(buckets[(start, end)]))
            target_files.update((relative, receipt_path))

        deletes.update(discovered - target_files)
        if (root / str(spec["legacy"])).exists():
            deletes.add(str(spec["legacy"]))

        payload["ledgers"][kind] = {
            "max_used": number(ordered[0][0]),
            "row_count": len(ordered),
            "hot_count": len(hot_rows),
            "hot_sha256": digest(hot_rendered.encode("utf-8")),
            "cold_count": len(cold_rows),
            "shard_count": len(buckets),
            "routing": routing_meta(kind),
        }

    return payload, writes, deletes


def _safe_path(root: Path, relative: str) -> Path:
    candidate = root / relative
    if candidate.is_symlink():
        raise Error(f"refuse symlink target: {relative}")
    resolved_parent = candidate.parent.resolve()
    ai_root = (root / ".ai").resolve()
    if resolved_parent != ai_root and ai_root not in resolved_parent.parents:
        raise Error(f"path escapes .ai: {relative}")
    return candidate


def atomic_update(
    root: Path,
    writes: dict[str, str],
    deletes: set[str],
    replace: Callable[[str | os.PathLike[str], str | os.PathLike[str]], None] = os.replace,
) -> None:
    targets = {relative: _safe_path(root, relative) for relative in set(writes) | set(deletes)}
    backups = {relative: path.read_bytes() if path.exists() else None for relative, path in targets.items()}
    temps: list[tuple[Path, Path]] = []
    try:
        for relative, text in writes.items():
            path = targets[relative]
            path.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
            temps.append((Path(temporary), path))
        for temporary, path in temps:
            replace(temporary, path)
        for relative in deletes:
            path = targets[relative]
            if path.exists():
                path.unlink()
    except Exception:
        for relative, path in targets.items():
            previous = backups[relative]
            if previous is None:
                if path.exists():
                    path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(previous)
        raise
    finally:
        for temporary, _ in temps:
            if temporary.exists():
                temporary.unlink()


def inspect(root: Path, hot_limit: int, shard_size: int) -> dict[str, object]:
    return build(root, hot_limit, shard_size)[0]


def migrate(root: Path, hot_limit: int, shard_size: int) -> dict[str, object]:
    payload, writes, deletes = build(root, hot_limit, shard_size)
    writes[INDEX] = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    atomic_update(root, writes, deletes)
    return payload


def _load_index(root: Path) -> tuple[dict[str, object], int]:
    data = regular_bytes(root, INDEX)
    assert data is not None
    try:
        payload = json.loads(decode(data, INDEX))
    except json.JSONDecodeError as exc:
        raise Error("invalid state index JSON") from exc
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise Error(f"state index schema must be {SCHEMA_VERSION}; run migrate")
    return payload, len(data)


def _validate_routing(kind: str, ledger: dict[str, object]) -> None:
    if ledger.get("routing") != routing_meta(kind):
        raise Error(f"invalid routing metadata: {kind}")


def check(root: Path) -> dict[str, object]:
    saved, _ = _load_index(root)
    try:
        hot_limit = int(saved["hot_limit"])
        shard_size = int(saved["shard_size"])
        for kind in SPEC:
            _validate_routing(kind, saved["ledgers"][kind])
    except (KeyError, TypeError, ValueError) as exc:
        raise Error("invalid state index") from exc
    payload, writes, deletes = build(root, hot_limit, shard_size)
    if deletes:
        raise Error(f"legacy or orphan managed files present: {sorted(deletes)}")
    if payload != saved:
        raise Error("state index metadata is stale")
    for relative, expected in writes.items():
        actual = regular_bytes(root, relative)
        assert actual is not None
        if actual != expected.encode("utf-8"):
            raise Error(f"managed ledger/shard/receipt drift: {relative}")
    return saved


def lookup(root: Path, identifier: str) -> tuple[int, dict[str, object]]:
    if identifier.startswith("ITER-"):
        kind = "iterations"
    elif identifier.startswith("MILE-"):
        kind = "milestones"
    else:
        raise Error("identity must start with ITER- or MILE-")
    if not valid_identity(kind, identifier):
        raise Error("identity must be canonical positive ASCII digits with at least four places")

    index, bytes_read = _load_index(root)
    try:
        shard_size = int(index["shard_size"])
        ledger = index["ledgers"][kind]
        _validate_routing(kind, ledger)
    except (KeyError, TypeError, ValueError) as exc:
        raise Error("invalid state index routing") from exc

    spec = SPEC[kind]
    hot_data = regular_bytes(root, str(spec["hot"]))
    assert hot_data is not None
    bytes_read += len(hot_data)
    hot_rows = parse_rows(decode(hot_data, str(spec["hot"])), str(spec["prefix"]), int(spec["columns"]))
    if digest(hot_data) != ledger.get("hot_sha256") or len(hot_rows) != ledger.get("hot_count"):
        raise Error(f"hot ledger does not match state index: {spec['hot']}")
    hot_seen: set[str] = set()
    for row in hot_rows:
        if not valid_identity(kind, row[0]):
            raise Error(f"invalid id in hot ledger: {row[0]}")
        if row[0] in hot_seen:
            raise Error(f"duplicate id in hot ledger: {row[0]}")
        hot_seen.add(row[0])
        if row[0] == identifier:
            return 0, {
                "schema_version": SCHEMA_VERSION,
                "status": "found",
                "id": identifier,
                "source": str(spec["hot"]),
                "bytes_read": bytes_read,
                "row": row,
            }

    start, end = shard_bounds(number(identifier), shard_size)
    relative = shard_relative(kind, start, end)
    receipt_path = shard_relative(kind, start, end, "json")
    shard_data = regular_bytes(root, relative, required=False)
    receipt_data = regular_bytes(root, receipt_path, required=False)
    if shard_data is None and receipt_data is None:
        return 1, {
            "schema_version": SCHEMA_VERSION,
            "status": "not_found",
            "id": identifier,
            "bytes_read": bytes_read,
        }
    if shard_data is None or receipt_data is None:
        raise Error(f"incomplete shard pair: {relative}")
    bytes_read += len(shard_data) + len(receipt_data)
    try:
        receipt = json.loads(decode(receipt_data, receipt_path))
    except json.JSONDecodeError as exc:
        raise Error(f"invalid shard receipt: {receipt_path}") from exc
    shard_text = decode(shard_data, relative)
    shard_rows = parse_rows(shard_text, str(spec["prefix"]), int(spec["columns"]))
    seen: set[str] = set()
    for row in shard_rows:
        if not valid_identity(kind, row[0]):
            raise Error(f"invalid id in shard: {row[0]}")
        if row[0] in seen:
            raise Error(f"duplicate id in shard: {row[0]}")
        seen.add(row[0])
        value = number(row[0])
        if not start <= value <= end:
            raise Error(f"row routed to wrong shard: {row[0]}")
    expected_receipt = {
        "schema_version": SHARD_RECEIPT_SCHEMA,
        "kind": kind,
        "start": start,
        "end": end,
        "path": relative,
        "count": len(shard_rows),
        "sha256": digest(shard_data),
    }
    if receipt != expected_receipt:
        raise Error(f"shard receipt mismatch: {receipt_path}")
    for row in shard_rows:
        if row[0] == identifier:
            return 0, {
                "schema_version": SCHEMA_VERSION,
                "status": "found",
                "id": identifier,
                "source": relative,
                "bytes_read": bytes_read,
                "row": row,
            }
    return 1, {
        "schema_version": SCHEMA_VERSION,
        "status": "not_found",
        "id": identifier,
        "source": relative,
        "bytes_read": bytes_read,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("inspect", "migrate", "check", "lookup"))
    parser.add_argument("identity", nargs="?")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--hot-limit", type=int, default=DEFAULT_HOT_LIMIT)
    parser.add_argument("--shard-size", type=int, default=DEFAULT_SHARD_SIZE)
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    try:
        if args.command == "check":
            result = check(root)
            exit_code = 0
        elif args.command == "migrate":
            result = migrate(root, args.hot_limit, args.shard_size)
            exit_code = 0
        elif args.command == "inspect":
            result = inspect(root, args.hot_limit, args.shard_size)
            exit_code = 0
        else:
            if not args.identity:
                raise Error("lookup requires ITER-NNNN or MILE-NNNN")
            exit_code, result = lookup(root, args.identity)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return exit_code
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, Error) as exc:
        print(json.dumps({"schema_version": SCHEMA_VERSION, "status": "error", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
