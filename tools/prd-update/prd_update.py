#!/usr/bin/env python3
"""Transactional updates for one independently identified Butler PRD."""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


STATUS_DIR = Path(__file__).resolve().parents[1] / "prd-status"
sys.path.insert(0, str(STATUS_DIR))
import prd_status as status_contract  # noqa: E402


SCHEMA_VERSION = 1
UPDATE_ID_RE = re.compile(r"^UPD-[0-9a-f]{12}$")
VERSION_RE = re.compile(r"^v[0-9]+(?:\.[0-9]+)+$")
SPEC_KEYS = {
    "schema_version", "prd_id", "expected_old_version", "new_version",
    "confirmed", "confirmation", "active_modules", "removed_slugs", "dispositions",
}
MODULE_KEYS = {"module_slug", "title", "source", "origins"}
CONFIRMATION_KEYS = {"mode", "at"}
DISPOSITION_KEYS = {"path", "decision", "note"}
RECEIPT_KEYS = {
    "schema_version", "update_id", "prd_id", "applied_at", "old_version", "new_version",
    "spec_sha256", "pre_collection_tree_sha256", "post_collection_tree_sha256",
    "archive_path", "archive_tree_sha256", "backup", "module_changes", "impact",
    "dispositions", "source_files", "confirmation", "receipt_payload_sha256",
}
DECISIONS = {
    "future": {"use-new-on-start", "defer", "not-applicable"},
    "active": {"amend-and-refreeze", "keep-pinned", "defer"},
    "closed": {"keep-pinned-history", "open-follow-up", "defer"},
}


class UpdateError(ValueError):
    pass


class UpdateArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UpdateError(f"invalid arguments: {message}")


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def version_tuple(value: str) -> tuple[int, ...]:
    if not VERSION_RE.fullmatch(value):
        raise UpdateError(f"invalid PRD version: {value}")
    parts = [int(part) for part in value[1:].split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def resolve_root(value: str) -> Path:
    try:
        root = Path(value).resolve(strict=True)
    except OSError as error:
        raise UpdateError(f"project root does not exist: {value}") from error
    if not root.is_dir() or not (root / ".ai").is_dir():
        raise UpdateError("project root must be an existing Butler project")
    status_contract.validate_project_path(root, root / ".ai/references/prd")
    return root


def tree_entries(root: Path, *, exclude: set[str] | None = None) -> list[dict[str, str]]:
    excluded = exclude or set()
    if root.is_symlink() or not root.is_dir():
        raise UpdateError(f"tree root must be a real directory: {root}")
    result: list[dict[str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if relative in excluded:
            continue
        if path.is_symlink():
            raise UpdateError(f"symlink rejected: {relative}")
        if path.is_dir():
            result.append({"kind": "dir", "path": relative, "sha256": "—"})
        elif path.is_file():
            result.append({"kind": "file", "path": relative, "sha256": sha256(path.read_bytes())})
        else:
            raise UpdateError(f"non-regular tree entry rejected: {relative}")
    return result


def tree_hash(root: Path, *, exclude: set[str] | None = None) -> str:
    return sha256(b"\n".join(canonical_json(item) for item in tree_entries(root, exclude=exclude)))


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        actual = set(value) if isinstance(value, dict) else set()
        raise UpdateError(f"{label} fields mismatch: {sorted(actual ^ keys)}")
    return value


def read_source(spec_path: Path, locator: str) -> tuple[Path, bytes]:
    candidate = Path(locator)
    path = candidate if candidate.is_absolute() else spec_path.parent / candidate
    if path.is_symlink():
        raise UpdateError(f"module source must not be a symlink: {locator}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise UpdateError(f"module source is missing: {locator}") from error
    if not resolved.is_file():
        raise UpdateError(f"module source must be a regular file: {locator}")
    data = resolved.read_bytes()
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise UpdateError(f"module source must be UTF-8 Markdown: {locator}") from error
    if not data:
        raise UpdateError(f"module source must not be empty: {locator}")
    return resolved, data


def load_spec(path_value: str) -> tuple[Path, dict[str, Any], dict[str, bytes], str]:
    path = Path(path_value)
    if path.is_symlink():
        raise UpdateError("update spec must not be a symlink")
    try:
        path = path.resolve(strict=True)
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, json.JSONDecodeError) as error:
        raise UpdateError(f"cannot read update spec: {error}") from error
    spec = exact_object(value, SPEC_KEYS, "update spec")
    if spec["schema_version"] != 1:
        raise UpdateError("update spec schema_version must be 1")
    status_contract.validate_prd_id(str(spec["prd_id"]))
    old_version = str(spec["expected_old_version"])
    new_version = str(spec["new_version"])
    if version_tuple(new_version) <= version_tuple(old_version):
        raise UpdateError("new_version must be strictly greater than expected_old_version")
    if not isinstance(spec["confirmed"], bool):
        raise UpdateError("confirmed must be boolean")
    confirmation = exact_object(spec["confirmation"], CONFIRMATION_KEYS, "confirmation")
    if confirmation["mode"] not in {"pending", "user-ack", "dangerous-self-review"}:
        raise UpdateError("confirmation.mode is invalid")
    if confirmation["mode"] == "pending":
        if confirmation["at"] is not None or spec["confirmed"]:
            raise UpdateError("pending confirmation requires confirmed=false and at=null")
    else:
        if not spec["confirmed"] or not isinstance(confirmation["at"], str):
            raise UpdateError("completed confirmation requires confirmed=true and an ISO timestamp")
        try:
            dt.datetime.fromisoformat(confirmation["at"])
        except ValueError as error:
            raise UpdateError("confirmation.at must be an ISO-8601 timestamp") from error
    modules = spec["active_modules"]
    if not isinstance(modules, list) or not modules:
        raise UpdateError("active_modules must be a non-empty list")
    sources: dict[str, bytes] = {}
    normalized_sources: list[dict[str, Any]] = []
    source_paths: set[Path] = set()
    slugs: set[str] = set()
    for index, item_value in enumerate(modules):
        item = exact_object(item_value, MODULE_KEYS, f"active_modules[{index}]")
        slug = str(item["module_slug"])
        if not status_contract.MODULE_RE.fullmatch(slug) or slug in slugs:
            raise UpdateError(f"invalid or duplicate active module_slug: {slug}")
        slugs.add(slug)
        title = item["title"]
        if not isinstance(title, str) or not title.strip() or "\n" in title or "|" in title:
            raise UpdateError(f"module title must be one safe non-empty line: {slug}")
        origins = item["origins"]
        if not isinstance(origins, list) or any(not isinstance(origin, str) for origin in origins) or len(origins) != len(set(origins)):
            raise UpdateError(f"origins must be a unique string list: {slug}")
        if not isinstance(item["source"], str) or not item["source"]:
            raise UpdateError(f"module source locator is invalid: {slug}")
        source_path, data = read_source(path, item["source"])
        if source_path in source_paths:
            raise UpdateError(f"two modules cannot reuse one source file: {source_path}")
        source_paths.add(source_path)
        sources[slug] = data
        normalized_sources.append({"module_slug": slug, "sha256": sha256(data)})
    removed = spec["removed_slugs"]
    if not isinstance(removed, list) or any(not isinstance(slug, str) for slug in removed) or len(removed) != len(set(removed)):
        raise UpdateError("removed_slugs must be a unique string list")
    dispositions = spec["dispositions"]
    if not isinstance(dispositions, list):
        raise UpdateError("dispositions must be a list")
    seen_paths: set[str] = set()
    for index, item_value in enumerate(dispositions):
        item = exact_object(item_value, DISPOSITION_KEYS, f"dispositions[{index}]")
        if not isinstance(item["path"], str) or not item["path"] or item["path"] in seen_paths:
            raise UpdateError("disposition paths must be unique non-empty strings")
        seen_paths.add(item["path"])
        if not isinstance(item["decision"], str) or not isinstance(item["note"], str):
            raise UpdateError("disposition decision/note must be strings")
    normalized = dict(spec)
    normalized["active_modules"] = [
        {key: item[key] for key in ("module_slug", "title", "source", "origins")}
        for item in modules
    ]
    normalized["source_files"] = sorted(normalized_sources, key=lambda item: item["module_slug"])
    spec_hash = sha256(canonical_json(normalized))
    return path, spec, sources, spec_hash


def locate_table(text: str, required: set[str]) -> tuple[int, int, list[str], list[str]]:
    lines = text.splitlines()
    for index in range(len(lines) - 1):
        if not lines[index].lstrip().startswith("|"):
            continue
        headers = [part.strip() for part in lines[index].strip().strip("|").split("|")]
        divider = [part.strip() for part in lines[index + 1].strip().strip("|").split("|")]
        if len(headers) != len(divider) or not all(re.fullmatch(r":?-{3,}:?", part) for part in divider):
            continue
        canonical = [status_contract.canonical_header(header) for header in headers]
        if required.issubset({item for item in canonical if item}):
            end = index + 2
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            return index, end, headers, canonical
    raise UpdateError(f"required Markdown table is missing: {sorted(required)}")


def render_project_index(text: str, prd_id: str, new_version: str) -> str:
    required = {"prd_id", "title", "current_version", "status", "source_hint", "entry"}
    start, end, _, canonical = locate_table(text, required)
    lines = text.splitlines()
    id_col = canonical.index("prd_id")
    version_col = canonical.index("current_version")
    matched = 0
    for index in range(start + 2, end):
        cells = [part.strip() for part in lines[index].strip().strip("|").split("|")]
        if status_contract.clean_cell(cells[id_col]) == prd_id:
            cells[version_col] = new_version
            lines[index] = "| " + " | ".join(cells) + " |"
            matched += 1
    if matched != 1:
        raise UpdateError(f"project index must contain exactly one target row: {prd_id}")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def render_requirement_index(text: str, new_version: str, rows: list[dict[str, str]]) -> str:
    pattern = re.compile(r"(?m)^(\s*-\s*current_version\s*:\s*)`?([^`\s]+)`?(\s*)$")
    text, count = pattern.subn(rf"\g<1>{new_version}\g<3>", text)
    if count != 1:
        raise UpdateError("single-PRD index must contain one current_version identity field")
    required = {"module_slug", "module_title", "first_version", "current_version", "status"}
    start, end, _, _ = locate_table(text, required)
    lines = text.splitlines()
    table = [
        "| module_slug | 标题 / 章节 | 首见版本 | 当前版本 | 状态 |",
        "|---|---|---|---|---|",
    ]
    for row in sorted(rows, key=lambda item: item["module_slug"]):
        table.append(f"| {row['module_slug']} | {row['module_title']} | {row['first_version']} | {row['current_version']} | {row['status']} |")
    lines[start:end] = table
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def referenced_modules(text: str, prd_id: str) -> set[str]:
    pattern = re.compile(
        rf"(?m)^\s*-\s*prd_id:\s*{re.escape(prd_id)}\s*$\n"
        r"^\s+prd_version:\s*\S+\s*$\n^\s+module_slugs:\s*\[([^]]*)]"
    )
    modules: set[str] = set()
    for group in pattern.findall(text):
        modules.update(item.strip() for item in group.split(",") if item.strip())
    return modules


def impact_scan(root: Path, prd_id: str, changed_slugs: set[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    milestone = root / ".ai/MILESTONE.md"
    if milestone.is_file() and not milestone.is_symlink():
        text = milestone.read_text(encoding="utf-8")
        route_state = {"planned": "future", "active": "active", "closed": "closed"}
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not re.fullmatch(r"R[0-9]+", cells[0]) or cells[-1] not in route_state:
                continue
            found = {
                slug for slug in changed_slugs
                if re.search(rf"(?<![a-z0-9-]){re.escape(prd_id)}#{re.escape(slug)}(?![a-z0-9-])", line)
            }
            if found:
                results.append({"state": route_state[cells[-1]], "path": f".ai/MILESTONE.md#{cells[0]}", "module_slugs": sorted(found)})
    active = root / ".ai/AC_LIST.md"
    if active.is_file() and not active.is_symlink():
        found = referenced_modules(active.read_text(encoding="utf-8"), prd_id) & changed_slugs
        if found:
            results.append({"state": "active", "path": ".ai/AC_LIST.md", "module_slugs": sorted(found)})
    archive = root / ".ai/iterations"
    if archive.is_symlink():
        raise UpdateError(".ai/iterations must not be a symlink")
    if archive.is_dir():
        ledger = root / ".ai/ITERATIONS.md"
        if ledger.is_symlink() or not ledger.is_file():
            raise UpdateError("ITERATIONS ledger is required for archived impact classification")
        statuses: dict[str, str] = {}
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| ITER-"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 3:
                statuses[cells[0]] = cells[2]
        for path in sorted(archive.glob("ITER-*/AC_LIST.md")):
            if path.is_symlink():
                raise UpdateError(f"archived AC must not be a symlink: {path.relative_to(root)}")
            iteration = path.parent.name
            if statuses.get(iteration) != "closed":
                continue
            found = referenced_modules(path.read_text(encoding="utf-8"), prd_id) & changed_slugs
            if found:
                results.append({"state": "closed", "path": path.relative_to(root).as_posix(), "module_slugs": sorted(found)})
    return sorted(results, key=lambda item: (item["state"], item["path"]))


def disposition_report(spec: dict[str, Any], impact: list[dict[str, Any]]) -> tuple[list[dict[str, str]], list[str]]:
    by_path = {item["path"]: item for item in spec["dispositions"]}
    impact_paths = {item["path"] for item in impact}
    extras = sorted(set(by_path) - impact_paths)
    if extras:
        raise UpdateError(f"dispositions reference paths outside current impact: {extras}")
    missing: list[str] = []
    normalized: list[dict[str, str]] = []
    for item in impact:
        disposition = by_path.get(item["path"])
        if disposition is None:
            missing.append(item["path"])
            continue
        decision = disposition["decision"]
        if decision not in DECISIONS[item["state"]]:
            raise UpdateError(f"invalid {item['state']} disposition for {item['path']}: {decision}")
        normalized.append({"path": item["path"], "state": item["state"], "decision": decision, "note": disposition["note"]})
    return normalized, missing


def receipt_dir(prd_root: Path, prd_id: str) -> Path:
    return prd_root / prd_id / ".butler-updates"


def read_receipt(root: Path, prd_id: str, update_id: str | None = None) -> tuple[Path, dict[str, Any]]:
    status_contract.validate_prd_id(prd_id)
    directory = receipt_dir(root / ".ai/references/prd", prd_id)
    if directory.is_symlink() or not directory.is_dir():
        raise UpdateError(f"update receipt directory is missing for {prd_id}")
    candidates = sorted(directory.glob("UPD-*.json"))
    if update_id:
        if not UPDATE_ID_RE.fullmatch(update_id):
            raise UpdateError("update_id is invalid")
        candidates = [directory / f"{update_id}.json"]
    receipts: list[tuple[Path, dict[str, Any]]] = []
    for path in candidates:
        if path.is_symlink() or not path.is_file():
            raise UpdateError(f"update receipt must be a real file: {path}")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise UpdateError(f"invalid update receipt: {path}") from error
        receipt = exact_object(value, RECEIPT_KEYS, "update receipt")
        if receipt["schema_version"] != 1 or receipt["prd_id"] != prd_id or receipt["update_id"] != path.stem or not UPDATE_ID_RE.fullmatch(str(receipt["update_id"])):
            raise UpdateError("update receipt identity drift")
        payload_hash = receipt.get("receipt_payload_sha256")
        hash_input = dict(receipt)
        hash_input.pop("receipt_payload_sha256", None)
        if payload_hash != sha256(canonical_json(hash_input)):
            raise UpdateError("update receipt payload hash drift")
        try:
            dt.datetime.fromisoformat(str(receipt["applied_at"]))
        except ValueError as error:
            raise UpdateError("update receipt applied_at is invalid") from error
        receipts.append((path, receipt))
    if not receipts:
        raise UpdateError(f"update receipt not found: {prd_id}/{update_id or 'latest'}")
    if update_id:
        return receipts[0]
    return max(receipts, key=lambda item: (str(item[1]["applied_at"]), str(item[1]["update_id"])))


def existing_receipt_for_spec(root: Path, prd_id: str, spec_hash: str) -> dict[str, Any] | None:
    directory = receipt_dir(root / ".ai/references/prd", prd_id)
    if not directory.exists():
        return None
    if directory.is_symlink() or not directory.is_dir():
        raise UpdateError("update receipt directory is unsafe")
    matches: list[dict[str, Any]] = []
    for path in sorted(directory.glob("UPD-*.json")):
        _, receipt = read_receipt(root, prd_id, path.stem)
        if receipt["spec_sha256"] == spec_hash:
            matches.append(receipt)
    if len(matches) > 1:
        raise UpdateError("multiple receipts claim the same update spec")
    return matches[0] if matches else None


def build_plan(root: Path, spec_path_value: str) -> dict[str, Any]:
    spec_path, spec, sources, spec_hash = load_spec(spec_path_value)
    prd_root = root / ".ai/references/prd"
    status_contract.validate_no_symlinks(prd_root)
    requirements = status_contract.collection_status(root, prd_root)
    if requirements is None:
        raise UpdateError("PRD update requires collection layout; migrate legacy first")
    prd_id = str(spec["prd_id"])
    target = next((item for item in requirements if item["prd_id"] == prd_id), None)
    if target is None:
        raise UpdateError(f"target prd_id is not registered: {prd_id}")
    existing = existing_receipt_for_spec(root, prd_id, spec_hash)
    if existing is not None:
        verify_update(root, prd_id, str(existing["update_id"]))
        return {
            "schema_version": 1, "action": "plan", "changed": False, "apply_ready": True,
            "prd_id": prd_id, "old_version": existing["old_version"], "new_version": existing["new_version"],
            "spec_sha256": spec_hash, "existing_update_id": existing["update_id"], "module_changes": existing["module_changes"],
            "impact": existing["impact"], "dispositions": existing["dispositions"], "missing_dispositions": [],
        }
    if target["current_version"] != spec["expected_old_version"]:
        raise UpdateError(f"expected_old_version drift: spec={spec['expected_old_version']}, current={target['current_version']}")
    old_modules = {item["module_slug"]: item for item in target["modules"]}
    old_active = {slug for slug, item in old_modules.items() if item["status"] == "active"}
    old_removed = set(old_modules) - old_active
    final_items = {item["module_slug"]: item for item in spec["active_modules"]}
    final_slugs = set(final_items)
    removed = set(spec["removed_slugs"])
    if removed - old_active or removed & final_slugs:
        raise UpdateError("removed_slugs must name old active modules absent from final active_modules")
    if final_slugs & old_removed:
        raise UpdateError(f"removed module slugs cannot be resurrected: {sorted(final_slugs & old_removed)}")
    origin_usage: dict[str, int] = {}
    for item in final_items.values():
        for origin in item["origins"]:
            if origin not in old_active:
                raise UpdateError(f"module origin is not an old active slug: {origin}")
            origin_usage[origin] = origin_usage.get(origin, 0) + 1
    missing_old = old_active - final_slugs
    accounted_by_relation = set(origin_usage) & missing_old
    if missing_old != removed | accounted_by_relation or removed & accounted_by_relation:
        raise UpdateError("every disappearing old module must be covered exactly once by removed_slugs or origins")
    module_changes: list[dict[str, Any]] = []
    changed_slugs: set[str] = set()
    target_dir = prd_root / prd_id
    for slug in sorted(final_slugs):
        item = final_items[slug]
        origins = item["origins"]
        new_hash = sha256(sources[slug])
        if slug in old_active:
            if origins != [slug]:
                raise UpdateError(f"retained module must have origins=[itself]: {slug}")
            old = old_modules[slug]
            old_hash = sha256((target_dir / f"{slug}.md").read_bytes())
            title_changed = old["module_title"] != item["title"]
            content_changed = old_hash != new_hash
            kind = "updated" if content_changed else "renamed" if title_changed else "unchanged"
            old_title = old["module_title"]
        else:
            old_hash = None
            old_title = None
            if not origins:
                kind = "added"
            elif len(origins) > 1:
                kind = "merged"
            elif origin_usage[origins[0]] > 1 or origins[0] in final_slugs:
                kind = "split"
            else:
                raise UpdateError(f"one-to-one rename must preserve the old module_slug: {origins[0]} -> {slug}")
        change = {
            "module_slug": slug, "kind": kind, "origins": origins,
            "old_title": old_title, "new_title": item["title"], "old_sha256": old_hash, "new_sha256": new_hash,
        }
        module_changes.append(change)
        if kind != "unchanged":
            changed_slugs.add(slug)
            changed_slugs.update(origins)
    for slug in sorted(missing_old):
        old = old_modules[slug]
        module_changes.append({
            "module_slug": slug, "kind": "removed" if slug in removed else "replaced",
            "origins": [slug], "old_title": old["module_title"], "new_title": None,
            "old_sha256": sha256((target_dir / f"{slug}.md").read_bytes()), "new_sha256": None,
        })
        changed_slugs.add(slug)
    if not changed_slugs:
        return {
            "schema_version": 1, "action": "plan", "changed": False, "apply_ready": False,
            "prd_id": prd_id, "old_version": spec["expected_old_version"], "new_version": spec["new_version"],
            "spec_sha256": spec_hash, "module_changes": module_changes, "impact": [], "dispositions": [],
            "missing_dispositions": [], "reason": "no module content or title changes",
        }
    impact = impact_scan(root, prd_id, changed_slugs)
    dispositions, missing = disposition_report(spec, impact)
    source_files = [
        {"module_slug": slug, "locator": final_items[slug]["source"], "sha256": sha256(sources[slug])}
        for slug in sorted(final_slugs)
    ]
    return {
        "schema_version": 1, "action": "plan", "changed": True,
        "apply_ready": bool(spec["confirmed"] and not missing), "prd_id": prd_id,
        "old_version": spec["expected_old_version"], "new_version": spec["new_version"],
        "spec_path": str(spec_path), "spec_sha256": spec_hash,
        "pre_collection_tree_sha256": tree_hash(prd_root),
        "module_changes": module_changes, "impact": impact, "dispositions": dispositions,
        "missing_dispositions": missing, "source_files": source_files,
    }


def fail_at(point: str) -> None:
    if os.environ.get("BUTLER_PRD_UPDATE_FAIL_AT") == point:
        raise UpdateError(f"injected failure at {point}")


@contextlib.contextmanager
def update_lock(root: Path) -> Iterable[None]:
    path = root / ".ai/references/.prd-update.lock"
    if path.is_symlink():
        raise UpdateError("update lock path is a symlink")
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise UpdateError("another PRD update holds the lock") from error
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode())
        os.close(descriptor)
        yield
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    except BaseException:
        try:
            os.unlink(name)
        except FileNotFoundError:
            pass
        raise


def build_staged_tree(root: Path, plan: dict[str, Any], spec: dict[str, Any], sources: dict[str, bytes], stage_prd: Path, applied_at: str) -> dict[str, Any]:
    prd_root = root / ".ai/references/prd"
    shutil.copytree(prd_root, stage_prd)
    prd_id = plan["prd_id"]
    target = stage_prd / prd_id
    old_version = plan["old_version"]
    archive = target / ".archive" / old_version
    if archive.exists() or archive.is_symlink():
        raise UpdateError(f"archive version already exists: {prd_id}/.archive/{old_version}")
    archive.mkdir(parents=True)
    old_modules = status_contract.parse_modules(status_contract.read_file(target / "00_INDEX.md"), target)
    shutil.copy2(target / "00_INDEX.md", archive / "00_INDEX.md")
    for module in old_modules:
        shutil.copy2(target / f"{module['module_slug']}.md", archive / f"{module['module_slug']}.md")
    fail_at("after_archive")
    old_by_slug = {item["module_slug"]: item for item in old_modules}
    final_by_slug = {item["module_slug"]: item for item in spec["active_modules"]}
    new_rows: list[dict[str, str]] = []
    for slug, old in old_by_slug.items():
        if old["status"] == "removed":
            new_rows.append(old)
        elif slug not in final_by_slug:
            new_rows.append({**old, "current_version": plan["new_version"], "status": "removed"})
    for slug, item in final_by_slug.items():
        old = old_by_slug.get(slug)
        change = next(change for change in plan["module_changes"] if change["module_slug"] == slug and change["new_sha256"] is not None)
        new_rows.append({
            "module_slug": slug,
            "module_title": item["title"],
            "first_version": old["first_version"] if old else plan["new_version"],
            "current_version": old["current_version"] if change["kind"] == "unchanged" and old else plan["new_version"],
            "status": "active",
        })
        (target / f"{slug}.md").write_bytes(sources[slug])
    fail_at("after_live")
    index_path = target / "00_INDEX.md"
    index_path.write_text(render_requirement_index(index_path.read_text(encoding="utf-8"), plan["new_version"], new_rows), encoding="utf-8", newline="\n")
    project_index_path = stage_prd / "00_INDEX.md"
    project_index_path.write_text(render_project_index(project_index_path.read_text(encoding="utf-8"), prd_id, plan["new_version"]), encoding="utf-8", newline="\n")
    fail_at("after_index")
    status_contract.validate_no_symlinks(stage_prd)
    status_contract.collection_status(root, stage_prd)
    update_id = "UPD-" + hashlib.sha256(f"{plan['spec_sha256']}\0{plan['pre_collection_tree_sha256']}".encode()).hexdigest()[:12]
    receipt_relative = f"{prd_id}/.butler-updates/{update_id}.json"
    (stage_prd / prd_id / ".butler-updates").mkdir(parents=True, exist_ok=True)
    archive_hash = tree_hash(archive)
    post_hash = tree_hash(stage_prd, exclude={receipt_relative})
    receipt = {
        "schema_version": 1, "update_id": update_id, "prd_id": prd_id, "applied_at": applied_at,
        "old_version": plan["old_version"], "new_version": plan["new_version"],
        "spec_sha256": plan["spec_sha256"], "pre_collection_tree_sha256": plan["pre_collection_tree_sha256"],
        "post_collection_tree_sha256": post_hash,
        "archive_path": f".ai/references/prd/{prd_id}/.archive/{plan['old_version']}",
        "archive_tree_sha256": archive_hash,
        "backup": f".ai/references/.prd-update-backups/{update_id}",
        "module_changes": plan["module_changes"], "impact": plan["impact"],
        "dispositions": plan["dispositions"], "source_files": plan["source_files"],
        "confirmation": spec["confirmation"],
    }
    receipt["receipt_payload_sha256"] = sha256(canonical_json(receipt))
    atomic_json(stage_prd / receipt_relative, receipt)
    fail_at("after_receipt")
    if tree_hash(stage_prd, exclude={receipt_relative}) != post_hash:
        raise UpdateError("staged collection hash changed after receipt creation")
    return receipt


def verify_update(root: Path, prd_id: str, update_id: str | None = None) -> dict[str, Any]:
    path, receipt = read_receipt(root, prd_id, update_id)
    prd_root = root / ".ai/references/prd"
    status_contract.validate_no_symlinks(prd_root)
    receipt_relative = path.relative_to(prd_root).as_posix()
    expected_receipt = f"{prd_id}/.butler-updates/{receipt['update_id']}.json"
    if receipt_relative != expected_receipt:
        raise UpdateError("update receipt path is unsafe")
    backup_relative = Path(str(receipt["backup"]))
    archive_relative = Path(str(receipt["archive_path"]))
    if backup_relative.is_absolute() or ".." in backup_relative.parts or archive_relative.is_absolute() or ".." in archive_relative.parts:
        raise UpdateError("update receipt backup/archive path is unsafe")
    backup = root / backup_relative
    backup_root = root / ".ai/references/.prd-update-backups"
    if backup_root.is_symlink() or backup.is_symlink():
        raise UpdateError("update backup path is unsafe")
    try:
        if backup.resolve(strict=True).parent != backup_root.resolve(strict=True) or backup.name != receipt["update_id"]:
            raise UpdateError("update backup path escapes its managed root")
    except OSError as error:
        raise UpdateError("update backup is missing") from error
    if tree_hash(prd_root, exclude={receipt_relative}) != receipt["post_collection_tree_sha256"]:
        raise UpdateError("current collection no longer matches receipt post hash")
    if tree_hash(backup) != receipt["pre_collection_tree_sha256"]:
        raise UpdateError("update backup no longer matches receipt pre hash")
    archive = root / archive_relative
    expected_archive = prd_root / prd_id / ".archive" / str(receipt["old_version"])
    if archive.resolve(strict=True) != expected_archive.resolve(strict=True) or tree_hash(archive) != receipt["archive_tree_sha256"]:
        raise UpdateError("update archive path or hash drift")
    requirements = status_contract.collection_status(root, prd_root)
    target = next((item for item in requirements or [] if item["prd_id"] == prd_id), None)
    if target is None or target["current_version"] != receipt["new_version"]:
        raise UpdateError("updated target version does not match receipt")
    return {
        "schema_version": 1, "action": "verify", "verified": True,
        "update_id": receipt["update_id"], "prd_id": prd_id,
        "old_version": receipt["old_version"], "new_version": receipt["new_version"],
        "post_collection_tree_sha256": receipt["post_collection_tree_sha256"],
    }


def apply_update(root: Path, spec_path_value: str, applied_at: str) -> dict[str, Any]:
    try:
        dt.datetime.fromisoformat(applied_at)
    except ValueError as error:
        raise UpdateError("applied_at must be an ISO-8601 timestamp") from error
    with update_lock(root):
        plan = build_plan(root, spec_path_value)
        if not plan["changed"] and plan.get("existing_update_id"):
            return {"schema_version": 1, "action": "apply", "changed": False, **verify_update(root, plan["prd_id"], plan["existing_update_id"])}
        if not plan["changed"]:
            raise UpdateError("update spec has no material module changes")
        if not plan["apply_ready"]:
            raise UpdateError(f"update is not apply-ready; confirmed/dispositions missing: {plan['missing_dispositions']}")
        _, spec, sources, current_spec_hash = load_spec(spec_path_value)
        if current_spec_hash != plan["spec_sha256"]:
            raise UpdateError("update spec or source bytes drifted after plan")
        references = root / ".ai/references"
        prd_root = references / "prd"
        stage_container = Path(tempfile.mkdtemp(prefix=".prd-update-stage-", dir=references))
        stage_prd = stage_container / "prd"
        backup_root = references / ".prd-update-backups"
        created_backup_root = False
        backup: Path | None = None
        switched_old = False
        switched_new = False
        try:
            receipt = build_staged_tree(root, plan, spec, sources, stage_prd, applied_at)
            update_id = str(receipt["update_id"])
            if backup_root.is_symlink() or (backup_root.exists() and not backup_root.is_dir()):
                raise UpdateError("update backup root must be a real directory")
            if not backup_root.exists():
                backup_root.mkdir()
                created_backup_root = True
            backup = backup_root / update_id
            if backup.exists() or backup.is_symlink():
                raise UpdateError(f"update backup already exists: {update_id}")
            if tree_hash(prd_root) != plan["pre_collection_tree_sha256"]:
                raise UpdateError("collection drifted before transaction switch")
            os.replace(prd_root, backup)
            switched_old = True
            fail_at("after_first_rename")
            try:
                os.replace(stage_prd, prd_root)
                switched_new = True
                fail_at("after_second_rename")
                verify_update(root, plan["prd_id"], update_id)
            except BaseException:
                failed = references / f".prd-update-failed-{update_id}"
                if prd_root.exists():
                    os.replace(prd_root, failed)
                os.replace(backup, prd_root)
                switched_old = False
                switched_new = False
                if failed.exists():
                    shutil.rmtree(failed)
                raise
            return {
                "schema_version": 1, "action": "apply", "changed": True,
                "update_id": update_id, "prd_id": plan["prd_id"],
                "old_version": plan["old_version"], "new_version": plan["new_version"],
                "receipt": f".ai/references/prd/{plan['prd_id']}/.butler-updates/{update_id}.json",
                "backup": receipt["backup"],
            }
        finally:
            if switched_old and not prd_root.exists() and backup is not None and backup.exists():
                os.replace(backup, prd_root)
            if stage_container.exists():
                shutil.rmtree(stage_container)
            if created_backup_root and backup_root.exists() and not any(backup_root.iterdir()):
                backup_root.rmdir()


def rollback_update(root: Path, prd_id: str, update_id: str | None = None) -> dict[str, Any]:
    with update_lock(root):
        _, receipt = read_receipt(root, prd_id, update_id)
        verify_update(root, prd_id, str(receipt["update_id"]))
        references = root / ".ai/references"
        prd_root = references / "prd"
        backup = root / str(receipt["backup"])
        retired = references / f".prd-update-rollback-{receipt['update_id']}"
        if retired.exists() or retired.is_symlink():
            raise UpdateError("rollback temporary path already exists")
        os.replace(prd_root, retired)
        try:
            fail_at("rollback_after_first_rename")
            os.replace(backup, prd_root)
        except BaseException:
            os.replace(retired, prd_root)
            raise
        shutil.rmtree(retired)
        backup_root = references / ".prd-update-backups"
        if backup_root.is_dir() and not any(backup_root.iterdir()):
            backup_root.rmdir()
        return {
            "schema_version": 1, "action": "rollback", "changed": True,
            "update_id": receipt["update_id"], "prd_id": prd_id,
            "restored_version": receipt["old_version"],
        }


def parser() -> argparse.ArgumentParser:
    root = UpdateArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="action", required=True)
    for action in ("plan", "apply"):
        command = sub.add_parser(action)
        command.add_argument("--project-root", required=True)
        command.add_argument("--spec", required=True)
        if action == "apply":
            command.add_argument("--now", help=argparse.SUPPRESS)
    for action in ("verify", "rollback"):
        command = sub.add_parser(action)
        command.add_argument("--project-root", required=True)
        command.add_argument("--prd-id", required=True)
        command.add_argument("--update-id")
    return root


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def main(argv: Iterable[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        root = resolve_root(args.project_root)
        if args.action == "plan":
            result = build_plan(root, args.spec)
            code = 0 if result["changed"] and result["apply_ready"] else 1
        elif args.action == "apply":
            now = args.now or dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
            result = apply_update(root, args.spec, now)
            code = 0
        elif args.action == "verify":
            result = verify_update(root, args.prd_id, args.update_id)
            code = 0
        else:
            result = rollback_update(root, args.prd_id, args.update_id)
            code = 0
        emit(result)
        return code
    except (UpdateError, status_contract.StatusError, OSError, UnicodeError, json.JSONDecodeError) as error:
        emit({"schema_version": SCHEMA_VERSION, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
