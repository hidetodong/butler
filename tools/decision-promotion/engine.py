#!/usr/bin/env python3
"""Deterministic Decision Map to Milestone / Iteration promotion engine."""
from __future__ import annotations

import copy
import datetime as dt
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any, Iterator, NoReturn


SCHEMA_VERSION = 1
PLAN_SCHEMA_VERSION = 1
BUTLER_ROOT = Path(__file__).resolve().parents[2]
PROMOTIONS_RELATIVE = Path(".ai/decision-promotions")
LOCK_RELATIVE = Path(".ai/.decision-promotion.lock")
PENDING_RELATIVE = Path(".ai/.decision-promotion-pending")

PROMOTION_RE = re.compile(r"^PROM-[0-9]{4,}$", re.ASCII)
MAP_RE = re.compile(r"^DMAP-[0-9]{4,}$", re.ASCII)
DECISION_RE = re.compile(r"^DEC-[0-9]{4,}$", re.ASCII)
MILESTONE_RE = re.compile(r"^MILE-[0-9]{4,}$", re.ASCII)
ITERATION_RE = re.compile(r"^ITER-[0-9]{4,}$", re.ASCII)
ROUTE_RE = re.compile(r"^R[1-9][0-9]*$", re.ASCII)
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$", re.ASCII)
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", re.ASCII)

INTAKE_FIELDS = {
    "title",
    "summary",
    "model_recommendations",
    "open_questions",
    "in_scope",
    "out_of_scope",
}
ARRAY_FIELDS = {"model_recommendations", "open_questions", "in_scope", "out_of_scope"}


