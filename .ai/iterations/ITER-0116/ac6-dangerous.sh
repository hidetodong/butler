#!/usr/bin/env bash
# AC6 · dangerous 对 loop 规则文件的纸面依赖已拆，只改这一处
set -euo pipefail
cd "$(dirname "$0")/../../.."
F=Coder/65_Extension_Dangerous/dangerous-engine.md
NEEDLE="convergence-""loop-engine"

echo "== 全文引用 loop 规则文件（应为 0） =="
n=$(grep -c "$NEEDLE" "$F" || true); echo "count=${n}"; [ "$n" -eq 0 ] || { echo "FAIL"; exit 1; }

echo
echo "== §8 的新 RCA 指针在场 =="
grep -n 'bounded-convergence.md` §3 写 RCA' "$F" | awk '{print substr($0,1,200)}'

echo
echo "== §9 并列陈述保留 =="
grep -n '与收敛闭环 (`/butler:loop`)' "$F" | awk '{print substr($0,1,200)}'

echo
echo "== 改动范围：应为 1 增 1 删 =="
git diff --numstat -- "$F"
git diff -- "$F" | grep '^[-+]' | grep -vE '^(\+\+\+|---) ' | awk '{print substr($0,1,220)}'
a=$(git diff --numstat -- "$F" | awk '{print $1}'); d=$(git diff --numstat -- "$F" | awk '{print $2}')
[ "$a" -eq 1 ] && [ "$d" -eq 1 ] || { echo "FAIL: 改动行数不是 1/1"; exit 1; }
echo "AC6-OK"
