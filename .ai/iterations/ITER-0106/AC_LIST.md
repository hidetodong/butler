---
状态: ack-frozen
ACK 日期: 2026-08-02
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0106

## Goal

- 把已交付的 Explore / Decision Map / Decision Work / Decision Promotion 能力接入 Butler 现有单一语义入口，并以一个真实 Butler 大需求完成可恢复、可审计的端到端 dogfood；用预先声明的观测口径判断本地方案的实际价值与外部 tracker 是否值得建设，同时保证所有非 Explore 快路径零回归。

## In Scope

- Router 与宿主适配中的 Explore opt-in 语义、建议边界、显式进入和单一 Ideation workflow 路由。
- 明确小任务、直接 Iteration、直接 Milestone、轻量 Ideation 与持久化 Explore 的路由非回归矩阵。
- 以 `codex-structured-question-cards` 候办内容为真实样本，演练 Decision Map、Decision Work、恢复与 promotion/admission 边界。
- 恢复成本、错误路线、Research 并行效果与 Map 维护开销的可复现观测和结果报告。
- 基于 dogfood 证据给出外部 tracker 的 go / no-go / defer 裁决，并判断 MILE-0014 是否具备收口资格。

## Out of Scope

- 基于模型评分的需求清晰度、体量或置信度自动分类器。
- GitHub Issues、Linear 或其他外部 tracker 的实现、同步或迁移。
- 自动提升或实施 `codex-structured-question-cards` 候办；它在本轮仍为 deferred。
- 新用户入口、新 workflow ID、多 active Iteration、并行 P4 或修改 P1→P5 阶段门禁。

## Acceptance Checklist

- [ ] AC1: 单入口与显式 opt-in：共享 Router 把用户明确要求探索、Decision Map、跨会话决策或 Wayfinder 式深化的请求路由到既有 Ideation workflow；Standard 模式只有在能指出具体 blocker 时才可零写建议 Explore，并必须等待用户同意。模型不得按清晰度、大小或置信度静默建 Map、Milestone、Iteration 或切换流程。
- [ ] AC2: Router 单真源：Explore 接线继续复用唯一 `ideation` workflow 与现有 Claude / Codex / Pi 薄适配，不新增 Explore / Wayfinder workflow ID、别名入口或第二套算法正文；registry 投影、技能/命令和共同内核之间可机械对账。
- [ ] AC3: 快路径零回归：至少覆盖明确小任务、明确独立迭代、明确大需求直接 Milestone、轻量 Ideation、显式持久化 Explore、仅含模糊措辞但无具体 blocker 六类场景。每类均有唯一预期路线；非 Explore 场景不会产生 `.ai/decision-maps`、Decision Work 或 promotion 写入。
- [ ] AC4: 真实 dogfood 输入隔离：`codex-structured-question-cards` 候办被结晶为一个真实 Explore destination、已确认背景、Out of Scope、Fog 与依赖 DAG，但其 backlog 状态保持 `deferred`，不领取新 Milestone / Iteration、不修改该候办路线图，也不把候办内容冒充已确认的实现需求。
- [ ] AC5: Decision Map 演练：dogfood Map 经正式 `inspect / plan / apply / verify` 创建和推进，包含至少三个非平凡 Decision、一个依赖边以及可派生 Frontier；状态变化只由 Decision Map Module 提交，完整操作 receipt、revision 与 digest 可核验。
- [ ] AC6: Decision Work 演练：至少两个互不依赖的 Research Decision 经显式选择、逐项 claim、prepare、record、审阅和 absorb 流程；实际执行模式如实记录。无论宿主是否并行，helper 结果都不会自动 resolve，Map 最终仍由协调器单写吸收，失败/无结论也不得伪装成收益。
- [ ] AC7: 跨会话恢复观测：在不读取原始对话、只使用已落盘 Map/sidecar 的新进程或 fresh-context 中，单次 inspect 能恢复 destination、当前 Frontier、claim/result 状态和下一动作；报告记录所需命令、读取对象和人工重建步骤，不能只写“可恢复”。
- [ ] AC8: Promotion / admission dogfood：对一个已解决 source slice 执行真实 promotion 预演；若 live Butler 状态因 active Iteration 或无可用 planned route 不允许 apply，必须得到确定性拒绝且零部分写入，并在隔离项目 fixture 完成至少一个合法 adapter 的 apply / receipt / verify 全链路。不得为了演练改写 R5 路线所有权或自动提升候办。
- [ ] AC9: 四项观测报告：同一份 dogfood 报告分别列出恢复成本、错误路线/误写、Research 并行效果、Map 维护开销的预声明口径、原始观测、结论与局限。时间类结果不得作为唯一证据；“无正收益”或“证据不足”是允许且必须诚实保留的结果。
- [ ] AC10: 外部 tracker 裁决：依据 AC4–AC9 给出 `go`、`no-go` 或 `defer` 之一，并逐条说明本地文件方案是否在跨机器协作、多人写入、查询/通知或长期规模上出现已观察到的阻塞；没有实证阻塞时不得把 tracker 写成已需要建设。
- [ ] AC11: 生命周期与安全边界：Router 接线、dogfood 和报告不改变 P2 ACK、P3 Plan Admission、单 active Iteration、Milestone 路线所有权、Decision Map 单写和 promotion 显式 target；损坏状态、stale plan、未知字段或未授权自动升级继续 fail-closed。
- [ ] AC12: 集成质量与收口资格：新增/更新的 Router 合同测试、Decision Modules 回归、双宿主/三宿主静态检查、文档链接和完整 CI 均通过并生成 P5 evidence；MILE-0014 只有在 R5 交付、R1–R5 全部 closed 且版本级风险/延后项明确后才可另行执行里程碑收口。

