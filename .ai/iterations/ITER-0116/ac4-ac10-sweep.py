#!/usr/bin/env python3
"""ITER-0116 AC4/AC10 sweep — two directions, because this iteration edits without deleting.

Group A (negative): the things that must be gone are gone, repo-wide.
Group B (presence):  the /butler:loop entities that must survive are byte-identical
                     and still wired, plus the intended edits actually landed.

Group A patterns are assembled from fragments so this file never matches itself.
Exit 0 only when A is empty AND every B assertion holds.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SELF = Path(__file__).resolve()
BASELINE = Path(__file__).resolve().parent / "loop-entities.baseline"

# ---------------------------------------------------------------- group A ----

DETECT = "检测到"
COMPLEX = "复杂度"
LOOPNAME = "收敛闭环"

GROUP_A = {
    "A1 · 主动询问原句": "是否需要开启" + LOOPNAME + "模式",
    "A2 · 激活清单第三条": "Butler " + DETECT + "极高" + COMPLEX + "任务",
    "A3 · 已撤候办的键": "upgrade-" + "convergence-engine",
}
# AC5 也要求全仓不出现「检测到」+「复杂度」+「收敛闭环」的等价组合话术
COMBO = (DETECT, COMPLEX, LOOPNAME)

EXCLUDED_DIRS = {
    ".git", ".venv", ".pytest_cache", "node_modules",
    ".ai/iterations", ".ai/history", ".ai/.artifact-migration-backups",
    ".ai/verification-evidence",
    "deliveries", "migrations",
}
# 本迭代自己的工作区产物与状态文件：它们的职责就是记录这次清理，
# 命中属于预期，不是活引用。排除面在 VERIFY_REPORT 里逐份摊开。
EXCLUDED_FILES = {
    ".ai/CONCEPT.md", ".ai/AC_LIST.md", ".ai/TECH_PLAN.md", ".ai/VERIFY_REPORT.md",
    ".ai/01_CHANGELOG.md", ".ai/task-state.md", ".ai/02_SESSION_HANDOFF.md",
    ".ai/handoff-state.json", ".ai/ITERATIONS.md", ".ai/MILESTONE.md",
    ".ai/MILESTONES.md", ".ai/RUN_LOG.md", ".ai/00_IDEATION.md", ".ai/00_IDEATION.html",
}


def excluded(path: Path) -> bool:
    if path == SELF or path == BASELINE:
        return True
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDED_FILES:
        return True
    return any(rel == d or rel.startswith(d + "/") for d in EXCLUDED_DIRS)


def run_group_a() -> tuple[list[str], int]:
    hits: list[str] = []
    scanned = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink() or excluded(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            for name, pattern in GROUP_A.items():
                if pattern in line:
                    hits.append(f"{name}  {rel}:{number}: {line.strip()[:150]}")
            if all(token in line for token in COMBO):
                hits.append(f"A4 · 等价组合话术  {rel}:{number}: {line.strip()[:150]}")
    return hits, scanned


# ---------------------------------------------------------------- group B ----

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_baseline() -> dict[str, str]:
    table: dict[str, str] = {}
    for raw in BASELINE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        if len(digest) == 64:
            table[rel.strip()] = digest
    return table


def run_group_b() -> list[str]:
    fails: list[str] = []

    def check(ok: bool, label: str, detail: str = "") -> None:
        if not ok:
            fails.append(f"{label}{(' — ' + detail) if detail else ''}")

    # B1 六处 loop 实体逐字节未改
    baseline = load_baseline()
    check(len(baseline) == 6, "B1 基线条目数应为 6", f"实为 {len(baseline)}")
    for rel, expected in sorted(baseline.items()):
        path = ROOT / rel
        if not path.is_file():
            fails.append(f"B1 loop 实体缺失: {rel}")
            continue
        actual = sha256(path)
        check(actual == expected, f"B1 loop 实体被改动: {rel}", f"{actual[:12]} != {expected[:12]}")

    link = ROOT / ".agents/skills/butler-loop"
    check(link.is_symlink(), "B2 .agents/skills/butler-loop 不是软链")
    check(link.resolve().is_dir(), "B2 butler-loop 软链断链", str(link.resolve()))

    # B3 registry 仍带 loop、总数仍 12、仍必须显式点名
    registry = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
    flows = registry.get("workflows", [])
    check(len(flows) == 12, "B3 registry 工作流数应为 12", f"实为 {len(flows)}")
    loop = next((w for w in flows if w.get("id") == "loop"), None)
    check(loop is not None, "B3 registry 里没有 loop 条目")
    if loop is not None:
        check(loop.get("allow_implicit_invocation") is False,
              "B3 loop 的 allow_implicit_invocation 应为 false", repr(loop.get("allow_implicit_invocation")))
        check(loop.get("risk") == "high", "B3 loop 的 risk 应为 high", repr(loop.get("risk")))

    # B4 人读投影里 loop 行还在
    workflows_doc = (ROOT / "docs/workflows.md").read_text(encoding="utf-8")
    check("/butler:loop" in workflows_doc, "B4 docs/workflows.md 里没有 /butler:loop")

    # B5 冻结声明三要素齐备，且落在 H1 与 §1 之间
    engine_path = ROOT / "Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md"
    engine = engine_path.read_text(encoding="utf-8")
    head = engine.split("## 1. 身份")[0]
    check("已冻结" in head, "B5 冻结声明不在 H1 与 §1 之间")
    check("ITER-0116" in head and "R5" in head, "B5 冻结声明缺冻结起始（ITER-0116 / R5）")
    check("R13" in head and "使用数据" in head, "B5 冻结声明缺解冻条件（R13 · 使用数据）")
    check("原样保留" in head and "演进" in head, "B5 冻结声明缺冻结含义（保留行为 / 停演进）")

    # B6 §2 激活条件由 3 条减为 2 条，两条都还在
    section2 = engine.split("满足以下任一条件时激活：")[1].split("## 3.")[0]
    bullets = [l for l in section2.splitlines() if l.startswith("- ")]
    check(len(bullets) == 2, "B6 §2 激活条件应为 2 条", f"实为 {len(bullets)}")
    check(any("/butler:loop" in b for b in bullets), "B6 §2 丢了显式命令那条")
    check(any("死磕" in b for b in bullets), "B6 §2 丢了显式语义那条")

    # B7 §3–§8 的算法正文仍在（抽查各节标题）
    for heading in ["## 3. 核心逻辑", "## 4.", "## 5.", "## 6.", "## 7.", "## 8."]:
        check(heading in engine, f"B7 规则真源缺章节 {heading}")

    # B8 logic-protocol 模式清单仍 8 条、loop 那条仍在
    logic = (ROOT / "Coder/00_System_Prompt/logic-protocol.md").read_text(encoding="utf-8")
    modes_block = logic.split("你必须根据用户的指令或语义环境，丝滑切换模式：")[1].split("### 审计者意识")[0]
    modes = [l for l in modes_block.splitlines() if l.startswith("- **")]
    check(len(modes) == 8, "B8 模式清单应为 8 条", f"实为 {len(modes)}")
    check(any(LOOPNAME + "模式" in m for m in modes), "B8 模式清单里 loop 那条丢了")

    # B9 dangerous 的指针改到位、并列陈述保留、对 loop 规则文件零引用
    dangerous = (ROOT / "Coder/65_Extension_Dangerous/dangerous-engine.md").read_text(encoding="utf-8")
    check("convergence-" + "loop-engine" not in dangerous, "B9 dangerous 仍引用 loop 规则文件")
    check("bounded-convergence.md` §3 写 RCA" in dangerous, "B9 dangerous §8 的新 RCA 指针没落地")
    check("与" + LOOPNAME + " (`/butler:loop`)" in dangerous, "B9 dangerous §9 的并列陈述被误删")

    # B10 候办两侧删净、其余 9 份完好
    check(not (ROOT / ".ai/milestone-backlog/upgrade-" "convergence-engine.md").exists(),
          "B10 候办草稿文件仍在")
    drafts = sorted(p.name for p in (ROOT / ".ai/milestone-backlog").glob("*.md"))
    check(len(drafts) == 9, "B10 候办文件应剩 9 份", f"实为 {len(drafts)}")
    milestones = (ROOT / ".ai/MILESTONES.md").read_text(encoding="utf-8")
    backlog_rows = re.findall(r"^\| ([a-z0-9-]+) \|", milestones.split("## 待办区")[1], re.M)
    check(len(backlog_rows) == 9, "B10 待办区索引应剩 9 行", f"实为 {len(backlog_rows)}")
    check(sorted(backlog_rows) == sorted(d[:-3] for d in drafts),
          "B10 索引行与实际文件不是同一集合")

    # B11 debt 一删一增、净额仍 10
    debt = (ROOT / ".ai/debt.md").read_text(encoding="utf-8")
    items = [l for l in debt.splitlines() if l.startswith("- **")]
    check(len(items) == 10, "B11 debt 条目应为 10", f"实为 {len(items)}")
    check(not any("自动绑定" in i for i in items), "B11 已还清的旧账没删掉")
    check(any("演进冻结没有机器兜底" in i for i in items), "B11 新欠账没登记")

    # B12 §5.4 三条登记各自写到位
    milestone = (ROOT / ".ai/MILESTONE.md").read_text(encoding="utf-8")
    s54 = milestone.split("## 5.4 范围演进记录")[1]
    check(s54.count("- 2026-08-20（R5") == 3, "B12 §5.4 的 R5 登记应为 3 条",
          f"实为 {s54.count('- 2026-08-20（R5')}")
    check("名字撞车" in s54, "B12 §5.4 缺「候办与 loop 只是名字撞车」的说明")
    check("41ad694" in s54, "B12 §5.4 缺 debt 已还清的出处 commit")
    check("regen-entrypoints" in s54, "B12 §5.4 缺不触发入口重生成的判定")

    return fails


def main() -> int:
    hits, scanned = run_group_a()
    print(f"scanned {scanned} text files under {ROOT}")
    print(f"\n[A · 不该有的] patterns={len(GROUP_A) + 1} hits={len(hits)}")
    for item in hits:
        print(f"  {item}")

    fails = run_group_b()
    print(f"\n[B · 该留的] assertions failed={len(fails)}")
    for item in fails:
        print(f"  {item}")

    failed = bool(hits or fails)
    print("\nRESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
