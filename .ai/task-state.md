# Task State

> **活跃里程碑 MILE-0005**（butler 命令命名空间系统）· **无活跃迭代**（`ITERATIONS.current: none`）· R1 地基 ITER-0047 **已收口切版 v2.7.0**。里程碑仍进行中，R2–R4 待用户放行。分支 `feat/mile-0005-butler-command-namespace`。

## MILE-0005 里程碑（active）

把 butler 散在规则正文里的「散文触发词」（`/milestone`、`/review`、`/loop` 等只是文档暗号、没有真实命令文件）收敛成一整套 `/butler:xxx` 命名空间下的真实 slash command——补全菜单可见、全局任意项目可用、`butler:` 前缀隔离撞名。路线图 4 迭代：**R1** 地基（ITER-0047，✅ 已收口）→ **R2** 批量补 milestone/upgrade/ideation → **R3** preference（子命令最多）→ **R4** loop/dangerous（加风险闸）。产物真源 `.ai/MILESTONE.md`。

## ITER-0047（closed·R1 地基）

- **已交付**：① `.claude/commands/butler/` 命名空间目录；② `/butler-prd`→`/butler:prd` 破坏性迁移（`git mv` 正文零改 + 旧全局软链迁移清理）；③ `setup.sh` 逐文件软链→命名空间目录软链；④ `/butler:review` 薄壳范本（后续命令复制样板）。
- **切版**：v2.6.1→v2.7.0（MINOR），配方 `migrations/v2.7.0.md`（个人命令层 `[rename]` + 部署面 `[no-op]`+`[restamp]`）。
- **验证**：AC1–AC8 全过；隔离 HOME 实跑 setup.sh 16/16；P5 升格独立复核（验证者≠作者）confirm 8/refute 0/0 Must Fix。
- **危险模式自治**：P2 用户 ACK，P3 起自审门替代 ACK、自治到收口；审计轨迹 `.ai/RUN_LOG.md` ITER-0047。交付 `deliveries/ITER-0047-command-namespace-foundation.md`+`.html`。

## 下一步入口

- **续跑 MILE-0005 需用户放行**：R2（批量补 milestone/upgrade/ideation 三个低风险薄壳命令，套 R1 固化范本）是自然下一步；范本＝往 `butler/` 丢一个薄壳 `.md`（委托真源不复述 + 第 0 步优雅降级 + frontmatter 两行说人话），随目录软链自动全局可用。
- **本机生效动作**：主检出重跑一次 `./scripts/setup.sh`（清旧 `butler-prd.md` 软链 + 装 `butler/` 命名空间目录软链），`/butler:prd`·`/butler:review` 即在所有项目菜单可见。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → `.ai/MILESTONE.md`（里程碑范围）→ 代码。
