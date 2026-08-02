#!/usr/bin/env python3
"""Deterministic local Decision Map state engine.

The public Interface is deliberately limited to inspect, plan, apply, and
verify. State transitions are described by operation specs passed to plan.
"""
from __future__ import annotations

import copy
import datetime as dt
import errno
import fcntl
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, NoReturn


SCHEMA_VERSION = 1
PLAN_SCHEMA_VERSION = 1
MAX_LEASE_SECONDS = 86_400
MAPS_RELATIVE = Path(".ai/decision-maps")
LOCKS_RELATIVE = Path(".ai/.decision-map-locks")

MAP_RE = re.compile(r"^DMAP-[0-9]{4,}$", re.ASCII)
DECISION_RE = re.compile(r"^DEC-[0-9]{4,}$", re.ASCII)
FOG_RE = re.compile(r"^FOG-[0-9]{4,}$", re.ASCII)
OPERATION_RE = re.compile(r"^OP-[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$", re.ASCII)
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$", re.ASCII)
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", re.ASCII)

MAP_STATUSES = {"open", "closed"}
DECISION_STATUSES = {"open", "resolved", "abandoned"}
FOG_STATUSES = {"open", "graduated", "dismissed"}
OPERATION_KINDS = {
    "create_map",
    "add_decision",
    "add_fog",
    "link_dependency",
    "unlink_dependency",
    "claim",
    "renew",
    "release",
    "resolve",
    "abandon",
    "graduate_fog",
    "dismiss_fog",
    "close_map",
}


