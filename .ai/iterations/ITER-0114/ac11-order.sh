#!/usr/bin/env bash
# ITER-0114 · AC11：读序第 5 步补按需指针，五处载体仍逐字节相同、体量不超上限。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

SRC=Coder/40_Context_Management/context-persistence.md

echo "=== AC11 · 第 5 步的两个按需指针 ==="
step5=$(awk '/butler-context-order:begin/,/butler-context-order:end/' "$SRC" | grep '^5\. ')
if [ -z "$step5" ]; then
  bad "读序块里找不到第 5 步"
else
  for ptr in '`.ai/OVERVIEW.md`' '`.ai/invariants.md`'; do
    case "$step5" in
      *"$ptr"*) ok "第 5 步含指针 ${ptr}" ;;
      *) bad "第 5 步缺指针 ${ptr}" ;;
    esac
  done
  case "$step5" in
    *"按需读"*) ok "措辞是「按需读」" ;;
    *) bad "没写「按需读」" ;;
  esac
  case "$step5" in
    *"不是必读"*) ok "显式否掉「必读」，不给模糊空间" ;;
    *) bad "没写明「不是必读」" ;;
  esac
fi

echo "=== AC11 · 五步语义结构未被改动（R2 定的边界） ==="
steps=$(awk '/butler-context-order:begin/,/butler-context-order:end/' "$SRC" | grep -c '^[0-9]\. ')
if [ "$steps" = 5 ]; then ok "读序仍是 5 步，没增删"; else bad "读序变成 ${steps} 步"; fi

echo "=== AC11 · 体量与 metrics ==="
python3 tools/context-budget/context_budget.py check --project-root . > /tmp/iter0114-budget.json 2>&1
code=$?
if [ "$code" = 0 ]; then ok "context_budget.py check 退出码 0"; else bad "context_budget.py check 退出码 ${code}"; fi
python3 - <<'PY'
import json, sys
data = json.load(open("/tmp/iter0114-budget.json", encoding="utf-8"))
m = data.get("metrics", data)
for key, limit in (("order_bytes", 1400), ("order_nonempty_lines", 9), ("order_pointers", 10)):
    value = m.get(key)
    mark = "[OK]  " if value is not None and value <= limit else "[FAIL]"
    print(f"{mark} {key} = {value}（上限 {limit}）")
    if value is None or value > limit:
        sys.exit(1)
print(f"[OK]   order_projections = {m.get('order_projections')}（真源之外四处投影）")
sys.exit(0 if m.get("order_projections") == 4 else 1)
PY
[ $? = 0 ] || bad "metrics 不达标"

echo "=== AC11 · 五处载体逐字节相同（重跑 ITER-0113 的投影校验） ==="
if python3 .ai/iterations/ITER-0113/ac2-projection-sha.py > /tmp/iter0114-proj.log 2>&1; then
  ok "ITER-0113 ac2-projection-sha.py 重跑全 OK（$(grep -c '^\[OK\]' /tmp/iter0114-proj.log) 项）"
  grep '^\[OK\]   真源' /tmp/iter0114-proj.log | sed 's/^/       /'
else
  bad "投影校验重跑失败："
  sed 's/^/       /' /tmp/iter0114-proj.log
fi

echo "=== AC11 · 单测基线已跟上新体量 ==="
if python3 -m unittest discover -s tools/context-budget/tests > /tmp/iter0114-budget-tests.log 2>&1; then
  ok "context-budget 单测全过（$(grep -o 'Ran [0-9]* test' /tmp/iter0114-budget-tests.log | head -1)）"
else
  bad "context-budget 单测失败："
  tail -20 /tmp/iter0114-budget-tests.log | sed 's/^/       /'
fi

echo
[ "$fail" = 0 ] && echo "ORDER-CLEAN" || echo "ORDER-DIRTY"
exit "$fail"
