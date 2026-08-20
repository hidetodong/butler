#!/usr/bin/env python3
"""从机器源头生成项目全貌产物 `.ai/OVERVIEW.md`。

这份产物只装**可从机器源头派生的事实**，全文由本脚本写，人不许手改。机器算不出来的
东西有另外两个落点：长期决策与理由进 `.ai/invariants.md`（纯手写、纯追加），会过期的
判断进 `.ai/debt.md`（还掉即删）。三份各守一种性质，不混装——`.ai/project/frontier.md`
就是死于「可派生事实 + 会过期判断」塞在同一节，人一次只改一半，两半都没改。

`--check` 逐节比对而不是整文件比对：诊断必须指名是哪一节对不上，笼统说「文件有差异」
在真出问题时没法定位。页首不写生成时间戳——写了每次重跑都产生 diff，`--check` 会永远红。

顺带守一条 `.ai/invariants.md` 的棘轮：无真源指针的条目数不得超过历史基线。那批条目
复述了机制的具体形状却没给可核对的真源，是最容易悄悄变假的一类。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

OVERVIEW_RELATIVE = ".ai/OVERVIEW.md"
OVERVIEW_MAX_BYTES = 12000

# `.ai/invariants.md` 里允许不带真源指针的历史条目数。这是欠账不是额度，见 `.ai/debt.md`。
INVARIANT_POINTER_EXEMPT = 16
INVARIANT_RELATIVE = ".ai/invariants.md"

SECTION_VERSION = "版本与当前状态"
SECTION_MILESTONES = "里程碑时间线"
SECTION_RULES = "规则体系目录与职责"
SECTION_WORKFLOWS = "工作流清单"
SECTION_TOOLS = "驻留工具清单"

SOURCE_LABELS = (
    "`VERSION`",
    "`.ai/ITERATIONS.md`",
    "`.ai/MILESTONES.md`",
    "`Coder/README.md`",
    "`workflows/registry.json`",
    "`tools/`",
)

POINTER_RE = re.compile(r"`[^`]*[/.][^`]*`")
ENTRY_RE = re.compile(r"^- \*\*(.+?)\*\*", re.MULTILINE)


class OverviewError(RuntimeError):
    """源头缺失、无法解析或超出上限——一律不产出残缺页。"""


def read_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise OverviewError(f"missing source: {relative}")
    return path.read_text(encoding="utf-8")


def ledger_current(text: str, relative: str) -> str:
    match = re.search(r"^current:\s*(\S+)\s*$", text, re.MULTILINE)
    if not match:
        raise OverviewError(f"missing source: {relative} has no current line")
    return match.group(1)


def ledger_rows(text: str, relative: str) -> list[list[str]]:
    rows = []
    for line in text.split("\n"):
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"(ITER|MILE)-\d{4,}", cells[0]):
            rows.append(cells)
    if not rows:
        raise OverviewError(f"missing source: {relative} has no ledger rows")
    return rows


def section_version(root: Path, butler: Path) -> tuple[str, str]:
    version = read_text(butler, "VERSION").strip()
    iterations = read_text(root, ".ai/ITERATIONS.md")
    milestones = read_text(root, ".ai/MILESTONES.md")
    iter_current = ledger_current(iterations, ".ai/ITERATIONS.md")
    mile_current = ledger_current(milestones, ".ai/MILESTONES.md")
    iter_rows = ledger_rows(iterations, ".ai/ITERATIONS.md")
    mile_rows = ledger_rows(milestones, ".ai/MILESTONES.md")
    index = json.loads(read_text(root, ".ai/state-index.json"))
    ledgers = index.get("ledgers", {})
    iter_total = ledgers.get("iterations", {}).get("row_count", len(iter_rows))
    mile_total = ledgers.get("milestones", {}).get("row_count", len(mile_rows))
    body = "\n".join((
        f"- 规则源版本：**{version}**",
        f"- 当前 active 里程碑：{mile_current}",
        f"- 当前 active 迭代：{iter_current}",
        f"- 累计里程碑 {mile_total} 个、迭代 {iter_total} 个"
        f"（台账热表各留 {len(mile_rows)} / {len(iter_rows)} 行，其余在 `.ai/history/` 冷分片）",
    ))
    return SECTION_VERSION, body


def section_milestones(root: Path, butler: Path) -> tuple[str, str]:
    rows = ledger_rows(read_text(root, ".ai/MILESTONES.md"), ".ai/MILESTONES.md")
    lines = ["| 里程碑 | 标题 | 状态 | 起 | 止 | 含迭代 |", "|---|---|---|---|---|---|"]
    for cells in rows:
        number, title, status, opened, closed = cells[0], cells[1], cells[2], cells[3], cells[4]
        included = cells[5] if len(cells) > 5 else ""
        count = len([x for x in included.split(",") if x.strip()])
        lines.append(f"| {number} | {title} | {status} | {opened} | {closed} | {count} |")
    return SECTION_MILESTONES, "\n".join(lines)


def section_rules(root: Path, butler: Path) -> tuple[str, str]:
    readme = read_text(butler, "Coder/README.md")
    if "规则目录说明：" not in readme:
        raise OverviewError("missing source: Coder/README.md has no 规则目录说明 section")
    block = readme.split("规则目录说明：", 1)[1].split("\n## ", 1)[0]
    described = {}
    for match in re.finditer(r"^- `([0-9]{2}_[A-Za-z_]+)/`：(.+)$", block, re.MULTILINE):
        described[match.group(1)] = match.group(2).strip()
    root_dir = butler / "Coder"
    if not root_dir.is_dir():
        raise OverviewError("missing source: Coder/")
    directories = sorted(p.name for p in root_dir.iterdir() if p.is_dir())
    lines = ["| 目录 | 规则文件数 | 职责 |", "|---|---|---|"]
    for name in directories:
        if name not in described:
            raise OverviewError(f"directory has no description in Coder/README.md: {name}")
        count = len(list((root_dir / name).glob("*.md")))
        lines.append(f"| `{name}/` | {count} | {described[name]} |")
    return SECTION_RULES, "\n".join(lines)


def section_workflows(root: Path, butler: Path) -> tuple[str, str]:
    data = json.loads(read_text(butler, "workflows/registry.json"))
    router = data.get("router") or {}
    workflows = data.get("workflows") or []
    if not workflows:
        raise OverviewError("missing source: workflows/registry.json has no workflows")
    lines = [
        f"- 语义入口 Router：`{router.get('claude', {}).get('name', '—')}`"
        f" / `{router.get('codex', {}).get('name', '—')}`，不路由到自身。",
        "",
        "| ID | Claude | Codex | 风险 | 规则真源 |",
        "|---|---|---|---|---|",
    ]
    for item in workflows:
        lines.append(
            f"| {item['id']} | `{item.get('claude', {}).get('name', '—')}` |"
            f" `{item.get('codex', {}).get('name', '—')}` | {item.get('risk', '—')} |"
            f" `{item.get('rule_source', '—')}` |"
        )
    return SECTION_WORKFLOWS, "\n".join(lines)


def tool_summary(directory: Path) -> str:
    readme = directory / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").split("\n"):
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return "—"


def section_tools(root: Path, butler: Path) -> tuple[str, str]:
    tools_dir = butler / "tools"
    if not tools_dir.is_dir():
        raise OverviewError("missing source: tools/")
    directories = sorted(p for p in tools_dir.iterdir() if p.is_dir())
    if not directories:
        raise OverviewError("missing source: tools/ has no tool directories")
    lines = ["| 工具 | 用途 |", "|---|---|"]
    for item in directories:
        lines.append(f"| `tools/{item.name}/` | {tool_summary(item)} |")
    return SECTION_TOOLS, "\n".join(lines)


SECTIONS = (section_version, section_milestones, section_rules, section_workflows, section_tools)


def render(root: Path, butler: Path) -> tuple[str, list[tuple[str, str]]]:
    sections = [builder(root, butler) for builder in SECTIONS]
    header = "\n".join((
        "# 项目全貌（生成物）",
        "",
        f"> 本页由 {'、'.join(SOURCE_LABELS)} 通过 `python3 scripts/sync-project-overview.py --write` 生成，请勿手改。",
        "> 只装可从机器源头派生的事实；长期决策与理由见 `.ai/invariants.md`，会过期的判断见 `.ai/debt.md`。",
        "",
        "",
    ))
    body = "\n\n".join(f"## {title}\n\n{content}" for title, content in sections)
    return header + body + "\n", sections


def split_sections(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    result = []
    for index in range(1, len(parts), 2):
        result.append((parts[index].strip(), parts[index + 1].strip()))
    return result


def invariant_pointer_errors(root: Path) -> list[str]:
    path = root / INVARIANT_RELATIVE
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    missing = []
    for line in text.split("\n"):
        if not line.startswith("- **"):
            continue
        if POINTER_RE.search(line):
            continue
        match = ENTRY_RE.match(line)
        missing.append(match.group(1) if match else line[:40])
    if len(missing) <= INVARIANT_POINTER_EXEMPT:
        return []
    return [
        f"invariants without source pointer: {len(missing)} > {INVARIANT_POINTER_EXEMPT}"
        f" (超出基线的条目请自查以下全部无指针条目: {'; '.join(missing)})"
    ]


def check(root: Path, butler: Path) -> list[str]:
    expected, sections = render(root, butler)
    errors: list[str] = []
    encoded = expected.encode("utf-8")
    if len(encoded) > OVERVIEW_MAX_BYTES:
        errors.append(f"overview too large: {len(encoded)} > {OVERVIEW_MAX_BYTES}")
    path = root / OVERVIEW_RELATIVE
    if not path.is_file():
        errors.append(f"overview missing: {OVERVIEW_RELATIVE}")
        return errors + invariant_pointer_errors(root)
    actual_text = path.read_text(encoding="utf-8")
    actual = split_sections(actual_text)
    expected_titles = [title for title, _ in sections]
    actual_titles = [title for title, _ in actual]
    if expected_titles != actual_titles:
        errors.append(
            f"overview section set mismatch: expected={expected_titles} actual={actual_titles}"
        )
    else:
        for (title, content), (_, disk) in zip(sections, actual):
            if hashlib.sha256(content.strip().encode()).hexdigest() != hashlib.sha256(disk.encode()).hexdigest():
                errors.append(f"overview section drift: {title}")
        if not errors and actual_text != expected:
            errors.append("overview header drift: 页首说明与生成结果不一致")
    return errors + invariant_pointer_errors(root)


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.chmod(temp, 0o644)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--butler-root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.project_root.expanduser().resolve()
    butler = (args.butler_root or args.project_root).expanduser().resolve()
    try:
        if args.check:
            errors = check(root, butler)
            for item in errors:
                print(f"[DRIFT] {item}", file=sys.stderr)
            if errors:
                return 1
            print(json.dumps({"status": "ok", "overview": OVERVIEW_RELATIVE}, ensure_ascii=False))
            return 0
        content, _ = render(root, butler)
        encoded = content.encode("utf-8")
        if len(encoded) > OVERVIEW_MAX_BYTES:
            raise OverviewError(f"overview too large: {len(encoded)} > {OVERVIEW_MAX_BYTES}")
        atomic_write(root / OVERVIEW_RELATIVE, encoded)
        print(json.dumps(
            {"status": "written", "overview": OVERVIEW_RELATIVE, "bytes": len(encoded)},
            ensure_ascii=False,
        ))
        return 0
    except OverviewError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
