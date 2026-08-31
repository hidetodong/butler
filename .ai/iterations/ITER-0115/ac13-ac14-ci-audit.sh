#!/usr/bin/env bash
# ITER-0115 · AC13/AC14：§5.4 两条登记在场；完整 CI 绿；状态审计非 OK 行只剩发布态亮牌与历史诊断留存。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }
need() { grep -qF -- "$1" "$2" && ok "$3" || bad "$3（缺）"; }

echo "=== AC13 · MILESTONE.md §5.4 两条登记 ==="
M=.ai/MILESTONE.md
need 'R4 · 路线图点名两项不存在' "$M" "登记一：路线图点名两项不存在"
need 'rule_source'               "$M" "登记一写明 registry 的 rule_source 指回命令自身"
need 'templates/rule-card.md'    "$M" "登记一写明 rule-card 全文未提"
need '如实记为不适用'            "$M" "登记一表态：不适用，不假装完成"
need 'R4 · 发布处置登记'         "$M" "登记二：发布处置"
need '[global-install]'          "$M" "登记二写明 Codex 侧需要 [global-install]"
need '[regen-entrypoints]'       "$M" "登记二写明本轮不触发 [regen-entrypoints]"
need 'R15'                       "$M" "登记二写明归 R15"

echo "=== AC14 · 完整 CI ==="
bash scripts/verify-ci.sh > "${TMPDIR:-/tmp}/iter0115-ci.log" 2>&1
ci=$?
if [ "$ci" = 0 ]; then ok "bash scripts/verify-ci.sh 退出码 0"; else bad "verify-ci.sh 退出码 ${ci}"; fi
echo "       —— CI 末 12 行 ——"
tail -12 "${TMPDIR:-/tmp}/iter0115-ci.log" | sed 's/^/       /'

echo "=== AC14 · 状态审计 ==="
python3 scripts/audit-project-state.py --project-root . --allow-unreleased > "${TMPDIR:-/tmp}/iter0115-audit.log" 2>&1
au=$?
if [ "$au" = 0 ]; then ok "audit-project-state.py --allow-unreleased 退出码 0"; else bad "审计退出码 ${au}"; fi
echo "       —— 非 [OK] 行 ——"
grep -v '^\[OK\]' "${TMPDIR:-/tmp}/iter0115-audit.log" | sed 's/^/       /'
unreleased=$(grep -c '^\[UNRELEASED\]' "${TMPDIR:-/tmp}/iter0115-audit.log")
drift=$(grep -c '^\[DRIFT\]\|^\[ERROR\]\|^\[FAIL\]' "${TMPDIR:-/tmp}/iter0115-audit.log")
if [ "$unreleased" = 2 ]; then ok "两条 UNRELEASED 亮牌（发布态，非漂移）"; else bad "UNRELEASED 亮牌 ${unreleased} 条，不是 2 条"; fi
if [ "$drift" = 0 ]; then ok "零 DRIFT / ERROR"; else bad "仍有 ${drift} 条 DRIFT / ERROR"; fi

echo
[ "$fail" = 0 ] && echo "CI-AUDIT-CLEAN" || echo "CI-AUDIT-DIRTY"
exit "$fail"
