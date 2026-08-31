"""测试夹具：在临时目录里造一个最小可用的项目根。"""

from __future__ import annotations

import pathlib

MILESTONES_TMPL = """# 里程碑台账

current: {current}

| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |
|---|---|---|---|---|---|---|
{formal_rows}
## 待办区（未编号）

| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |
|---|---|---|---|---|
{backlog_rows}"""

ITERATIONS_TMPL = """# 迭代台账

## 最近迭代

current: {current}
| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
{rows}"""

MILESTONE_MD_TMPL = """# MILE-9999 — 夹具里程碑

## 5.1 范围评估

占位。

## 5.4 范围演进记录

- 2026-01-01（夹具）：初始行。
"""


def make_root(
    tmpdir,
    *,
    milestones_current="none",
    iterations_current="none",
    formal_rows=(),
    backlog_rows=(),
    iteration_rows=(),
    with_milestone_md=True,
):
    root = pathlib.Path(tmpdir)
    ai = root / ".ai"
    ai.mkdir(parents=True, exist_ok=True)
    (ai / "milestone-backlog").mkdir(exist_ok=True)
    (ai / "MILESTONES.md").write_text(
        MILESTONES_TMPL.format(
            current=milestones_current,
            formal_rows="".join(r + "\n" for r in formal_rows) + "\n",
            backlog_rows="".join(r + "\n" for r in backlog_rows),
        ),
        encoding="utf-8",
    )
    (ai / "ITERATIONS.md").write_text(
        ITERATIONS_TMPL.format(
            current=iterations_current,
            rows="".join(r + "\n" for r in iteration_rows),
        ),
        encoding="utf-8",
    )
    if with_milestone_md:
        (ai / "MILESTONE.md").write_text(MILESTONE_MD_TMPL, encoding="utf-8")
    return root


def snapshot(root):
    """把 .ai 下所有文件的字节内容抓成 {相对路径: bytes}。"""
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / ".ai").rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = p.read_bytes()
    return out
