---
title: Butler Explore / Ideation 探索引擎
audience: AI / 开发者
scope: P1→P5 之外的 opt-in 需求探索、Decision Map 决策状态与显式 promotion
---

# Butler Explore / Ideation 探索引擎

## 1. 身份

Explore 是 Butler 内建但 opt-in 的探索模式；Ideation 是它的既有 workflow 与兼容入口，不是第二套流程。该模块帮助用户澄清问题、比较取舍并形成可供后续交付参考的 Decision Map，但始终位于 P1→P5 执行生命周期之外。

## 2. 激活条件

只在以下任一条件成立时激活：

- 用户使用 `/butler:ideation`、`$butler-ideation` 或 legacy `/ideation`；
- 用户原始请求主动表达“脑暴、完善需求、想不清楚、还没想好、先探索或比较方向”等探索意图；
- Standard 模式按 `../20_Workflow_Lifecycle/lifecycle.md §1.1` 给出带具体阻塞理由的建议，并得到用户明确同意。

模型自行判断“可能不清晰、可能很大”不构成激活。建议尚未被接受时，本模块不得运行或落盘。

Router 的 `routed` 结果只表示选择了本 workflow，不等于同意持久化。直接显式要求 Decision Map / 跨会话探索的请求可继续走 §4 的项目根与写入门；轻量脑暴仍只留在对话。Standard 建议被接受后，把这次明确同意作为 Explore 激活事实，但是否需要结构化 Map 仍按用户要求和跨会话/并行需要判断，不把“接受建议”自动升级成持久化。

## 3. 执行流程

激活后，按以下阶段自主推进，不依赖外部 skill：

### 3.1 意图探测 (Intent Probing)

通过提问厘清用户真正想要什么：

- 这个需求要解决什么问题？背后的动机是什么？
- 谁会用这个功能？使用频率和场景是什么？
- 有没有已知的约束（时间、技术栈、兼容性）？
- 用户心里有没有已经倾向的方案？

不假设，不脑补。在用户回答之前，不进入下一步。

### 3.2 需求展开 (Requirement Expansion)

基于意图探测的结论，主动挖掘隐性需求：

- 正向路径之外的异常路径和边界场景
- 用户未提及但技术上必须处理的约束（并发、幂等、向后兼容）
- 与现有系统的集成点和数据流依赖

### 3.3 多维压力测试 (Stress Test)

对展开后的需求进行三维审视：

- **UX 维度**：用户路径是否合理，边界场景是否覆盖，交互是否符合直觉
- **架构维度**：与现有系统的耦合点、可扩展性风险、技术债
- **安全维度**：数据边界、权限模型、潜在注入点

### 3.4 收敛 (Convergence)

把压力测试后存活的内容整理为三类：**已确认决定、开放问题、参考依据**。可以给出可验证的 AC 候选，但必须明确标为候选；它们不是 P2 的 `AC_LIST.md`，也没有冻结效力。

## 4. 产物

Decision Map 是探索期“当前决定、未决问题及其依据”的逻辑真源角色，但不是新的用户入口或 workflow ID。目标项目根已按 `../20_Workflow_Lifecycle/mcv-deployment.md §0.1` 唯一解析、用户已经 opt-in，且本次需要结构化、跨会话或并行探索状态时，必须通过驻留 `tools/decision-map/` 的 `inspect / plan / apply / verify` Interface 写入 `.ai/decision-maps/DMAP-NNNN/state.json`；不得由模型或 helper 直接编辑 JSON。Frontier、依赖 DAG、Claim Lease、幂等和本地并发合同以该工具 README 为机器真源，本规则不复制算法。

模型不得因为内部判断“需求比较大”或“不够清晰”就自动创建 Map；持久化发生在用户已选择 Explore，且用户要求保留/并行推进，或明确接受了带具体理由的持久化建议之后。`.ai/00_IDEATION.md` 只保留为轻量对话探索或 legacy 记录；一旦某次探索已经创建结构化 Map，它不得再镜像同一 Map 的状态或成为第二真源。项目根不唯一或用户只要对话探索时，只在对话中呈现，不写 `.ai/`。