class DecisionPromotionError(ValueError):
    """Stable machine-readable error from the promotion Interface."""

    def __init__(self, code: str, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_code = exit_code


def _fail(code: str, message: str, exit_code: int = 2) -> NoReturn:
    raise DecisionPromotionError(code, message, exit_code)


def _conflict(code: str, message: str) -> NoReturn:
    _fail(code, message, 1)


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        _fail("module_unavailable", f"cannot load Butler module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


DECISION_MAP = _load_module("butler_decision_promotion_map", BUTLER_ROOT / "tools/decision-map/engine.py")
ITERATION_INTAKE = _load_module("butler_decision_promotion_intake", BUTLER_ROOT / "tools/iteration-intake/intake.py")
STATE_LEDGER = _load_module("butler_decision_promotion_ledger", BUTLER_ROOT / "tools/state-ledger/state_ledger.py")


def _exact(value: Any, required: set[str], optional: set[str], field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("invalid_field", f"{field} must be an object")
    missing = required - set(value)
    unknown = set(value) - required - optional
    if missing:
        _fail("missing_field", f"{field} missing fields: {sorted(missing)}")
    if unknown:
        _fail("unknown_field", f"{field} contains unknown fields: {sorted(unknown)}")
    return value


def _canonical_identity(value: Any, prefix: str, pattern: re.Pattern[str]) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        _fail("invalid_identity", f"expected canonical {prefix} identity")
    number = int(value.split("-", 1)[1])
    if number < 1 or value != f"{prefix}-{number:04d}":
        _fail("invalid_identity", f"non-canonical identity: {value}")
    return value


def _promotion_id(value: Any) -> str:
    return _canonical_identity(value, "PROM", PROMOTION_RE)


def _map_id(value: Any) -> str:
    return _canonical_identity(value, "DMAP", MAP_RE)


def _decision_id(value: Any) -> str:
    return _canonical_identity(value, "DEC", DECISION_RE)


def _milestone_id(value: Any) -> str:
    return _canonical_identity(value, "MILE", MILESTONE_RE)


def _iteration_id(value: Any) -> str:
    return _canonical_identity(value, "ITER", ITERATION_RE)


def _route_id(value: Any) -> str:
    if not isinstance(value, str) or ROUTE_RE.fullmatch(value) is None:
        _fail("invalid_identity", "expected canonical route identity R<number>")
    return value


def _optional_identity(value: Any, parser: Any, field: str) -> str | None:
    if value is None:
        return None
    try:
        return parser(value)
    except DecisionPromotionError as error:
        _fail(error.code, f"invalid {field}: {error.message}")


def _nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_field", f"{field} must be a non-empty string")
    return value.strip()


def _strings(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        _fail("invalid_field", f"{field} must be an array of non-empty strings")
    normalized = [item.strip() for item in value]
    if len(set(normalized)) != len(normalized):
        _fail("invalid_field", f"{field} must not contain duplicates")
    if nonempty and not normalized:
        _fail("invalid_field", f"{field} must not be empty")
    return normalized


def _identity_number(value: str) -> int:
    return int(value.split("-", 1)[1])


def _canonical_json(value: Any) -> bytes:
    try:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as error:
        _fail("invalid_json_value", str(error))


def _sha(value: bytes | dict[str, Any]) -> str:
    data = value if isinstance(value, bytes) else _canonical_json(value)
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


def _parse_utc(value: Any, field: str) -> str:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        _fail("invalid_time", f"{field} must be canonical UTC seconds")
    try:
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        _fail("invalid_time", f"invalid {field}: {error}")
    return value


def _now(value: str | dt.datetime | None) -> str:
    if value is None:
        current = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    elif isinstance(value, str):
        _parse_utc(value, "now")
        current = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    elif isinstance(value, dt.datetime) and value.tzinfo is not None:
        current = value.astimezone(dt.timezone.utc).replace(microsecond=0)
    else:
        _fail("invalid_time", "now must be timezone-aware or canonical UTC text")
    return current.strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_root(project_root: str | Path) -> tuple[Path, Path]:
    raw = Path(project_root)
    try:
        root = raw.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        _fail("invalid_project_root", f"project root does not exist: {raw}: {error}")
    if not root.is_dir():
        _fail("invalid_project_root", f"project root is not a directory: {root}")
    ai = root / ".ai"
    if ai.is_symlink() or not ai.is_dir():
        _fail("invalid_ai_directory", f"expected a real .ai directory under: {root}")
    return root, ai


def _regular_bytes(path: Path, label: str, *, missing_ok: bool = False) -> bytes | None:
    if not path.exists():
        if missing_ok and not path.is_symlink():
            return None
        _fail("missing_state", f"missing {label}: {path}", 1)
    if path.is_symlink() or not path.is_file():
        _fail("unsafe_path", f"{label} must be a regular file: {path}")
    try:
        return path.read_bytes()
    except OSError as error:
        _fail("io_error", f"cannot read {label}: {error}")


def _validate_intake(value: Any) -> dict[str, Any]:
    intake = _exact(value, INTAKE_FIELDS, set(), "target.intake")
    normalized: dict[str, Any] = {
        "title": _nonempty(intake["title"], "target.intake.title"),
        "summary": _nonempty(intake["summary"], "target.intake.summary"),
    }
    for field in ARRAY_FIELDS:
        normalized[field] = _strings(intake[field], f"target.intake.{field}", nonempty=field == "in_scope")
    return normalized


def _validate_request(value: Any) -> dict[str, Any]:
    request = _exact(value, {"schema_version", "promotion_id", "source", "target"}, set(), "request")
    if type(request["schema_version"]) is not int or request["schema_version"] != SCHEMA_VERSION:
        _fail("invalid_schema", f"request schema_version must be {SCHEMA_VERSION}")
    source = _exact(request["source"], {"map_id", "decision_ids"}, set(), "source")
    roots = [_decision_id(item) for item in _strings(source["decision_ids"], "source.decision_ids", nonempty=True)]
    if len(set(roots)) != len(roots):
        _fail("invalid_field", "source.decision_ids must not contain duplicates")
    roots.sort(key=_identity_number)
    target = _exact(request["target"], {"kind"}, {"milestone_id", "route_id", "intake"}, "target")
    kind = target["kind"]
    if kind == "route-reference":
        _exact(target, {"kind", "milestone_id", "route_id"}, set(), "target")
        normalized_target = {
            "kind": kind,
            "milestone_id": _milestone_id(target["milestone_id"]),
            "route_id": _route_id(target["route_id"]),
        }
    elif kind == "iteration-start":
        _exact(target, {"kind", "milestone_id", "route_id", "intake"}, set(), "target")
        milestone = _optional_identity(target["milestone_id"], _milestone_id, "milestone_id")
        route = _optional_identity(target["route_id"], _route_id, "route_id")
        if (milestone is None) != (route is None):
            _fail("invalid_target", "milestone_id and route_id must both be null or both be present")
        normalized_target = {"kind": kind, "milestone_id": milestone, "route_id": route, "intake": _validate_intake(target["intake"])}
    else:
        _fail("invalid_target", "target.kind must be route-reference or iteration-start")
    return {
        "schema_version": SCHEMA_VERSION,
        "promotion_id": _promotion_id(request["promotion_id"]),
        "source": {"map_id": _map_id(source["map_id"]), "decision_ids": roots},
        "target": normalized_target,
    }


def _source_slice(root: Path, source: dict[str, Any]) -> dict[str, Any]:
    try:
        inspected = DECISION_MAP.inspect(root, source["map_id"])
    except DECISION_MAP.DecisionMapError as error:
        raise DecisionPromotionError(error.code, error.message, error.exit_code) from error
    state = inspected["state"]
    decisions = state["decisions"]
    closure: set[str] = set()
    pending = list(reversed(source["decision_ids"]))
    while pending:
        identity = pending.pop()
        if identity in closure:
            continue
        item = decisions.get(identity)
        if item is None:
            _conflict("decision_not_found", f"Decision does not exist: {identity}")
        if item["status"] != "resolved" or item["resolution"] is None:
            _conflict("decision_not_resolved", f"Decision is not resolved: {identity}")
        closure.add(identity)
        pending.extend(reversed(item["depends_on"]))
    ordered = sorted(closure, key=_identity_number)
    projection = []
    confirmed = []
    for identity in ordered:
        item = decisions[identity]
        resolution = item["resolution"]
        projection.append(
            {
                "decision_id": identity,
                "question": item["question"],
                "depends_on": item["depends_on"],
                "resolution": {
                    "outcome": resolution["outcome"],
                    "rationale": resolution["rationale"],
                    "evidence": resolution["evidence"],
                    "at": resolution["at"],
                },
            }
        )
        confirmed.append(f"{identity} — {resolution['outcome']}（理由：{resolution['rationale']}）")
    digest_input = {"map_id": source["map_id"], "roots": source["decision_ids"], "decisions": projection}
    return {
        "map_id": source["map_id"],
        "roots": source["decision_ids"],
        "closure": ordered,
        "observed_revision": state["revision"],
        "slice_sha256": _sha(digest_input),
        "confirmed_decisions": confirmed,
    }


def _current(path: Path, label: str) -> str:
    data = _regular_bytes(path, label)
    assert data is not None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("invalid_encoding", f"{label} must be UTF-8: {error}")
    matches = re.findall(r"^current:\s*(\S+)\s*$", text, re.MULTILINE)
    if len(matches) != 1:
        _fail("invalid_ledger", f"{label} must contain exactly one current marker")
    return matches[0]


def _ledger_row(path: Path, identity: str, columns: int, label: str) -> list[str]:
    data = _regular_bytes(path, label)
    assert data is not None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("invalid_encoding", f"{label} must be UTF-8: {error}")
    matches: list[list[str]] = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == columns + 2 and cells[1] == identity:
            matches.append(cells[1:-1])
    if len(matches) != 1:
        _fail("invalid_ledger", f"{label} must contain exactly one row for {identity}")
    return matches[0]


def _route(path: Path, route_identity: str) -> dict[str, str]:
    data = _regular_bytes(path, "MILESTONE.md")
    assert data is not None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("invalid_encoding", f"MILESTONE.md must be UTF-8: {error}")
    found: list[dict[str, str]] = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 6 and cells[1] == route_identity:
            found.append({"route_id": cells[1], "title": cells[2], "iteration": cells[3], "status": cells[4]})
    if not found:
        _conflict("route_not_found", f"Milestone route does not exist: {route_identity}")
    if len(found) != 1:
        _fail("invalid_milestone", f"duplicate route in MILESTONE.md: {route_identity}")
    return found[0]


def _target_snapshot(root: Path, target: dict[str, Any], *, require_eligible: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    ai = root / ".ai"
    milestone_current = _current(ai / "MILESTONES.md", "MILESTONES.md")
    iteration_current = _current(ai / "ITERATIONS.md", "ITERATIONS.md")
    if milestone_current != "none":
        _milestone_id(milestone_current)
        if _ledger_row(ai / "MILESTONES.md", milestone_current, 7, "MILESTONES.md")[2] != "active":
            _fail("invalid_ledger", f"current Milestone row is not active: {milestone_current}")
    if iteration_current != "none":
        _iteration_id(iteration_current)
        if _ledger_row(ai / "ITERATIONS.md", iteration_current, 7, "ITERATIONS.md")[2] != "active":
            _fail("invalid_ledger", f"current Iteration row is not active: {iteration_current}")
    kind = target["kind"]
    if kind == "route-reference":
        if milestone_current == "none" or target["milestone_id"] != milestone_current:
            _conflict("milestone_mismatch", "route-reference must target the current active Milestone")
        route = _route(ai / "MILESTONE.md", target["route_id"])
        if require_eligible and (route["status"] != "planned" or route["iteration"] != "—"):
            _conflict("route_unavailable", f"route must be planned and unbound: {target['route_id']}")
        snapshot = {"milestone_current": milestone_current, "route": route}
        return snapshot, {"kind": kind, "milestone_id": milestone_current, "route_id": route["route_id"]}

    milestone = target["milestone_id"]
    route_identity = target["route_id"]
    if require_eligible and iteration_current != "none":
        _conflict("active_iteration", f"an active Iteration already exists: {iteration_current}")
    route = None
    if milestone_current == "none":
        if milestone is not None or route_identity is not None:
            _conflict("milestone_mismatch", "standalone iteration-start requires null milestone_id and route_id")
    else:
        if milestone != milestone_current or route_identity is None:
            _conflict("milestone_mismatch", "iteration-start must target the current active Milestone route")
        route = _route(ai / "MILESTONE.md", route_identity)
        if require_eligible and (route["status"] != "planned" or route["iteration"] != "—"):
            _conflict("route_unavailable", f"route must be planned and unbound: {route_identity}")
    index = _regular_bytes(ai / "state-index.json", "state-index.json", missing_ok=True)
    snapshot = {
        "iteration_current": iteration_current,
        "milestone_current": milestone_current,
        "route": route,
        "state_index_sha256": None if index is None else _sha(index),
    }
    intake_spec = _intake_spec(target, [], route_identity)
    proposed = ITERATION_INTAKE.plan(root, intake_spec)
    if require_eligible and proposed.get("status") != "ready":
        _conflict("intake_unavailable", f"iteration-intake refused target: {proposed.get('status')}")
    snapshot["proposed_iteration"] = proposed.get("iteration")
    result = {
        "kind": kind,
        "milestone_id": None if milestone_current == "none" else milestone_current,
        "route_id": route_identity,
        "iteration_id": proposed.get("iteration"),
    }
    return snapshot, result


def _intake_spec(target: dict[str, Any], confirmed: list[str], route_identity: str | None) -> dict[str, Any]:
    intake = target["intake"]
    return {
        "title": intake["title"],
        "summary": intake["summary"],
        "confirmed_decisions": confirmed,
        "model_recommendations": intake["model_recommendations"],
        "open_questions": intake["open_questions"],
        "in_scope": intake["in_scope"],
        "out_of_scope": intake["out_of_scope"],
        "milestone_route": route_identity,
    }


def _receipt_location(root: Path, promotion_identity: str) -> tuple[Path, Path]:
    directory = root / PROMOTIONS_RELATIVE / promotion_identity
    return directory, directory / "receipt.json"


def _validate_receipt(value: Any) -> dict[str, Any]:
    receipt = _exact(value, {"schema_version", "promotion_id", "request_sha256", "source", "target", "result", "created_at"}, set(), "receipt")
    if type(receipt["schema_version"]) is not int or receipt["schema_version"] != SCHEMA_VERSION:
        _fail("invalid_receipt", f"receipt schema_version must be {SCHEMA_VERSION}")
    identity = _promotion_id(receipt["promotion_id"])
    if not isinstance(receipt["request_sha256"], str) or SHA_RE.fullmatch(receipt["request_sha256"]) is None:
        _fail("invalid_receipt", "receipt.request_sha256 must be SHA-256")
    source = _exact(receipt["source"], {"map_id", "roots", "closure", "slice_sha256", "observed_revision"}, set(), "receipt.source")
    roots = [_decision_id(item) for item in source["roots"]] if isinstance(source["roots"], list) else _fail("invalid_receipt", "receipt.source.roots must be an array")
    closure = [_decision_id(item) for item in source["closure"]] if isinstance(source["closure"], list) else _fail("invalid_receipt", "receipt.source.closure must be an array")
    if roots != sorted(set(roots), key=_identity_number) or closure != sorted(set(closure), key=_identity_number):
        _fail("invalid_receipt", "receipt source identities must be unique and sorted")
    if not isinstance(source["slice_sha256"], str) or SHA_RE.fullmatch(source["slice_sha256"]) is None:
        _fail("invalid_receipt", "receipt.source.slice_sha256 must be SHA-256")
    if type(source["observed_revision"]) is not int or source["observed_revision"] < 1:
        _fail("invalid_receipt", "receipt.source.observed_revision must be positive")
    target = _exact(receipt["target"], {"kind", "milestone_id", "route_id"}, set(), "receipt.target")
    kind = target["kind"]
    milestone = _optional_identity(target["milestone_id"], _milestone_id, "receipt.target.milestone_id")
    route = _optional_identity(target["route_id"], _route_id, "receipt.target.route_id")
    result = receipt["result"]
    if kind == "route-reference":
        if milestone is None or route is None:
            _fail("invalid_receipt", "route-reference receipt requires milestone and route")
        _exact(result, {"kind", "milestone_id", "route_id"}, set(), "receipt.result")
        if result["kind"] != kind:
            _fail("invalid_receipt", "receipt result kind does not match target")
        normalized_result = {"kind": kind, "milestone_id": _milestone_id(result["milestone_id"]), "route_id": _route_id(result["route_id"])}
    elif kind == "iteration-start":
        if (milestone is None) != (route is None):
            _fail("invalid_receipt", "iteration-start target identities must both be null or present")
        _exact(result, {"kind", "milestone_id", "route_id", "iteration_id"}, set(), "receipt.result")
        if result["kind"] != kind:
            _fail("invalid_receipt", "receipt result kind does not match target")
        normalized_result = {
            "kind": kind,
            "milestone_id": _optional_identity(result["milestone_id"], _milestone_id, "receipt.result.milestone_id"),
            "route_id": _optional_identity(result["route_id"], _route_id, "receipt.result.route_id"),
            "iteration_id": _iteration_id(result["iteration_id"]),
        }
    else:
        _fail("invalid_receipt", "unsupported receipt target kind")
    _parse_utc(receipt["created_at"], "receipt.created_at")
    if normalized_result["milestone_id"] != milestone or normalized_result["route_id"] != route:
        _fail("receipt_binding_mismatch", "receipt result target does not match receipt target")
    return {
        "schema_version": SCHEMA_VERSION,
        "promotion_id": identity,
        "request_sha256": receipt["request_sha256"],
        "source": {
            "map_id": _map_id(source["map_id"]),
            "roots": roots,
            "closure": closure,
            "slice_sha256": source["slice_sha256"],
            "observed_revision": source["observed_revision"],
        },
        "target": {"kind": kind, "milestone_id": milestone, "route_id": route},
        "result": normalized_result,
        "created_at": receipt["created_at"],
    }


def _read_receipt(root: Path, promotion_identity: str, *, missing_ok: bool = False) -> dict[str, Any] | None:
    directory, path = _receipt_location(root, promotion_identity)
    if not directory.exists():
        if missing_ok and not directory.is_symlink():
            return None
        _conflict("promotion_not_found", f"promotion receipt does not exist: {promotion_identity}")
    if directory.is_symlink() or not directory.is_dir():
        _fail("unsafe_path", f"promotion directory must be real: {directory}")
    data = _regular_bytes(path, "promotion receipt")
    assert data is not None
    receipt = _validate_receipt(_decode_json(data, str(path)))
    if receipt["promotion_id"] != promotion_identity:
        _fail("receipt_binding_mismatch", f"receipt identity does not match directory: {promotion_identity}")
    if data != _canonical_json(receipt):
        _fail("noncanonical_receipt", f"receipt is not canonical JSON: {promotion_identity}")
    return receipt


def _discover_receipts(root: Path) -> list[str]:
    base = root / PROMOTIONS_RELATIVE
    if not base.exists():
        if base.is_symlink():
            _fail("unsafe_path", f"promotion root must be real: {base}")
        return []
    if base.is_symlink() or not base.is_dir():
        _fail("unsafe_path", f"promotion root must be a real directory: {base}")
    identities: list[str] = []
    for entry in sorted(base.iterdir(), key=lambda item: item.name):
        if entry.name.startswith(".tmp-"):
            continue
        try:
            identities.append(_promotion_id(entry.name))
        except DecisionPromotionError:
            _fail("unexpected_promotion_entry", f"unexpected promotion entry: {entry.name}")
    return sorted(identities, key=_identity_number)


def _make_receipt(request: dict[str, Any], request_sha: str, source: dict[str, Any], result: dict[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "promotion_id": request["promotion_id"],
        "request_sha256": request_sha,
        "source": {
            "map_id": source["map_id"],
            "roots": source["roots"],
            "closure": source["closure"],
            "slice_sha256": source["slice_sha256"],
            "observed_revision": source["observed_revision"],
        },
        "target": {
            "kind": request["target"]["kind"],
            "milestone_id": request["target"].get("milestone_id"),
            "route_id": request["target"].get("route_id"),
        },
        "result": result,
        "created_at": created_at,
    }


def _make_pending(request: dict[str, Any], request_sha: str, source: dict[str, Any], result: dict[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "promotion_id": request["promotion_id"],
        "request_sha256": request_sha,
        "source_slice_sha256": source["slice_sha256"],
        "target": {
            "kind": request["target"]["kind"],
            "milestone_id": request["target"].get("milestone_id"),
            "route_id": request["target"].get("route_id"),
        },
        "result": result,
        "created_at": created_at,
    }


def _validate_pending(value: Any) -> dict[str, Any]:
    pending = _exact(
        value,
        {"schema_version", "promotion_id", "request_sha256", "source_slice_sha256", "target", "result", "created_at"},
        set(),
        "pending promotion",
    )
    if type(pending["schema_version"]) is not int or pending["schema_version"] != SCHEMA_VERSION:
        _fail("invalid_pending", f"pending schema_version must be {SCHEMA_VERSION}")
    identity = _promotion_id(pending["promotion_id"])
    for field in ("request_sha256", "source_slice_sha256"):
        if not isinstance(pending[field], str) or SHA_RE.fullmatch(pending[field]) is None:
            _fail("invalid_pending", f"pending.{field} must be SHA-256")
    target = _exact(pending["target"], {"kind", "milestone_id", "route_id"}, set(), "pending.target")
    if target["kind"] != "iteration-start":
        _fail("invalid_pending", "only iteration-start may have a pending journal")
    milestone = _optional_identity(target["milestone_id"], _milestone_id, "pending.target.milestone_id")
    route = _optional_identity(target["route_id"], _route_id, "pending.target.route_id")
    if (milestone is None) != (route is None):
        _fail("invalid_pending", "pending target identities must both be null or present")
    result = _exact(pending["result"], {"kind", "milestone_id", "route_id", "iteration_id"}, set(), "pending.result")
    if result["kind"] != "iteration-start":
        _fail("invalid_pending", "pending result kind must be iteration-start")
    result_milestone = _optional_identity(result["milestone_id"], _milestone_id, "pending.result.milestone_id")
    result_route = _optional_identity(result["route_id"], _route_id, "pending.result.route_id")
    if result_milestone != milestone or result_route != route:
        _fail("invalid_pending", "pending result target does not match target")
    normalized = {
        "schema_version": SCHEMA_VERSION,
        "promotion_id": identity,
        "request_sha256": pending["request_sha256"],
        "source_slice_sha256": pending["source_slice_sha256"],
        "target": {"kind": "iteration-start", "milestone_id": milestone, "route_id": route},
        "result": {"kind": "iteration-start", "milestone_id": result_milestone, "route_id": result_route, "iteration_id": _iteration_id(result["iteration_id"])},
        "created_at": _parse_utc(pending["created_at"], "pending.created_at"),
    }
    return normalized


def _pending_location(root: Path, promotion_identity: str) -> Path:
    return root / PENDING_RELATIVE / f"{promotion_identity}.json"


def _read_pending(root: Path, promotion_identity: str, *, missing_ok: bool = False) -> dict[str, Any] | None:
    path = _pending_location(root, promotion_identity)
    base = path.parent
    if not base.exists():
        if missing_ok and not base.is_symlink():
            return None
        _fail("missing_state", f"missing pending promotion root: {base}", 1)
    if base.is_symlink() or not base.is_dir():
        _fail("unsafe_path", f"pending promotion root must be a real directory: {base}")
    data = _regular_bytes(path, "pending promotion", missing_ok=missing_ok)
    if data is None:
        return None
    pending = _validate_pending(_decode_json(data, str(path)))
    if pending["promotion_id"] != promotion_identity:
        _fail("pending_binding_mismatch", f"pending identity does not match filename: {promotion_identity}")
    if data != _canonical_json(pending):
        _fail("noncanonical_pending", f"pending journal is not canonical JSON: {promotion_identity}")
    return pending


def _publish_pending(root: Path, pending: dict[str, Any]) -> None:
    normalized = _validate_pending(pending)
    base = root / PENDING_RELATIVE
    if base.exists():
        if base.is_symlink() or not base.is_dir():
            _fail("unsafe_path", f"pending promotion root must be a real directory: {base}")
    else:
        base.mkdir(mode=0o700)
    target = base / f"{normalized['promotion_id']}.json"
    if target.exists() or target.is_symlink():
        _conflict("incomplete_promotion", f"pending promotion already exists: {normalized['promotion_id']}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{normalized['promotion_id']}.", suffix=".tmp", dir=base)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json(normalized))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        _fsync_directory(base)
    finally:
        if temporary.exists():
            temporary.unlink()


def _remove_pending(root: Path, promotion_identity: str) -> None:
    path = _pending_location(root, promotion_identity)
    base = path.parent
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or not path.is_file():
        _fail("unsafe_path", f"pending promotion must be a regular file: {path}")
    path.unlink()
    _fsync_directory(base)
    try:
        base.rmdir()
    except OSError:
        pass


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _publish_receipt(root: Path, receipt: dict[str, Any]) -> None:
    base = root / PROMOTIONS_RELATIVE
    if base.exists():
        if base.is_symlink() or not base.is_dir():
            _fail("unsafe_path", f"promotion root must be a real directory: {base}")
    else:
        base.mkdir(mode=0o755)
    target = base / receipt["promotion_id"]
    if target.exists() or target.is_symlink():
        _conflict("promotion_exists", f"promotion already exists: {receipt['promotion_id']}")
    staging = Path(tempfile.mkdtemp(prefix=f".tmp-{receipt['promotion_id']}-", dir=base))
    published = False
    try:
        path = staging / "receipt.json"
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json(_validate_receipt(receipt)))
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(staging)
        os.rename(staging, target)
        published = True
        _fsync_directory(base)
    finally:
        if not published and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


@contextmanager
def _promotion_lock(root: Path) -> Iterator[None]:
    try:
        root_descriptor = os.open(root, os.O_RDONLY)
    except OSError as error:
        _fail("lock_error", f"cannot open project root guard: {error}")
    try:
        try:
            fcntl.flock(root_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _conflict("promotion_busy", "another promotion apply is active")
    except Exception:
        os.close(root_descriptor)
        raise
    descriptor: int | None = None
    try:
        path = root / LOCK_RELATIVE
        if path.is_symlink():
            _fail("unsafe_lock", f"promotion lock must not be a symlink: {path}")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(path, flags, 0o600)
        except OSError as error:
            _fail("lock_error", f"cannot open promotion lock: {error}")
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            _fail("unsafe_lock", f"promotion lock must be a regular file: {path}")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _conflict("promotion_busy", "another promotion apply is active")
        yield
    finally:
        try:
            if descriptor is not None:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            if descriptor is not None:
                os.close(descriptor)
            try:
                fcntl.flock(root_descriptor, fcntl.LOCK_UN)
            finally:
                os.close(root_descriptor)


def _validate_plan(value: Any) -> dict[str, Any]:
    planned = _exact(
        value,
        {"schema_version", "status", "action", "promotion_id", "request_sha256", "source_slice_sha256", "target_sha256", "planned_at", "request", "effect"},
        set(),
        "plan",
    )
    if type(planned["schema_version"]) is not int or planned["schema_version"] != PLAN_SCHEMA_VERSION or planned["status"] != "ok" or planned["action"] != "apply":
        _fail("invalid_plan", "unsupported plan schema or action")
    request = _validate_request(copy.deepcopy(planned["request"]))
    if _promotion_id(planned["promotion_id"]) != request["promotion_id"]:
        _fail("invalid_plan", "plan promotion_id does not match request")
    for field in ("request_sha256", "source_slice_sha256", "target_sha256"):
        if not isinstance(planned[field], str) or SHA_RE.fullmatch(planned[field]) is None:
            _fail("invalid_plan", f"plan.{field} must be SHA-256")
    if planned["request_sha256"] != _sha(request):
        _fail("plan_digest_mismatch", "plan request digest does not match request")
    _parse_utc(planned["planned_at"], "plan.planned_at")
    if not isinstance(planned["effect"], dict):
        _fail("invalid_plan", "plan.effect must be an object")
    return {**planned, "request": request}


def inspect(
    project_root: str | Path,
    promotion_id: str | None = None,
    milestone_id: str | None = None,
    route_id: str | None = None,
    now: str | dt.datetime | None = None,
) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    observed = _now(now)
    promotion = _promotion_id(promotion_id) if promotion_id is not None else None
    milestone = _milestone_id(milestone_id) if milestone_id is not None else None
    route = _route_id(route_id) if route_id is not None else None
    if (milestone is None) != (route is None):
        _fail("invalid_filter", "milestone_id and route_id filters must be used together")
    identities = [promotion] if promotion is not None else _discover_receipts(root)
    receipts = []
    for identity in identities:
        receipt = _read_receipt(root, identity)
        assert receipt is not None
        if milestone is not None and (receipt["target"]["milestone_id"] != milestone or receipt["target"]["route_id"] != route):
            continue
        receipts.append(receipt)
    return {"schema_version": SCHEMA_VERSION, "status": "ok", "action": "inspect", "observed_at": observed, "receipts": receipts}


def plan(project_root: str | Path, request: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    normalized = _validate_request(copy.deepcopy(request))
    request_sha = _sha(normalized)
    if _read_pending(root, normalized["promotion_id"], missing_ok=True) is not None:
        _conflict("incomplete_promotion", f"pending promotion requires inspection: {normalized['promotion_id']}")
    existing = _read_receipt(root, normalized["promotion_id"], missing_ok=True)
    if existing is not None:
        if existing["request_sha256"] != request_sha:
            _conflict("promotion_id_conflict", f"promotion_id already used for another request: {normalized['promotion_id']}")
        effect = copy.deepcopy(existing["result"])
        effect["idempotent"] = True
        return {
            "schema_version": PLAN_SCHEMA_VERSION,
            "status": "ok",
            "action": "apply",
            "promotion_id": normalized["promotion_id"],
            "request_sha256": request_sha,
            "source_slice_sha256": existing["source"]["slice_sha256"],
            "target_sha256": _sha(existing["target"]),
            "planned_at": _now(now),
            "request": normalized,
            "effect": effect,
        }
    source = _source_slice(root, normalized["source"])
    target_snapshot, effect = _target_snapshot(root, normalized["target"])
    effect["source"] = {
        "map_id": source["map_id"],
        "roots": source["roots"],
        "closure": source["closure"],
        "slice_sha256": source["slice_sha256"],
    }
    effect["idempotent"] = False
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "status": "ok",
        "action": "apply",
        "promotion_id": normalized["promotion_id"],
        "request_sha256": request_sha,
        "source_slice_sha256": source["slice_sha256"],
        "target_sha256": _sha(target_snapshot),
        "planned_at": _now(now),
        "request": normalized,
        "effect": effect,
    }


def _inject_source_reference(ai: Path, request: dict[str, Any], source: dict[str, Any]) -> None:
    path = ai / "CONCEPT.md"
    data = _regular_bytes(path, "CONCEPT.md")
    assert data is not None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        _fail("invalid_encoding", f"CONCEPT.md must be UTF-8: {error}")
    marker = "## Current Understanding\n\n"
    if text.count(marker) != 1:
        _fail("invalid_concept", "CONCEPT.md lacks one Current Understanding section")
    receipt_path = f".ai/decision-promotions/{request['promotion_id']}/receipt.json"
    roots = ", ".join(source["roots"])
    reference = f"- Promotion Source：`{request['promotion_id']}` 引用 `{source['map_id']}` roots `{roots}`；不可变回执：`{receipt_path}`。\n"
    path.write_text(text.replace(marker, marker + reference, 1), encoding="utf-8")


def apply(project_root: str | Path, planned: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, ai = _resolve_root(project_root)
    normalized = _validate_plan(copy.deepcopy(planned))
    request = normalized["request"]
    with _promotion_lock(root):
        if _read_pending(root, request["promotion_id"], missing_ok=True) is not None:
            _conflict("incomplete_promotion", f"pending promotion requires inspection: {request['promotion_id']}")
        existing = _read_receipt(root, request["promotion_id"], missing_ok=True)
        if existing is not None:
            if existing["request_sha256"] != normalized["request_sha256"]:
                _conflict("promotion_id_conflict", f"promotion_id already used for another request: {request['promotion_id']}")
            result = copy.deepcopy(existing["result"])
            result["idempotent"] = True
            return result
        try:
            source = _source_slice(root, request["source"])
            target_snapshot, result = _target_snapshot(root, request["target"])
        except DecisionPromotionError as error:
            if error.exit_code == 1:
                _conflict("stale_plan", "promotion source or target changed after plan; create a new plan")
            raise
        if source["slice_sha256"] != normalized["source_slice_sha256"] or _sha(target_snapshot) != normalized["target_sha256"]:
            _conflict("stale_plan", "promotion source or target changed after plan; create a new plan")
        created_at = _now(now)
        result = copy.deepcopy(result)
        if request["target"]["kind"] == "route-reference":
            receipt = _make_receipt(request, normalized["request_sha256"], source, result, created_at)
            _publish_receipt(root, receipt)
        else:
            intake_spec = _intake_spec(request["target"], source["confirmed_decisions"], request["target"]["route_id"])
            expected_iteration = result["iteration_id"]

            def after_write() -> None:
                _inject_source_reference(ai, request, source)
                receipt = _make_receipt(request, normalized["request_sha256"], source, result, created_at)
                _publish_receipt(root, receipt)

            pending = _make_pending(request, normalized["request_sha256"], source, result, created_at)
            _publish_pending(root, pending)
            try:
                try:
                    applied = ITERATION_INTAKE.apply(root, intake_spec, after_write=after_write)
                except ITERATION_INTAKE.IntakeError as error:
                    _conflict("intake_failed", str(error))
            finally:
                _remove_pending(root, request["promotion_id"])
            if applied.get("iteration") != expected_iteration:
                _fail("intake_result_mismatch", "iteration-intake allocated an unexpected identity")
        stored = _read_receipt(root, request["promotion_id"])
        assert stored is not None
        output = copy.deepcopy(stored["result"])
        output["idempotent"] = False
        return output


def _milestone_document(root: Path, milestone: str) -> Path:
    ai = root / ".ai"
    current = _current(ai / "MILESTONES.md", "MILESTONES.md")
    if current == milestone:
        return ai / "MILESTONE.md"
    return ai / "milestones" / milestone / "MILESTONE.md"


def _verify_target(root: Path, receipt: dict[str, Any]) -> None:
    target = receipt["target"]
    if target["kind"] == "route-reference":
        document = _milestone_document(root, target["milestone_id"])
        _route(document, target["route_id"])
        return
    try:
        exit_code, lookup = STATE_LEDGER.lookup(root, receipt["result"]["iteration_id"])
    except STATE_LEDGER.Error as error:
        _fail("invalid_iteration_ledger", str(error))
    if exit_code != 0 or lookup.get("status") != "found":
        _conflict("iteration_not_found", f"promoted Iteration is missing: {receipt['result']['iteration_id']}")


def _incomplete_markers(root: Path, known: set[str]) -> list[str]:
    candidates = [root / ".ai/CONCEPT.md"]
    archive = root / ".ai/iterations"
    if archive.exists() and not archive.is_symlink() and archive.is_dir():
        candidates.extend(sorted(archive.glob("ITER-*/CONCEPT.md")))
    missing: set[str] = set()
    pattern = re.compile(r"Promotion Source：`(PROM-[0-9]{4,})`")
    for path in candidates:
        if not path.exists() or path.is_symlink() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for identity in pattern.findall(text):
            if identity not in known:
                missing.add(identity)
    return sorted(missing, key=_identity_number)


def verify(project_root: str | Path, promotion_id: str | None = None, now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    observed = _now(now)
    errors: list[dict[str, str]] = []
    checked: list[dict[str, Any]] = []
    identities: list[str] = []
    if promotion_id is not None:
        identities = [_promotion_id(promotion_id)]
    else:
        base = root / PROMOTIONS_RELATIVE
        if base.exists():
            if base.is_symlink() or not base.is_dir():
                errors.append({"code": "unsafe_path", "message": f"promotion root must be a real directory: {base}"})
            else:
                for entry in sorted(base.iterdir(), key=lambda item: item.name):
                    if entry.name.startswith(".tmp-"):
                        errors.append({"code": "stale_staging", "message": f"stale promotion staging entry: {entry.name}"})
                        continue
                    try:
                        identities.append(_promotion_id(entry.name))
                    except DecisionPromotionError:
                        errors.append({"code": "unexpected_promotion_entry", "message": f"unexpected promotion entry: {entry.name}"})
    known = set(identities)
    for identity in identities:
        try:
            receipt = _read_receipt(root, identity)
            assert receipt is not None
            source = _source_slice(root, {"map_id": receipt["source"]["map_id"], "decision_ids": receipt["source"]["roots"]})
            if source["closure"] != receipt["source"]["closure"] or source["slice_sha256"] != receipt["source"]["slice_sha256"]:
                _fail("source_slice_mismatch", f"promotion source slice drift: {identity}")
            _verify_target(root, receipt)
            checked.append({"promotion_id": identity, "source_slice_sha256": source["slice_sha256"], "target": receipt["target"], "result": receipt["result"]})
        except DecisionPromotionError as error:
            errors.append({"code": error.code, "message": error.message})
    if promotion_id is None:
        pending_root = root / PENDING_RELATIVE
        if pending_root.exists():
            if pending_root.is_symlink() or not pending_root.is_dir():
                errors.append({"code": "unsafe_path", "message": f"pending promotion root must be a real directory: {pending_root}"})
            else:
                for entry in sorted(pending_root.iterdir(), key=lambda item: item.name):
                    match = re.fullmatch(r"(PROM-[0-9]{4,})\.json", entry.name)
                    if match is None:
                        errors.append({"code": "stale_staging", "message": f"unexpected pending promotion entry: {entry.name}"})
                        continue
                    try:
                        identity = _promotion_id(match.group(1))
                        pending = _read_pending(root, identity)
                        assert pending is not None
                        errors.append({"code": "incomplete_promotion", "message": f"pending iteration-start requires inspection: {identity}"})
                    except DecisionPromotionError as error:
                        errors.append({"code": error.code, "message": error.message})
        for identity in _incomplete_markers(root, known):
            errors.append({"code": "incomplete_promotion", "message": f"CONCEPT references missing promotion receipt: {identity}"})
    checked.sort(key=lambda item: _identity_number(item["promotion_id"]))
    return {"schema_version": SCHEMA_VERSION, "status": "ok" if not errors else "error", "action": "verify", "observed_at": observed, "checked": checked, "errors": errors}
