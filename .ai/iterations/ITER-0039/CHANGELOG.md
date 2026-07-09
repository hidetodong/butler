# 01_CHANGELOG — ITER-0039（MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线）

> 本文件是**当前活跃迭代 ITER-0039** 的对象级变更流（ADD/EDIT/DELETE）。收口时切片归档至 `iterations/ITER-0039/CHANGELOG.md`。

## EDIT · `Coder/20_Workflow_Lifecycle/acceptance-schema.md`

- EDIT §2 交付约定：新增 `prd_version` 可选 frontmatter 说明（引用 `references/prd/` 切片时必填、记 ACK 冻结那刻 PRD 全局版本、冻结绑定之后钉住；非 PRD 迭代不写、frontmatter 逐字不变）。
- EDIT §3 标准模板：frontmatter 加 `prd_version: —` 行 + 注释；`External References` 示例补一条 PRD 切片来源（版本＝frontmatter、正文不重复版本号）。
- EDIT §4 冻结状态字段：加 `prd_version` 绑定/钉住语义（置 ack-frozen 绑当刻全局版、之后钉住）+ amend 重冻可重绑（接 `iteration-schema §5.3`，改版完整同步属 `/prd update`）。
- EDIT §5 编写规则：加"版本化锚点 = slug + frontmatter 全局 `prd_version`、版本单一存 frontmatter、正文不重复、解析 live/`.archive/vN/` 回指 `references-schema §5 步骤 2/§7`、标 AC↔slug"。

## EDIT · `Coder/20_Workflow_Lifecycle/tech-plan-schema.md`

- EDIT §3 标准模板：`External References` 示例补一条 PRD 切片来源（版本继承 AC frontmatter `prd_version`、方案不自立版本）。
- EDIT §4 编写规则：加"引用 `references/prd/` 切片时版本继承 AC 钉住的 `prd_version`、不自立版本、口径回指 `acceptance-schema §5`、对着钉住版设计"。

## EDIT · `Coder/20_Workflow_Lifecycle/verify-schema.md`

- EDIT §3 标准模板：`References Compliance` 行注"PRD 切片对 AC 钉住的 `prd_version` 核"。
- EDIT §4 编写规则：`References Compliance` 补 **PRD 切片专项**——对着 AC 钉住 `prd_version` 核、非对 live 最新核；同迭代 live 即钉住版，回溯复核历史迭代才读 `.archive/vN/<slug>.md`；语义/读侧回指 `acceptance-schema §4` / `references-schema §5 步骤 2`。

## EDIT · `Coder/40_Context_Management/references-schema.md`

- EDIT §7 落盘契约：`prd_version` bullet flip 为**已落地**（指 `acceptance-schema §4/§5`）。
- EDIT §8 边界表：R4 行 flip 为 **✅ 已由 `acceptance-/tech-plan-/verify-schema` 落地**。
