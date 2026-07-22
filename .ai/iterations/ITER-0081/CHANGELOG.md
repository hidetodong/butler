> ITER-0081 · verified · 2026-07-22

## ADD

- 新增 `tools/prd-update/`：确定性 `plan/apply/verify/rollback`、排他锁、整集合事务交换、receipt 与故障注入。
- 新增 12 项事务行为 fixture 与 7 项规则/双宿主结构合同。

## EDIT

- 重写 PRD update 规则，以显式 `prd_id`、确认 spec、影响处置和 hash 门禁取代对话式隐式更新。
- status 增加目标需求最近 update receipt 的只读投影；Claude/Codex update 分支委托同一 CLI。
- 完整 CI 接入 update 行为组，README、reference 路由与 registry 投影同步。

## DELETE

- 无
