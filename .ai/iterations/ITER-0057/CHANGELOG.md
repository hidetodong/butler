# 01_CHANGELOG

> 验证证据链与状态审计 · closed · 2026-07-18

## ADD

- `tools/verification-evidence/ §CLI/契约/测试` — 新增真实命令证据 runner、只读 verifier、hot/archive 单真源移动与 11 项异常回归 → AC1, AC2, AC3, AC6, AC8
- `scripts/audit-project-state.py §Audit` — 新增只读台账/交付/归档/Evidence Index/fold receipt/发布元数据审计器 → AC3, AC6, AC7
- `scripts/test-audit-project-state.py §StateAuditTests` — 新增 11 项正常/漂移/只读/发布/证据与折叠 fixture → AC4, AC6, AC7, AC8

## EDIT

- `Coder/30_Quality_Gate/testing-strategy.md + Coder/20_Workflow_Lifecycle/verify-schema.md` — 自动道改为无机器 record 不打绿，失败证据保留但不能覆盖绿 AC → AC4
- `Coder/60_Extension_CodeReview/review-engine.md + Coder/62_Extension_Agents/independent-review.md` — 复核统一 reported/captured/reproduced，并要求风险抽样产生 review 证据 → AC5
- `Coder/20_Workflow_Lifecycle/{lifecycle,iteration-schema,milestone-schema,mcv-deployment,delivery-summary,versioning-schema}.md` — 接入证据热区/归档、状态审计与发布前 UNRELEASED 边界 → AC4, AC6, AC7
- `Coder/40_Context_Management/{context-persistence,project-digest-schema,handoff-spec}.md + Coder/62_Extension_Agents/knowledge-fold.md` — 增 fold receipt、证据归档和冷启动/交接对账 → AC6, AC7
- `Coder/65_Extension_Dangerous/dangerous-engine.md + templates/rule-card.md` — 标准/危险模式共守无证据不打绿 → AC4, AC5
- `scripts/verify-dual-host.sh §matrix` — 接入 runner/auditor 专项测试、规则强度与 Evidence Index 回归 → AC5, AC8
- `README.md + Coder/README.md + HUMAN_GUIDE.md` — 注册自动证据/状态审计工具、敏感输出与未发布亮牌说明 → AC8
- `.ai/project/{architecture,capabilities,frontier,invariants}.md` — 折叠驻留工具、收口不变量与当前 R2 战线 → AC6, AC7, AC8

## DELETE

- 无
