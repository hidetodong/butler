#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== §5.4 的 R6 登记恰 3 条 =="
n=$(grep -c '^- 2026-08-20（R6 · ' .ai/MILESTONE.md)
echo "count=$n"; [ "$n" -eq 3 ] || { echo FAIL; exit 1; }
echo "== 三条各自的主题 =="
grep -o '^- 2026-08-20（R6 · [^）]*）' .ai/MILESTONE.md
echo "== 三条各含处置与理由的关键措辞 =="
grep -c '两份并存，靠声明分工' .ai/MILESTONE.md
grep -c '按\*\*真实路径\*\*写' .ai/MILESTONE.md
grep -c '造出第二个真源' .ai/MILESTONE.md
echo "AC8 PASS"
