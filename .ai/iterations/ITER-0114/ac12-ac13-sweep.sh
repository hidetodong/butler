#!/usr/bin/env bash
# ITER-0114 · AC12 残留扫描 + AC13 前提修正登记核对
# 查的是**活引用**——把 `.ai/project/invariants.md` / `frontier.md` 当作现存产物去读、去写、
# 或要求读取。**叙述性提及**（迁出留痕、设计理由、历史记录）不算残留，反而必须留着，
# 否则这些欠债和判断就没了出处；每一处都在下面的白名单里注明理由。
#
# 扫描面排除五类，每类都有理由：
#   .ai/iterations/ .ai/history/ deliveries/  —— 历史归档，按纪律不追改
#   migrations/                               —— 已发布的迁移配方冻结，改了 manifest 一致性校验会红
#   .venv/                                    —— 第三方依赖，不是本仓内容
#   .ai/ 工作区五件套与状态文件               —— 本迭代产物正在描述这次迁移本身，必然提到旧路径
set -uo pipefail
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

scan() {
  grep -rn "$1" --include='*.md' --include='*.py' --include='*.json' --include='*.sh' --include='*.template' . 2>/dev/null \
    | grep -v '^\./\?\.git/' \
    | grep -v '^\./\?\.ai/iterations/' \
    | grep -v '^\./\?\.ai/history/' \
    | grep -v '^\./\?deliveries/' \
    | grep -v '^\./\?migrations/' \
    | grep -v '^\./\?\.ai/CONCEPT\.md' \
    | grep -v '^\./\?\.ai/AC_LIST\.md' \
    | grep -v '^\./\?\.ai/TECH_PLAN\.md' \
    | grep -v '^\./\?\.ai/VERIFY_REPORT\.md' \
    | grep -v '^\./\?\.ai/01_CHANGELOG\.md' \
    | grep -v '^\./\?\.ai/MILESTONE\.md' \
    | grep -v '^\./\?\.ai/task-state\.md' \
    | grep -v '^\./\?\.ai/02_SESSION_HANDOFF\.md' \
    | grep -v '^\./\?\.ai/handoff-state\.json'
}

echo "=== 旧路径的活引用（叙述性提及见白名单）==="
# 白名单：允许出现旧文件名的叙述性位置，逐处理由。
#   scripts/sync-project-overview.py            —— 模块 docstring 讲设计由来：为什么要按性质分家
#   Coder/40_Context_Management/context-persistence.md —— 规则正文解释「整体覆写为什么会停」
#   .ai/invariants.md                           —— 不变量条目把它当作规律的实测证据
#   .ai/debt.md                                 —— 每条迁来的欠债都要注明出处
#   .ai/RUN_LOG.md / .ai/milestone-backlog/ / .ai/milestones/ —— 历史运行记录与旧候办，不追改
NARRATIVE='scripts/sync-project-overview\.py|Coder/40_Context_Management/context-persistence\.md|\.ai/invariants\.md|\.ai/debt\.md|\.ai/RUN_LOG\.md|\.ai/milestone-backlog/|\.ai/milestones/'
for pat in '\.ai/project/invariants\.md' '\.ai/project/frontier\.md'; do
  hits="$(scan "$pat" | grep -Ev "$NARRATIVE")"
  if [ -z "$hits" ]; then ok "零活引用：$pat"; else bad "仍有活引用：$pat"; echo "$hits" | cut -c1-160; fi
done

# `.ai/project/workspaces.md` 的引用**有意不动**：那是目标项目侧 PRD / 工作区机制的规格落点，
# 与本轮退役的知识文件夹同目录但不同机制，去留归 R9（已在 .ai/MILESTONE.md §5.4 登记）。
ws="$(scan '\.ai/project/workspaces\.md' | wc -l | tr -d ' ')"
[ "$ws" -gt 0 ] && ok "workspaces.md 规格引用按 Out of Scope 保留（$ws 处）" || bad "workspaces.md 规格引用意外消失"

echo "=== 白名单各处确有叙述性提及（不是白名单空转）==="
for f in scripts/sync-project-overview.py Coder/40_Context_Management/context-persistence.md .ai/debt.md; do
  grep -q 'frontier' "$f" && ok "$f 保留了出处说明" || bad "$f 的出处说明丢了"
done

echo "=== 目录已移除 ==="
[ ! -e .ai/project ] && ok ".ai/project/ 不存在" || bad ".ai/project/ 仍在"
[ -f .ai/invariants.md ] && ok ".ai/invariants.md 在位" || bad ".ai/invariants.md 缺失"
[ -f .ai/OVERVIEW.md ] && ok ".ai/OVERVIEW.md 在位" || bad ".ai/OVERVIEW.md 缺失"

echo "=== 注册与说明在场 ==="
grep -q 'sync-project-overview.py' Coder/README.md && ok "Coder/README.md 已注册生成器" || bad "Coder/README.md 未注册"
grep -q 'sync-project-overview.py --write' Coder/40_Context_Management/context-persistence.md && ok "context-persistence.md 写了重算命令" || bad "context-persistence.md 缺重算命令"
grep -q '一份只装一种' Coder/40_Context_Management/context-persistence.md && ok "context-persistence.md 写了性质分工" || bad "context-persistence.md 缺性质分工"

echo "=== AC13 · MILESTONE §5.4 的两条前提修正登记 ==="
S54=$(awk '/^#+ .*5\.4/{f=1} f' .ai/MILESTONE.md)
need() {
  if printf '%s\n' "${S54}" | grep -qF -- "$1"; then ok "$2"; else bad "$2（缺）"; fi
}
need '2026-08-19（R3 · 前提修正一 · `frontier.md`）' "登记一在场：frontier.md 前提修正"
need 'commit `0cf01e9`' "  实测证据：停更在 ITER-0111 的 commit 号"
need '正文写「版本 v3.5.1」' "  实测证据：正文版本号与实际不符"
need '整体覆写只在有东西强制触发重写时才活得下来' "  修正后的规律写清楚了"
need '2026-08-19（R3 · 前提修正二 · `invariants.md`）' "登记二在场：invariants.md 前提修正"
need '「收口是原子仪式」仍写五步' "  实测证据：第 47 行那条已假"
need '「冷启动读序固定」仍写旧四步' "  实测证据：第 42 行那条已假"
need '16 条完全不带真源指针' "  实测证据：16 条无指针"
need '纯追加只保证「新条目不覆盖旧条目」，不保证「旧条目描述的东西没变」' "  修正后的规律写清楚了"
need 'R3 · 发布处置追记' "追记在场：R3 再动两份部署入口模板，[regen-entrypoints] 要求不变"
need '去留归 **R9**' "追记写明 .ai/project/ 这个名字的去留归 R9"

echo
[ "$fail" = "0" ] && echo "SWEEP-CLEAN" || echo "SWEEP-DIRTY"
exit "$fail"
