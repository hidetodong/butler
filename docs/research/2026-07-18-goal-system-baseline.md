---
title: Butler 目标体系现状基线与假完成失败模型
audience: Butler 规则维护者
scope: MILE-0008 R1 对目标载体、权威边界、宿主能力与后续路线输入的事实审计
---

# Butler 目标体系现状基线

## 1. 结论先行

Butler 不是没有目标相关规则，而是缺少一条统一的 **Goal 完成裁决链**。

现有规则已经分别定义了版本方向、迭代范围、目标理解、完成标准、技术方案、执行进度、验证证据和审查结论；但这些事实还没有被一个共同合同聚合成“此刻能否把 Goal 标成 complete”。因此宿主任务列表全部勾完、原生 Goal 被更新为 complete，仍可能与项目内 AC、证据或审查真相冲突。

R1 只冻结这个事实与负向 oracle。它不决定未来应该新增独立 Goal 文件，还是从现有产物派生 Goal 视图；该选型留给 R2。

## 2. 来源等级

| 等级 | 含义 | 可否作为共同规则长期依赖 |
|---|---|---|
| `documented-butler` | Butler 仓内已有规则、schema、台账或工具合同 | 可以，但后续修改仍须保持真源单一 |
| `observed-current-session` | 当前 Codex 会话实际暴露的能力合同 | 只能用于 R1 能力盘点，R6 接线时必须重新核验 |
| `unknown` | 当前没有可验证合同或两宿主能力不能证明对称 | 不可以；必须降级或停在项目内共同状态 |

## 3. 目标与完成载体盘点

| 载体 | 层级 / 角色 | 当前权威度 | 主要消费者 | 当前完成语义 | 来源 |
|---|---|---|---|---|---|
| `.ai/MILESTONE.md` | 大版本方向、关键交付目标、路线图 | 版本方向真源 | milestone/iteration 路由、版本交付 | 路线全部 closed 后才可收口；不冻结单迭代 AC | `documented-butler` |
| `.ai/ITERATIONS.md` 迭代表 | 单轮范围索引与 active/closed/abandoned | 迭代身份和归属真源 | lifecycle、auditor、冷启动 | 行状态只表示迭代生命周期，不单独证明 AC 达成 | `documented-butler` |
| `.ai/ITERATIONS.md` 危险模式北极星 | 无人值守场次跨迭代保持的总需求方向 | 自治方向真源，不是完成裁决 | dangerous master loop、跨会话恢复 | 指导是否继续开下一迭代；不能凭一句“整体达成”绕过各迭代证据和强审 | `documented-butler` |
| `.ai/CONCEPT.md # Goal` | P1 对本轮要解决问题的结构化表达 | 目标理解真源 | P2 | 目标变化必须回 P1；没有独立完成状态 | `documented-butler` |
| `.ai/AC_LIST.md` | In/Out Scope、可验证完成定义 | 单迭代完成定义真源 | P3、P4、P5、phase gate | `ack-frozen` 只表示范围冻结，不表示 AC 已满足 | `documented-butler` |
| `.ai/TECH_PLAN.md` | AC 到改动、契约、任务和验证的方案映射 | 方案真源 | P4、P5 alignment | 当前只有危险模式 P3 自审要求，没有通用机器可读方案 verdict | `documented-butler` |
| `.ai/task-state.md` | 已完成/进行中/下一任务的运行投影 | 续接指针，不是验收真源 | 冷启动、handoff | 任务完成只表示执行进度，规则明确不取代 AC 回填 | `documented-butler` |
| `.ai/VERIFY_REPORT.md` + evidence | 逐 AC 结果、机器记录、置信与剩余风险 | 验证事实真源 | P5、auditor、交付 | 自动 AC 没有 passed record 不得勾选；弱/待人不得冒充可靠 | `documented-butler` |
| review verdict | Must Fix / Should Fix 与断言核对 | 审查裁决真源 | P5、修复回流 | Must Fix 阻断收口；Should Fix 必须留风险 | `documented-butler` |
| `.ai/RUN_LOG.md` | 危险模式自主 ACK、路线变更和强审轨迹 | 自治审计真源 | 事后复盘 | 证明模型如何自决，不替代 AC、证据或 review | `documented-butler` |
| delivery + closed ledger | 已收口的人读总结和索引 | 交付结果，不是原始证明 | 人类读者、auditor | 必须由前序闭环产生；不能反向用“已有交付文件”证明目标达成 | `documented-butler` |
| Codex Goal（当前会话） | objective 与 active/complete/blocked 生命周期 | 宿主运行投影 | Codex harness | 当前合同要求目标真正达成且无剩余必做工作才 complete；本身不审查 Butler AC/plan/evidence | `observed-current-session` |
| Claude 原生 task/goal | 可能存在的宿主任务载体 | 未建立映射 | Claude harness | Butler 当前没有可验证的统一 Goal 接线合同 | `unknown` |
| Butler plugin skills | 发现并路由 8 个工作流 | 入口适配，不是目标状态 | Codex | skills 能执行规则，但 plugin manifest/skill 不保存项目 Goal 真相 | `documented-butler` |

