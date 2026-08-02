#!/usr/bin/env python3
"""Deterministic Decision Work Module.

The external Interface is deliberately limited to inspect, plan, apply, and
verify. Helpers exchange immutable task/result documents; only absorb calls
the Decision Map Module.
"""
from __future__ import annotations

import copy
import datetime as dt
import errno
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any, Iterator, NoReturn


SCHEMA_VERSION = 1
PLAN_SCHEMA_VERSION = 1
MAX_PARALLEL = 8
MAX_TEXT = 8192
MAX_ITEMS = 64
MAX_DOCUMENT_BYTES = 1_048_576
WORK_RELATIVE = Path(".ai/decision-work")
LOCKS_RELATIVE = Path(".ai/.decision-work-locks")

MAP_RE = re.compile(r"^DMAP-[0-9]{4,}$", re.ASCII)
DECISION_RE = re.compile(r"^DEC-[0-9]{4,}$", re.ASCII)
ATTEMPT_RE = re.compile(r"^ATT-[0-9]{4,}$", re.ASCII)
OPERATION_RE = re.compile(r"^OP-[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$", re.ASCII)
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$", re.ASCII)
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", re.ASCII)
POINTER_RE = re.compile(
    r"^decision-work:\.ai/decision-work/(DMAP-[0-9]{4,})/(DEC-[0-9]{4,})/(ATT-[0-9]{4,})/result\.json#(sha256:[0-9a-f]{64})$",
    re.ASCII,
)

WORK_TYPES = {"research", "prototype", "grilling", "task"}
RESULT_STATUSES = {"candidate", "needs_input", "failed", "cancelled"}
EXECUTION_MODES = {"parallel", "serial", "hitl"}
OPERATION_KINDS = {"prepare_attempts", "record_result", "absorb_result"}


