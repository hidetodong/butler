#!/usr/bin/env bash
# AC10：butler 仓真实 dogfood 的收口态——闪念行、真草稿、待办区 9 → 10
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1
fail=0
ok(){ echo "[OK] $1"; }; bad(){ echo "[FAIL] $1"; fail=1; }

KEY=2026-08-20-ship-delivery-renderer
SLUG=delivery-renderer-in-repo
DRAFT=.ai/milestone-backlog/$SLUG.md

[ -f .ai/INBOX.md ] && ok "闪念口文件已由工具建出" || bad "闪念口文件已由工具建出"
grep -qF '| 闪念键 | 记于 | 一句话 | 状态 | 去向 |' .ai/INBOX.md && ok "表头逐字符合契约" || bad "表头逐字符合契约"
grep -qF "| $KEY | 2026-08-20 |" .ai/INBOX.md && ok "闪念行在场且键为日期化形态" || bad "闪念行在场"
grep -qF "| incubated | $DRAFT |" .ai/INBOX.md && ok "状态 incubated 且去向指向草稿" || bad "状态 incubated 且去向指向草稿"

[ -f "$DRAFT" ] && ok "草稿文件存在" || bad "草稿文件存在"
grep -qF "候办键: $SLUG" "$DRAFT" && ok "草稿头部标明候办键" || bad "草稿头部标明候办键"
grep -qF '候办状态: deferred' "$DRAFT" && ok "草稿头部标明候办状态" || bad "草稿头部标明候办状态"
grep -qF '规模: iteration' "$DRAFT" && ok "草稿头部标明规模档" || bad "草稿头部标明规模档"
grep -qF '## 要解决什么' "$DRAFT" && grep -qF '## 暂缓原因' "$DRAFT" \
  && ok "iteration 档两段齐备" || bad "iteration 档两段齐备"
n=$(grep -c 'TODO(''intake)' "$DRAFT" || true)
[ "$n" = "0" ] && ok "占位标记已被真内容替换" || bad "占位标记仍残留（${n}）"

grep -qF "| $SLUG |" .ai/MILESTONES.md && ok "待办区索引行在场" || bad "待办区索引行在场"
n=$(awk '/^## 待办区/{f=1;next} f&&/^\| /&&!/^\| 候办键/&&!/^\|-/{c++} END{print c+0}' .ai/MILESTONES.md)
[ "$n" = "10" ] && ok "待办区由 9 增为 10" || bad "待办区应为 10 行，实为 ${n}"
d=$(find .ai/milestone-backlog -name '*.md' | wc -l | tr -d ' ')
[ "$d" = "10" ] && ok "草稿文件恰 10 份，与索引集合相等" || bad "草稿文件应为 10 份，实为 ${d}"

echo "  收口态复读（工具只读路径）："
python3 tools/intake/intake.py list --project-root . --layer inbox
exit $fail