## 4. 层级边界与不可替代关系

| 问题 | 唯一回答位置 | 不能被什么替代 |
|---|---|---|
| 这个大版本为什么做、分几条路线？ | `MILESTONE.md` | 宿主 Goal 标题、单轮任务清单 |
| 当前这一轮圈定什么范围？ | `ITERATIONS.md` + `CONCEPT.md` | milestone 路线标题、对话记忆 |
| 什么叫本轮完成？ | `AC_LIST.md` | tasks 全勾、代码已写、Goal UI 显示 complete |
| 准备用什么方案达成？ | `TECH_PLAN.md` | AC 本身、执行日志 |
| 目前做到哪一步？ | `task-state.md` | AC 勾选、VERIFY 最终结论 |
| 实际是否满足 AC？ | `VERIFY_REPORT.md` + evidence | 测试命令文本、口头 passed、task-state |
| 是否仍有必须修的问题？ | review verdict | 作者自述、测试全绿 |
| 是否允许收口？ | 现行 iteration/milestone close discipline | 单独的宿主 complete 动作 |

由此得到一个 R2 必须保留的不变量：**Goal 状态若存在，只能聚合和投影这些真源，不能成为覆盖它们的新真源。**

## 5. 已有保障与缺口

### 已有保障

- P1→P5 强制产物链把目标理解、完成定义、方案和验证分开。
- `AC_LIST` 冻结门阻止未确认范围直接进入实现。
- `task-state` 已明确只是任务进度投影，不取代 AC。
- verification evidence 拒绝只靠口头/命令文本打绿。
- review 的 Must Fix 会阻断危险模式收口。
- state auditor 能对账台账、归档、交付、证据与发布状态。

### 仍缺的保障

- 没有统一 Goal Contract 指明 Goal objective、完成义务与项目真源之间的映射。
- 没有通用、结构化的方案 verdict；危险模式 P3 自审仍主要是散文结论。
- 没有 Goal completion candidate 阶段把 tasks done 与 outcome achieved 分开。
- 没有机械规则在宿主 complete 与项目内 `revise/blocked/Must Fix/evidence missing` 冲突时拒绝或回滚宿主状态。
- 没有标准回流矩阵把新问题路由到 P1/P2/P3/P4/P5 或新迭代。
- 双宿主没有明确“原生 goal/task 只是薄投影、共同 `.ai/` 才是真相”的接线合同。

## 6. 假完成失败模型

机器可读真源为 [`goal-failure-cases.v1.json`](goal-failure-cases.v1.json)。本节只给人读摘要，case ID 必须一一对应。

