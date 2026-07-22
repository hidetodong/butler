---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：模型已过验收自审门并自主冻结（ITER-0080，2026-07-22）。

# Goal

- 让首切、状态和双宿主入口真正按独立 `prd_id` 工作，且任何只读查询都不改变项目。

# In Scope

- 身份四态、日期目录首切、双层索引、workspace 范围、status CLI、milestone 指针与双宿主注册。

# Out of Scope

- 不实现 update 事务/receipt、代码范围 hook 或真实 apps dogfood。

# Acceptance Checklist

- [ ] AC1：首切在任何写盘前判定 `new-requirement` / `new-version` / `duplicate` / `ambiguous`；仅第一态继续，其余明确路由或停止。
- [ ] AC2：新需求要求可审计的首次进入日期与合法 `YYYY-MM-DD-<slug>`；不得从文件时间、当前时间或模型猜测日期，冲突/歧义 fail-closed。
- [ ] AC3：确认后的首切只写项目级 `prd/00_INDEX.md` 和目标 `<prd_id>/`，保持模块原文逐字、独立版本/归档边界；小 PRD 仍为目录内单模块。
- [ ] AC4：同一次 soft 对齐展示并确认身份、模块 slug/边界与四类 Workspace Scope；模块范围只能是需求总范围子集。
- [ ] AC5：只读 status CLI 能稳定列出项目需求，并按 `--prd-id` 下钻版本/模块/workspace、按 `--workspace` 筛选；两个 PRD 的同名 module slug 相互独立。
- [ ] AC6：status 对 collection 与 legacy 都可读；混合布局、重复 `prd_id`、坏日期目录、symlink、索引/目录不一致时 fail-closed，且所有查询树 hash 不变。
- [ ] AC7：milestone 新交叉指针使用 `<prd_id>#<module_slug>`，旧 slug-only 只作历史兼容，不回写 closed 历史。
- [ ] AC8：`/butler:prd` 与 `$butler-prd` 的 split/status 参数和路由一致，registry 投影无漂移；update 明确要求目标 `prd_id` 但继续委托 R7 前的既有规则。
- [ ] AC9：专项 fixture、结构合同、完整 CI、diff check、Goal/state audit 通过。

# Verification Method

- AC1–AC4、AC7–AC8：规则结构断言、registry 生成检查和双宿主投影对账。
- AC5–AC6：临时 collection/legacy 项目运行 CLI，比较前后 tree hash 并覆盖负向输入。
- AC9：专项 unittest/pytest + `bash scripts/verify-ci.sh` + evidence/Goal/state audit。

# Open Questions / Risks

- legacy status 只能报告单需求隐式身份；升级/筛选能力需先按 R5 指南显式迁移。
