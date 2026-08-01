# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：无 active；阶段：Iteration Closed。
- 状态：ITER-0100 已完成实现、证据归档、交付与台账收口；真实 Claude / ChatGPT App 发现交互保留为非阻断弱验证。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：如需在本机立即启用新入口，用户显式运行 Butler setup / refresh；否则交付即止。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
