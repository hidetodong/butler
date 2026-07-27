---
title: Goal Contract 与派生状态规范
audience: AI / 开发者
scope: 非极小任务的目标组成、状态推导、完成候选、层级关系与宿主投影边界
---

# Goal Contract

## 1. 目标

Goal 不是“待办是否全勾”的别名，而是对结果的可审计承诺。Butler 不新增 `.ai/GOAL.md`：Goal 是从既有阶段产物派生的逻辑视图，避免 objective、AC、方案、进度和证据在第二台账重复后漂移。

本规范定义共同合同与状态语义；方案准入由 `tech-plan-schema.md` 提供结构化 verdict，问题回流、完成裁决器和 Claude/Codex 投影分别由 MILE-0008 R4–R6 承接。当前机械门只保护“显式非 pass 不进入源码执行”，不得表述成已能判断方案内容正确或 Goal 已有最终裁决器。

## 2. 两层 Goal 视图

### 2.1 Iteration Goal

| 合同槽 | 唯一真源 | 回答的问题 |
|---|---|---|
| Objective | `.ai/CONCEPT.md # Goal` | 本轮要达成什么结果 |
| Scope / Non-goals / Constraints | `CONCEPT.md` + `AC_LIST.md` | 哪些算本轮、哪些明确不做、受什么约束 |
| Outcome obligations | `.ai/AC_LIST.md` | 什么叫完成、如何验证 |
| Plan | `.ai/TECH_PLAN.md` | 用什么方案兑现 obligations |
| Progress | `.ai/task-state.md` | 当前执行到哪里；仅投影，不证明完成 |
| Proof | `.ai/VERIFY_REPORT.md` + evidence | 各 obligation 是否有可复核证明 |
| Verdict | review + iteration close state | 是否有 Must Fix、是否允许收口 |

### 2.2 Milestone Goal

| 合同槽 | 唯一真源 | 回答的问题 |
|---|---|---|
| Objective / Non-goals | `.ai/MILESTONE.md` 范围评估与关键交付目标 | 大版本承诺什么、不承诺什么 |
| Outcome obligations | `.ai/MILESTONE.md` 路线图 + 各归属迭代 AC | 哪些独立切片共同构成版本结果 |
| Progress | 路线项状态 + 两份台账归属 | 版本推进到哪里 |
| Proof / Verdict | 各迭代归档/交付/evidence + 里程碑收口审计 | 整体是否有资格关闭 |

里程碑 Goal 不覆盖迭代 Goal；它聚合各迭代结果。迭代 closed 也不自动等于里程碑 complete，必须等全部版本义务和里程碑收口仪式完成。

`.ai/MILESTONES.md` 待办区与 `.ai/milestone-backlog/` 里的未编号草稿尚未正式开启，**不派生 Milestone Goal**。只有候办草稿按 `milestone-schema.md` §7.1 提升、领取 `MILE-NNNN` 并成为 `current` 后，上表的合同槽才生效。

## 3. 派生状态机

封闭状态集合：`active`、`at-risk`、`blocked`、`completion-candidate`、`complete`、`abandoned`。

### 3.1 推导优先级

按下列顺序命中即停，禁止模型挑一个听起来顺耳的状态：

1. **终态优先**：台账为 `abandoned` → `abandoned`；台账为 `closed` 且收口产物/证据/交付一致 → `complete`。终态出现确定性漂移时不是降回 active，而是由状态审计报错并修复事实。
2. **真正阻塞**：任务尚未终态，且缺外部条件、权限或用户决策，当前无法安全取得任何有意义进展 → `blocked`。只是困难、测试失败或仍可修复，不算 blocked。
3. **已知风险**：任务尚可推进，但 TECH_PLAN 为 `draft/revise`、`goal-calibration.md` 存在 completion-blocking open signal、范围漂移、失败验证、Must Fix、未覆盖 outcome 或会阻止完成的剩余问题 → `at-risk`。校准投影为 blocked 且当前无法安全推进时按上一条派生 `blocked`。
4. **完成候选**：计划内执行任务已完成，没有已知 blocked/at-risk 条件，但 P5 proof/verdict 或收口仪式尚未完成 → `completion-candidate`。
5. **其余进行态**：已开启且仍在正常分析、设计、实现或验证 → `active`。

### 3.2 状态不是新台账字段

