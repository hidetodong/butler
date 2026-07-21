# ITER-0073 交付总结

## 本次交付目标

新增 `/butler:progress` 只读聚合命令，给使用 butler 的项目提供一个稳定的结构化进度查看入口。

## 已完成内容

- 新建 Claude Code 命令文件 `.claude/commands/butler/progress.md`：只读聚合器，读 `.ai/` 下 8+ 状态文件，输出固定 9 段结构化报告（项目概况 → 里程碑 → 迭代 → Goal → 验收 → 执行 → 验证 → 风险 → 最近变更）；支持 `brief` 参数输出一行摘要
- 新建 Codex skill `plugins/butler/skills/butler-progress/SKILL.md` + `.agents/skills/butler-progress` 软链
- 注册进 `workflows/registry.json` 成为第 10 个工作流
- 更新 `scripts/sync-workflow-registry.py` 的 EXPECTED_IDS 与计数（9→10）
- 运行 `sync-workflow-registry.py --write` 同步 41 个投影到 `docs/workflows.md`
- 更新 4 份文档中的工作流/skill 计数（8→10）：capabilities.md / HUMAN_GUIDE.md / README.md / codex-compatibility.md

## 关键变更 / 用户可感知变化

- 任意已部署 butler 的项目里，用户可以敲 `/butler:progress` 获取完整 9 段进度报告，或 `/butler:progress brief` 获取一行摘要
- Codex 用户可用 `$butler-progress` 获得同样能力
- 命令经 setup.sh 目录软链机制自动全局可用，无需重跑安装

## 高层影响范围

| 层 | 影响 |
|---|---|
| 命令文件 | 新增 `.claude/commands/butler/progress.md` |
| Codex skill | 新增 `plugins/butler/skills/butler-progress/` |
| Registry | 新增 progress 条目（10 个工作流） |
| 投影 | docs/workflows.md 自动更新 |
| 文档 | 4 处计数 8→10 |
| `Coder/**` | 无变更 |
| Hook | 无变更 |
| 目标项目 `.ai/` | 无变更 |

## 验证结论

6 条 AC 全部由机器命令验证通过，置信档：可靠。

## 风险与后续

- 无已知风险
- 命令是纯只读聚合器，不修改任何文件，不影响执行流程
- 后续可考虑：是否需要 `--json` 参数输出机器可读格式（不在本迭代范围）
