#!/usr/bin/env bash
# ITER-0113 · AC6 / AC7 确定性验证
# 两条都是确定性检查：旧硬编码列表是否真删干净、过渡措辞是否按半清理。
set -euo pipefail
fail=0
ok()  { echo "[OK]   $*"; }
bad() { echo "[FAIL] $*"; fail=1; }

CP=Coder/40_Context_Management/context-persistence.md
HS=Coder/40_Context_Management/handoff-spec.md
RC=templates/rule-card.md
VC=scripts/verify-codex-foundation.sh
MS=.ai/MILESTONE.md
DL=deliveries/ITER-0113-cold-start-read-order.md

echo "=== AC6 · codex 基线脚本不再自抄读序 ==="
if bash "$VC" > /dev/null 2>&1; then ok "verify-codex-foundation.sh 退出码 0"; else bad "verify-codex-foundation.sh 非零退出"; fi
for needle in '.ai/MILESTONES.md' '.ai/ITERATIONS.md' '.ai/task-state.md' '.ai/CONCEPT.md' '.ai/VERIFY_REPORT.md'; do
  if grep -qF -- "$needle" "$VC"; then bad "旧硬编码路径仍在：$needle"; else ok "旧硬编码路径已删：$needle"; fi
done
grep -qF 'butler-context-order:begin' "$VC" && ok "改为校验读序块起始标记" || bad "未校验读序块标记"
grep -qF 'butler-context-order:end' "$VC" && ok "改为校验读序块结束标记" || bad "未校验结束标记"

echo "=== AC7 · 过渡措辞按半清理 ==="
if grep -qF 'R2' "$CP"; then bad "$CP 仍有 R2 措辞"; else ok "$CP 无 R2 措辞"; fi
if grep -qF 'R2' "$HS"; then bad "$HS 仍有 R2 措辞"; else ok "$HS 无 R2 措辞"; fi
grep -qF 'R3' "$CP" && ok "$CP 保留 R3（全貌产物）那半" || bad "$CP 丢了 R3 那半"
grep -qF 'R3' "$HS" && ok "$HS 保留 R3（全貌产物）那半" || bad "$HS 丢了 R3 那半"


echo
[ "$fail" = "0" ] && echo "CLEANUP-CLEAN" || echo "CLEANUP-DIRTY"
exit "$fail"
