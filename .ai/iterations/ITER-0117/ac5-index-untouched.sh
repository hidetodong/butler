#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== .ai/MILESTONES.md 与 P4 前基线逐字节比对 =="
want=$(grep ' \.ai/MILESTONES\.md$' .ai/iterations/ITER-0117/pre-p4.baseline | awk '{print $1}')
got=$(shasum -a 256 .ai/MILESTONES.md | awk '{print $1}')
echo "baseline=$want"
echo "current =$got"
[ "$want" = "$got" ] || { echo "FAIL: 索引被改动"; exit 1; }
echo "== 表头仍 5 列 · 待办区仍 9 行 =="
grep -n '^| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |$' .ai/MILESTONES.md
awk '/^## 待办区/{f=1} f && /^\| [a-z]/{c++} END{print "backlog rows="c}' .ai/MILESTONES.md
echo "AC5 PASS"
