#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PRD_ID = re.compile(r"(\d{4})-(\d{2})-(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
MODULE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION = re.compile(r"v[0-9]+(?:\.[0-9]+)*$")
VERSION_IN_INDEX = re.compile(r"(?:当前版本|Current Version|PRD 版本|Version)\s*(?:\*\*)?\s*[：:]\s*(?:\*\*)?\s*(v[0-9]+(?:\.[0-9]+)*)", re.I)
VERSION_TABLE = re.compile(r"\|\s*(?:当前版本|Current Version|PRD 版本|Version)\s*\|\s*(v[0-9]+(?:\.[0-9]+)*)\s*\|", re.I)
VERSION_HEADING = re.compile(r"(?mi)^#\s+.*?\b(v[0-9]+(?:\.[0-9]+)*)\b")
DOC_VERSION = re.compile(r"doc\s+version\s*(?:\*\*)?\s*[：:]?\s*(?:\*\*)?\s*([0-9]+)\b", re.I)
CURRENT_DOC_VERSION = re.compile(r"(?mi)^-\s*(?:\*\*)?(?:源|source)(?:\*\*)?\s*[：:].*?doc\s+version\s*(?:\*\*)?\s*[：:]?\s*(?:\*\*)?\s*([0-9]+)\b")
RECEIPT = ".butler-migration.json"
MIGRATION_ID = re.compile(r"MIG-[0-9a-f]{12}$")


class MigrationError(ValueError):
    pass


def resolve_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir() or not (root / ".ai").is_dir():
        raise MigrationError("project root must be an existing Butler project with .ai/")
    if (root / ".ai").is_symlink():
        raise MigrationError("project .ai directory must not be a symlink")
    references = root / ".ai/references"
    if references.is_symlink():
        raise MigrationError(".ai/references must not be a symlink")
    return root


def validate_prd_id(value: str) -> str:
    match = PRD_ID.fullmatch(value)
    if not match:
        raise MigrationError("prd_id must match YYYY-MM-DD-requirement-slug")
    try:
        datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError as error:
        raise MigrationError("prd_id contains an invalid calendar date") from error
    return value


