# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：无 active；阶段：Iteration Closed。
- 状态：ITER-0099 已完成编号迁移、升级器 hook 摘要口径修复、证据归档、双格式交付和知识折叠。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：提交 ITER-0099 收口变更；是否发布新版本由后续独立决定。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
