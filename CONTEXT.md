# Butler Workflow Context

Butler 用这些术语区分探索期的决策状态与交付期的执行真源，避免模型判断、协作占用和生命周期状态混为一谈。

## Language

**Explore**:
用户选择进入的需求探索模式，位于交付生命周期之外。
_Avoid_: 自动前置阶段、需求分类结果、Wayfinder 入口

**Decision Map**:
一次 Explore 中相互关联的未知、决定与依赖关系的持久化集合；进入交付后只作为理由、证据和历史参考。
_Avoid_: Milestone、Iteration、冻结需求

**Decision**:
Decision Map 中一个可独立解决、可声明依赖的明确问题。
_Avoid_: Task、Iteration、AC

**Fog**:
尚不足以表述为 Decision 的开放未知；澄清后可结晶为一个或多个 Decision。
_Avoid_: Decision、Backlog、失败状态

**Dependency**:
一个 Decision 在可处理前必须先解决的另一个 Decision。
_Avoid_: 执行顺序偏好、Milestone 路线

**Frontier**:
当前依赖已经解决且未被有效领取、因此可以开始处理的开放 Decision 集合。
_Avoid_: 持久化队列、模型优先级、Backlog

**Claim Lease**:
某个协作者在有限时间内处理一个 Frontier Decision 的临时独占权；到期后不再有效。
_Avoid_: Decision 状态、永久所有权、权限认证

**Attempt**:
围绕一个已领取 Decision 发起的一次不可变决策工作记录；输入和结果一旦发布都不覆盖。
_Avoid_: 可变 job、Iteration、自动重试

**Task Packet**:
Attempt 的 host-neutral 输入，绑定问题、已确认上下文、约束、预期输出与 Claim 摘要，但不含明文 token、原始对话或项目写权。
_Avoid_: Agent prompt、交付任务单、权限凭证

**Result Envelope**:
Attempt 的不可变输出，只有 candidate、needs_input、failed、cancelled；它记录 helper 事实，不直接改变 Decision。
_Avoid_: Decision resolution、验收结论、自动 promotion

**Needs Input**:
当前 Attempt 因缺真人回答、评价或材料而终结；取得输入后用绑定 predecessor 的新 Attempt 接续。
_Avoid_: 可变暂停状态、覆盖旧结果、自动 retry

**Absorb**:
协调器明确接受 candidate，并通过 Decision Map Module 把其结论与摘要证据指针提交为 Decision resolution 的动作。
_Avoid_: helper 完成、record、自动 resolve

**Promotion**:
用户明确选择 resolved Decision slice 和交付目标后的交接动作；可以只引用到既有 Milestone planned route，或复用 iteration-intake 从新的 Iteration P1 开始。
_Avoid_: 自动路由、自动创建路线、直接进入 P2、Decision Map 同步

**Promotion Receipt**:
一次显式交接的不可变引用，绑定 source closure digest、target 与结果；用于追溯，不拥有 Map、Milestone 或 Iteration 状态。
_Avoid_: 第四个真源、可变索引、冻结 AC

**Explore Dogfood Harness**:
只在临时项目编排 Decision Map、Decision Work 与 Decision Promotion 公共边界的内部回归工具；可用单条零写命令聚合恢复视图，但不保存派生缓存。
_Avoid_: 用户入口、Router、状态真源、agent scheduler、外部 tracker
