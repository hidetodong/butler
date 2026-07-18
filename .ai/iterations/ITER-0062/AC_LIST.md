---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0062，2026-07-18）。

# Goal

- 交付不复制阶段产物的 Goal Contract 与可确定推导的状态机。

# In Scope

- 逻辑合同组成、层级、状态集合/优先级、完成候选、宿主投影纪律、极小任务降级与规则接线。

# Out of Scope

- 不实现方案 verdict、问题回流、完成裁决 CLI/hook 或双宿主同步。

# Acceptance Checklist

- [ ] AC1：Goal Contract 明确 milestone/iteration 两层 objective、obligations、plan、progress、proof/verdict 的既有真源，不新增 GOAL 文件。
- [ ] AC2：定义 `active / at-risk / blocked / completion-candidate / complete / abandoned`，给出确定优先级、进入/退出条件和禁止跃迁。
- [ ] AC3：`completion-candidate` 明确为 tasks done 但尚待 P5 裁决；只有收口事实可派生 complete，覆盖 GFC-002/003/004/008。
- [ ] AC4：宿主 Goal/task 仅为可丢失投影；冲突时项目 `.ai/` 获胜，无原生能力不影响共同流程。
- [ ] AC5：lifecycle、concept/acceptance schema、context persistence、milestone schema 与 Coder 读序都指向同一合同，不复制算法。
- [ ] AC6：结构测试机械检查必需章节、状态集合、优先级、禁止独立 GOAL 台账与接线；完整矩阵和状态审计通过。

# Verification Method

- 运行新增 unittest、完整 CI、状态审计和 diff check，并用 evidence 捕获；逐项对 R1 GFC 反例做文本合同核对。

# Open Questions / Risks

- R2 是规范门而非可执行裁决器；机械拒绝 complete 要到 R5。
