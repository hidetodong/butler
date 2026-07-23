#!/usr/bin/env python3
"""Machine contract for Butler's five live iteration artifacts."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable

MARKER_RE = re.compile(r"<!-- butler-artifact-template: ([0-9]+\.[0-9]+\.[0-9]+) artifact=([a-z_]+) -->")
H2_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^([^#\n][^:\n]{0,40}):\s*(.*?)\s*$", re.MULTILINE)


class ContractError(ValueError):
    pass


PHASE_ORDER = {"P1": 1, "P2": 2, "P3": 3, "P5": 4, "close": 5}


def load_manifest(tool_root: Path) -> dict[str, object]:
    path = tool_root / "artifacts.v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("artifacts"), dict):
        raise ContractError("unsupported artifact manifest")
    return data


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContractError("unterminated frontmatter")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or key.strip() in result:
            raise ContractError("invalid or duplicate frontmatter key")
        result[key.strip()] = value.strip()
    return result


def table_header(section_body: str) -> list[str] | None:
    for line in section_body.splitlines():
        if line.startswith("| ") and line.endswith(" |") and not line.startswith("|---"):
            return [cell.strip() for cell in line.strip().strip("|").split("|")]
    return None


def validate_text(name: str, text: str, manifest: dict[str, object], require_marker: bool = True) -> list[str]:
    errors: list[str] = []
    artifacts = manifest["artifacts"]
    if name not in artifacts:
        return [f"unknown artifact: {name}"]
    spec = artifacts[name]
    marker = MARKER_RE.search(text)
    if require_marker and (marker is None or marker.group(1) != manifest["template_version"] or marker.group(2) != name):
        errors.append("template marker mismatch")
    headings = H2_RE.findall(text)
    if headings != spec["sections"]:
        errors.append(f"section order mismatch: {headings!r}")
    if len(re.findall(r"^# (?!#)", text, re.MULTILINE)) != 1:
        errors.append("artifact must contain exactly one H1")
    meta = frontmatter(text)
    for key, allowed in spec.get("frontmatter", {}).items():
        value = meta.get(key)
        if value is None:
            errors.append(f"missing frontmatter: {key}")
        elif isinstance(allowed, list) and value not in allowed:
            errors.append(f"invalid frontmatter value: {key}")
        elif allowed == "date-or-dash" and value != "—" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
            errors.append(f"invalid date field: {key}")
    fields = dict(FIELD_RE.findall(text))
    for key, allowed in spec.get("fields", {}).items():
        if fields.get(key) not in allowed:
            errors.append(f"invalid or missing field: {key}")
    sections = re.split(r"^## .+?\s*$", text, flags=re.MULTILINE)[1:]
    for heading, body in zip(headings, sections):
        expected = spec.get("fixed_tables", {}).get(heading)
        if expected is not None and table_header(body) != expected:
            errors.append(f"table header mismatch: {heading}")
    return errors


def validate_templates(tool_root: Path) -> dict[str, list[str]]:
    manifest = load_manifest(tool_root)
    failures: dict[str, list[str]] = {}
    for name, spec in manifest["artifacts"].items():
        path = tool_root / spec["template"]
        errors = validate_text(name, path.read_text(encoding="utf-8"), manifest)
        if errors:
            failures[name] = errors
    return failures


def render(tool_root: Path, name: str, iteration: str, title: str = "") -> str:
    manifest = load_manifest(tool_root)
    try:
        spec = manifest["artifacts"][name]
    except KeyError as exc:
        raise ContractError(f"unknown artifact: {name}") from exc
    text = (tool_root / spec["template"]).read_text(encoding="utf-8")
    return text.replace("{{ITERATION}}", iteration).replace("{{TITLE}}", title).replace("{{CONTENT}}", "N/A")


def atomic_write(path: Path, text: str, replace: Callable = os.replace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def generate(project_root: Path, tool_root: Path, name: str, iteration: str, title: str, mode: str, current_phase: str, dry_run: bool, force: bool) -> dict[str, object]:
    manifest = load_manifest(tool_root)
    if name not in manifest["artifacts"]:
        raise ContractError(f"unknown artifact: {name}")
    spec = manifest["artifacts"][name]
    if current_phase not in PHASE_ORDER or PHASE_ORDER[spec["phase"]] > PHASE_ORDER[current_phase]:
        raise ContractError(f"artifact {name} is downstream of {current_phase}")
    target = project_root / spec["path"]
    if target.is_symlink():
        raise ContractError(f"refuse symlink target: {spec['path']}")
    exists = target.exists()
    if mode == "init" and exists:
        return {"status": "unchanged", "artifact": name, "path": spec["path"], "changed": False}
    if mode == "reset" and exists and not force:
        raise ContractError("reset requires --force when target exists")
    text = render(tool_root, name, iteration, title)
    changed = not exists or target.read_text(encoding="utf-8") != text
    if changed and not dry_run:
        atomic_write(target, text)
    return {"status": "planned" if dry_run else "ok", "artifact": name, "path": spec["path"], "changed": changed}


def check_artifact(project_root: Path, tool_root: Path, name: str) -> dict[str, object]:
    manifest = load_manifest(tool_root)
    if name not in manifest["artifacts"]:
        raise ContractError(f"unknown artifact: {name}")
    spec = manifest["artifacts"][name]
    path = project_root / spec["path"]
    if path.is_symlink() or not path.is_file():
        return {"artifact": name, "path": spec["path"], "status": "drift", "errors": ["missing or non-regular file"]}
    text = path.read_text(encoding="utf-8")
    if MARKER_RE.search(text) is None:
        return {"artifact": name, "path": spec["path"], "status": "legacy", "errors": []}
    errors = validate_text(name, text, manifest)
    return {"artifact": name, "path": spec["path"], "status": "drift" if errors else "ok", "errors": errors}


def check_project(project_root: Path, tool_root: Path) -> dict[str, object]:
    manifest = load_manifest(tool_root)
    results = [check_artifact(project_root, tool_root, name) for name in manifest["artifacts"]]
    drift = [item["artifact"] for item in results if item["status"] == "drift"]
    return {"status": "drift" if drift else "ok", "drift": drift, "artifacts": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("render", "init", "reset", "check"))
    parser.add_argument("artifact")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--iteration", default="ITER-0001")
    parser.add_argument("--title", default="")
    parser.add_argument("--current-phase", default="close", choices=tuple(PHASE_ORDER))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    tool_root = Path(__file__).resolve().parent
    try:
        if args.command == "check":
            result = check_project(Path(args.project_root).resolve(), tool_root) if args.artifact == "project" else check_artifact(Path(args.project_root).resolve(), tool_root, args.artifact)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 1 if result.get("status") == "drift" else 0
        if args.command == "render":
            manifest = load_manifest(tool_root)
            spec = manifest["artifacts"].get(args.artifact)
            if spec is None or PHASE_ORDER[spec["phase"]] > PHASE_ORDER[args.current_phase]:
                raise ContractError("unknown or downstream artifact")
            print(render(tool_root, args.artifact, args.iteration, args.title), end="")
            return 0
        result = generate(Path(args.project_root).resolve(), tool_root, args.artifact, args.iteration, args.title, args.command, args.current_phase, args.dry_run, args.force)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, ContractError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
