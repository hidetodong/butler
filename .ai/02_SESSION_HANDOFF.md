# Session Handoff

## 任务断点

危险模式 ON。ITER-0059 / R4 已收口，当前无 active 迭代；自治目标要求立即开启 R5 / ITER-0060，最终关闭 MILE-0007。

## 关键决策摘要

- 可执行升级真源是 `migrations/manifest.json` + `tools/butler-upgrade/upgrade.py`，Markdown 只人读。
- 项目 action、split decision、global machine action 分域；plan 零写入，apply 带 hash/lock/backup/journal/恢复。
- R4 checkpoint 为 `c061209`，隔离分支 `feat/mile-0007-engineering-hardening`。

## 环境脏点

- R4 工作树尚未提交新的迭代 checkpoint；R1–R3 + R4 P1/P2 已在 `c061209`，R4 实现/收口待提交。
- 发布真相仍为 v2.16.0；MILE-0007 未整体发布。

## 已知风险

- 真实外部老项目仍未 dogfood；fixture E2E 已覆盖。
- GitHub workflow/required 状态仍受 R3 已记录的未推送与私有仓库套餐限制。

## 唤醒指令

- 先 announce `.ai/local-constraints.md` dangerous ON，再读 RUN_LOG、MILESTONE 和本文件；开启 ITER-0060，不等待用户 ACK。

## 状态指针

- `.ai/task-state.md`
