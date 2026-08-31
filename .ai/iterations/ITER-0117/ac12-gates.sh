#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== CI =="
bash scripts/verify-ci.sh > /tmp/.ci0117 2>&1; echo "verify-ci exit=$?"
tail -3 /tmp/.ci0117
echo "== 审计 =="
python3 scripts/audit-project-state.py --project-root . --allow-unreleased > /tmp/.au0117 2>&1; echo "audit exit=$?"
echo "OK lines = $(grep -cE '^\[OK\]| OK' /tmp/.au0117)"
echo "UNRELEASED = $(grep -c '^\[UNRELEASED\]' /tmp/.au0117)"
grep -E 'DRIFT|FAIL|ERROR' /tmp/.au0117 && { echo "FAIL: 审计有漂移"; exit 1; } || echo "no drift"
[ "$(grep -c '^\[UNRELEASED\]' /tmp/.au0117)" -eq 2 ] || { echo "FAIL: UNRELEASED 不是 2 条"; exit 1; }
echo "== 两组扫描 =="
python3 .ai/iterations/ITER-0117/ac-sweep.py
echo "AC12 PASS"
