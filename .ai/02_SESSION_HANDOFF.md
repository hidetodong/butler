# Session Handoff

## 任务断点

MILE-0006 的 R1 / ITER-0051 已收口并发布 v2.12.0。当前没有 active 迭代；下一步是另开 R2 skills/plugin 迭代。

## 关键决策摘要

- 目标是 Claude Code + Codex 双宿主兼容，不替换或删除 Claude Code 支持。
- `.ai/` 与 `Coder/` 保持共同状态层和规则真源；宿主差异收敛在入口、skills/commands、hooks 与安装配置。
- 里程碑规划为四条路线：R1 注入地基、R2 skills/plugin、R3 hooks、R4 部署升级与双端回归。
- 四项方向已确认：plugin 为最终分发面、四迭代拆分、目标项目最终双入口、一迭代一版。
- R1 收紧为仓库规则发现、目标模板和双宿主架构契约；skills/plugin、hooks、完整部署升级接线仍归 R2–R4。

## 环境脏点

- 分支：`feat/mile-0006-codex-compatibility`。
- 本地版本 / tag：v2.12.0；没有 push 或合并。
- ITER-0051 归档在 `.ai/iterations/ITER-0051/`，交付在 `deliveries/ITER-0051-codex-compatibility-foundation.{md,html}`。

## 已知风险

- 当前 Codex hook 尚未适配：现有 gate 只接受 `Edit/Write/MultiEdit` 与 `file_path`，不能把 `apply_patch` 当成已受机械门禁保护。
- 若 Codex 与 Claude 各维护一份规则正文，会形成漂移；后续设计必须坚持入口薄壳 + 共同真源。

## 唤醒指令

先读 `.ai/MILESTONE.md` 的 R2，再开新迭代做 skills/plugin；不要把 R3 hooks 或 R4 部署升级接线并入 R2。

## 状态指针

- `.ai/task-state.md`
- `.ai/MILESTONE.md`
- `.ai/CONCEPT.md`
