#!/usr/bin/env bash
# ITER-0115 · AC8/AC9：四份人读文档改齐；两条不变量去数字化且其余正文未动。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC8 · README 能力表那行是删除、不是替换 ==="
if grep -q 'butler:progress' README.md; then bad "README 仍有 /butler:progress"; else ok "README 无 /butler:progress"; fi
if grep -qE '进度总览|进度一览|看进度' README.md; then
  bad "README 补了替代说法，与「直接删、不补替代」的决定不符"
else
  ok "没补任何替代说法"
fi
added=$(git diff -- README.md | grep -c '^+[^+]')
removed=$(git diff -- README.md | grep -c '^-[^-]')
echo "       README 本轮 diff：+${added} / -${removed}"
if [ "$added" = 0 ] && [ "$removed" = 1 ]; then ok "纯删一行"; else bad "不是纯删一行"; fi

echo "=== AC8 · 三份散文计数收敛 ==="
check_doc() {
  local file="$1" old="$2" new="$3" want="$4"
  local n_old n_new
  n_old=$(grep -cF -- "$old" "$file" | tr -d ' ')
  n_new=$(grep -cF -- "$new" "$file" | tr -d ' ')
  if [ "$n_old" = 0 ]; then ok "${file}：旧表述零命中"; else bad "${file}：旧表述仍有 ${n_old} 处"; fi
  if [ "$n_new" = "$want" ]; then ok "${file}：新表述 ${n_new} 处（期望 ${want}）"; else bad "${file}：新表述 ${n_new} 处，期望 ${want}"; fi
}
check_doc HUMAN_GUIDE.md "13 个业务 skills" "12 个业务 skills" 3
check_doc Coder/README.md "13 个业务工作流 skill" "12 个业务工作流 skill" 1
check_doc docs/codex-compatibility.md "Router 元入口和 13 个业务工作流" "Router 元入口和 12 个业务工作流" 1

echo "=== AC9 · 不变量条目数与去数字化 ==="
entries=$(grep -c '^- \*\*' .ai/invariants.md | tr -d ' ')
if [ "$entries" = 47 ]; then ok "条目总数仍为 ${entries}"; else bad "条目总数 ${entries}，期望 47"; fi
python3 - <<'PY'
import re, sys, pathlib
bad = 0
text = pathlib.Path(".ai/invariants.md").read_text(encoding="utf-8")
targets = ["Codex skill 单一实体源", "工作流元数据单一注册源"]
for name in targets:
    line = next((l for l in text.splitlines() if name in l), None)
    if line is None:
        print(f"[FAIL] 找不到条目：{name}"); bad = 1; continue
    if re.search(r"\d+\s*个业务", line):
        print(f"[FAIL] {name} 仍复述工作流个数"); bad = 1
    else:
        print(f"[OK]   {name} 已去数字化")
    if "workflows/registry.json" in line or "plugins/butler/skills/" in line:
        print(f"[OK]   {name} 带真源指针")
    else:
        print(f"[FAIL] {name} 丢了真源指针"); bad = 1
    if "*为什么*" in line:
        print(f"[OK]   {name} 保留了原有的为什么")
    else:
        print(f"[FAIL] {name} 的为什么被改没了"); bad = 1
sys.exit(bad)
PY
[ $? = 0 ] || fail=1
changed=$(git diff --numstat -- .ai/invariants.md | awk '{print $1"/"$2}')
echo "       invariants.md 本轮 diff（增/删行）：${changed}"
if [ "$changed" = "2/2" ]; then ok "只动了那两条"; else bad "改动行数不是 2/2"; fi

echo "=== AC9 · 无指针条目棘轮 ==="
if python3 scripts/sync-project-overview.py --check > /dev/null 2>&1; then
  ok "sync-project-overview --check 通过（内含无指针条目棘轮）"
else
  bad "棘轮或全貌校验未通过"
fi

echo
[ "$fail" = 0 ] && echo "DOCS-CLEAN" || echo "DOCS-DIRTY"
exit "$fail"
