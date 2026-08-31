#!/usr/bin/env bash
# AC14：OVERVIEW 由 --write 重算、--check 退出码 0，三处计数正确
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

python3 scripts/sync-project-overview.py --check && ok "--check 退出码 0" || bad "--check 退出码 0"
grep -qF '| `tools/intake/` | intake — 三层录入契约的写盘者 |' .ai/OVERVIEW.md \
  && ok "驻留工具清单新增 tools/intake/ 且说明非破折号" || bad "驻留工具清单新增 tools/intake/"
n=$(awk '/^\| `40_Context_Management\/`/{print $4}' .ai/OVERVIEW.md)
[ "$n" = "13" ] && ok "40_Context_Management 规则文件数 12 → 13" || bad "规则文件数应为 13，实为 ${n}"
n=$(awk '/^## 工作流清单/{f=1;next} f&&/^## /{exit} f&&/^\| [a-z]/{c++} END{print c+0}' .ai/OVERVIEW.md)
[ "$n" = "12" ] && ok "工作流清单仍 12 行" || bad "工作流清单应为 12 行，实为 ${n}"
grep -qF '| inbox | `/butler:inbox` | `$butler-inbox` | normal | `Coder/40_Context_Management/intake-workflow.md` |' .ai/OVERVIEW.md \
  && ok "inbox 行的规则真源已改指新动作层" || bad "inbox 行的规则真源已改指新动作层"
exit $fail
