# ITER-0072 · /butler:init 命令

## 本次交付目标
新增 /butler:init 命令，新项目一键部署 Butler 基地车。

## 已完成内容
- Claude 命令 + Codex skill + registry + sync 脚本适配
- sync --check: 9 workflows 37 projections 零漂移

## 关键变更
- 新项目 /butler:init → 自动侦察、展开 .ai/、生成双入口、拷贝 hooks、提示 setup.sh
- 已部署项目 → 提示终止
- 已有 8 工作流无回归

## 引用
- .ai/iterations/ITER-0072/
- .claude/commands/butler/init.md
- plugins/butler/skills/butler-init/SKILL.md
- workflows/registry.json
