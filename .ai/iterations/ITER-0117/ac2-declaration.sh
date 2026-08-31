#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
F=Coder/40_Context_Management/intake-schema.md
echo "== 声明在 H1 底下的引用块 =="
sed -n '/^# intake-schema/,/^需求从产生/p' "$F" | grep -c '^>'
echo "== 三要素 =="
for m in "生效时点声明" "两份规则真源" "零写入" "一律以 \`inbox-schema.md\` 为准" "没有任何机器检查兜底"; do
  printf '%-30s ' "$m"; grep -cF "$m" "$F"
done
echo "== 旧两文件逐字节未改 =="
grep -E 'inbox-schema\.md$|inbox-workflow\.md$' .ai/iterations/ITER-0117/legacy-inbox.baseline > /tmp/.b0117 || true
while read -r d p; do
  a=$(shasum -a 256 "$p" | awk '{print $1}')
  if [ "$a" != "$d" ]; then echo "FAIL drift: $p"; exit 1; fi
  echo "unchanged: $p"
done < /tmp/.b0117
echo "AC2 PASS"
