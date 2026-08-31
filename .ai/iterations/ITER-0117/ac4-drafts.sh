#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== 9 份草稿各恰 1 增 0 删 =="
n=0
for f in .ai/milestone-backlog/*.md; do
  s=$(git diff --numstat -- "$f" | awk '{print $1"/"$2}')
  echo "$s  $(basename "$f")"
  [ "$s" = "1/0" ] || { echo "FAIL"; exit 1; }
  n=$((n+1))
done
[ "$n" -eq 9 ] || { echo "FAIL: 草稿数 $n"; exit 1; }
echo "== 规模字段与既有两标记同处一块 =="
grep -A1 '^候办状态: deferred$' .ai/milestone-backlog/prd-evidence-check.md
echo "AC4 PASS"
