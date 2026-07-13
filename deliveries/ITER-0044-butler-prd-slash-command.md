# `/butler-prd` 一等命令入口纳管：butler 第一个真实 slash command 文件

> ITER-0044 · 独立迭代（无所属里程碑）· 收口 2026-07-13 · dogfood butler 自身 · 判 MINOR·聚合切 v2.4.0（命令 butler 自用、部署面 `[no-op]`）

## 本次交付目标

- butler 的 slash command 长期只是规则正文里的**散文触发词**（`/prd`、`/milestone` 等到处被引用，却没有一个真实的 Claude Code 命令文件）——结果命令在补全菜单里零存在感，用户既看不到、也记不住。
- 本次把已经原型化并实跑验证过的 `/butler-prd` **正式落为一个真实、受版本管理的命令文件** `.claude/commands/butler-prd.md`，成为 butler 第一个「真命令」。这是追认式收口：文件已成型，本轮做的是纳管 + 逐项验收 + 切版。

## 已完成内容

- **命令文件纳入版本管理**：`.claude/commands/butler-prd.md` 从未跟踪原型（`?? .claude/`，仅 `.claude/worktrees/` 被 gitignore）正式 `git add` 纳管，成 butler 仓第一个真实 slash command 文件。本迭代**不改其内容**——前序会话已把它的菜单文字说人话化、正文薄壳也经本会话 `/butler-prd status` 实跑验证可用。
- **菜单可见两行说人话**：`description` = 「把权威 PRD 拆进项目知识库，并随改版保持同步——首次拆分 / 改版对齐 / 只读看板」；`argument-hint` = 「[status=只读看板 | update=改版同步 | 贴 PRD 或路径；留空=首次拆分]」。去掉了「薄壳 / 首切 / 真源规则」等内部术语（这些只留在正文——给 AI 的执行指令、菜单不可见）。
- **正文是薄壳路由器（守 DRY）**：只做三件事——① 第 0 步强制先读 `references-schema` 契约（治「该响应时没响应」的老病）；② 按 `$ARGUMENTS` 三分支路由（留空/贴 PRD → `prd-split` 首切、`update` → `prd-update` 改版、`status` → `prd-update §7` 只读看板）；③ 委托真源规则执行，明确声明「具体算法一律以被指向的规则文件为准、本文件不复述」。
- **知识文件夹前滚**：`.ai/project/capabilities.md` 命令表加 `/butler-prd` 真实文件行；`frontier.md` 版本态刷新至 v2.4.0 + 记「slash command 首次落真实文件」战线；`debt.md` 记「命令未下发目标项目」待定。

## 关键变更 / 用户可感知变化

- **`/butler-prd` 现在是真命令了**：在 butler 仓里敲 `/butler-prd`，补全菜单能看到它、能读懂它在干什么（PRD 先行：首次拆分 / 改版同步 / 只读看板），不再是藏在规则正文里的散文触发词。
- **只在编辑 butler 仓时可用**：这个命令住 butler 自己的 `.claude/`，**没有下发给目标项目**——用 butler 部署的其他项目暂时没有 `/butler-prd`。这是本轮有意的边界（先把自用命令跑顺），不是遗漏。
- **对已部署项目零影响**：命令不在部署模板 `templates/` 里，目标项目升级到 v2.4.0 无任何结构变化，只需重打版本戳。

## 高层影响范围

- 纳管（1 新文件，迭代内容提交）：`.claude/commands/butler-prd.md`（butler 仓自身 Claude Code 命令配置）。
- 知识文件夹前滚：`.ai/project/capabilities.md` / `frontier.md` / `debt.md`。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.3.0→2.4.0、`CHANGELOG.md` 顶条、`migrations/v2.4.0.md`。
- 没碰（守最小影响面）：任何 `Coder/**` 规则正文、`templates/**`、四件套 schema 字段结构、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机——逐个 `git status` / `git show --stat` 核清。

## 验证方式与结果摘要

- **6 项验收（AC1–AC6）全过**，AC2/AC3/AC4/AC5 均 **auto·可靠**、对**真实文件 + 真实 git 状态**核（非纸面声明）：frontmatter 术语黑名单 grep 零命中（AC2）、正文薄壳三要点齐（第 0 步契约读 + 三分支路由 + 「不复述」声明，AC3）、`git status` 确认唯一非 `.ai/` 改动即该命令文件（AC4）、交付 + `frontier`/`debt` 均写清「butler 自用未下发」边界（AC5）。
- **AC1/AC6 依赖提交与切版动作**：feat 提交后 `git ls-files` 命中该路径（从未跟踪转纳管）；收口五步齐 + v2.4.0 三处版本载体（`VERSION` == tag `v2.4.0` == `CHANGELOG` 顶条）对齐 + `migrations/v2.4.0.md` 就部署面给 `[no-op]`+`[restamp]`。
- **未触发独立复核**：改动是纳管一个既有、已实跑验证的 Markdown 命令文件，无逻辑 / 无代码 / 无契约面，影响面经 git 机器核封死——不满足复核触发条件（对比 ITER-0043 改 `identity` 哲学底座才必过复核）。

## 已知剩余风险 / 延后事项

- **`/butler-prd` 仅 butler 自用、未下发目标项目**：编辑 butler 仓时可用，目标项目无此命令——已如实入 `debt.md`。下发（进 `templates/` + 配套升级配方）是独立决策，待定、不隐藏。
- **切版意义如实标注**：MINOR 标的是「本仓新增命令能力」；`migrations/v2.4.0.md` 就部署面诚实给 `[no-op]`，不夸大 v2.4.0 对目标项目的影响。
- **追认式迭代**：产物后于文件成型，但全部 AC 对真实文件 / git 状态核过，非事后补声明——风险已闭。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0044/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 纳管产物：`.claude/commands/butler-prd.md`
- 命令委托的真源规则：`Coder/40_Context_Management/references-schema.md` / `prd-split.md` / `prd-update.md`
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.4.0]`）、`migrations/v2.4.0.md`
