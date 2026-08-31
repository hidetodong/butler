#!/usr/bin/env bash
# ITER-0115 · AC10：全貌产物重算后与源头一致、工作流清单少一行、体量仍在上限内。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

if python3 scripts/sync-project-overview.py --check; then ok "--check 退出码 0"; else bad "--check 未通过"; fi
bytes=$(wc -c < .ai/OVERVIEW.md | tr -d ' ')
if [ "$bytes" -le 12000 ]; then ok "体量 ${bytes} 字节，上限 12000"; else bad "体量 ${bytes} 字节，超上限"; fi
if grep -q 'progress' .ai/OVERVIEW.md; then bad "全貌里仍有 progress"; else ok "全貌零 progress"; fi
rows=$(awk '/^\| ID \| Claude \| Codex/{flag=1;next} /^## /{flag=0} flag && /^\| [a-z]/' .ai/OVERVIEW.md | wc -l | tr -d ' ')
if [ "$rows" = 12 ]; then ok "工作流清单 ${rows} 行"; else bad "工作流清单 ${rows} 行，期望 12"; fi
echo "       —— 本轮 OVERVIEW diff ——"
git diff -- .ai/OVERVIEW.md | grep -E '^[+-][^+-]' | sed 's/^/       /'

echo
[ "$fail" = 0 ] && echo "OVERVIEW-CLEAN" || echo "OVERVIEW-DIRTY"
exit "$fail"
