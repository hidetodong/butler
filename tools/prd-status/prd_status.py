#!/usr/bin/env python3
"""Deterministic, read-only status for Butler PRD collections."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = 1
PRD_ID_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
MODULE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^v[0-9]+(?:\.[0-9]+)*$")
REQ_STATUSES = {"active", "superseded", "retired"}
MODULE_STATUSES = {"active", "removed"}
SCOPE_KEYS = ("primary_write", "supporting_write", "read_only", "excluded")
UPDATE_ID_RE = re.compile(r"^UPD-[0-9a-f]{12}$")
UPDATE_RECEIPT_KEYS = {
    "schema_version", "update_id", "prd_id", "applied_at", "old_version", "new_version",
    "spec_sha256", "pre_collection_tree_sha256", "post_collection_tree_sha256",
    "archive_path", "archive_tree_sha256", "backup", "module_changes", "impact",
    "dispositions", "source_files", "confirmation", "receipt_payload_sha256",
}


class StatusError(ValueError):
    pass


class StatusArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise StatusError(f"invalid arguments: {message}")


def clean_cell(value: str) -> str:
    value = value.strip().strip("`").strip()
    match = re.fullmatch(r"\[([^]]+)]\(([^)]+)\)", value)
    return match.group(2).strip() if match else value


def parse_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = text.splitlines()
    result: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index + 1 < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        header = [part.strip() for part in lines[index].strip().strip("|").split("|")]
        divider = [part.strip() for part in lines[index + 1].strip().strip("|").split("|")]
        if len(header) != len(divider) or not divider or not all(re.fullmatch(r":?-{3,}:?", part) for part in divider):
            index += 1
            continue
        rows: list[list[str]] = []
        index += 2
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            row = [part.strip() for part in lines[index].strip().strip("|").split("|")]
            if len(row) != len(header):
                raise StatusError("markdown table row width does not match its header")
            rows.append(row)
            index += 1
        result.append((header, rows))
    return result


ALIASES = {
    "prd_id": {"prd_id"},
    "title": {"标题", "title"},
    "current_version": {"当前版本", "current_version", "current version"},
    "status": {"状态", "status"},
    "source_hint": {"来源线索", "source_hint", "source hint"},
    "entry": {"入口", "entry"},
    "module_slug": {"module_slug", "slug"},
    "module_title": {"标题 / 章节", "标题/章节", "title / section", "title/section"},
    "first_version": {"首见版本", "first_version", "first version"},
    "workspace_key": {"workspace_key"},
    "package_identity": {"package_identity"},
    "path": {"path"},
    "kind": {"kind"},
    "evidence": {"evidence"},
}


def canonical_header(value: str) -> str | None:
    normalized = value.strip().strip("`").lower()
    for canonical, aliases in ALIASES.items():
        if normalized in {item.lower() for item in aliases}:
            return canonical
    return None


def find_table(text: str, required: set[str]) -> list[dict[str, str]] | None:
    for headers, rows in parse_tables(text):
        canon = [canonical_header(header) for header in headers]
        if required.issubset({item for item in canon if item}):
            if len({item for item in canon if item}) != len([item for item in canon if item]):
                raise StatusError("markdown table contains duplicate semantic columns")
            return [
                {key: clean_cell(value) for key, value in zip(canon, row) if key}
                for row in rows
            ]
    return None


def read_file(path: Path) -> str:
    if path.is_symlink():
        raise StatusError(f"symlink is not allowed: {path}")
    if not path.is_file():
        raise StatusError(f"required file is missing: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise StatusError(f"cannot read UTF-8 file {path}: {error}") from error


def validate_prd_id(value: str) -> None:
    match = PRD_ID_RE.fullmatch(value)
    if not match:
        raise StatusError(f"invalid prd_id: {value}")
    try:
        dt.date.fromisoformat(match.group(1))
    except ValueError as error:
        raise StatusError(f"invalid prd_id date: {value}") from error


def validate_no_symlinks(root: Path) -> None:
    if root.is_symlink():
        raise StatusError(f"PRD root must not be a symlink: {root}")
    for current, dirs, files in os.walk(root, followlinks=False):
        base = Path(current)
        for name in [*dirs, *files]:
            path = base / name
            if path.is_symlink():
                raise StatusError(f"symlink is not allowed: {path.relative_to(root)}")


def validate_project_path(project_root: Path, path: Path) -> None:
    current = project_root
    try:
        relative = path.relative_to(project_root)
    except ValueError as error:
        raise StatusError(f"path is outside project root: {path}") from error
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise StatusError(f"project state path must not traverse a symlink: {current}")
    try:
        path.resolve(strict=True).relative_to(project_root)
    except (OSError, ValueError) as error:
        raise StatusError(f"project state path is missing or escapes project root: {path}") from error


def parse_identity(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for key in ("prd_id", "current_version", "status"):
        matches = re.findall(rf"(?m)^\s*-\s*{key}\s*:\s*`?([^`\s]+)`?\s*$", text)
        if len(matches) != 1:
            raise StatusError(f"single-PRD index must contain exactly one {key} identity field")
        values[key] = matches[0]
    return values


def parse_scope(text: str, active_workspaces: set[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for key in SCOPE_KEYS:
        matches = re.findall(rf"(?m)^\s*-\s*{key}\s*:\s*\[([^]]*)]\s*$", text)
        if len(matches) != 1:
            raise StatusError(f"Workspace Scope must contain exactly one {key} list")
        items = [item.strip().strip("`") for item in matches[0].split(",") if item.strip()]
        if len(items) != len(set(items)):
            raise StatusError(f"Workspace Scope {key} contains duplicate keys")
        result[key] = sorted(items)
    seen: dict[str, str] = {}
    for category, items in result.items():
        for item in items:
            if not item or any(char.isspace() for char in item) or item in {"*", "all"}:
                raise StatusError(f"invalid workspace key in {category}: {item!r}")
            if item in seen:
                raise StatusError(f"workspace key {item} appears in both {seen[item]} and {category}")
            if item not in active_workspaces:
                raise StatusError(f"workspace key is missing or not active in project map: {item}")
            seen[item] = category
    if not result["primary_write"]:
        raise StatusError("Workspace Scope primary_write must not be empty")
    return result


def parse_modules(text: str, directory: Path) -> list[dict[str, str]]:
    required = {"module_slug", "module_title", "first_version", "current_version", "status"}
    rows = find_table(text, required)
    if rows is None:
        raise StatusError(f"module registry table is missing: {directory / '00_INDEX.md'}")
    modules: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        slug = row["module_slug"]
        if not MODULE_RE.fullmatch(slug) or slug in seen:
            raise StatusError(f"invalid or duplicate module_slug in {directory.name}: {slug}")
        seen.add(slug)
        if row["status"] not in MODULE_STATUSES:
            raise StatusError(f"invalid module status for {directory.name}#{slug}: {row['status']}")
        if not VERSION_RE.fullmatch(row["first_version"]) or not VERSION_RE.fullmatch(row["current_version"]):
            raise StatusError(f"invalid module version for {directory.name}#{slug}")
        modules.append({key: row[key] for key in ("module_slug", "module_title", "first_version", "current_version", "status")})
    files = {path.stem for path in directory.glob("*.md") if path.name != "00_INDEX.md"}
    if files != seen:
        raise StatusError(f"module registry/file mismatch in {directory.name}: registered={sorted(seen)}, files={sorted(files)}")
    return sorted(modules, key=lambda item: item["module_slug"])


def latest_update(directory: Path, prd_id: str) -> dict[str, Any] | None:
    receipts = directory / ".butler-updates"
    if not receipts.exists():
        return None
    if receipts.is_symlink() or not receipts.is_dir():
        raise StatusError(f"update receipt directory is unsafe: {prd_id}")
    unknown = [path.name for path in receipts.iterdir() if not path.is_file() or not UPDATE_ID_RE.fullmatch(path.stem) or path.suffix != ".json"]
    if unknown:
        raise StatusError(f"unknown entries in update receipt directory for {prd_id}: {sorted(unknown)}")
    values: list[dict[str, Any]] = []
    for path in sorted(receipts.glob("UPD-*.json")):
        if path.is_symlink():
            raise StatusError(f"update receipt must not be a symlink: {path}")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise StatusError(f"invalid update receipt for {prd_id}: {path.name}") from error
        if not isinstance(value, dict) or set(value) != UPDATE_RECEIPT_KEYS or value.get("schema_version") != 1:
            raise StatusError(f"update receipt schema drift for {prd_id}: {path.name}")
        if value.get("update_id") != path.stem or value.get("prd_id") != prd_id:
            raise StatusError(f"update receipt identity drift for {prd_id}: {path.name}")
        payload_hash = value.get("receipt_payload_sha256")
        hash_input = dict(value)
        hash_input.pop("receipt_payload_sha256", None)
        expected_hash = "sha256:" + hashlib.sha256(json.dumps(hash_input, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        if payload_hash != expected_hash:
            raise StatusError(f"update receipt payload hash drift for {prd_id}: {path.name}")
        if not isinstance(value.get("module_changes"), list) or not isinstance(value.get("impact"), list) or not isinstance(value.get("dispositions"), list):
            raise StatusError(f"update receipt list fields are invalid for {prd_id}: {path.name}")
        values.append(value)
    if not values:
        raise StatusError(f"update receipt directory is empty: {prd_id}")
    latest = max(values, key=lambda item: (str(item["applied_at"]), str(item["update_id"])))
    return {
        "update_id": latest["update_id"],
        "applied_at": latest["applied_at"],
        "old_version": latest["old_version"],
        "new_version": latest["new_version"],
        "module_changes": latest["module_changes"],
        "impact": latest["impact"],
        "dispositions": latest["dispositions"],
    }


def requirement_from_row(prd_root: Path, row: dict[str, str], active_workspaces: set[str]) -> dict[str, Any]:
    prd_id = row["prd_id"]
    validate_prd_id(prd_id)
    if row["status"] not in REQ_STATUSES:
        raise StatusError(f"invalid requirement status for {prd_id}: {row['status']}")
    if not VERSION_RE.fullmatch(row["current_version"]):
        raise StatusError(f"invalid requirement version for {prd_id}: {row['current_version']}")
    expected_entry = f"{prd_id}/00_INDEX.md"
    if row["entry"].removeprefix("./") != expected_entry:
        raise StatusError(f"entry mismatch for {prd_id}: expected {expected_entry}")
    directory = prd_root / prd_id
    if directory.is_symlink() or not directory.is_dir():
        raise StatusError(f"requirement directory is missing or not real: {prd_id}")
    text = read_file(directory / "00_INDEX.md")
    identity = parse_identity(text)
    for key in ("prd_id", "current_version", "status"):
        if identity[key] != row[key]:
            raise StatusError(f"project/single index {key} mismatch for {prd_id}")
    scope = parse_scope(text, active_workspaces)
    modules = parse_modules(text, directory)
    return {
        "prd_id": prd_id,
        "title": row["title"],
        "current_version": row["current_version"],
        "status": row["status"],
        "source_hint": row["source_hint"],
        "entry": expected_entry,
        "workspace_scope": scope,
        "workspace_matches": [],
        "modules": modules,
        "latest_update": latest_update(directory, prd_id),
    }


def load_active_workspaces(project_root: Path) -> set[str]:
    path = project_root / ".ai" / "project" / "workspaces.md"
    validate_project_path(project_root, path)
    text = read_file(path)
    required = {"workspace_key", "package_identity", "path", "kind", "status", "evidence"}
    rows = find_table(text, required)
    if rows is None:
        raise StatusError(f"workspace map table is missing: {path}")
    seen: set[str] = set()
    active: set[str] = set()
    for row in rows:
        key = row["workspace_key"]
        if not key or key in seen:
            raise StatusError(f"invalid or duplicate workspace_key in project map: {key!r}")
        seen.add(key)
        if row["status"] not in {"active", "retired"}:
            raise StatusError(f"invalid workspace status for {key}: {row['status']}")
        if row["status"] == "active":
            active.add(key)
    return active


def collection_status(project_root: Path, prd_root: Path) -> list[dict[str, Any]] | None:
    index_text = read_file(prd_root / "00_INDEX.md")
    required = {"prd_id", "title", "current_version", "status", "source_hint", "entry"}
    rows = find_table(index_text, required)
    if rows is None:
        return None
    active_workspaces = load_active_workspaces(project_root)
    ids = [row["prd_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise StatusError("project PRD index contains duplicate prd_id rows")
    root_modules = [path.name for path in prd_root.glob("*.md") if path.name != "00_INDEX.md"]
    if root_modules:
        raise StatusError(f"mixed collection/legacy layout: root modules {sorted(root_modules)}")
    requirements = [requirement_from_row(prd_root, row, active_workspaces) for row in rows]
    registered = set(ids)
    discovered = {path.name for path in prd_root.iterdir() if path.is_dir() and PRD_ID_RE.fullmatch(path.name)}
    if discovered != registered:
        raise StatusError(f"project index/directory mismatch: indexed={sorted(registered)}, directories={sorted(discovered)}")
    unknown_dirs = [path.name for path in prd_root.iterdir() if path.is_dir() and path.name not in registered]
    if unknown_dirs:
        raise StatusError(f"unknown directories in PRD collection: {sorted(unknown_dirs)}")
    return sorted(requirements, key=lambda item: item["prd_id"])


def legacy_status(prd_root: Path) -> list[dict[str, Any]]:
    text = read_file(prd_root / "00_INDEX.md")
    root_modules = sorted(path for path in prd_root.glob("*.md") if path.name != "00_INDEX.md")
    if not root_modules:
        raise StatusError("PRD index is neither a collection index nor a legacy PRD with root modules")
    dated_dirs = [path.name for path in prd_root.iterdir() if path.is_dir() and PRD_ID_RE.fullmatch(path.name)]
    if dated_dirs:
        raise StatusError("mixed collection/legacy layout")
    version_matches = re.findall(r"(?im)(?:current[_ ]version|当前版本|PRD\s*版本)\s*[:：|]\s*`?(v[0-9]+(?:\.[0-9]+)*)", text)
    if not version_matches:
        version_matches = re.findall(r"\bv[0-9]+(?:\.[0-9]+)*\b", text)
    versions = sorted(set(version_matches))
    if len(versions) != 1:
        raise StatusError("legacy PRD index must identify exactly one current version")
    module_rows = find_table(text, {"module_slug", "module_title", "first_version", "current_version", "status"})
    if module_rows is None:
        modules = [{"module_slug": path.stem, "module_title": path.stem, "first_version": versions[0], "current_version": versions[0], "status": "active"} for path in root_modules]
    else:
        modules = parse_modules(text, prd_root)
    return [{
        "prd_id": None,
        "title": "legacy single PRD",
        "current_version": versions[0],
        "status": "active",
        "source_hint": None,
        "entry": "00_INDEX.md",
        "workspace_scope": {key: [] for key in SCOPE_KEYS},
        "workspace_matches": [],
        "modules": modules,
        "latest_update": None,
        "migration_required": True,
    }]


def run_status(project_root: Path, prd_id: str | None, workspace: str | None) -> tuple[dict[str, Any], int]:
    if prd_id:
        validate_prd_id(prd_id)
    if workspace is not None and (not workspace or any(char.isspace() for char in workspace)):
        raise StatusError("workspace key must be non-empty and contain no whitespace")
    project_root = project_root.resolve(strict=True)
    prd_root = project_root / ".ai" / "references" / "prd"
    validate_project_path(project_root, prd_root)
    if not prd_root.is_dir():
        raise StatusError(f"PRD root is not a directory: {prd_root}")
    validate_no_symlinks(prd_root)
    requirements = collection_status(project_root, prd_root)
    layout = "collection"
    if requirements is None:
        layout = "legacy"
        requirements = legacy_status(prd_root)
        if prd_id:
            raise StatusError("legacy PRD has no explicit prd_id; migrate before --prd-id lookup")
    if prd_id:
        requirements = [item for item in requirements if item["prd_id"] == prd_id]
    if workspace is not None:
        matched: list[dict[str, Any]] = []
        for item in requirements:
            categories = [key for key in SCOPE_KEYS if workspace in item["workspace_scope"][key]]
            if categories:
                item = dict(item)
                item["workspace_matches"] = categories
                matched.append(item)
        requirements = matched
    payload = {
        "schema_version": SCHEMA_VERSION,
        "layout": layout,
        "filters": {"prd_id": prd_id, "workspace": workspace},
        "requirements": requirements,
    }
    return payload, 0 if requirements else 1


def parser() -> argparse.ArgumentParser:
    root = StatusArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    status = sub.add_parser("status", help="read PRD collection status")
    status.add_argument("--project-root", required=True, type=Path)
    status.add_argument("--prd-id")
    status.add_argument("--workspace")
    return root


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))


def main(argv: Iterable[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        payload, code = run_status(args.project_root, args.prd_id, args.workspace)
        emit(payload)
        return code
    except (StatusError, OSError) as error:
        emit({"schema_version": SCHEMA_VERSION, "error": str(error)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
