<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0100 · Butler 统一语义 Router 与会话转迭代入口

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-08-01

## Current Understanding

- **一句话**：Butler 现在有 12 个可独立发现的工作流，却没有统一入口帮用户分发自然语言需求，也没有「把当前会话结晶为 P1 并领取一个迭代」的标准工作流。本迭代要同时补上共享语义 Router 和会话转迭代入口，让 Claude 与 Codex / ChatGPT 在两个高频场景下得到一致结果。
- **Goal**：用一份宿主无关的路由规则和一份 registry 元数据真源，支持 Claude `/butler <需求>` 与 Codex / ChatGPT Butler Router 的语义分发；新增可被 Router 命中的 `butler-iteration`，把「总结当前 session 已确认内容并领一个迭代」收敛为可重复的 Butler 动作。
- 直接命中具体工作流时跳过 Router；只在用户选择 Butler 总入口、意图模糊或多候选冲突时由 Router 介入。
- `butler-iteration` 的写入触发必须同时含有「结晶当前会话」和「现在领取 / 开启迭代」的明确意图；单纯「总结一下」仍是只读，不能擅自改 `.ai/` 状态。
- `loop` 与 `dangerous` 现有 `allow_implicit_invocation=false` 是两端共用的安全边界；Router 只能提示显式入口，不得替用户隐式开启。
- 项目是 Markdown 规则仓并附带 Python 同步与校验工具；未命中 Domain / Stack Profile，仅按通用 SOP 和双宿主边界推进。

## Scope

- **In Scope**：新增宿主无关的 Router 规则真源；扩展 `workflows/registry.json` 表达 Router 入口和工作流消歧元数据；新增 Claude `/butler` 与 Codex `butler-router` 两个薄入口；扩展同步器、人读文档与双端回归测试。
- 新增 `butler-iteration` 业务工作流：共享算法放在 `Coder` 的迭代录入规则中，覆盖项目根解析、当前 active 检查、会话结晶、分流、号码分配、五件套 overwrite-reset、P1 CONCEPT、task-state 与 handoff 同步；Claude `/butler:iteration` 和 Codex `$butler-iteration` 仅做薄适配。
- Router 是 registry 的元入口，不作为可路由到自身的业务工作流；`butler-iteration` 是新的第 13 个业务工作流。具体 registry schema 在 P2 / P3 固定。
- 两个宿主适配层只做发现、路由和输入输出转换，不复制语义分类算法，不改现有 12 个工作流的业务规则。
- **Out of Scope**：不在本迭代新增 Pi 总入口；不引入独立分类服务、向量库或用户行为学习；不将高风险工作流改为隐式可调；不改宿主平台本身的 `@` / slash / `$` 交互机制；不把原始会话全文持久化到 `.ai/`。

## Open Questions / Risks

- Claude 中根文件 `.claude/commands/butler.md` 与已有 `.claude/commands/butler/` 目录能在文件系统共存，但需用实际发现测试确认 `/butler` 不会破坏 `/butler:progress` 等现有命令。
- ChatGPT App 的用户界面选择 Butler 后能否始终把普通语言交给 Router，受平台发现和隐式调用政策约束；仓内可机械保证的是 Skill 元数据、优先级和安全退路。
- 语义路由本质上存在模糊输入。必须定义统一的 `routed / ambiguous / explicit-required / not-butler` 结果和消歧门，不能为了「自动」就强行猜测。
- 当一个请求需要前置工作流与后续工作流串联时，MVP 倾向一次只选一个主路由、完成后重新判定，避免 Router 越权编排整条执行链。
- 会话结晶必须区分「用户已确认的决策」、「模型建议」与「待澄清项」；否则 Skill 会把建议误写成用户承诺。
- 如果已有 active 迭代，`butler-iteration` 不得再领新号：P1 未冻结时提议并入当前 CONCEPT；P2 后按修订 / 扩张规则处理，不能制造双 active。