class DecisionMapError(ValueError):
    """A stable machine-readable failure from the Decision Map Interface."""

    def __init__(self, code: str, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_code = exit_code


def _fail(code: str, message: str, exit_code: int = 2) -> NoReturn:
    raise DecisionMapError(code, message, exit_code)


def _conflict(code: str, message: str) -> NoReturn:
    _fail(code, message, 1)


def _canonical_identity(value: Any, prefix: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        _fail("invalid_identity", f"expected canonical {prefix}-NNNN identity")
    number = int(value.split("-", 1)[1])
    if number < 1 or value != f"{prefix}-{number:04d}":
        _fail("invalid_identity", f"non-canonical identity: {value}")
    return value


def _map_id(value: Any) -> str:
    return _canonical_identity(value, "DMAP", MAP_RE)


def _decision_id(value: Any) -> str:
    return _canonical_identity(value, "DEC", DECISION_RE)


def _fog_id(value: Any) -> str:
    return _canonical_identity(value, "FOG", FOG_RE)


def _operation_id(value: Any) -> str:
    if not isinstance(value, str) or OPERATION_RE.fullmatch(value) is None:
        _fail("invalid_operation_id", "operation_id must match OP-<stable-id>")
    return value


def _nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_field", f"{field} must be a non-empty string")
    return value.strip()


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        _fail("invalid_field", f"{field} must be an array of non-empty strings")
    normalized = [item.strip() for item in value]
    if len(set(normalized)) != len(normalized):
        _fail("invalid_field", f"{field} must not contain duplicates")
    return normalized


def _exact(value: Any, required: set[str], optional: set[str], field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("invalid_field", f"{field} must be an object")
    keys = set(value)
    missing = required - keys
    unknown = keys - required - optional
    if missing:
        _fail("missing_field", f"{field} missing fields: {sorted(missing)}")
    if unknown:
        _fail("unknown_field", f"{field} contains unknown fields: {sorted(unknown)}")
    return value


def _canonical_json(value: Any) -> bytes:
    try:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as error:
        _fail("invalid_json_value", str(error))


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _decode_json(data: bytes, label: str) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("invalid_encoding", f"{label} must be UTF-8: {error}")
    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs)
    except (json.JSONDecodeError, ValueError) as error:
        _fail("invalid_json", f"invalid JSON in {label}: {error}")


def _parse_utc(value: Any, field: str) -> dt.datetime:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        _fail("invalid_time", f"{field} must be canonical UTC seconds (YYYY-MM-DDTHH:MM:SSZ)")
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as error:
        _fail("invalid_time", f"invalid {field}: {error}")
    return parsed


def _format_utc(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now(value: str | dt.datetime | None) -> tuple[dt.datetime, str]:
    if value is None:
        current = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    elif isinstance(value, str):
        current = _parse_utc(value, "now")
    elif isinstance(value, dt.datetime) and value.tzinfo is not None:
        current = value.astimezone(dt.timezone.utc).replace(microsecond=0)
    else:
        _fail("invalid_time", "now must be timezone-aware or canonical UTC text")
    return current, _format_utc(current)


def _resolve_root(project_root: str | Path) -> tuple[Path, Path]:
    raw = Path(project_root)
    try:
        root = raw.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        _fail("invalid_project_root", f"project root does not exist: {raw}: {error}")
    if not root.is_dir():
        _fail("invalid_project_root", f"project root is not a directory: {raw}")
    ai = root / ".ai"
    if ai.is_symlink() or not ai.is_dir():
        _fail("invalid_ai_directory", f"expected a real .ai directory under: {root}")
    return root, ai


def _state_location(root: Path, map_identity: str) -> tuple[Path, Path]:
    map_identity = _map_id(map_identity)
    directory = root / MAPS_RELATIVE / map_identity
    return directory, directory / "state.json"


def _assert_real_directory(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_dir():
        _fail("unsafe_path", f"{label} must be a real directory: {path}")


def _read_state(root: Path, map_identity: str, *, missing_ok: bool = False) -> tuple[dict[str, Any] | None, bytes | None]:
    directory, path = _state_location(root, map_identity)
    if not directory.exists():
        if missing_ok:
            return None, None
        _fail("map_not_found", f"Decision Map does not exist: {map_identity}", 1)
    _assert_real_directory(directory, "Decision Map directory")
    entries = list(directory.iterdir())
    if any(item.name != "state.json" for item in entries):
        _fail("unexpected_map_entry", f"unexpected entry in {map_identity}")
    if path.is_symlink() or not path.is_file():
        _fail("unsafe_state_path", f"state.json must be a regular file: {map_identity}")
    data = path.read_bytes()
    state = _decode_json(data, f"{map_identity}/state.json")
    validated = _validate_state(state, expected_map=map_identity)
    if data != _canonical_json(validated):
        _fail("noncanonical_state", f"state.json is not canonical: {map_identity}")
    return validated, data


def _validate_claim(value: Any, field: str) -> dict[str, Any] | None:
    if value is None:
        return None
    claim = _exact(value, {"owner", "token", "claimed_at", "expires_at"}, set(), field)
    claim["owner"] = _nonempty(claim["owner"], f"{field}.owner")
    claim["token"] = _nonempty(claim["token"], f"{field}.token")
    claimed = _parse_utc(claim["claimed_at"], f"{field}.claimed_at")
    expires = _parse_utc(claim["expires_at"], f"{field}.expires_at")
    if expires <= claimed:
        _fail("invalid_claim", f"{field}.expires_at must be later than claimed_at")
    return claim


def _validate_decision(value: Any, key: str) -> dict[str, Any]:
    decision = _exact(
        value,
        {"id", "question", "status", "depends_on", "claim", "resolution", "abandon"},
        set(),
        f"decision {key}",
    )
    identity = _decision_id(decision["id"])
    if identity != key:
        _fail("identity_mismatch", f"decision key does not match id: {key}")
    decision["question"] = _nonempty(decision["question"], f"decision {key}.question")
    if decision["status"] not in DECISION_STATUSES:
        _fail("invalid_status", f"invalid Decision status: {decision['status']}")
    depends = decision["depends_on"]
    if not isinstance(depends, list):
        _fail("invalid_dependency", f"decision {key}.depends_on must be an array")
    normalized_depends = [_decision_id(item) for item in depends]
    if len(set(normalized_depends)) != len(normalized_depends) or normalized_depends != sorted(normalized_depends, key=_identity_number):
        _fail("invalid_dependency", f"decision {key}.depends_on must be unique and numerically sorted")
    if key in normalized_depends:
        _fail("dependency_cycle", f"decision cannot depend on itself: {key}")
    decision["depends_on"] = normalized_depends
    decision["claim"] = _validate_claim(decision["claim"], f"decision {key}.claim")

    resolution = decision["resolution"]
    if resolution is not None:
        resolution = _exact(resolution, {"outcome", "rationale", "evidence", "at"}, set(), f"decision {key}.resolution")
        resolution["outcome"] = _nonempty(resolution["outcome"], f"decision {key}.resolution.outcome")
        resolution["rationale"] = _nonempty(resolution["rationale"], f"decision {key}.resolution.rationale")
        resolution["evidence"] = _string_list(resolution["evidence"], f"decision {key}.resolution.evidence")
        _parse_utc(resolution["at"], f"decision {key}.resolution.at")
        decision["resolution"] = resolution
    abandoned = decision["abandon"]
    if abandoned is not None:
        abandoned = _exact(abandoned, {"reason", "at"}, set(), f"decision {key}.abandon")
        abandoned["reason"] = _nonempty(abandoned["reason"], f"decision {key}.abandon.reason")
        _parse_utc(abandoned["at"], f"decision {key}.abandon.at")
        decision["abandon"] = abandoned

    status = decision["status"]
    if status == "open" and (decision["resolution"] is not None or decision["abandon"] is not None):
        _fail("invalid_decision", f"open Decision has terminal data: {key}")
    if status == "resolved" and (decision["resolution"] is None or decision["abandon"] is not None or decision["claim"] is not None):
        _fail("invalid_decision", f"resolved Decision has inconsistent data: {key}")
    if status == "abandoned" and (decision["abandon"] is None or decision["resolution"] is not None or decision["claim"] is not None):
        _fail("invalid_decision", f"abandoned Decision has inconsistent data: {key}")
    return decision


def _validate_fog(value: Any, key: str) -> dict[str, Any]:
    fog = _exact(value, {"id", "description", "status", "graduation", "dismissal"}, set(), f"fog {key}")
    identity = _fog_id(fog["id"])
    if identity != key:
        _fail("identity_mismatch", f"Fog key does not match id: {key}")
    fog["description"] = _nonempty(fog["description"], f"fog {key}.description")
    if fog["status"] not in FOG_STATUSES:
        _fail("invalid_status", f"invalid Fog status: {fog['status']}")
    graduation = fog["graduation"]
    if graduation is not None:
        graduation = _exact(graduation, {"decision_ids", "at"}, set(), f"fog {key}.graduation")
        if not isinstance(graduation["decision_ids"], list) or not graduation["decision_ids"]:
            _fail("invalid_fog", f"fog {key}.graduation.decision_ids must be non-empty")
        ids = [_decision_id(item) for item in graduation["decision_ids"]]
        if len(set(ids)) != len(ids):
            _fail("invalid_fog", f"fog {key}.graduation.decision_ids must be unique")
        graduation["decision_ids"] = ids
        _parse_utc(graduation["at"], f"fog {key}.graduation.at")
        fog["graduation"] = graduation
    dismissal = fog["dismissal"]
    if dismissal is not None:
        dismissal = _exact(dismissal, {"reason", "at"}, set(), f"fog {key}.dismissal")
        dismissal["reason"] = _nonempty(dismissal["reason"], f"fog {key}.dismissal.reason")
        _parse_utc(dismissal["at"], f"fog {key}.dismissal.at")
        fog["dismissal"] = dismissal
    status = fog["status"]
    if status == "open" and (fog["graduation"] is not None or fog["dismissal"] is not None):
        _fail("invalid_fog", f"open Fog has terminal data: {key}")
    if status == "graduated" and (fog["graduation"] is None or fog["dismissal"] is not None):
        _fail("invalid_fog", f"graduated Fog has inconsistent data: {key}")
    if status == "dismissed" and (fog["dismissal"] is None or fog["graduation"] is not None):
        _fail("invalid_fog", f"dismissed Fog has inconsistent data: {key}")
    return fog


def _validate_receipts(value: Any, map_identity: str, revision: int) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("invalid_receipts", "applied_operations must be an object")
    receipts: dict[str, Any] = {}
    revisions: set[int] = set()
    for key, raw in value.items():
        identity = _operation_id(key)
        receipt = _exact(raw, {"request_sha256", "revision", "result"}, set(), f"receipt {key}")
        if not isinstance(receipt["request_sha256"], str) or SHA_RE.fullmatch(receipt["request_sha256"]) is None:
            _fail("invalid_receipt", f"invalid request digest for {key}")
        if type(receipt["revision"]) is not int or not 1 <= receipt["revision"] <= revision:
            _fail("invalid_receipt", f"invalid receipt revision for {key}")
        result = receipt["result"]
        if not isinstance(result, dict):
            _fail("invalid_receipt", f"receipt result must be an object: {key}")
        expected = {"status": "ok", "action": "apply", "map_id": map_identity, "operation_id": identity, "revision": receipt["revision"]}
        if any(result.get(field) != expected_value for field, expected_value in expected.items()):
            _fail("invalid_receipt", f"receipt result identity mismatch: {key}")
        _nonempty(result.get("kind"), f"receipt {key}.result.kind")
        if receipt["revision"] in revisions:
            _fail("invalid_receipt", f"multiple operation receipts for revision {receipt['revision']}")
        revisions.add(receipt["revision"])
        receipts[identity] = receipt
    if revisions != set(range(1, revision + 1)):
        _fail("invalid_receipts", "operation receipts must cover every committed revision")
    return receipts


def _validate_state(value: Any, *, expected_map: str | None = None) -> dict[str, Any]:
    state = _exact(
        value,
        {"schema_version", "map_id", "revision", "status", "title", "destination", "created_at", "updated_at", "decisions", "fog", "applied_operations"},
        set(),
        "state",
    )
    if type(state["schema_version"]) is not int or state["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported_schema", f"state schema must be {SCHEMA_VERSION}")
    identity = _map_id(state["map_id"])
    if expected_map is not None and identity != expected_map:
        _fail("identity_mismatch", f"state map_id does not match directory: {expected_map}")
    if type(state["revision"]) is not int or state["revision"] < 1:
        _fail("invalid_revision", "revision must be a positive integer")
    if state["status"] not in MAP_STATUSES:
        _fail("invalid_status", f"invalid Map status: {state['status']}")
    state["title"] = _nonempty(state["title"], "state.title")
    state["destination"] = _nonempty(state["destination"], "state.destination")
    created = _parse_utc(state["created_at"], "state.created_at")
    updated = _parse_utc(state["updated_at"], "state.updated_at")
    if updated < created:
        _fail("invalid_time", "updated_at must not precede created_at")
    if not isinstance(state["decisions"], dict) or not isinstance(state["fog"], dict):
        _fail("invalid_collection", "decisions and fog must be objects")
    decisions = {_decision_id(key): _validate_decision(raw, key) for key, raw in state["decisions"].items()}
    fog = {_fog_id(key): _validate_fog(raw, key) for key, raw in state["fog"].items()}
    state["decisions"] = decisions
    state["fog"] = fog

    for identity_key, decision in decisions.items():
        for dependency in decision["depends_on"]:
            if dependency not in decisions:
                _fail("missing_dependency", f"{identity_key} depends on missing {dependency}")
            if decision["status"] == "open" and decisions[dependency]["status"] == "abandoned":
                _fail("abandoned_dependency", f"open {identity_key} depends on abandoned {dependency}")
    _validate_dag(decisions)
    for fog_item in fog.values():
        if fog_item["graduation"] is not None:
            for decision_identity in fog_item["graduation"]["decision_ids"]:
                if decision_identity not in decisions:
                    _fail("missing_graduated_decision", f"Fog references missing {decision_identity}")
    if state["status"] == "closed":
        if any(item["status"] == "open" for item in decisions.values()) or any(item["status"] == "open" for item in fog.values()):
            _fail("invalid_closed_map", "closed Map cannot contain open Decision or Fog")
    state["applied_operations"] = _validate_receipts(state["applied_operations"], identity, state["revision"])
    return state


def _validate_dag(decisions: dict[str, dict[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identity: str) -> None:
        if identity in visiting:
            _fail("dependency_cycle", f"dependency cycle includes {identity}")
        if identity in visited:
            return
        visiting.add(identity)
        for dependency in decisions[identity]["depends_on"]:
            visit(dependency)
        visiting.remove(identity)
        visited.add(identity)

    for identity in decisions:
        visit(identity)


def _identity_number(value: str) -> int:
    return int(value.split("-", 1)[1])


def _effective_claim(decision: dict[str, Any], current: dt.datetime) -> dict[str, Any] | None:
    claim = decision["claim"]
    if claim is None or current >= _parse_utc(claim["expires_at"], "claim.expires_at"):
        return None
    return claim


def _frontier(state: dict[str, Any], current: dt.datetime) -> list[str]:
    decisions = state["decisions"]
    return sorted(
        (
            identity
            for identity, decision in decisions.items()
            if decision["status"] == "open"
            and all(decisions[dependency]["status"] == "resolved" for dependency in decision["depends_on"])
            and _effective_claim(decision, current) is None
        ),
        key=_identity_number,
    )


def _discover(root: Path, *, strict: bool = True) -> list[str]:
    base = root / MAPS_RELATIVE
    if not base.exists():
        return []
    _assert_real_directory(base, "Decision Map root")
    found: list[str] = []
    for entry in base.iterdir():
        if entry.name.startswith(".tmp-"):
            if strict:
                _fail("stale_staging", f"stale Decision Map staging entry: {entry.name}")
            continue
        try:
            identity = _map_id(entry.name)
        except DecisionMapError:
            if strict:
                _fail("unexpected_map_entry", f"unexpected Decision Map entry: {entry.name}")
            continue
        _assert_real_directory(entry, "Decision Map directory")
        found.append(identity)
    return sorted(found, key=_identity_number)


def _validate_operation_spec(value: Any) -> dict[str, Any]:
    spec = _exact(value, {"schema_version", "operation_id", "operation"}, set(), "operation spec")
    if type(spec["schema_version"]) is not int or spec["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported_schema", f"operation schema must be {SCHEMA_VERSION}")
    spec["operation_id"] = _operation_id(spec["operation_id"])
    operation = spec["operation"]
    if not isinstance(operation, dict) or not isinstance(operation.get("kind"), str):
        _fail("invalid_operation", "operation.kind is required")
    kind = operation["kind"]
    if kind not in OPERATION_KINDS:
        _fail("invalid_operation", f"unsupported operation kind: {kind}")
    required: dict[str, set[str]] = {
        "create_map": {"kind", "title", "destination"},
        "add_decision": {"kind", "decision_id", "question", "depends_on"},
        "add_fog": {"kind", "fog_id", "description"},
        "link_dependency": {"kind", "decision_id", "dependency_id"},
        "unlink_dependency": {"kind", "decision_id", "dependency_id"},
        "claim": {"kind", "decision_id", "owner", "lease_seconds"},
        "renew": {"kind", "decision_id", "owner", "token", "lease_seconds"},
        "release": {"kind", "decision_id", "owner", "token"},
        "resolve": {"kind", "decision_id", "outcome", "rationale", "evidence"},
        "abandon": {"kind", "decision_id", "reason"},
        "graduate_fog": {"kind", "fog_id", "decisions"},
        "dismiss_fog": {"kind", "fog_id", "reason"},
        "close_map": {"kind"},
    }
    optional = {"owner", "token"} if kind == "resolve" else set()
    operation = _exact(operation, required[kind], optional, f"operation {kind}")
    if kind == "create_map":
        operation["title"] = _nonempty(operation["title"], "operation.title")
        operation["destination"] = _nonempty(operation["destination"], "operation.destination")
    elif kind == "add_decision":
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["question"] = _nonempty(operation["question"], "operation.question")
        operation["depends_on"] = _dependency_list(operation["depends_on"], "operation.depends_on")
    elif kind == "add_fog":
        operation["fog_id"] = _fog_id(operation["fog_id"])
        operation["description"] = _nonempty(operation["description"], "operation.description")
    elif kind in {"link_dependency", "unlink_dependency"}:
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["dependency_id"] = _decision_id(operation["dependency_id"])
    elif kind in {"claim", "renew"}:
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["owner"] = _nonempty(operation["owner"], "operation.owner")
        if type(operation["lease_seconds"]) is not int or not 1 <= operation["lease_seconds"] <= MAX_LEASE_SECONDS:
            _fail("invalid_lease", f"lease_seconds must be between 1 and {MAX_LEASE_SECONDS}")
        if kind == "renew":
            operation["token"] = _nonempty(operation["token"], "operation.token")
    elif kind == "release":
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["owner"] = _nonempty(operation["owner"], "operation.owner")
        operation["token"] = _nonempty(operation["token"], "operation.token")
    elif kind == "resolve":
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["outcome"] = _nonempty(operation["outcome"], "operation.outcome")
        operation["rationale"] = _nonempty(operation["rationale"], "operation.rationale")
        operation["evidence"] = _string_list(operation["evidence"], "operation.evidence")
        has_owner, has_token = "owner" in operation, "token" in operation
        if has_owner != has_token:
            _fail("invalid_claim_credentials", "resolve owner and token must be supplied together")
        if has_owner:
            operation["owner"] = _nonempty(operation["owner"], "operation.owner")
            operation["token"] = _nonempty(operation["token"], "operation.token")
    elif kind == "abandon":
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["reason"] = _nonempty(operation["reason"], "operation.reason")
    elif kind == "graduate_fog":
        operation["fog_id"] = _fog_id(operation["fog_id"])
        if not isinstance(operation["decisions"], list) or not operation["decisions"]:
            _fail("invalid_graduation", "graduate_fog.decisions must be non-empty")
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, raw in enumerate(operation["decisions"]):
            item = _exact(raw, {"decision_id", "question", "depends_on"}, set(), f"graduate_fog.decisions[{index}]")
            identity = _decision_id(item["decision_id"])
            if identity in seen:
                _fail("duplicate_identity", f"duplicate graduated Decision: {identity}")
            seen.add(identity)
            normalized.append({"decision_id": identity, "question": _nonempty(item["question"], f"graduate_fog.decisions[{index}].question"), "depends_on": _dependency_list(item["depends_on"], f"graduate_fog.decisions[{index}].depends_on")})
        operation["decisions"] = normalized
    elif kind == "dismiss_fog":
        operation["fog_id"] = _fog_id(operation["fog_id"])
        operation["reason"] = _nonempty(operation["reason"], "operation.reason")
    spec["operation"] = operation
    return spec


def _dependency_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        _fail("invalid_dependency", f"{field} must be an array")
    normalized = [_decision_id(item) for item in value]
    if len(set(normalized)) != len(normalized):
        _fail("invalid_dependency", f"{field} must not contain duplicates")
    return sorted(normalized, key=_identity_number)


def _request_digest(map_identity: str, spec: dict[str, Any]) -> str:
    return _sha(_canonical_json({"map_id": map_identity, "spec": spec}))


def _open_state(state: dict[str, Any]) -> None:
    if state["status"] != "open":
        _conflict("map_closed", "closed Decision Map is read-only")


def _find_decision(state: dict[str, Any], identity: str) -> dict[str, Any]:
    if identity not in state["decisions"]:
        _conflict("decision_not_found", f"Decision does not exist: {identity}")
    return state["decisions"][identity]


def _find_fog(state: dict[str, Any], identity: str) -> dict[str, Any]:
    if identity not in state["fog"]:
        _conflict("fog_not_found", f"Fog does not exist: {identity}")
    return state["fog"][identity]


def _new_decision(identity: str, question: str, depends_on: list[str]) -> dict[str, Any]:
    return {"id": identity, "question": question, "status": "open", "depends_on": depends_on, "claim": None, "resolution": None, "abandon": None}


def _new_fog(identity: str, description: str) -> dict[str, Any]:
    return {"id": identity, "description": description, "status": "open", "graduation": None, "dismissal": None}


def _reduce(
    state: dict[str, Any] | None,
    map_identity: str,
    spec: dict[str, Any],
    current: dt.datetime,
    now_text: str,
    *,
    token: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    operation = spec["operation"]
    kind = operation["kind"]
    next_revision = 1 if state is None else state["revision"] + 1
    result: dict[str, Any] = {
        "status": "ok",
        "action": "apply",
        "map_id": map_identity,
        "operation_id": spec["operation_id"],
        "kind": kind,
        "revision": next_revision,
    }

    if kind == "create_map":
        if state is not None:
            _conflict("map_exists", f"Decision Map already exists: {map_identity}")
        candidate = {
            "schema_version": SCHEMA_VERSION,
            "map_id": map_identity,
            "revision": next_revision,
            "status": "open",
            "title": operation["title"],
            "destination": operation["destination"],
            "created_at": now_text,
            "updated_at": now_text,
            "decisions": {},
            "fog": {},
            "applied_operations": {},
        }
        return candidate, result

    if state is None:
        _conflict("map_not_found", f"Decision Map does not exist: {map_identity}")
    candidate = copy.deepcopy(state)
    _open_state(candidate)
    decisions = candidate["decisions"]
    fog = candidate["fog"]

    if kind == "add_decision":
        identity = operation["decision_id"]
        if identity in decisions:
            _conflict("decision_exists", f"Decision already exists: {identity}")
        decisions[identity] = _new_decision(identity, operation["question"], operation["depends_on"])
        result["decision_id"] = identity
    elif kind == "add_fog":
        identity = operation["fog_id"]
        if identity in fog:
            _conflict("fog_exists", f"Fog already exists: {identity}")
        fog[identity] = _new_fog(identity, operation["description"])
        result["fog_id"] = identity
    elif kind in {"link_dependency", "unlink_dependency"}:
        identity = operation["decision_id"]
        dependency = operation["dependency_id"]
        decision = _find_decision(candidate, identity)
        _find_decision(candidate, dependency)
        if decision["status"] != "open":
            _conflict("decision_not_open", f"Decision is not open: {identity}")
        if _effective_claim(decision, current) is not None:
            _conflict("decision_claimed", f"cannot edit dependencies while claimed: {identity}")
        if kind == "link_dependency":
            if dependency in decision["depends_on"]:
                _conflict("dependency_exists", f"dependency already exists: {identity} -> {dependency}")
            decision["depends_on"].append(dependency)
            decision["depends_on"].sort(key=_identity_number)
        else:
            if dependency not in decision["depends_on"]:
                _conflict("dependency_not_found", f"dependency does not exist: {identity} -> {dependency}")
            decision["depends_on"].remove(dependency)
        result.update({"decision_id": identity, "dependency_id": dependency})
    elif kind == "claim":
        identity = operation["decision_id"]
        decision = _find_decision(candidate, identity)
        if identity not in _frontier(candidate, current):
            _conflict("not_frontier", f"Decision is not on Frontier: {identity}")
        actual_token = token or "planned-token"
        expires = current + dt.timedelta(seconds=operation["lease_seconds"])
        decision["claim"] = {"owner": operation["owner"], "token": actual_token, "claimed_at": now_text, "expires_at": _format_utc(expires)}
        result.update({"decision_id": identity, "owner": operation["owner"], "token": actual_token, "expires_at": _format_utc(expires)})
    elif kind == "renew":
        identity = operation["decision_id"]
        decision = _find_decision(candidate, identity)
        claim = _effective_claim(decision, current)
        if claim is None:
            _conflict("claim_expired", f"Decision has no effective claim: {identity}")
        if claim["owner"] != operation["owner"] or claim["token"] != operation["token"]:
            _conflict("claim_mismatch", f"claim credentials do not match: {identity}")
        base = max(current, _parse_utc(claim["expires_at"], "claim.expires_at"))
        claim["expires_at"] = _format_utc(base + dt.timedelta(seconds=operation["lease_seconds"]))
        result.update({"decision_id": identity, "owner": claim["owner"], "token": claim["token"], "expires_at": claim["expires_at"]})
    elif kind == "release":
        identity = operation["decision_id"]
        decision = _find_decision(candidate, identity)
        claim = _effective_claim(decision, current)
        if claim is None:
            _conflict("claim_expired", f"Decision has no effective claim: {identity}")
        if claim["owner"] != operation["owner"] or claim["token"] != operation["token"]:
            _conflict("claim_mismatch", f"claim credentials do not match: {identity}")
        decision["claim"] = None
        result["decision_id"] = identity
    elif kind == "resolve":
        identity = operation["decision_id"]
        decision = _find_decision(candidate, identity)
        if decision["status"] != "open" or not all(decisions[item]["status"] == "resolved" for item in decision["depends_on"]):
            _conflict("not_resolvable", f"Decision is not resolvable: {identity}")
        claim = _effective_claim(decision, current)
        supplied = "owner" in operation
        if claim is not None:
            if not supplied or claim["owner"] != operation["owner"] or claim["token"] != operation["token"]:
                _conflict("claim_mismatch", f"active claim credentials are required: {identity}")
        elif supplied:
            _conflict("claim_expired", f"Decision has no effective claim: {identity}")
        decision["status"] = "resolved"
        decision["claim"] = None
        decision["resolution"] = {"outcome": operation["outcome"], "rationale": operation["rationale"], "evidence": operation["evidence"], "at": now_text}
        result["decision_id"] = identity
    elif kind == "abandon":
        identity = operation["decision_id"]
        decision = _find_decision(candidate, identity)
        if decision["status"] != "open":
            _conflict("decision_not_open", f"Decision is not open: {identity}")
        if _effective_claim(decision, current) is not None:
            _conflict("decision_claimed", f"cannot abandon an actively claimed Decision: {identity}")
        dependents = [item_id for item_id, item in decisions.items() if item["status"] == "open" and identity in item["depends_on"]]
        if dependents:
            _conflict("open_dependents", f"Decision has open dependents: {', '.join(sorted(dependents, key=_identity_number))}")
        decision["status"] = "abandoned"
        decision["claim"] = None
        decision["abandon"] = {"reason": operation["reason"], "at": now_text}
        result["decision_id"] = identity
    elif kind == "graduate_fog":
        identity = operation["fog_id"]
        fog_item = _find_fog(candidate, identity)
        if fog_item["status"] != "open":
            _conflict("fog_not_open", f"Fog is not open: {identity}")
        new_ids: list[str] = []
        for item in operation["decisions"]:
            decision_identity = item["decision_id"]
            if decision_identity in decisions:
                _conflict("decision_exists", f"Decision already exists: {decision_identity}")
            decisions[decision_identity] = _new_decision(decision_identity, item["question"], item["depends_on"])
            new_ids.append(decision_identity)
        fog_item["status"] = "graduated"
        fog_item["graduation"] = {"decision_ids": new_ids, "at": now_text}
        result.update({"fog_id": identity, "decision_ids": new_ids})
    elif kind == "dismiss_fog":
        identity = operation["fog_id"]
        fog_item = _find_fog(candidate, identity)
        if fog_item["status"] != "open":
            _conflict("fog_not_open", f"Fog is not open: {identity}")
        fog_item["status"] = "dismissed"
        fog_item["dismissal"] = {"reason": operation["reason"], "at": now_text}
        result["fog_id"] = identity
    elif kind == "close_map":
        if any(item["status"] == "open" for item in decisions.values()) or any(item["status"] == "open" for item in fog.values()):
            _conflict("map_not_converged", "Map cannot close while Decision or Fog remains open")
        candidate["status"] = "closed"
    else:  # pragma: no cover - validated before reduction
        _fail("invalid_operation", f"unsupported operation kind: {kind}")

    candidate["revision"] = next_revision
    candidate["updated_at"] = now_text
    return candidate, result


def _candidate_with_receipt(
    state: dict[str, Any] | None,
    map_identity: str,
    spec: dict[str, Any],
    current: dt.datetime,
    now_text: str,
    request_sha: str,
    *,
    token: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate, result = _reduce(state, map_identity, spec, current, now_text, token=token)
    candidate["applied_operations"][spec["operation_id"]] = {"request_sha256": request_sha, "revision": candidate["revision"], "result": copy.deepcopy(result)}
    return _validate_state(candidate, expected_map=map_identity), result


def inspect(project_root: str | Path, map_id: str | None = None, now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    current, now_text = _now(now)
    if map_id is not None:
        identity = _map_id(map_id)
        state, _ = _read_state(root, identity)
        assert state is not None
        effective = {item_id: claim for item_id, item in state["decisions"].items() if (claim := _effective_claim(item, current)) is not None}
        return {"schema_version": SCHEMA_VERSION, "status": "ok", "action": "inspect", "observed_at": now_text, "state": state, "frontier": _frontier(state, current), "effective_claims": effective}
    maps: list[dict[str, Any]] = []
    for identity in _discover(root):
        state, _ = _read_state(root, identity)
        assert state is not None
        maps.append({"map_id": identity, "title": state["title"], "destination": state["destination"], "status": state["status"], "revision": state["revision"], "frontier_count": len(_frontier(state, current))})
    return {"schema_version": SCHEMA_VERSION, "status": "ok", "action": "inspect", "observed_at": now_text, "maps": maps}


def plan(project_root: str | Path, map_id: str, spec: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    identity = _map_id(map_id)
    normalized = _validate_operation_spec(copy.deepcopy(spec))
    current, now_text = _now(now)
    state, data = _read_state(root, identity, missing_ok=True)
    request_sha = _request_digest(identity, normalized)
    receipt = state["applied_operations"].get(normalized["operation_id"]) if state is not None else None
    if receipt is not None:
        if receipt["request_sha256"] != request_sha:
            _conflict("operation_id_conflict", f"operation_id already used for another request: {normalized['operation_id']}")
        effect = copy.deepcopy(receipt["result"])
        effect["idempotent"] = True
    else:
        _, effect = _candidate_with_receipt(state, identity, normalized, current, now_text, request_sha, token=None)
        if normalized["operation"]["kind"] == "claim":
            effect["token"] = "<generated-at-apply>"
        effect["idempotent"] = False
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "status": "ok",
        "action": "apply",
        "map_id": identity,
        "base_revision": None if state is None else state["revision"],
        "base_sha256": None if data is None else _sha(data),
        "request_sha256": request_sha,
        "planned_at": now_text,
        "operation": normalized,
        "effect": effect,
    }


def _validate_plan(value: Any) -> dict[str, Any]:
    planned = _exact(value, {"schema_version", "status", "action", "map_id", "base_revision", "base_sha256", "request_sha256", "planned_at", "operation", "effect"}, set(), "plan")
    if type(planned["schema_version"]) is not int or planned["schema_version"] != PLAN_SCHEMA_VERSION or planned["status"] != "ok" or planned["action"] != "apply":
        _fail("invalid_plan", "unsupported plan schema or action")
    planned["map_id"] = _map_id(planned["map_id"])
    if planned["base_revision"] is not None and (type(planned["base_revision"]) is not int or planned["base_revision"] < 1):
        _fail("invalid_plan", "base_revision must be null or a positive integer")
    if planned["base_sha256"] is not None and (not isinstance(planned["base_sha256"], str) or SHA_RE.fullmatch(planned["base_sha256"]) is None):
        _fail("invalid_plan", "base_sha256 must be null or SHA-256")
    if (planned["base_revision"] is None) != (planned["base_sha256"] is None):
        _fail("invalid_plan", "base_revision and base_sha256 must both be null or present")
    if not isinstance(planned["request_sha256"], str) or SHA_RE.fullmatch(planned["request_sha256"]) is None:
        _fail("invalid_plan", "request_sha256 must be SHA-256")
    _parse_utc(planned["planned_at"], "plan.planned_at")
    planned["operation"] = _validate_operation_spec(planned["operation"])
    if not isinstance(planned["effect"], dict):
        _fail("invalid_plan", "effect must be an object")
    expected = _request_digest(planned["map_id"], planned["operation"])
    if expected != planned["request_sha256"]:
        _fail("plan_digest_mismatch", "plan request digest does not match operation")
    return planned


@contextmanager
def _map_lock(root: Path, map_identity: str) -> Iterator[None]:
    lock_root = root / LOCKS_RELATIVE
    if lock_root.exists():
        _assert_real_directory(lock_root, "Decision Map lock root")
    else:
        try:
            lock_root.mkdir(mode=0o700)
        except FileExistsError:
            pass
        _assert_real_directory(lock_root, "Decision Map lock root")
    path = lock_root / f"{map_identity}.lock"
    flags = os.O_CREAT | os.O_RDWR
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as error:
        _fail("lock_error", f"cannot open Decision Map lock: {error}")
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            _fail("unsafe_lock", f"Decision Map lock is not a regular file: {path}")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _conflict("map_locked", f"Decision Map is being modified: {map_identity}")
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _publish_new(root: Path, map_identity: str, data: bytes) -> None:
    base = root / MAPS_RELATIVE
    if base.exists():
        _assert_real_directory(base, "Decision Map root")
    else:
        try:
            base.mkdir(mode=0o755)
        except FileExistsError:
            pass
        _assert_real_directory(base, "Decision Map root")
    target = base / map_identity
    if target.exists() or target.is_symlink():
        _conflict("map_exists", f"Decision Map already exists: {map_identity}")
    staging = Path(tempfile.mkdtemp(prefix=f".tmp-{map_identity}-", dir=base))
    published = False
    try:
        state_path = staging / "state.json"
        descriptor = os.open(state_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(staging)
        try:
            os.rename(staging, target)
        except OSError as error:
            if error.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                _conflict("map_exists", f"Decision Map already exists: {map_identity}")
            raise
        published = True
        _fsync_directory(base)
    finally:
        if not published and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def _publish_existing(root: Path, map_identity: str, data: bytes) -> None:
    directory, path = _state_location(root, map_identity)
    _assert_real_directory(directory, "Decision Map directory")
    if path.is_symlink() or not path.is_file():
        _fail("unsafe_state_path", f"state.json must be a regular file: {map_identity}")
    descriptor, name = tempfile.mkstemp(prefix=".state.", suffix=".tmp", dir=directory)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply(project_root: str | Path, planned: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    normalized = _validate_plan(copy.deepcopy(planned))
    identity = normalized["map_id"]
    current, now_text = _now(now)
    with _map_lock(root, identity):
        state, data = _read_state(root, identity, missing_ok=True)
        operation_identity = normalized["operation"]["operation_id"]
        receipt = state["applied_operations"].get(operation_identity) if state is not None else None
        if receipt is not None:
            if receipt["request_sha256"] != normalized["request_sha256"]:
                _conflict("operation_id_conflict", f"operation_id already used for another request: {operation_identity}")
            result = copy.deepcopy(receipt["result"])
            result["idempotent"] = True
            return result
        actual_revision = None if state is None else state["revision"]
        actual_sha = None if data is None else _sha(data)
        if actual_revision != normalized["base_revision"] or actual_sha != normalized["base_sha256"]:
            _conflict("stale_plan", "Decision Map changed after plan; create a new plan")
        token = secrets.token_urlsafe(32) if normalized["operation"]["operation"]["kind"] == "claim" else None
        candidate, result = _candidate_with_receipt(state, identity, normalized["operation"], current, now_text, normalized["request_sha256"], token=token)
        encoded = _canonical_json(candidate)
        if state is None:
            _publish_new(root, identity, encoded)
        else:
            _publish_existing(root, identity, encoded)
        result["idempotent"] = False
        return result


def verify(project_root: str | Path, map_id: str | None = None, now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    current, now_text = _now(now)
    errors: list[dict[str, str]] = []
    checked: list[dict[str, Any]] = []
    identities: list[str] = []
    if map_id is not None:
        identities = [_map_id(map_id)]
    else:
        base = root / MAPS_RELATIVE
        if base.exists():
            try:
                _assert_real_directory(base, "Decision Map root")
                for entry in sorted(base.iterdir(), key=lambda item: item.name):
                    if entry.name.startswith(".tmp-"):
                        errors.append({"code": "stale_staging", "message": f"stale staging entry: {entry.name}"})
                        continue
                    try:
                        identities.append(_map_id(entry.name))
                    except DecisionMapError as error:
                        errors.append({"code": "unexpected_map_entry", "message": f"unexpected entry: {entry.name}"})
            except DecisionMapError as error:
                errors.append({"code": error.code, "message": error.message})
    for identity in identities:
        try:
            state, data = _read_state(root, identity)
            assert state is not None and data is not None
            checked.append({"map_id": identity, "revision": state["revision"], "sha256": _sha(data), "frontier": _frontier(state, current)})
        except DecisionMapError as error:
            errors.append({"code": error.code, "message": error.message})
    checked.sort(key=lambda item: _identity_number(item["map_id"]))
    return {"schema_version": SCHEMA_VERSION, "status": "ok" if not errors else "error", "action": "verify", "observed_at": now_text, "checked": checked, "errors": errors}
