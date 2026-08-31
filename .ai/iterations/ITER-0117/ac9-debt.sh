#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== debt 条目数 10 -> 12 =="
n=$(grep -c '^- \*\*' .ai/debt.md); echo "count=$n"; [ "$n" -eq 12 ] || { echo FAIL; exit 1; }
echo "== 12 条标题 =="
grep -o '^- \*\*[^*]*\*\*' .ai/debt.md | awk '{print NR": "$0}' | awk '{print substr($0,1,90)}'
echo "== 新增两条各含缺口/有意不做的理由/自然消解路径 =="
tail -2 .ai/debt.md | grep -c '本轮有意不加检查\|有意不做的理由'
tail -2 .ai/debt.md | grep -c '自然消解路径'
echo "AC9 PASS"
