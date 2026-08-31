#!/usr/bin/env bash
# AC9 · OVERVIEW 由生成器重算、--check 绿，工作流清单仍 12 且 loop 行在场
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== --check 退出码 =="
python3 scripts/sync-project-overview.py --check --project-root .; echo "exit=$?"

echo
echo "== 体量 =="
wc -c .ai/OVERVIEW.md

echo
echo "== 工作流清单行数（应 12） =="
n=$(awk '/^## 工作流清单/{f=1} f && /^\| [a-z]/{c++} /^## 驻留工具清单/{f=0} END{print c+0}' .ai/OVERVIEW.md)
echo "count=${n}"; [ "$n" -eq 12 ] || { echo "FAIL"; exit 1; }

echo
echo "== loop 行在场 =="
grep -n '^| loop |' .ai/OVERVIEW.md | awk '{print substr($0,1,160)}'

echo
echo "== 相对 HEAD 只应有台账跟随行 + ITER-0115 的 progress 删除 =="
git diff -U0 -- .ai/OVERVIEW.md | grep '^[-+]' | grep -vE '^(\+\+\+|---) ' | awk '{print substr($0,1,140)}'
echo "AC9-OK"
