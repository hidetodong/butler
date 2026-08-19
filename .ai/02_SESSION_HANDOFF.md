# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：MILE-0016；阶段：ITER-0113 已收口（2026-08-19），等待开启下一迭代。
- 状态：MILE-0016 R2 完成。冷启动读序收成 `Coder/40_Context_Management/context-persistence.md §6` 一份真源（`butler-context-order` 标记块，1194 字节 / 6 非空行 / 7 指针），四处载体逐字节投影并由 `context_budget.py` 守护，Claude 宿主入口首次带上读序。12 条 AC 全部达成，9 条机器证据全 passed（另留 1 条失败诊断），完整 CI 与状态审计均退出码 0。已登记：下个发布版必须含 `[regen-entrypoints]`，老项目的滞后归 R15。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：按里程碑路线开启 MILE-0016 R3（项目全貌产物重建，承接 `.ai/project/` 剩下的 `invariants.md` 与 `frontier.md`）。本地已提交、未推送，推哪个远端等用户定。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `.ai/MILESTONE.md`