def safe_tree_entries(root: Path, *, exclude: set[str] | None = None) -> list[dict[str, str]]:
    excluded = exclude or set()
    entries: list[dict[str, str]] = []
    if root.is_symlink():
        raise MigrationError(f"symlink root rejected: {root.name}")
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if relative in excluded:
            continue
        if path.is_symlink():
            raise MigrationError(f"symlink rejected: {relative}")
        if path.is_dir():
            entries.append({"path": relative, "kind": "dir", "sha256": "—"})
        elif path.is_file():
            entries.append({"path": relative, "kind": "file", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        else:
            raise MigrationError(f"non-regular entry rejected: {relative}")
    return entries


def tree_hash(entries: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
    return "sha256:" + digest.hexdigest()


def layout(root: Path) -> dict[str, object]:
    prd = root / ".ai/references/prd"
    if prd.is_symlink():
        raise MigrationError("references/prd symlink rejected")
    if not prd.exists():
        return {"state": "absent", "prd_root": ".ai/references/prd"}
    if not prd.is_dir():
        raise MigrationError("references/prd must be a real directory")
    entries = safe_tree_entries(prd)
    dated = sorted(path.name for path in prd.iterdir() if path.is_dir() and PRD_ID.fullmatch(path.name))
    root_modules = sorted(path.name for path in prd.glob("*.md") if path.name != "00_INDEX.md")
    legacy_archive = (prd / ".archive").is_dir()
    receipt = (prd / RECEIPT).is_file()
    if dated and (root_modules or legacy_archive):
        state = "mixed"
    elif dated:
        state = "collection"
    elif (prd / "00_INDEX.md").is_file() and root_modules:
        state = "legacy"
    elif not entries:
        state = "empty"
    else:
        state = "unknown"
    return {
        "state": state, "prd_root": ".ai/references/prd", "prd_ids": dated,
        "root_modules": root_modules, "has_legacy_archive": legacy_archive,
        "has_receipt": receipt, "tree_sha256": tree_hash(entries), "entries": entries,
    }


def index_version(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise MigrationError(f"cannot read PRD index: {path}") from error
    current_doc_versions = sorted(set(CURRENT_DOC_VERSION.findall(text)))
    if len(current_doc_versions) == 1:
        return f"v{current_doc_versions[0]}"
    if len(current_doc_versions) > 1:
        raise MigrationError(f"PRD index exposes conflicting current doc versions: {current_doc_versions}")
    doc_versions = sorted(set(DOC_VERSION.findall(text)))
    if len(doc_versions) == 1:
        return f"v{doc_versions[0]}"
    if len(doc_versions) > 1:
        raise MigrationError(f"PRD index exposes conflicting doc versions: {doc_versions}")
    matches = sorted({value.lower() for value in (
        set(VERSION_IN_INDEX.findall(text))
        | set(VERSION_TABLE.findall(text))
        | set(VERSION_HEADING.findall(text))
    )})
    if len(matches) != 1:
        raise MigrationError(f"PRD index must expose exactly one current version, found={matches}")
    return matches[0]


def reference_impact(root: Path) -> list[dict[str, object]]:
    candidates = [root / ".ai/MILESTONE.md", root / ".ai/AC_LIST.md", root / ".ai/TECH_PLAN.md", root / ".ai/VERIFY_REPORT.md"]
    archive = root / ".ai/iterations"
    if archive.is_symlink():
        raise MigrationError(".ai/iterations symlink rejected during impact scan")
    if archive.is_dir():
        candidates.extend(sorted(archive.glob("ITER-*/AC_LIST.md")))
        candidates.extend(sorted(archive.glob("ITER-*/TECH_PLAN.md")))
        candidates.extend(sorted(archive.glob("ITER-*/VERIFY_REPORT.md")))
    results: list[dict[str, object]] = []
    pattern = re.compile(r"(?:\.ai/)?references/prd/(?![0-9]{4}-[0-9]{2}-[0-9]{2}-)([a-z0-9][a-z0-9-]*\.md)")
    route_pattern = re.compile(r"(?:→\s*)?prd\s*:\s*([a-z0-9][a-z0-9-]*(?:\s*,\s*[a-z0-9][a-z0-9-]*)*)", re.I)
    for path in candidates:
        if not path.is_file() or path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8")
        refs = sorted(set(pattern.findall(text)))
        route_slugs = sorted({slug.strip() for group in route_pattern.findall(text) for slug in group.split(",")})
        if not refs and not route_slugs:
            continue
        relative = path.relative_to(root).as_posix()
        if relative == ".ai/MILESTONE.md":
            group = "milestone"
        elif relative.startswith(".ai/iterations/"):
            group = "closed-history"
        else:
            group = "active-or-future"
        results.append({"path": relative, "group": group, "legacy_refs": refs, "route_slugs": route_slugs})
    return results


def build_plan(root: Path, prd_id: str, title: str) -> dict[str, object]:
    validate_prd_id(prd_id)
    if not title.strip() or "\n" in title or "|" in title:
        raise MigrationError("title must be a non-empty single-line value without table separators")
    info = layout(root)
    if info["state"] != "legacy":
        raise MigrationError(f"migration requires legacy layout, found {info['state']}")
    prd = root / ".ai/references/prd"
    version = index_version(prd / "00_INDEX.md")
    mappings = [
        {"legacy_path": f".ai/references/prd/{entry['path']}", "collection_path": f".ai/references/prd/{prd_id}/{entry['path']}", "sha256": entry["sha256"]}
        for entry in info["entries"] if entry["kind"] == "file"
    ]
    return {
        "schema_version": 1, "action": "plan", "state": "legacy", "prd_id": prd_id,
        "title": title.strip(), "current_version": version, "changed": True,
        "legacy_tree_sha256": info["tree_sha256"], "mappings": mappings,
        "impact": reference_impact(root),
    }


def project_index(prd_id: str, title: str, version: str) -> str:
    return (
        "# PRD Collection\n\n"
        "| prd_id | 标题 | 当前版本 | 状态 | 来源线索 | 入口 |\n"
        "|---|---|---|---|---|---|\n"
        f"| {prd_id} | {title} | {version} | active | legacy-migration-receipt | {prd_id}/00_INDEX.md |\n"
    )


def atomic_json(path: Path, payload: dict[str, object]) -> None:
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush(); os.fsync(stream.fileno())
        os.replace(name, path)
    except BaseException:
        try: os.unlink(name)
        except FileNotFoundError: pass
        raise


def apply(root: Path, prd_id: str, title: str, now: str) -> dict[str, object]:
    info = layout(root)
    if info["state"] == "collection" and info.get("has_receipt"):
        receipt = json.loads((root / ".ai/references/prd" / RECEIPT).read_text(encoding="utf-8"))
        if receipt.get("prd_id") == prd_id and receipt.get("title") == title.strip():
            verify_result = verify(root)
            return {"schema_version": 1, "action": "apply", "changed": False, **verify_result}
    plan = build_plan(root, prd_id, title)
    references = root / ".ai/references"
    if references.is_symlink():
        raise MigrationError(".ai/references must not be a symlink")
    prd = references / "prd"
    migration_id = "MIG-" + hashlib.sha256(f"{prd_id}\0{plan['legacy_tree_sha256']}".encode()).hexdigest()[:12]
    backups = references / ".prd-migration-backups"
    if backups.is_symlink() or (backups.exists() and not backups.is_dir()):
        raise MigrationError("migration backup root must be a real directory")
    backups.mkdir(parents=True, exist_ok=True)
    backup = backups / migration_id
    if backup.exists():
        raise MigrationError(f"backup already exists: {backup.relative_to(root)}")
    stage = Path(tempfile.mkdtemp(prefix=".prd-migrate-stage-", dir=references))
    switched = False
    try:
        shutil.copytree(prd, stage / prd_id)
        (stage / "00_INDEX.md").write_text(project_index(prd_id, title.strip(), str(plan["current_version"])), encoding="utf-8", newline="\n")
        collection_entries = safe_tree_entries(stage)
        collection_hash = tree_hash(collection_entries)
        receipt: dict[str, object] = {
            "schema_version": 1, "migration_id": migration_id, "prd_id": prd_id,
            "title": title.strip(), "migrated_at": now,
            "backup": backup.relative_to(root).as_posix(),
            "legacy_tree_sha256": plan["legacy_tree_sha256"],
            "collection_tree_sha256": collection_hash,
            "mappings": plan["mappings"], "impact": plan["impact"],
        }
        atomic_json(stage / RECEIPT, receipt)
        os.replace(prd, backup)
        switched = True
        try:
            os.replace(stage, prd)
        except BaseException:
            os.replace(backup, prd)
            switched = False
            raise
        try:
            result = verify(root)
        except BaseException:
            failed = references / f".prd-failed-{migration_id}"
            os.replace(prd, failed)
            os.replace(backup, prd)
            switched = False
            shutil.rmtree(failed)
            raise
        return {"schema_version": 1, "action": "apply", "changed": True, **result}
    finally:
        if stage.exists():
            shutil.rmtree(stage)
        if switched and not prd.exists() and backup.exists():
            os.replace(backup, prd)


def read_receipt(root: Path) -> dict[str, object]:
    path = root / ".ai/references/prd" / RECEIPT
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MigrationError("collection migration receipt missing or invalid") from error
    required = {"schema_version", "migration_id", "prd_id", "title", "migrated_at", "backup", "legacy_tree_sha256", "collection_tree_sha256", "mappings", "impact"}
    if not isinstance(value, dict) or set(value) != required or value["schema_version"] != 1:
        raise MigrationError("collection migration receipt schema drift")
    validate_prd_id(str(value["prd_id"]))
    if not MIGRATION_ID.fullmatch(str(value["migration_id"])):
        raise MigrationError("migration receipt id is unsafe")
    backup = Path(str(value["backup"]))
    backup_root = root / ".ai/references/.prd-migration-backups"
    if backup_root.is_symlink():
        raise MigrationError("migration receipt backup root is unsafe")
    expected_backup_root = backup_root.resolve()
    resolved_backup = (root / backup).resolve()
    if backup.is_absolute() or ".." in backup.parts or resolved_backup.parent != expected_backup_root or resolved_backup.name != value["migration_id"]:
        raise MigrationError("migration receipt backup path is unsafe")
    if not isinstance(value["mappings"], list):
        raise MigrationError("migration receipt mappings must be a list")
    collection_root = (root / ".ai/references/prd" / str(value["prd_id"])).resolve()
    for mapping in value["mappings"]:
        if not isinstance(mapping, dict) or set(mapping) != {"legacy_path", "collection_path", "sha256"}:
            raise MigrationError("migration receipt mapping schema drift")
        target = Path(str(mapping["collection_path"]))
        legacy = Path(str(mapping["legacy_path"]))
        resolved_target = (root / target).resolve()
        legacy_root = Path(".ai/references/prd")
        if legacy.is_absolute() or ".." in legacy.parts or legacy_root not in legacy.parents:
            raise MigrationError("migration receipt legacy path is unsafe")
        if target.is_absolute() or ".." in target.parts or collection_root not in resolved_target.parents:
            raise MigrationError("migration receipt collection path is unsafe")
    return value


def verify(root: Path) -> dict[str, object]:
    info = layout(root)
    if info["state"] != "collection" or not info.get("has_receipt"):
        raise MigrationError(f"verify requires migrated collection, found {info['state']}")
    receipt = read_receipt(root)
    prd = root / ".ai/references/prd"
    actual = tree_hash(safe_tree_entries(prd, exclude={RECEIPT}))
    if actual != receipt["collection_tree_sha256"]:
        raise MigrationError(f"collection tree hash drift: {actual}")
    for mapping in receipt["mappings"]:
        target = root / str(mapping["collection_path"])
        if not target.is_file() or target.is_symlink() or hashlib.sha256(target.read_bytes()).hexdigest() != mapping["sha256"]:
            raise MigrationError(f"migrated file drift: {mapping['collection_path']}")
    backup = root / str(receipt["backup"])
    if not backup.is_dir() or tree_hash(safe_tree_entries(backup)) != receipt["legacy_tree_sha256"]:
        raise MigrationError("migration backup missing or drifted")
    return {"verified": True, "migration_id": receipt["migration_id"], "prd_id": receipt["prd_id"], "collection_tree_sha256": actual}


def rollback(root: Path) -> dict[str, object]:
    receipt = read_receipt(root)
    verify(root)
    prd = root / ".ai/references/prd"
    backup = root / str(receipt["backup"])
    retired = prd.parent / f".prd-rollback-{receipt['migration_id']}"
    if retired.exists():
        raise MigrationError("rollback staging path already exists")
    os.replace(prd, retired)
    try:
        os.replace(backup, prd)
    except BaseException:
        os.replace(retired, prd)
        raise
    shutil.rmtree(retired)
    return {"schema_version": 1, "action": "rollback", "changed": True, "migration_id": receipt["migration_id"], "state": "legacy"}


def parse_frontmatter(path: Path) -> tuple[list[dict[str, object]], str | None]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise MigrationError("AC file frontmatter missing")
    front = text.split("\n---\n", 1)[0].splitlines()[1:]
    legacy_lines = [line.split(":", 1)[1].strip() for line in front if re.match(r"^prd_version\s*:", line)]
    ref_indexes = [index for index, line in enumerate(front) if re.match(r"^prd_refs\s*:", line)]
    if len(legacy_lines) > 1 or len(ref_indexes) > 1:
        raise MigrationError("duplicate PRD pin field")
    legacy = legacy_lines[0] if legacy_lines else None
    has_refs = bool(ref_indexes)
    if legacy and has_refs:
        raise MigrationError("prd_refs and legacy prd_version cannot coexist")
    refs: list[dict[str, object]] = []
    block: list[str] = []
    if has_refs:
        header = ref_indexes[0]
        if front[header].strip() != "prd_refs:":
            raise MigrationError("prd_refs must use the documented block form")
        cursor = header + 1
        while cursor < len(front) and (not front[cursor].strip() or front[cursor].startswith(" ")):
            if front[cursor].strip():
                block.append(front[cursor])
            cursor += 1
    index = 0
    while index < len(block):
        match = re.match(r"^  - prd_id:\s*(\S+)\s*$", block[index])
        if not match:
            raise MigrationError("unexpected field in prd_refs block")
        if index + 2 >= len(block):
            raise MigrationError("incomplete prd_refs item")
        version_match = re.match(r"^    prd_version:\s*(\S+)\s*$", block[index + 1])
        modules_match = re.match(r"^    module_slugs:\s*\[([^]]*)\]\s*$", block[index + 2])
        if not version_match or not modules_match:
            raise MigrationError("prd_refs item must contain prd_version then inline module_slugs")
        modules = [value.strip() for value in modules_match.group(1).split(",") if value.strip()]
        prd_id = validate_prd_id(match.group(1)); version = version_match.group(1)
        if not VERSION.fullmatch(version) or not modules or len(modules) != len(set(modules)) or any(not MODULE_SLUG.fullmatch(value) for value in modules):
            raise MigrationError("invalid prd_refs version or module_slugs")
        refs.append({"prd_id": prd_id, "prd_version": version, "module_slugs": modules})
        index += 3
    if has_refs and not refs:
        raise MigrationError("prd_refs is empty or malformed")
    if len({str(item["prd_id"]) for item in refs}) != len(refs):
        raise MigrationError("duplicate prd_id in prd_refs")
    if legacy and not VERSION.fullmatch(legacy):
        raise MigrationError("legacy prd_version is invalid")
    return refs, legacy


def resolve_reference(root: Path, ac_file: Path, reference: str) -> dict[str, object]:
    refs, legacy_version = parse_frontmatter(ac_file)
    value = reference.removeprefix(".ai/").removeprefix("references/")
    parts = Path(value).parts
    if not parts or parts[0] != "prd" or Path(value).is_absolute() or ".." in parts:
        raise MigrationError("reference must be a safe PRD-relative path")
    prd_root = root / ".ai/references/prd"
    if refs:
        if len(parts) != 3:
            raise MigrationError("collection reference must be prd/<prd_id>/<module>.md")
        prd_id, filename = parts[1], parts[2]
        module = filename.removesuffix(".md")
        if filename != f"{module}.md" or not MODULE_SLUG.fullmatch(module):
            raise MigrationError("invalid collection module filename")
        item = next((entry for entry in refs if entry["prd_id"] == prd_id), None)
        if item is None or module not in item["module_slugs"]:
            raise MigrationError("reference is not pinned in prd_refs")
        version = str(item["prd_version"])
    elif legacy_version:
        if len(parts) != 2:
            raise MigrationError("legacy reference must be prd/<module>.md")
        filename = parts[1]; module = filename.removesuffix(".md"); version = legacy_version
        if filename != f"{module}.md" or (module != "00_INDEX" and not MODULE_SLUG.fullmatch(module)):
            raise MigrationError("invalid legacy module filename")
        info = layout(root)
        if info["state"] == "legacy":
            prd_id = None
        elif info["state"] == "collection":
            prd_id = str(read_receipt(root)["prd_id"])
        else:
            raise MigrationError("legacy reference has no unique PRD identity")
    else:
        raise MigrationError("AC file has no PRD pin")
    base = prd_root / prd_id if prd_id else prd_root
    current = index_version(base / "00_INDEX.md")
    target = base / filename if current == version else base / ".archive" / version / filename
    if not target.is_file() or target.is_symlink():
        raise MigrationError(f"pinned PRD target missing: {target.relative_to(root)}")
    return {"schema_version": 1, "action": "resolve", "prd_id": prd_id or "legacy-implicit", "prd_version": version, "module_slug": module, "path": target.relative_to(root).as_posix(), "sha256": "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan, migrate, verify, and resolve Butler PRD collections.")
    sub = parser.add_subparsers(dest="action", required=True)
    for name in ("inspect", "plan", "apply", "verify", "rollback", "resolve"):
        command = sub.add_parser(name); command.add_argument("--project-root", required=True)
        if name in {"plan", "apply"}:
            command.add_argument("--prd-id", required=True); command.add_argument("--title", required=True)
        if name == "apply":
            command.add_argument("--now", help=argparse.SUPPRESS)
        if name == "resolve":
            command.add_argument("--ac-file", required=True); command.add_argument("--ref", required=True)
    args = parser.parse_args(argv)
    try:
        root = resolve_root(args.project_root)
        if args.action == "inspect": result = {"schema_version": 1, "action": "inspect", "changed": False, **layout(root)}
        elif args.action == "plan": result = build_plan(root, args.prd_id, args.title)
        elif args.action == "apply": result = apply(root, args.prd_id, args.title, args.now or datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"))
        elif args.action == "verify": result = {"schema_version": 1, "action": "verify", "changed": False, **verify(root)}
        elif args.action == "rollback": result = rollback(root)
        else:
            ac = (root / args.ac_file).resolve()
            try: ac.relative_to(root)
            except ValueError as error: raise MigrationError("AC file escapes project root") from error
            result = resolve_reference(root, ac, args.ref)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except (MigrationError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"schema_version": 1, "error": str(error)}, ensure_ascii=False, sort_keys=True)); return 2


if __name__ == "__main__":
    raise SystemExit(main())
