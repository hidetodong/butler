#!/usr/bin/env python3
"""Generate and verify a bounded handoff derived from authoritative project state."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

SCHEMA_VERSION = 1
HANDOFF = ".ai/02_SESSION_HANDOFF.md"
RECEIPT = ".ai/handoff-state.json"
ID_RE = re.compile(r"^(?:ITER|MILE)-[0-9]{4,}$")


class HandoffError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_file(root: Path, relative: str, *, required: bool = True) -> bytes | None:
    root = root.resolve()
    path = root / relative
    if path.is_symlink():
        raise HandoffError(f"拒绝 symlink 输入：{relative}")
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        if required:
            raise HandoffError(f"缺少状态文件：{relative}")
        return None
    if resolved.parent != root and root not in resolved.parents:
        raise HandoffError(f"状态路径越出项目根：{relative}")
    if not resolved.is_file():
        raise HandoffError(f"状态路径不是普通文件：{relative}")
    return resolved.read_bytes()


def decode(data: bytes, relative: str) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise HandoffError(f"状态文件不是 UTF-8：{relative}") from error


def current(text: str, label: str, prefix: str) -> str:
    match = re.search(r"^current:\s*(\S+)\s*$", text, re.MULTILINE)
    if not match:
        raise HandoffError(f"{label} 缺少 current 指针")
    value = match.group(1)
    if value != "none" and (not ID_RE.fullmatch(value) or not value.startswith(prefix + "-")):
        raise HandoffError(f"{label} current 非法：{value}")
    if value != "none":
        rows = [line for line in text.splitlines() if line.startswith(f"| {value} |")]
        if not rows:
            raise HandoffError(f"{label} current 在台账中无对应行：{value}")
        cells = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]
        if len(cells) < 3 or cells[2] != "active":
            raise HandoffError(f"{label} current 对应行不是 active：{value}")
    return value


def task_fields(text: str) -> dict[str, str]:
    aliases = {
        "iteration": "当前迭代",
        "milestone": "当前里程碑",
        "phase": "阶段",
        "status": "状态",
        "next": "下一动作",
    }
    result: dict[str, str] = {}
    for key, label in aliases.items():
        match = re.search(rf"^- {re.escape(label)}[：:]\s*(.+?)\s*$", text, re.MULTILINE)
        if not match:
            raise HandoffError(f"task-state 缺少字段：{label}")
        result[key] = match.group(1).strip()
    return result


def section_bullets(text: str, names: tuple[str, ...], limit: int = 3) -> list[str]:
    headings = "|".join(re.escape(name) for name in names)
    match = re.search(rf"^#(?:#)?\s+(?:{headings})\s*$\n(.*?)(?=^#|\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    values = []
    for line in match.group(1).splitlines():
        if line.startswith("- ") and line[2:].strip() not in {"N/A", "无", "—"}:
            values.append(line[2:].strip())
        if len(values) == limit:
            break
    return values


def source_paths(root: Path, fields: dict[str, str], iteration: str, milestone: str) -> list[str]:
    paths = [".ai/task-state.md", ".ai/ITERATIONS.md"]
    if (root / ".ai/MILESTONES.md").is_file():
        paths.append(".ai/MILESTONES.md")
    if milestone != "none":
        paths.append(".ai/MILESTONE.md")
    if iteration != "none":
        phase = fields["phase"].upper()
        paths.append(".ai/CONCEPT.md")
        if any(token in phase for token in ("P2", "P3", "P4", "P5")):
            paths.append(".ai/AC_LIST.md")
        if any(token in phase for token in ("P3", "P4", "P5")):
            paths.append(".ai/TECH_PLAN.md")
        if "P5" in phase:
            paths.append(".ai/VERIFY_REPORT.md")
    return paths


def build_snapshot(root: Path) -> tuple[dict[str, object], list[dict[str, str]], dict[str, str]]:
    task_data = regular_file(root, ".ai/task-state.md")
    iter_data = regular_file(root, ".ai/ITERATIONS.md")
    assert task_data is not None and iter_data is not None
    task_text = decode(task_data, ".ai/task-state.md")
    iter_text = decode(iter_data, ".ai/ITERATIONS.md")
    fields = task_fields(task_text)
    iteration = current(iter_text, "ITERATIONS.md", "ITER")
    milestone = "none"
    milestone_data = regular_file(root, ".ai/MILESTONES.md", required=False)
    if milestone_data is not None:
        milestone = current(decode(milestone_data, ".ai/MILESTONES.md"), "MILESTONES.md", "MILE")
    normalized_iteration = "none" if fields["iteration"] in {"none", "无 active"} else fields["iteration"]
    normalized_milestone = "none" if fields["milestone"] in {"none", "无 active"} else fields["milestone"]
    if normalized_iteration != iteration or normalized_milestone != milestone:
        raise HandoffError("task-state 与台账 current 不一致")
    paths = source_paths(root, fields, iteration, milestone)
    sources: list[dict[str, str]] = []
    texts: dict[str, str] = {}
    for relative in paths:
        data = regular_file(root, relative)
        assert data is not None
        sources.append({"path": relative, "sha256": digest(data)})
        texts[relative] = decode(data, relative)
    decisions: list[str] = []
    risks: list[str] = []
    for relative in reversed(paths):
        text = texts[relative]
        if not decisions:
            decisions = section_bullets(text, ("Design Decisions", "Current Understanding", "关键决策摘要"))
        if not risks:
            risks = section_bullets(text, ("Risks / Open Questions", "Open Questions", "Open Questions / Risks", "Remaining Risks"))
    snapshot: dict[str, object] = {
        "iteration": iteration,
        "milestone": milestone,
        "phase": fields["phase"],
        "status": fields["status"],
        "next": fields["next"],
        "decisions": decisions,
        "risks": risks,
        "pointers": paths,
    }
    return snapshot, sources, texts


def render(snapshot: dict[str, object]) -> str:
    iteration = snapshot["iteration"]
    milestone = snapshot["milestone"]
    iteration_label = "无 active" if iteration == "none" else iteration
    milestone_label = "无 active" if milestone == "none" else milestone
    decisions = snapshot["decisions"] or ["以当前阶段产物和 task-state 为准；本文件不另立决策真源。"]
    risks = snapshot["risks"] or ["N/A"]
    lines = [
        "# Session Handoff", "", "## 任务断点", "",
        f"- 迭代：{iteration_label}；里程碑：{milestone_label}；阶段：{snapshot['phase']}。",
        f"- 状态：{snapshot['status']}", "", "## 关键决策摘要", "",
        *[f"- {item}" for item in decisions], "", "## 环境脏点", "",
        "- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。", "",
        "## 已知风险", "", *[f"- {item}" for item in risks], "", "## 唤醒指令", "",
        f"- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：{snapshot['next']}",
        "", "## 状态指针", "", *[f"- `{item}`" for item in snapshot["pointers"]], "",
    ]
    return "\n".join(lines)


def safe_target(root: Path, relative: str) -> Path:
    root = root.resolve()
    path = root / relative
    if path.is_symlink():
        raise HandoffError(f"拒绝覆盖 symlink：{relative}")
    if path.parent.resolve() != (root / ".ai").resolve():
        raise HandoffError(f"输出路径越界：{relative}")
    return path


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def transactional_pair(first: Path, first_data: bytes, second: Path, second_data: bytes) -> None:
    originals = {path: path.read_bytes() if path.is_file() else None for path in (first, second)}
    try:
        atomic_write(first, first_data)
        atomic_write(second, second_data)
    except BaseException:
        for path in (first, second):
            original = originals[path]
            if original is None:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            else:
                atomic_write(path, original)
        raise


def expected(root: Path) -> tuple[dict[str, object], bytes, bytes]:
    snapshot, sources, _ = build_snapshot(root)
    handoff = render(snapshot).encode("utf-8")
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "sources": sources,
        "handoff_sha256": digest(handoff),
        "snapshot": snapshot,
    }
    receipt_bytes = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return receipt, handoff, receipt_bytes


def inspect(root: Path) -> dict[str, object]:
    receipt, handoff, _ = expected(root)
    return {"schema_version": SCHEMA_VERSION, "status": "inspect", "snapshot": receipt["snapshot"], "sources": receipt["sources"], "handoff_sha256": digest(handoff)}


def sync(root: Path) -> dict[str, object]:
    receipt, handoff, receipt_bytes = expected(root)
    handoff_path = safe_target(root, HANDOFF)
    receipt_path = safe_target(root, RECEIPT)
    changed = not handoff_path.is_file() or handoff_path.read_bytes() != handoff or not receipt_path.is_file() or receipt_path.read_bytes() != receipt_bytes
    transactional_pair(handoff_path, handoff, receipt_path, receipt_bytes)
    return {"schema_version": SCHEMA_VERSION, "status": "fresh", "changed": changed, "handoff_sha256": receipt["handoff_sha256"]}


def check(root: Path) -> tuple[int, dict[str, object]]:
    expected_receipt, expected_handoff, _ = expected(root)
    reasons: list[str] = []
    handoff_data = regular_file(root, HANDOFF, required=False)
    receipt_data = regular_file(root, RECEIPT, required=False)
    if handoff_data is None:
        reasons.append("handoff-missing")
    if receipt_data is None:
        reasons.append("receipt-missing")
    actual: object = None
    if receipt_data is not None:
        try:
            actual = json.loads(decode(receipt_data, RECEIPT))
        except (json.JSONDecodeError, HandoffError):
            reasons.append("receipt-invalid")
    if isinstance(actual, dict):
        if actual.get("schema_version") != SCHEMA_VERSION:
            reasons.append("receipt-schema")
        if actual.get("sources") != expected_receipt["sources"]:
            reasons.append("sources-changed")
        if actual.get("snapshot") != expected_receipt["snapshot"]:
            reasons.append("snapshot-changed")
        if handoff_data is not None and actual.get("handoff_sha256") != digest(handoff_data):
            reasons.append("handoff-tampered")
    if handoff_data is not None and handoff_data != expected_handoff:
        reasons.append("handoff-not-current")
    reasons = sorted(set(reasons))
    result = {"schema_version": SCHEMA_VERSION, "status": "fresh" if not reasons else "stale", "reasons": reasons}
    return (0 if not reasons else 1), result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "sync", "check"):
        item = sub.add_parser(name)
        item.add_argument("--project-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.project_root.expanduser().resolve(strict=True)
        if not root.is_dir() or not (root / ".ai").is_dir():
            raise HandoffError("project-root 不是 Butler 项目")
        if args.command == "inspect":
            result = inspect(root)
            code = 0
        elif args.command == "sync":
            result = sync(root)
            code = 0
        else:
            code, result = check(root)
    except (HandoffError, OSError) as error:
        result = {"schema_version": SCHEMA_VERSION, "status": "error", "error": str(error)}
        code = 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
