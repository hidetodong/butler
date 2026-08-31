#!/usr/bin/env python3
"""ITER-0118 两组扫描：A 组查越界（不该出现的东西不在），B 组查在场（该出现的都在）。

模式串一律用片段拼接构造，避免本脚本自命中。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

ACTIVE_DIRS = ["Coder", "templates", "tools", "scripts", "workflows", "plugins",
               ".claude", "docs", "migrations", "deliveries"]
TEXT_SUFFIX = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".template", ".toml"}

# 片段拼接：R9 才存在的孵化区路径、R8 才退役的旧编号前缀与双指纹字段名
FUTURE_DIR = ".ai/" + "backlog" + "/"
OLD_ID_PREFIX = "SR" + "C-"
OLD_FIELDS = ["observed" + "_sha256", "processed" + "_sha256"]
OLD_SOURCE_DIR = "ori" + "gin/"
OLD_ACTION_RULE = "inbox" + "-workflow.md"

SHELLS = [".claude/commands/butler/inbox.md",
          "plugins/butler/skills/butler-inbox/SKILL.md"]

failures: list[str] = []
checks = 0


def check(label, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        failures.append(f"{label}" + (f" — {detail}" if detail else ""))
    print(f"[{'OK' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail and not ok else ""))


def active_files():
    seen = []
    for name in ACTIVE_DIRS:
        base = ROOT / name
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in TEXT_SUFFIX and ".git" not in p.parts:
                seen.append(p)
    seen += [p for p in ROOT.glob("*.md") if p.is_file()]
    return sorted(set(seen))


def read(path):
    try:
        return pathlib.Path(path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return ""


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------- A 组 · 越界
def group_a():
    print("\n=== A 组 · 越界（这些东西不该出现）===")
    files = active_files()
    hits = [str(p.relative_to(ROOT)) for p in files
            if FUTURE_DIR in read(p) and p != pathlib.Path(__file__)]
    check(f"A1 活跃面不出现 R9 才存在的孵化区路径（扫 {len(files)} 份）",
          not hits, ", ".join(hits))

    new_surface = ["tools/intake/intake.py", "tools/intake/README.md",
                   "tools/intake/tests/test_intake.py", "tools/intake/tests/helpers.py",
                   "Coder/40_Context_Management/intake-schema.md",
                   "Coder/40_Context_Management/intake-workflow.md"]
    bad = [f for f in new_surface if OLD_ID_PREFIX in read(ROOT / f)]
    check("A2a 新工具与新规则不出现旧编号前缀", not bad, ", ".join(bad))
    bad = [f"{f}:{field}" for f in new_surface for field in OLD_FIELDS
           if field in read(ROOT / f)]
    check("A2b 新工具与新规则不出现双指纹字段名", not bad, ", ".join(bad))

    for shell in SHELLS:
        text = read(ROOT / shell)
        check(f"A3a {shell} 不再提旧来源目录", OLD_SOURCE_DIR not in text)
        check(f"A3b {shell} 不再提旧动作层规则", OLD_ACTION_RULE not in text)


# ---------------------------------------------------------------- B 组 · 在场
def group_b():
    print("\n=== B 组 · 在场（这些东西必须都在）===")

    # B1 旧链逐字节未动
    baseline = ROOT / ".ai/iterations/ITER-0118/pre-p4.baseline"
    guarded_prefixes = ("Coder/40_Context_Management/inbox-schema.md",
                        "Coder/40_Context_Management/inbox-workflow.md",
                        "templates/hooks/tests/test_inbox_contract.py",
                        "tools/inbox/")
    drift = []
    for line in baseline.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        digest, path = line.split(None, 1)
        path = path.strip()
        if not path.startswith(guarded_prefixes):
            continue
        if sha(ROOT / path) != digest:
            drift.append(path)
    check("B1 旧链（旧契约 / 旧动作层 / 旧测试 / 旧工具全目录）逐字节未动",
          not drift, ", ".join(drift))

    # B2 三个动作在场
    tool = read(ROOT / "tools/intake/intake.py")
    for action in ("add", "list", "handle"):
        check(f"B2a 工具注册了 {action} 子命令", f'sub.add_parser("{action}"' in tool)
    rule = read(ROOT / "Coder/40_Context_Management/intake-workflow.md")
    for action in ("add", "list", "handle"):
        check(f"B2b 动作层写了 {action} 的边界", f"`{action}`" in rule)
    for shell in SHELLS:
        text = read(ROOT / shell)
        check(f"B2c {shell} 调用新工具", "tools/intake/" in text)
        check(f"B2d {shell} 读新契约", "intake-schema.md" in text)

    # B3 README 两处注册
    readme = read(ROOT / "Coder/README.md")
    tree_hits = len(re.findall(r"^ {4}intake-workflow\.md$", readme, re.M))
    check("B3a 目录结构里注册恰 1 次", tree_hits == 1, str(tree_hits))
    ptr_hits = len(re.findall(r"^- `40_Context_Management/intake-workflow\.md`", readme, re.M))
    check("B3b 读取顺序指针里注册恰 1 次", ptr_hits == 1, str(ptr_hits))

    # B4 §7.6 已改指工具，且本轮改动落在 §7.6 内
    schema_path = "Coder/20_Workflow_Lifecycle/milestone-schema.md"
    schema = read(ROOT / schema_path)
    check("B4a §7.6 已改指工具", "tools/intake/intake.py" in schema)
    lines = schema.splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("### 7.6")) + 1
    end = next(i for i, l in enumerate(lines) if l.startswith("## 8.")) + 1
    diff = subprocess.run(["git", "diff", "-U0", "--", schema_path],
                          cwd=ROOT, capture_output=True, text=True).stdout
    hunks = re.findall(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M)
    check("B4b 该文件对 HEAD 恰 2 个改动块（另一块是 ITER-0117 的 §4.5 分档）",
          len(hunks) == 2, str(len(hunks)))
    mine = [(int(a), int(b) if b else 1) for a, b in hunks if int(a) >= start]
    check("B4c 本轮的改动块落在 §7.6 区间内",
          len(mine) == 1 and start <= mine[0][0] and mine[0][0] + mine[0][1] - 1 <= end,
          f"§7.6=[{start},{end}] hunks={hunks}")

    # B5 候办 9 → 10
    milestones = read(ROOT / ".ai/MILESTONES.md")
    body = milestones.split("## 待办区")[1]
    rows = [l for l in body.splitlines() if l.startswith("| ") and not l.startswith("| 候办键")]
    check("B5a 待办区索引恰 10 行", len(rows) == 10, str(len(rows)))
    drafts = sorted(p.name for p in (ROOT / ".ai/milestone-backlog").glob("*.md"))
    check("B5b 草稿文件恰 10 份且与索引集合相等",
          len(drafts) == 10 and {r.split("|")[1].strip() + ".md" for r in rows} == set(drafts),
          str(drafts))

    # B6 dogfood 草稿无占位残留、闪念行已回写
    draft = read(ROOT / ".ai/milestone-backlog/delivery-renderer-in-repo.md")
    check("B6a dogfood 草稿已填实（无占位标记残留）",
          "TODO(" + "intake)" not in draft)
    check("B6b dogfood 草稿是 iteration 档", "规模: iteration" in draft)
    inbox = read(ROOT / ".ai/INBOX.md")
    check("B6c 闪念行已回写为 incubated 且去向指向那份草稿",
          "| incubated | .ai/milestone-backlog/delivery-renderer-in-repo.md |" in inbox)
    check("B6d 闪念表用的是新契约表头",
          "| 闪念键 | 记于 | 一句话 | 状态 | 去向 |" in inbox)

    # B7 路由示例已换措辞
    examples = read(ROOT / "workflows/router-examples.json")
    check("B7a 路由示例不再描述已经不存在的行为",
          "处理 " + OLD_SOURCE_DIR.rstrip("/") + " 里的需求收件箱" not in examples)
    check("B7b 路由示例换成了新语义", "闪念口" in examples)

    # B8 注册表
    registry = json.loads(read(ROOT / "workflows/registry.json"))
    entry = [w for w in registry["workflows"] if w["id"] == "inbox"][0]
    check("B8a inbox 条目 rule_source 指向新动作层",
          entry["rule_source"] == "Coder/40_Context_Management/intake-workflow.md",
          entry["rule_source"])
    check("B8b 业务工作流仍 12 个", len(registry["workflows"]) == 12,
          str(len(registry["workflows"])))

    # B9 三条出口在场
    for name in ("promote", "iterate", "withdraw"):
        check(f"B9 出口 {name} 在工具与动作层都在场",
              f'"{name}"' in tool and f"`{name}`" in rule)

    # B10 CI 已接入
    ci = read(ROOT / "scripts/verify-ci.sh")
    check("B10a CI 接入了新工具的测试", "tools/intake/tests" in ci)
    check("B10b CI 仍保留旧工具的测试（R8 才删）", "tools.inbox.tests.test_inbox" in ci)


if __name__ == "__main__":
    group_a()
    group_b()
    print(f"\n共 {checks} 项检查")
    if failures:
        print("SWEEP FAIL:")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("SWEEP PASS")
