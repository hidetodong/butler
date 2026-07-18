---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0063，2026-07-18）。

# Goal

- 交付可审计、可机读且不能靠措辞自我放行的 P3 方案准入门。

# In Scope

- TECH_PLAN verdict 与审查元数据、Plan Admission 反证清单、P3 状态转移、共享 hook、兼容策略、规则接线和自动化证据。

# Out of Scope

- 不实现 R4 问题回流、R5 完成裁决器、R6 宿主 Goal 同步；不自动判断方案内容是否正确。

# Acceptance Checklist

- [ ] AC1：TECH_PLAN schema 定义必填 `方案状态`、审查日期/方式和封闭状态 `draft / pass / revise / blocked`，并明确旧版无字段仅为 hook 兼容态。
- [ ] AC2：`Plan Admission` 必须逐项检查 AC 覆盖、关键假设、替代方案与取舍、失败路径、影响面/范围挑战、验证盲区，并记录 verdict 理由。
- [ ] AC3：标准模式用户 ACK 与危险模式自审都只能在无已知 Must Fix 时置 `pass`；实质改方案退回 `draft`，`revise` 回 P3，`blocked` 诚实停机。
- [ ] AC4：Claude/Codex 共享 `phase_gate` 对显式 `draft/revise/blocked/未知值` 拒绝源码写，只允许 `pass`；旧版无字段继续放行并有正负回归。
- [ ] AC5：Goal Contract 将非 pass 方案派生为 `at-risk` 或 `blocked`，任务完成与用户 ACK 都不得掩盖方案 verdict。
- [ ] AC6：lifecycle、dangerous engine、rule-card、部署/Hook 说明均指向同一准入合同，不复制出第二状态真源。
- [ ] AC7：专项结构测试、phase gate 测试、完整固定矩阵、diff check 与状态审计由 evidence runner 捕获；强审 Must Fix 清零后才能收口。

# Verification Method

- 用结构测试机械检查 schema/接线/状态语义，用 pytest 覆盖 hook 正负状态，用固定 CI 入口与状态审计验证非回归；全部命令经 evidence runner 留 argv、exit、log 与 hash。

# Open Questions / Risks

- hook 只能机械校验 verdict，不会证明方案内容真实充分；结构质量由准入清单、审查和后续 R5 裁决共同约束。