| Case | 失败情形 | 为什么不能 complete | 预期处置 | 后续路线 |
|---|---|---|---|---|
| `GFC-001` | 方案自审 verdict 仍是 revise，执行任务却全部完成 | 执行了未获准方案 | revise，回 P3 | R3 |
| `GFC-002` | Goal outcome 没有被任何 AC 覆盖 | 没有可验证完成定义 | revise，回 P2 | R2 |
| `GFC-003` | AC 被勾选，但没有 passed evidence record | 只有声称，没有可审计证明 | revise，留在 P5 | R5 |
| `GFC-004` | review 仍有 Must Fix | 已知阻断问题尚未修复 | revise，回 P4 | R5 |
| `GFC-005` | 关键剩余风险卡住下游且没有弱验证/隔离路径 | 目标依赖未满足 | blocked，诚实交还 | R4 |
| `GFC-006` | 实现影响面超出冻结 AC/plan，但没有回退重规划 | 当前目标和方案已失真 | revise，回 P2/P3 或新迭代 | R4 |
| `GFC-007` | 宿主 Goal 显示 complete，项目 iteration 仍 active 且 AC 未闭合 | 投影覆盖了项目真相 | revise，纠正宿主投影 | R6 |
| `GFC-008` | TECH_PLAN tasks 全部 done，但至少一个 AC 仍 failed/pending | 动作完成不等于结果达成 | revise，按失败 AC 回流 | R4/R5 |

## 7. 宿主能力边界

### Codex

当前会话可观察到：Codex Goal 接受 objective，维护活动目标，并允许最终更新为 complete 或 blocked；complete 只能在目标实际达成且没有剩余必做工作时使用，blocked 也有严格的真正阻塞条件。这与 Butler 想要的方向一致，但仍只是 `observed-current-session`：它没有自动读取 Butler 的 AC、evidence、review，也不能替代项目内完成裁决。

### Claude Code

Butler 仓已有 Claude commands、hooks 和 P1–P5 入口，但本轮没有找到一份 Butler 维护的“Claude 原生 Goal 状态 ↔ `.ai/` 真相”合同。因此能力标为 `unknown`，R6 不能凭名称相似假设与 Codex 对称。

### Plugin 与无原生 Goal 降级

Butler plugin 的 skills/hooks 能路由流程和观察部分写操作，但 plugin 本身不是 Goal 数据库。若宿主没有原生 Goal 能力，共同规则仍必须能仅靠 `.ai/` 完成；宿主投影缺失不能让项目状态失效。

## 8. R2–R6 输入与依赖

| 路线 | 必须消费的 R1 结论 | 不得跳过的前置 |
|---|---|---|
| R2 Goal Contract | §3–§4 的层级与不可替代关系；GFC-002 | 先决定 Goal 是独立对象还是派生视图，再定义最小状态机 |
| R3 方案准入 | TECH_PLAN 当前缺 verdict；GFC-001 | verdict 必须结构化、失败可回流，不能只加“请认真自审” |
| R4 执行校准 | GFC-005/006/008 | 新事实必须有 P1–P5/新迭代路由，tasks done 不能直接 complete |
| R5 完成裁决器 | GFC-002/003/004/008 | AC、evidence、review 和风险必须共同参与负向拒绝 |
| R6 双宿主接线 | §2、§7；GFC-007 | 重新核验当时宿主能力；原生状态只能投影共同真相 |

## 9. 明确延期的设计决策

- Goal 是新增 `.ai/GOAL.*` 持久对象，还是由现有产物派生：**deferred to R2**。
- 最终公共状态枚举和状态迁移：**deferred to R2**。
- 方案 verdict 放在 TECH_PLAN frontmatter、独立记录还是审计字段：**deferred to R3**。
- 问题回流是否需要机器 action code：**deferred to R4**。
- 完成裁决器是 auditor 子命令、独立驻留工具还是 hook：**deferred to R5**。
- Codex/Claude 原生 Goal/Task 的具体 API 与同步时机：**deferred to R6**。

R1 的完成只代表问题模型已冻结，不代表 Butler 已经能阻止假完成。
