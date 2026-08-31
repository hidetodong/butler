#!/usr/bin/env bash
# ITER-0115 · AC1/AC2：三个实体消失、软链数收敛且不断链、registry 摘掉 progress 块。
set -uo pipefail
cd "$(dirname "$0")/../../.."
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

echo "=== AC1 · 三个实体不存在 ==="
for target in .claude/commands/butler/progress.md plugins/butler/skills/butler-progress .agents/skills/butler-progress; do
  if [ -e "$target" ] || [ -L "$target" ]; then bad "${target} 仍存在"; else ok "${target} 已消失"; fi
done

echo "=== AC1 · 软链数与完整性 ==="
links=$(find .agents/skills -mindepth 1 -maxdepth 1 -type l | wc -l | tr -d ' ')
if [ "$links" = 13 ]; then ok "软链 ${links} 条（Router + 12 业务）"; else bad "软链 ${links} 条，期望 13"; fi
broken=0
for link in .agents/skills/*; do
  [ -e "$link/SKILL.md" ] || { bad "断链：${link}"; broken=$((broken+1)); }
done
[ "$broken" = 0 ] && ok "13 条软链全部指向存在的 SKILL.md"
dirs=$(find plugins/butler/skills -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
if [ "$dirs" = 13 ]; then ok "skill 实体目录 ${dirs} 个"; else bad "skill 实体目录 ${dirs} 个，期望 13"; fi

echo "=== AC2 · registry 摘除结果 ==="
python3 - <<'PY'
import json, sys
data = json.load(open("workflows/registry.json", encoding="utf-8"))
wf = data["workflows"]
bad = 0
def ok(m): print(f"[OK]   {m}")
def no(m):
    global bad
    print(f"[FAIL] {m}"); bad = 1
ok(f"workflows 长度 {len(wf)}") if len(wf) == 12 else no(f"workflows 长度 {len(wf)}，期望 12")
ids = [w["id"] for w in wf]
no("registry 里仍有 progress") if "progress" in ids else ok(f"无 progress：{ids}")
review = next(w for w in wf if w["id"] == "review")
neg = review["routing"]["negative_triggers"]
if any("进度" in t or "status" in t for t in neg):
    no(f"review 仍带指向 progress 的负向触发词：{neg}")
else:
    ok(f"review negative_triggers = {neg}（原有的两条消歧触发词已随 progress 一并退役）")
raw = open("workflows/registry.json", encoding="utf-8").read()
ok("registry 全文零 progress 字样") if "progress" not in raw else no("registry 全文仍含 progress 字样")
sys.exit(bad)
PY
[ $? = 0 ] || fail=1

echo
[ "$fail" = 0 ] && echo "ENTITIES-CLEAN" || echo "ENTITIES-DIRTY"
exit "$fail"
