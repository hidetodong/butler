---
状态: ack-frozen
ACK 日期: 2026-07-18
---
> ⚠️ 危险模式自主 ACK（ITER-0066）。

# Goal
- 完成共享 Goal 闭环的双宿主投影与部署验证。

# Acceptance Checklist
- [ ] AC1：定义 Claude/Codex 共用 host projection：objective/state/reason/next，项目 `.ai/` 优先，host complete 不反写。
- [ ] AC2：capability-detect：有原生 Goal/Task 则投影，无则只用 task-state/handoff，功能语义一致。
- [ ] AC3：共同 rule-card、AGENTS/CLAUDE 渲染、compatibility、deployment/update 文档接入 plan/calibration/adjudicator。
- [ ] AC4：跨会话读序恢复 plan verdict、calibration 与 adjudication next step，不依赖宿主会话记忆。
- [ ] AC5：host wiring 测试证明双入口含同一规则卡、无宿主专属真源/第九 workflow，CLI 对 target project 可达。
- [ ] AC6：诚实披露部署态：新部署/重渲染可用；外部旧项目自动迁移需后续版本发布，不冒称已升级。
- [ ] AC7：专项、完整矩阵、diff、state audit、强审及 milestone 聚合交付均有证据。

# Verification Method
- 结构/隔离渲染测试、完整 CI、状态审计与 milestone 对账。

# Open Questions / Risks
- 宿主原生 API 非稳定合同，采用 capability-detect 与 `.ai/` 降级。
