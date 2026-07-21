# Concept

## 一句话

新增 `/butler:progress` 只读聚合命令，把当前项目的里程碑、迭代、Goal、验收、执行、验证、风险一页看完。

## Goal

给使用 butler 的项目提供一个稳定的结构化进度查看入口——用户在任意已部署 butler 的项目里敲 `/butler:progress`，就能拿到固定格式的 9 段进度报告，不需要自己逐个翻 `.ai/` 下的状态文件。

## Scope

- Claude Code 命令文件 `.claude/commands/butler/progress.md`
- Codex skill `plugins/butler/skills/butler-progress/SKILL.md` + `.agents/skills/` 软链
- 注册进 `workflows/registry.json`（第 10 个工作流）
- `scripts/sync-workflow-registry.py` 计数同步
- 文档计数更新（capabilities / HUMAN_GUIDE / README / codex-compatibility）

## Non-goals

- 不做写入——纯只读聚合
- 不做独立引擎规则文件——聚合逻辑本身就是命令主体，不需要被其他规则引用
- 不做里程碑/迭代级别的进度聚合——只看当前项目当前状态
- 不做历史趋势对比

## Constraints

- 守 butler 命令范式：第 0 步优雅降级 + 参数路由 + 只读
- 不碰 `Coder/**` 规则算法
- 不下发目标项目（个人工具，与 `/butler:review` 同模型）
