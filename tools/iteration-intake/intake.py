#!/usr/bin/env python3
"""Plan or transactionally apply a crystallized session-to-iteration intake."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

BUTLER_ROOT = Path(__file__).resolve().parents[2]
FIELDS = {"title", "summary", "confirmed_decisions", "model_recommendations", "open_questions", "in_scope", "out_of_scope", "milestone_route"}
ARRAY_FIELDS = {"confirmed_decisions", "model_recommendations", "open_questions", "in_scope", "out_of_scope"}
LIVE = ("CONCEPT.md", "AC_LIST.md", "TECH_PLAN.md", "VERIFY_REPORT.md", "01_CHANGELOG.md")


class IntakeError(ValueError):
    pass


def validate_spec(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - FIELDS:
        raise IntakeError("spec must be an object with only documented fields")
    required = FIELDS - {"milestone_route"}
    if set(value) < required:
        raise IntakeError(f"spec missing fields: {sorted(required - set(value))}")
    for field in ("title", "summary"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise IntakeError(f"{field} must be a non-empty string")
    for field in ARRAY_FIELDS:
        items = value[field]
        if not isinstance(items, list) or any(not isinstance(item, str) or not item.strip() for item in items):
            raise IntakeError(f"{field} must be an array of non-empty strings")
    if not value["in_scope"]:
        raise IntakeError("in_scope must not be empty")
    route = value.get("milestone_route")
    if route is not None and (not isinstance(route, str) or not re.fullmatch(r"R[1-9][0-9]*", route)):
        raise IntakeError("milestone_route must be null or R<number>")
    return value


def read_spec(path: Path) -> dict[str, Any]:
    try:
        return validate_spec(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise IntakeError(f"cannot read spec: {error}") from error


def current_value(path: Path) -> str:
    match = re.search(r"^current:\s*(\S+)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise IntakeError(f"missing current marker: {path}")
    return match.group(1)


def next_iteration(ai: Path) -> str:
    numbers = []
    sources = [ai / "ITERATIONS.md", ai / "state-index.json"]
    history = ai / "history" / "iterations"
    if history.is_dir() and not history.is_symlink():
        sources.extend(path for path in history.iterdir() if path.is_file() and not path.is_symlink())
    for path in sources:
        if path.is_file():
            try:
                numbers.extend(int(value) for value in re.findall(r"ITER-(\d+)", path.read_text(encoding="utf-8")))
            except (OSError, UnicodeDecodeError):
                continue
    return f"ITER-{max(numbers, default=0) + 1:04d}"


def active_iterations(path: Path) -> list[str]:
    return re.findall(r"^\|\s*(ITER-\d+)\s*\|[^\n]*\|\s*active\s*\|", path.read_text(encoding="utf-8"), re.MULTILINE)


def plan(project_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    project_root = project_root.resolve()
    ai = project_root / ".ai"
    ledger = ai / "ITERATIONS.md"
    milestones = ai / "MILESTONES.md"
    if ai.is_symlink() or not ai.is_dir() or not ledger.is_file() or not milestones.is_file():
        raise IntakeError("project is not a Butler-enabled project")
    active = active_iterations(ledger)
    current = current_value(ledger)
    if active or current != "none":
        return {"status": "active-exists", "active_iterations": active or [current], "writes": []}
    milestone = current_value(milestones)
    if milestone != "none" and not spec.get("milestone_route"):
        return {"status": "needs-milestone-route", "milestone": milestone, "writes": []}
    identity = next_iteration(ai)
    writes = [f".ai/{name}" for name in LIVE] + [".ai/ITERATIONS.md", ".ai/task-state.md", ".ai/02_SESSION_HANDOFF.md", ".ai/handoff-state.json", ".ai/state-index.json"]
    if milestone != "none":
        writes.extend([".ai/MILESTONES.md", ".ai/MILESTONE.md"])
    return {"status": "ready", "iteration": identity, "flow": "complete", "milestone": None if milestone == "none" else milestone, "milestone_route": spec.get("milestone_route"), "writes": writes}


def bullets(items: list[str], empty: str = "N/A") -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {empty}"


def render_artifacts(ai: Path, identity: str, spec: dict[str, Any]) -> None:
    templates = BUTLER_ROOT / "tools/artifact-pipeline/templates"
    for name in LIVE:
        text = (templates / name).read_text(encoding="utf-8").replace("{{ITERATION}}", identity).replace("{{TITLE}}", spec["title"])
        if name == "CONCEPT.md":
            understanding = [spec["summary"], *[f"已确认：{item}" for item in spec["confirmed_decisions"]], *[f"建议（未确认）：{item}" for item in spec["model_recommendations"]]]
            text = text.replace("- {{CONTENT}}", bullets(understanding), 1)
            text = text.replace("- {{CONTENT}}", bullets(spec["in_scope"]), 1)
            text = text.replace("- N/A", bullets(spec["open_questions"]), 1)
        (ai / name).write_text(text, encoding="utf-8")


def update_ledger(path: Path, identity: str, title: str, milestone: str | None) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^current:\s*none\s*$", f"current: {identity}", text, count=1, flags=re.MULTILINE)
    separator = "|---|---|---|---|---|---|---|"
    row = f"| {identity} | {title} | active | {dt.date.today().isoformat()} | — | {milestone or '—'} | — |"
    if separator not in text:
        raise IntakeError("iteration ledger table header is invalid")
    path.write_text(text.replace(separator, separator + "\n" + row, 1), encoding="utf-8")


def update_milestone(ai: Path, milestone: str, route: str, identity: str) -> None:
    board = ai / "MILESTONES.md"
    lines = board.read_text(encoding="utf-8").splitlines()
    found = False
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 9 and cells[1] == milestone:
            cells[6] = identity if cells[6] in {"", "—"} else f"{cells[6]}, {identity}"
            lines[index] = "| " + " | ".join(cells[1:-1]) + " |"
            found = True
            break
    if not found:
        raise IntakeError(f"active milestone row missing: {milestone}")
    board.write_text("\n".join(lines) + "\n", encoding="utf-8")
    detail = ai / "MILESTONE.md"
    if not detail.is_file():
        raise IntakeError("active milestone detail is missing")
    route_lines = detail.read_text(encoding="utf-8").splitlines()
    found = False
    for index, line in enumerate(route_lines):
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 6 and cells[1] == route and cells[3] == "—" and cells[4] == "planned":
            cells[3], cells[4] = identity, "active"
            route_lines[index] = "| " + " | ".join(cells[1:-1]) + " |"
            found = True
            break
    if not found:
        raise IntakeError(f"milestone route is unavailable: {route}")
    detail.write_text("\n".join(route_lines) + "\n", encoding="utf-8")


def sync_state(project_root: Path) -> None:
    commands = [
        [sys.executable, str(BUTLER_ROOT / "tools/state-ledger/state_ledger.py"), "migrate", "--project-root", str(project_root)],
        [sys.executable, str(BUTLER_ROOT / "tools/handoff/handoff.py"), "sync", "--project-root", str(project_root)],
    ]
    for command in commands:
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode:
            raise IntakeError(result.stderr.strip() or result.stdout.strip() or "state synchronization failed")


def apply(project_root: Path, spec: dict[str, Any], *, after_write: Callable[[], None] | None = None) -> dict[str, Any]:
    project_root = project_root.resolve()
    proposed = plan(project_root, spec)
    if proposed["status"] != "ready":
        raise IntakeError(f"apply refused: {proposed['status']}")
    ai = project_root / ".ai"
    lock = ai / ".iteration-intake.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
    except FileExistsError as error:
        raise IntakeError("another iteration intake is active") from error
    snapshot_parent = Path(tempfile.mkdtemp(prefix="butler-iteration-intake-", dir=project_root.parent))
    snapshot = snapshot_parent / "ai"
    try:
        shutil.copytree(ai, snapshot, symlinks=True, ignore=shutil.ignore_patterns(lock.name))
        identity = proposed["iteration"]
        update_ledger(ai / "ITERATIONS.md", identity, spec["title"], proposed["milestone"])
        if proposed["milestone"]:
            update_milestone(ai, proposed["milestone"], spec["milestone_route"], identity)
        render_artifacts(ai, identity, spec)
        (ai / "task-state.md").write_text(
            f"# Task State\n\n- 当前迭代：{identity}\n- 当前里程碑：{proposed['milestone'] or '无 active'}\n- 阶段：P1 Analysis\n- 状态：已从会话结晶需求，等待确认 Current Understanding 与 Scope。\n- 下一动作：审阅 `.ai/CONCEPT.md`，确认后进入 P2。\n",
            encoding="utf-8",
        )
        if after_write:
            after_write()
        sync_state(project_root)
        return {**proposed, "status": "applied"}
    except Exception:
        lock.unlink(missing_ok=True)
        shutil.rmtree(ai)
        shutil.copytree(snapshot, ai, symlinks=True)
        raise
    finally:
        lock.unlink(missing_ok=True)
        shutil.rmtree(snapshot_parent, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "apply"))
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        spec = read_spec(args.spec.resolve())
        result = plan(args.project_root, spec) if args.command == "plan" else apply(args.project_root, spec)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] in {"ready", "applied"} else 3
    except (IntakeError, OSError) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
