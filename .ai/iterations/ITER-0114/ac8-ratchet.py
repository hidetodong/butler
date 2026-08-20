#!/usr/bin/env python3
"""ITER-0114 · AC8：文件头三条纪律在场，无真源指针的条目上了只防增量的棘轮。"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOL = ROOT / "scripts" / "sync-project-overview.py"
INVARIANTS = ROOT / ".ai" / "invariants.md"
COPY = (".ai", "Coder", "workflows", "tools", "scripts", "VERSION")

fail = 0


def ok(msg):
    print(f"[OK]   {msg}")


def bad(msg):
    global fail
    fail = 1
    print(f"[FAIL] {msg}")


text = INVARIANTS.read_text(encoding="utf-8")
head = text.split("\n- **", 1)[0]

print("=== AC8 · 文件头三条写作纪律 ===")
DISCIPLINES = {
    "只写决策与理由，不复述机制的具体形状": "①只写决策与理由",
    "每条至少带一个反引号真源指针": "②必带真源指针",
    "还成立才留，作废即删": "③作废即删",
}
for needle, label in DISCIPLINES.items():
    (ok if needle in head else bad)(f"{label}：{'在场' if needle in head else '缺失'}")

print("=== AC8 · 棘轮基线登记在文件头 ===")
if re.search(r"无真源指针的历史条目当前 16 条", head):
    ok("文件头写明基线 16 条")
else:
    bad("文件头没写基线数字")
if "scripts/sync-project-overview.py --check" in head:
    ok("文件头点名了卡它的机器检查")
else:
    bad("文件头没点名机器检查")
if "16 是欠账不是允许额度" in head and ".ai/debt.md" in head:
    ok("文件头声明 16 是欠账并指向 `.ai/debt.md`")
else:
    bad("文件头没把基线声明成欠账")

print("=== AC8 · 实测无指针条目数 ===")
POINTER_RE = re.compile(r"`[^`]*[/.][^`]*`")
entries = [line for line in text.split("\n") if line.startswith("- **")]
missing = [line for line in entries if not POINTER_RE.search(line)]
print(f"       条目总数 {len(entries)}，其中无真源指针 {len(missing)}")
if len(missing) == 16:
    ok("实测 16 条，正好落在基线上")
else:
    bad(f"实测 {len(missing)} 条，与基线 16 不符")

source = TOOL.read_text(encoding="utf-8")
match = re.search(r"^INVARIANT_POINTER_EXEMPT = (\d+)$", source, re.MULTILINE)
if match and match.group(1) == "16":
    ok("基线 16 写死在生成器常量")
else:
    bad(f"生成器基线常量不是 16：{match.group(1) if match else '未找到'}")

print("=== AC8 · 现状不报警 ===")
proc = subprocess.run([sys.executable, str(TOOL), "--check", "--project-root", str(ROOT)],
                      capture_output=True, text=True)
if proc.returncode == 0:
    ok("当前仓 --check 退出码 0，棘轮不误伤存量")
else:
    bad(f"当前仓 --check 退出码 {proc.returncode}：{(proc.stdout + proc.stderr)[:200]}")

print("=== AC8 · 加一条无指针条目就必须被拦 ===")
with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp) / "repo"
    root.mkdir()
    for item in COPY:
        src, dst = ROOT / item, root / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    subprocess.run([sys.executable, str(TOOL), "--write", "--project-root", str(root)],
                   capture_output=True, text=True)
    target = root / ".ai" / "invariants.md"
    target.write_text(
        target.read_text(encoding="utf-8")
        + "- **故意不带真源指针的负例条目**：这条只讲道理不给任何可核对的出处。*为什么*：用来验棘轮。\n",
        encoding="utf-8")
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--project-root", str(root)],
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    if proc.returncode == 0:
        bad("加了第 17 条无指针条目却仍然退出码 0")
    else:
        ok(f"加到 17 条 → 退出码 {proc.returncode}")
        if "invariants without source pointer: 17 > 16" in out:
            ok("诊断给出实测值与基线（17 > 16）")
        else:
            bad(f"诊断没给出实测值与基线：{out[:200]}")
        if "故意不带真源指针的负例条目" in out:
            ok("诊断把无指针条目逐条列出来，能定位到新增的那条")
        else:
            bad("诊断没列出具体条目")

print("=== AC8 · 只防增量：删一条无指针条目不报警 ===")
with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp) / "repo"
    root.mkdir()
    for item in COPY:
        src, dst = ROOT / item, root / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    subprocess.run([sys.executable, str(TOOL), "--write", "--project-root", str(root)],
                   capture_output=True, text=True)
    target = root / ".ai" / "invariants.md"
    lines = target.read_text(encoding="utf-8").split("\n")
    for index, line in enumerate(lines):
        if line.startswith("- **") and not POINTER_RE.search(line):
            del lines[index]
            break
    target.write_text("\n".join(lines), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--project-root", str(root)],
                          capture_output=True, text=True)
    if proc.returncode == 0:
        ok("减到 15 条 → 退出码 0，棘轮只往紧的方向走")
    else:
        bad(f"删条目反而报错（退出码 {proc.returncode}）：{(proc.stdout + proc.stderr)[:200]}")

print()
print("RATCHET-CLEAN" if fail == 0 else "RATCHET-DIRTY")
sys.exit(fail)