- `task-state.md` 可回声当前派生状态和原因，供冷启动续接；它是缓存，可随真源重新计算。
- 不向 `.ai/ITERATIONS.md` 增加上述状态。迭代台账仍只允许 `active / closed / abandoned`，避免与 lifecycle 状态混成一列。
- 不创建 `.ai/GOAL.md`、`.ai/GOALS.md` 或宿主专属 Goal 状态副本。

## 4. 完成候选不是完成

`completion-candidate` 专门切断“tasks done → complete”的错误捷径：

- TECH_PLAN 的 Execution Steps 全勾，只能说明计划动作完成。
- 至少还要逐 AC 生成 proof、完成 review verdict、处置阻断风险并执行收口仪式。
- 任一 AC 无覆盖、evidence 缺失/失败、review 有 Must Fix、TECH_PLAN verdict 非 `pass` 或范围已漂移，状态回到 `at-risk` / `blocked`，不能停在完成候选；用户 ACK 与任务全勾都不能覆盖该 verdict。
- R1 fixture `GFC-002/003/004/008` 是本边界的负向 oracle；R5 应把它们接入机械裁决器。
- 里程碑对应语义：全部路线项和归属迭代均已 closed、关键交付目标无已知风险，但里程碑归档/版本级交付/台账收口尚未完成时，才是 `completion-candidate`；不能因最后一个迭代 closed 直接把里程碑写成 complete。

## 5. 允许与禁止跃迁

- `active ↔ at-risk`：发现问题或问题修复后正常往返。
- `active / at-risk → blocked`：只有真正无法安全继续时；条件恢复后回到对应进行态。
- `active / at-risk → completion-candidate`：必须先清零已知风险并完成计划动作，不得跳过。
- `completion-candidate → at-risk`：P5 或 review 发现问题时必须回流；不得为了保住完成进度压低问题等级。
- `completion-candidate → complete`：只能在 proof/verdict 与收口事实全部成立后派生。
- active iteration 由 `tools/goal-assurance/goal.py evaluate` 机械裁决 close eligibility；`eligible` 只允许执行收口，不等于 complete。工具拒绝 AC/plan/calibration/evidence/review/blocker 任一不一致；TECH_PLAN 显式声明 TDD cycle 时还必须通过 Red→Green 配对检查，未声明则 N/A。裁决器不读取 host/tasks 作为绿依据。
- `complete / abandoned` 是终态；后续新需求开新迭代，不能把历史归档静默改回 active。
- 禁止 `active → complete`、`tasks done → complete`、`host complete → project complete` 三类直跳。

## 6. 层级与宿主投影

- 项目 `.ai/` 共同状态永远优先于 Claude/Codex 的原生 Goal/Task UI。
- 宿主投影可丢失、可重建，只显示 objective、派生状态、阻断原因与下一步指针；不得把宿主 complete 反向写成项目 closed。
- 两端能力不对称时保持诚实降级：有原生 Goal 就投影，没有就只靠 `.ai/` 运行，不维护第二套替代文件。
- 当前 Codex Goal 合同仅是 R1 的 `observed-current-session`；具体适配必须由 R6 当场核验，未知 Claude 能力不得猜测。

### 6.1 双宿主投影协议

Claude/Codex 均只投影四项：iteration/milestone objective、派生 state、blocking reason、next step。写入方向永远是 project `.ai/` → host；宿主 UI 的 done/complete 不得反写台账、AC、plan 或 VERIFY。

每次会话按 capability-detect 执行：宿主提供原生 Goal/Task 工具时更新上述薄投影；未提供、调用失败或能力未知时，不伪造成功、不建宿主替代文件，只用 `.ai/task-state.md` 与 `02_SESSION_HANDOFF.md` 继续。两条路径的完成资格都由 `tools/goal-assurance/goal.py` 裁决，语义完全一致。

## 7. 极小任务降级

极小任务没有持久阶段产物时，不强制构造 Goal 文件或状态缓存；对话中仍须说明 objective、完成条件和验证结果。若任务升级为简化/完整路径，再按 lifecycle 补产物并启用本合同。

## 8. 与后续路线的边界

- R3：已由 `tech-plan-schema.md` 与共享 phase gate 把“方案未获准”变成结构化 verdict 和 P4 写门。
- R4：已由 `goal-calibration.md` 把 at-risk/blocked 原因投影并路由到 P1–P5、修订或新迭代。
- R5：实现只读 Goal 视图与完成裁决，机械消费 R1 fixture。
- R6：把派生视图投影到 Claude/Codex，并验证降级路径。
