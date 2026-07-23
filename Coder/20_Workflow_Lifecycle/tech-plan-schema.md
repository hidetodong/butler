---
title: 技术方案模板
audience: AI / 开发者
scope: P3 Design 阶段的技术方案模板、方案准入状态、反证门、边界字段与验证规划口径
---

# Tech Plan Schema

> 结构机器真源：`tools/artifact-pipeline/artifacts.v1.json` + `templates/TECH_PLAN.md`。本文件解释字段语义；新 live 产物的 H2/方案状态由 manifest 固定，条件段 N/A 不删除，legacy 归档不追溯改写。

## 1. 目标

用于在进入实现前，把改动边界、关键设计决策与验证方式说明清楚。

## 2. 交付约定

- 必须产出：`.ai/TECH_PLAN.md`
- 必填 frontmatter：`方案状态`、`方案审查日期`、`方案审查方式`
- 必填字段：`Goal`、`Files / Modules to Change`、`Interface / Contract`、`State / Boundary`、`Design Decisions`、`Plan Admission`、`Execution Steps`、`Verification Plan`、`Risks / Open Questions`；AC 含 `prd_refs` 时还必须有 `Workspace Write Plan`
- 可选字段：`External References`（当 `.ai/references/` 下存在参考资料时必填）

## 3. 标准模板

```md
---
方案状态: draft
方案审查日期: —
方案审查方式: —
---

# Goal
- 本阶段要支撑哪些 AC

# Files / Modules to Change
- 计划修改的文件、模块或目录
- 每个改动点的职责

# External References
- .ai/references/api-xxx.md — 接口契约来源，影响 Interface / Contract 定义
- .ai/references/design-xxx.md — UI 规格来源，影响 Files / Design Decisions
- .ai/references/prd/2026-07-22-user-login/login-flow.md — PRD 切片来源（身份、版本、模块继承 AC frontmatter prd_refs，方案不自立版本），影响 Interface / Design Decisions

# Interface / Contract
- 涉及的接口契约
- 数据结构、输入输出或依赖关系
- 若接口定义来自外部参考资料，标注来源文件

# State / Boundary
- 状态边界
- 模块职责边界
- 明确不在本次处理范围内的扩展点

# Workspace Write Plan

| workspace_key | access | path_patterns | rationale |
|---|---|---|---|
| @acme/web | primary_write | [apps/web/src/**] | 核心实现 |
| @acme/ui | supporting_write | [packages/ui/src/login/**] | 配套组件 |

# Design Decisions
- 关键设计选择
- 取舍与原因
- 受哪些 active profiles 约束

# Plan Admission
- AC Coverage：逐项说明 AC 是否有设计和验证映射
- Assumptions：列关键假设及其验证方式
- Alternatives / Trade-offs：至少说明采用方案与被放弃方案的取舍；只有唯一合理方案时说明原因
- Failure Modes：主动寻找失败路径、边界输入与恢复策略
- Impact / Scope Challenge：检查影响面遗漏、范围膨胀和更小可行方案
- Verification Blind Spots：说明机器验证仍看不到什么，不把未知写成已覆盖
- Verdict：`pass / revise / blocked` + 一句话理由

# Execution Steps
- 按执行顺序列为可勾选任务项；每项绑定所服务的 AC，可标依赖与可并行（编号 T<n> 可选，小迭代可省）
- [ ] T1 <动词开头的可执行任务> → AC1
- [ ] T2 <…>（依赖 T1）→ AC2
- [ ] T3 [P] <可与 T2 并行的任务> → AC3
- 粒度随迭代大小：大迭代（多文件 / 可并行 / TDD）展开到任务级；小 / 简化迭代保持粗粒度实现顺序即可，不强制细拆

# Verification Plan
- 每个 AC 或关键改动点如何验证

# Risks / Open Questions
- 当前剩余风险
- 尚未关闭的问题
```

## 4. 编写规则

### 4.1 方案状态与准入

`方案状态` 是封闭枚举：`draft` / `pass` / `revise` / `blocked`。

