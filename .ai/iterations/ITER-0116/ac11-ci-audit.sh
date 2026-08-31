#!/usr/bin/env bash
# AC11 · 完整 CI 与状态审计
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "===== bash scripts/verify-ci.sh ====="
bash scripts/verify-ci.sh > /tmp/butler-ci-0116.log 2>&1; ci=$?
echo "verify-ci exit=${ci}"
tail -8 /tmp/butler-ci-0116.log
[ "$ci" -eq 0 ] || exit 1

echo
echo "===== audit-project-state.py --allow-unreleased ====="
python3 scripts/audit-project-state.py --project-root . --allow-unreleased > /tmp/butler-audit-0116.log 2>&1; au=$?
echo "audit exit=${au}"
echo "[OK] 行数 = $(grep -c '^\[OK\]' /tmp/butler-audit-0116.log)"
echo "--- 非 OK / 非 INFO 行 ---"
grep -vE '^\[(OK|INFO)\]' /tmp/butler-audit-0116.log | awk '{print substr($0,1,200)}'
flags=$(grep -c '^\[UNRELEASED\]' /tmp/butler-audit-0116.log)
echo "UNRELEASED 标记数=${flags}（预期恰为 2：工作树未发布 + tag 不指向 HEAD）"
[ "$au" -eq 0 ] && [ "$flags" -eq 2 ] || exit 1
echo "AC11-OK"
