#!/usr/bin/env python3
"""沙箱 dogfood：在临时项目根上把「提升为里程碑」与「开为迭代」两条出口各跑一遍。

为什么要沙箱：这两条出口都要求台账的 `current` 是 `none`，而 butler 仓当前
MILE-0016 与 ITER-0118 都 active，跑不了。**这证明的是代码路径通，不是真实使用下好用。**
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[3]
ENTRY = REPO / "tools" / "intake" / "intake.py"

MILESTONES = """# 里程碑台账

current: none

| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |
|---|---|---|---|---|---|---|
| MILE-0001 | 沙箱旧里程碑 | closed | 2026-01-01 | 2026-01-02 | ITER-0001 | — |

## 待办区（未编号）

| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |
|---|---|---|---|---|
| sandbox-direction | 沙箱方向 | 2026-08-20 | .ai/milestone-backlog/sandbox-direction.md | 沙箱里造的，只为跑通出口 |
"""

ITERATIONS = """# 迭代台账

## 最近迭代

current: none
| 迭代号 | 标题 | 状态 | 开启 | 收口 | 所属 milestone | 交付 |
|---|---|---|---|---|---|---|
| ITER-0001 | 沙箱旧迭代 | closed | 2026-01-01 | 2026-01-02 | MILE-0001 | — |
"""

MILESTONE_MD = """# MILE-0001 — 沙箱旧里程碑

## 5.4 范围演进记录

- 2026-01-01（沙箱）：初始行。
"""

DRAFT_BODY = {
    "milestone": (
        "## 范围评估\n\n沙箱内容。\n\n## 理解阐释\n\n沙箱内容。\n\n"
        "## 拆分路线图\n\n沙箱内容。\n\n## 范围演进记录\n\n沙箱内容。\n"
    ),
    "iteration": "## 要解决什么\n\n沙箱内容。\n\n## 暂缓原因\n\n沙箱内容。\n",
}

INBOX = """# INBOX — 闪念口

## 闪念

| 闪念键 | 记于 | 一句话 | 状态 | 去向 |
|---|---|---|---|---|
| 2026-08-19-sandbox-seed | 2026-08-19 | 沙箱种子闪念 | incubated | .ai/milestone-backlog/sandbox-direction.md |
"""

failures = []


def check(label, ok, detail=""):
    print(f"[{'OK' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        failures.append(label)


def build(scale):
    root = pathlib.Path(tempfile.mkdtemp(prefix="intake-sandbox-"))
    ai = root / ".ai"
    (ai / "milestone-backlog").mkdir(parents=True)
    (ai / "MILESTONES.md").write_text(MILESTONES, encoding="utf-8")
    (ai / "ITERATIONS.md").write_text(ITERATIONS, encoding="utf-8")
    (ai / "MILESTONE.md").write_text(MILESTONE_MD, encoding="utf-8")
    (ai / "INBOX.md").write_text(INBOX, encoding="utf-8")
    (ai / "milestone-backlog" / "sandbox-direction.md").write_text(
        f"# 沙箱方向\n\n候办键: sandbox-direction\n候办状态: deferred\n规模: {scale}\n\n"
        + DRAFT_BODY[scale],
        encoding="utf-8",
    )
    return root


def call(root, *args):
    proc = subprocess.run(
        [sys.executable, str(ENTRY), "handle", "--project-root", str(root), *args],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def run_promote():
    print("\n=== 出口一 · promote（提升为里程碑）===")
    root = build("milestone")
    try:
        code, out, err = call(root, "--backlog", "sandbox-direction", "--exit", "promote",
                              "--date", "2026-08-20")
        print(out or err)
        check("promote 退出码为 0", code == 0, err)
        payload = json.loads(out) if code == 0 else {}
        check("领到 MILE-0002", payload.get("id") == "MILE-0002", str(payload.get("id")))
        ledger = (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8")
        check("current 指向新号", "current: MILE-0002" in ledger)
        check("正式表出现 active 行",
              "| MILE-0002 | 沙箱方向 | active | 2026-08-20 | — | — | — |" in ledger)
        check("待办区索引行已删", "sandbox-direction" not in ledger)
        check("草稿文件已删",
              not (root / ".ai" / "milestone-backlog" / "sandbox-direction.md").exists())
        body = (root / ".ai" / "MILESTONE.md").read_text(encoding="utf-8")
        check("活工作区四段齐备并按 §5 重新编号",
              all(s in body for s in ("## 5.1 范围评估", "## 5.2 理解阐释",
                                      "## 5.3 拆分路线图", "## 5.4 范围演进记录")))
        check("活工作区标题带上新号", body.startswith("# MILE-0002 — 沙箱方向"))
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run_iterate():
    print("\n=== 出口二 · iterate（开为迭代）===")
    root = build("iteration")
    try:
        code, out, err = call(root, "--backlog", "sandbox-direction", "--exit", "iterate",
                              "--date", "2026-08-20")
        print(out or err)
        check("iterate 退出码为 0", code == 0, err)
        payload = json.loads(out) if code == 0 else {}
        check("领到 ITER-0002", payload.get("id") == "ITER-0002", str(payload.get("id")))
        check("回执给出下一步而不是代劳四件套",
              "iteration-schema.md §5.1" in payload.get("next_step", ""))
        ledger = (root / ".ai" / "ITERATIONS.md").read_text(encoding="utf-8")
        check("current 指向新号", "current: ITER-0002" in ledger)
        check("台账出现 active 行",
              "| ITER-0002 | 沙箱方向 | active | 2026-08-20 | — |" in ledger)
        check("四件套未被代写",
              not (root / ".ai" / "CONCEPT.md").exists())
        milestones = (root / ".ai" / "MILESTONES.md").read_text(encoding="utf-8")
        check("待办区索引行已删", "sandbox-direction" not in milestones)
        check("草稿文件已删",
              not (root / ".ai" / "milestone-backlog" / "sandbox-direction.md").exists())
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run_blocked():
    print("\n=== 对照 · current 非 none 时两条出口都被拦下 ===")
    for scale, exit_name, field, value in (
        ("milestone", "promote", "MILESTONES.md", "MILE-0001"),
        ("iteration", "iterate", "ITERATIONS.md", "ITER-0001"),
    ):
        root = build(scale)
        try:
            path = root / ".ai" / field
            path.write_text(
                path.read_text(encoding="utf-8").replace("current: none", f"current: {value}", 1),
                encoding="utf-8",
            )
            code, out, err = call(root, "--backlog", "sandbox-direction", "--exit", exit_name,
                                  "--date", "2026-08-20")
            check(f"{exit_name} 被 current 拦下", code != 0)
            check(f"{exit_name} 拦下时草稿仍在",
                  (root / ".ai" / "milestone-backlog" / "sandbox-direction.md").exists())
            print("  " + (out or err))
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    run_promote()
    run_iterate()
    run_blocked()
    print("\n" + ("SANDBOX DOGFOOD PASS" if not failures else f"SANDBOX DOGFOOD FAIL: {failures}"))
    sys.exit(1 if failures else 0)
