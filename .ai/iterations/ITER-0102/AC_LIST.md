---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0102

## Goal

- 建立 Butler Explore / Decision Map 的稳定边界合同：普通任务保持原有快路径，只有用户主动表达探索意图，或用户接受了带具体阻塞理由的 suggest，才进入探索；探索结果通过显式 promotion 接回现有 Iteration P1，而不是自行成为冻结需求。

## In Scope

- 统一 Butler 自然语言入口、显式 Ideation 兼容入口和建议式 opt-in 的语义。
- 固定 Explore、Decision Map、Milestone、Iteration 与 P1→P5 的真源所有权和交接优先级。
- 纠正 Ideation 自动生成 `CONCEPT.md`、直接进入 P2 的旧交接语义。
- 同步规则真源、工作流 registry、宿主薄适配说明和相关人读文档。
- 增加可重复的静态合同与工作流分发检查，证明快路径和既有入口未回归。

## Out of Scope

- 不实现 Decision Map 文件结构、依赖 DAG、Frontier、claim、research helper 或 promotion 工具。
- 不实现 Decision Map 与 Milestone 路线、Iteration Admission 的机器接线。
- 不实现需求清晰度、复杂度或交付体量的自动分类器。
- 不增加 `off / explicit-only` 项目配置，也不新增 `/explore` 或 `$butler-explore` 入口。
- 不修改 P2 ACK、P3 方案准入、单 active Iteration、P4/P5 或证据收口纪律。

## Acceptance Checklist

- [x] AC1: 权威规则明确 Butler 仍只有一个自然语言入口；Explore 是内建但 opt-in 的可选探索模式，未启用时普通明确需求继续走原有简化路径、独立 Iteration 或 Milestone。
- [x] AC2: suggest 是唯一默认策略：建议必须列出会改变目标、范围、AC、路线或高成本约束的具体阻塞项；建议本身零状态写入，用户未同意时不得创建持久化 Decision Map、Milestone 或 Iteration。
- [x] AC3: 显式 `/butler:ideation`、`$butler-ideation` 与 legacy `/ideation` 继续可用；它们进入同一探索真源，不新增 Explore 工作流 ID、命令或第二套算法。
- [x] AC4: Ideation/Explore 始终位于 P1→P5 之外；收敛产物只保存已确认决定、开放问题和参考依据，用户显式 promotion 后才解析项目根、启动 Iteration 并在 P1 生成 `CONCEPT.md`，不得直接跳入 P2 或把脑暴 AC 当成冻结 AC。
- [x] AC5: 真源优先级被明确且无双写：探索期 Decision Map 拥有决策状态；交付期 Milestone 拥有版本路线、Iteration 四件套拥有当前交付；已结晶决定进入交付后，Decision Map 降为理由、证据和历史参考，不得覆盖当前 Milestone、CONCEPT 或冻结 AC。
- [x] AC6: registry、Claude/Codex 薄适配和人读文档与共同规则真源语义一致；自动检查覆盖 suggest 边界、显式入口兼容、禁止自动 P2、无新增 Explore 工作流，以及现有工作流 registry/分发不回归。

## Verification Method

- AC1: 静态合同测试检查 lifecycle / ideation 真源中的单入口、opt-in 与快路径不变语义；人工对照完整 diff。
- AC2: 静态合同测试检查“具体阻塞理由、零写建议、等待确认”三项同时存在，并确认无自动创建状态的相反表述。
- AC3: 运行 workflow registry 同步检查与 Codex workflow 验证，确认 ideation ID、三类兼容入口和现有业务工作流集合不变。
- AC4: 静态合同测试拒绝 ideation 真源继续包含“自动写 CONCEPT / 进入 P2”，并确认 promotion 指向 Iteration P1 和项目根解析。
- AC5: 静态合同测试检查 Decision Map / Milestone / Iteration 的真源职责与交付期优先级；人工审阅不存在复制 AC 或覆盖下游真源的描述。
- AC6: 运行新增专项测试、`scripts/sync-workflow-registry.py --check`、`scripts/verify-codex-workflows.sh`、Markdown 链接检查、`git diff --check` 和完整 `scripts/verify-ci.sh`。

## External References

- N/A

## Open Questions / Risks

- 自动判断清晰度与交付体量不属于本迭代；测试只能证明 suggest 在已有具体阻塞项时行为正确。
- 现有 registry 允许 ideation 被语义触发；R1 必须把“用户主动表达尚未想清/脑暴”视为主动 opt-in，并与 Butler 在普通任务中提出但尚未获准的 suggest 区分开。
