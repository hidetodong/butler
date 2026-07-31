---
title: Butler 主交付链上下文映射
audience: AI / 开发者
scope: PRD→AC→Plan→Evidence→Goal→Handoff 的跨上下文交接；不复制字段全集、状态枚举或执行算法
---

# Butler Context Map

## 1. 定位

本文件是按需读取的主链导航合同。它只说明跨上下文时带什么、保什么、何时拒绝、谁负责和事实归谁；字段、枚举与算法仍由每段列出的直接真源拥有。

只在设计或审计 PRD→AC→Plan→Evidence→Goal→Handoff 主链时读取。先从 `domain-model.md` 定位上下文，再只读当前转换块和首批最多 3 份直接真源；禁止递归追随引用或整目录展开。

## 2. 事实层级

| 层级 | 含义 | 写入边界 |
|---|---|---|
| 权威事实 | 决定当前需求、承诺、方案或项目状态的唯一记录 | 只能由所属 schema / 台账 / 阶段流程改变 |
| 受控投影 | 对外部规格或真实执行的可校验落盘表示 | 必须保留身份、版本、结果或 hash，不能反写来源 |
| 派生视图 | 从权威事实与受控投影计算出的状态、资格或恢复入口 | 可重建；冲突时服从上游，不得反写真源 |
| 叙述摘要 | 给人阅读的有损说明 | 只引用结论，不参与门禁或状态推导 |

## 3. 主链转换

### PRD→AC

- 源上下文：需求与范围
- 目标上下文：可信保证
- 输入：PRD 受控投影，或非 PRD 对话中已确认的目标与范围
- 输出：冻结的验收义务与验证方法
- 最小保真：需求集合保留 `prd_id + prd_version + module_slugs`；非 PRD 流保留目标、范围、排除项与可验证义务
- 失效条件：引用缺失、版本/模块冲突、冻结后跟随 live PRD 漂移，或需求语义无法唯一认领 → 修复：`Coder/20_Workflow_Lifecycle/acceptance-schema.md`
- 责任方：P2 Acceptance 冻结门；PRD 身份由需求与范围上下文拥有
- 权威关系：受控投影 → 权威事实；AC 钉版后不被 PRD live 反向改写
- 直接真源：`Coder/40_Context_Management/references-schema.md`；`Coder/20_Workflow_Lifecycle/acceptance-schema.md`

### AC→TECH_PLAN

- 源上下文：可信保证
- 目标上下文：交付生命周期
- 输入：已冻结 AC、范围、验证义务与钉版参考
- 输出：逐 AC 映射且通过准入的技术方案
- 最小保真：AC 身份、范围边界、验证义务和全部 `prd_refs` 原样继承；Execution Steps 只做计划投影
- 失效条件：AC 未冻结、方案漏映射、擅自升级 PRD/扩大模块、用任务替代 AC，或实质改动后沿用旧 verdict → 修复：`Coder/20_Workflow_Lifecycle/tech-plan-schema.md`
- 责任方：P3 Plan Admission；范围扩张回到 P2 重冻
- 权威关系：权威事实 → 权威事实；TECH_PLAN 拥有实现方案，但不重定义 AC 或 PRD
- 直接真源：`Coder/20_Workflow_Lifecycle/acceptance-schema.md`；`Coder/20_Workflow_Lifecycle/tech-plan-schema.md`

### TECH_PLAN→Evidence

- 源上下文：交付生命周期
- 目标上下文：可信保证
- 输入：通过准入的方案、冻结 AC 与实际验证命令
- 输出：机器 evidence record 与逐 AC 验证回填
- 最小保真：迭代/AC 身份、argv、cwd、outcome、日志 hash、证据强度和方案对齐结论；失败记录保留但不提供绿色覆盖
- 失效条件：方案非 pass、record 缺失/损坏、证据未绑定 AC、把 reported 冒充 reproduced，或失败 evidence 打绿 → 修复：`Coder/20_Workflow_Lifecycle/verify-schema.md`
- 责任方：P5 Verify 与 verification-evidence runner
- 权威关系：权威事实 → 受控投影；record 表示真实执行结果，不反写方案或 AC
- 直接真源：`Coder/20_Workflow_Lifecycle/tech-plan-schema.md`；`Coder/20_Workflow_Lifecycle/verify-schema.md`；`tools/verification-evidence/README.md`

### Evidence→Goal Verdict

- 源上下文：可信保证
- 目标上下文：可信保证
- 输入：AC 覆盖、plan verdict、calibration、evidence、TDD 配对、review、blocker 与迭代台账事实
- 输出：Goal close eligibility；收口后才可由一致事实派生 complete
- 最小保真：迭代身份、全部 outcome obligations、证明结果、阻断/反证和收口事实；`eligible` 必须与 `complete` 分离
- 失效条件：任一输入缺失/矛盾、Must Fix 未清、失败证据被忽略、host/tasks 被当绿依据，或 eligible 直写 complete → 修复：`Coder/20_Workflow_Lifecycle/goal-contract.md`
- 责任方：Goal Assurance 只读裁决器；生命周期收口仪式改变台账事实
- 权威关系：权威事实 + 受控投影 → 派生视图；Goal verdict 可重算且不得反写输入
- 直接真源：`Coder/20_Workflow_Lifecycle/goal-contract.md`；`Coder/20_Workflow_Lifecycle/verify-schema.md`；`tools/goal-assurance/README.md`

### Goal/权威状态→Handoff

- 源上下文：交付生命周期、可信保证
- 目标上下文：知识连续性
- 输入：当前台账、task-state、阶段产物、里程碑和可重算 Goal 状态
- 输出：`02_SESSION_HANDOFF.md` 与新鲜度 receipt
- 最小保真：当前迭代/里程碑、阶段、状态、关键决策、风险、下一动作、状态指针和来源指纹
- 失效条件：来源已变化、current 与状态矛盾、指纹不符、源状态非法，或 handoff 被用来反写上游 → 修复：`Coder/40_Context_Management/handoff-spec.md`
- 责任方：handoff generator 负责生成与 check；新会话只消费 fresh 结果
- 权威关系：权威事实 + 派生视图 → 派生视图；handoff 可重建、不可审批或覆盖上游
- 直接真源：`Coder/40_Context_Management/handoff-spec.md`；`Coder/40_Context_Management/context-persistence.md`；`tools/handoff/README.md`

## 4. 停止与修复原则

- 当前转换块和直接真源足以回答问题即停止，不继续展开上下游全部文档。
- 发现失效时回到该块标明的修复真源；导航合同、Goal 或 Handoff 都不能代替所有者修改事实。
- 需要改变字段、枚举或算法时修改相应直接真源，并同步本文件的最小保真摘要；不得把执行合同搬进本文件。
