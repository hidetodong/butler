# MILESTONE — MILE-0014 · Butler Explore 决策地图接入

> 方向性产物（非冻结、不走 ACK）。把持久化决策探索作为 Butler 的 opt-in 内建能力，衔接既有 Milestone / Iteration；本里程碑暂以用户已确认的阻塞决策与交付切片为输入，不解决入口处的清晰度与体量自动判定。

## 5.1 范围评估

**In Scope（版本级）**

- 保持 Butler 对用户只有一个自然语言入口；把 Explore 定位为按需启用的内部探索模式，而不是所有任务进入 P1 前的强制阶段。
- 在上游已经给出并经用户确认的“持久化阻塞决策”和“独立交付切片”基础上，建立本地优先、跨会话可恢复的 Decision Map；本里程碑只消费这些结构化输入，不负责判断需求是否清晰或体量大小。
- 为 Decision Map 定义 Destination、已确认背景、决策问题、Fog、Out of Scope、依赖 DAG、Frontier、claim lease、resolution 和 evidence pointer 等最小合同。
- 区分 research、prototype、grilling、task 等决策工作类型；允许 research 在互不依赖时受控并行，地图与结论仍由单一协调器写入。
- 建立 Decision Map 与交付容器的确定性衔接：一个已确认切片可进入独立 Iteration，多个已确认切片可形成 Milestone planned 路线；未来路线按阻塞决策是否解决滚动取得 Iteration Admission。
- 明确真源所有权：Decision Map 只拥有决策状态，Milestone 只拥有版本范围与路线状态，Iteration 继续独占 P1→P5 的 CONCEPT、AC、方案、实现、证据和收口。
- 建立 plan/apply/verify、幂等 promotion receipt、依赖校验、过期 claim 恢复和归档机制；任何 active Milestone / Iteration 的创建仍需现有用户意图与 Butler 台账纪律。
- 调整现有 Ideation 收敛语义：探索结论不得自动写成某个 Iteration 的 `CONCEPT.md` 或跳入 P2；只有选定路线通过 Iteration Admission 后才进入现有 P1→P5。
- 以 Butler 自身的真实大需求做 dogfood，验证跨会话恢复成本、错误路线减少量、研究并行收益和地图维护负担，再决定是否扩展外部 tracker 适配。

**Out of Scope（版本级）**

- 不在本里程碑中定义“需求是否清晰”“一个还是多个交付切片”的判定算法、评分器或模型置信度规则；这是当前尚未解决的独立脆弱点。
- 不允许模型凭“高 / 低复杂度”静默创建 Decision Map、Milestone 或 Iteration；候选决策与切片必须可检查，生命周期状态转换继续遵守用户确认。
- 不把 Explore 变成普通明确任务的必经长流程；明确小任务继续使用简化路径或独立 Iteration，明确大需求可直接进入 Milestone。
- 不替换 Butler 现有 P1→P5、P2 ACK、单 active Iteration、Milestone 方向性演进和证据收口纪律。
- 不把 Decision ticket 等同于实现任务，不把 Milestone 路线项改造成决策票，也不让 Decision Map 直接冻结 AC。
- 不引入多 active Iteration、不借本方向实现并行 P4；相关能力继续由已有独立候办承接。
- MVP 不以 GitHub Issues 或其他外部系统作为唯一真源；是否需要外部 tracker 等本地 dogfood 后再评估。

**关键交付目标**

- 在“阻塞决策与交付切片已被确认”这一明确前提下，后续 Decision Map、Milestone 和 Iteration 的创建、关联、推进与收口可以由结构化合同和确定性工具驱动，不再依赖模型临场发明流程。
- 大需求可以先形成版本方向，再由 Decision Map 为未来 planned 路线滚动消除不确定性；无需等整张地图完全结束，也不会提前占用未来 Iteration 编号。
- 任一路线进入 P1 前都能机械回答：它引用哪些已解决决定、是否仍有阻塞决定、由哪个 Milestone 路线承接、为何具备 Iteration Admission 资格。
- 任何新研究结论只影响尚未冻结的方向或未来路线；已进入 P2 冻结的 Iteration 仍严格走现有修订、回退或范围扩张分流。
- 未启用 Explore / Decision Map 时，现有简化路径、独立 Iteration、Milestone 和 P1→P5 行为零变化。

## 5.2 理解阐释