当某个开放 Decision 需要受控求证时，协调器先通过 Decision Map `inspect` 展示 Frontier，让用户/协调器显式选择 ID，再逐项 claim；随后才可通过驻留 `tools/decision-work/` 的同名四动作 Interface prepare Task Packet、record Result Envelope，并在审阅候选后显式 absorb。并行的只能是多个已显式选择、分别 claim 的 Research 求证，Map 写入和 absorb 始终由协调器串行提交；Prototype、Grilling、Task 保持单项 serial/HITL。helper 不接收明文 token、不写目标项目或 Map，完成/record/absorbable 都不会自动 resolve。Task/Result、迟到/接续、降级和证据 pointer 的完整合同只以该工具 README 与 `../62_Extension_Agents/decision-work.md` 为真源，本规则不复制 schema。

内部端到端回归可使用驻留 `tools/explore-dogfood/`，但它不是 workflow，也不参与用户请求路由。R5 单仓 dogfood 只证明本地恢复、显式单写和安全降级；不得把 `requested=parallel / actual=serial` 写成已取得并行收益，也不得据一次本地演练自动建设外部 tracker。当前观测与 `defer` 裁决见 `docs/explore-dogfood-r5.md`。

持久化内容只记录：

- 用户已确认的决定及其状态；
- 尚未解决的开放问题；
- 支撑或反驳决定的参考依据。

不要保存模型私有推理，不把候选 AC 伪装成冻结 AC，也不在未 promotion 时创建 Milestone、Iteration、`CONCEPT.md`、`AC_LIST.md` 或后续阶段产物。R2 的 Decision Map 工具同样无权写这些交付期真源。

### 4.1 真源所有权

- **探索期**：Decision Map 拥有探索决策状态。
- **交付期**：Milestone 拥有版本方向与多迭代路线；当前 Iteration 四件套拥有本次交付的目标、冻结 AC、方案和验证事实。
- **promotion 后**：已结晶的 Decision Map 降为理由、证据和历史参考；它不得覆盖当前 `.ai/MILESTONE.md`、`.ai/CONCEPT.md` 或已冻结 `.ai/AC_LIST.md`。发现冲突时按生命周期回退规则修改下游真源，不做双写覆盖。

### 4.2 显式 promotion

当用户明确选择 resolved Decision slice 及交付目标后，协调器才可调用驻留 `tools/decision-promotion/` 的 `inspect / plan / apply / verify` Interface。资格是纯机械谓词：显式 roots 的传递依赖闭包全部 resolved、目标容器兼容、需要开工时没有 active Iteration；它不判断“够不够清晰”“算大还是小”。

- `route-reference` 只引用当前 active Milestone 中已经存在的 planned route，不创建路线、不启动 Iteration。
- `iteration-start` 复用 iteration-intake 从 P1 开始；有 active Milestone 时必须选择其既有 planned route，无 active Milestone 时才可 standalone。

两个 adapter 不能自动串联。`plan` 先展示 source closure、target 和预计结果，用户显式提交该 plan 才允许 `apply`。receipt 是交接引用，不是第四个交付真源；Map 的 close 与 promotion 正交，完整机器合同只以工具 README 为真源。

## 5. 独立 Agent 增强集成

用户可在 Butler 产出阶段产物后，另启独立 agent 使用 `superpowers:brainstorming` skill 进行更深层次的需求探索。

集成方式：

- Agent 读取 Butler 已产出的 `.ai/00_IDEATION.md` 或对话中的 Decision Map 摘要作为输入上下文。
- Agent 产出的分析报告写入 `.ai/references/insight-brainstorm.md`。
- 用户 promotion 后，Butler 在后续 P1 / P2 / P3 按参考资料注入规则读取该报告；报告本身不触发 promotion。

Butler 不主动调用该 skill，也不依赖其产出。Agent 增强是可选路径，Butler 主流程始终自闭环。

## 6. 暂停、退出与 promotion

- 用户暂停或只要探索结果：保留当前 Decision Map，仍在 P1→P5 之外，不创建 Iteration。
- 用户结束探索但不交付：返回 Standard Mode，不自动启动生命周期。
- 用户明确要求“开始做、进入交付、按这个方向实施”等 promotion：先按 `../20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析唯一 `PROJECT_ROOT`，再遵循 `../20_Workflow_Lifecycle/lifecycle.md` 开启或归属 Iteration，**从 P1 Analysis 生成该迭代 `.ai/CONCEPT.md`**。

promotion 不得直接进入 P2，不得把 Decision Map 的 AC 候选视为 P2 ACK，也不得跳过现有 Milestone、P2/P3 ACK 或单 active Iteration 纪律。
