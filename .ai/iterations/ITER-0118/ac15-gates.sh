#!/usr/bin/env bash
# AC15：两条门禁取退出码 + 两组扫描零命中
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

LOG=$(mktemp)
bash scripts/verify-ci.sh > "$LOG" 2>&1; rc=$?
[ "$rc" -eq 0 ] && ok "verify-ci.sh 退出码 0" || bad "verify-ci.sh 退出码 ${rc}"
grep -qF 'Ran 28 tests' "$LOG" && ok "新工具的 28 条测试确实在 CI 里跑过" || bad "新工具的测试没在 CI 里跑"
rm -f "$LOG"

LOG=$(mktemp)
python3 scripts/audit-project-state.py --project-root . --allow-unreleased > "$LOG" 2>&1; rc=$?
[ "$rc" -eq 0 ] && ok "审计退出码 0" || bad "审计退出码 ${rc}"
n=$(grep -c '^\[UNRELEASED\]' "$LOG" || true)
[ "$n" = "2" ] && ok "UNRELEASED 恰 2 条" || bad "UNRELEASED 应为 2 条，实为 ${n}"
n=$(grep -c '^\[DRIFT\]' "$LOG" || true)
[ "$n" = "0" ] && ok "DRIFT 0 条" || bad "DRIFT ${n} 条"
echo "  审计 OK 行数：$(grep -c '^\[OK\]' "$LOG")"
rm -f "$LOG"

python3 .ai/iterations/ITER-0118/ac-sweep.py > /dev/null 2>&1 \
  && ok "两组扫描全通过" || bad "两组扫描有命中"
python3 .ai/iterations/ITER-0118/ac-sweep.py | tail -3
exit $fail
