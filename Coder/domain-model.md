---
title: Butler 限界上下文地图
audience: AI / 开发者
scope: L1 核心概念边界、语义所有权、渐进读取与审计导航；不保存术语全集、状态枚举或执行算法
---

# Butler Domain Model

## 1. 定位

本文件是 L1 上下文地图，只回答“概念属于哪个问题范围、由谁拥有、下一步去哪里查”。规则分层仍见 `architecture-overview.md`；具体术语见 `domain-glossary.md`；字段、枚举与算法始终由所指真源拥有。

普通单模块任务不读本文件。仅在跨模块所有权、同名状态消歧、真源冲突或新增 Butler 核心术语时进入 L1；定位完成后按当前问题下钻，不批量展开指针。

## 2. 五个限界上下文

| 上下文 | 目的 | 语义所有权 | 明确不负责 | 首要真源 |
|---|---|---|---|---|
| 需求与范围 | 保存需求来源、钉住规格并限定允许影响的工作区 | PRD、外部参考、Workspace Scope | 不决定迭代阶段、完成资格或宿主权限 | `Coder/40_Context_Management/references-schema.md` |
| 交付生命周期 | 把方向拆成迭代并推进 P1→P5 | Milestone、Route Item、Iteration、Phase、阶段产物、Plan Verdict | 不把任务勾选当完成证明，不重定义外部规格 | `Coder/20_Workflow_Lifecycle/lifecycle.md` |
| 可信保证 | 定义完成义务、证明强度、审查与收口资格 | AC、Goal、Evidence、Review Verdict、Completion Eligibility | 不分配迭代号，不把 eligible 写成 complete | `Coder/20_Workflow_Lifecycle/goal-contract.md` |
| 宿主运行时 | 解析施工根和配置，在宿主中执行模式、权限与门禁 | Project Root、Project Config、Dangerous Mode、Convergence Loop、hook | 不改变需求语义，不用模式开关扩大文件授权 | `Coder/00_System_Prompt/logic-protocol.md` |
| 知识连续性 | 让新会话恢复断点与项目全貌 | Handoff、Project Knowledge Folder、task-state、历史导航 | 不重新定义生命周期状态，不让摘要覆盖权威产物 | `Coder/40_Context_Management/context-persistence.md` |

主链关系：需求与范围提供钉版输入，交付生命周期组织工作，可信保证决定是否足以继续或收口，知识连续性负责恢复而不改写事实；需要输入、输出、保真与失效细节时按需读 `Coder/context-map.md`，不在 L1 展开。

## 3. 渐进读取路径

| 路径 | 触发 | 读取 | 停止条件 |
|---|---|---|---|
| 普通冷启动 | 单模块、无概念歧义 | L0 → 目标专项规则 | 目标规则足以完成任务；不读 L1–L3 |
| 单术语消歧 | 已知待查术语 | L0 → L2 对应行 → 首批直接真源 | 证据足够即停 |
| 跨上下文设计 | 所有权、同名状态或真源关系跨模块 | L0 → L1 → 必要 L2 行 → 首批直接真源 | 边界与合同足够即停 |
| 完整领域审查 | 用户显式要求审计、追溯或冲突取证 | L0 → L1/L2 建索引 → L3 分段证据 | 审计范围覆盖或外部条件不足 |

直接真源每批最多 3 份。若仍不足，先压缩前批事实并产出一条扇出升级回执，包含：

- 当前问题
- 已知结论
- 缺失证据
- 已读来源
- 下一批来源
- 选择理由

短任务把回执写入用户可见的进度更新；跨会话 Butler 任务还要同步 `.ai/task-state.md`。下一批仍最多 3 份，可继续分批、显式升级 L3，或在缺外部条件时诚实阻塞。禁止递归追随引用、整目录读取或因预算不足伪造结论。

## 4. L3 审计入口

L3 保存完整历史与冲突证据，不进入普通冷启动、单术语或跨上下文设计的默认读取链：

- R1 冻结范围与验收：`.ai/iterations/ITER-0099/AC_LIST.md`
- R1 人类交付摘要：`deliveries/ITER-0099-domain-model-boundaries.md`
- 当前已知语义债务：`.ai/project/debt.md`

历史证据只读；新的执行定义仍回到各上下文真源修改，不复制回本地图或术语表。
