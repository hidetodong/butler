<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0106 · Explore Router 接线与 Butler 自身 dogfood（MILE-0014 R5）

## Current Understanding

- 启动 MILE-0014 最后一条 planned 路线：把已交付的 Explore、Decision Map、Decision Work 与 Decision Promotion 接到 Butler 统一语义入口，并用一个真实大需求验证恢复成本、错误路线、并行收益和维护开销，最后对外部 tracker 价值作出证据化裁决。
- 已确认：用户已明确继续，现启动 MILE-0014 R5，而不是直接关闭里程碑。
- 已确认：Butler 继续只有一个自然语言入口；Explore 是 opt-in 深化模式，不能由模型按清晰度、大小或置信度静默启用。
- 已确认：Decision Map 是交付可引用的决策来源，不替代 Milestone、Iteration、冻结 AC 或 P1→P5。
- 已确认：R5 必须保持普通明确任务的快路径零回归，并以 Butler 自身真实大需求做 dogfood 后再裁决外部 tracker 是否值得建设。
- 已确认：把现有 codex-structured-question-cards 候办作为本轮 dogfood 样本，因为它包含跨宿主能力、交互合同与架构取舍；本轮只探索它，不自动提升候办、不进入其实现生命周期。
- 已确认：先定义可复现的 dogfood 场景与最小观测口径，再做 Router 接线；恢复成本、错误路线、Research 并行效果和 Map 维护开销都以机器记录与操作轨迹为依据，不用主观顺滑感代替证据，也不预设结果必须为正。

## Scope

- 把 Explore opt-in 建议与显式进入语义接入现有 Router / 宿主适配，保持单一入口和 explicit-only 边界。
- 为明确小任务、独立 Iteration、直接 Milestone 与 Explore 深化路径建立零回归合同与负向测试。
- 选择一个真实 Butler 大需求，端到端演练 Decision Map、Decision Work、promotion 与跨会话恢复。
- 记录并比较恢复成本、错误路线、Research 并行收益和 Map 维护开销，形成外部 tracker 的 go / no-go 裁决。
- 完成 R5 后按证据判断 MILE-0014 是否具备版本级收口资格。

## Open Questions / Risks

- dogfood 可以证明本地状态与合同是否可用，但不能仅凭一次仓内演练证明多用户、跨机器或第三方宿主的真实效率收益；结论必须区分“已证明”“未观察到”和“尚无证据”。
- 结构化提问卡片候办仍由自己的未编号 backlog 文件拥有；本轮产生的 Decision Map、工作结果或报告不能被当作该候办已开工。
