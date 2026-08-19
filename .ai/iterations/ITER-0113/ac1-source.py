#!/usr/bin/env python3
"""AC1：读序真源结构 + 标记对数 + 三条硬约束落在对应步骤内。"""
import io, re, sys, pathlib

BEGIN = "<!-- butler-context-order:begin -->"
END = "<!-- butler-context-order:end -->"
SRC = "Coder/40_Context_Management/context-persistence.md"
CARRIERS = [SRC, "AGENTS.md", "Coder/README.md",
            "templates/AGENTS.md.template", "templates/CLAUDE.md.template"]
fail = 0


def ok(msg):
    print(f"[OK]   {msg}")


def bad(msg):
    global fail
    print(f"[FAIL] {msg}")
    fail = 1


# 标记对数：只数规则 / 入口 / 模板载体。工作区四件套里出现的是本迭代自己在
# 描述这套机制的散文，不是载体，按 ITER-0112 AC6 同样的白名单纪律排除。
hits = sorted(
    str(p) for p in pathlib.Path(".").rglob("*")
    if p.is_file()
    and not str(p).startswith((".git/", ".ai/"))
    and "__pycache__" not in str(p)
    and p.suffix in {".md", ".template"}
    and BEGIN in p.read_text(encoding="utf-8", errors="ignore")
)
if hits == sorted(CARRIERS):
    ok(f"标记对数为 {len(hits)}（真源 1 + 投影 4），载体清单与预期一致")
else:
    bad(f"载体清单不符：{hits}")

text = io.open(SRC, encoding="utf-8").read()
if text.count(BEGIN) == 1 and text.count(END) == 1:
    ok("真源标记各恰好一次")
else:
    bad("真源标记数量异常")

block = text.split(BEGIN, 1)[1].split(END, 1)[0]
matches = list(re.finditer(r"^(\d+)\. ", block, re.M))
steps = {}
for i, m in enumerate(matches):
    stop = matches[i + 1].start() if i + 1 < len(matches) else len(block)
    steps[int(m.group(1))] = block[m.start():stop]

if sorted(steps) == [1, 2, 3, 4, 5]:
    ok("五步编号连续 1..5")
else:
    bad(f"步骤编号异常：{sorted(steps)}")

CONSTRAINTS = {
    2: ["`.ai/state-index.json`", "`lookup`", "禁止默认读取整个 `.ai/history/`"],
    3: ["check", "`fresh` 才读", "`stale` 先 `sync` 重建", "`error` 先修权威状态"],
    4: ["state / reason / next", "可重建投影"],
}
for step, needles in CONSTRAINTS.items():
    body = steps.get(step, "")
    for needle in needles:
        if needle in body:
            ok(f"第 {step} 步含硬约束片段：{needle}")
        else:
            bad(f"第 {step} 步缺硬约束片段：{needle}")

if "R2" not in text:
    ok("真源正文已无 R2 过渡措辞")
else:
    bad("真源正文仍有 R2 过渡措辞")

print()
print("AC1-CLEAN" if not fail else "AC1-DIRTY")
sys.exit(fail)
