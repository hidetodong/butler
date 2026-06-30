> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-06-30

# 一句话

butler 的 `.ai/` 现在只存"每个迭代改了什么"（变更流 delta）和"现在卡在哪"（瞬时 handoff），唯独没有一份"这系统现在整体是什么、为何如此、有哪些长期约束与欠债"的常驻全貌。长寿项目冷启动时，AI 只能从一堆迭代一句话 + 代码倒推整只豹——管中窥豹。本迭代新增 `.ai/PROJECT.md`：一份**状态取向**、有界、收口时前滚维护的项目摘要，做冷启动第一读。

# 背景与判断

- 冷启动信息源盘点：`02_SESSION_HANDOFF.md`=瞬时断点；`ITERATIONS.md` / `deliveries/`=变更流（N 条一行 delta）；`MILESTONE.md`=版本范围、松耦合可选；`task-state.md`=运行态。全是瞬时或 delta，**没有状态取向（全部 delta 的积分）的全貌产物**。
- `Coder/architecture-overview.md` 不顶用：butler 仓专属、手维护、不是通用 `.ai/` SOP 的一部分。
- 缺口结论：长寿项目冷启动缺一份"系统现在是什么 + 长期不变量 + 长期欠债"的常驻脊柱。这是 MILE-0001 的 R1。

# Goal

- G1 定义 `.ai/PROJECT.md` 产物：状态取向（写"现在是什么"，不是变更日志）、有界（token 上限 + 指针化）；字段含 目的 / 架构与模块地图 / 关键长期决策与不变量（带"为什么"）/ 现行约束 / 已知长期欠债 / 指针。
- G2 新增 schema 文件定义其字段、维护触发（收口前滚）、与既有产物的分工边界；写作口径复用 `artifact-style.md`，不另起一套。
- G3 接线冷启动读序：`PROJECT.md` 为冷启动第一读（是什么/到哪了 → 时间线 → 断点 → 代码）；更新 `README.md` 与 `context-persistence.md`。
- G4 落地维护与部署：把"前滚 PROJECT.md"加进收口步（iteration / milestone）；`mcv-deployment.md` 部署时创建种子；评估并落实迁移配方对已部署项目的补建。
- G5 dogfood：butler 仓自身落一份真实的 `.ai/PROJECT.md` 种子，验证 schema 可用。

# Constraints

- 不改四件套字段结构、不改 AC 验收脊柱、不改 P1-P5 状态机。
- 本迭代不碰 hook 代码、不加存在性硬门禁——PROJECT.md 是状态摘要不是阶段门禁产物，执行门槛归 R2/ITER-0018。
- 维护成本可控：收口前滚"按需"，多数迭代只动 0-2 行或不动（合 `maintenance-boundaries.md`）。
- 守本仓 `CLAUDE.md` 五约束（不破分层 / 不破产物链 / 不引隐式依赖 / 模板单一来源 / audience 标注）。

# Impact Scope

- 新增：`Coder/20_Workflow_Lifecycle/project-digest-schema.md`（命名 P3 定）、`.ai/PROJECT.md`（butler 自己 dogfood 种子）。
- 改：`Coder/README.md`（注册新 schema + 读序加 PROJECT.md 第一读）、`Coder/40_Context_Management/context-persistence.md`（冷启动章节引用）、`Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5`（收口加前滚步）、`milestone-schema.md §7.4`（如适用）、`mcv-deployment.md`（部署种子）。
- 评估联动：`templates/rule-card.md`（PROJECT.md 是否进强制产物集，P3 定）、迁移配方（聚合发布时产出，给已部署项目补建）。
- 不影响：四件套字段结构、AC 脊柱、P1-P5 状态机、hook 代码、lifecycle 分流、版本机制。

# Project Type / Active Profiles

- 形态：Markdown 规则仓库（butler 自己）。Profiles：无。

# Open Questions

- Q1 命名：产物 `.ai/PROJECT.md`（倾向）vs `OVERVIEW.md` / `STATE.md`；schema 文件 `project-digest-schema.md`？（P3 定）
- Q2 token 上限：handoff 是 ≤500；PROJECT.md 是全貌应更宽，倾向 ≤1500-2000 + 指针化。（P3 定）
- Q3 是否进 hook / rule-card 硬门禁？倾向否——靠收口前滚 + R2 探针兜底，不做存在性硬拦。（P3 定，与 R2 协调）
- Q4 迁移配方在本迭代写还是聚合发布时写？倾向发布时按 `versioning-schema §5` 产出，本迭代 TECH_PLAN 先定补建口径。（P3 定）
