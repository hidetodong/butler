#!/usr/bin/env bash
# AC8 / AC9：§7.6 改指工具且改动全落 §7.6 内；新动作层在 Coder/README.md 两处注册并写明分界
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

F=Coder/20_Workflow_Lifecycle/milestone-schema.md
grep -qF 'tools/intake/intake.py' "$F" && ok "§7.6 已指向工具" || bad "§7.6 已指向工具"
n=$(grep -c '各自把已合成的 §5 内容写入' "$F" || true)
[ "$n" = "0" ] && ok "并行的手工写盘步骤已删" || bad "并行的手工写盘步骤已删（${n}）"

python3 - <<'PY'
import re, subprocess, sys, pathlib
path = "Coder/20_Workflow_Lifecycle/milestone-schema.md"
lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith("### 7.6")) + 1
end = next(i for i, l in enumerate(lines) if l.startswith("## 8.")) + 1
diff = subprocess.run(["git", "diff", "-U0", "--", path], capture_output=True, text=True).stdout
hunks = [(int(a), int(b) if b else 1) for a, b in re.findall(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", diff, re.M)]
mine = [h for h in hunks if h[0] >= start]
older = [h for h in hunks if h[0] < start]
print(f"  §7.6 行区间 = [{start}, {end}]；对 HEAD 的改动块 = {hunks}")
print(f"  其中 ITER-0117 遗留（§4.5 规模分档）= {older}，本轮 = {mine}")
if len(mine) != 1 or not (start <= mine[0][0] and mine[0][0] + mine[0][1] - 1 <= end):
    print("[FAIL] 本轮改动块没有全部落在 §7.6 内"); sys.exit(1)
if len(older) != 1:
    print(f"[FAIL] 预期只有 1 个 ITER-0117 遗留块，实为 {len(older)}"); sys.exit(1)
print("[OK] 本轮对该文件的改动块恰 1 个且完全落在 §7.6 内")
PY
[ $? -eq 0 ] || fail=1

R=Coder/README.md
n=$(grep -c '^    intake-workflow\.md$' "$R" || true)
[ "$n" = "1" ] && ok "目录结构注册恰 1 次" || bad "目录结构注册恰 1 次（${n}）"
n=$(grep -c '^- `40_Context_Management/intake-workflow\.md`' "$R" || true)
[ "$n" = "1" ] && ok "读取顺序指针注册恰 1 次" || bad "读取顺序指针注册恰 1 次（${n}）"

W=Coder/40_Context_Management/intake-workflow.md
grep -qF '工具确定性决定的' "$W" && ok "动作层写了「工具决定」小节" || bad "动作层写了「工具决定」小节"
grep -qF '必须问用户的' "$W" && ok "动作层写了「必须问用户」小节" || bad "动作层写了「必须问用户」小节"
for a in add list handle; do
  grep -qF "\`$a\`" "$W" && ok "动作层覆盖 $a" || bad "动作层覆盖 $a"
done
exit $fail
