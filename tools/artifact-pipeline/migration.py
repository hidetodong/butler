#!/usr/bin/env python3
"""Transactional legacy live-artifact migration to the canonical v1 templates."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("artifact_contract", HERE / "contract.py")
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class MigrationError(ValueError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sections(text: str, allowed: list[str]) -> tuple[list[str], dict[str, str], str | None]:
    all_headings = list(re.finditer(r"^(#{1,2}) (.+?)\s*$", text, re.MULTILINE))
    title: str | None = None
    matches = []
    unknown: list[str] = []
    for match in all_headings:
        name = match.group(2)
        if name in allowed:
            matches.append(match)
        elif match.group(1) == "#" and title is None:
            title = match.group(0)
        else:
            unknown.append(name)
    if unknown:
        raise MigrationError(f"unknown headings: {unknown}")
    names = [match.group(2) for match in matches]
    if len(names) != len(set(names)):
        raise MigrationError("duplicate section")
    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        bodies[match.group(2)] = text[match.end():end].strip("\n")
    return names, bodies, title


def migrate_text(name: str, text: str, manifest: dict[str, object], iteration: str) -> str:
    if contract.MARKER_RE.search(text):
        errors = contract.validate_text(name, text, manifest)
        if errors:
            raise MigrationError(f"strict artifact is invalid: {name}: {errors}")
        return text
    spec = manifest["artifacts"][name]
    names, bodies, old_title = sections(text, spec["sections"])
    rendered = contract.render(HERE, name, iteration, "migrated")
    if old_title:
        rendered = re.sub(r"^# (?!#).+$", old_title, rendered, count=1, flags=re.MULTILINE)
    if text.startswith("---\n") and rendered.startswith("---\n"):
        old_end, new_end = text.find("\n---\n", 4), rendered.find("\n---\n", 4)
        if old_end < 0:
            raise MigrationError("unterminated frontmatter")
        rendered = text[:old_end + 5] + rendered[new_end + 5:]
    old_status = re.search(r"^方案状态:\s*.+$", text, re.MULTILINE)
    if old_status:
        rendered = re.sub(r"^方案状态:\s*.+$", old_status.group(0), rendered, count=1, flags=re.MULTILINE)
    for heading, body in bodies.items():
        pattern = rf"(^## {re.escape(heading)}\s*$\n)(.*?)(?=^## |\Z)"
        replacement = rf"\1\n{body}\n\n"
        rendered = re.sub(pattern, replacement, rendered, count=1, flags=re.MULTILINE | re.DOTALL)
    errors = contract.validate_text(name, rendered, manifest)
    if errors:
        raise MigrationError(f"migrated artifact invalid: {name}: {errors}")
    return rendered.rstrip() + "\n"


def plan(root: Path) -> tuple[dict[str, object], dict[str, bytes], dict[str, bytes]]:
    manifest = contract.load_manifest(HERE)
    iteration_text = (root / ".ai/ITERATIONS.md").read_text(encoding="utf-8")
    match = re.search(r"^current:\s*(ITER-[0-9]+)\s*$", iteration_text, re.MULTILINE)
    if not match:
        raise MigrationError("active iteration required")
    before: dict[str, bytes] = {}
    after: dict[str, bytes] = {}
    items: list[dict[str, object]] = []
    for name, spec in manifest["artifacts"].items():
        relative = spec["path"]
        path = root / relative
        if path.is_symlink() or not path.is_file():
            raise MigrationError(f"missing or unsafe live artifact: {relative}")
        data = path.read_bytes()
        migrated = migrate_text(name, data.decode("utf-8"), manifest, match.group(1)).encode("utf-8")
        before[relative] = data
        after[relative] = migrated
        items.append({"artifact": name, "path": relative, "pre_sha256": sha(data), "post_sha256": sha(migrated), "changed": data != migrated})
    migration_id = "ART-" + sha("".join(item["pre_sha256"] for item in items).encode())[:12]
    return {"schema_version": 1, "migration_id": migration_id, "iteration": match.group(1), "apply_ready": True, "items": items}, before, after


def atomic_group(root: Path, payloads: dict[str, bytes]) -> None:
    originals = {relative: (root / relative).read_bytes() for relative in payloads}
    temps: list[tuple[Path, Path]] = []
    try:
        for relative, data in payloads.items():
            target = root / relative
            fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            temps.append((Path(temporary), target))
        for temporary, target in temps:
            os.replace(temporary, target)
    except BaseException:
        for relative, data in originals.items():
            (root / relative).write_bytes(data)
        raise
    finally:
        for temporary, _ in temps:
            if temporary.exists():
                temporary.unlink()


def apply(root: Path) -> dict[str, object]:
    receipt, before, after = plan(root)
    if not any(item["changed"] for item in receipt["items"]):
        receipt["changed"] = False
        return receipt
    backup = root / ".ai/.artifact-migration-backups" / receipt["migration_id"]
    if backup.exists():
        for relative, data in before.items():
            saved = backup / Path(relative).name
            if not saved.is_file() or saved.read_bytes() != data:
                raise MigrationError(f"existing backup does not match pre state: {saved}")
    else:
        backup.mkdir(parents=True)
        for relative, data in before.items():
            (backup / Path(relative).name).write_bytes(data)
    receipt["changed"] = True
    receipt["backup"] = str(backup.relative_to(root))
    atomic_group(root, after)
    (backup / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return receipt


def verify(root: Path, migration_id: str) -> dict[str, object]:
    receipt_path = root / ".ai/.artifact-migration-backups" / migration_id / "receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    drift = [item["path"] for item in receipt["items"] if sha((root / item["path"]).read_bytes()) != item["post_sha256"]]
    return {"status": "drift" if drift else "ok", "migration_id": migration_id, "drift": drift}


def rollback(root: Path, migration_id: str) -> dict[str, object]:
    checked = verify(root, migration_id)
    if checked["drift"]:
        raise MigrationError(f"post state drift: {checked['drift']}")
    backup = root / ".ai/.artifact-migration-backups" / migration_id
    receipt = json.loads((backup / "receipt.json").read_text(encoding="utf-8"))
    payloads = {item["path"]: (backup / Path(item["path"]).name).read_bytes() for item in receipt["items"]}
    atomic_group(root, payloads)
    return {"status": "rolled_back", "migration_id": migration_id}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("plan", "apply", "verify", "rollback"))
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--migration-id")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    try:
        if args.command == "plan": result = plan(root)[0]
        elif args.command == "apply": result = apply(root)
        elif args.command == "verify": result = verify(root, args.migration_id or "")
        else: result = rollback(root, args.migration_id or "")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 1 if result.get("status") == "drift" else 0
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
