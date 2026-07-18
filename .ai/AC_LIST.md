---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0064，2026-07-18）。

# Goal

- 交付不会吞掉运行时坏消息的 Goal 校准与问题回流合同。

# In Scope

- 信号分类、task-state 活跃投影、Goal 状态影响、P1–P5 路由、修订/扩张/已关闭分流、验证/审查接线与结构测试。

# Out of Scope

- 不实现 R5 完成裁决程序或 R6 宿主同步；不长期保存所有已解决尝试；不改变既有 ACK/方案准入算法。

# Acceptance Checklist

- [ ] AC1：定义实现偏差、假设失效、范围漂移、验证失败、审查发现、外部阻塞六类运行时信号及触发判据。
- [ ] AC2：`.ai/task-state.md # Goal Calibration` 以 ID/信号/事实来源/影响/路由/状态保存当前未闭合项；它是可重算投影，不复制日志或取代真源。
- [ ] AC3：确定路由到 P1 objective、P2 AC、P3 plan、P4 implementation、P5 proof/review 或 honest stop；禁止只记风险后沿旧计划继续。
- [ ] AC4：任何会阻止目标完成的 open 信号派生 Goal `at-risk`，真正无法安全推进为 `blocked`；tasks done 不得覆盖。
- [ ] AC5：AC 变化退 draft 重 ACK，方案变化退 draft 重准入；范围扩张/closed 历史开新迭代，修复后重跑对应 evidence/review 才可 resolved。
- [ ] AC6：lifecycle、correction、context persistence、verify、review、dangerous 与 rule-card 指向单一校准合同，并明确 P5 回填未闭合项。
- [ ] AC7：结构测试检查分类、投影字段、路由、状态影响、禁止捷径与接线；完整矩阵、diff、状态审计和强审有机器 evidence。

# Verification Method

- 结构测试机械检查合同与消费者指针；完整固定矩阵验证规则/双宿主非回归；evidence runner 捕获所有绿结论。

# Open Questions / Risks

- task-state 是人/AI 更新的运行投影，R4 只能规范 fail-honest；R5 再提供机械 complete 拒绝器。
