#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


START = "<!-- butler-inbox:managed:start -->"
END = "<!-- butler-inbox:managed:end -->"
SOURCE_FIELDS = (
    "source_id", "kind", "locator", "source_revision", "observed_sha256",
    "processed_sha256", "observed_at", "status", "classification",
    "proposed_route", "actual_route", "summary", "note",
)
DERIVATION_FIELDS = ("source_id", "artifact_kind", "artifact_ref", "relation", "recorded_at")
SOURCE_ID = re.compile(r"SRC-(\d{4,})$")
SHA256 = re.compile(r"sha256:[0-9a-f]{64}$")
SOURCE_KINDS = {"origin-file", "conversation", "external-document"}
SOURCE_STATUSES = {"unprocessed", "analyzed", "awaiting-confirmation", "routed", "ignored", "source-changed", "failed"}


class InboxError(ValueError):
    pass


@dataclass
class Ledger:
    prefix: str
    suffix: str
    sources: list[dict[str, str]]
    derivations: list[dict[str, str]]


def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def split_row(line: str) -> list[str]:
    value = line.strip()
    if not value.startswith("|") or not value.endswith("|"):
        raise InboxError(f"invalid markdown table row: {line}")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in value[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def parse_table(block: str, heading: str, fields: tuple[str, ...]) -> list[dict[str, str]]:
    lines = block.splitlines()
    try:
        start = lines.index(heading)
    except ValueError as error:
        raise InboxError(f"managed block missing {heading}") from error
    cursor = start + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor + 1 >= len(lines):
        raise InboxError(f"managed table incomplete: {heading}")
    if split_row(lines[cursor]) != list(fields):
        raise InboxError(f"managed table header drift: {heading}")
    separator = split_row(lines[cursor + 1])
    if len(separator) != len(fields) or any(cell != "---" for cell in separator):
        raise InboxError(f"managed table separator drift: {heading}")
    rows: list[dict[str, str]] = []
    for line in lines[cursor + 2 :]:
        if line.startswith("### ") or not line.strip():
            break
        cells = split_row(line)
        if len(cells) != len(fields):
            raise InboxError(f"managed table column drift: {heading}")
        rows.append(dict(zip(fields, cells, strict=True)))
    return rows


def read_ledger(path: Path) -> Ledger:
    if not path.exists():
        return Ledger("# Butler Inbox\n\n", "", [], [])
    text = path.read_text(encoding="utf-8")
    starts, ends = text.count(START), text.count(END)
    if starts == 0 and ends == 0:
        prefix = text
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        if prefix and not prefix.endswith("\n\n"):
            prefix += "\n"
        if not prefix:
            prefix = "# Butler Inbox\n\n"
        return Ledger(prefix, "", [], [])
    if starts != 1 or ends != 1 or text.index(START) > text.index(END):
        raise InboxError("INBOX managed markers must appear exactly once in order")
    before, rest = text.split(START, 1)
    block, after = rest.split(END, 1)
    ledger = Ledger(
        before,
        after,
        parse_table(block, "### Sources", SOURCE_FIELDS),
        parse_table(block, "### Derivations", DERIVATION_FIELDS),
    )
    validate_ledger(ledger)
    return ledger


def validate_ledger(ledger: Ledger) -> None:
    ids: set[str] = set()
    locators: set[str] = set()
    for row in ledger.sources:
        source_id = row["source_id"]
        locator = row["locator"]
        if not SOURCE_ID.fullmatch(source_id) or source_id in ids:
            raise InboxError(f"invalid or duplicate source_id: {source_id}")
        if not locator or locator == "—" or locator in locators:
            raise InboxError(f"invalid or duplicate locator: {locator}")
        if row["kind"] not in SOURCE_KINDS:
            raise InboxError(f"invalid source kind: {row['kind']}")
        if row["status"] not in SOURCE_STATUSES:
            raise InboxError(f"invalid source status: {row['status']}")
        for field in ("observed_sha256", "processed_sha256"):
            value = row[field]
            if value != "—" and not SHA256.fullmatch(value):
                raise InboxError(f"invalid {field}: {source_id}")
        ids.add(source_id)
        locators.add(locator)
    relation_keys: set[tuple[str, str, str, str]] = set()
    for row in ledger.derivations:
        if row["source_id"] not in ids:
            raise InboxError(f"derivation references unknown source_id: {row['source_id']}")
        key = tuple(row[field] for field in ("source_id", "artifact_kind", "artifact_ref", "relation"))
        if key in relation_keys:
            raise InboxError(f"duplicate derivation: {row['source_id']}")
        relation_keys.add(key)


def render_table(fields: tuple[str, ...], rows: list[dict[str, str]]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "|" + "|".join("---" for _ in fields) + "|"
    body = ["| " + " | ".join(escape(row.get(field, "—")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def render(ledger: Ledger) -> str:
    block = (
        f"{START}\n"
        "## Managed Inbox Ledger\n\n"
        "> This block is owned by `$BUTLER_PATH/tools/inbox/inbox.py`; content outside the markers is preserved.\n\n"
        "### Sources\n\n"
        f"{render_table(SOURCE_FIELDS, ledger.sources)}\n\n"
        "### Derivations\n\n"
        f"{render_table(DERIVATION_FIELDS, ledger.derivations)}\n"
        f"{END}"
    )
    return ledger.prefix + block + ledger.suffix


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def discover(project_root: Path) -> tuple[dict[str, Path], list[dict[str, str]]]:
    origin = project_root / "origin"
    found: dict[str, Path] = {}
    rejected: list[dict[str, str]] = []
    if origin.is_symlink():
        return found, [{"locator": "origin", "reason": "origin must be a real directory"}]
    if not origin.exists():
        return found, rejected
    if not origin.is_dir():
        return found, [{"locator": "origin", "reason": "origin must be a real directory"}]
    for current, dirs, files in os.walk(origin, followlinks=False):
        current_path = Path(current)
        kept: list[str] = []
        for name in sorted(dirs):
            candidate = current_path / name
            if candidate.is_symlink():
                rejected.append({"locator": candidate.relative_to(project_root).as_posix(), "reason": "symlink directory rejected"})
            else:
                kept.append(name)
        dirs[:] = kept
        for name in sorted(files):
            candidate = current_path / name
            locator = candidate.relative_to(project_root).as_posix()
            if "\n" in locator or "\r" in locator:
                rejected.append({"locator": "<control-character-path>", "reason": "newline in locator rejected"})
                continue
            if candidate.is_symlink():
                rejected.append({"locator": locator, "reason": "symlink file rejected"})
                continue
            if not candidate.is_file():
                rejected.append({"locator": locator, "reason": "non-regular file rejected"})
                continue
            try:
                candidate.resolve().relative_to(origin.resolve())
            except ValueError:
                rejected.append({"locator": locator, "reason": "path escapes origin"})
                continue
            found[locator] = candidate
    return dict(sorted(found.items())), sorted(rejected, key=lambda item: item["locator"])


def next_source_id(rows: list[dict[str, str]]) -> str:
    numbers: list[int] = []
    for row in rows:
        match = SOURCE_ID.fullmatch(row.get("source_id", ""))
        if not match:
            raise InboxError(f"invalid source_id: {row.get('source_id')}")
        numbers.append(int(match.group(1)))
    return f"SRC-{max(numbers, default=0) + 1:04d}"


def scan(project_root: Path, ledger: Ledger, now: str) -> dict[str, object]:
    validate_ledger(ledger)
    by_locator: dict[str, dict[str, str]] = {}
    ids: set[str] = set()
    for row in ledger.sources:
        source_id, locator = row.get("source_id", ""), row.get("locator", "")
        if source_id in ids or locator in by_locator:
            raise InboxError("duplicate source_id or locator in managed Sources")
        ids.add(source_id)
        by_locator[locator] = row
    found, rejected = discover(project_root)
    counts = {key: 0 for key in ("added", "changed", "unchanged", "missing", "rejected")}
    counts["rejected"] = len(rejected)
    seen: set[str] = set()
    for locator, path in found.items():
        seen.add(locator)
        observed = sha256(path)
        row = by_locator.get(locator)
        if row is None:
            row = {field: "—" for field in SOURCE_FIELDS}
            row.update({
                "source_id": next_source_id(ledger.sources), "kind": "origin-file", "locator": locator,
                "observed_sha256": observed, "observed_at": now, "status": "unprocessed",
                "summary": path.name,
            })
            ledger.sources.append(row)
            by_locator[locator] = row
            counts["added"] += 1
        elif row["observed_sha256"] != observed:
            row["observed_sha256"] = observed
            row["observed_at"] = now
            row["note"] = "source content changed"
            row["status"] = "source-changed" if row["processed_sha256"] != "—" else "unprocessed"
            counts["changed"] += 1
        else:
            counts["unchanged"] += 1
    for row in ledger.sources:
        if row["kind"] == "origin-file" and row["locator"] not in seen:
            counts["missing"] += 1
            if row["note"] in {"—", "source content changed"}:
                row["note"] = "source unavailable at last scan"
    ledger.sources.sort(key=lambda row: int(SOURCE_ID.fullmatch(row["source_id"]).group(1)))
    pending = [
        {"source_id": row["source_id"], "locator": row["locator"], "status": row["status"], "sha256": row["observed_sha256"]}
        for row in ledger.sources if row["status"] in {"unprocessed", "source-changed", "failed"}
    ]
    return {"counts": counts, "pending": pending, "rejected": rejected}


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".INBOX.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def resolve_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir() or not (root / ".ai").is_dir():
        raise InboxError("project root must be an existing Butler project with .ai/")
    return root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan Butler origin/ without modifying user source files.")
    subparsers = parser.add_subparsers(dest="action", required=True)
    for name in ("status", "scan"):
        command = subparsers.add_parser(name)
        command.add_argument("--project-root", required=True)
        if name == "scan":
            command.add_argument("--apply", action="store_true")
            command.add_argument("--now", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        root = resolve_root(args.project_root)
        path = root / ".ai/INBOX.md"
        ledger = read_ledger(path)
        before = path.read_bytes() if path.exists() else None
        if args.action == "status":
            result = {
                "schema_version": 1, "action": "status", "changed": False,
                "counts": {"sources": len(ledger.sources), "derivations": len(ledger.derivations)},
                "sources": ledger.sources,
            }
        else:
            now = args.now or datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
            details = scan(root, ledger, now)
            content = render(ledger)
            encoded = content.encode("utf-8")
            changed = encoded != before
            if args.apply and changed:
                atomic_write(path, content)
            result = {
                "schema_version": 1, "action": "scan", "apply": args.apply, "changed": changed,
                **details,
            }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (InboxError, OSError, UnicodeError) as error:
        print(json.dumps({"schema_version": 1, "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
