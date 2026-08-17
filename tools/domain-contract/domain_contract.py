#!/usr/bin/env python3
"""Machine contract for Butler's high-risk domain identities, states and references.

`domains.v1.json` registers only navigation metadata — concept identity, bounded
context, controlled contract type, unique owner and in-repo truth-source pointer —
plus relations and file-level assertions. Every entry must be anchored by at
least one assertion or relation, so a registered concept always has something
that can catch it breaking. It must never copy execution enums,
bridge field sets or artifact algorithms (those stay with their owners); unknown
payload fields are rejected fail-closed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ENTRY_FIELDS = {"id", "concept", "context", "type", "owner", "source"}
RELATION_KINDS = {"并列", "共享策略"}


class ContractError(ValueError):
    pass


def load_registry(tool_root: Path) -> dict[str, object]:
    path = tool_root / "domains.v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ContractError("unsupported domain-contract registry")
    for key in ("contexts", "contract_types", "entries", "relations", "assertions"):
        if not isinstance(data.get(key), list):
            raise ContractError(f"missing or non-list registry key: {key}")
    return data


def _resolve_source(root: Path, raw: str) -> Path | None:
    candidate = root / raw
    if candidate.is_symlink() or not candidate.is_file():
        return None
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return None
    if not resolved.is_relative_to(root):
        return None
    return resolved


def _validate_entries(root: Path, registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    contexts = set(registry["contexts"])
    types = set(registry["contract_types"])
    seen_ids: set[str] = set()
    entries = registry["entries"]
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            errors.append(f"entry {index} is not an object")
            continue
        unknown = set(entry) - ENTRY_FIELDS
        if unknown:
            errors.append(f"entry {index} has copy-type payload fields: {sorted(unknown)}")
        ident = entry.get("id")
        if not isinstance(ident, str) or not ident:
            errors.append(f"entry {index} missing or empty id")
            continue
        if ident in seen_ids:
            errors.append(f"duplicate id: {ident}")
        seen_ids.add(ident)
        if not isinstance(entry.get("concept"), str) or not entry["concept"]:
            errors.append(f"{ident}: missing or empty concept")
        if entry.get("context") not in contexts:
            errors.append(f"{ident}: unknown context: {entry.get('context')!r}")
        if entry.get("type") not in types:
            errors.append(f"{ident}: unknown contract type: {entry.get('type')!r}")
        owner = entry.get("owner")
        if not isinstance(owner, str) or not owner:
            errors.append(f"{ident}: missing or non-single owner (co-ownership forbidden)")
        source = entry.get("source")
        if not isinstance(source, str) or not source:
            errors.append(f"{ident}: missing source")
        elif _resolve_source(root, source) is None:
            errors.append(f"{ident}: source missing, symlink or out-of-bounds: {source}")
    return errors


def _validate_relations(registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    known = {entry["id"] for entry in registry["entries"] if isinstance(entry, dict)}
    for index, relation in enumerate(registry["relations"], start=1):
        if not isinstance(relation, dict):
            errors.append(f"relation {index} is not an object")
            continue
        if relation.get("kind") not in RELATION_KINDS:
            errors.append(f"relation {index}: unknown kind: {relation.get('kind')!r}")
        for side in ("left", "right"):
            value = relation.get(side)
            if not isinstance(value, str) or not value:
                errors.append(f"relation {index}: missing {side}")
            elif value not in known:
                errors.append(f"relation {index}: dangling {side} reference: {value!r}")
    return errors


def _validate_assertions(root: Path, registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for index, assertion in enumerate(registry["assertions"], start=1):
        if not isinstance(assertion, dict):
            errors.append(f"assertion {index} is not an object")
            continue
        file = assertion.get("file")
        if not isinstance(file, str) or not file:
            errors.append(f"assertion {index}: missing file")
            continue
        path = _resolve_source(root, file)
        if path is None:
            errors.append(f"assertion {index}: file missing or out-of-bounds: {file}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in assertion.get("must_contain", []):
            if token not in text:
                errors.append(
                    f"assertion {index} ({file}): must contain {token!r} — {assertion.get('reason', '')}"
                )
        for token in assertion.get("must_not_contain", []):
            if token in text:
                errors.append(
                    f"assertion {index} ({file}): must not contain {token!r} — {assertion.get('reason', '')}"
                )
    return errors


def _validate_coverage(registry: dict[str, object]) -> list[str]:
    """Every registered entry must be reachable by at least one regression anchor.

    An entry counts as covered when a file-level assertion targets its owner or
    source, or when its id appears on either side of a relation. Registering a
    concept without any anchor means nothing can catch it breaking, so it fails
    closed and names the entry.
    """
    errors: list[str] = []
    assertion_files = {
        assertion["file"]
        for assertion in registry["assertions"]
        if isinstance(assertion, dict) and isinstance(assertion.get("file"), str)
    }
    related_ids: set[str] = set()
    for relation in registry["relations"]:
        if not isinstance(relation, dict):
            continue
        for side in ("left", "right"):
            value = relation.get(side)
            if isinstance(value, str) and value:
                related_ids.add(value)
    for entry in registry["entries"]:
        if not isinstance(entry, dict):
            continue
        ident = entry.get("id")
        if not isinstance(ident, str) or not ident:
            continue
        anchors = {entry.get("owner"), entry.get("source")} & assertion_files
        if anchors or ident in related_ids:
            continue
        errors.append(f"{ident}: not covered by any assertion or relation")
    return errors


def check(root: Path) -> tuple[bool, list[str]]:
    root = root.resolve()
    tool_root = Path(__file__).resolve().parent
    registry = load_registry(tool_root)
    errors: list[str] = []
    errors.extend(_validate_entries(root, registry))
    errors.extend(_validate_relations(registry))
    errors.extend(_validate_assertions(root, registry))
    errors.extend(_validate_coverage(registry))
    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args(argv)
    try:
        ok, errors = check(Path(args.project_root))
    except (OSError, UnicodeError, ValueError, ContractError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2
    payload = {"status": "ok" if ok else "failed", "errors": errors}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
