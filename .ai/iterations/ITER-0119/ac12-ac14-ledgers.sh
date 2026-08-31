#!/usr/bin/env bash
# AC12/AC13/AC14 —— §5.4 五条登记、debt.md 清账、OVERVIEW 重算。
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== AC12 · .ai/MILESTONE.md §5.4 本轮新增五条 =="
awk '/^## 5.4/,0' .ai/MILESTONE.md | grep "^- 2026-08-21（R8" | cut -c1-72

echo "== AC13 · .ai/debt.md 清账 =="
echo -n "  条目数（开工前 14，删 1 改 1 增 2）: "; grep -c "^- \*\*" .ai/debt.md
echo "  已删除的条目（两份 inbox 规则真源并存）命中数: $(grep -c '两份 inbox 规则真源并存' .ai/debt.md || true)"
grep -o "^- \*\*[^*]*\*\*" .ai/debt.md | cut -c1-60

echo "== AC14 · OVERVIEW 重算 =="
grep -n '40_Context_Management/' .ai/OVERVIEW.md
echo -n "  驻留工具清单里 tools/inbox 命中数: "; grep -c 'tools/inbox' .ai/OVERVIEW.md || true
echo -n "  工作流清单行数（应为 12）: "
awk '/^\| ID \| Claude \| Codex \| 风险 \| 规则真源 \|/{f=1;next} f&&/^\|---/{next} f&&/^\|/{c++} f&&!/^\|/{exit} END{print c}' .ai/OVERVIEW.md
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python scripts/sync-project-overview.py --check
