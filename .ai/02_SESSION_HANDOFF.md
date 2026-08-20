# Session Handoff

## 任务断点

- 迭代：无 active；里程碑：MILE-0016；阶段：ITER-0114 已收口（2026-08-20），等待开启下一迭代。
- 状态：MILE-0016 R3 完成。项目全貌按内容性质分成三份落地——`.ai/OVERVIEW.md` 由 `scripts/sync-project-overview.py` 从五个机器源头生成（8897 / 12000 字节），`--check` 进 CI 逐节比对、诊断指名到节；`.ai/invariants.md` 从 `.ai/project/` 迁位到 `.ai/` 根（47 条原样，git 记为全等重命名），补写作纪律三条并对无真源指针条目上棘轮（基线 16，只防增量）；`.ai/debt.md` 追加 6 条（4 条从退役的 `frontier.md` 迁入）。`.ai/project/frontier.md` 三节 28 条逐条处置后退役，`.ai/project/` 目录移除。读序第 5 步加了两个按需指针，五处载体仍逐字节相同（1284 / 1400）。15 条 AC 全部达成，10 条机器证据全 passed，完整 CI 与状态审计均退出码 0。

## 关键决策摘要

- 以当前阶段产物和 task-state 为准；本文件不另立决策真源。

## 环境脏点

- 运行 `git status --short` 获取实时工作树；handoff 不缓存易陈旧的文件清单。

## 已知风险

- N/A

## 唤醒指令

- 先运行 `python3 tools/handoff/handoff.py check --project-root .`；若 stale，运行同工具 `sync` 后再读 `.ai/task-state.md`。下一动作：按里程碑路线开启 MILE-0016 R4（砍 `/butler:progress` 全链）。本地未提交/未推送状态见工作树；发布侧未动，未切版、未打 tag。

## 状态指针

- `.ai/task-state.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `.ai/MILESTONE.md`
