#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
F=Coder/40_Context_Management/intake-schema.md
FUTURE=".ai/""backlog""/"
echo "== 新契约不得出现 R9 才存在的路径 =="
if grep -nF "$FUTURE" "$F"; then echo "FAIL"; exit 1; fi
echo "hits = 0"
echo "== 写的是当前真实落点 =="
grep -c '\.ai/milestone-backlog/' "$F"
echo "== R9 改名预告在场 =="
grep -n 'R9 会把它改成\|归 MILE-0016 R9' "$F" | head -3
echo "AC3 PASS"
