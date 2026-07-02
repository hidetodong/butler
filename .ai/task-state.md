# Task State

> 无活跃迭代 · 上一收口 ITER-0019（MILE-0001 R2，2026-06-30）。

## 当前状态

- 无活跃迭代（current=none）。ITER-0019 已收口，MILE-0001 三路线项 R1/R2/R3 全 closed。
- 里程碑 MILE-0001「冷启动可恢复性与收口知识固结」方向达成，尚未聚合发布（按用户指令本轮只提交推送、不切版）。

## 下一步入口

- 若开新迭代：按 `iteration-schema §5.1` 开启（hook `single_active_iteration` 会校验无残留 active），P1 起走四件套。
- 若发布 MILE-0001：聚合切版（MINOR）——更新 `VERSION`、根 `CHANGELOG.md`（聚合 ITER-0017~0019）、按需写 `migrations/`、打 tag。
