#!/usr/bin/env bash
# ITER-0112 · AC2 / AC9 / AC10 的弱档代理验证
# 机器只能查「写没写、指的真源在不在」，判不了「写得对不对」。
set -euo pipefail
fail=0
ok()   { echo "[OK]   $*"; }
bad()  { echo "[FAIL] $*"; fail=1; }

CL=.ai/01_CHANGELOG.md
MS=.ai/MILESTONE.md
DL=deliveries/ITER-0112-retire-project-knowledge-folder.md

echo "=== AC2 · capabilities.md 22 小节迁出核查留痕 ==="
n=$(python3 .ai/iterations/ITER-0112/ac2-count-sections.py)
[ "$n" = "22" ] && ok "变更流列出 22 个小节（计 ${n}）" || bad "小节计数为 ${n}，期望 22"
grep -q '已迁入 `.ai/debt.md`' "$CL" && ok "无真源判断的迁出落点已写明" || bad "变更流未写明迁出落点"
grep -q '从未在真实已部署项目上跑过' .ai/debt.md && ok "迁出条目确实落在 .ai/debt.md" || bad "迁出条目不在 .ai/debt.md"
for f in Coder/README.md workflows/registry.json docs/workflows.md docs/codex-compatibility.md \
         migrations/manifest.json HUMAN_GUIDE.md README.md CONTRIBUTING.md SECURITY.md \
         Coder/20_Workflow_Lifecycle/versioning-schema.md Coder/30_Quality_Gate/testing-strategy.md; do
  [ -f "$f" ] && ok "被指为真源的文件存在：$f" || bad "被指为真源的文件缺失：$f"
done

echo "=== AC9 · MILESTONE §5.4 的 R14 / R15 交接登记 ==="
reg=$(awk '/^## 5.4/,0' "$MS" | grep -F 'R1 收口 · 交接登记' || true)
[ -n "$reg" ] && ok "§5.4 存在交接登记条目" || bad "§5.4 缺交接登记条目"
for k in '`[split]` 标签' '`--split defer|now`' '空种子例外'; do
  printf '%s' "$reg" | grep -qF "$k" && ok "登记含：$k" || bad "登记缺：$k"
done
printf '%s' "$reg" | grep -qF '**R14**' && ok "登记点名归属 R14" || bad "登记未点名 R14"
printf '%s' "$reg" | grep -qF '**R15**' && ok "登记点名归属 R15" || bad "登记未点名 R15"
grep -qF '[split]' Coder/20_Workflow_Lifecycle/migration-schema.md \
  && ok "现状核对：[split] 标签仍在 migration-schema.md" || bad "现状与登记不符：[split] 已不在"
grep -qF -- '--split' tools/butler-upgrade/upgrade.py \
  && ok "现状核对：--split 参数仍在 upgrade.py" || bad "现状与登记不符：--split 已不在"
grep -qF 'project-knowledge-shape-valid' tools/butler-upgrade/upgrade.py \
  && ok "现状核对：project-knowledge-shape-valid 前置仍在" || bad "现状与登记不符：前置已不在"
grep -qF '已于 ITER-0112 退役' Coder/20_Workflow_Lifecycle/mcv-deployment.md \
  && ok "现状核对：mcv-deployment.md 空种子理由已删并留退役说明" || bad "mcv-deployment.md 未见退役说明"

echo "=== AC10 · 交付总结记录两项信息损失 ==="
grep -qF '折叠回执的历史不可再机器验证' "$DL" && ok "损失一：折叠回执历史不可再机器验证" || bad "交付缺损失一"
grep -qF '不是「已证明它从未被读过」' "$DL" && ok "损失二：论证的是无证据被消费" || bad "交付缺损失二"
grep -qF 'R11' "$DL" && ok "损失二写明确定性数据要等 R11" || bad "交付未写明 R11"

echo
[ "$fail" = "0" ] && echo "PROXY-CLEAN" || echo "PROXY-DIRTY"
exit "$fail"