class DecisionWorkError(ValueError):
    """Stable machine-readable failure from the Decision Work Interface."""

    def __init__(self, code: str, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_code = exit_code


def _fail(code: str, message: str, exit_code: int = 2) -> NoReturn:
    raise DecisionWorkError(code, message, exit_code)


def _conflict(code: str, message: str) -> NoReturn:
    _fail(code, message, 1)


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
        _fail("invalid_identity", f"expected canonical {prefix}-NNNN identity")
    number = int(value.split("-", 1)[1])
    if number < 1 or value != f"{prefix}-{number:04d}":
        _fail("invalid_identity", f"non-canonical identity: {value}")
    return value


def _map_id(value: Any) -> str:
    return _canonical_identity(value, "DMAP", MAP_RE)


def _decision_id(value: Any) -> str:
    return _canonical_identity(value, "DEC", DECISION_RE)


def _attempt_id(value: Any) -> str:
    return _canonical_identity(value, "ATT", ATTEMPT_RE)


def _operation_id(value: Any) -> str:
    if not isinstance(value, str) or OPERATION_RE.fullmatch(value) is None:
        _fail("invalid_operation_id", "operation_id must match OP-<stable-id>")
    return value


def _nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_field", f"{field} must be a non-empty string")
    normalized = value.strip()
    if len(normalized) > MAX_TEXT:
        _fail("field_too_large", f"{field} exceeds {MAX_TEXT} characters")
    return normalized


def _string_list(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        _fail("invalid_field", f"{field} must be an array of at most {MAX_ITEMS} strings")
    if nonempty and not value:
        _fail("invalid_field", f"{field} must not be empty")
    normalized = [_nonempty(item, f"{field}[]") for item in value]
    if len(set(normalized)) != len(normalized):
        _fail("invalid_field", f"{field} must not contain duplicates")
    return normalized


def _sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    try:
        data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as error:
        _fail("invalid_json_value", str(error))
    if len(data) > MAX_DOCUMENT_BYTES:
        _fail("document_too_large", f"canonical document exceeds {MAX_DOCUMENT_BYTES} bytes")
    return data


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _decode_json(data: bytes, label: str) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        _fail("invalid_json", f"invalid JSON in {label}: {error}")


def _parse_utc(value: Any, field: str) -> dt.datetime:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        _fail("invalid_time", f"{field} must be canonical UTC seconds")
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as error:
        _fail("invalid_time", f"invalid {field}: {error}")


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


def _assert_real_directory(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_dir():
        _fail("unsafe_path", f"{label} must be a real directory: {path}")


def _attempt_directory(root: Path, map_identity: str, decision_identity: str, attempt_identity: str) -> Path:
    return root / WORK_RELATIVE / _map_id(map_identity) / _decision_id(decision_identity) / _attempt_id(attempt_identity)


def _read_canonical(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    if path.is_symlink() or not path.is_file():
        _fail("unsafe_path", f"{label} must be a regular file: {path}")
    data = path.read_bytes()
    if len(data) > MAX_DOCUMENT_BYTES:
        _fail("document_too_large", f"{label} exceeds {MAX_DOCUMENT_BYTES} bytes")
    value = _decode_json(data, label)
    if not isinstance(value, dict):
        _fail("invalid_document", f"{label} must contain an object")
    if data != _canonical_json(value):
        _fail("noncanonical_document", f"{label} is not canonical")
    return value, data


_DECISION_MAP_MODULE: ModuleType | None = None


def _decision_map_module() -> ModuleType:
    global _DECISION_MAP_MODULE
    if _DECISION_MAP_MODULE is not None:
        return _DECISION_MAP_MODULE
    path = Path(__file__).resolve().parents[1] / "decision-map" / "engine.py"
    spec = importlib.util.spec_from_file_location("butler_decision_map_engine_for_work", path)
    if spec is None or spec.loader is None:
        _fail("decision_map_unavailable", f"cannot load Decision Map Module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for action in ("inspect", "plan", "apply", "verify"):
        if not callable(getattr(module, action, None)):
            _fail("decision_map_unavailable", f"Decision Map Interface missing: {action}")
    _DECISION_MAP_MODULE = module
    return module


def _r2_call(action: str, *args: Any) -> dict[str, Any]:
    module = _decision_map_module()
    try:
        return getattr(module, action)(*args)
    except module.DecisionMapError as error:
        raise DecisionWorkError(f"decision_map_{error.code}", error.message, error.exit_code) from error


def _map_view(root: Path, map_identity: str, now_text: str) -> dict[str, Any]:
    return _r2_call("inspect", root, map_identity, now_text)


def _map_sha(view: dict[str, Any]) -> str:
    return _sha(_canonical_json(view["state"]))


def _validate_member(value: Any, field: str) -> dict[str, str]:
    item = _exact(value, {"decision_id", "attempt_id"}, set(), field)
    return {"decision_id": _decision_id(item["decision_id"]), "attempt_id": _attempt_id(item["attempt_id"])}


def _validate_task(value: Any, *, expected: tuple[str, str, str] | None = None) -> dict[str, Any]:
    task = _exact(
        value,
        {
            "schema_version", "map_id", "decision_id", "attempt_id", "work_type", "question",
            "confirmed_context", "constraints", "expected_output", "predecessor_attempt_id",
            "prepare_operation_id", "request_sha256", "map_revision", "map_sha256",
            "claim_operation_id", "claim_owner", "claim_token_sha256", "claim_observed_expires_at",
            "requested_execution_mode", "batch_id", "batch_members", "created_at",
        },
        set(),
        "task",
    )
    if type(task["schema_version"]) is not int or task["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported_schema", "task schema must be 1")
    task["map_id"] = _map_id(task["map_id"])
    task["decision_id"] = _decision_id(task["decision_id"])
    task["attempt_id"] = _attempt_id(task["attempt_id"])
    if expected is not None and tuple(task[key] for key in ("map_id", "decision_id", "attempt_id")) != expected:
        _fail("identity_mismatch", "task identity does not match its directory")
    if task["work_type"] not in WORK_TYPES:
        _fail("invalid_work_type", f"unsupported work type: {task['work_type']}")
    task["question"] = _nonempty(task["question"], "task.question")
    task["confirmed_context"] = _string_list(task["confirmed_context"], "task.confirmed_context")
    task["constraints"] = _string_list(task["constraints"], "task.constraints")
    task["expected_output"] = _string_list(task["expected_output"], "task.expected_output", nonempty=True)
    predecessor = task["predecessor_attempt_id"]
    task["predecessor_attempt_id"] = None if predecessor is None else _attempt_id(predecessor)
    if task["predecessor_attempt_id"] == task["attempt_id"]:
        _fail("invalid_predecessor", "attempt cannot reference itself")
    task["prepare_operation_id"] = _operation_id(task["prepare_operation_id"])
    task["batch_id"] = _operation_id(task["batch_id"])
    for field in ("request_sha256", "map_sha256", "claim_token_sha256"):
        if not isinstance(task[field], str) or SHA_RE.fullmatch(task[field]) is None:
            _fail("invalid_digest", f"task.{field} must be SHA-256")
    if type(task["map_revision"]) is not int or task["map_revision"] < 1:
        _fail("invalid_revision", "task.map_revision must be positive")
    task["claim_operation_id"] = _operation_id(task["claim_operation_id"])
    task["claim_owner"] = _nonempty(task["claim_owner"], "task.claim_owner")
    _parse_utc(task["claim_observed_expires_at"], "task.claim_observed_expires_at")
    _parse_utc(task["created_at"], "task.created_at")
    if task["requested_execution_mode"] not in EXECUTION_MODES:
        _fail("invalid_execution_mode", "unsupported requested execution mode")
    members = [_validate_member(item, f"task.batch_members[{index}]") for index, item in enumerate(task["batch_members"])] if isinstance(task["batch_members"], list) else _fail("invalid_batch", "task.batch_members must be an array")
    keys = [(item["decision_id"], item["attempt_id"]) for item in members]
    if not members or len(members) > MAX_PARALLEL or len(set(keys)) != len(keys) or (task["decision_id"], task["attempt_id"]) not in keys:
        _fail("invalid_batch", "invalid task batch membership")
    if members != sorted(members, key=lambda item: (int(item["decision_id"].split("-")[1]), int(item["attempt_id"].split("-")[1]))):
        _fail("invalid_batch", "task batch members must be numerically sorted")
    task["batch_members"] = members
    if task["work_type"] != "research" and len(members) != 1:
        _fail("invalid_batch", "only research may contain multiple attempts")
    if task["work_type"] != "research" and task["requested_execution_mode"] == "parallel":
        _fail("invalid_execution_mode", "only research may request parallel execution")
    return task


def _validate_candidate_payload(work_type: str, value: Any) -> dict[str, Any]:
    if work_type == "research":
        payload = _exact(value, {"findings", "sources", "uncertainties"}, set(), "research payload")
        return {"findings": _string_list(payload["findings"], "payload.findings", nonempty=True), "sources": _string_list(payload["sources"], "payload.sources", nonempty=True), "uncertainties": _string_list(payload["uncertainties"], "payload.uncertainties")}
    if work_type == "prototype":
        payload = _exact(value, {"artifacts", "observations", "human_evaluation"}, set(), "prototype payload")
        return {"artifacts": _string_list(payload["artifacts"], "payload.artifacts", nonempty=True), "observations": _string_list(payload["observations"], "payload.observations", nonempty=True), "human_evaluation": _nonempty(payload["human_evaluation"], "payload.human_evaluation")}
    if work_type == "grilling":
        payload = _exact(value, {"questions", "human_answers", "assumptions", "tradeoffs", "self_answered"}, set(), "grilling payload")
        if type(payload["self_answered"]) is not bool or payload["self_answered"]:
            _fail("self_answered_grilling", "grilling candidate requires real human answers")
        return {"questions": _string_list(payload["questions"], "payload.questions", nonempty=True), "human_answers": _string_list(payload["human_answers"], "payload.human_answers", nonempty=True), "assumptions": _string_list(payload["assumptions"], "payload.assumptions"), "tradeoffs": _string_list(payload["tradeoffs"], "payload.tradeoffs", nonempty=True), "self_answered": False}
    payload = _exact(value, {"action", "evidence", "unblocked"}, set(), "task payload")
    if type(payload["unblocked"]) is not bool:
        _fail("invalid_field", "payload.unblocked must be boolean")
    return {"action": _nonempty(payload["action"], "payload.action"), "evidence": _string_list(payload["evidence"], "payload.evidence", nonempty=True), "unblocked": payload["unblocked"]}


def _normalize_result(value: Any, work_type: str) -> dict[str, Any]:
    if not isinstance(value, dict) or "status" not in value:
        _fail("invalid_result", "result.status is required")
    status = value["status"]
    common = {"status", "actual_execution_mode", "fresh_context"}
    if status == "candidate":
        result = _exact(value, common | {"outcome", "rationale", "evidence", "payload"}, set(), "candidate result")
        result["outcome"] = _nonempty(result["outcome"], "result.outcome")
        result["rationale"] = _nonempty(result["rationale"], "result.rationale")
        result["evidence"] = _string_list(result["evidence"], "result.evidence")
        result["payload"] = _validate_candidate_payload(work_type, result["payload"])
    elif status == "needs_input":
        result = _exact(value, common | {"questions", "artifact_pointers"}, set(), "needs_input result")
        result["questions"] = _string_list(result["questions"], "result.questions")
        result["artifact_pointers"] = _string_list(result["artifact_pointers"], "result.artifact_pointers")
        if not result["questions"] and not result["artifact_pointers"]:
            _fail("invalid_result", "needs_input requires questions or artifact pointers")
    elif status == "failed":
        result = _exact(value, common | {"error_code", "error_summary"}, set(), "failed result")
        result["error_code"] = _nonempty(result["error_code"], "result.error_code")
        result["error_summary"] = _nonempty(result["error_summary"], "result.error_summary")
    elif status == "cancelled":
        result = _exact(value, common | {"reason"}, set(), "cancelled result")
        result["reason"] = _nonempty(result["reason"], "result.reason")
    else:
        _fail("invalid_result_status", f"unsupported result status: {status}")
    if result["actual_execution_mode"] not in EXECUTION_MODES:
        _fail("invalid_execution_mode", "unsupported actual execution mode")
    if work_type != "research" and result["actual_execution_mode"] == "parallel":
        _fail("invalid_execution_mode", "only research may report parallel execution")
    if type(result["fresh_context"]) is not bool:
        _fail("invalid_field", "result.fresh_context must be boolean")
    return result


def _validate_result(value: Any, task: dict[str, Any]) -> dict[str, Any]:
    result = _exact(
        value,
        {"schema_version", "map_id", "decision_id", "attempt_id", "task_sha256", "record_operation_id", "request_sha256", "status", "actual_execution_mode", "fresh_context", "submitted_at", "details"},
        set(),
        "result",
    )
    if type(result["schema_version"]) is not int or result["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported_schema", "result schema must be 1")
    for field, validator in (("map_id", _map_id), ("decision_id", _decision_id), ("attempt_id", _attempt_id)):
        result[field] = validator(result[field])
        if result[field] != task[field]:
            _fail("identity_mismatch", f"result.{field} does not match task")
    if not isinstance(result["task_sha256"], str) or SHA_RE.fullmatch(result["task_sha256"]) is None:
        _fail("invalid_digest", "result.task_sha256 must be SHA-256")
    result["record_operation_id"] = _operation_id(result["record_operation_id"])
    if not isinstance(result["request_sha256"], str) or SHA_RE.fullmatch(result["request_sha256"]) is None:
        _fail("invalid_digest", "result.request_sha256 must be SHA-256")
    _parse_utc(result["submitted_at"], "result.submitted_at")
    normalized = _normalize_result({"status": result["status"], "actual_execution_mode": result["actual_execution_mode"], "fresh_context": result["fresh_context"], **result["details"]}, task["work_type"])
    result["status"] = normalized.pop("status")
    result["actual_execution_mode"] = normalized.pop("actual_execution_mode")
    result["fresh_context"] = normalized.pop("fresh_context")
    result["details"] = normalized
    request_spec = {
        "schema_version": SCHEMA_VERSION,
        "operation_id": result["record_operation_id"],
        "operation": {
            "kind": "record_result",
            "map_id": result["map_id"],
            "decision_id": result["decision_id"],
            "attempt_id": result["attempt_id"],
            "task_sha256": result["task_sha256"],
            "result": {
                "status": result["status"],
                "actual_execution_mode": result["actual_execution_mode"],
                "fresh_context": result["fresh_context"],
                **result["details"],
            },
        },
    }
    if result["request_sha256"] != _request_digest(result["map_id"], request_spec):
        _fail("result_request_mismatch", "result content does not bind its record request")
    return result


def _read_attempt(root: Path, map_identity: str, decision_identity: str, attempt_identity: str) -> tuple[dict[str, Any], bytes, dict[str, Any] | None, bytes | None]:
    directory = _attempt_directory(root, map_identity, decision_identity, attempt_identity)
    _assert_real_directory(directory, "Decision Work attempt directory")
    entries = {item.name for item in directory.iterdir()}
    if not entries <= {"task.json", "result.json"} or "task.json" not in entries:
        _fail("unexpected_attempt_entry", f"invalid entries in {map_identity}/{decision_identity}/{attempt_identity}")
    task, task_data = _read_canonical(directory / "task.json", "task.json")
    task = _validate_task(task, expected=(map_identity, decision_identity, attempt_identity))
    result = None
    result_data = None
    if "result.json" in entries:
        result, result_data = _read_canonical(directory / "result.json", "result.json")
        result = _validate_result(result, task)
        if result["task_sha256"] != _sha(task_data):
            _fail("task_digest_mismatch", "result does not bind current task bytes")
    return task, task_data, result, result_data


def _result_pointer(task: dict[str, Any], result_data: bytes) -> str:
    relative = WORK_RELATIVE / task["map_id"] / task["decision_id"] / task["attempt_id"] / "result.json"
    return f"decision-work:{relative.as_posix()}#{_sha(result_data)}"


def _validate_task_binding(task: dict[str, Any], view: dict[str, Any]) -> None:
    state = view["state"]
    decision = state.get("decisions", {}).get(task["decision_id"])
    if decision is None:
        _fail("dangling_decision", f"task references missing Decision: {task['map_id']}/{task['decision_id']}")
    if task["question"] != decision["question"]:
        _fail("task_binding_mismatch", f"task question no longer binds Decision: {task['map_id']}/{task['decision_id']}/{task['attempt_id']}")
    claim_receipt = state.get("applied_operations", {}).get(task["claim_operation_id"])
    claim_result = claim_receipt.get("result", {}) if isinstance(claim_receipt, dict) else {}
    if (
        claim_result.get("kind") != "claim"
        or claim_result.get("decision_id") != task["decision_id"]
        or claim_result.get("owner") != task["claim_owner"]
        or _sha(str(claim_result.get("token", "")).encode()) != task["claim_token_sha256"]
        or claim_result.get("expires_at") != task["claim_observed_expires_at"]
    ):
        _fail("task_binding_mismatch", f"task no longer binds its claim receipt: {task['map_id']}/{task['decision_id']}/{task['attempt_id']}")


def _derive(task: dict[str, Any], result: dict[str, Any] | None, result_data: bytes | None, view: dict[str, Any], current: dt.datetime) -> dict[str, Any]:
    state = view["state"]
    decision = state.get("decisions", {}).get(task["decision_id"])
    pointer = _result_pointer(task, result_data) if result is not None and result_data is not None else None
    absorbed = bool(decision and decision.get("status") == "resolved" and pointer in (decision.get("resolution") or {}).get("evidence", []))
    effective = view.get("effective_claims", {}).get(task["decision_id"])
    current_claim = bool(effective and effective.get("owner") == task["claim_owner"] and _sha(effective.get("token", "").encode()) == task["claim_token_sha256"])
    dependencies_ready = bool(decision and all(state["decisions"].get(item, {}).get("status") == "resolved" for item in decision.get("depends_on", [])))
    relation = "absorbed" if absorbed else "current" if decision and decision.get("status") == "open" and current_claim and dependencies_ready else "stale"
    if result is None:
        expiry = _parse_utc(effective["expires_at"], "claim.expires_at") if current_claim else _parse_utc(task["claim_observed_expires_at"], "task.claim_observed_expires_at")
        lifecycle = "pending" if relation == "current" and current < expiry else "expired"
        timeliness = "N/A"
        status = None
    else:
        lifecycle = "recorded"
        timeliness = "on_time" if _parse_utc(result["submitted_at"], "result.submitted_at") < _parse_utc(task["claim_observed_expires_at"], "task.claim_observed_expires_at") else "late"
        status = result["status"]
    absorbable = status == "candidate" and relation == "current"
    reason = "ok" if absorbable else "already_absorbed" if absorbed else "no_result" if result is None else "result_not_candidate" if status != "candidate" else "stale_work"
    return {"result_status": status, "lifecycle": lifecycle, "timeliness": timeliness, "relation": relation, "absorbable": absorbable, "absorbability_code": reason, "evidence_pointer": pointer}


def _discover_attempts(root: Path, map_id: str | None = None, decision_id: str | None = None, attempt_id: str | None = None, *, strict: bool = True) -> list[tuple[str, str, str]]:
    base = root / WORK_RELATIVE
    if not base.exists():
        return []
    _assert_real_directory(base, "Decision Work root")
    found: list[tuple[str, str, str]] = []
    for map_path in base.iterdir():
        if map_path.name.startswith(".tmp-"):
            if strict:
                _fail("stale_staging", f"stale Decision Work staging: {map_path.name}")
            continue
        try:
            mid = _map_id(map_path.name)
        except DecisionWorkError:
            if strict:
                _fail("unexpected_work_entry", f"unexpected Decision Work entry: {map_path.name}")
            continue
        if map_id is not None and mid != _map_id(map_id):
            continue
        _assert_real_directory(map_path, "Decision Work Map directory")
        for decision_path in map_path.iterdir():
            try:
                did = _decision_id(decision_path.name)
            except DecisionWorkError:
                if strict:
                    _fail("unexpected_work_entry", f"unexpected Decision entry: {decision_path.name}")
                continue
            if decision_id is not None and did != _decision_id(decision_id):
                continue
            _assert_real_directory(decision_path, "Decision Work Decision directory")
            for attempt_path in decision_path.iterdir():
                if attempt_path.name.startswith(".tmp-"):
                    if strict:
                        _fail("stale_staging", f"stale attempt staging: {attempt_path.name}")
                    continue
                try:
                    aid = _attempt_id(attempt_path.name)
                except DecisionWorkError:
                    if strict:
                        _fail("unexpected_work_entry", f"unexpected Attempt entry: {attempt_path.name}")
                    continue
                if attempt_id is not None and aid != _attempt_id(attempt_id):
                    continue
                found.append((mid, did, aid))
    return sorted(found, key=lambda item: tuple(int(value.split("-")[1]) for value in item))


def inspect(project_root: str | Path, map_id: str | None = None, decision_id: str | None = None, attempt_id: str | None = None, now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    current, now_text = _now(now)
    if attempt_id is not None and (map_id is None or decision_id is None):
        _fail("invalid_filter", "attempt_id requires map_id and decision_id")
    if decision_id is not None and map_id is None:
        _fail("invalid_filter", "decision_id requires map_id")
    views: dict[str, dict[str, Any]] = {}
    attempts: list[dict[str, Any]] = []
    for mid, did, aid in _discover_attempts(root, map_id, decision_id, attempt_id):
        task, _, result, result_data = _read_attempt(root, mid, did, aid)
        if mid not in views:
            views[mid] = _map_view(root, mid, now_text)
        _validate_task_binding(task, views[mid])
        attempts.append({"map_id": mid, "decision_id": did, "attempt_id": aid, "task": task, "result": result, "derived": _derive(task, result, result_data, views[mid], current)})
    return {"schema_version": SCHEMA_VERSION, "status": "ok", "action": "inspect", "observed_at": now_text, "attempts": attempts}


def _normalize_attempt_request(value: Any, index: int) -> dict[str, Any]:
    item = _exact(
        value,
        {"decision_id", "attempt_id", "confirmed_context", "constraints", "expected_output", "claim_operation_id", "claim_owner", "claim_token", "requested_execution_mode"},
        {"predecessor_attempt_id"},
        f"attempts[{index}]",
    )
    item["decision_id"] = _decision_id(item["decision_id"])
    item["attempt_id"] = _attempt_id(item["attempt_id"])
    item["confirmed_context"] = _string_list(item["confirmed_context"], f"attempts[{index}].confirmed_context")
    item["constraints"] = _string_list(item["constraints"], f"attempts[{index}].constraints")
    item["expected_output"] = _string_list(item["expected_output"], f"attempts[{index}].expected_output", nonempty=True)
    item["claim_operation_id"] = _operation_id(item["claim_operation_id"])
    item["claim_owner"] = _nonempty(item["claim_owner"], f"attempts[{index}].claim_owner")
    item["claim_token"] = _nonempty(item["claim_token"], f"attempts[{index}].claim_token")
    if item["requested_execution_mode"] not in EXECUTION_MODES:
        _fail("invalid_execution_mode", "unsupported requested execution mode")
    predecessor = item.get("predecessor_attempt_id")
    item["predecessor_attempt_id"] = None if predecessor is None else _attempt_id(predecessor)
    return item


def _validate_operation_spec(value: Any, map_identity: str) -> dict[str, Any]:
    spec = _exact(value, {"schema_version", "operation_id", "operation"}, set(), "operation spec")
    if type(spec["schema_version"]) is not int or spec["schema_version"] != SCHEMA_VERSION:
        _fail("unsupported_schema", "operation schema must be 1")
    spec["operation_id"] = _operation_id(spec["operation_id"])
    operation = spec["operation"]
    if not isinstance(operation, dict) or operation.get("kind") not in OPERATION_KINDS:
        _fail("invalid_operation", "unsupported operation kind")
    kind = operation["kind"]
    if kind == "prepare_attempts":
        operation = _exact(operation, {"kind", "map_id", "work_type", "attempts"}, {"max_parallel"}, "prepare_attempts")
        operation["map_id"] = _map_id(operation["map_id"])
        if operation["map_id"] != map_identity:
            _fail("identity_mismatch", "operation map_id does not match plan map_id")
        if operation["work_type"] not in WORK_TYPES:
            _fail("invalid_work_type", "unsupported work type")
        if not isinstance(operation["attempts"], list) or not operation["attempts"]:
            _fail("invalid_batch", "prepare_attempts requires at least one attempt")
        operation["attempts"] = [_normalize_attempt_request(item, index) for index, item in enumerate(operation["attempts"])]
        keys = [(item["decision_id"], item["attempt_id"]) for item in operation["attempts"]]
        if len(set(keys)) != len(keys):
            _fail("invalid_batch", "prepare attempts must be unique")
        maximum = operation.get("max_parallel", 1)
        if type(maximum) is not int or not 1 <= maximum <= MAX_PARALLEL:
            _fail("invalid_parallelism", f"max_parallel must be 1..{MAX_PARALLEL}")
        operation["max_parallel"] = maximum
        if len(operation["attempts"]) > maximum:
            _fail("invalid_parallelism", "batch size exceeds max_parallel")
        if operation["work_type"] != "research" and len(operation["attempts"]) != 1:
            _fail("invalid_batch", "only research may prepare multiple attempts")
        if operation["work_type"] != "research" and any(item["requested_execution_mode"] == "parallel" for item in operation["attempts"]):
            _fail("invalid_execution_mode", "only research may request parallel execution")
    elif kind == "record_result":
        operation = _exact(operation, {"kind", "map_id", "decision_id", "attempt_id", "task_sha256", "result"}, set(), "record_result")
        operation["map_id"] = _map_id(operation["map_id"])
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["attempt_id"] = _attempt_id(operation["attempt_id"])
        if operation["map_id"] != map_identity:
            _fail("identity_mismatch", "operation map_id does not match plan map_id")
        if not isinstance(operation["task_sha256"], str) or SHA_RE.fullmatch(operation["task_sha256"]) is None:
            _fail("invalid_digest", "task_sha256 must be SHA-256")
        if not isinstance(operation["result"], dict):
            _fail("invalid_result", "record_result.result must be an object")
    else:
        operation = _exact(operation, {"kind", "map_id", "decision_id", "attempt_id", "owner", "token", "resolve_operation_id"}, set(), "absorb_result")
        operation["map_id"] = _map_id(operation["map_id"])
        operation["decision_id"] = _decision_id(operation["decision_id"])
        operation["attempt_id"] = _attempt_id(operation["attempt_id"])
        if operation["map_id"] != map_identity:
            _fail("identity_mismatch", "operation map_id does not match plan map_id")
        operation["owner"] = _nonempty(operation["owner"], "operation.owner")
        operation["token"] = _nonempty(operation["token"], "operation.token")
        operation["resolve_operation_id"] = _operation_id(operation["resolve_operation_id"])
    spec["operation"] = operation
    return spec


def _request_digest(map_identity: str, spec: dict[str, Any]) -> str:
    return _sha(_canonical_json({"map_id": map_identity, "spec": spec}))


def _predecessor(root: Path, map_identity: str, decision_identity: str, predecessor: str | None, successor: str) -> None:
    if predecessor is None:
        return
    task, _, result, _ = _read_attempt(root, map_identity, decision_identity, predecessor)
    if result is None or result["status"] != "needs_input":
        _conflict("invalid_predecessor", "predecessor must have a needs_input result")
    for mid, did, aid in _discover_attempts(root, map_identity, decision_identity):
        if aid == successor:
            continue
        other, _, _, _ = _read_attempt(root, mid, did, aid)
        if other["predecessor_attempt_id"] == predecessor:
            _conflict("predecessor_already_continued", f"predecessor already has successor: {aid}")


def _prepare_documents(root: Path, map_identity: str, spec: dict[str, Any], request_sha: str, now_text: str, *, created_at: str | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    operation = spec["operation"]
    view = _map_view(root, map_identity, now_text)
    state = view["state"]
    if state["status"] != "open":
        _conflict("map_closed", "closed Decision Map cannot prepare work")
    members = sorted(({"decision_id": item["decision_id"], "attempt_id": item["attempt_id"]} for item in operation["attempts"]), key=lambda item: (int(item["decision_id"].split("-")[1]), int(item["attempt_id"].split("-")[1])))
    timestamp = created_at or now_text
    documents: list[dict[str, Any]] = []
    for item in operation["attempts"]:
        identity = item["decision_id"]
        decision = state["decisions"].get(identity)
        if decision is None or decision["status"] != "open" or not all(state["decisions"].get(dep, {}).get("status") == "resolved" for dep in decision.get("depends_on", [])):
            _conflict("decision_not_work_ready", f"Decision is not work-ready: {identity}")
        claim = view.get("effective_claims", {}).get(identity)
        if claim is None or claim["owner"] != item["claim_owner"] or claim["token"] != item["claim_token"]:
            _conflict("claim_mismatch", f"current Claim does not match: {identity}")
        receipt = state["applied_operations"].get(item["claim_operation_id"])
        result = receipt.get("result", {}) if isinstance(receipt, dict) else {}
        if result.get("kind") != "claim" or result.get("decision_id") != identity or result.get("owner") != item["claim_owner"] or result.get("token") != item["claim_token"]:
            _conflict("claim_receipt_mismatch", f"Claim receipt does not bind Decision: {identity}")
        _predecessor(root, map_identity, identity, item["predecessor_attempt_id"], item["attempt_id"])
        task = {
            "schema_version": SCHEMA_VERSION,
            "map_id": map_identity,
            "decision_id": identity,
            "attempt_id": item["attempt_id"],
            "work_type": operation["work_type"],
            "question": decision["question"],
            "confirmed_context": item["confirmed_context"],
            "constraints": item["constraints"],
            "expected_output": item["expected_output"],
            "predecessor_attempt_id": item["predecessor_attempt_id"],
            "prepare_operation_id": spec["operation_id"],
            "request_sha256": request_sha,
            "map_revision": state["revision"],
            "map_sha256": _map_sha(view),
            "claim_operation_id": item["claim_operation_id"],
            "claim_owner": item["claim_owner"],
            "claim_token_sha256": _sha(item["claim_token"].encode()),
            "claim_observed_expires_at": claim["expires_at"],
            "requested_execution_mode": item["requested_execution_mode"],
            "batch_id": spec["operation_id"],
            "batch_members": members,
            "created_at": timestamp,
        }
        documents.append(_validate_task(task, expected=(map_identity, identity, item["attempt_id"])))
    return documents, {"map_revision": state["revision"], "map_sha256": _map_sha(view)}


def _work_base(root: Path, targets: list[tuple[str, str, str]]) -> str:
    snapshot: list[dict[str, Any]] = []
    for mid, did, aid in sorted(targets):
        directory = _attempt_directory(root, mid, did, aid)
        item: dict[str, Any] = {"map_id": mid, "decision_id": did, "attempt_id": aid, "exists": directory.exists() or directory.is_symlink()}
        if item["exists"]:
            task, task_data, result, result_data = _read_attempt(root, mid, did, aid)
            item.update({"task_sha256": _sha(task_data), "result_sha256": None if result_data is None else _sha(result_data)})
        snapshot.append(item)
    return _sha(_canonical_json(snapshot))


def plan(project_root: str | Path, map_id: str, spec: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    map_identity = _map_id(map_id)
    normalized = _validate_operation_spec(copy.deepcopy(spec), map_identity)
    _, now_text = _now(now)
    request_sha = _request_digest(map_identity, normalized)
    operation = normalized["operation"]
    kind = operation["kind"]
    if kind == "prepare_attempts":
        targets = [(map_identity, item["decision_id"], item["attempt_id"]) for item in operation["attempts"]]
        existing_times: set[str] = set()
        for mid, did, aid in targets:
            directory = _attempt_directory(root, mid, did, aid)
            if directory.exists() or directory.is_symlink():
                task, _, _, _ = _read_attempt(root, mid, did, aid)
                if task["request_sha256"] != request_sha or task["prepare_operation_id"] != normalized["operation_id"]:
                    _conflict("attempt_exists", f"Attempt already exists with another request: {did}/{aid}")
                existing_times.add(task["created_at"])
        if len(existing_times) > 1:
            _fail("inconsistent_batch", "idempotent batch has inconsistent created_at")
        all_existing = all(_attempt_directory(root, *target).exists() for target in targets)
        if all_existing:
            view = _map_view(root, map_identity, now_text)
            documents = []
            provenance: set[tuple[int, str]] = set()
            for target in targets:
                task, _, _, _ = _read_attempt(root, *target)
                _validate_task_binding(task, view)
                documents.append(task)
                provenance.add((task["map_revision"], task["map_sha256"]))
            if len(provenance) != 1:
                _fail("inconsistent_batch", "idempotent batch has inconsistent Map provenance")
            revision, digest = next(iter(provenance))
            map_base = {"map_revision": revision, "map_sha256": digest}
        else:
            created_at = next(iter(existing_times), now_text)
            documents, map_base = _prepare_documents(root, map_identity, normalized, request_sha, now_text, created_at=created_at)
        effect = {"kind": kind, "tasks": documents, "idempotent": all_existing}
    elif kind == "record_result":
        targets = [(map_identity, operation["decision_id"], operation["attempt_id"])]
        task, task_data, existing, _ = _read_attempt(root, *targets[0])
        _validate_task_binding(task, _map_view(root, map_identity, now_text))
        if _sha(task_data) != operation["task_sha256"]:
            _conflict("task_digest_mismatch", "record_result task digest is stale")
        details = _normalize_result(copy.deepcopy(operation["result"]), task["work_type"])
        status = details.pop("status")
        actual = details.pop("actual_execution_mode")
        fresh = details.pop("fresh_context")
        document = _validate_result({"schema_version": SCHEMA_VERSION, "map_id": map_identity, "decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "task_sha256": operation["task_sha256"], "record_operation_id": normalized["operation_id"], "request_sha256": request_sha, "status": status, "actual_execution_mode": actual, "fresh_context": fresh, "submitted_at": now_text if existing is None else existing["submitted_at"], "details": details}, task)
        if existing is not None and (existing["request_sha256"] != request_sha or existing != document):
            _conflict("result_exists", "result.json already exists with another request")
        effect = {"kind": kind, "result": document, "idempotent": existing is not None}
        map_base = None
    else:
        targets = [(map_identity, operation["decision_id"], operation["attempt_id"])]
        task, _, result, result_data = _read_attempt(root, *targets[0])
        if result is None or result_data is None or result["status"] != "candidate":
            _conflict("result_not_candidate", "only candidate result can be absorbed")
        view = _map_view(root, map_identity, now_text)
        _validate_task_binding(task, view)
        if operation["owner"] != task["claim_owner"] or _sha(operation["token"].encode()) != task["claim_token_sha256"]:
            _conflict("claim_mismatch", "absorb credentials do not bind task Claim")
        r2_spec = {"schema_version": 1, "operation_id": operation["resolve_operation_id"], "operation": {"kind": "resolve", "decision_id": task["decision_id"], "owner": operation["owner"], "token": operation["token"], "outcome": result["details"]["outcome"], "rationale": result["details"]["rationale"], "evidence": [*result["details"]["evidence"], _result_pointer(task, result_data)]}}
        nested = _r2_call("plan", root, map_identity, r2_spec, now_text)
        derived = _derive(task, result, result_data, view, _parse_utc(now_text, "now"))
        if not nested["effect"].get("idempotent", False) and not derived["absorbable"]:
            _conflict("result_not_absorbable", f"result is not absorbable: {derived['absorbability_code']}")
        map_base = {"map_revision": nested["base_revision"], "map_sha256": nested["base_sha256"]}
        effect = {"kind": kind, "nested_decision_map_plan": nested, "evidence_pointer": _result_pointer(task, result_data), "idempotent": nested["effect"].get("idempotent", False)}
    return {"schema_version": PLAN_SCHEMA_VERSION, "status": "ok", "action": "apply", "map_id": map_identity, "base_work_sha256": _work_base(root, targets), "base_map": map_base, "request_sha256": request_sha, "planned_at": now_text, "operation": normalized, "effect": effect}


def _validate_plan(value: Any) -> dict[str, Any]:
    planned = _exact(value, {"schema_version", "status", "action", "map_id", "base_work_sha256", "base_map", "request_sha256", "planned_at", "operation", "effect"}, set(), "plan")
    if type(planned["schema_version"]) is not int or planned["schema_version"] != PLAN_SCHEMA_VERSION or planned["status"] != "ok" or planned["action"] != "apply":
        _fail("invalid_plan", "unsupported plan schema or action")
    planned["map_id"] = _map_id(planned["map_id"])
    for field in ("base_work_sha256", "request_sha256"):
        if not isinstance(planned[field], str) or SHA_RE.fullmatch(planned[field]) is None:
            _fail("invalid_plan", f"{field} must be SHA-256")
    _parse_utc(planned["planned_at"], "plan.planned_at")
    planned["operation"] = _validate_operation_spec(planned["operation"], planned["map_id"])
    if planned["request_sha256"] != _request_digest(planned["map_id"], planned["operation"]):
        _fail("plan_digest_mismatch", "plan request digest does not match operation")
    if not isinstance(planned["effect"], dict):
        _fail("invalid_plan", "plan.effect must be an object")
    if planned["base_map"] is not None:
        base = _exact(planned["base_map"], {"map_revision", "map_sha256"}, set(), "plan.base_map")
        if type(base["map_revision"]) is not int or base["map_revision"] < 1 or not isinstance(base["map_sha256"], str) or SHA_RE.fullmatch(base["map_sha256"]) is None:
            _fail("invalid_plan", "invalid map base")
    return planned


@contextmanager
def _work_lock(root: Path, map_identity: str) -> Iterator[None]:
    lock_root = root / LOCKS_RELATIVE
    if lock_root.exists():
        _assert_real_directory(lock_root, "Decision Work lock root")
    else:
        try:
            lock_root.mkdir(mode=0o700)
        except FileExistsError:
            pass
        _assert_real_directory(lock_root, "Decision Work lock root")
    path = lock_root / f"{map_identity}.lock"
    flags = os.O_CREAT | os.O_RDWR | (getattr(os, "O_NOFOLLOW", 0))
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as error:
        _fail("lock_error", f"cannot open Decision Work lock: {error}")
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            _fail("unsafe_lock", "Decision Work lock is not a regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _conflict("work_locked", f"Decision Work is being modified: {map_identity}")
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


def _ensure_directory(path: Path, label: str) -> None:
    if path.exists():
        _assert_real_directory(path, label)
        return
    try:
        path.mkdir(mode=0o755)
    except FileExistsError:
        pass
    _assert_real_directory(path, label)


def _prune_empty_work_parents(root: Path, start: Path) -> None:
    boundary = root / WORK_RELATIVE
    current = start
    while current == boundary or boundary in current.parents:
        try:
            current.rmdir()
        except OSError:
            return
        if current == boundary:
            return
        current = current.parent


def _publish_task(root: Path, task: dict[str, Any]) -> bool:
    base = root / WORK_RELATIVE
    _ensure_directory(base, "Decision Work root")
    map_path = base / task["map_id"]
    _ensure_directory(map_path, "Decision Work Map directory")
    decision_path = map_path / task["decision_id"]
    _ensure_directory(decision_path, "Decision Work Decision directory")
    target = decision_path / task["attempt_id"]
    data = _canonical_json(task)
    if target.exists() or target.is_symlink():
        existing, existing_data, _, _ = _read_attempt(root, task["map_id"], task["decision_id"], task["attempt_id"])
        if existing_data == data:
            return False
        _conflict("attempt_exists", f"Attempt exists with different bytes: {task['attempt_id']}")
    staging = Path(tempfile.mkdtemp(prefix=f".tmp-{task['attempt_id']}-", dir=decision_path))
    published = False
    try:
        path = staging / "task.json"
        with path.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(staging)
        try:
            os.rename(staging, target)
        except OSError as error:
            if error.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                _conflict("attempt_exists", f"Attempt already exists: {task['attempt_id']}")
            raise
        published = True
        _fsync_directory(decision_path)
        return True
    finally:
        if not published and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        if not published:
            _prune_empty_work_parents(root, decision_path)


def _publish_result(root: Path, task: dict[str, Any], result: dict[str, Any]) -> bool:
    directory = _attempt_directory(root, task["map_id"], task["decision_id"], task["attempt_id"])
    _assert_real_directory(directory, "Decision Work attempt directory")
    target = directory / "result.json"
    data = _canonical_json(result)
    if target.exists() or target.is_symlink():
        existing, existing_data = _read_canonical(target, "result.json")
        if existing_data == data:
            return False
        _conflict("result_exists", "result.json is immutable")
    descriptor, name = tempfile.mkstemp(prefix=".result.", suffix=".tmp", dir=directory)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            _conflict("result_exists", "result.json is immutable")
        _fsync_directory(directory)
        return True
    finally:
        if temporary.exists():
            temporary.unlink()


def apply(project_root: str | Path, planned: dict[str, Any], now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    normalized = _validate_plan(copy.deepcopy(planned))
    map_identity = normalized["map_id"]
    _, now_text = _now(now)
    operation = normalized["operation"]["operation"]
    kind = operation["kind"]
    if kind == "prepare_attempts":
        targets = [(map_identity, item["decision_id"], item["attempt_id"]) for item in operation["attempts"]]
    else:
        targets = [(map_identity, operation["decision_id"], operation["attempt_id"])]
    with _work_lock(root, map_identity):
        if _work_base(root, targets) != normalized["base_work_sha256"]:
            # Existing identical immutable output is a valid lost-response retry.
            if kind == "prepare_attempts" and all(_attempt_directory(root, *target).exists() for target in targets):
                tasks = [_read_attempt(root, *target)[0] for target in targets]
                if all(task["request_sha256"] == normalized["request_sha256"] for task in tasks):
                    return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "attempts": [{"decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "task_sha256": _sha(_canonical_json(task))} for task in tasks], "idempotent": True}
            if kind == "record_result":
                task, _, result, result_data = _read_attempt(root, *targets[0])
                if result is not None and result["request_sha256"] == normalized["request_sha256"]:
                    return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "result_sha256": _sha(result_data or b""), "idempotent": True}
            _conflict("stale_plan", "Decision Work changed after plan; create a new plan")
        if kind == "prepare_attempts":
            effect_tasks = normalized["effect"].get("tasks")
            if not isinstance(effect_tasks, list):
                _fail("invalid_plan", "prepare plan is missing tasks")
            if normalized["effect"].get("idempotent") is True and all(_attempt_directory(root, *target).exists() for target in targets):
                tasks = [_read_attempt(root, *target)[0] for target in targets]
                view = _map_view(root, map_identity, now_text)
                for task in tasks:
                    _validate_task_binding(task, view)
                if tasks != effect_tasks or any(task["request_sha256"] != normalized["request_sha256"] for task in tasks):
                    _fail("plan_digest_mismatch", "idempotent prepare effect does not bind existing tasks")
                return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "attempts": [{"decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "task_sha256": _sha(_canonical_json(task))} for task in tasks], "idempotent": True}
            # Revalidate live R2 state and compare the exact planned documents.
            documents, map_base = _prepare_documents(root, map_identity, normalized["operation"], normalized["request_sha256"], now_text, created_at=normalized["planned_at"])
            if documents != effect_tasks or map_base != normalized["base_map"]:
                _conflict("stale_plan", "Decision Map changed after work plan")
            created: list[Path] = []
            try:
                for task in documents:
                    if _publish_task(root, task):
                        created.append(_attempt_directory(root, task["map_id"], task["decision_id"], task["attempt_id"]))
            except Exception:
                for path in reversed(created):
                    shutil.rmtree(path, ignore_errors=True)
                    _prune_empty_work_parents(root, path.parent)
                raise
            return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "attempts": [{"decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "task_sha256": _sha(_canonical_json(task))} for task in documents], "idempotent": not created}
        if kind == "record_result":
            task, task_data, existing, _ = _read_attempt(root, *targets[0])
            if existing is not None:
                _conflict("result_exists", "result.json is immutable")
            document = normalized["effect"].get("result")
            if not isinstance(document, dict):
                _fail("invalid_plan", "record plan is missing result")
            document = _validate_result(document, task)
            if document["task_sha256"] != _sha(task_data):
                _conflict("task_digest_mismatch", "task changed after result plan")
            _publish_result(root, task, document)
            return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "result_sha256": _sha(_canonical_json(document)), "idempotent": False}
        task, _, result, result_data = _read_attempt(root, *targets[0])
        if result is None or result_data is None or result["status"] != "candidate":
            _conflict("result_not_candidate", "only candidate result can be absorbed")
        nested = normalized["effect"].get("nested_decision_map_plan")
        if not isinstance(nested, dict):
            _fail("invalid_plan", "absorb plan is missing Decision Map plan")
        if normalized["effect"].get("evidence_pointer") != _result_pointer(task, result_data):
            _fail("plan_digest_mismatch", "absorb evidence pointer changed")
        result_value = _r2_call("apply", root, nested, now_text)
        return {"schema_version": 1, "status": "ok", "action": "apply", "kind": kind, "map_id": map_identity, "decision_id": task["decision_id"], "attempt_id": task["attempt_id"], "decision_map_result": result_value, "evidence_pointer": _result_pointer(task, result_data), "idempotent": bool(result_value.get("idempotent"))}


def verify(project_root: str | Path, map_id: str | None = None, now: str | dt.datetime | None = None) -> dict[str, Any]:
    root, _ = _resolve_root(project_root)
    current, now_text = _now(now)
    errors: list[dict[str, str]] = []
    checked: list[dict[str, Any]] = []
    identities: list[tuple[str, str, str]] = []
    try:
        identities = _discover_attempts(root, map_id)
    except DecisionWorkError as error:
        errors.append({"code": error.code, "message": error.message})
    views: dict[str, dict[str, Any]] = {}
    try:
        map_ids = [_map_id(map_id)] if map_id is not None else [item["map_id"] for item in _r2_call("inspect", root, None, now_text)["maps"]]
        for identity in map_ids:
            views[identity] = _map_view(root, identity, now_text)
    except DecisionWorkError as error:
        errors.append({"code": error.code, "message": error.message})
    for mid, did, aid in identities:
        try:
            task, task_data, result, result_data = _read_attempt(root, mid, did, aid)
            if mid not in views:
                views[mid] = _map_view(root, mid, now_text)
            state = views[mid]["state"]
            _validate_task_binding(task, views[mid])
            for member in task["batch_members"]:
                path = _attempt_directory(root, mid, member["decision_id"], member["attempt_id"])
                if not path.exists() or path.is_symlink():
                    _fail("incomplete_batch", f"missing batch member: {member['decision_id']}/{member['attempt_id']}")
                other, _, _, _ = _read_attempt(root, mid, member["decision_id"], member["attempt_id"])
                if other["batch_id"] != task["batch_id"] or other["batch_members"] != task["batch_members"]:
                    _fail("inconsistent_batch", f"batch membership drift: {other['attempt_id']}")
            if task["predecessor_attempt_id"] is not None:
                predecessor, _, predecessor_result, _ = _read_attempt(root, mid, did, task["predecessor_attempt_id"])
                if predecessor_result is None or predecessor_result["status"] != "needs_input":
                    _fail("invalid_predecessor", f"invalid predecessor for {aid}")
            derived = _derive(task, result, result_data, views[mid], current)
            checked.append({"map_id": mid, "decision_id": did, "attempt_id": aid, "task_sha256": _sha(task_data), "result_sha256": None if result_data is None else _sha(result_data), "derived": derived})
        except DecisionWorkError as error:
            errors.append({"code": error.code, "message": error.message})
    for mid, view in views.items():
        for did, decision in view["state"].get("decisions", {}).items():
            resolution = decision.get("resolution") or {}
            for pointer in resolution.get("evidence", []):
                if not isinstance(pointer, str) or not pointer.startswith("decision-work:"):
                    continue
                match = POINTER_RE.fullmatch(pointer)
                if match is None:
                    errors.append({"code": "invalid_evidence_pointer", "message": f"invalid Decision Work evidence pointer: {mid}/{did}"})
                    continue
                pointer_map, pointer_decision, pointer_attempt, pointer_digest = match.groups()
                if pointer_map != mid or pointer_decision != did:
                    errors.append({"code": "cross_binding_pointer", "message": f"Decision Work evidence pointer crosses its resolution: {mid}/{did}"})
                    continue
                result_path = _attempt_directory(root, pointer_map, pointer_decision, pointer_attempt) / "result.json"
                if not result_path.exists():
                    errors.append({"code": "missing_result", "message": f"absorbed Decision Work result is missing: {pointer_map}/{pointer_decision}/{pointer_attempt}"})
                    continue
                try:
                    _, _, result, result_data = _read_attempt(root, pointer_map, pointer_decision, pointer_attempt)
                    if result is None or result_data is None:
                        _fail("missing_result", f"absorbed Decision Work result is missing: {pointer_map}/{pointer_decision}/{pointer_attempt}")
                    if result["status"] != "candidate":
                        _fail("absorbed_result_not_candidate", f"absorbed Decision Work result is not candidate: {pointer_map}/{pointer_decision}/{pointer_attempt}")
                    if _sha(result_data) != pointer_digest:
                        _fail("result_digest_mismatch", f"absorbed Decision Work result digest changed: {pointer_map}/{pointer_decision}/{pointer_attempt}")
                except DecisionWorkError as error:
                    errors.append({"code": error.code, "message": error.message})
    return {"schema_version": SCHEMA_VERSION, "status": "ok" if not errors else "error", "action": "verify", "observed_at": now_text, "checked": checked, "errors": errors}
