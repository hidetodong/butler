# 版本升级 SOP 化：迁移配方台账 + butler-upgrade 改执行器

> ITER-0014 · 迭代交付（小版本累积） · 收口 2026-06-30

> ⚠️ **危险模式自治披露**：本迭代在 `/dangerous` 无人值守自治下完成，P2/P3 的 ACK 由模型自审门替代（未经用户逐阶段确认），P5 经强制完整审查 + 独立复核。自治轨迹见 `.ai/RUN_LOG.md`。

## 本次交付目标

- 你反馈：每次在不同项目跑 `butler-upgrade`，模型都得现场比对"目标项目 vs butler 最新仓"、自己拼升级流程——同样的活每次重做、还因人而异。
- 这次把版本升级 SOP 化：每次切版顺手记一份"这一版升级要做哪几步"的**迁移配方**，升级时不再现推、直接照配方按序执行。

## 已完成内容

- **新增迁移配方规范** `Coder/20_Workflow_Lifecycle/migration-schema.md`：定义配方放哪（仓库根 `migrations/vX.Y.Z.md`）、每份必含什么、六个 typed 操作标签（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`），以及"幂等 + 先校验起始态 + 漂移就停下问人"的契约。
- **回填三份配方** `migrations/v1.1.0.md` / `v1.2.0.md` / `v1.3.0.md`：如实列出每个历史版本对已部署项目要做的步骤，台账不再是空的、老项目能立刻用。
- **`butler-upgrade.md` 改成执行器**：侦察阶段按目标版本戳收集区间配方排队，执行阶段按序幂等应用；内容 diff 从"主驱动"降为"每步起始态校验 + 冲突兜底"；顺带补上了一直缺的 `.claude/hooks/` 副本同步（`[sync-hooks]`，覆盖 `mcv-deployment §5.4` 的已知缺口）。无版本戳的老项目仍走原全量首次升级兜底。
- **`versioning-schema.md §5` 切版流程加一步**："写迁移配方"成为发布必做步（无影响也要写 `[no-op]`），让配方不会漏记。
- **`Coder/README.md`** 三处注册新规范。

## 关键变更 / 用户可感知变化

- 以后升级：模型从"现场想流程"变成"照配方执行"，跨项目、跨模型结果一致、可审计。
- 升级现在会一并把目标项目的 hook 副本同步到最新（以前不会，副本会悄悄漂）。
- 对已手工改过的项目仍安全：每步先校验起始态，对不上就停下报告、等你决定，不盲目按版本号套。

## 高层影响范围

- 新增：`migration-schema.md`、`migrations/` 目录 + 三份配方。
- 改：`butler-upgrade.md`、`versioning-schema.md`、`Coder/README.md`。
- 没碰：hook 代码、四件套字段结构、lifecycle 分流、对话层规则、历史 `deliveries/`。

## 验证方式与结果摘要

- AC1–AC11 全部满足。**独立复核（另起一个不带本会话上下文的子 agent）查出一个实质 bug**：`v1.1.0` 配方漏了 `[regen-claude]`——经 `git log -- templates/rule-card.md` 证实 ITER-0008/0009/0010 都改过 rule-card，配方必须重生成目标 CLAUDE.md 的内联规则卡。已补步修复，并在 `migration-schema.md` 加"漏判防线"判据（区间内任一迭代动过 rule-card 即必须 regen）防复发。
- 本仓 CLAUDE.md 五约束自检通过；新文件已注册、模板单一来源未破。

## 已知剩余风险 / 延后事项

- 配方靠"切版时记录"规则纪律 + 漏判防线维持，无 hook 机械强制——降低漏记概率但不根除（与版本治理本身"无 hook 强制"同源）。
- 本迭代**未切版**（切版属用户门控动作）。建议把本迭代发为 v1.4.0 并按新规则写 `migrations/v1.4.0.md` 做 dogfood：本迭代未动 rule-card，该配方应为 `[no-op]` + `[restamp]`，正好演示 `[no-op]` 场景。

## 引用（只引用路径，不嵌全文）

- `.ai/iterations/ITER-0014/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`
- `.ai/RUN_LOG.md`（危险模式自治审计轨迹）
- 新增规则：`Coder/20_Workflow_Lifecycle/migration-schema.md`
- 配方台账：`migrations/v1.1.0.md` / `v1.2.0.md` / `v1.3.0.md`
- 改动规则：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`、`versioning-schema.md`、`Coder/README.md`
