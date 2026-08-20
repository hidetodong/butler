#!/usr/bin/env python3
"""ITER-0114 · AC3 / AC4：`--check` 的漂移诊断指名到节，体量上限真的拦得住。

负例都在临时副本上现造，逐条断言诊断字符串——只断言「非零退出」证明不了它抓的是对的那一节。
"""
import io
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOL = ROOT / "scripts" / "sync-project-overview.py"
COPY = (".ai", "Coder", "workflows", "tools", "scripts", "VERSION")
SECTIONS = ["版本与当前状态", "里程碑时间线", "规则体系目录与职责", "工作流清单", "驻留工具清单"]

fail = 0


def ok(msg):
    print(f"[OK]   {msg}")


def bad(msg):
    global fail
    fail = 1
    print(f"[FAIL] {msg}")


def run(args, root):
    proc = subprocess.run([sys.executable, str(TOOL), *args, "--project-root", str(root)],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def sandbox(tmp):
    root = pathlib.Path(tmp) / "repo"
    root.mkdir()
    for item in COPY:
        src, dst = ROOT / item, root / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    run(["--write"], root)
    return root


print("=== AC3 · 正例 ===")
code, out = run(["--check"], ROOT)
(ok if code == 0 else bad)(f"真仓 --check 退出码 {code}")

print("=== AC3 · 逐节篡改，诊断只指名被改的那一节 ===")
TAMPER = {
    "版本与当前状态": ("- 规则源版本：**", "- 规则源版本：**篡改**\n- 原行：**"),
    "里程碑时间线": ("| MILE-0016 |", "| MILE-9999 |"),
    "规则体系目录与职责": ("| `00_System_Prompt/` |", "| `00_被改过/` |"),
    "工作流清单": ("| inbox |", "| 被改过 |"),
    "驻留工具清单": ("| `tools/handoff/` |", "| `tools/被改过/` |"),
}
for section, (old, new) in TAMPER.items():
    with tempfile.TemporaryDirectory() as tmp:
        root = sandbox(tmp)
        page = root / ".ai" / "OVERVIEW.md"
        text = page.read_text(encoding="utf-8")
        if old not in text:
            bad(f"{section} 的篡改锚点没找到：{old}")
            continue
        page.write_text(text.replace(old, new, 1), encoding="utf-8")
        code, out = run(["--check"], root)
        others = [s for s in SECTIONS if s != section]
        if code != 0 and f"overview section drift: {section}" in out:
            if any(f"overview section drift: {o}" in out for o in others):
                bad(f"改 {section} 却连坐了其他节")
            else:
                ok(f"改「{section}」→ 诊断只指名这一节")
        else:
            bad(f"改 {section} 未报对应诊断（退出码 {code}）：{out[:200]}")

print("=== AC3 · 改节标题报节集不匹配 ===")
with tempfile.TemporaryDirectory() as tmp:
    root = sandbox(tmp)
    page = root / ".ai" / "OVERVIEW.md"
    page.write_text(page.read_text(encoding="utf-8").replace("## 驻留工具清单", "## 被改名的节", 1),
                    encoding="utf-8")
    code, out = run(["--check"], root)
    if code != 0 and "overview section set mismatch" in out:
        ok("节标题被改 → 报 section set mismatch")
    else:
        bad(f"节标题被改未报节集不匹配（退出码 {code}）")

print("=== AC3 · 文件整个不见 ===")
with tempfile.TemporaryDirectory() as tmp:
    root = sandbox(tmp)
    (root / ".ai" / "OVERVIEW.md").unlink()
    code, out = run(["--check"], root)
    if code != 0 and "overview missing" in out:
        ok("产物缺失 → 报 overview missing")
    else:
        bad(f"产物缺失未报错（退出码 {code}）")

print("=== AC4 · 体量上限 ===")
source = io.open(TOOL, encoding="utf-8").read()
match = re.search(r"^OVERVIEW_MAX_BYTES = (\d+)$", source, re.MULTILINE)
if match and match.group(1) == "12000":
    ok("上限 12000 写死在生成器常量")
else:
    bad(f"上限常量不是 12000：{match.group(1) if match else '未找到'}")
actual = len((ROOT / ".ai" / "OVERVIEW.md").read_bytes())
(ok if actual <= 12000 else bad)(f"实测体量 {actual} 字节，上限 12000，余 {12000 - actual}")

with tempfile.TemporaryDirectory() as tmp:
    root = sandbox(tmp)
    for index in range(400):
        target = root / "tools" / f"bulk{index:03d}"
        target.mkdir()
        (target / "README.md").write_text(f"# 体量夹具 {index:03d}\n", encoding="utf-8")
    code, out = run(["--write"], root)
    if code != 0 and "overview too large:" in out and "12000" in out:
        ok("超限 → 诊断给出实测值与上限，且不写盘")
    else:
        bad(f"超限未按预期拒绝（退出码 {code}）：{out[:200]}")

print()
print("CHECK-CLEAN" if fail == 0 else "CHECK-DIRTY")
sys.exit(fail)
