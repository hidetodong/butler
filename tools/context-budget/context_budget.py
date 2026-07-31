#!/usr/bin/env python3
"""Deterministic checks for Butler's progressive context-loading contract."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


L0_BEGIN = "<!-- butler-context-l0:begin -->"
L0_END = "<!-- butler-context-l0:end -->"
L0_LIMITS = {"bytes": 1600, "nonempty_lines": 18, "pointers": 4}
L1_LIMITS = {"bytes": 7000, "lines": 70, "pointers": 15}
CONTEXT_MAP_LIMITS = {"bytes": 9000, "lines": 120, "pointers": 24}
CONTEXTS = {
    "需求与范围",
    "交付生命周期",
    "可信保证",
    "宿主运行时",
    "知识连续性",
}
ROUTES = {"普通冷启动", "单术语消歧", "跨上下文设计", "完整领域审查"}
FACT_CLASSES = {"权威事实", "受控投影", "派生视图", "叙述摘要"}
TRANSITIONS = {
    "PRD→AC": ("需求与范围", "可信保证"),
    "AC→TECH_PLAN": ("可信保证", "交付生命周期"),
    "TECH_PLAN→Evidence": ("交付生命周期", "可信保证"),
    "Evidence→Goal Verdict": ("可信保证", "可信保证"),
    "Goal/权威状态→Handoff": ("交付生命周期、可信保证", "知识连续性"),
}
TRANSITION_FIELDS = {
    "源上下文",
    "目标上下文",
    "输入",
    "输出",
    "最小保真",
    "失效条件",
    "责任方",
    "权威关系",
    "直接真源",
}
RECEIPT_FIELDS = {
    "当前问题",
    "已知结论",
    "缺失证据",
    "已读来源",
    "下一批来源",
    "选择理由",
}
DUPLICATE_CANDIDATES = (
    "Coder/README.md",
    "Coder/architecture-overview.md",
    ".ai/project/architecture.md",
    ".ai/project/invariants.md",
    ".ai/project/debt.md",
)
CONTEXT_HEADER = ("上下文", "目的", "语义所有权", "明确不负责", "首要真源")
GLOSSARY_HEADER = (
    "概念",
    "上下文限定",
    "白话定义",
    "语义所有者",
    "定义真源",
    "明确不代表",
)
MD_POINTER_RE = re.compile(r"`([^`\n]+\.md(?:#[^`\n]+)?)`")


@dataclass(frozen=True)
class CheckResult:
    metrics: dict[str, int]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _read(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise ValueError(f"missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def _table(text: str, expected_header: tuple[str, ...]) -> list[list[str]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = _cells(line)
        if tuple(cells) != expected_header:
            continue
        if index + 1 >= len(lines) or not _is_separator(_cells(lines[index + 1])):
            raise ValueError(f"table missing separator: {' | '.join(expected_header)}")
        rows: list[list[str]] = []
        for candidate in lines[index + 2 :]:
            row = _cells(candidate)
            if not row:
                break
            if len(row) != len(expected_header):
                raise ValueError(
                    f"table row has {len(row)} cells, expected {len(expected_header)}: {candidate}"
                )
            rows.append(row)
        return rows
    raise ValueError(f"table not found: {' | '.join(expected_header)}")


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _pointer_count(text: str) -> int:
    return len(MD_POINTER_RE.findall(text))


def _transition_blocks(text: str) -> dict[str, dict[str, str]]:
    blocks: dict[str, dict[str, str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = None
            continue
        if line.startswith("### "):
            current = line.removeprefix("### ").strip()
            if current in blocks:
                raise ValueError(f"duplicate transition: {current}")
            blocks[current] = {}
            continue
        if current is None or not line.startswith("- ") or "：" not in line:
            continue
        label, value = line.removeprefix("- ").split("：", 1)
        label = label.strip()
        if label in blocks[current]:
            raise ValueError(f"duplicate transition field: {current}.{label}")
        blocks[current][label] = value.strip()
    return blocks


def _metric_errors(
    name: str, text: str, limits: dict[str, int], *, physical_lines: bool
) -> tuple[dict[str, int], list[str]]:
    metrics = {
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.splitlines()),
        "nonempty_lines": sum(bool(line.strip()) for line in text.splitlines()),
        "pointers": _pointer_count(text),
    }
    errors: list[str] = []
    for key, limit in limits.items():
        actual_key = "lines" if physical_lines and key == "lines" else key
        if metrics[actual_key] > limit:
            errors.append(f"{name} {actual_key}={metrics[actual_key]} exceeds {limit}")
    return metrics, errors


def _validate_source(root: Path, raw: str) -> bool:
    relative = raw.split("#", 1)[0]
    if not relative or relative.startswith("/") or ".." in Path(relative).parts:
        return False
    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        return False
    return resolved.is_relative_to(root) and resolved.is_file()


def check_project(root: Path) -> CheckResult:
    root = root.resolve()
    readme = _read(root, "Coder/README.md")
    l1 = _read(root, "Coder/domain-model.md")
    glossary = _read(root, "Coder/domain-glossary.md")
    context_map = _read(root, "Coder/context-map.md")
    errors: list[str] = []

    if readme.count(L0_BEGIN) != 1 or readme.count(L0_END) != 1:
        raise ValueError("L0 markers must each occur exactly once")
    before, remainder = readme.split(L0_BEGIN, 1)
    l0, after = remainder.split(L0_END, 1)
    if L0_END in before or L0_BEGIN in after:
        raise ValueError("L0 markers are malformed")

    l0_metrics, l0_errors = _metric_errors(
        "L0", l0, L0_LIMITS, physical_lines=False
    )
    l1_metrics, l1_errors = _metric_errors(
        "L1", l1, L1_LIMITS, physical_lines=True
    )
    errors.extend(l0_errors)
    errors.extend(l1_errors)
    map_metrics, map_errors = _metric_errors(
        "context-map", context_map, CONTEXT_MAP_LIMITS, physical_lines=True
    )
    errors.extend(map_errors)

    l0_requirements = {
        "ordinary-stop": ("普通单模块任务", "不得默认加载"),
        "route-to-l1": ("跨模块所有权", "domain-model.md"),
        "no-recursion": ("不得递归", "整目录读取"),
    }
    for label, tokens in l0_requirements.items():
        if not all(token in l0 for token in tokens):
            errors.append(f"L0 missing semantic requirement: {label}")

    context_rows = _table(l1, CONTEXT_HEADER)
    context_names = [row[0] for row in context_rows]
    if set(context_names) != CONTEXTS or len(context_names) != len(CONTEXTS):
        errors.append(f"L1 contexts mismatch: {context_names}")
    if any(not all(row) for row in context_rows):
        errors.append("L1 context table contains an empty required cell")

    route_rows = _table(l1, ("路径", "触发", "读取", "停止条件"))
    route_names = [row[0] for row in route_rows]
    if set(route_names) != ROUTES or len(route_names) != len(ROUTES):
        errors.append(f"L1 routes mismatch: {route_names}")
    if not RECEIPT_FIELDS.issubset(set(re.findall(r"^- (.+)$", l1, re.MULTILINE))):
        errors.append("L1 fan-out receipt is missing one or more required fields")
    for forbidden in ("## 统一语言审计", "## 用现存冲突反向验证", "允许递归", "默认整目录读取"):
        if forbidden in l1:
            errors.append(f"L1 contains forbidden pattern: {forbidden}")
    if "禁止递归追随引用" not in l1 or "每批最多 3 份" not in l1:
        errors.append("L1 is missing batch or no-recursion guard")

    glossary_rows = _table(glossary, GLOSSARY_HEADER)
    if len(glossary_rows) != 20:
        errors.append(f"L2 term count={len(glossary_rows)}, expected 20")
    concepts = [row[0] for row in glossary_rows]
    if len(set(concepts)) != len(concepts):
        errors.append("L2 concepts must be unique")
    for index, row in enumerate(glossary_rows, start=1):
        if not all(row):
            errors.append(f"L2 row {index} contains an empty required cell")
            continue
        if row[3] not in CONTEXTS:
            errors.append(f"L2 row {index} has unknown owner: {row[3]}")
        sources = MD_POINTER_RE.findall(row[4])
        if len(sources) != 1 or not _validate_source(root, sources[0]):
            errors.append(f"L2 row {index} has invalid definition source: {row[4]}")

    fact_rows = _table(context_map, ("层级", "含义", "写入边界"))
    fact_names = [row[0] for row in fact_rows]
    if set(fact_names) != FACT_CLASSES or len(fact_names) != len(FACT_CLASSES):
        errors.append(f"context-map fact classes mismatch: {fact_names}")
    if any(not all(row) for row in fact_rows):
        errors.append("context-map fact table contains an empty required cell")

    transition_blocks = _transition_blocks(context_map)
    if set(transition_blocks) != set(TRANSITIONS):
        errors.append(
            f"context-map transitions mismatch: {sorted(transition_blocks)}"
        )
    for name, expected_contexts in TRANSITIONS.items():
        fields = transition_blocks.get(name)
        if fields is None:
            continue
        if set(fields) != TRANSITION_FIELDS:
            missing = sorted(TRANSITION_FIELDS - set(fields))
            extra = sorted(set(fields) - TRANSITION_FIELDS)
            errors.append(
                f"context-map {name} fields mismatch: missing={missing}, extra={extra}"
            )
            continue
        if any(not value for value in fields.values()):
            errors.append(f"context-map {name} contains an empty required field")
        if (fields["源上下文"], fields["目标上下文"]) != expected_contexts:
            errors.append(
                f"context-map {name} context direction mismatch: "
                f"{fields['源上下文']} -> {fields['目标上下文']}"
            )
        relation = fields["权威关系"]
        relation_clause = relation.split("；", 1)[0]
        relation_sides = relation_clause.split("→")
        if (
            len(relation_sides) != 2
            or not all(
                tokens
                and all(token in FACT_CLASSES for token in tokens)
                for tokens in (
                    [token.strip() for token in side.split("+") if token.strip()]
                    for side in relation_sides
                )
            )
        ):
            errors.append(f"context-map {name} has invalid authority relation")
        direct_sources = MD_POINTER_RE.findall(fields["直接真源"])
        if not 1 <= len(direct_sources) <= 3:
            errors.append(
                f"context-map {name} direct source count={len(direct_sources)}, expected 1..3"
            )
        elif any(not _validate_source(root, source) for source in direct_sources):
            errors.append(f"context-map {name} has invalid direct source")
        failure = fields["失效条件"]
        repair_sources = MD_POINTER_RE.findall(failure.split("修复：", 1)[-1])
        if "修复：" not in failure or len(repair_sources) != 1:
            errors.append(f"context-map {name} must name exactly one repair source")
        elif repair_sources[0] not in direct_sources:
            errors.append(
                f"context-map {name} repair source must also be a direct source"
            )
        for label, value in fields.items():
            if len(value) > 360:
                errors.append(
                    f"context-map {name}.{label} length={len(value)} exceeds 360"
                )

    if "禁止递归追随引用" not in context_map or "首批最多 3 份" not in context_map:
        errors.append("context-map is missing progressive-loading guards")
    for forbidden in ("允许递归", "默认整目录读取", "| Evidence ID | AC | 强度 |"):
        if forbidden in context_map:
            errors.append(f"context-map contains forbidden pattern: {forbidden}")

    for relative in DUPLICATE_CANDIDATES:
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if relative != "Coder/README.md" and "| 上下文 | 目的 | 语义所有权 |" in text:
            errors.append(f"duplicate context table outside L1: {relative}")
        if "| 概念 | 上下文限定 | 白话定义 |" in text:
            errors.append(f"duplicate glossary table outside L2: {relative}")
        if "### PRD→AC" in text or "- 源上下文：" in text:
            errors.append(f"duplicate context-map block outside context-map: {relative}")

    metrics = {
        "l0_bytes": l0_metrics["bytes"],
        "l0_nonempty_lines": l0_metrics["nonempty_lines"],
        "l0_pointers": l0_metrics["pointers"],
        "l1_bytes": l1_metrics["bytes"],
        "l1_lines": l1_metrics["lines"],
        "l1_pointers": l1_metrics["pointers"],
        "contexts": len(context_rows),
        "terms": len(glossary_rows),
        "routes": len(route_rows),
        "fact_classes": len(fact_rows),
        "transitions": len(transition_blocks),
        "context_map_bytes": map_metrics["bytes"],
        "context_map_lines": map_metrics["lines"],
        "context_map_pointers": map_metrics["pointers"],
    }
    return CheckResult(metrics=metrics, errors=errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("--project-root", required=True)
    args = parser.parse_args()

    try:
        result = check_project(Path(args.project_root))
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2

    payload = {
        "status": "ok" if result.ok else "failed",
        "metrics": result.metrics,
        "errors": result.errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
