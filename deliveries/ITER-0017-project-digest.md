# 新增 .ai/PROJECT.md 常驻项目摘要：冷启动全貌产物（状态取向）

> ITER-0017 · 迭代交付（小版本）· 收口 2026-06-30 · 所属 MILE-0001（R1）

## 本次交付目标

- 补冷启动"管中窥豹"缺口：butler 的 `.ai/` 此前只有变更流（ITERATIONS）和瞬时断点（handoff），没有一份"系统现在整体是什么、为何如此、有哪些长期约束与欠债"的状态取向全貌。长寿项目冷启动时 AI 只能从一堆迭代一句话倒推整只豹。
- 本迭代新增 `.ai/PROJECT.md`（常驻全貌摘要）+ 其格式契约，并接进冷启动读序与收口维护，让"全貌"成为冷启动第一读。

## 已完成内容

- 新增 `Coder/40_Context_Management/project-digest-schema.md`：定义 `.ai/PROJECT.md` 的 6 段字段（目的 / 架构与模块地图 / 关键长期决策与不变量[带为什么] / 现行约束 / 已知长期欠债 / 指针）、有界（≤1500 tokens）、指针化、收口前滚维护、与 ITERATIONS/handoff/MILESTONE 的四产物边界。
- 新增 `.ai/PROJECT.md`：butler 自身的全貌摘要（dogfood，验证 schema 可用）。
- 冷启动读序接线：`context-persistence.md` 新增「冷启动读序」段、`handoff-spec.md` 补"状态全貌由 PROJECT 承载"、`README.md` 注册新 schema 并补读序。
- 收口前滚接线：`iteration-schema.md §5.5` 与 `milestone-schema.md §7.4` 收口加第四步「按需前滚 PROJECT.md」，`lifecycle.md` 同步。
- 部署接线：`mcv-deployment.md` 登记 PROJECT.md 为运行态文件（按需产生）。

## 关键变更 / 用户可感知变化

- 冷启动认知顺序固化：以后新会话先读 `.ai/PROJECT.md` 抓系统全貌，再看时间线、断点、代码——不再从 N 个迭代 delta 倒推。
- 收口多一步"按需前滚 PROJECT.md"：本迭代若改变了某条长期事实才更新，多数迭代 0-2 行或不动（维护成本可控）。
- PROJECT.md 不进 hook / rule-card 硬门禁：它是状态摘要不是阶段门禁产物，存在性靠收口前滚纪律（机械门槛留给 MILE-0001 R2）。
- 向后兼容：纯新增 + 接线，未动四件套字段、AC 脊柱、状态机、hook；老项目不受影响（升级时按需补建）。

## 高层影响范围

- 新增：`Coder/40_Context_Management/project-digest-schema.md`、`.ai/PROJECT.md`。
- 改（40 层）：README、context-persistence、handoff-spec；（20 层）：iteration-schema、milestone-schema、mcv-deployment、lifecycle。
- 没碰：四件套字段 schema、hook、rule-card、P1-P5 状态机分流、版本机制。

## 验证方式与结果摘要

- 10 条 AC 全部满足（逐项见 VERIFY_REPORT）：schema 字段/有界/边界、冷启动读序、README 注册、收口前滚、部署登记、dogfood、rule-card 裁决、不变量。
- git diff 核对改动集中、未外溢；grep 确认四件套字段 schema / hook / rule-card 零改动。
- 两处如实披露：① AC7 按 mcv `§2` 原则化解为"按需产生"（非部署建空骨架）；② P5 发现 `lifecycle.md` 收口步复述漂移、已同步修。
- P5 默认简评（含 dogfood 自检）：无 Must Fix、无 Should Fix。

## 已知剩余风险 / 延后事项

- `migration-schema` 无"新建文件"步型，已部署项目补建口径已定、实际配方与是否加 `[add-file]` 留聚合发布时定。
- PROJECT.md 维护靠收口前滚纪律、无机械门禁（butler 自身不跑 hook）——MILE-0001 R2（ITER-0018）拟补一致性探针。
- 本轮不切版；MILE-0001 待 R2 / R3 收口后聚合发布。

## 引用

- 归档四件套：`.ai/iterations/ITER-0017/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`
- 新增规则：`Coder/40_Context_Management/project-digest-schema.md`
- 改动规则：`Coder/README.md`、`Coder/40_Context_Management/context-persistence.md`、`Coder/40_Context_Management/handoff-spec.md`、`Coder/20_Workflow_Lifecycle/iteration-schema.md`、`Coder/20_Workflow_Lifecycle/milestone-schema.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/20_Workflow_Lifecycle/lifecycle.md`
- dogfood 产物：`.ai/PROJECT.md` · 里程碑：`.ai/MILESTONE.md`（MILE-0001 R1）
