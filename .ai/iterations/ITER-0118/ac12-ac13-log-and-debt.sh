#!/usr/bin/env bash
# AC12 / AC13：§5.4 三项定序登记在场；debt 如实增减、原有条目未被误删
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

M=.ai/MILESTONE.md
grep -qF '复用 `inbox` 这个 id，不新开工作流' "$M" && ok "① 为什么复用 id 已登记" || bad "① 为什么复用 id 已登记"
grep -qF '必须动 R6 声明不碰的 `test_inbox_workflow.py`' "$M" && ok "② 为什么必须动那份测试、边界在哪已登记" || bad "② 已登记"
grep -qF '执行分流两条出口在自己仓里跑不通' "$M" && ok "③ 两条出口跑不通与沙箱折衷已登记" || bad "③ 已登记"
n=$(grep -c '^- 2026-08-20（R7' "$M" || true)
[ "$n" -ge 3 ] && ok "R7 条目共 ${n} 条（不少于 3）" || bad "R7 条目只有 ${n} 条"

D=.ai/debt.md
n=$(grep -c '^- \*\*' "$D" || true)
[ "$n" = "14" ] && ok "债务条目 12 → 14" || bad "债务条目应为 14，实为 ${n}"
grep -qF 'R7 后剩余范围已收窄' "$D" && ok "两份 inbox 真源那条已重新表述" || bad "两份 inbox 真源那条已重新表述"
grep -qF '跨文件写盘的回滚本身失败时仍会留半截态' "$D" && ok "新增：回滚可能失败" || bad "新增：回滚可能失败"
grep -qF '六条动作路径里只有两条被真实用过' "$D" && ok "新增：真实使用覆盖不足" || bad "新增：真实使用覆盖不足"
for keep in 'butler 仓自身不 dogfood 运行自己的 hook' '`/butler:upgrade` 从未在真实已部署项目上跑过' \
            '运行时观测缺位' '远端 required check 未启用' '人读文档里的工作流计数没有机器兜底' \
            '`/butler:loop` 的演进冻结没有机器兜底' '已部署项目里旧格式 `.ai/INBOX.md` 的迁移义务没人认领'; do
  grep -qF "$keep" "$D" && ok "原有条目仍在：${keep}" || bad "原有条目丢失：${keep}"
done
exit $fail
