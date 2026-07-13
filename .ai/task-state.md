# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**ITER-0044 已收口**，正在切版 **v2.4.0**（聚合 ITER-0044·`/butler-prd` 一等命令入口纳管）。前一版 v2.3.0（ITER-0043）。

## ITER-0044 收口小结

- 把既成的未跟踪原型 `.claude/commands/butler-prd.md` 正式**纳入版本管理**，成 butler 第一个真实 slash command 文件——补齐历史「命令只是散文触发词、菜单零存在感」的缺。本迭代**不改文件内容**（前序会话已说人话化、本会话 `/butler-prd status` 实跑验证过），只追认纳管 + 逐 AC 对真实文件/git 状态核。
- 6 条 AC 全过（AC2/AC3/AC4/AC5 auto·可靠实测：frontmatter 无术语 / 薄壳三要点齐 / 影响面守恒 / 边界如实记；AC1/AC6 依赖提交与切版动作）。未触发独立复核（纳管 Markdown、无逻辑/代码/契约面）。
- 交付 `deliveries/ITER-0044-butler-prd-slash-command.md`+`.html`，归档 `.ai/iterations/ITER-0044/`。全貌产物已折（`capabilities` 命令表 + `frontier` v2.4.0 + `debt` 未下发）。
- **切版 v2.4.0 判 MINOR**（本仓新增命令能力），但命令住 butler 自身 `.claude/`、**未进 `templates/`、未下发目标项目** → `migrations/v2.4.0.md` 就部署面给 `[no-op]`+`[restamp]`。发布提交独立于迭代 feat 提交。

## 下一步入口

- **待用户给方向**：新里程碑 / 独立迭代由用户发起。候选——① PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程），还上"从未真跑"欠账；② slash command 成体系化（`/butler-prd` 已开真实文件先例，续落 `/milestone`·`/prd` 等 + 评估是否进 `templates/` 下发）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
