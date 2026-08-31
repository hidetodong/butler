#!/usr/bin/env bash
# AC10/AC11 —— 不变量第 48 条改写不删；旧格式回归防线在场且真的锁着行为。
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== AC10 · .ai/invariants.md 第 48 条 =="
grep -n "闪念口只记去向" .ai/invariants.md
echo -n "  invariants 总条目数: "; grep -c "^- \*\*" .ai/invariants.md

echo "== AC11 · 旧格式回归防线 =="
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m unittest \
  tools.intake.tests.test_intake.TestLegacyInboxIsRefusedNotRewritten -v 2>&1 | tail -8
echo "  全量 intake 测试："
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m unittest discover -s tools/intake/tests -t . 2>&1 | tail -3
