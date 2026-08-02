<!-- butler-artifact-template: 1.0.0 artifact=concept -->
> 分流: 完整 | 命中升级信号: 契约变更、多文件改动、跨模块影响、设计取舍 | 2026-08-01

# CONCEPT — ITER-0104 · Decision Map 决策工作 helper 与单写者吸收合同（MILE-0014 R3）

## Current Understanding

**一句话**

R3 要解决的不是“让模型自己选工作并自动做决定”，而是把一次决策工作拆成可检查的任务包、不可变结果和显式吸收三步。Research 可在已明确选中的独立 Frontier 上并行；所有 Map 状态变化仍由协调器通过 R2 的确定性 Module 单写提交。

**Goal**

- 为 research、prototype、grilling、task 建立一个公共工作合同，使任务可跨会话派发、结果可核验、失败可恢复、并行不争写。
- 把“helper 产出了什么”与“该结果是否足以解决 Decision”分开；前者是事实记录，后者始终需要协调器显式吸收。

**已确认的上游事实**

- MILE-0014 R1 已冻结单入口、Explore opt-in 和显式 promotion 边界；R2 已交付 Decision Map 单真源、DAG/Frontier、Claim Lease 与 `inspect / plan / apply / verify` 四动作 Interface。
- R3 只处理决策工作执行、并行隔离、证据指针和单写吸收，不实现 R4 的 Milestone / Iteration Admission 或 promotion。
- research、prototype、grilling、task 是“如何消除一个 Decision 的不确定性”，不是新的 Butler workflow，也不等同于 P4 实现任务。

**已于 2026-08-01 确认的最小模型**

- 新增一个深的 Decision Work Module，状态放在 `.ai/decision-work/` 不可变 sidecar；不往 R2 的 `state.json` 增加 job scheduler，也不在 Map 目录内创建会被 R2 判为非法的旁文件。
- Module 继续只暴露 `inspect / plan / apply / verify`。内部 operation 至少覆盖：准备 attempt、记录 result、显式吸收 result；具体文件、锁、哈希、乱序和恢复逻辑都藏在 Implementation 内。
- 一个 attempt 由不可变 `task.json` 和至多一个不可变 `result.json` 组成。当前状态由文件是否存在、当前 UTC 与 R2 Map 状态派生，不维护第二份可漂移的 mutable status。
- Task Packet 只包含 Decision 问题、已确认上下文、约束、预期输出、work type 与 task digest；不包含 Claim token、项目写权限或原始对话。helper 是纯 worker，只返回 Result Envelope，不写 `.ai/` 或 Decision Map。
- Result Envelope 使用严格 schema 和 work type discriminator。公共结果区分 `candidate / needs_input / failed / cancelled`；`needs_input` 终结当前 attempt，后续以显式 predecessor 新建 attempt 接续，不覆盖旧结果。超时由 Claim Lease 到期派生；迟到结果可作为不可变参考保存，但不能绕过当前 claim 自动吸收。
- 吸收时机械校验 task/result 哈希、Map/Decision/attempt 绑定、result 为 candidate、Decision 仍可解决、当前 owner/token 有效以及 R2 base revision 未过期；随后只通过 R2 Module 提交 `resolve`。重复吸收依赖 R2 operation receipt 幂等。

**四种工作类型的职责**

- `research`：查外部事实、文档、代码库或知识库；允许对用户或协调器显式选择的多个独立 Frontier Decision 受控并行，结果必须给 findings、source/evidence pointer 与不确定项。
- `prototype`：产出便宜、可丢弃的实验或交互实物供人判断；artifact 本身不是 resolution，必须带观察结果和人类评价后才能形成候选结论。
- `grilling`：通过真实问答暴露假设并形成取舍；不得由 helper 自问自答伪造人的偏好，因此保持 HITL，由协调器会话承接。
- `task`：完成解除决策阻塞所需的前置动作或真实链路验证；不得借机实现最终交付物，也不自动进入 P4。

**并行与选择规则**

- v1 只允许 `research` 一次准备多个 attempt；prototype、grilling、task 每次只处理一个 Decision。
- 并行集合必须由调用方从 inspect 返回的 Frontier 中显式选出 Decision ID，并逐项通过 R2 claim；prepare 随后验证它们属于同一 Map、仍 open、依赖已 resolved、互不重复且当前 Claim 匹配。Decision 被 Claim 后不再属于当前 Frontier，不制造“已领取且仍是 Frontier”的矛盾；也不由模型按“第一张”或内部置信度自动选票。
- 并行 worker 只在隔离临时目录工作并返回有界 JSON；协调器串行记录结果、逐个显式吸收。并行的是求证，不是 Map 写入。

**Project Type / Active Profiles**

- 项目是 Python 驻留工具 + Markdown 规则真源 + Claude/Codex/Pi 薄适配的规则仓；本轮没有命中特定 Domain / Stack Profile，仅按通用 SOP、现有 Python 测试与双宿主合同推进。

## Scope

**In Scope**

- 定义 Task Packet、Result Envelope、attempt identity、不可变 sidecar 布局和 canonical evidence pointer。
- 实现 Decision Work Module 的四动作 Interface、严格 schema、零写 plan/inspect/verify、原子 task/result 发布与跨会话恢复。
- 让 `absorb` 复用 R2 Decision Map Module 完成唯一状态写入，并覆盖 stale revision、过期/替换 claim、重复、乱序、失败、取消和迟到结果。
- 为四种 work type 写清执行约束；为 research 定义显式 Frontier batch 和 host-neutral helper packet，不把某家子 agent 工具写进核心合同。
- 更新帮手名册/Ideation 指针、驻留工具部署说明、专项测试与完整 CI，保持 R1/R2 零回归。

**Out of Scope**

- R4 的 Milestone 路线引用 Decision、Iteration Admission、promotion plan/apply/receipt、P2 冻结后的变更分流和 Map 归档。
- 新增用户入口或 workflow registry ID；按模型的清晰度、大小或置信度自动创建 Map、选择 Decision、决定并行度或吸收结论。
- 多 active Iteration、并行 P4、跨主机调度、网络文件系统一致性、外部 tracker 或长期通用 job scheduler。
- 把 prototype/grilling/task 强行后台化；v1 只规范它们的输入输出和吸收，不替代现有 HITL 对话与工具。

## Open Questions / Risks

- P1 已确认：“Research 才允许多项并行；其余三类保持单项/HITL”，且“helper 完成永不自动 resolve，必须显式 absorb”。
- 并行批次需要硬上限以避免失控；建议 v1 `1..8`，并要求调用方显式给出 `max_parallel`，默认 `1`。这是资源安全阈值，不是需求大小判断。
- Sidecar 会积累不可变 attempt/result；R3 只保证按 Map/Decision 有界读取与校验，不做删除或压缩。归档与生命周期跟随 Map 的规则留给 R4。
- Host 是否真正支持 fresh-context / parallel worker 属 Adapter 能力；核心 Module 只保证 packet/result 合同。宿主不支持时必须串行执行并如实标注，不能伪称并行或独立。
