#!/usr/bin/env python3
"""Read-only real-project dogfood with all mutations confined to a temp copy."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DISCOVER = REPO / "tools/workspace-scope/workspace_scope.py"
MIGRATE = REPO / "tools/prd-migrate/prd_migrate.py"


class DogfoodError(ValueError):
    pass


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        digest.update(path.relative_to(root).as_posix().encode())
        if path.is_symlink():
            digest.update(b"L" + str(path.readlink()).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
        else:
            digest.update(b"D")
    return "sha256:" + digest.hexdigest()


def status_hash(root: Path) -> str:
    result = subprocess.run(["git", "-C", str(root), "status", "--porcelain=v1", "-z"], capture_output=True, check=False)
    if result.returncode:
        raise DogfoodError("sample root must be a readable Git worktree")
    return "sha256:" + hashlib.sha256(result.stdout).hexdigest()


def call(tool: Path, *args: str) -> dict:
    result = subprocess.run([sys.executable, str(tool), *args], text=True, capture_output=True, check=False)
    if result.returncode:
        try:
            detail = json.loads(result.stdout).get("error", result.stdout.strip())
        except json.JSONDecodeError:
            detail = result.stdout.strip() or result.stderr.strip()
        raise DogfoodError(f"{tool.name} failed: {detail}")
    return json.loads(result.stdout)


def copy_sample(source: Path, target: Path) -> None:
    shutil.copytree(source / ".ai", target / ".ai")
    shutil.copy2(source / "package.json", target / "package.json")
    for group in ("apps", "packages"):
        parent = source / group
        if not parent.is_dir() or parent.is_symlink():
            continue
        for manifest in sorted(parent.glob("*/package.json")):
            if manifest.is_symlink():
                raise DogfoodError(f"sample manifest is a symlink: {manifest.relative_to(source)}")
            destination = target / manifest.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest, destination)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-root", required=True, type=Path)
    parser.add_argument("--prd-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--ac-file", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--now", required=True)
    args = parser.parse_args(argv)
    try:
        source = args.sample_root.resolve(strict=True)
        if not (source / ".ai/references/prd").is_dir() or not (source / "package.json").is_file():
            raise DogfoodError("sample root lacks required .ai PRD state or package.json")
        before_status = status_hash(source)
        before_prd = tree_hash(source / ".ai/references/prd")
        ledger = (source / ".ai/MILESTONES.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="butler-mile0009-dogfood-") as temporary:
            target = Path(temporary) / "sample"
            copy_sample(source, target)
            discovery = call(DISCOVER, "discover", "--project-root", str(target))["discovery"]
            inspected = call(MIGRATE, "inspect", "--project-root", str(target))
            planned = call(MIGRATE, "plan", "--project-root", str(target), "--prd-id", args.prd_id, "--title", args.title)
            applied = call(MIGRATE, "apply", "--project-root", str(target), "--prd-id", args.prd_id, "--title", args.title, "--now", args.now)
            verified = call(MIGRATE, "verify", "--project-root", str(target))
            resolved = call(MIGRATE, "resolve", "--project-root", str(target), "--ac-file", args.ac_file, "--ref", args.ref)
            rolled_back = call(MIGRATE, "rollback", "--project-root", str(target))
            restored = call(MIGRATE, "inspect", "--project-root", str(target))
        after_status = status_hash(source)
        after_prd = tree_hash(source / ".ai/references/prd")
        if before_status != after_status or before_prd != after_prd:
            raise DogfoodError("read-only sample changed during dogfood")
        if inspected["tree_sha256"] != restored["tree_sha256"] or restored["state"] != "legacy":
            raise DogfoodError("temporary rollback did not restore the legacy PRD tree")
        payload = {
            "schema_version": 1,
            "ok": True,
            "sample_zero_write": True,
            "sample_status_sha256": before_status,
            "sample_prd_tree_sha256": before_prd,
            "workspace_count": len(discovery["candidates"]),
            "legacy_state": inspected["state"],
            "legacy_tree_sha256": inspected["tree_sha256"],
            "impact_groups": sorted({item["group"] for item in planned["impact"]}),
            "milestone_state_markers": {"active": "active" in ledger, "queued": "queued" in ledger},
            "migration_id": applied["migration_id"],
            "verified": verified["verified"],
            "resolved_path": resolved["path"],
            "resolved_sha256": resolved["sha256"],
            "rollback_state": rolled_back["state"],
            "restored_tree_sha256": restored["tree_sha256"],
        }
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (DogfoodError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"schema_version": 1, "ok": False, "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
