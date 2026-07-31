# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：无 active；阶段：Iteration Closed。
- 状态：ITER-0098 已完成开源授权、README 上手链路、贡献指南、安全策略、证据归档与双格式交付。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：仓库管理员核对 GitHub Private Vulnerability Reporting 开关；行为准则与双语 README 按真实需要另开迭代。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
