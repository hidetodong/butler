---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：模型已过验收自审门并自主冻结（ITER-0081，2026-07-22）。

# Goal

- 让指定 PRD 的改版成为可计划、可确认、可恢复、可追溯的确定性事务。

# In Scope

- update spec、plan/apply/verify/rollback、archive/live/index/receipt 原子切换、影响处置、status receipt 视图与 fixture。

# Out of Scope

- 不做语义自动切分/认亲、不自动改工作产物、不做 R8 范围门禁或 apps dogfood。

# Acceptance Checklist

- [x] AC1：update spec 强制显式合法 `prd_id`、expected old/new version、最终 active 模块 source/origins、removed、confirmed 事实与 dispositions；未知/重复/矛盾字段 fail-closed。
- [x] AC2：`plan` 默认零写，复用 collection/status 合同校验现场，逐模块报告 unchanged/updated/renamed/added/removed/split/merged、source hash、影响三态和缺失处置。
- [x] AC3：`apply` 在排他 lock 下重算 plan，于 staging 中先建立 `<prd_id>/.archive/<old>/` 全量 self-contained 快照，再更新目标 live、单需求索引与项目总索引；其他 PRD bytes 不变。
- [x] AC4：receipt 持久记录 update ID、时间、身份/版本、spec/source/pre/post/archive hash、模块认亲、三态影响和逐项 disposition；status 只读展示目标最近 receipt。
- [x] AC5：active/closed/future 命中未全部显式处置时 apply 拒绝；工具不回写 MILESTONE、AC、迭代归档或 origin。
- [x] AC6：同一 spec 重复 apply 幂等；现场/spec/source 漂移、archive/version 冲突、symlink、并发 lock、篡改 receipt/backup 均 fail-closed。
- [x] AC7：verify 对账 post tree、archive 与 backup；rollback 仅在当前 post/pre hash 完全吻合时反切换，后续任何改动存在就拒绝覆盖。
- [x] AC8：故障注入覆盖 archive/live/index/receipt/stage→backup/backup→live 各点，失败后 collection 精确恢复且无 stage/lock 残留。
- [x] AC9：`prd-update.md`、双宿主 update 路由、status receipt 视图、CLI README/fixture/CI 一致；完整 CI、diff check、Goal/state audit 通过。

# Verification Method

- AC1–AC8：临时多 PRD 项目 subprocess，整树 hash、源 bytes、archive/backup/receipt JSON 和故障注入逐项断言。
- AC4/AC9：status 行为扩展、规则/命令结构合同和 registry check。
- AC9：专项 unittest/pytest + `bash scripts/verify-ci.sh` + evidence/Goal/state audit。

# Open Questions / Risks

- spec 是确认结果，不是替代 soft 对齐；坏认亲只能由确认环节避免，工具负责拒绝结构矛盾和保留证据。
