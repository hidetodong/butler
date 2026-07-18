---
方案状态: pass
方案审查日期: 2026-07-18
方案审查方式: dangerous-self-review
---

> ⚠️ 危险模式：本方案经结构化设计自审后自主置 `pass`，未经用户逐项确认（ITER-0064，2026-07-18）。

# Goal

- 用一份共同路由合同把运行时坏消息映射回既有阶段真源和 Goal 状态。

# Files / Modules to Change

- 新增 `Coder/20_Workflow_Lifecycle/goal-calibration.md`；窄接线 lifecycle/goal contract/correction/context/verify/review/dangerous/rule-card/README。
- 新增 `scripts/test-goal-calibration.py` 并接 `verify-ci.sh`。

# Interface / Contract

- task-state 活跃投影行：`ID | Signal | Fact Source | Goal Impact | Route | Status`。
- Signal 封闭六类；Status 为 `open / blocked / resolved`，工作区只保留当前有效 open/blocked 与必要的最近 resolved 结论。

# State / Boundary

- 发现→登记→派生 at-risk/blocked→路由回阶段→修复/重审/重验→resolved→重算 Goal。
- 事实与修改仍写原阶段产物；投影只给跨会话恢复。

# Design Decisions

- 不新增 issue ledger：运行时投影住 task-state，长期事实守既有产物/evidence/review；代价是消费者需按指针读取真源。
- 用“事实性质”而非发现阶段路由，例如 P5 发现方案错误仍回 P3。
- resolved 必须有验证/审查依据，不能靠改状态清零。

# Plan Admission

- AC Coverage：pass；AC1–AC7 均有规则章节、消费者接线或结构/evidence 验证。
- Assumptions：现有 task-state 已是长任务运行态载体；context persistence 可约束其投影格式。
- Alternatives / Trade-offs：否决新 `.ai/ISSUES.md`（第二台账）；否决所有问题一律回 P4（会吞目标/AC/方案变化）。
- Failure Modes：问题只入风险不路由、resolved 无证据、closed 历史被改、任务勾完覆盖 open signal；合同分别机械禁止并由结构测试锁定。
- Impact / Scope Challenge：仅加共同规则与指针，不提前实现 R5 CLI；不改 phase gate 的 P3 职责。
- Verification Blind Spots：结构测试不能证明每次模型都正确分类；R5 completion reader 会进一步机械消费未闭合信号。
- Verdict：pass；方案保持单一真源与最小新结构，没有已知 Must Fix。

# Execution Steps

- [ ] T1 写校准信号、投影和路由合同 → AC1–AC5
- [ ] T2 接入生命周期、纠错、上下文、验证、审查、危险模式与规则卡 → AC6
- [ ] T3 增加结构测试并接完整 CI → AC7
- [ ] T4 evidence、强审、归档、交付、知识折叠和收口 → AC1–AC7

# Verification Plan

- 结构测试覆盖六类信号、六个投影字段、P1–P5/stop 路由、Goal 状态与禁止捷径；完整矩阵和状态审计留机器证据。

# Risks / Open Questions

- R4 是可审计规则而非自动分类器；分类错误仍需 review 发现，R5 提供最终机械拒绝面。
