#!/usr/bin/env bash
# AC6/AC7/AC8 —— references 定位重写、部署两目录四处一致、brief 与 PRD 文件通道改指新位置。
set -euo pipefail
cd "$(dirname "$0")/../../.."

echo "== AC6 · references-schema.md §1/§2 重写 =="
sed -n '/^## 1. 定位/,/^## 3\./p' Coder/40_Context_Management/references-schema.md
echo -n "  §1 是否还拿已退役的 .ai/project/ 做对照（应为 0）: "
grep -c '\.ai/project/' Coder/40_Context_Management/references-schema.md || true

echo "== AC7 · 部署只建两个目录，四处说法一致 =="
grep -n "两类基础目录\|两个目录" Coder/20_Workflow_Lifecycle/mcv-deployment.md Coder/README.md .claude/commands/butler/init.md templates/rule-card.md
grep -n 'create `.ai/` and `deliveries/`' plugins/butler/skills/butler-init/SKILL.md

echo "== AC8 · brief 与 PRD 的文件通道 =="
grep -n 'references/raw/' Coder/20_Workflow_Lifecycle/milestone-schema.md .claude/commands/butler/prd.md HUMAN_GUIDE.md
