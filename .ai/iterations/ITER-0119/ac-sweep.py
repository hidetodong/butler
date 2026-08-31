#!/usr/bin/env python3
"""ITER-0119（MILE-0016 R8）的可重跑验收扫描。

两组断言，缺一不可：
- **A 组 · 残留**：旧 inbox 全链与 `origin/` 这个目录名在活跃面必须零命中。
- **B 组 · 在场**：这轮该活下来的东西必须还在——新契约与新工具的接线、
  用户原件只读那条纪律、部署只建两个目录、剩余测试用例、hook 树摘要、
  以及 `.ai/INBOX.md` 里那条真实闪念行逐字节未动。

只查 A 组会犯一个很隐蔽的错：把纪律连同旧目录一起删掉，扫描一样零命中、
看起来很干净，实际上把一条真规矩弄丢了。所以 B 组和 A 组同等重要。

用法：python3 .ai/iterations/ITER-0119/ac-sweep.py
退出码 0 = 全过；1 = 有失败项，逐条列出。
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------- 扫描面
# A 组扫的是**「教人怎么做事」的那一面**：规则、人读文档、命令与 skill 薄壳、
# 工具代码、测试与 CI 脚本、工作流注册表。这一面上出现旧链名字或 `origin/`，
# 就是一条指向不存在东西的死引用，必须零命中。
#
# 明确不在 A 组扫描面内的两类，理由都写死在这里：
# 1. `.ai/` 整个目录是**本项目自己的台账与工作记录**（迭代四件套、里程碑范围、
#    欠债、运行状态、冷分片）。它们要能说清「这轮退役了什么」，就必然得叫出
#    旧东西的名字；把它们一起改写，等于让记录描述不了自己在做什么。同理还有
#    `CHANGELOG.md`、`migrations/`、`deliveries/`、`docs/research/`——都是记述。
#    代价是 `.ai/` 里真出现死引用扫不到，所以 B 组逐条钉住了 `.ai/` 里
#    真正要紧的几处（不变量第 48 条、OVERVIEW 计数、INBOX 字节）。
# 2. `tools/intake/tests/test_intake.py` 里那份旧格式夹具。它是**负向测试资产**，
#    整份存在的意义就是「拿一份长得像旧契约的文件喂进去，证明工具会拒绝且零写入」，
#    里面必须有 SRC-0001、双指纹字段和旧的受管区块标记。B 组反过来钉住它还在，
#    免得有人为了让 A 组变绿把夹具掏空。
SCAN_ROOTS = (
    "Coder/", "templates/", ".claude/", "plugins/", "scripts/", "tools/",
    "workflows/", "docs/",
)
SCAN_ROOT_FILES = ("README.md", "HUMAN_GUIDE.md", "CLAUDE.md", "AGENTS.md")
SCAN_EXCLUDED = (
    "docs/research/",                      # 预研记录，结论未冻结也不回写
    "tools/intake/tests/test_intake.py",   # 旧格式负向夹具，见上文第 2 条
    "__pycache__/", ".pytest_cache/",
)

SCANNED_SUFFIXES = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".toml"}

# 字面串拼出来，免得这个脚本自己命中自己。
FRAG = {
    "inbox_schema":   "inbox" + "-schema",
    "inbox_workflow": "inbox" + "-workflow",
    "tools_inbox":    "tools/" + "inbox",
    "dotted_inbox":   "tools." + "inbox",
    "origin_dir":     "orig" + "in/",
    "src_id":         re.compile(r"SRC-" + r"[0-9]{4}"),
    "observed":       "observed" + "_sha256",
    "processed":      "processed" + "_sha256",
}

failures: list[str] = []
notes: list[str] = []


def live_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(ROOT).as_posix()
        in_scope = rel in SCAN_ROOT_FILES or any(rel.startswith(p) for p in SCAN_ROOTS)
        if not in_scope:
            continue
        if any(rel == p or rel.startswith(p) or f"/{p}" in f"/{rel}" for p in SCAN_EXCLUDED):
            continue
        if path.suffix not in SCANNED_SUFFIXES:
            continue
        yield rel, path


LIVE = list(live_files())


def scan_absent(label: str, needle) -> None:
    hits = []
    for rel, path in LIVE:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if isinstance(needle, re.Pattern):
            found = [n for n, line in enumerate(text.splitlines(), 1) if needle.search(line)]
        else:
            found = [n for n, line in enumerate(text.splitlines(), 1) if needle in line]
        # git 的 remote 叫 origin，`origin/main` 之类不是本轮的目录名
        if needle == FRAG["origin_dir"]:
            found = [
                n for n in found
                if not re.search(r"(remotes/origin/|push origin/|origin/(main|HEAD)\b)",
                                 text.splitlines()[n - 1])
            ]
        hits.extend(f"{rel}:{n}" for n in found)
    if hits:
        failures.append(f"[A 组] {label} 仍有 {len(hits)} 处命中：{', '.join(hits[:8])}")
    else:
        notes.append(f"[A 组] {label} 零命中（扫了 {len(LIVE)} 份活跃文件）")


def expect_text(rel: str, needle: str, label: str) -> None:
    path = ROOT / rel
    if not path.exists():
        failures.append(f"[B 组] {label}：文件不存在 {rel}")
        return
    if needle not in path.read_text(encoding="utf-8"):
        failures.append(f"[B 组] {label}：{rel} 里找不到「{needle}」")
    else:
        notes.append(f"[B 组] {label} ✓ {rel}")


def expect_absent_path(rel: str, label: str) -> None:
    if (ROOT / rel).exists():
        failures.append(f"[B 组] {label}：{rel} 本应已删除，仍然存在")
    else:
        notes.append(f"[B 组] {label} ✓ {rel} 已不存在")


# ---------------------------------------------------------------- A 组 · 残留
for key in ("inbox_schema", "inbox_workflow", "tools_inbox", "dotted_inbox",
            "origin_dir", "src_id", "observed", "processed"):
    scan_absent(key, FRAG[key])

# ---------------------------------------------------------------- B 组 · 在场
# 1. 旧链实体确实没了
for rel in ("Coder/40_Context_Management/inbox-schema.md",
            "Coder/40_Context_Management/inbox-workflow.md",
            "templates/hooks/tests/test_inbox_contract.py",
            "tools/inbox"):
    expect_absent_path(rel, "旧链实体已删")

# 2. 新契约与新工具三处接线仍在
expect_text("workflows/registry.json",
            '"rule_source": "Coder/40_Context_Management/intake-workflow.md"',
            "注册表 inbox 条目指新契约")
expect_text(".claude/commands/butler/inbox.md", "tools/intake/", "Claude 薄壳指新工具")
expect_text("plugins/butler/skills/butler-inbox/SKILL.md", "tools/intake/", "Codex skill 指新工具")

# 3. 用户原件只读纪律仍在，且已绑到新位置
expect_text("Coder/40_Context_Management/references-schema.md",
            "`.ai/references/raw/` 用户原稿不因 PRD 集合而被改写、移动或删除",
            "非回归门那条纪律（逐字，与合同测试配对）")
expect_text("templates/hooks/tests/test_prd_collection_contract.py",
            "`.ai/references/raw/` 用户原稿不因 PRD 集合而被改写、移动或删除",
            "合同测试那条逐字断言")
expect_text("Coder/20_Workflow_Lifecycle/mcv-deployment.md",
            "只读、不写不改不重命名不移动不归档不删除",
            "部署协议里的只读纪律")
expect_text(".ai/invariants.md", "`.ai/references/raw/` 里的材料归用户",
            "不变量第 48 条已改写、纪律未丢")

# 4. 部署只建两个目录，四处说法一致
expect_text("Coder/20_Workflow_Lifecycle/mcv-deployment.md",
            "`.ai/` 与 `deliveries/` 两类基础目录", "部署协议：两个目录")
expect_text("Coder/README.md", "只在已解析项目根创建 `.ai/` 与 `deliveries/` 两个目录",
            "Coder/README：两个目录")
expect_text(".claude/commands/butler/init.md", "创建 `.ai/` 与 `deliveries/` 两个目录",
            "init 命令：两个目录")
expect_text("plugins/butler/skills/butler-init/SKILL.md",
            "create `.ai/` and `deliveries/`", "init skill：两个目录")
expect_text("templates/rule-card.md", "只在该项目根创建 `.ai/`、`deliveries/` 与双宿主入口",
            "规则卡：两个目录")

# 5. test_inbox_workflow.py 只剩两个活接线用例
wf = (ROOT / "templates/hooks/tests/test_inbox_workflow.py").read_text(encoding="utf-8")
defs = re.findall(r"^def (test_\w+)", wf, re.M)
if defs != ["test_inbox_is_registered_for_both_hosts",
            "test_host_entries_are_thin_and_resolve_project_root"]:
    failures.append(f"[B 组] test_inbox_workflow.py 用例集不对：{defs}")
else:
    notes.append("[B 组] test_inbox_workflow.py 只剩两个活接线用例 ✓")

# 6. 旧格式回归防线在场
expect_text("tools/intake/tests/test_intake.py",
            "class TestLegacyInboxIsRefusedNotRewritten", "旧格式回归防线")
# 夹具本身不许被掏空——A 组把这份文件排除在外，就得由 B 组守住它
for marker, label in (
    ("butler-inbox:managed:start", "旧受管区块标记"),
    ("SRC-" + "0001", "旧的递增来源号"),
    ("observed" + "_sha256", "旧的双指纹字段"),
):
    expect_text("tools/intake/tests/test_intake.py", marker, f"夹具仍含{label}")

# 7. hook 树摘要与开工前逐字节相同
# 口径必须与 `tools/butler-upgrade/upgrade.py` 的 skip_hook_file() 逐条一致，
# 否则算出来的摘要跟升级器对不上，比对结论没有意义。
NON_DEPLOYED_HOOK_FILES = frozenset({"conftest.py", "pytest.ini"})


def hook_digest() -> str:
    root = ROOT / "templates" / "hooks"
    files = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_file() or path.is_symlink():
            continue
        parts = rel.parts
        if "tests" in parts or "__pycache__" in parts or ".pytest_cache" in parts:
            continue
        if rel.suffix == ".pyc":
            continue
        if rel.as_posix() in NON_DEPLOYED_HOOK_FILES:
            continue
        files[rel] = path.read_bytes()
    digest = hashlib.sha256()
    for rel, content in sorted(files.items(), key=lambda kv: kv[0].as_posix()):
        digest.update(rel.as_posix().encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


BASELINE_HOOK_DIGEST = "bd92a614f9582451ec3150d2c1113a2262bb874b97fd085adf6ad0ce7c91e56d"
actual = hook_digest()
if actual != BASELINE_HOOK_DIGEST:
    failures.append(f"[B 组] hook 树摘要变了：{actual} != {BASELINE_HOOK_DIGEST}")
else:
    notes.append(f"[B 组] hook 树摘要与开工前相同 ✓ {actual[:12]}…")

# 8. .ai/INBOX.md 那条真实闪念行逐字节未动
BASELINE_INBOX_SHA = "b27e04da72db4f6b00f89b4a0181fba54315d486256b0ec5903fc61a8ffd027e"
inbox_sha = hashlib.sha256((ROOT / ".ai/INBOX.md").read_bytes()).hexdigest()
if inbox_sha != BASELINE_INBOX_SHA:
    failures.append(f"[B 组] .ai/INBOX.md 被改过：{inbox_sha} != {BASELINE_INBOX_SHA}")
else:
    notes.append("[B 组] .ai/INBOX.md 逐字节未动 ✓")

# 9. 40_Context_Management 规则文件 13 → 11，OVERVIEW 已同步
rule_count = len(list((ROOT / "Coder/40_Context_Management").glob("*.md")))
if rule_count != 11:
    failures.append(f"[B 组] 40_Context_Management 规则文件数 = {rule_count}，应为 11")
else:
    notes.append("[B 组] 40_Context_Management 规则文件数 13 → 11 ✓")
expect_text(".ai/OVERVIEW.md", "| `40_Context_Management/` | 11 |", "OVERVIEW 计数已重算")

# ---------------------------------------------------------------- 汇报
for line in notes:
    print(line)
if failures:
    print()
    for line in failures:
        print("FAIL " + line)
    print(f"\n{len(failures)} 项失败。")
    sys.exit(1)
print(f"\nAC-SWEEP PASS · A 组 8 项零命中 / B 组 {len(notes) - 8} 项在场（扫描面 {len(LIVE)} 份文件）。")