Wayfinder 最值得 Butler 借鉴的部分，是把跨会话的大型模糊工作表达为“决策问题 + 依赖图 + 当前 Frontier”，并让互不依赖的 research 问题并行解决。Butler 已经拥有更完整的交付控制面：Milestone 管版本方向与 planned 路线，Iteration 作为冻结需求的单元独立走 P1→P5，并由 P2 ACK、P5 evidence 和收口审计保证可信交付。因此正确接入方式不是在 Butler 前面再放一条独立 Wayfinder 流程，而是给 Explore 增加可选的持久化 Decision Map，并把其结果通过显式引用喂给现有 Milestone / Iteration。

本次讨论已经稳定了这一后半段架构，但暴露出真正脆弱的前置问题：系统如何可靠判断“当前需求是否足够清晰”和“是否存在多个独立交付切片”。若把这两个语义判断继续交给模型以高 / 低标签控制路由，后续再确定性的状态机也会建立在不可信入口上。因此本里程碑明确把该问题列为外部前提，不在同一版本里假装解决。MVP 先接受用户确认过的阻塞决策与切片清单，验证后续机制的实际价值；前置判定合同成熟后再接入自动建议。

设计来源是 2026-08-01 关于 mattpocock Wayfinder 与 Butler 工作流衔接的讨论。该讨论确认 Butler 仍保持单一用户入口和原有交付生命周期；Ideation 是探索方法，Decision Map 是可选持久化产物，Milestone 是版本路线容器，Iteration 才是唯一需求冻结与交付单元。这份对话输入是普通产品 / 工程 brief，不是需要逐字保真的大 PRD，因此不触发 PRD 切分。

## 5.3 拆分路线图

预计由 5 个迭代承接；实际迭代号在各路线项开启时再绑定。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | Explore / Decision Map 边界合同：冻结单入口、按需升级、真源所有权、用户确认边界和与现有 Ideation/P1 的兼容语义；输入暂以用户确认的阻塞决策与交付切片为准 | ITER-0102 | closed |
| R2 | Decision Map 本地合同与确定性状态机：地图/决策文件、依赖 DAG、Frontier、claim lease、resolve、Fog graduation、校验与跨会话恢复 | ITER-0103 | closed |
| R3 | 决策工作执行与 research helper：research/prototype/grilling/task 输入输出合同、并行研究隔离、证据指针和协调器单写者吸收机制 | ITER-0104 | closed |
| R4 | Milestone / Iteration 衔接：planned 路线引用 Decision、Iteration Admission、promotion plan/apply/receipt、P2 冻结后的变更分流和收口归档 | ITER-0105 | closed |
| R5 | Router 接线与 Butler 自身 dogfood：保持快路径零回归，选择真实大需求验证恢复成本、错误路线、并行收益和维护开销，再裁决外部 tracker 是否值得建设 | ITER-0106 | closed |

## 5.4 范围演进记录

- 2026-08-01：由 Wayfinder 接入 Butler 的工作流讨论建立候办；冻结 Decision Map→Milestone/Iteration 的稳定后半段，把“清晰度与交付体量如何可靠判定”明确排除为尚待单独攻克的前置脆弱点。
- 2026-08-01：用户明确启动候办，正式开启 MILE-0014；保留 5 条 planned 路线，尚未绑定或预占任何 Iteration 编号。
- 2026-08-01：R1 由 ITER-0102 交付并收口；Explore 统一为既有 Ideation 的 opt-in 深化模式，Standard 只可 suggest 零写等待同意，显式 promotion 从 Iteration P1 接回。R2–R5 保持 planned。
- 2026-08-01：R2 由 ITER-0103 交付并收口；Decision Map 获得本地单真源、确定性状态机、依赖 Frontier、Claim Lease、幂等并发与恢复合同。R3–R5 保持 planned，不自动开启。
- 2026-08-01：R3 由 ITER-0104 交付并收口；Decision Work 以不可变 Task/Result sidecar 和单一 helper 合同承接四类决策工作，只有 Research 可受控并行，任何候选都须协调器显式吸收。R4–R5 保持 planned，不自动开启。
- 2026-08-02：R4 由 ITER-0105 交付并收口；Decision Promotion 以两个显式 adapter、resolved slice、不可变 receipt、项目根锁和 pending journal 确定性衔接既有路线或 Iteration P1。R5 保持 planned，不自动开启。
- 2026-08-02：R5 由 ITER-0106 交付并收口；共享 Router 仍只有既有 Ideation 入口，真实 dogfood 验证恢复与显式交接，Research 实际串行，外部 tracker 裁决为 defer。R1–R5 已全部 closed，MILE-0014 具备版本级收口资格。
