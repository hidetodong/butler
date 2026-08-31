#!/usr/bin/env python3
"""三层录入契约的唯一写盘者。

数据形态的真源是 `Coder/40_Context_Management/intake-schema.md`；动作边界的真源是
`Coder/40_Context_Management/intake-workflow.md`。本文件只负责校验与落盘，不做语义判断：
「这条闪念该孵化还是该丢」由命令层问过用户之后，以已经定好的目标态传进来。
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import tempfile

INBOX_REL = ".ai/INBOX.md"
MILESTONES_REL = ".ai/MILESTONES.md"
ITERATIONS_REL = ".ai/ITERATIONS.md"
MILESTONE_REL = ".ai/MILESTONE.md"
BACKLOG_REL = ".ai/milestone-backlog"

INBOX_HEADER = "| 闪念键 | 记于 | 一句话 | 状态 | 去向 |"
INBOX_SEP = "|---|---|---|---|---|"
INBOX_SCAFFOLD = f"""# INBOX — 闪念口

> 结构、状态与转移的真源是 `Coder/40_Context_Management/intake-schema.md §1`。
> 本文件由 `tools/intake/intake.py` 写入，不手工编辑。

## 闪念

{INBOX_HEADER}
{INBOX_SEP}
"""

STATES = ("new", "incubated", "done", "dropped")
# intake-schema.md §1.5 穷举的四条转移，终态不回头。
TRANSITIONS = {
    ("new", "incubated"),
    ("new", "done"),
    ("new", "dropped"),
    ("incubated", "dropped"),
}
SCALES = ("milestone", "iteration", "undecided")
EXITS = ("promote", "iterate", "withdraw")

PLACEHOLDER_MARK = "<!-- TODO(intake):"
PLACEHOLDER = PLACEHOLDER_MARK + " 这一段还没填，填完删掉本行 -->"

# intake-schema.md §2.3 的按档段落。
SECTIONS = {
    "milestone": ["范围评估", "理解阐释", "拆分路线图", "范围演进记录"],
    "iteration": ["要解决什么", "暂缓原因"],
    "undecided": ["想做什么", "卡在哪"],
}
# 提升为里程碑时，四段按 milestone-schema.md §5 重新编号。
MILESTONE_SECTION_NUMBERS = {
    "范围评估": "5.1",
    "理解阐释": "5.2",
    "拆分路线图": "5.3",
    "范围演进记录": "5.4",
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DASH = "—"


class IntakeError(Exception):
    """契约校验不过或写盘失败；抛出时整次不落盘。"""


# ---------------------------------------------------------------------------
# 落盘原语：单个文件的写是原子的，跨文件靠「先算后写 + 失败即回滚」。
# ---------------------------------------------------------------------------
def _write_file(path: pathlib.Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".intake-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _remove_file(path: pathlib.Path) -> None:
    path.unlink()


def apply_plan(plan):
    """按序执行写盘计划；任一步失败就把已经动过的按逆序还原。

    plan 的每一项是 (路径, 新字节或 None 表示删除, 原字节或 None 表示原本不存在)。
    这不是数据库那种事务：回滚本身也可能失败（磁盘满、权限变化），那时仍会留下半截态。
    """
    applied = []
    try:
        for path, new, _old in plan:
            if new is None:
                _remove_file(path)
            else:
                _write_file(path, new)
            applied.append((path, new, _old))
    except BaseException as exc:
        for path, _new, old in reversed(applied):
            try:
                if old is None:
                    if path.exists():
                        _remove_file(path)
                else:
                    _write_file(path, old)
            except BaseException:
                pass
        raise IntakeError(f"写盘失败，已尝试回滚：{exc}") from exc


def read_bytes(path: pathlib.Path):
    return path.read_bytes() if path.exists() else None


def as_plan_entry(path: pathlib.Path, text):
    """text 为 None 表示删除。"""
    new = None if text is None else text.encode("utf-8")
    return (path, new, read_bytes(path))


# ---------------------------------------------------------------------------
# Markdown 表格的读写
# ---------------------------------------------------------------------------
def split_row(line: str):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def join_row(cells) -> str:
    return "| " + " | ".join(cells) + " |"


def table_bounds(lines, start=0, stop=None):
    """返回 [start, stop) 区间里第一张表的 (表头行号, 末行行号)；没有表返回 None。"""
    stop = len(lines) if stop is None else stop
    idx = [i for i in range(start, stop) if lines[i].strip().startswith("|")]
    if len(idx) < 2:
        return None
    head = idx[0]
    last = head
    for i in idx:
        if i == last or i == last + 1:
            last = i
    return head, last


def check_cell(value: str, field: str) -> str:
    value = value.strip()
    if not value:
        raise IntakeError(f"{field} 不能为空")
    if "|" in value or "\n" in value or "\r" in value:
        raise IntakeError(f"{field} 不得包含竖线或换行，否则会撑坏表格：{value!r}")
    return value


def check_slug(value: str, field: str = "slug") -> str:
    value = value.strip()
    if not SLUG_RE.match(value):
        raise IntakeError(f"{field} 只能是小写字母、数字与连字符（kebab）：{value!r}")
    return value


def derive_slug(text: str) -> str:
    return "-".join(re.findall(r"[a-z0-9]+", text.lower()))


def today(date: str | None) -> str:
    if date is None:
        return datetime.date.today().isoformat()
    if not DATE_RE.match(date):
        raise IntakeError(f"--date 必须是 YYYY-MM-DD：{date!r}")
    return date


# ---------------------------------------------------------------------------
# 第一层 · 闪念口
# ---------------------------------------------------------------------------
class Inbox:
    def __init__(self, path: pathlib.Path):
        self.path = path
        if path.exists():
            self.lines = path.read_text(encoding="utf-8").splitlines()
        else:
            self.lines = INBOX_SCAFFOLD.splitlines()
        bounds = table_bounds(self.lines)
        if bounds is None:
            raise IntakeError(f"{path} 里找不到闪念表；结构见 intake-schema.md §1")
        self.head, self.last = bounds
        if self.lines[self.head].strip() != INBOX_HEADER:
            raise IntakeError(f"{path} 的表头必须逐字是 {INBOX_HEADER}")

    def rows(self):
        return [(i, split_row(self.lines[i])) for i in range(self.head + 2, self.last + 1)]

    def find(self, key: str):
        for i, cells in self.rows():
            if cells[0] == key:
                return i, cells
        return None, None

    def keys(self):
        return {cells[0] for _i, cells in self.rows()}

    def append(self, cells):
        self.lines.insert(self.last + 1, join_row(cells))
        self.last += 1

    def replace(self, index: int, cells):
        self.lines[index] = join_row(cells)

    def find_by_target(self, target: str):
        for i, cells in self.rows():
            if len(cells) >= 5 and cells[4] == target:
                return i, cells
        return None, None

    def text(self) -> str:
        return "\n".join(self.lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# 第二层 · 孵化区（索引在 MILESTONES.md 待办区，草稿在 milestone-backlog/）
# ---------------------------------------------------------------------------
class Milestones:
    def __init__(self, path: pathlib.Path):
        if not path.exists():
            raise IntakeError(f"缺少 {path}")
        self.path = path
        self.lines = path.read_text(encoding="utf-8").splitlines()
        marks = [i for i, l in enumerate(self.lines) if l.startswith("## 待办区")]
        if not marks:
            raise IntakeError(f"{path} 里找不到「## 待办区」小节")
        self.backlog_head_line = marks[0]
        formal = table_bounds(self.lines, 0, self.backlog_head_line)
        if formal is None:
            raise IntakeError(f"{path} 里找不到正式里程碑表")
        self.formal_head, self.formal_last = formal
        backlog = table_bounds(self.lines, self.backlog_head_line)
        if backlog is None:
            raise IntakeError(f"{path} 的待办区里找不到索引表")
        self.backlog_head, self.backlog_last = backlog

    # -- current 指针 --
    def current_index(self):
        for i, line in enumerate(self.lines):
            if line.startswith("current:"):
                return i
        raise IntakeError(f"{self.path} 里找不到 current: 行")

    def current(self) -> str:
        return self.lines[self.current_index()].split(":", 1)[1].strip()

    def set_current(self, value: str) -> None:
        self.lines[self.current_index()] = f"current: {value}"

    # -- 待办区 --
    def backlog_rows(self):
        return [
            (i, split_row(self.lines[i]))
            for i in range(self.backlog_head + 2, self.backlog_last + 1)
        ]

    def find_backlog(self, key: str):
        for i, cells in self.backlog_rows():
            if cells[0] == key:
                return i, cells
        return None, None

    def append_backlog(self, cells):
        self.lines.insert(self.backlog_last + 1, join_row(cells))
        self.backlog_last += 1

    def drop_backlog(self, index: int):
        del self.lines[index]
        self.backlog_last -= 1

    # -- 正式表 --
    def formal_rows(self):
        return [
            (i, split_row(self.lines[i]))
            for i in range(self.formal_head + 2, self.formal_last + 1)
        ]

    def next_milestone_id(self) -> str:
        used = [
            int(m.group(1))
            for _i, cells in self.formal_rows()
            for m in [re.match(r"MILE-(\d+)$", cells[0])]
            if m
        ]
        return f"MILE-{max(used, default=0) + 1:04d}"

    def insert_formal(self, cells):
        self.lines.insert(self.formal_head + 2, join_row(cells))
        self.formal_last += 1
        self.backlog_head_line += 1
        self.backlog_head += 1
        self.backlog_last += 1

    def text(self) -> str:
        return "\n".join(self.lines).rstrip("\n") + "\n"


class Iterations:
    def __init__(self, path: pathlib.Path):
        if not path.exists():
            raise IntakeError(f"缺少 {path}")
        self.path = path
        self.lines = path.read_text(encoding="utf-8").splitlines()
        bounds = table_bounds(self.lines)
        if bounds is None:
            raise IntakeError(f"{path} 里找不到迭代表")
        self.head, self.last = bounds

    def current_index(self):
        for i, line in enumerate(self.lines):
            if line.startswith("current:"):
                return i
        raise IntakeError(f"{self.path} 里找不到 current: 行")

    def current(self) -> str:
        return self.lines[self.current_index()].split(":", 1)[1].strip()

    def set_current(self, value: str) -> None:
        self.lines[self.current_index()] = f"current: {value}"

    def next_iteration_id(self) -> str:
        used = []
        for i in range(self.head + 2, self.last + 1):
            m = re.match(r"ITER-(\d+)$", split_row(self.lines[i])[0])
            if m:
                used.append(int(m.group(1)))
        return f"ITER-{max(used, default=0) + 1:04d}"

    def insert_row(self, cells):
        self.lines.insert(self.head + 2, join_row(cells))
        self.last += 1

    def text(self) -> str:
        return "\n".join(self.lines).rstrip("\n") + "\n"


def draft_path(root: pathlib.Path, key: str) -> pathlib.Path:
    return root / BACKLOG_REL / f"{key}.md"


def render_draft(*, key: str, title: str, scale: str) -> str:
    body = [f"# {title}", "", f"候办键: {key}", "候办状态: deferred", f"规模: {scale}", ""]
    for section in SECTIONS[scale]:
        body += [f"## {section}", "", PLACEHOLDER, ""]
    return "\n".join(body).rstrip("\n") + "\n"


def read_draft_scale(path: pathlib.Path):
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("规模:"):
            return line.split(":", 1)[1].strip()
    return None


def read_draft_state(path: pathlib.Path):
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("候办状态:"):
            return line.split(":", 1)[1].strip()
    return None


# ---------------------------------------------------------------------------
# 三个子命令
# ---------------------------------------------------------------------------
def cmd_add(root: pathlib.Path, args) -> dict:
    text = check_cell(args.text, "--text")
    date = today(args.date)
    slug = check_slug(args.slug, "--slug") if args.slug else derive_slug(text)
    if not slug:
        raise IntakeError(
            "从 --text 推不出 kebab 形态的闪念键（正文里没有 ASCII 字母或数字），"
            "请显式给 --slug"
        )
    slug = check_slug(slug, "闪念键 slug")

    inbox = Inbox(root / INBOX_REL)
    used = inbox.keys()
    key = f"{date}-{slug}"
    n = 1
    while key in used:
        n += 1
        key = f"{date}-{slug}-{n}"

    inbox.append([key, date, text, "new", DASH])
    apply_plan([as_plan_entry(root / INBOX_REL, inbox.text())])
    return {"key": key, "state": "new", "written": [INBOX_REL]}


def cmd_list(root: pathlib.Path, args) -> dict:
    layer = args.layer or "all"
    if layer not in ("inbox", "backlog", "all"):
        raise IntakeError(f"--layer 只能是 inbox / backlog / all：{layer!r}")
    if args.state and args.state not in STATES:
        raise IntakeError(f"--state 只能是 {' / '.join(STATES)}：{args.state!r}")
    if args.scale and args.scale not in SCALES:
        raise IntakeError(f"--scale 只能是 {' / '.join(SCALES)}：{args.scale!r}")

    inbox_entries = []
    if layer in ("inbox", "all") and (root / INBOX_REL).exists():
        for _i, cells in Inbox(root / INBOX_REL).rows():
            inbox_entries.append(
                {
                    "key": cells[0],
                    "date": cells[1],
                    "text": cells[2],
                    "state": cells[3],
                    "target": cells[4] if len(cells) > 4 else DASH,
                    "scale": None,
                }
            )

    backlog_entries = []
    if layer in ("backlog", "all"):
        milestones = Milestones(root / MILESTONES_REL)
        for _i, cells in milestones.backlog_rows():
            path = root / cells[3] if len(cells) > 3 and cells[3] != DASH else draft_path(root, cells[0])
            exists = path.exists()
            raw = path.read_text(encoding="utf-8") if exists else ""
            backlog_entries.append(
                {
                    "key": cells[0],
                    "title": cells[1] if len(cells) > 1 else "",
                    "deferred": cells[2] if len(cells) > 2 else "",
                    "draft": str(path.relative_to(root)) if exists else (cells[3] if len(cells) > 3 else ""),
                    "reason": cells[4] if len(cells) > 4 else "",
                    "state": read_draft_state(path) or "deferred",
                    "scale": read_draft_scale(path),
                    "missing": not exists,
                    "incomplete": PLACEHOLDER_MARK in raw,
                }
            )

    def keep(entry):
        if args.state and entry.get("state") != args.state:
            return False
        if args.scale and entry.get("scale") != args.scale:
            return False
        return True

    return {
        "inbox": [e for e in inbox_entries if keep(e)],
        "backlog": [e for e in backlog_entries if keep(e)],
    }


def _handle_inbox(root: pathlib.Path, args) -> dict:
    target = args.to
    if target not in STATES:
        raise IntakeError(f"--to 只能是 {' / '.join(STATES)}：{target!r}")

    inbox = Inbox(root / INBOX_REL)
    index, cells = inbox.find(args.inbox)
    if index is None:
        raise IntakeError(f"闪念口里没有这一条：{args.inbox}")
    state = cells[3]
    if state not in STATES:
        raise IntakeError(f"{args.inbox} 当前状态不在四态之内：{state!r}")
    if state == "incubated" and target == "dropped":
        raise IntakeError(
            "孵化过的条目不能只回写闪念行，那会留下一份没人认领的草稿。"
            "请走 `handle --backlog <候办键> --exit withdraw`，两侧一起撤。"
        )
    if (state, target) not in TRANSITIONS:
        raise IntakeError(
            f"{state} → {target} 不在 intake-schema.md §1.5 穷举的四条转移里，拒绝执行"
        )

    date = today(args.date)
    if target != "incubated":
        note = check_cell(args.note or "", f"--note（转 {target} 时必填）")
        inbox.replace(index, [cells[0], cells[1], cells[2], target, note])
        apply_plan([as_plan_entry(root / INBOX_REL, inbox.text())])
        return {"key": args.inbox, "state": target, "written": [INBOX_REL]}

    for name, value in (("--slug", args.slug), ("--scale", args.scale),
                        ("--title", args.title), ("--reason", args.reason)):
        if not value:
            raise IntakeError(f"转 incubated 时 {name} 必填")
    backlog_key = check_slug(args.slug, "候办键")
    scale = args.scale
    if scale not in SCALES:
        raise IntakeError(f"--scale 只能是 {' / '.join(SCALES)}：{scale!r}")
    title = check_cell(args.title, "--title")
    reason = check_cell(args.reason, "--reason")

    milestones = Milestones(root / MILESTONES_REL)
    if milestones.find_backlog(backlog_key)[0] is not None:
        raise IntakeError(f"待办区已经有 {backlog_key} 这一行，一方向一文件，换个键")
    target_path = draft_path(root, backlog_key)
    if target_path.exists():
        raise IntakeError(f"草稿 {target_path} 已存在，不覆盖")

    rel_draft = f"{BACKLOG_REL}/{backlog_key}.md"
    inbox.replace(index, [cells[0], cells[1], cells[2], "incubated", rel_draft])
    milestones.append_backlog([backlog_key, title, date, rel_draft, reason])

    plan = [
        as_plan_entry(root / INBOX_REL, inbox.text()),
        as_plan_entry(target_path, render_draft(key=backlog_key, title=title, scale=scale)),
        as_plan_entry(root / MILESTONES_REL, milestones.text()),
    ]
    apply_plan(plan)
    return {
        "key": args.inbox,
        "state": "incubated",
        "backlog_key": backlog_key,
        "draft": rel_draft,
        "scale": scale,
        "written": [INBOX_REL, rel_draft, MILESTONES_REL],
    }


def _promote(root, args, milestones, row_index, cells, path, scale, date):
    if scale != "milestone":
        raise IntakeError(f"提升为里程碑只接受 milestone 档，这份是 {scale!r}；先改档或改走别的出口")
    cur = milestones.current()
    if cur != "none":
        raise IntakeError(
            f"里程碑台账的 current 是 {cur}，单 active 约束下不能再提升一个；先收口它"
        )
    mile_id = milestones.next_milestone_id()
    title = cells[1]

    body_lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            continue
        if line.startswith(("候办键:", "候办状态:", "规模:")):
            continue
        if line.startswith("## "):
            name = line[3:].strip()
            number = MILESTONE_SECTION_NUMBERS.get(name)
            line = f"## {number} {name}" if number else line
        body_lines.append(line)
    body = "\n".join(body_lines).strip("\n")
    milestone_md = f"# {mile_id} — {title}\n\n{body}\n"

    milestones.drop_backlog(row_index)
    milestones.insert_formal([mile_id, title, "active", date, DASH, DASH, DASH])
    milestones.set_current(mile_id)

    plan = [
        as_plan_entry(root / MILESTONE_REL, milestone_md),
        as_plan_entry(root / MILESTONES_REL, milestones.text()),
        (path, None, read_bytes(path)),
    ]
    apply_plan(plan)
    return {
        "exit": "promote",
        "id": mile_id,
        "title": title,
        "written": [MILESTONE_REL, MILESTONES_REL],
        "removed": [str(path.relative_to(root))],
        "next_step": "按 milestone-schema.md §5 把四段内容补实，再开第一个迭代",
    }


def _iterate(root, args, milestones, row_index, cells, path, scale, date):
    if scale != "iteration":
        raise IntakeError(f"开为迭代只接受 iteration 档，这份是 {scale!r}；先改档或改走别的出口")
    iterations = Iterations(root / ITERATIONS_REL)
    cur = iterations.current()
    if cur != "none":
        raise IntakeError(f"迭代台账的 current 是 {cur}，先收口它再开新的")
    iter_id = iterations.next_iteration_id()
    title = cells[1]
    owner = milestones.current()
    owner = DASH if owner == "none" else owner

    iterations.insert_row([iter_id, title, "active", date, DASH, owner, DASH])
    iterations.set_current(iter_id)
    milestones.drop_backlog(row_index)

    plan = [
        as_plan_entry(root / ITERATIONS_REL, iterations.text()),
        as_plan_entry(root / MILESTONES_REL, milestones.text()),
        (path, None, read_bytes(path)),
    ]
    apply_plan(plan)
    return {
        "exit": "iterate",
        "id": iter_id,
        "title": title,
        "written": [ITERATIONS_REL, MILESTONES_REL],
        "removed": [str(path.relative_to(root))],
        "next_step": "按 iteration-schema.md §5.1 覆盖式重写四件套，从 P1 的 .ai/CONCEPT.md 开始",
    }


def _append_scope_log(text: str, line: str) -> str | None:
    lines = text.splitlines()
    head = None
    for i, l in enumerate(lines):
        if l.startswith("## ") and "范围演进记录" in l:
            head = i
            break
    if head is None:
        return None
    stop = len(lines)
    for i in range(head + 1, len(lines)):
        if lines[i].startswith("## "):
            stop = i
            break
    while stop > head + 1 and not lines[stop - 1].strip():
        stop -= 1
    lines.insert(stop, line)
    return "\n".join(lines).rstrip("\n") + "\n"


def _withdraw(root, args, milestones, row_index, cells, path, scale, date):
    reason = check_cell(args.reason or "", "--reason（撤回时必填）")
    rel_draft = cells[3] if len(cells) > 3 else str(path.relative_to(root))
    milestones.drop_backlog(row_index)

    plan = [as_plan_entry(root / MILESTONES_REL, milestones.text())]
    written = [MILESTONES_REL]
    notes = []

    milestone_md = root / MILESTONE_REL
    if milestone_md.exists():
        updated = _append_scope_log(
            milestone_md.read_text(encoding="utf-8"),
            f"- {date}（撤回候办 {cells[0]}）：{reason}",
        )
        if updated is None:
            notes.append(f"{MILESTONE_REL} 里没有「范围演进记录」小节，撤回原因未登记")
        else:
            plan.append(as_plan_entry(milestone_md, updated))
            written.append(MILESTONE_REL)
    else:
        notes.append(f"{MILESTONE_REL} 不存在，撤回原因未登记")

    inbox_path = root / INBOX_REL
    linked = None
    if inbox_path.exists():
        inbox = Inbox(inbox_path)
        idx, row = inbox.find_by_target(rel_draft)
        if idx is not None:
            linked = row[0]
            inbox.replace(idx, [row[0], row[1], row[2], "dropped", reason])
            plan.append(as_plan_entry(inbox_path, inbox.text()))
            written.append(INBOX_REL)
        else:
            notes.append("闪念口里没有指向这份草稿的行，跳过回写")

    if path.exists():
        plan.append((path, None, read_bytes(path)))

    apply_plan(plan)
    return {
        "exit": "withdraw",
        "key": cells[0],
        "linked_inbox_key": linked,
        "written": written,
        "removed": [rel_draft],
        "notes": notes,
    }


def _handle_backlog(root: pathlib.Path, args) -> dict:
    exit_name = args.exit
    if exit_name not in EXITS:
        raise IntakeError(f"--exit 只能是 {' / '.join(EXITS)}：{exit_name!r}")
    milestones = Milestones(root / MILESTONES_REL)
    row_index, cells = milestones.find_backlog(args.backlog)
    if row_index is None:
        raise IntakeError(f"待办区里没有这一条：{args.backlog}")
    path = root / cells[3] if len(cells) > 3 and cells[3] != DASH else draft_path(root, cells[0])
    if not path.exists() and exit_name != "withdraw":
        raise IntakeError(f"索引指向的草稿不存在：{cells[3] if len(cells) > 3 else path}")
    scale = read_draft_scale(path)
    if scale is None and exit_name != "withdraw":
        raise IntakeError(f"{path} 顶部没有「规模:」行，按 intake-schema.md §2.2 补上再分流")
    date = today(args.date)
    fn = {"promote": _promote, "iterate": _iterate, "withdraw": _withdraw}[exit_name]
    return fn(root, args, milestones, row_index, cells, path, scale, date)


def cmd_handle(root: pathlib.Path, args) -> dict:
    if bool(args.inbox) == bool(args.backlog):
        raise IntakeError("--inbox 与 --backlog 必须给且只能给一个，工具不猜你说的是哪一层")
    if args.inbox:
        if not args.to:
            raise IntakeError("--inbox 必须配 --to")
        return _handle_inbox(root, args)
    if not args.exit:
        raise IntakeError("--backlog 必须配 --exit")
    return _handle_backlog(root, args)


# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intake.py",
        description="三层录入契约（闪念口 / 孵化区 / 执行分流）的唯一写盘者",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--project-root", required=True)
        p.add_argument("--date", default=None, help="YYYY-MM-DD；省略时取当天")

    p_add = sub.add_parser("add", help="记一条闪念")
    common(p_add)
    p_add.add_argument("--text", required=True, help="一句话")
    p_add.add_argument("--slug", default=None, help="闪念键的 kebab 部分；省略时从 --text 推")

    p_list = sub.add_parser("list", help="只读地列出两层条目")
    common(p_list)
    p_list.add_argument("--layer", default="all")
    p_list.add_argument("--state", default=None)
    p_list.add_argument("--scale", default=None)

    p_handle = sub.add_parser("handle", help="执行一次已经定好的处置")
    common(p_handle)
    p_handle.add_argument("--inbox", default=None, help="闪念键")
    p_handle.add_argument("--to", default=None, help="目标状态")
    p_handle.add_argument("--note", default=None)
    p_handle.add_argument("--slug", default=None, help="转 incubated 时的候办键")
    p_handle.add_argument("--scale", default=None)
    p_handle.add_argument("--title", default=None)
    p_handle.add_argument("--reason", default=None)
    p_handle.add_argument("--backlog", default=None, help="候办键")
    p_handle.add_argument("--exit", default=None, help="promote / iterate / withdraw")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = pathlib.Path(args.project_root).resolve()
    handlers = {"add": cmd_add, "list": cmd_list, "handle": cmd_handle}
    try:
        if not root.is_dir():
            raise IntakeError(f"--project-root 不是目录：{root}")
        payload = handlers[args.command](root, args)
    except IntakeError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")))
        print(f"intake: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
