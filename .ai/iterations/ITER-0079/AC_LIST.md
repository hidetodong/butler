---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：模型已过验收自审门并自主冻结（ITER-0079，2026-07-22）。

# Goal

- 让多份 PRD 可以被同一迭代准确钉版，并让 legacy 单 PRD 显式、可恢复地迁入需求集合而不改写历史。

# In Scope

- 多 PRD 引用合同、兼容 resolver、迁移工具/receipt/rollback、历史影响面扫描、指南和自动验证。

# Out of Scope

- 不实现 R6 split/status，不实现 R7 update，不写外部 apps 项目，不自动改 frozen/closed 工作。

# Acceptance Checklist

- [ ] AC1：`acceptance-schema` 定义 `prd_refs` 列表，完整锚点含 `prd_id + prd_version + module_slugs`；集合新写法与 legacy `prd_version` 互斥，非 PRD 仍省略。
- [ ] AC2：`tech-plan-schema` 与 `verify-schema` 继承 AC 的每项钉版并逐 PRD 解析/核对，不自立版本；live 与独立 archive 路径准确。
- [ ] AC3：标准库 reference resolver 同时解析 collection `prd_refs` 和 legacy `prd_version + prd/<slug>.md`，稳定 JSON/退出码，歧义、缺文件、版本不存在 fail-closed。
- [ ] AC4：迁移 `inspect/plan` 默认零写，要求显式合法 `prd_id`/标题，盘点 legacy 文件、版本、hash 与引用影响面；集合/空/混合/符号链接输入准确拒绝或报告。
- [ ] AC5：`apply` 用同父 staging + backup + rename 事务迁移成项目索引/单需求目录，写机器 receipt；origin 与 closed 归档零写，失败不留下半成品。
- [ ] AC6：重复 apply/verify 幂等；rollback 只在 receipt/当前 hash 对账通过时恢复本次 backup，漂移时拒绝破坏现场。
- [ ] AC7：迁移影响面分 MILESTONE、active/future、closed；closed/frozen 文件不回写，legacy 旧引用经 receipt/resolver 仍定位原 `prd_id`、版本和模块。
- [ ] AC8：`docs/prd-migration-guide.md` 可独立照做，覆盖迁移前盘点、首次进入日期证据、`prd_id`、MILESTONE、冻结/closed AC、apply/verify、失败恢复和备份清理；HUMAN_GUIDE 有入口。
- [ ] AC9：隔离 fixture 覆盖多 PRD refs、legacy live/archive、plan 零写、apply/verify/重复、注入故障/rollback、历史零写与坏输入；完整 CI 和 diff check 通过。

# Verification Method

- AC1–AC3：schema 结构测试 + resolver 临时 collection/legacy fixture。
- AC4–AC7：临时项目 CLI subprocess、树 hash、故障注入和归档 hash 对账。
- AC8：指南章节/命令/恢复红线结构测试与 Markdown link check。
- AC9：专项 unittest/pytest + `bash scripts/verify-ci.sh` + Goal/state audit。

# Open Questions / Risks

- 真实 apps 项目形态和权限留 R8，不用本仓 fixture 冒充真实迁移已完成。
