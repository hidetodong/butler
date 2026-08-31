#!/usr/bin/env bash
# AC5：转 incubated 三处联动，注入写失败时全部回滚、不留半截态
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

python3 -m unittest tools.intake.tests.test_intake.TestIncubateWritesThreePlaces -v 2>&1 | tail -3
python3 -m unittest tools.intake.tests.test_intake.TestIncubateWritesThreePlaces >/dev/null 2>&1 \
  && ok "三处联动写盘用例全通过" || bad "三处联动写盘用例全通过"

python3 -m unittest tools.intake.tests.test_intake.TestRollback -v 2>&1 | tail -3
python3 -m unittest tools.intake.tests.test_intake.TestRollback >/dev/null 2>&1 \
  && ok "注入第二处 / 第三处写失败后全部回滚" || bad "注入第二处 / 第三处写失败后全部回滚"

grep -qF '不等于数据库那种事务' Coder/40_Context_Management/intake-workflow.md \
  && ok "动作层如实写明这不是事务" || bad "动作层如实写明这不是事务"
grep -qF '不得**用「原子事务」' Coder/40_Context_Management/intake-workflow.md \
  || grep -qF '**不得**用「原子事务」这类过头的词' Coder/40_Context_Management/intake-workflow.md \
  && ok "动作层禁止把它说成原子事务" || bad "动作层禁止把它说成原子事务"
exit $fail
