<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0102 · Explore 与 Decision Map 边界合同（MILE-0014 R1）

## Current Understanding

- 把本轮已稳定的产品边界结晶成 Butler 的权威规则合同：Explore 是按需启用而非普通需求必经阶段，Decision Map 在探索期管理决策状态并在交付后作为决策依据参考，Milestone 与 Iteration 继续沿用现有真源和 P1→P5 纪律。本迭代只建立边界、激活和兼容语义，不实现 Decision Map 状态机。
- 已确认：MILE-0014 已正式开启，本轮启动其 R1，其他 R2–R5 保持 planned。
- 已确认：Explore / Decision Map 是 Butler 的 opt-in 内建能力，不替换普通明确需求的现有快路径。
- 已确认：需求是否清晰、一个还是多个交付切片的自动判定是独立脆弱点，不纳入本里程碑和本迭代。
- 已确认：Decision Map 在探索期承载决策状态；结论进入 Milestone、CONCEPT 和 AC 后，Decision Map 主要作为原因、证据和历史脉络的参考来源。
- 已确认：Milestone 管版本方向和路线，Iteration 仍是唯一需求冻结与 P1→P5 交付单元。
- 已确认：后续梳理必须保持已确认主干稳定，设计变化以增量修订表达，不再每轮重新生成一套流程。
- 已确认：用户入口继续统一为 Butler 自然语言入口；Explore 是内部可选模式，现有 `/butler:ideation`、`$butler-ideation` 和 legacy `/ideation` 只作为显式入口兼容，不新增平级 Explore 命令。
- 已确认：统一采用建议式 opt-in。模型发现具体阻塞问题时可以给出理由并建议进入 Explore，但必须等待用户同意；不得静默创建持久化 Decision Map、Milestone 或 Iteration，也不得无理由拖慢普通任务。
- 已确认：现有 Ideation 收敛后不再自动写 `CONCEPT.md` 或跳入 P2；只有用户显式 promotion 到执行、解析唯一项目根并启动 Iteration 后，才从 P1 结晶交付范围。
- 已确认：未启用 Explore 时，简化路径、独立 Iteration、Milestone 和 P1→P5 行为必须保持不变。
- Context Discovery：`Coder/20_Workflow_Lifecycle/lifecycle.md` 负责 P1 前的 suggest 边界；`Coder/50_Extension_Ideation/ideation-engine.md` 负责探索过程、产物身份和 promotion；`Coder/00_System_Prompt/workflow-router.md` 与 `workflows/registry.json` 负责统一入口和显式/隐式语义；Claude command 与 Codex skill 继续只做薄适配。
- Context Discovery：`Coder/README.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md` 和相关生成投影存在旧的“收敛 AC→CONCEPT→P2”表述，需要随真源合同同步，不能留下第二套旧流程。

## Scope

- 定义 Butler 单入口、快路径和 opt-in Explore 的边界与激活语义。
- 定义 Decision Map、Milestone、Iteration 和 P1→P5 之间的真源所有权及引用优先级。
- 修正 Ideation 到 CONCEPT/P1/P2 的交接语义，使探索结论不被当作冻结 AC。
- 定义探索期到交付期的 promotion 边界、用户确认责任和 Decision Map 降级为参考来源的规则。
- 建立文档、skill/router 与非回归检查所需的最小 R1 变更集。

## Open Questions / Risks

- 产品决策已闭合；R1 不增加 `off / explicit-only` 项目配置，未来若有真实需求再独立评估。
- 主要风险是同一语义散落在 lifecycle、ideation、README、logic protocol、registry 和宿主投影后再次漂移；P3 必须以最小真源修改 + 生成投影 + 静态合同检查约束它。
- “需求是否清晰、一个还是多个交付切片”的可靠判定仍是明确排除项；R1 只能规定拿到具体阻塞项后的 suggest 行为，不得声称解决了入口判定。
