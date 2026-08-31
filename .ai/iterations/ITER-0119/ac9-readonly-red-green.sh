#!/usr/bin/env bash
# AC9 —— 用户原件只读那条纪律：规则正文与合同测试逐字配对，删掉正文那句测试必须红。
set -euo pipefail
cd "$(dirname "$0")/../../.."
SRC=Coder/40_Context_Management/references-schema.md
BAK="$(mktemp)"
cp "$SRC" "$BAK"
restore() { cp "$BAK" "$SRC"; rm -f "$BAK"; }
trap restore EXIT

echo "== 1) 现状：应全绿 =="
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m pytest templates/hooks/tests/test_prd_collection_contract.py -q 2>&1 | tail -2

echo "== 2) 把规则正文那句纪律删掉：合同测试必须红 =="
python3 - <<'PY'
import pathlib
p = pathlib.Path("Coder/40_Context_Management/references-schema.md")
t = p.read_text(encoding="utf-8")
line = "- `.ai/references/raw/` 用户原稿不因 PRD 集合而被改写、移动或删除。\n"
assert line in t, "规则正文里找不到那条纪律"
p.write_text(t.replace(line, "", 1), encoding="utf-8")
PY
set +e
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m pytest templates/hooks/tests/test_prd_collection_contract.py -q > /tmp/iter0119-red.log 2>&1
rc=$?
set -e
tail -3 /tmp/iter0119-red.log
test "$rc" -ne 0 && echo "  ✓ 如期变红（退出码 ${rc}）"

echo "== 3) 还原后应重新全绿 =="
restore
trap - EXIT
UV_NO_SYNC=1 uv run --locked --python 3.12.12 python -m pytest templates/hooks/tests/test_prd_collection_contract.py -q 2>&1 | tail -2
