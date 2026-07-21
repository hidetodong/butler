# Tech Plan

方案状态: pass

## 方案概述

按 butler 既有命令范式新增 `/butler:progress`——与其他命令不同的是，progress 不做薄壳路由委托（没有独立引擎规则文件），而是自身就是只读聚合器，直接读 `.ai/` 下多个状态文件按固定格式输出。

## 改动清单

1. **新建命令文件** `.claude/commands/butler/progress.md`
   - frontmatter: description + argument-hint
   - 第 0 步：检查 `.ai/` 存在，不存在优雅降级
   - 分支 A：`brief` → 一行摘要（只读 task-state.md）
   - 分支 B：留空 → 完整 9 段报告（§1 项目概况 → §9 最近变更）
   - 数据源：task-state.md / MILESTONES.md / AC_LIST.md / TECH_PLAN.md / VERIFY_REPORT.md / 01_CHANGELOG.md

2. **新建 Codex skill** `plugins/butler/skills/butler-progress/SKILL.md`
   - 与 Claude 命令同逻辑的精简版
   - `.agents/skills/butler-progress` 软链指向

3. **注册进 registry** `workflows/registry.json`
   - 新增 `progress` 工作流条目（risk: normal, allow_implicit: true）
   - `scripts/sync-workflow-registry.py`：EXPECTED_IDS 加 `progress`，计数 9→10

4. **同步投影** 运行 `sync-workflow-registry.py --write`
   - 更新 `docs/workflows.md`

5. **文档计数更新**
   - `.ai/project/capabilities.md`：命令表加一行 + 工作流/skill 计数 8→10
   - `HUMAN_GUIDE.md`：3 处 8→10
   - `README.md`：1 处 8→10
   - `docs/codex-compatibility.md`：1 处 8→10

## Execution Steps

- [x] 1. 新建 `.claude/commands/butler/progress.md`
- [x] 2. 新建 `plugins/butler/skills/butler-progress/SKILL.md`
- [x] 3. 创建 `.agents/skills/butler-progress` 软链
- [x] 4. 更新 `workflows/registry.json` 加 progress 条目
- [x] 5. 更新 `scripts/sync-workflow-registry.py` 计数
- [x] 6. 运行 `sync-workflow-registry.py --write` 同步投影
- [x] 7. 更新 capabilities.md / HUMAN_GUIDE.md / README.md / codex-compatibility.md 计数
- [x] 8. 验证：`sync-workflow-registry.py --check` 通过
- [x] 9. 验证：文件结构与软链正确
- [x] 10. 开迭代台账 + 收口交付
