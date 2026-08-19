#!/usr/bin/env bash
# ITER-0113 · AC8 / AC11 / AC12 弱档代理验证
# 弱档：机器只查得出这几段话写没写、指针互指在不在，判不了写得对不对，最终仍需人读。
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

echo "=== AC8 · rule-card 与读序块分工不互抄 ==="
n=$(grep -cF '派生视图' "$RC")
[ "${n}" = "1" ] && ok "规则卡「派生视图」定性仅 1 处（计 ${n}）" || bad "规则卡「派生视图」出现 ${n} 次"
blk=$(python3 - <<'PY'
import io
s=io.open('Coder/40_Context_Management/context-persistence.md',encoding='utf-8').read()
print(s.split('<!-- butler-context-order:begin -->',1)[1].split('<!-- butler-context-order:end -->',1)[0])
PY
)
printf '%s' "$blk" | grep -qF '派生视图' && bad "读序块复述了「派生视图」定性" || ok "读序块未复述「派生视图」定性"
printf '%s' "$blk" | grep -qF '规则卡「强制工作流」' && ok "读序块指向规则卡" || bad "读序块缺指向规则卡的指针"
grep -qF '会话起始：恢复项目状态' "$RC" && ok "规则卡指向宿主入口的读序块" || bad "规则卡缺指向读序块的指针"
printf '%s' "$blk" | grep -qE '^[0-9]+\. ' && ok "读序步骤在块内" || bad "读序块无编号步骤"
grep -qE '^[0-9]+\. \*\*欠债与边界\*\*' "$RC" && bad "规则卡自己列了读序步骤" || ok "规则卡未列读序步骤"

echo "=== AC11 · [regen-entrypoints] 登记 ==="
reg=$(awk '/^## 5.4/,0' "$MS" | grep -F 'R2 · 发布处置登记' || true)
[ -n "$reg" ] && ok "§5.4 存在 R2 发布处置登记" || bad "§5.4 缺 R2 发布处置登记"
for k in 'templates/AGENTS.md.template' 'templates/CLAUDE.md.template' '[regen-entrypoints]' 'R15'; do
  printf '%s' "$reg" | grep -qF "$k" && ok "登记含：$k" || bad "登记缺：$k"
done

echo "=== AC12 · 交付记录覆盖面变化 ==="
if [ -f "$DL" ]; then
  grep -qF '不是等价替换' "$DL" && ok "交付写明不是等价替换" || bad "交付未写明不是等价替换"
  grep -qF '结构断言' "$DL" && ok "交付写明结构断言是唯一兜底" || bad "交付未提结构断言兜底"
else
  bad "交付文件尚未产出：$DL"
fi


echo
[ "$fail" = "0" ] && echo "PROXY-CLEAN" || echo "PROXY-DIRTY"
exit "$fail"
