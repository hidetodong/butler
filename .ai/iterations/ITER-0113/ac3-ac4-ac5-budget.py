#!/usr/bin/env python3
"""ITER-0113 · AC3 / AC4 / AC5：读序块的投影校验、结构断言与体量上限实测。

正例走仓库真实状态；负例在临时副本上现造，断言诊断字符串指名到具体文件 / 具体缺项，
不只断言"报错了"。
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "context-budget" / "context_budget.py"
SOURCE = "Coder/40_Context_Management/context-persistence.md"
PROJECTIONS = ("AGENTS.md", "Coder/README.md",
               "templates/AGENTS.md.template", "templates/CLAUDE.md.template")
CARRIERS = (SOURCE,) + PROJECTIONS
LIMITS = {"order_bytes": 1400, "order_nonempty_lines": 9, "order_pointers": 10}

fail = 0


def ok(msg):
    print(f"[OK]   {msg}")


def bad(msg):
    global fail
    fail = 1
    print(f"[FAIL] {msg}")


def run_check(root):
    proc = subprocess.run([sys.executable, str(TOOL), "check", "--project-root", str(root)],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


# 与 tools/context-budget/tests 的 setUp 同一份清单：check 会 fail-closed 地要求这些文件在场
FIXTURE_FILES = CARRIERS + (
    "templates/rule-card.md",
    "Coder/domain-model.md",
    "Coder/domain-glossary.md",
    "Coder/context-map.md",
    "Coder/architecture-overview.md",
    ".ai/project/invariants.md",
    ".ai/debt.md",
    ".ai/iterations/ITER-0107/AC_LIST.md",
    "deliveries/ITER-0107-domain-model-boundaries.md",
)


def sandbox(tmp):
    root = pathlib.Path(tmp) / "repo"
    root.mkdir()
    for rel in dict.fromkeys(FIXTURE_FILES):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    # 术语表与上下文地图里的 md 指针必须落地，否则 check 在指针存在性上就先红了
    pointer_text = "\n".join(
        (root / rel).read_text(encoding="utf-8")
        for rel in ("Coder/domain-glossary.md", "Coder/context-map.md")
    )
    for raw in re.findall(r"`([^`]+\.md)(?:#[^`]*)?`", pointer_text):
        target = root / raw.split("#", 1)[0]
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# fixture\n", encoding="utf-8")
    return root


print("=== AC5 · 体量上限与 metrics 实测 ===")
code, out = run_check(ROOT)
if code == 0:
    ok("仓库真实状态 context_budget.py check 退出码 0")
else:
    bad(f"仓库真实状态 check 退出码 {code}：{out[:400]}")
metrics = json.loads(out).get("metrics", {})
for key, limit in LIMITS.items():
    value = metrics.get(key)
    if value is None:
        bad(f"metrics 缺 {key}")
    elif value <= limit:
        ok(f"{key} = {value}（上限 {limit}）")
    else:
        bad(f"{key} = {value} 超出上限 {limit}")
if metrics.get("order_projections") == 4:
    ok("order_projections = 4，四处投影全部纳入校验")
else:
    bad(f"order_projections = {metrics.get('order_projections')}，应为 4")

print("=== AC3 · 投影失配指名到具体文件 ===")
for target in PROJECTIONS:
    with tempfile.TemporaryDirectory() as tmp:
        root = sandbox(tmp)
        path = root / target
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("读 `.ai/debt.md`", "读 `.ai/debt.md`（篡改）", 1),
                        encoding="utf-8")
        code, out = run_check(root)
        needle = f"order projection mismatch: {target}"
        others = [p for p in PROJECTIONS if p != target]
        if code != 0 and needle in out:
            if any(f"order projection mismatch: {o}" in out for o in others):
                bad(f"{target} 被改，却连带报了其他投影")
            else:
                ok(f"篡改 {target} → 诊断指名该文件，未连坐其他三处")
        else:
            bad(f"篡改 {target} 未报 `{needle}`（退出码 {code}）")

print("=== AC3 · 真源被改致四处同时失配 ===")
with tempfile.TemporaryDirectory() as tmp:
    root = sandbox(tmp)
    path = root / SOURCE
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("读 `.ai/debt.md`", "读 `.ai/debt.md`（篡改）", 1),
                    encoding="utf-8")
    code, out = run_check(root)
    hits = [p for p in PROJECTIONS if f"order projection mismatch: {p}" in out]
    if code != 0 and len(hits) == 4:
        ok("改真源 → 四处投影全部报失配")
    else:
        bad(f"改真源只报了 {len(hits)} 处失配（退出码 {code}）")

print("=== AC3 · 标记缺失 fail-closed ===")
with tempfile.TemporaryDirectory() as tmp:
    root = sandbox(tmp)
    path = root / "AGENTS.md"
    path.write_text(path.read_text(encoding="utf-8")
                    .replace("<!-- butler-context-order:begin -->", "", 1), encoding="utf-8")
    code, out = run_check(root)
    if code != 0 and "AGENTS.md" in out and "order markers" in out:
        ok("AGENTS.md 缺标记 → fail-closed 且诊断带文件名")
    else:
        bad(f"标记缺失未 fail-closed 或诊断不带文件名（退出码 {code}）：{out[:300]}")

print("=== AC4 · 结构断言三条负例各自指名 ===")
cases = [
    ("编号断开", "5. **产物与代码**", "6. **产物与代码**", "order steps must be"),
    ("某步无 .ai/ 路径", "读 `.ai/debt.md`：还悬着什么账", "看还悬着什么账", "has no .ai/ pointer"),
    ("抽掉锚点", "再沿 `.ai/state-index.json` 用", "再沿冷分片索引用", "missing anchor"),
]
for name, old, new, needle in cases:
    with tempfile.TemporaryDirectory() as tmp:
        root = sandbox(tmp)
        for rel in CARRIERS:
            path = root / rel
            path.write_text(path.read_text(encoding="utf-8").replace(old, new),
                            encoding="utf-8")
        code, out = run_check(root)
        if code != 0 and needle in out:
            ok(f"{name} → 诊断含 `{needle}`")
        else:
            bad(f"{name} 未报 `{needle}`（退出码 {code}）：{out[:300]}")

print()
print("BUDGET-CLEAN" if fail == 0 else "BUDGET-DIRTY")
sys.exit(fail)