## Verification Method

- AC1：用 Router fixture 验证显式触发、具体 blocker 建议、拒绝静默写入与等待同意；对建议前后项目树做 hash 对比。
- AC2：运行 registry 生成/检查与 workflow contract 测试，断言仍只有一个 `ideation` workflow，Claude / Codex / Pi 入口只引用共同真源。
- AC3：以表驱动路由测试覆盖六类输入，断言 chosen workflow / no-route、写集和 `.ai/decision-maps` 等路径前后 hash。
- AC4：对 dogfood 前后 `.ai/MILESTONES.md`、候办文件、ITER/MILE 最大号与状态做对比；检查 Map 输入将未确认内容保留为 Decision/Fog 而非 resolution。
- AC5：保存创建/推进/核验命令与 evidence；用 `verify` 检查 DAG、Frontier、revision、digest、receipt 和非法直接写负例。
- AC6：保存两个 Research Task/Result Envelope 与实际执行模式，检查 claim/predecessor/batch 绑定、record 后未自动 resolve、显式 absorb 后 Map 状态。
- AC7：启动不携带会话内容的新进程执行 inspect，保存 stdout 与读取路径；由断言检查 destination、Frontier、work 状态和 next action 均可重建。
- AC8：在 live 项目保存 plan/拒绝与树 hash；在临时隔离项目执行 plan→apply→幂等重放→verify，核对 receipt 和目标结果。
- AC9：用固定 schema/章节检查 dogfood 报告四项均包含口径、观测、结论、局限，并交叉链接对应 evidence ID。
- AC10：静态检查裁决枚举唯一且理由覆盖四类外部化信号；人工复核结论不超出已归档证据。
- AC11：运行 phase/ledger/Decision Map/Work/Promotion 负向回归与状态审计，检查 explicit-only、single-writer、single-active 和 fail-closed 不变量。
- AC12：运行专项测试、workflow registry 检查、`scripts/verify-dual-host.sh`、Markdown link check、完整 `scripts/verify-ci.sh` 与收口前 `audit-project-state.py --allow-unreleased`；P5 Evidence Index 逐 AC 覆盖。

## External References

- N/A

## Open Questions / Risks

- 一次本地 dogfood 不能充分证明多人、跨机器和第三方宿主的长期收益；AC10 可以据此选择 `defer`，但不能冒称已验证。
- 当前宿主不允许本轮主动创建子 agent；Decision Work 必须如实使用可用的 serial / HITL 路径或既有并发工具证据，不能伪造 fresh-context 并行执行。
