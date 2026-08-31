#!/usr/bin/env bash
# AC15 —— CI 与状态审计双绿。
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== CI =="
bash scripts/verify-ci.sh > /tmp/iter0119-ci.log 2>&1
echo "  verify-ci.sh 退出码 = $?"
tail -4 /tmp/iter0119-ci.log

echo "== 状态审计 =="
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python scripts/audit-project-state.py \
  --project-root . --allow-unreleased > /tmp/iter0119-audit.log 2>&1
echo "  audit 退出码 = $?"
echo "  OK=$(grep -c '^\[OK\]' /tmp/iter0119-audit.log)  DRIFT=$(grep -c '^\[DRIFT\]' /tmp/iter0119-audit.log)  FAIL=$(grep -c '^\[FAIL\]' /tmp/iter0119-audit.log)  UNRELEASED=$(grep -c '^\[UNRELEASED\]' /tmp/iter0119-audit.log)"
grep -E '^\[(DRIFT|FAIL|UNRELEASED)\]' /tmp/iter0119-audit.log || true
