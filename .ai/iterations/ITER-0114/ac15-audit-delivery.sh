#!/usr/bin/env bash
# ITER-0114 · AC15：状态审计干净，交付总结如实记下那项覆盖面事实。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

D=deliveries/ITER-0114-project-overview-rebuild

echo "=== AC15 · 状态审计 ==="
python3 scripts/audit-project-state.py --project-root . --allow-unreleased > /tmp/iter0114-audit.log 2>&1
code=$?
if [ "$code" = 0 ]; then ok "audit-project-state.py --allow-unreleased 退出码 0"; else bad "审计退出码 ${code}"; fi
echo "       —— 非 [OK] 行 ——"
grep -v '^\[OK\]' /tmp/iter0114-audit.log | sed 's/^/       /'
unreleased=$(grep -c '^\[UNRELEASED\]' /tmp/iter0114-audit.log)
drift=$(grep -c '^\[DRIFT\]\|^\[ERROR\]\|^\[FAIL\]' /tmp/iter0114-audit.log)
if [ "$unreleased" = 2 ]; then ok "两条 UNRELEASED 亮牌（发布态，非漂移）"; else bad "UNRELEASED 亮牌 ${unreleased} 条，不是 2 条"; fi
if [ "$drift" = 0 ]; then ok "零 DRIFT / ERROR"; else bad "仍有 ${drift} 条 DRIFT / ERROR"; fi

echo "=== AC15 · 交付总结双格式在位 ==="
[ -f "${D}.md" ]   && ok "${D}.md 在位（$(wc -c < "${D}.md" | tr -d ' ') 字节）"   || bad "${D}.md 缺失"
[ -f "${D}.html" ] && ok "${D}.html 在位（$(wc -c < "${D}.html" | tr -d ' ') 字节）" || bad "${D}.html 缺失"
if grep -q '{{' "${D}.html"; then bad "HTML 里还剩未填的占位符"; else ok "HTML 占位符全部填好"; fi
if grep -q 'ROADMAP' "${D}.html"; then bad "迭代级交付不该留 ROADMAP 块"; else ok "ROADMAP 块按迭代级删除"; fi
if grep -qE 'https?://|<link |<script ' "${D}.html"; then bad "HTML 引了外部资源，破坏离线自包含"; else ok "HTML 单文件自包含，无外链"; fi

echo "=== AC15 · 覆盖面事实如实记录 ==="
need() { grep -qF -- "$1" "${D}.md" && ok "$2" || bad "$2（缺）"; }
need '证明不了「这份全貌被任何会话读过」' "写明 --check 证不了「被读过」"
need '生成段与机器源头一致'               "写明 --check 只能证明生成段与源头一致"
need 'R11'                                "写明这半个证明要等 R11 的运行时观测"
need '不在冷启动必读路径上'               "写明它不在必读路径上，可能永远不被打开"

echo "=== AC15 · 估数与实测的差如实记下 ==="
need '不少于 9 条'   "记下方案里的估数 9"
need '10 个测试方法覆盖 11 个负例场景' "记下实测 10 方法 / 11 场景"
need '没有回头改方案' "写明没有回头改方案"

echo "=== AC15 · 两条 amend 如实记下 ==="
need '§5.3' "写明 amend 走的是 iteration-schema.md §5.3"
need '实际 22' "记下 AC2 的计数错与更正"
need '零活引用' "记下 AC12 的口径修订"

echo "=== AC15 · 引用只给路径、不嵌四件套全文 ==="
refs=$(awk '/^## 引用/,0' "${D}.md" | grep -c '^- `')
if [ "$refs" -ge 6 ]; then ok "引用段 ${refs} 条路径指针"; else bad "引用段只有 ${refs} 条"; fi
if grep -q '^## Acceptance Checklist\|^## Design Decisions\|^## Goal' "${D}.md"; then
  bad "交付总结里嵌了四件套章节全文"
else
  ok "没有嵌四件套全文"
fi

echo
[ "$fail" = 0 ] && echo "AUDIT-DELIVERY-CLEAN" || echo "AUDIT-DELIVERY-DIRTY"
exit "$fail"
