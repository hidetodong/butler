# Session Handoff

## 任务断点

危险模式已开启。ITER-0059 的 P2 已通过强制自审门并自主冻结，当前进入 P3；目标是连续完成 R4、R5 后收口 MILE-0007。

## 关键决策摘要

- 施工项目根固定为 `/Users/cyborgno2/Documents/WorkCode.nosync/butler`；所有台账继续只写项目内 `.ai/`。
- 机器迁移台账将成为执行真源，历史 Markdown 只做人读说明并受覆盖校验，程序不得正则解释散文。
- 项目内 mechanical action、人工 split/bootstrap 决策和机器级 global install 分域；默认 dry-run/apply 均不改 HOME。
- 项目 apply 必须全队列预检、加锁、原子写、journal/恢复 manifest 和故障自动恢复；不借 git reset 覆盖用户工作树。

## 环境脏点

- ITER-0056、ITER-0057、ITER-0058 已收口但尚未提交/发布；当前工作树叠加三轮增量和本轮 P1/P2。
- 当前发布真相仍是 v2.16.0；R4 不在 P2 阶段切版。

## 已知风险

- v2.13.0/v2.14.0 配方缺迁移步骤章节，v2.6.0 有非标准标签；机器台账迁录时必须保留历史意图并用 fixture 复核。
- `[split]` 不能靠确定性程序安全理解任意用户内容；本轮只承诺诚实决策边界，不承诺静默全自动语义拆分。
- global install 修改 HOME，不属于目标项目事务恢复边界。

## 唤醒指令

- 先读 `.ai/local-constraints.md` 并显式 announce 危险模式 ON，再读 RUN_LOG、CONCEPT、AC_LIST 与本文件；继续 P3 自审，不等待人工 ACK。

## 状态指针

- `.ai/task-state.md`
