#!/usr/bin/env python3
"""ITER-0117 两组扫描。

A 组查越界：本轮不该出现的东西，命中即失败。
B 组查在场：本轮该落地的东西，缺席即失败。

模式串一律用片段拼接，避免脚本自己命中自己。
"""
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
ITER = ROOT / ".ai/iterations/ITER-0117"
CONTRACT = ROOT / "Coder/40_Context_Management/intake-schema.md"

failures = []
notes = []


def fail(tag, msg):
    failures.append(f"[{tag}] {msg}")


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


# ---------------------------------------------------------------- A 组：越界
# 活跃接线面：真正会被宿主/工具/规则读到的目录与根级文档。
# 刻意排除 .ai/ 下的迭代产物（CONCEPT / AC_LIST / TECH_PLAN / MILESTONE），
# 那里讨论「R9 才改名」这件事本身，出现该路径是正确的，排除面在 VERIFY_REPORT 逐份摊开。
ACTIVE_DIRS = [
    "Coder", "templates", "tools", "scripts", "workflows",
    "plugins", ".claude", "docs", "migrations", "deliveries",
]
SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", ".pytest_cache"}
TEXT_SUFFIX = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".template", ".toml"}

FUTURE_DIR = ".ai/" + "backlog" + "/"   # R9 才存在的路径，本轮不得写进活跃面

scanned = 0
a1_hits = []
targets = []
for d in ACTIVE_DIRS:
    base = ROOT / d
    if not base.exists():
        continue
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_SUFFIX:
            continue
        targets.append(p)
for p in sorted(ROOT.glob("*.md")):
    targets.append(p)

for p in targets:
    try:
        text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    scanned += 1
    if FUTURE_DIR in text:
        a1_hits.append(str(p.relative_to(ROOT)))

notes.append(f"A1 扫描文本文件 {scanned} 份，覆盖 {len(ACTIVE_DIRS)} 个活跃目录 + 根级 *.md")
if a1_hits:
    fail("A1", f"活跃面出现 R9 才存在的孵化区路径：{a1_hits}")

contract_text = read("Coder/40_Context_Management/intake-schema.md")
OLD_ID_PREFIX = "SR" + "C-"
OLD_FIELDS = ["observed" + "_sha256", "processed" + "_sha256"]
if OLD_ID_PREFIX in contract_text:
    fail("A2", "新契约里出现了旧契约的编号前缀，等于把号池抄了过来")
for field in OLD_FIELDS:
    if field in contract_text:
        fail("A2", f"新契约里出现了旧契约的双指纹字段名 {field}")

baseline_p4 = {}
for line in (ITER / "pre-p4.baseline").read_text(encoding="utf-8").splitlines():
    if line.startswith("#") or not line.strip():
        continue
    digest, path = line.split(None, 1)
    baseline_p4[path.strip()] = digest

ledger = ".ai/MILESTONES.md"
if baseline_p4.get(ledger) != sha(ledger):
    fail("A3", "待办区索引 .ai/MILESTONES.md 被改动了——本轮明确一字不改（见 AC5 与 §5.3 修订记录）")

# ---------------------------------------------------------------- B 组：在场
legacy = {}
for line in (ITER / "legacy-inbox.baseline").read_text(encoding="utf-8").splitlines():
    if line.startswith("#") or not line.strip():
        continue
    digest, path = line.split(None, 1)
    legacy[path.strip()] = digest

drifted = [p for p, d in legacy.items() if sha(p) != d]
if drifted:
    fail("B1", f"旧 inbox 链被动了（本轮归 R8，应零改动）：{drifted}")
notes.append(f"B1 旧 inbox 链核对 {len(legacy)} 份，全部未变" if not drifted else "B1 有漂移")

# B2 生效时点声明三要素 + 三层骨架
DECL_MARKS = [
    "生效时点声明",
    "两份规则真源",
    "零写入",
    "一律以 `inbox-schema.md` 为准",
    "没有任何机器检查兜底",
]
for mark in DECL_MARKS:
    if mark not in contract_text:
        fail("B2", f"生效时点声明缺要素：{mark}")
if not re.search(r"^> \*\*⚠️ 生效时点声明", contract_text, re.M):
    fail("B2", "生效时点声明不在 H1 底下的引用块里")

for heading in ["## 1. 第一层 · 闪念口", "## 2. 第二层 · 孵化区", "## 3. 第三层 · 执行分流"]:
    if heading not in contract_text:
        fail("B3", f"新契约缺三层骨架：{heading}")

# B4 闪念状态：恰好四态封闭
状态段 = contract_text.split("### 1.4")[1].split("### 1.5")[0]
状态值 = re.findall(r"^\| `([a-z]+)` \|", 状态段, re.M)
if 状态值 != ["new", "incubated", "done", "dropped"]:
    fail("B4", f"闪念状态枚举不是预期的四态：{状态值}")

# B5 合法转移：恰好四条
转移段 = contract_text.split("### 1.5")[1].split("### 1.6")[0]
转移行 = re.findall(r"^\| `(\w+) → (\w+)` \|", 转移段, re.M)
预期转移 = [("new", "incubated"), ("new", "done"), ("new", "dropped"), ("incubated", "dropped")]
if 转移行 != 预期转移:
    fail("B5", f"合法转移不是预期的四条：{转移行}")
if "终态不回头" not in contract_text:
    fail("B5", "缺终态不回头的明文约束")

# B6 规模三档封闭
规模段 = contract_text.split("### 2.2")[1].split("### 2.3")[0]
规模值 = re.findall(r"^\| `([a-z]+)` \|", 规模段, re.M)
if 规模值 != ["milestone", "iteration", "undecided"]:
    fail("B6", f"规模档位不是预期的三档：{规模值}")

