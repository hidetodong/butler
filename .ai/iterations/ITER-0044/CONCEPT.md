> 分流: 完整 | 命中升级信号: 首次把 butler slash command 落为真实 tracked 文件（新增一等命令入口） | 2026-07-13

# 一句话
- 之前 butler 的 slash command 只是规则正文里的「散文触发词」——没有真实的 Claude Code 命令文件，用户在补全菜单里看不到、也记不住。
- 本迭代把已经原型化的 `/butler-prd` **正式落为一个真实、受版本管理的命令文件** `.claude/commands/butler-prd.md`（薄壳路由器 + 说人话菜单），是 butler 第一个真命令；追认式收口，并聚合切 MINOR v2.4.0。

# Goal
- 把 `.claude/commands/butler-prd.md`（PRD 先行动作的薄壳路由命令）从「未跟踪的原型文件」正式**纳入版本管理**，让 `/butler-prd` 成为 butler 仓自身可用、可发现、可维护的一等命令入口。
- 确认该命令满足三条质量口径：① 菜单可见字段（`description` / `argument-hint`）说人话、无内部术语；② 命令正文是**薄壳**——按 `$ARGUMENTS` 路由到真源规则、不复述算法（守 DRY）；③ 影响面守恒——只加这一个文件。

# Current Understanding
- **背景（已核）**：历史会话确认 butler slash command 长期是「prose references, not implemented files」——`Coder/` 规则里到处写 `/prd` / `/milestone` 等触发词，但 butler 仓从无 `.claude/commands/` 真实文件，导致命令在补全菜单里零存在感、用户记不住。
- **现状（git 已核）**：`.claude/commands/butler-prd.md` 已作为**未跟踪文件**存在（`?? .claude/`，仅 `.claude/worktrees/` 被 gitignore）。前序会话已把它的 frontmatter 说人话化（`description` / `argument-hint` 去掉「薄壳 / 首切 / 真源规则」等术语）。本迭代做的是把这个既成文件**追认形式化 + 纳管 + 切版**，非从零新写。
- **文件形态（已读）**：frontmatter 两行（菜单可见）+ 正文薄壳路由（第 0 步强制读 `references-schema` 契约 → 按 `$ARGUMENTS` 三分支：留空/贴 PRD=首切走 `prd-split`、`update`=改版走 `prd-update`、`status`=只读看板走 `prd-update §7`）。正文明确「具体算法一律以被指向的规则文件为准，本文件不复述」——守 DRY。

# Constraints
- **最小实现 + 影响面守恒**：迭代内容提交只纳管 `.claude/commands/butler-prd.md` 一个文件；**不**改任何规则正文、不动 `templates/`（不扩部署面）、不改四件套 schema / hook / `VERSION`（VERSION 属独立发布提交）。
- **DRY 铁律**：命令正文只做「读对规则 + 路由 + 委托」，不得把 `prd-split` / `prd-update` / `references-schema` 的算法搬进命令文件重述。
- **butler 仓内部工具，不部署**：该命令住 butler 自己的 `.claude/`，只在**编辑 butler 仓**时可用；**不进 `templates/`、不下发给目标项目**（部署面零变化）。这条限制必须在交付里如实记录，避免误以为目标项目也能用 `/butler-prd`。
- **说人话**：菜单可见的 `description` / `argument-hint` 守 `artifact-style §2` 说人话三条（术语先解释 / 别让英文·变量裸奔）——它们是唯一对用户可见的两行。

# Impact Scope
- 纳管（1 新文件）：`.claude/commands/butler-prd.md`（butler 仓自身 Claude Code 命令配置）。
- 明确不影响：任何 `Coder/**` 规则正文、`templates/**`、四件套 schema 字段结构、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机、`VERSION`（发布提交单独 bump）。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.3.0→2.4.0、`CHANGELOG.md` 顶条、`migrations/v2.4.0.md`。

# Project Type / Active Profiles
- butler 规则仓库自身 dogfood——编辑仓库资产本身，非用规则开发软件。
- 无 Domain / Stack Profile 命中；按通用 SOP + 仓库 `CLAUDE.md` 编辑约定推进。

# Open Questions
- `/butler-prd` 是否该进 `templates/` 下发给目标项目？→ **本迭代不做**（scope 外）：先把 butler 自用命令跑顺、验证一等命令文件的形态；下发是独立决策，记入 frontier/debt 待定，不在本轮扩张。
- 是否要一次把 `/milestone` / `/prd` 等其他散文命令也落为真实文件？→ **不**：本轮只追认已成型的 `/butler-prd` 一个，避免范围膨胀；成体系铺开是后续独立方向。
