#!/usr/bin/env bash
# ITER-0114 · AC5：--check 进 CI，位置与其他 --check 类检查一致，完整 CI 全绿。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC5 · CI 脚本里的两行 ==="
n=$(grep -c 'sync-project-overview' scripts/verify-ci.sh)
if [ "$n" -ge 1 ]; then ok "scripts/verify-ci.sh 含 sync-project-overview 共 ${n} 行"; else bad "CI 脚本里没有 sync-project-overview"; fi
grep -n 'sync-project-overview' scripts/verify-ci.sh | sed 's/^/       /'
if grep -qF 'sync-project-overview.py" --check --project-root .' scripts/verify-ci.sh; then
  ok "--check 一行在场且带 --project-root ."
else
  bad "--check 那一行不在或形状不对"
fi

echo "=== AC5 · 位置与其他 --check 类检查一致 ==="
python3 - <<'PY'
import pathlib, sys
lines = pathlib.Path("scripts/verify-ci.sh").read_text(encoding="utf-8").split("\n")
def find(needle):
    return next((i + 1 for i, l in enumerate(lines) if needle in l), None)
pairs = [
    ("artifact-pipeline", "discover -s tools/artifact-pipeline/tests", "contract.py check project"),
    ("context-budget",    "discover -s tools/context-budget/tests",    "context_budget.py check"),
    ("project-overview",  "test-sync-project-overview.py",             'sync-project-overview.py" --check'),
    ("domain-contract",   "discover -s tools/domain-contract/tests",   "domain_contract.py check"),
]
rows, bad = [], 0
for name, test_needle, check_needle in pairs:
    t, c = find(test_needle), find(check_needle)
    rows.append((name, t, c))
    mark = " ← 本轮新增" if name == "project-overview" else ""
    print(f"       {name:<18} 测试 L{t} → 校验 L{c}{mark}")
    if t is None or c is None or c != t + 1:
        print(f"[FAIL] {name} 不是「先跑测试、紧跟 --check」的成对形状")
        bad = 1
order = [c for _, _, c in rows]
if order == sorted(order) and None not in order:
    print(f"[OK]   四组校验按 L{order[0]}→L{order[-1]} 连续排列，本轮新增夹在 context-budget 与 domain-contract 之间")
else:
    print("[FAIL] 校验行不连续或顺序错乱")
    bad = 1
sys.exit(bad)
PY
[ $? = 0 ] || bad "位置不一致"

echo "=== AC5 · 完整 CI ==="
if bash scripts/verify-ci.sh > /tmp/iter0114-ci.log 2>&1; then
  ok "bash scripts/verify-ci.sh 退出码 0（$(wc -l < /tmp/iter0114-ci.log | tr -d ' ') 行输出）"
  tail -5 /tmp/iter0114-ci.log | sed 's/^/       /'
else
  bad "完整 CI 失败："; tail -30 /tmp/iter0114-ci.log | sed 's/^/       /'
fi

echo
[ "$fail" = 0 ] && echo "CI-CLEAN" || echo "CI-DIRTY"
exit "$fail"