# B7 按档结构 + undecided 的出区压力
结构段 = contract_text.split("### 2.3")[1].split("### 2.4")[0]
for seg in ["范围评估 / 理解阐释 / 拆分路线图 / 范围演进记录", "要解决什么 / 暂缓原因", "想做什么 / 卡在哪"]:
    if seg not in 结构段:
        fail("B7", f"按档结构缺一档：{seg}")
if "点名一个具体缺口" not in contract_text:
    fail("B7", "undecided 档缺「卡在哪必须点名具体缺口」这条出区压力")

# B8 执行分流：恰好三条出口 + 两侧原子 + ideation 不是出口
出口段 = contract_text.split("### 3.1")[1].split("### 3.2")[0]
出口行 = re.findall(r"^\| (提升为里程碑|开为迭代|撤回) \|", 出口段, re.M)
if 出口行 != ["提升为里程碑", "开为迭代", "撤回"]:
    fail("B8", f"执行分流出口不是预期的三条：{出口行}")
if "不得直接出区" not in 出口段:
    fail("B8", "缺 undecided 不得直接出区的约束")
if "ideation（探索）不是出口" not in contract_text:
    fail("B8", "缺「ideation 是孵化手段不是出口」的明文")
if "两侧原子" not in contract_text or "milestones.backlog_set" not in contract_text:
    fail("B8", "缺两侧原子的约束或它的现成兜底指针")

# B9 路径写的是当下真实存在的落点 + R9 改名预告
if "`.ai/milestone-backlog/`" not in contract_text:
    fail("B9", "新契约没写当前真实的孵化区路径")
if "R9" not in contract_text or "改名" not in contract_text:
    fail("B9", "新契约没预告 R9 会改名、届时同批更新")

# B10 9 份草稿的规模字段
drafts = sorted((ROOT / ".ai/milestone-backlog").glob("*.md"))
if len(drafts) != 9:
    fail("B10", f"孵化区草稿数应为 9，实为 {len(drafts)}")
for d in drafts:
    text = d.read_text(encoding="utf-8")
    for marker, want in [("候办键: ", 1), ("候办状态: deferred", 1), ("规模: milestone", 1)]:
        if text.count(marker) != want:
            fail("B10", f"{d.name} 的标记 {marker!r} 出现 {text.count(marker)} 次，应为 {want}")

# B11 milestone-schema §4.5 两条改到位，索引表模板与 §5 未动
ms = read("Coder/20_Workflow_Lifecycle/milestone-schema.md")
sec45 = ms.split("### 4.5")[1].split("## 5. 里程碑工作区")[0]
if "一次 `规模: milestone|iteration|undecided`" not in sec45:
    fail("B11", "§4.5 草稿头部标记没扩为三项")
if "按 `规模` 分档" not in sec45 or "intake-schema.md" not in sec45:
    fail("B11", "§4.5 的四段强制没改为按档，或没给新契约指针")
if "| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |" not in sec45:
    fail("B11", "§4.5 的 5 列索引表模板被动过")
for h in ["### 5.1 范围评估", "### 5.2 理解阐释", "### 5.3 拆分路线图", "### 5.4 范围演进记录"]:
    if h not in ms:
        fail("B11", f"§5 的四段标题缺失：{h}")

# B12 README 两处注册
readme = read("Coder/README.md")
if readme.count("\n    intake-schema.md\n") != 1:
    fail("B12", "README 目录结构树里没有恰好一条新文件注册")
if readme.count("- `40_Context_Management/intake-schema.md`") != 1:
    fail("B12", "README 读取顺序的逐文件指针里没有恰好一条新文件说明")

# B13 debt 10 → 12，原 10 条逐条仍在
debt = read(".ai/debt.md")
titles = re.findall(r"^- \*\*(.+?)\*\*", debt, re.M)
if len(titles) != 12:
    fail("B13", f"debt 条目数应为 12，实为 {len(titles)}")
BEFORE_10 = [
    "butler 仓自身不 dogfood 运行自己的 hook",
    "项目自有 hook 与 Butler 受管目录不能共存",
    "`/butler:upgrade` 从未在真实已部署项目上跑过",
    "运行时观测缺位",
    "远端 required check 未启用",
    "双宿主语义入口未经真实安装人测",
    "`.ai/invariants.md` 有 16 条不带真源指针",
    "`iteration-schema.md §5.3` 的修订记录要求与产物合同冲突",
    "人读文档里的工作流计数没有机器兜底",
    "`/butler:loop` 的演进冻结没有机器兜底",
]
if titles[:10] != BEFORE_10:
    fail("B13", "原 10 条欠账被动过（顺序或标题不符）")
NEW_2 = ["两份 inbox 规则真源并存，没有机器兜底", "已部署项目里旧格式 `.ai/INBOX.md` 的迁移义务没人认领"]
if titles[10:] != NEW_2:
    fail("B13", f"新增两条欠账不符：{titles[10:]}")

# B14 MILESTONE.md §5.4 恰好三条 R6 登记
mile = read(".ai/MILESTONE.md")
r6 = re.findall(r"^- 2026-08-20（R6 · ", mile, re.M)
if len(r6) != 3:
    fail("B14", f"§5.4 的 R6 登记应为 3 条，实为 {len(r6)}")

# ---------------------------------------------------------------- 输出
for n in notes:
    print("note:", n)
if failures:
    print(f"\nFAIL {len(failures)} 条：")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print(f"\nPASS  A 组零命中 · B 组零缺席（扫描 {scanned} 份文本文件）")
