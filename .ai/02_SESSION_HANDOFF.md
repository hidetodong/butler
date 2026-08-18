# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：MILE-0016；阶段：里程碑已开启，尚未开启承接迭代。
- 状态：候办 `butler-slim-down` 已提升为正式 MILE-0016，`.ai/MILESTONE.md` 整体覆写，台账置 active、`current: MILE-0016`，待办索引与草稿已原子移除。路线图按 schema 拍平为 13 个平级路线项（止血 R1–R4 / 重造 R5–R9 / 治根 R10–R13），三段严格串行。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：开启 R1 承接迭代（退役 `.ai/project/` 知识文件夹 + 两个折叠帮手 + 解除收口仪式对折叠的强制），从 P1 走起。迭代号开启时按台账分配。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `.ai/MILESTONE.md`
