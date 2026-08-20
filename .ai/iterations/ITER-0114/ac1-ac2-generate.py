#!/usr/bin/env python3
"""ITER-0114 · AC1 / AC2：生成器读的是真源头，生成的每节数字与源头实测一致。

AC1 查「五个源头是不是真的在读」——删掉任一个，生成器必须指名报错且不产出残缺页。
AC2 查「生成出来的数字对不对」——逐节拿生成结果和源头对数，不是只看页面存在。
"""
import io
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOL = ROOT / "scripts" / "sync-project-overview.py"
OVERVIEW = ROOT / ".ai" / "OVERVIEW.md"

fail = 0


def ok(msg):
    print(f"[OK]   {msg}")


def bad(msg):
    global fail
    fail = 1
    print(f"[FAIL] {msg}")


def run(args, cwd=None):
    proc = subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, cwd=cwd)
    return proc.returncode, proc.stdout + proc.stderr


print("=== AC1 · CLI 形状 ===")
code, out = run(["--project-root", str(ROOT)])
if code != 0 and "one of the arguments" in out:
    ok("--check / --write 缺一必报错")
else:
    bad(f"缺动作参数未报错（退出码 {code}）")
code, out = run(["--check", "--write", "--project-root", str(ROOT)])
if code != 0 and "not allowed with argument" in out:
    ok("--check 与 --write 互斥")
else:
    bad(f"互斥未生效（退出码 {code}）")

print("=== AC1 · 五个源头真的在读，缺一即拒绝出页 ===")
COPY = (".ai", "Coder", "workflows", "tools", "scripts", "VERSION")
CASES = [
    ("VERSION", "VERSION"),
    (".ai/ITERATIONS.md", ".ai/ITERATIONS.md"),
    (".ai/MILESTONES.md", ".ai/MILESTONES.md"),
    ("Coder/README.md", "Coder/README.md"),
    ("workflows/registry.json", "workflows/registry.json"),
]
for relative, needle in CASES:
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / "repo"
        root.mkdir()
        for item in COPY:
            src = ROOT / item
            dst = root / item
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(src, dst)
        (root / ".ai" / "OVERVIEW.md").unlink(missing_ok=True)
        (root / relative).unlink()
        code, out = run(["--write", "--project-root", str(root)])
        produced = (root / ".ai" / "OVERVIEW.md").exists()
        if code != 0 and f"missing source: {needle}" in out and not produced:
            ok(f"删 {relative} → 指名报错且未产出残缺页")
        else:
            bad(f"删 {relative} 未按预期失败（退出码 {code}，产出={produced}）：{out[:200]}")

with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp) / "repo"
    root.mkdir()
    for item in COPY:
        src = ROOT / item
        dst = root / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    shutil.rmtree(root / "tools")
    code, out = run(["--write", "--project-root", str(root)])
    if code != 0 and "missing source: tools/" in out:
        ok("删 tools/ → 指名报错")
    else:
        bad(f"删 tools/ 未按预期失败（退出码 {code}）")

print("=== AC2 · 页首与结构 ===")
text = io.open(OVERVIEW, encoding="utf-8").read()
for needle in ("请勿手改", "scripts/sync-project-overview.py --write"):
    (ok if needle in text else bad)(f"页首含「{needle}」")
if "<!-- user-managed" not in text and "{{" not in text:
    ok("全文无手写槽位与占位符")
else:
    bad("页面里出现了手写槽位或占位符")
titles = re.findall(r"^## (.+)$", text, re.MULTILINE)
expected = ["版本与当前状态", "里程碑时间线", "规则体系目录与职责", "工作流清单", "驻留工具清单"]
(ok if titles == expected else bad)(f"五节齐全且有序：{titles}")

print("=== AC2 · 每节数字与机器源头实测一致 ===")
version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
(ok if f"规则源版本：**{version}**" in text else bad)(f"版本号与 VERSION 一致（{version}）")

milestones = (ROOT / ".ai/MILESTONES.md").read_text(encoding="utf-8")
mile_rows = [l for l in milestones.split("\n") if re.match(r"^\| MILE-\d{4,} \|", l)]
page_rows = [l for l in text.split("\n") if re.match(r"^\| MILE-\d{4,} \|", l)]
(ok if len(mile_rows) == len(page_rows) else bad)(
    f"里程碑行数与台账一致（台账 {len(mile_rows)} / 页面 {len(page_rows)}）")

registry = json.loads((ROOT / "workflows/registry.json").read_text(encoding="utf-8"))
wf_rows = [l for l in text.split("\n") if re.match(r"^\| [a-z0-9-]+ \| `/butler", l)]
(ok if len(wf_rows) == len(registry["workflows"]) else bad)(
    f"工作流行数与 registry 一致（registry {len(registry['workflows'])} / 页面 {len(wf_rows)}）")

tool_dirs = sorted(p.name for p in (ROOT / "tools").iterdir() if p.is_dir())
tool_rows = re.findall(r"^\| `tools/([^/]+)/` \|", text, re.MULTILINE)
(ok if tool_rows == tool_dirs else bad)(
    f"驻留工具清单与 tools/ 一致（{len(tool_dirs)} 项）")

coder_dirs = sorted(p.name for p in (ROOT / "Coder").iterdir() if p.is_dir())
rule_rows = re.findall(r"^\| `([0-9]{2}_[A-Za-z_]+)/` \| (\d+) \|", text, re.MULTILINE)
(ok if [n for n, _ in rule_rows] == coder_dirs else bad)(
    f"规则目录清单与 Coder/ 一致（{len(coder_dirs)} 个）")
bad_counts = [n for n, c in rule_rows if int(c) != len(list((ROOT / "Coder" / n).glob("*.md")))]
(ok if not bad_counts else bad)(f"各目录规则文件数实测一致{'' if not bad_counts else '，不符：' + str(bad_counts)}")

print()
print("GENERATE-CLEAN" if fail == 0 else "GENERATE-DIRTY")
sys.exit(fail)
