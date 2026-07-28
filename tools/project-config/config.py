#!/usr/bin/env python3
"""Strict reader and atomic writer for project-local Butler configuration."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn


SCHEMA_VERSION = 1
CONFIG_RELATIVE_PATH = Path(".ai/butler.config.json")
LEGACY_RELATIVE_PATH = Path(".ai/local-constraints.md")
FIELDS = (
    "schema_version",
    "dangerous",
    "independent_review",
    "preference",
    "profiles",
)
BOOLEAN_FIELDS = ("dangerous", "independent_review", "preference")
DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "dangerous": False,
    "independent_review": False,
    "preference": True,
    "profiles": [],
}
LEGACY_HEADINGS = (
    "Project Type",
    "Active Profiles",
    "Local Constraints",
    "Scope Exceptions",
    "External References",
    "Butler 功能开关",
    "Review Policy",
)
MACHINE_HEADINGS = {"Active Profiles", "Butler 功能开关", "Review Policy"}
PROFILE_RE = re.compile(r"[a-z0-9][a-z0-9._-]*")


@dataclass(frozen=True)
class ConfigError(Exception):
    code: str
    message: str
    exit_code: int = 2


def _fail(code: str, message: str, exit_code: int = 2) -> NoReturn:
    raise ConfigError(code, message, exit_code)


def default_config() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "dangerous": False,
        "independent_review": False,
        "preference": True,
        "profiles": [],
    }


def resolve_paths(project_root: str | Path) -> tuple[Path, Path]:
    raw = Path(project_root)
    try:
        root = raw.resolve(strict=True)
    except (OSError, RuntimeError):
        _fail("invalid_project_root", f"project root does not exist: {raw}")
    if not root.is_dir():
        _fail("invalid_project_root", f"project root is not a directory: {raw}")

    ai_dir = root / ".ai"
    if ai_dir.is_symlink() or not ai_dir.is_dir():
        _fail("invalid_ai_directory", f"expected a real .ai directory under: {root}")
    return root, ai_dir / "butler.config.json"


def _legacy_path(project_root: str | Path) -> tuple[Path, Path]:
    root, _ = resolve_paths(project_root)
    path = root / LEGACY_RELATIVE_PATH
    if path.is_symlink():
        _fail("unsafe_legacy_path", f"legacy configuration must not be a symlink: {path}")
    if path.exists() and not path.is_file():
        _fail("unsafe_legacy_path", f"legacy configuration must be a regular file: {path}")
    return root, path


def _sections(text: str) -> dict[str, tuple[int, int, int]]:
    wanted = set(LEGACY_HEADINGS)
    boundaries = [
        match
        for match in re.finditer(r"(?m)^# ([^\r\n]+)[ \t]*(?:\r?\n|$)", text)
        if not match.group(1).strip().startswith("项目级 butler 持久模式开关")
    ]
    sections: dict[str, tuple[int, int, int]] = {}
    for index, match in enumerate(boundaries):
        heading = match.group(1).strip()
        if heading not in wanted:
            continue
        if heading in sections:
            _fail("ambiguous_legacy", f"duplicate legacy section: {heading}")
        end = boundaries[index + 1].start() if index + 1 < len(boundaries) else len(text)
        sections[heading] = (match.start(), match.end(), end)
    return sections


def _section_lines(text: str, section: tuple[int, int, int]) -> list[str]:
    _, body_start, end = section
    return text[body_start:end].splitlines()


def _bullet_values(lines: list[str], heading: str) -> list[str]:
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--") or stripped.startswith("# "):
            continue
        match = re.fullmatch(r"-\s+(.+?)\s*", stripped)
        if not match:
            _fail("ambiguous_legacy", f"unsupported content in legacy {heading}: {stripped}")
        values.append(match.group(1))
    return values


def _parse_profiles(values: list[str]) -> list[str]:
    if not values:
        return []
    if len(values) == 1 and values[0].lstrip().startswith("无"):
        return []
    profiles: list[str] = []
    for value in values:
        candidate = value.strip()
        if candidate.startswith("`") and candidate.endswith("`") and candidate.count("`") == 2:
            candidate = candidate[1:-1]
        if not PROFILE_RE.fullmatch(candidate):
            _fail("ambiguous_legacy", f"ambiguous Active Profiles entry: {value}")
        profiles.append(candidate)
    if len(set(profiles)) != len(profiles):
        _fail("duplicate_profile", "legacy Active Profiles contains duplicates")
    return profiles


def _parse_switches(values: list[str], heading: str) -> dict[str, bool]:
    result: dict[str, bool] = {}
    allowed = set(BOOLEAN_FIELDS)
    if heading == "Review Policy":
        allowed = {"independent_review"}
    for value in values:
        match = re.fullmatch(
            r"(dangerous|independent_review|preference)\s*:\s*(on|off)(?:\s+#.*)?",
            value,
        )
        if not match or match.group(1) not in allowed:
            _fail("ambiguous_legacy", f"invalid legacy switch entry: {value}")
        key, raw = match.groups()
        if key in result:
            _fail("ambiguous_legacy", f"duplicate legacy switch: {key}")
        result[key] = raw == "on"
    return result


def parse_legacy(text: str) -> tuple[dict[str, Any], bool]:
    sections = _sections(text)
    config = default_config()
    has_legacy = any(heading in sections for heading in MACHINE_HEADINGS)
    if "Active Profiles" in sections:
        config["profiles"] = _parse_profiles(
            _bullet_values(_section_lines(text, sections["Active Profiles"]), "Active Profiles")
        )
    switches: dict[str, bool] = {}
    if "Butler 功能开关" in sections:
        switches.update(
            _parse_switches(
                _bullet_values(
                    _section_lines(text, sections["Butler 功能开关"]),
                    "Butler 功能开关",
                ),
                "Butler 功能开关",
            )
        )
    if "Review Policy" in sections:
        review_switches = _parse_switches(
            _bullet_values(_section_lines(text, sections["Review Policy"]), "Review Policy"),
            "Review Policy",
        )
        review_value = review_switches.get("independent_review")
        if (
            review_value is not None
            and "independent_review" in switches
            and switches["independent_review"] != review_value
        ):
            _fail(
                "ambiguous_legacy",
                "conflicting independent_review values in legacy sections",
            )
        switches.update(review_switches)
    config.update(switches)
    return validate(config), has_legacy


def read_legacy(project_root: str | Path) -> tuple[dict[str, Any], bool, Path, str | None]:
    _, path = _legacy_path(project_root)
    if not path.exists():
        return default_config(), False, path, None
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        _fail("invalid_legacy_encoding", "legacy configuration must be UTF-8")
    config, has_legacy = parse_legacy(text)
    return config, has_legacy, path, text


def read_compatible(
    project_root: str | Path,
) -> tuple[dict[str, Any], str, Path, list[str]]:
    config, source, path = read(project_root)
    legacy, has_legacy, _, _ = read_legacy(project_root)
    if source == "config":
        conflicts = [field for field in FIELDS[1:] if has_legacy and config[field] != legacy[field]]
        return config, source, path, conflicts
    if has_legacy:
        return legacy, "legacy", path, []
    return config, source, path, []


def strip_legacy_machine_sections(text: str) -> str:
    sections = _sections(text)
    ranges = sorted(
        (sections[heading][0], sections[heading][2])
        for heading in MACHINE_HEADINGS
        if heading in sections
    )
    for start, end in reversed(ranges):
        text = text[:start] + text[end:]
    return text


def plan_migration(project_root: str | Path) -> dict[Path, bytes]:
    config, source, config_path = read(project_root)
    legacy, has_legacy, legacy_path, legacy_text = read_legacy(project_root)
    if source == "config" and has_legacy:
        conflicts = [field for field in FIELDS[1:] if config[field] != legacy[field]]
        if conflicts:
            _fail("legacy_conflict", f"JSON and legacy configuration conflict: {', '.join(conflicts)}")
    chosen = config if source == "config" else legacy
    changes: dict[Path, bytes] = {}
    if source == "missing":
        changes[CONFIG_RELATIVE_PATH] = _encoded(chosen)
    if has_legacy and legacy_text is not None:
        stripped = strip_legacy_machine_sections(legacy_text).encode("utf-8")
        if stripped != legacy_text.encode("utf-8"):
            changes[LEGACY_RELATIVE_PATH] = stripped
    return changes


def validate(config: Any) -> dict[str, Any]:
    if not isinstance(config, dict):
        _fail("invalid_type", "configuration root must be an object")

    missing = [field for field in FIELDS if field not in config]
    if missing:
        _fail("missing_field", f"missing required field(s): {', '.join(missing)}")

    unknown = sorted(set(config) - set(FIELDS))
    if unknown:
        _fail("unknown_field", f"unknown field(s): {', '.join(unknown)}")

    version = config["schema_version"]
    if type(version) is not int:
        _fail("invalid_type", "schema_version must be an integer")
    if version != SCHEMA_VERSION:
        _fail("unsupported_schema", f"unsupported schema_version: {version}")

    for field in BOOLEAN_FIELDS:
        if type(config[field]) is not bool:
            _fail("invalid_type", f"{field} must be a boolean")

    profiles = config["profiles"]
    if not isinstance(profiles, list):
        _fail("invalid_type", "profiles must be an array")
    if any(not isinstance(profile, str) or len(profile) == 0 for profile in profiles):
        _fail("invalid_profile", "profiles must contain non-empty strings")
    if len(set(profiles)) != len(profiles):
        _fail("duplicate_profile", "profiles must not contain duplicates")

    return {field: config[field] for field in FIELDS}


def read(project_root: str | Path) -> tuple[dict[str, Any], str, Path]:
    _, path = resolve_paths(project_root)
    if path.is_symlink():
        _fail("unsafe_config_path", f"configuration must not be a symlink: {path}")
    if not path.exists():
        return default_config(), "missing", path
    if not path.is_file():
        _fail("unsafe_config_path", f"configuration must be a regular file: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
        parsed = json.loads(raw)
    except UnicodeDecodeError:
        _fail("invalid_encoding", "configuration must be UTF-8")
    except json.JSONDecodeError as exc:
        _fail("invalid_json", f"invalid JSON at line {exc.lineno}, column {exc.colno}")
    return validate(parsed), "config", path


def _encoded(config: dict[str, Any]) -> bytes:
    canonical = validate(config)
    return (json.dumps(canonical, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _fsync_directory(directory: Path) -> None:
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write(path: Path, config: dict[str, Any], *, replace: bool) -> None:
    data = _encoded(config)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".butler.config.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    published = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # Keep every fallible durability step before the atomic publication.
        # Once replace/link succeeds the command must not report failure after
        # having changed the visible configuration.
        _fsync_directory(path.parent)
        if replace:
            if path.is_symlink() or not path.is_file():
                _fail("unsafe_config_path", f"configuration must be a regular file: {path}")
            os.replace(temporary, path)
            published = True
        else:
            try:
                os.link(temporary, path)
            except FileExistsError:
                _fail("already_exists", f"configuration already exists: {path}", 1)
            published = True
    finally:
        if temporary.exists():
            try:
                temporary.unlink()
            except OSError:
                if not published:
                    raise


def initialize(project_root: str | Path) -> tuple[dict[str, Any], Path]:
    _, path = resolve_paths(project_root)
    if path.exists() or path.is_symlink():
        _fail("already_exists", f"configuration already exists: {path}", 1)
    config = default_config()
    write(path, config, replace=False)
    return config, path


def parse_value(field: str, value: str) -> Any:
    if field in BOOLEAN_FIELDS:
        if value not in {"true", "false"}:
            _fail("invalid_value", f"{field} accepts only true or false")
        return value == "true"
    if field == "profiles":
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            _fail("invalid_value", "profiles must be a JSON array of strings")
        candidate = default_config()
        candidate["profiles"] = parsed
        try:
            return validate(candidate)["profiles"]
        except ConfigError as exc:
            _fail("invalid_value", exc.message)
    _fail("invalid_field", f"field is not writable: {field}")


def update(project_root: str | Path, field: str, value: str) -> tuple[dict[str, Any], Path]:
    config, source, path = read(project_root)
    if source == "missing":
        _fail("missing_config", f"configuration does not exist: {path}")
    config[field] = parse_value(field, value)
    write(path, config, replace=True)
    return config, path


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        _fail("invalid_arguments", message)


def parser() -> argparse.ArgumentParser:
    root = JsonArgumentParser(description=__doc__)
    actions = root.add_subparsers(dest="action", required=True)
    for name in ("inspect", "resolve", "init"):
        command = actions.add_parser(name)
        command.add_argument("--project-root", required=True)
    change = actions.add_parser("set")
    change.add_argument("field")
    change.add_argument("value")
    change.add_argument("--project-root", required=True)
    return root


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if args.action == "inspect":
            config, source, path = read(args.project_root)
            emit({"status": "ok", "source": source, "path": str(path), "config": config})
        elif args.action == "resolve":
            config, source, path, conflicts = read_compatible(args.project_root)
            emit(
                {
                    "status": "ok",
                    "source": source,
                    "path": str(path),
                    "config": config,
                    "legacy_conflicts": conflicts,
                }
            )
        elif args.action == "init":
            config, path = initialize(args.project_root)
            emit({"status": "ok", "source": "created", "path": str(path), "config": config})
        else:
            config, path = update(args.project_root, args.field, args.value)
            emit({"status": "ok", "source": "config", "path": str(path), "config": config})
        return 0
    except ConfigError as exc:
        emit({"status": "error", "code": exc.code, "message": exc.message})
        return exc.exit_code
    except OSError as exc:
        emit({"status": "error", "code": "io_error", "message": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
