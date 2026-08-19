#!/usr/bin/env python3
"""AC2：五处读序块 sha256 全等 + 部署入口渲染后仍字节一致。"""
import hashlib, io, subprocess, sys, tempfile

BEGIN = "<!-- butler-context-order:begin -->"
END = "<!-- butler-context-order:end -->"
SRC = "Coder/40_Context_Management/context-persistence.md"
PROJ = ["AGENTS.md", "Coder/README.md",
        "templates/AGENTS.md.template", "templates/CLAUDE.md.template"]
fail = 0


def block(path):
    s = io.open(path, encoding="utf-8").read()
    assert s.count(BEGIN) == 1 and s.count(END) == 1, path
    return s.split(BEGIN, 1)[1].split(END, 1)[0]


src = block(SRC)
digest = hashlib.sha256(src.encode()).hexdigest()
print(f"[OK]   真源 {SRC} sha256={digest[:16]} bytes={len(src.encode())}")
for p in PROJ:
    d = hashlib.sha256(block(p).encode()).hexdigest()
    if d == digest:
        print(f"[OK]   投影一致：{p}")
    else:
        print(f"[FAIL] 投影不一致：{p} sha256={d[:16]}")
        fail = 1

tpl = io.open("templates/CLAUDE.md.template", encoding="utf-8").read()
if "## 会话起始：恢复项目状态" in tpl and tpl.index("## 会话起始") < tpl.index(BEGIN):
    print("[OK]   CLAUDE 模板的读序块位于新增「会话起始：恢复项目状态」章节下")
else:
    print("[FAIL] CLAUDE 模板章节缺失或块不在其后")
    fail = 1

# 渲染一次真实部署入口，确认两个宿主拿到的仍是同一份字节
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["python3", "scripts/render-project-entrypoints.py",
                    "--target", d, "--butler-root", "."],
                   check=True, capture_output=True)
    for name in ("CLAUDE.md", "AGENTS.md"):
        s = io.open(f"{d}/{name}", encoding="utf-8").read()
        if s.count(BEGIN) == 1 and s.split(BEGIN, 1)[1].split(END, 1)[0] == src:
            print(f"[OK]   渲染后的部署入口 {name} 读序块与真源逐字节相同")
        else:
            print(f"[FAIL] 渲染后的部署入口 {name} 读序块失配")
            fail = 1

print()
print("AC2-CLEAN" if not fail else "AC2-DIRTY")
sys.exit(fail)
