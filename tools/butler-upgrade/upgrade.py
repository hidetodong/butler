#!/usr/bin/env python3
"""Plan and transactionally apply Butler project upgrades."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXIT_INVALID = 2
EXIT_DECISION = 3
EXIT_LOCKED = 4
EXIT_RESTORED = 5
EXIT_EXTERNAL = 6
STAMP_RE = re.compile(r"规则源：butler v(\d+\.\d+\.\d+)")
MANAGED_START = "<!-- butler-managed:start -->"
MANAGED_END = "<!-- butler-managed:end -->"
USER_START = "<!-- user-managed -->"
USER_END = "<!-- /user-managed -->"
ACTION_DOMAINS = {
    "regen_entrypoints": "project",
    "sync_hooks": "project",
    "rename": "project",
    "add_field": "project",
    "restamp": "project",
    "no_op": "project",
    "split": "decision",
    "global_install": "machine",
}
ACTION_KEYS = {
    "regen_entrypoints": set(),
    "sync_hooks": set(),
    "rename": {"from", "to"},
    "add_field": {"path", "section", "key", "value"},
    "restamp": set(),
    "no_op": set(),
    "split": set(),
    "global_install": set(),
}
ACTION_PRECONDITIONS = {
    "regen_entrypoints": ["entrypoint-markers-valid"],
    "sync_hooks": ["hook-tree-recognized-or-absent", "settings-shape-valid"],
    "rename": ["source-destination-shape-valid", "target-path-owned"],
    "add_field": ["target-path-owned", "field-shape-valid"],
    "restamp": ["entrypoint-markers-valid"],
    "no_op": [],
    "split": ["project-knowledge-shape-valid", "explicit-split-decision"],
    "global_install": ["explicit-machine-confirmation"],
}
COMMON_ACTION_KEYS = {"id", "type", "domain", "preconditions"}


class UpgradeError(ValueError):
    def __init__(self, message: str, *, code: int = EXIT_INVALID, status: str = "conflict"):
        super().__init__(message)
        self.code = code
        self.status = status


@dataclass(frozen=True)
class Change:
    path: Path
    operation: str
    content: bytes | None = None
    mode: int = 0o644
    source: Path | None = None


def semver(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise UpgradeError(f"invalid semantic version: {value}")
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise UpgradeError(f"cannot read JSON {path}: {error}") from error


def validate_manifest(data: Any, butler_root: Path) -> dict[str, Any]:
    if not isinstance(data, dict) or set(data) - {
        "schema_version", "baseline_version", "migrations", "known_hook_tree_digests"
    }:
        raise UpgradeError("manifest has unknown or invalid top-level fields")
    if data.get("schema_version") != 1:
        raise UpgradeError("manifest schema_version must be 1")
    baseline = data.get("baseline_version")
    semver(baseline)
    migrations = data.get("migrations")
    if not isinstance(migrations, list) or not migrations:
        raise UpgradeError("manifest migrations must be a non-empty array")
    expected_source = baseline
    ids: set[str] = set()
    recipes: set[str] = set()
    last_target = semver(baseline)
    for migration in migrations:
        if not isinstance(migration, dict) or set(migration) != {
            "source", "target", "recipe", "actions"
        }:
            raise UpgradeError("migration must contain only source/target/recipe/actions")
        source, target, recipe = (
            migration.get("source"), migration.get("target"), migration.get("recipe")
        )
        if source != expected_source:
            raise UpgradeError(f"migration chain break: expected source {expected_source}, got {source}")
        target_key = semver(target)
        if target_key <= last_target:
            raise UpgradeError(f"migration targets are not strictly increasing: {target}")
        if recipe != f"v{target}.md" or not (butler_root / "migrations" / recipe).is_file():
            raise UpgradeError(f"missing or mismatched recipe for {target}: {recipe}")
        actions = migration.get("actions")
        if not isinstance(actions, list) or not actions:
            raise UpgradeError(f"migration {target} has no actions")
        for action in actions:
            if not isinstance(action, dict):
                raise UpgradeError(f"migration {target} contains a non-object action")
            action_type = action.get("type")
            if action_type not in ACTION_DOMAINS:
                raise UpgradeError(f"unknown action type: {action_type}")
            allowed = COMMON_ACTION_KEYS | ACTION_KEYS[action_type]
            if set(action) != allowed:
                raise UpgradeError(f"invalid fields for action {action.get('id')}: {sorted(set(action) ^ allowed)}")
            action_id = action.get("id")
            if not isinstance(action_id, str) or not action_id.startswith(f"{target}/") or action_id in ids:
                raise UpgradeError(f"invalid or duplicate action id: {action_id}")
            if action.get("domain") != ACTION_DOMAINS[action_type]:
                raise UpgradeError(f"invalid domain for action {action_id}")
            if action.get("preconditions") != ACTION_PRECONDITIONS[action_type]:
                raise UpgradeError(f"invalid preconditions for action {action_id}")
            for field in ACTION_KEYS[action_type]:
                if not isinstance(action.get(field), str) or not action[field]:
                    raise UpgradeError(f"action {action_id} requires non-empty {field}")
            if action_type in {"rename", "add_field"}:
                for field in ({"from", "to"} if action_type == "rename" else {"path"}):
                    validate_owned_action_path(action_type, safe_relative(action[field]))
            ids.add(action_id)
        recipes.add(recipe)
        expected_source = target
        last_target = target_key
    markdown_recipes = {path.name for path in (butler_root / "migrations").glob("v*.md")}
    if recipes != markdown_recipes:
        raise UpgradeError(
            f"manifest/Markdown recipe mismatch: missing={sorted(markdown_recipes-recipes)}, extra={sorted(recipes-markdown_recipes)}"
        )
    digests = data.get("known_hook_tree_digests", [])
    if not isinstance(digests, list) or any(not re.fullmatch(r"[0-9a-f]{64}", x or "") for x in digests):
        raise UpgradeError("known_hook_tree_digests must be SHA-256 strings")
    return data


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts or path == Path("."):
        raise UpgradeError(f"unsafe project-relative path: {value}")
    return path


def validate_owned_action_path(action_type: str, path: Path) -> None:
    if action_type == "add_field" and path != Path(".ai/local-constraints.md"):
        raise UpgradeError(f"add_field path is not owned by the upgrader: {path}")
    if action_type == "rename":
        if not path.parts or path.parts[0] != ".ai":
            raise UpgradeError(f"rename path must stay under .ai/: {path}")
        protected = {"iterations", "milestones", "references", "verification-evidence", "butler-upgrade"}
        if len(path.parts) > 1 and path.parts[1] in protected:
            raise UpgradeError(f"rename path targets protected project state: {path}")


def load_renderer(butler_root: Path):
    path = butler_root / "scripts" / "render-project-entrypoints.py"
    spec = importlib.util.spec_from_file_location("butler_entrypoint_renderer", path)
    if not spec or not spec.loader:
        raise UpgradeError("cannot load entrypoint renderer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def resolve_roots(project_arg: str, butler_root: Path) -> tuple[Path, Path]:
    butler_root = butler_root.expanduser().resolve()
    project = Path(project_arg).expanduser().resolve()
    if not project.is_dir():
        raise UpgradeError(f"project root is not an existing directory: {project}")
    if project == butler_root or butler_root in project.parents:
        raise UpgradeError("refusing to upgrade Butler itself or a path inside Butler")
    if not (project / ".ai").is_dir():
        raise UpgradeError("target is not a deployed Butler project: missing .ai/")
    return project, butler_root


def validate_entrypoint(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.is_symlink():
        raise UpgradeError(f"entrypoint may not be a symlink: {path.name}")
    text = path.read_text(encoding="utf-8")
    outer = (text.count(MANAGED_START), text.count(MANAGED_END))
    user = (text.count(USER_START), text.count(USER_END))
    if outer not in {(0, 0), (1, 1)} or user not in {(0, 0), (1, 1)}:
        raise UpgradeError(f"invalid markers in {path.name}")
    if outer == (1, 1) and text.index(MANAGED_START) > text.index(MANAGED_END):
        raise UpgradeError(f"out-of-order managed markers in {path.name}")
    if user == (1, 1) and text.index(USER_START) > text.index(USER_END):
        raise UpgradeError(f"out-of-order user markers in {path.name}")
    stamps = STAMP_RE.findall(text)
    if len(stamps) > 1:
        raise UpgradeError(f"multiple Butler version stamps in {path.name}")
    if stamps and outer == (0, 0) and user != (1, 1):
        raise UpgradeError(f"unmanaged Butler signature is ambiguous in {path.name}")
    return stamps[0] if stamps else None


def deployed_version(project: Path, current: str, manifest: dict[str, Any]) -> tuple[str | None, str]:
    claude = validate_entrypoint(project / "CLAUDE.md")
    agents = validate_entrypoint(project / "AGENTS.md")
    stamps = {value for value in (claude, agents) if value}
    if len(stamps) > 1:
        raise UpgradeError(f"entrypoint version drift: CLAUDE={claude}, AGENTS={agents}")
    if not stamps:
        return None, "manual-bootstrap"
    version = stamps.pop()
    known = {manifest["baseline_version"]}
    known.update(item["target"] for item in manifest["migrations"])
    if semver(version) > semver(current):
        raise UpgradeError(f"project version {version} is newer than Butler {current}")
    if version not in known:
        raise UpgradeError(f"project version is outside the supported migration chain: {version}")
    return version, "stamped"


def contained_target(project: Path, relative: Path) -> Path:
    target = project / relative
    cursor = project
    for part in relative.parts[:-1]:
        cursor = cursor / part
        if cursor.is_symlink():
            raise UpgradeError(f"symlink directory escapes ownership boundary: {cursor.relative_to(project)}")
    if target.is_symlink():
        raise UpgradeError(f"symlink target is not writable by upgrader: {relative}")
    try:
        target.parent.resolve().relative_to(project)
    except ValueError as error:
        raise UpgradeError(f"path escapes project root: {relative}") from error
    return target


def hook_source_files(butler_root: Path) -> dict[Path, bytes]:
    root = butler_root / "templates" / "hooks"
    result: dict[Path, bytes] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_file() or path.is_symlink():
            continue
        if "tests" in rel.parts or "__pycache__" in rel.parts or ".pytest_cache" in rel.parts:
            continue
        if path.suffix == ".pyc":
            continue
        result[rel] = path.read_bytes()
    return result


def tree_digest(files: dict[Path, bytes]) -> str:
    digest = hashlib.sha256()
    for path, content in sorted(files.items(), key=lambda item: item[0].as_posix()):
        digest.update(path.as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


def target_hook_files(project: Path) -> dict[Path, bytes]:
    root = project / ".claude" / "hooks"
    if not root.exists():
        return {}
    if root.is_symlink():
        raise UpgradeError(".claude/hooks may not be a symlink")
    result: dict[Path, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise UpgradeError(f"hook symlink is not owned: {path.relative_to(project)}")
        if path.is_file():
            rel = path.relative_to(root)
            if "__pycache__" in rel.parts or ".pytest_cache" in rel.parts or path.suffix == ".pyc":
                continue
            result[rel] = path.read_bytes()
    return result


def merge_settings(existing: bytes | None, snippet_path: Path) -> bytes:
    try:
        data = json.loads(existing.decode("utf-8")) if existing else {}
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise UpgradeError(f"invalid .claude/settings.json: {error}") from error
    if not isinstance(data, dict):
        raise UpgradeError(".claude/settings.json must contain an object")
    snippet = read_json(snippet_path)
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise UpgradeError("settings hooks must be an object")
    for event, entries in snippet["hooks"].items():
        current = hooks.setdefault(event, [])
        if not isinstance(current, list):
            raise UpgradeError(f"settings hooks.{event} must be an array")
        wanted_name = "butler_gate.py" if event == "PreToolUse" else "butler_advisor.py"
        found = False
        for entry in current:
            if not isinstance(entry, dict):
                raise UpgradeError(f"settings hooks.{event} contains a non-object entry")
            commands = entry.get("hooks", [])
            if entry.get("matcher") == "Edit|Write|MultiEdit" and isinstance(commands, list):
                found = any(
                    isinstance(item, dict)
                    and isinstance(item.get("command"), str)
                    and item["command"].endswith(wanted_name)
                    for item in commands
                )
            if found:
                break
        if not found:
            current.extend(entries)
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def add_field_content(existing: bytes, action: dict[str, Any]) -> bytes:
    text = existing.decode("utf-8")
    key_re = re.compile(rf"(?m)^\s*-\s*{re.escape(action['key'])}\s*:\s*(\S.*)$")
    match = key_re.search(text)
    if match:
        return existing
    heading = f"# {action['section']}"
    pos = text.find(heading)
    if pos < 0:
        separator = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        text += f"{separator}{heading}\n\n- {action['key']}: {action['value']}\n"
    else:
        line_end = text.find("\n", pos)
        insert = len(text) if line_end < 0 else line_end + 1
        text = text[:insert] + f"\n- {action['key']}: {action['value']}\n" + text[insert:]
    return text.encode("utf-8")


def build_plan(project: Path, butler_root: Path, split_choice: str | None) -> dict[str, Any]:
    project = project.resolve()
    butler_root = butler_root.resolve()
    if project == butler_root or butler_root in project.parents:
        raise UpgradeError("refusing to upgrade Butler itself or a path inside Butler")
    lock = project / ".ai" / "butler-upgrade" / "apply.lock"
    if lock.exists():
        raise UpgradeError(
            "an apply lock exists; inspect its run before planning another upgrade",
            code=EXIT_LOCKED,
            status="locked",
        )
    manifest = validate_manifest(read_json(butler_root / "migrations" / "manifest.json"), butler_root)
    current = (butler_root / "VERSION").read_text(encoding="utf-8").strip()
    from_version, deployment = deployed_version(project, current, manifest)
    result: dict[str, Any] = {
        "status": "ready",
        "project_root": str(project),
        "from_version": from_version,
        "to_version": current,
        "deployment": deployment,
        "actions": [],
        "changes": [],
        "conflicts": [],
        "external_pending": [],
        "run_id": None,
        "_planned": [],
    }
    if from_version is None:
        result["status"] = "manual-bootstrap"
        result["conflicts"].append("no Butler version stamp; use initial deployment/manual bootstrap")
        return result
    queue = [
        item for item in manifest["migrations"]
        if semver(from_version) < semver(item["target"]) <= semver(current)
    ]
    actions = [dict(action, migration=item["target"]) for item in queue for action in item["actions"]]
    result["actions"] = actions
    if not queue:
        renderer = load_renderer(butler_root)
        drifted = [
            item.path.name for item in renderer.plan(project, butler_root)
            if not item.path.exists() or item.path.read_text(encoding="utf-8") != item.content
        ]
        if drifted:
            raise UpgradeError(f"current-version entrypoint content drift: {', '.join(drifted)}")
        existing_hooks = target_hook_files(project)
        current_hooks = hook_source_files(butler_root)
        if existing_hooks and tree_digest(existing_hooks) != tree_digest(current_hooks):
            raise UpgradeError("current-version hook content drift")
        result["status"] = "already-current"
        return result

    has_split = any(action["type"] == "split" for action in actions)
    old_project = project / ".ai" / "PROJECT.md"
    index = project / ".ai" / "project" / "00_INDEX.md"
    project_dir = project / ".ai" / "project"
    partial = project_dir.exists() and any(project_dir.iterdir()) and not index.exists()
    if partial or (old_project.exists() and index.exists()):
        raise UpgradeError("split target is partially formed or conflicts with .ai/PROJECT.md")
    if has_split and old_project.exists() and not index.exists():
        if split_choice is None:
            result["status"] = "needs-decision"
            result["conflicts"].append("split decision required: choose defer or now")
            return result
        if split_choice == "now":
            result["status"] = "manual-split"
            result["conflicts"].append("semantic split requires a supervised handoff; project remains unchanged")
            return result

    changes: dict[Path, Change] = {}
    def plan_write(rel: Path, content: bytes, mode: int = 0o644) -> None:
        path = contained_target(project, rel)
        current_bytes = path.read_bytes() if path.exists() else None
        if current_bytes != content:
            changes[rel] = Change(path, "write", content, mode)
    def plan_delete(rel: Path) -> None:
        path = contained_target(project, rel)
        if path.exists():
            changes[rel] = Change(path, "delete")

    if any(action["type"] in {"regen_entrypoints", "restamp"} for action in actions):
        renderer = load_renderer(butler_root)
        for item in renderer.plan(project, butler_root):
            plan_write(item.path.relative_to(project), item.content.encode("utf-8"),
                       (item.path.stat().st_mode & 0o777) if item.path.exists() else 0o644)

    for action in actions:
        if action["type"] == "add_field":
            rel = safe_relative(action["path"])
            path = contained_target(project, rel)
            existing = path.read_bytes() if path.exists() else b""
            plan_write(rel, add_field_content(existing, action),
                       (path.stat().st_mode & 0o777) if path.exists() else 0o644)
        elif action["type"] == "rename":
            old_rel, new_rel = safe_relative(action["from"]), safe_relative(action["to"])
            old, new = contained_target(project, old_rel), contained_target(project, new_rel)
            if old.exists() and new.exists():
                raise UpgradeError(f"rename conflict: both {old_rel} and {new_rel} exist")
            if old.exists():
                plan_write(new_rel, old.read_bytes(), old.stat().st_mode & 0o777)
                plan_delete(old_rel)

    if any(action["type"] == "sync_hooks" for action in actions):
        source = hook_source_files(butler_root)
        existing = target_hook_files(project)
        known = set(manifest.get("known_hook_tree_digests", [])) | {tree_digest(source)}
        if existing and tree_digest(existing) not in known:
            raise UpgradeError("target hook tree is not a recognized Butler-managed version; refusing overwrite")
        for rel, content in source.items():
            source_path = butler_root / "templates" / "hooks" / rel
            plan_write(Path(".claude/hooks") / rel, content, source_path.stat().st_mode & 0o777)
        for rel in set(existing) - set(source):
            plan_delete(Path(".claude/hooks") / rel)
        settings_rel = Path(".claude/settings.json")
        settings = contained_target(project, settings_rel)
        plan_write(settings_rel, merge_settings(
            settings.read_bytes() if settings.exists() else None,
            butler_root / "templates" / "settings.hooks-snippet.json",
        ), (settings.stat().st_mode & 0o777) if settings.exists() else 0o644)

    external = [action["id"] for action in actions if action["domain"] == "machine"]
    result["external_pending"] = external
    ordered = sorted(changes.items(), key=lambda item: item[0].as_posix())
    result["_planned"] = [change for _, change in ordered]
    result["changes"] = [
        {
            "path": rel.as_posix(),
            "operation": change.operation,
            "before_sha256": sha256(change.path.read_bytes()) if change.path.exists() else None,
            "after_sha256": sha256(change.content) if change.content is not None else None,
        }
        for rel, change in ordered
    ]
    result["status"] = "ready-with-external-pending" if external else "ready"
    return result


def public_result(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if not key.startswith("_")}


def atomic_write(path: Path, content: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.chmod(temp, mode)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def apply_plan(result: dict[str, Any], project: Path) -> dict[str, Any]:
    project = project.resolve()
    if result["status"] in {"already-current"}:
        return result
    if not result["status"].startswith("ready"):
        raise UpgradeError("plan is not applicable", code=EXIT_DECISION, status=result["status"])
    changes: list[Change] = result["_planned"]
    if not changes:
        result["status"] = "applied-external-pending" if result["external_pending"] else "already-current"
        return result
    expected = {item["path"]: item["before_sha256"] for item in result["changes"]}
    for change in changes:
        rel = change.path.relative_to(project).as_posix()
        actual = sha256(change.path.read_bytes()) if change.path.exists() else None
        if actual != expected[rel]:
            raise UpgradeError(f"target changed after planning: {rel}")
    state_root = project / ".ai" / "butler-upgrade"
    lock = state_root / "apply.lock"
    state_root.mkdir(parents=True, exist_ok=True)
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise UpgradeError("another apply is active or left an unresolved lock", code=EXIT_LOCKED, status="locked") from error
    run_id = f"{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:8]}"
    run_dir = state_root / "runs" / run_id
    backup_dir = run_dir / "backup"
    restore: list[dict[str, Any]] = []
    journal = {
        **public_result(result), "run_id": run_id, "status": "applying",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        with os.fdopen(lock_fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"pid": os.getpid(), "run_id": run_id}) + "\n")
        run_dir.mkdir(parents=True)
        for change in changes:
            rel = change.path.relative_to(project)
            existed = change.path.exists()
            before = change.path.read_bytes() if existed else None
            mode = (change.path.stat().st_mode & 0o777) if existed else None
            if existed:
                backup = backup_dir / rel
                backup.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(backup, before or b"", mode or 0o644)
            restore.append({
                "path": rel.as_posix(), "existed": existed, "mode": mode,
                "before_sha256": sha256(before) if before is not None else None,
                "after_sha256": sha256(change.content) if change.content is not None else None,
            })
        atomic_write(run_dir / "restore.json", (json.dumps(restore, indent=2) + "\n").encode(), 0o600)
        atomic_write(run_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode(), 0o600)
    except Exception as error:
        try:
            os.close(lock_fd)
        except OSError:
            pass
        lock.unlink(missing_ok=True)
        raise UpgradeError(
            f"cannot prepare upgrade transaction; no target files changed: {error}",
            code=EXIT_RESTORED,
            status="prepare-failed",
        ) from error
    fail_after = int(os.environ.get("BUTLER_UPGRADE_FAIL_AFTER", "0"))
    touched = 0
    try:
        for change in changes:
            if change.operation == "write":
                atomic_write(change.path, change.content or b"", change.mode)
            else:
                change.path.unlink()
            touched += 1
            if fail_after and touched >= fail_after:
                raise OSError(f"injected failure after {touched} changes")
        journal["status"] = "applied-external-pending" if result["external_pending"] else "applied"
        journal["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        atomic_write(run_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode(), 0o600)
        result["status"] = journal["status"]
        result["run_id"] = run_id
        return result
    except Exception as error:
        restore_errors: list[str] = []
        for item in reversed(restore[:touched]):
            path = contained_target(project, Path(item["path"]))
            try:
                if item["existed"]:
                    backup = backup_dir / item["path"]
                    atomic_write(path, backup.read_bytes(), item["mode"] or 0o644)
                elif path.exists():
                    path.unlink()
            except Exception as restore_error:  # pragma: no cover - catastrophic path
                restore_errors.append(f"{item['path']}: {restore_error}")
        journal["status"] = "restore-failed" if restore_errors else "failed-restored"
        journal["error"] = str(error)
        journal["restore_errors"] = restore_errors
        journal["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        atomic_write(run_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode(), 0o600)
        raise UpgradeError(
            f"apply failed; {'restore also failed: ' + '; '.join(restore_errors) if restore_errors else 'all project files restored'}",
            code=EXIT_RESTORED, status=journal["status"],
        ) from error
    finally:
        lock.unlink(missing_ok=True)


def global_install(butler_root: Path, confirm: bool) -> dict[str, Any]:
    if not confirm:
        raise UpgradeError("global-install requires --confirm", code=EXIT_DECISION, status="needs-confirmation")
    process = subprocess.run(["bash", str(butler_root / "scripts" / "setup.sh")], cwd=butler_root)
    if process.returncode:
        raise UpgradeError("global installer failed", code=EXIT_EXTERNAL, status="external-failed")
    return {"status": "external-applied", "project_root": None, "from_version": None,
            "to_version": (butler_root / "VERSION").read_text().strip(), "actions": [],
            "changes": [], "conflicts": [], "external_pending": [], "run_id": None}


def emit(result: dict[str, Any], as_json: bool) -> None:
    result = public_result(result)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"status: {result['status']}")
    if result.get("project_root"):
        print(f"project: {result['project_root']}")
        print(f"version: {result.get('from_version') or 'unversioned'} -> {result.get('to_version')}")
    for action in result.get("actions", []):
        print(f"action: {action['id']} [{action['domain']}] {action['type']}")
    for change in result.get("changes", []):
        print(f"change: {change['operation']} {change['path']}")
    for conflict in result.get("conflicts", []):
        print(f"conflict: {conflict}")
    for action_id in result.get("external_pending", []):
        print(f"external-pending: {action_id}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--butler-root", type=Path, default=Path(__file__).resolve().parents[2])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "plan", "apply"):
        child = sub.add_parser(name)
        child.add_argument("--project-root", required=True)
        child.add_argument("--json", action="store_true")
        if name in {"plan", "apply"}:
            child.add_argument("--split", choices=("defer", "now"), required=name == "apply")
    external = sub.add_parser("global-install")
    external.add_argument("--project-root", required=True)
    external.add_argument("--confirm", action="store_true")
    external.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        project, butler_root = resolve_roots(args.project_root, args.butler_root)
        if args.command == "global-install":
            result = global_install(butler_root, args.confirm)
            result["project_root"] = str(project)
        else:
            result = build_plan(project, butler_root, getattr(args, "split", None))
            if args.command == "apply":
                result = apply_plan(result, project)
        emit(result, args.json)
        if result["status"] in {"needs-decision", "manual-split", "manual-bootstrap"}:
            return EXIT_DECISION
        return 0
    except UpgradeError as error:
        result = {"status": error.status, "error": str(error)}
        if getattr(args, "json", False):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"butler-upgrade: {error}", file=sys.stderr)
        return error.code


if __name__ == "__main__":
    raise SystemExit(main())
