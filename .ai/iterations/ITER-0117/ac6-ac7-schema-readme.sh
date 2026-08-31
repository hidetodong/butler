#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
MS=Coder/20_Workflow_Lifecycle/milestone-schema.md
echo "== milestone-schema 改动行号（须全在 §4.5 编写规则段内） =="
s=$(grep -n '^### 4.5 ' "$MS" | cut -d: -f1)
e=$(grep -n '^## 5\. 里程碑工作区' "$MS" | cut -d: -f1)
echo "§4.5 区间 = [$s, $e)"
git diff -U0 -- "$MS" | grep -E '^@@' | sed 's/.*+\([0-9]*\).*/\1/' | while read -r ln; do
  echo "changed line $ln"
  [ "$ln" -gt "$s" ] && [ "$ln" -lt "$e" ] || { echo "FAIL: 改动溢出 §4.5"; exit 1; }
done
git diff -- "$MS" | grep -vE '^(\+\+\+|---) ' | grep -E '^[-+]' | awk '{print substr($0,1,120)}'
echo "== 两条改到位 =="
sed -n "${s},${e}p" "$MS" | grep -c '一次 `规模: milestone|iteration|undecided`'
sed -n "${s},${e}p" "$MS" | grep -c '按 `规模` 分档'
sed -n "${s},${e}p" "$MS" | grep -c 'intake-schema.md'
echo "== 索引表模板与 §5 零改动 =="
sed -n "${s},${e}p" "$MS" | grep -c '^| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |$'
grep -c '^### 5\.[1-4] ' "$MS"
echo "== AC7: README 两处注册 =="
grep -c '^    intake-schema.md$' Coder/README.md
grep -c '^- `40_Context_Management/intake-schema.md`' Coder/README.md
echo "AC6/AC7 PASS"