- `draft`：方案已起草但尚未完成准入审查；不得进入 P4。
- `pass`：`Plan Admission` 已完成且没有已知 Must Fix；这是进入 P4 的唯一合法状态。
- `revise`：发现可在 P3 修复的设计缺陷；修订时先退回 `draft`，完成全项重审后再判定。
- `blocked`：缺外部条件、权限或必须由用户决定的关键取舍，当前无法安全完成方案；诚实停机，条件恢复后退回 `draft` 重审。

`方案审查日期` 记录 verdict 当日日期；`方案审查方式` 记录 `user-ack`、`dangerous-self-review` 或项目定义的等价可审计方式。标准模式的用户 ACK 只确认一份已通过结构审查的方案，不能覆盖已知 Must Fix；危险模式按 `dangerous-engine.md §5.2` 自审。

TECH_PLAN 任何实质修改（AC 映射、接口、边界、关键决策、步骤或验证方法变化）都使旧 verdict 失效，必须先置回 `draft` 并重新执行全部 Plan Admission。只修错字或链接不触发重审。

新产物不得省略上述 frontmatter。共享 hook 对已存在但非 `pass` 的状态 fail-closed；无 `方案状态` / `plan_status` 字段仅作为旧版部署兼容而放行，**不是**新方案的合法省略方式。

### 4.2 内容与边界

- 必须能映射回已确认的 AC，禁止脱离验收标准独立扩张。
- 文件范围、接口契约、边界与验证方式必须明确。
- 若存在 active profiles，应写明其约束点；未命中时只按通用 SOP 与质量门禁设计。
- 若 `.ai/references/` 下存在已处理的外部参考资料，必须在 `External References` 中列出，并在 `Interface / Contract` 和 `Design Decisions` 中标注哪些决策来源于参考资料。
- 引用需求集合切片时，技术方案逐项继承 `AC_LIST.md` 的 `prd_refs`，不得改 `prd_id`、升级某项版本、扩大 `module_slugs` 或另立版本表；路径带 `prd_id`，精确解析回指 `acceptance-schema.md §5`。
- legacy 旧迭代只有 `prd_version` 时继续按兼容 resolver 读取；新 TECH_PLAN 不把 legacy 字段转换成自造 `prd_refs`，迁移身份由 migration receipt 提供。非 PRD 方案保持不写引用字段。
- AC 含 `prd_refs` 时，`# Workspace Write Plan` 必须使用精确表头 `workspace_key | access | path_patterns | rationale`；字段、权限交集与扩张纪律以 `workspace-scope-schema.md §8` 为真源。P3 准入前运行 `check-plan`，不得用宽目录或计划外写入替代 PRD 范围扩张。
- 不把执行细节写成流水账，重点保留关键设计与实现边界。
- `Execution Steps` 列为可勾选任务清单：每项一行、动词开头、绑定所服务的 AC（`→ ACn`）；有依赖标"依赖 T<m>"、可并行标 `[P]`；任务编号 `T<n>` 建议但不强制，小迭代可省。
- 任务清单粒度随迭代大小：大迭代（多文件 / 可并行 / TDD）展开到任务级；极小 / 简化路径保持粗粒度实现顺序即可，不强制细拆，避免过度工程。
- 任务清单是**计划态**单一存放处；P4 执行时的活进度（已完成 / 进行中 / 下一条）镜像到 `.ai/task-state.md`（见 `40_Context_Management/context-persistence.md §4`），不在本字段反复改勾，AC 仍是验收脊柱、任务不取代 AC 回填。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）；任务清单的书写细节见 `artifact-style.md`「Execution Steps 任务清单书写」节。

## 5. 与执行流程的关系

- P3 阶段必须产出 `.ai/TECH_PLAN.md`，完成 Plan Admission 并得到 `pass`，才可作为 P4 执行的唯一边界依据。
- P3 从 `.ai/AC_LIST.md` 读取输入，逐项映射验收项。
- P4 阶段实现必须逐项遵循这里的边界与执行顺序。
- 若设计影响面扩大，应回退到 P3、把状态退回 `draft`、更新此文件并重新准入。
- 简化路径下可口头确认方案，不强制产出此文件。
