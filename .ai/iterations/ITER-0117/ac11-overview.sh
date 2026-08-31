#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
echo "== --check 退出码 =="
python3 scripts/sync-project-overview.py --check; echo "exit=$?"
echo "== 40_Context_Management 规则文件计数（新增后应为 12） =="
grep -n '^| `40_Context_Management/` |' .ai/OVERVIEW.md
ls Coder/40_Context_Management/*.md | wc -l
echo "== 工作流清单仍 12 行 =="
awk '/^## 工作流清单/{f=1} f && /^\| [a-z]/{c++} /^## 驻留工具清单/{f=0} END{print "rows="c}' .ai/OVERVIEW.md
echo "AC11 PASS"
