# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：MILE-0016；阶段：迭代间隙（ITER-0112 已于 2026-08-18 收口），等待开启 MILE-0016 R2。
- 状态：R1 完成——`.ai/project/` 里靠 delta 折叠维护的五份文件、折叠结构契约 `project-digest-schema.md`、`knowledge-fold` 与 `drift-check` 两个帮手已删除，两处收口仪式不再强制折叠，34 处活引用改到自洽。`invariants.md` 与 `frontier.md` 原位保留、只改了三条因删除而变假的不变量，留给 R3。`debt.md` 迁到 `.ai/debt.md`。10/10 AC 达成（7 条可靠档、3 条弱档），完整 CI 退出码 0。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：开 R2（冷启动读序改造）。R1 在 `context-persistence.md §6` 留下的过渡措辞（第一读已不指知识文件夹、新读序尚未正式定义）是 R2 的直接输入；两份入口模板的读序段落本轮未动，归 R2。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `.ai/MILESTONE.md`
