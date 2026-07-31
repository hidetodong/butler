# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：MILE-0014；阶段：Closed。
- 状态：ITER-0101 / MILE-0014 R3 已关闭；13 个 evidence、五件套和双格式交付均已归档。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：按用户指令开启 MILE-0014 R4，结构化最小高风险合同并完成 dangerous/loop 与人测所有权双试点。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `.ai/MILESTONE.md`
