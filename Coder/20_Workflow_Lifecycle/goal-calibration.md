---
title: Goal 运行时校准与问题回流
audience: AI / 开发者
scope: P4/P5 新事实的分类、Goal 状态影响、task-state 投影、阶段回流与重新取得完成资格
---

# Goal Calibration

## 1. 目标

执行不是照旧计划把任务勾完，而是持续用新事实校准 Goal。只要实现、测试或审查揭示原目标、AC、方案或证明有问题，就必须先亮为 `at-risk / blocked`，回到正确层修复；禁止把坏消息只写进总结后沿旧计划继续并宣布完成。

本规则不新增 `.ai/ISSUES.md` 或第二套问题台账。事实仍以 CONCEPT、AC、TECH_PLAN、代码、evidence 和 review 为真源；`.ai/task-state.md` 只保存当前未闭合信号、影响和下一步，是可重算的运行投影。

## 2. 六类校准信号

封闭分类如下。按“事实改变了哪一层”分类，不按“在哪个阶段发现”分类：P5 发现方案错误仍是 `assumption-invalidated` 或 `scope-drift`，应回 P3/P2，而不是留在 P5 写风险。

| Signal | 触发事实 | 典型来源 |
|---|---|---|
| `implementation-deviation` | 实现偏离已通过方案/AC，或实现自身有缺陷 | diff、运行探测、代码阅读 |
| `assumption-invalidated` | TECH_PLAN 关键假设被事实推翻，原方案不再可靠 | 集成结果、依赖行为、数据现实 |
| `scope-drift` | 发现目标/完成定义遗漏、范围变大或原边界不成立 | 新业务事实、接口影响面、用户修订 |
| `verification-failure` | 预期通过的自动/人测 evidence 失败、超时、不完整或结论冲突 | evidence record、人测回传 |
| `review-finding` | review 的 Must Fix、refuted AC 或会影响完成的 Should Fix | review verdict |
| `external-blocker` | 缺权限、外部条件或必要决策，当前无法安全取得有意义进展 | 环境、第三方、用户决策 |

同一事实可能暴露多个信号时，以最深真源为主、必要时拆行。例如测试失败只是症状，确认根因是方案假设失效后，主信号改为 `assumption-invalidated`，不能永远停在 `verification-failure` 修症状。

## 3. task-state 活跃投影

长任务出现信号时，立即在 `.ai/task-state.md` 增加 `# Goal Calibration` 表：

```md
| ID | Signal | Fact Source | Goal Impact | Route | Status |
|---|---|---|---|---|---|
| CAL-001 | assumption-invalidated | evidence:integration-tests | at-risk | P3 → TECH_PLAN draft | open |
```

- `ID`：本迭代内单调编号 `CAL-NNN`，只为引用稳定。
- `Signal`：§2 六类之一。
- `Fact Source`：指向代码、产物、review 条目或 evidence ID，不复制日志。
- `Goal Impact`：`at-risk` 或 `blocked`；无影响的普通执行笔记不进本表。
- `Route`：§4 的目标阶段和必须动作，不能只写“之后处理”。
- `Status`：`open / blocked / resolved`。工作区保留全部 open/blocked；resolved 只保留当前续接需要的最近结论，最终处置在 VERIFY/review/evidence 中可追溯。
- 没有信号时保留表头但不造占位数据行，在表外写“当前无未闭合信号（N/A）”；`—` 或自然语言不能冒充 Signal/Status 枚举值。

投影与真源冲突时重算投影，绝不反向篡改真源。不得靠把行删掉或把 `open` 手改 `resolved` 消除风险；resolved 必须满足 §6 的重新验证条件。

## 4. 按事实性质回流

| 事实改变的层 | Route | 必须动作 |
|---|---|---|
| Objective / non-goal / 根约束理解 | P1 | 更新 CONCEPT；重新经过下游 P2/P3 |
| Outcome obligation / AC / 验证定义 | P2 | AC_LIST 退 `draft`，按修订/扩张规则重新 ACK |
| 方案假设、接口、边界、关键决策或验证设计 | P3 | TECH_PLAN 退 `draft`，重做 Plan Admission；只有重新 `pass` 可 P4 |
| 实现没有兑现仍有效的 AC/方案 | P4 | 按 correction contract 修根因并重新探测 |
| proof 缺失、失败、不完整或互相冲突 | P5 | 产生新 evidence ID 重跑；失败 record 保留，不覆盖 |
| 真正无法安全推进 | honest stop | 标 `blocked`，写清所缺条件/决策；条件恢复后回对应阶段 |

发现阶段不提供豁免：P4/P5/review 任一处都可触发以上回流。完成旧步骤、时间已投入、用户说“继续”或危险模式自治都不能成为沿旧计划硬走的理由。

## 5. 修订、扩张与历史边界

- 未突破原影响面的 AC/方案修订留在当前迭代，但必须复用既有 `draft → ACK` 与 `draft → Plan Admission → pass` 门。
- 新增跨模块/契约/关键路径义务属于范围扩张，按 `iteration-schema.md` 开新迭代承接；不得塞进已冻结迭代。
- 已 `closed / abandoned` 的历史迭代不重开、不静默改归档；新发现开新迭代并引用历史事实。
- 仅实现缺陷且目标/AC/方案仍成立时留 P4，不为普通 bug 伪造范围变化。

## 6. Goal 状态与 resolved 条件

- 任一会阻止完成的 `open` 信号 → Goal 至少 `at-risk`，即使 Execution Steps 已全勾。
- `external-blocker` 或其他信号导致当前无法安全取得有意义进展 → `blocked`。
- 只有所有 completion-blocking 信号都按正确 route 处置，才能重新计算 `active / completion-candidate`。
- `resolved` 必须引用与问题匹配的新事实：P1/P2/P3 的重新确认/准入，P4/P5 的新 passed evidence，review Must Fix/refute 的定点复查。原失败 evidence 与 finding 保留。
- `defer` 只有在明确证明“不影响当前 Goal 完成资格”时才可转为 Remaining Risk；会影响完成的项不得换个词绕过。

禁止捷径：`tasks done → ignore signal`、`risk noted → continue old plan`、`delete row → resolved`、`closed history → reopen`。

## 7. P5 回填与后续边界

VERIFY_REPORT 必须说明本轮发现过哪些 completion-blocking calibration signal、各自 route 和最终依据；仍 open/blocked 就不能把相应 AC 勾绿或收口。没有信号时明确写 N/A，不虚构条目。

R4 只定义记录与回流合同；R5 completion adjudicator 将机械读取 TECH_PLAN verdict、Evidence Index、review 和 task-state 未闭合信号，拒绝假完成。R6 再处理宿主投影。
