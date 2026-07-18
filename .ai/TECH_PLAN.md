---
方案状态: pass
方案审查日期: 2026-07-18
方案审查方式: dangerous-self-review
---

> ⚠️ 危险模式：本方案经结构化设计自审后自主置 `pass`，未经用户逐项确认（ITER-0063，2026-07-18）。

# Goal

- 以 TECH_PLAN 单一状态源、结构化反证和共享 hook 把 P3 准入变成可执行合同。

# Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/tech-plan-schema.md`：状态、准入清单与转移真源。
- `lifecycle.md`、`goal-contract.md`、`dangerous-engine.md`、`templates/rule-card.md`、`mcv-deployment.md`：窄接线。
- `templates/hooks/rules/phase_gate.py` 与测试：共享机械门禁。
- `scripts/test-plan-admission.py`、`scripts/verify-ci.sh`：结构合同与完整入口。

# Interface / Contract

- 新方案必须显式写 `方案状态`；`pass` 是 P4 唯一合法前置态。
- hook 同时识别 `方案状态` / `plan_status`，字段值不区分大小写；显式非 pass fail-closed，无字段 legacy allow。

# State / Boundary

- `draft → pass | revise | blocked`；`revise → draft` 修订重审；阻塞解除后 `blocked → draft`；pass 后实质变更 `pass → draft`。
- R3 只管“能否从 P3 进入 P4”，不裁决实现与 Goal 最终完成。

# Design Decisions

- verdict 放在 TECH_PLAN frontmatter，收益是原子读取与零双写；代价是旧方案须兼容窗口。
- 选择明确状态 + 人读反证清单，不尝试用 hook 理解自然语言方案质量；机械门负责拒绝已知未通过，内容审查负责发现问题。
- 共享 hook 一次实现覆盖 Claude/Codex，宿主层不各写算法。

# Plan Admission

- AC Coverage：pass；AC1–AC7 均映射到规则、hook、测试或证据动作。
- Assumptions：共享 phase gate 是两宿主源码写门的共同入口；仓内测试可验证该假设。
- Alternatives / Trade-offs：否决独立审批文件（会双写漂移）；否决直接拒绝无字段旧方案（会破坏既有部署）；保留明确兼容窗口。
- Failure Modes：伪造 pass、pass 后改方案不回退、unknown 值误放行、只改一端 hook；分别由规范禁止、审计纪律、fail-closed 测试和共享实现约束。
- Impact / Scope Challenge：改动限 P3 准入与必要接线，不提前实现 R4–R6；规则卡属于已部署高注意力合同，需同步最小指针。
- Verification Blind Spots：自动化不能证明每个自然语言判断绝对正确；强审与 evidence 只能证明流程与已知检查真实执行，必须如实披露。
- Verdict：pass；未发现阻止进入 P4 的 Must Fix，兼容性与不可自动证明边界已显式处置。

# Execution Steps

- [ ] T1 落 TECH_PLAN 状态机、反证清单与生命周期/Goal/危险模式接线 → AC1–AC3、AC5–AC6
- [ ] T2 增强共享 phase gate 并补全状态正负回归 → AC4
- [ ] T3 增加结构合同测试并接入固定 CI → AC1–AC6
- [ ] T4 采集证据、强审、修复、归档和收口 → AC7

# Verification Plan

- 结构测试核字段、状态、准入维度与所有接线；pytest 核 pass/非 pass/未知/英文键/legacy；完整矩阵验证其余规则、生成物和双宿主 hook 不回归。

# Risks / Open Questions

- legacy allow 是迁移兼容而非新合同，必须在文档中明确，避免新方案借兼容路径省字段。
