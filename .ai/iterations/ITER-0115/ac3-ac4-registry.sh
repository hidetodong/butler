#!/usr/bin/env bash
# ITER-0115 · AC3/AC4：EXPECTED_IDS 收敛、--check 对账通过、docs/workflows.md 重算结果。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC3 · EXPECTED_IDS ==="
python3 - <<'PY'
import ast, pathlib, sys
src = pathlib.Path("scripts/sync-workflow-registry.py").read_text(encoding="utf-8")
tree = ast.parse(src)
ids = None
for node in tree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "EXPECTED_IDS":
        ids = {ast.literal_eval(e) for e in node.value.elts}
bad = 0
if ids is not None and len(ids) == 12 and "progress" not in ids:
    print(f"[OK]   EXPECTED_IDS 共 {len(ids)} 项且不含 progress")
else:
    print(f"[FAIL] EXPECTED_IDS = {sorted(ids) if ids else None}"); bad = 1
if "len(EXPECTED_IDS)" in src:
    print("[OK]   registry 数量校验改为从 EXPECTED_IDS 派生，不再硬编码")
else:
    print("[FAIL] 数量校验仍是硬编码"); bad = 1
sys.exit(bad)
PY
[ $? = 0 ] || fail=1

echo "=== AC3 · registry 与全部投影对账 ==="
if python3 scripts/sync-workflow-registry.py --check; then ok "--check 退出码 0"; else bad "--check 未通过"; fi

echo "=== AC4 · docs/workflows.md 重算结果 ==="
rows=$(awk '/^\| ID \| Claude Code/{flag=1;next} /^## /{flag=0} flag && /^\| [a-z]/' docs/workflows.md | wc -l | tr -d ' ')
if [ "$rows" = 12 ]; then ok "工作流表 ${rows} 行"; else bad "工作流表 ${rows} 行，期望 12"; fi
if grep -q 'progress' docs/workflows.md; then bad "仍有 progress 行"; else ok "无 progress 行"; fi
if grep -qF '其余 10 项显式' docs/workflows.md; then
  ok "安全段文案已重算为「其余 10 项」（按 TECH_PLAN D4，中文数字换阿拉伯数字并改为派生）"
else
  bad "安全段文案未按派生结果重算"
fi
if grep -qF 'Router + 12 个业务 Skill' docs/workflows.md; then ok "分发状态表计数已重算为 12"; else bad "分发状态表计数没跟上"; fi
if grep -qF '请勿手改' docs/workflows.md; then ok "页首「请勿手改」声明保留"; else bad "页首声明丢了"; fi

echo "=== AC4 · 生成投影幂等 ==="
before=$(shasum -a 256 docs/workflows.md | cut -d' ' -f1)
python3 scripts/sync-workflow-registry.py --write > /dev/null 2>&1
after=$(shasum -a 256 docs/workflows.md | cut -d' ' -f1)
if [ "$before" = "$after" ]; then ok "再跑一次 --write 逐字节不变（幂等）"; else bad "重跑 --write 产生了差异"; fi

echo
[ "$fail" = 0 ] && echo "REGISTRY-CLEAN" || echo "REGISTRY-DIRTY"
exit "$fail"
