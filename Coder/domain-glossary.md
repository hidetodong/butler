---
title: Butler 核心术语查询表
audience: AI / 开发者
scope: L2 高风险术语的上下文限定、白话定义、语义所有者与定义真源；按相关行查询，不作为冷启动全文
---

# Butler Domain Glossary

## 1. 使用方式

本文件是 L2 查询表，不进入普通冷启动。已知术语需要消歧时，只读取相关行，再沿该行的定义真源读取首批最多 3 份文档；字段、封闭枚举和执行算法仍以定义真源为准。

## 2. 术语

| 概念 | 上下文限定 | 白话定义 | 语义所有者 | 定义真源 | 明确不代表 |
|---|---|---|---|---|---|
| PRD | 需求与范围 | 一份独立需求的可版本化规格集合，以稳定 `prd_id` 寻址 | 需求与范围 | `Coder/40_Context_Management/references-schema.md` | 项目唯一文档、里程碑或实现计划 |
| Workspace Scope | 需求与范围 | 某份需求允许写、配套写、只读或排除的稳定工作区集合 | 需求与范围 | `Coder/40_Context_Management/workspace-scope-schema.md` | 宿主文件权限、TECH_PLAN 的具体写路径 |
| Milestone | 交付生命周期 | 聚合多个迭代的大版本范围单元，正式开工才领取 `MILE-NNNN` | 交付生命周期 | `Coder/20_Workflow_Lifecycle/milestone-schema.md` | 单次迭代、未编号候办、发布 tag |
| `active`（Milestone） | 交付生命周期 | 当前唯一正在推进并自动接收新迭代归属的里程碑状态 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/milestone-schema.md` | 迭代 active、路线项 active、Goal active |
| Route Item | 交付生命周期 | 里程碑内“一项方向约等于一个迭代”的规划切片 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/milestone-schema.md` | 未开工迭代、任务子项 |
| `planned/active`（Route Item） | 交付生命周期 | 路线项的规划状态；planned 尚无迭代号，active 已绑定真实迭代 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/milestone-schema.md` | `.ai/ITERATIONS.md` 的迭代状态 |
| Iteration | 交付生命周期 | 一轮冻结验收范围并走完 P1→P5 的可独立收口单元 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/iteration-schema.md` | 对话回合、任务步骤、路线项 |
| `active`（Iteration） | 交付生命周期 | 当前唯一占用工作区五件套、尚未收口的迭代状态 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/iteration-schema.md` | 里程碑 active、Goal active、路线项 active |
| Lifecycle Phase | 交付生命周期 | P1 分析、P2 验收、P3 设计、P4 执行、P5 验证中的一个阶段 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/lifecycle.md` | 迭代、宿主任务状态 |
| Acceptance Criterion | 可信保证 | 一条可验证的完成义务，贯穿设计、实现和验证 | 可信保证 | `Coder/20_Workflow_Lifecycle/acceptance-schema.md` | 执行步骤、Goal 状态、测试用例本身 |
| `pass`（Plan Verdict） | 交付生命周期 | TECH_PLAN 反证审查后没有已知 Must Fix，允许进入 P4 | 交付生命周期 | `Coder/20_Workflow_Lifecycle/tech-plan-schema.md` | Review pass、测试通过、Goal complete |
| Goal | 可信保证 | 从目标、范围、AC、方案、进度、证据和收口事实派生的结果承诺 | 可信保证 | `Coder/20_Workflow_Lifecycle/goal-contract.md` | 第二台账、Task done、宿主 complete |
| Evidence | 可信保证 | 对真实命令、结果、日志和哈希的机器记录，用来支撑 AC 结论 | 可信保证 | `tools/verification-evidence/README.md` | 对话自述、测试名称、未捕获的“已通过” |
| `pass`（Review Verdict） | 可信保证 | 审查没有未解决 Must Fix；只说明审查门，不替代验证和收口 | 可信保证 | `Coder/60_Extension_CodeReview/review-engine.md` | Plan pass、Evidence passed、Goal complete |
| Completion Eligibility | 可信保证 | active 迭代满足收口前机器条件的裁决结果 eligible | 可信保证 | `Coder/20_Workflow_Lifecycle/goal-contract.md` | 已收口、complete、自动执行收口 |
| Project Root | 宿主运行时 | 本次允许读写项目级 Butler 状态的唯一施工根 | 宿主运行时 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md` | 会话 cwd、工作区父目录、文件权限授权 |
| Dangerous Mode | 宿主运行时 | 用强制自审和审计替代人工把关的持久自治外壳 | 宿主运行时 | `Coder/65_Extension_Dangerous/dangerous-engine.md` | 文件权限扩大、跳过审查、Convergence Loop 本身 |
| Convergence Loop | 宿主运行时 | 在 P4 常驻纠错契约上显式开启的高强度纠错与定量熔断升档 | 宿主运行时 | `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` | Dangerous Mode、普通 P4、harness 循环 |
| Handoff | 知识连续性 | 从权威状态生成并可验鲜的当前会话断点入口 | 知识连续性 | `Coder/40_Context_Management/handoff-spec.md` | 权威状态、完整项目全貌、交付总结 |
| Project Knowledge Folder | 知识连续性 | 按主题保存项目当前全貌的常驻知识地图，收口时由变更增量折叠 | 知识连续性 | `Coder/40_Context_Management/project-digest-schema.md` | 迭代历史、handoff、规则算法真源 |

同名 `active` 与 `pass` 必须连同括号内命名空间使用，不能用裸词合并定义。需要完整历史、冲突证据或术语演进时，沿 `domain-model.md` 的 L3 入口分段审计。
