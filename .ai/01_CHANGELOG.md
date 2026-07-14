# 01_CHANGELOG

> **ITER-0048 已收口**（MILE-0005 R2·批量补低风险命名空间命令）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度。本迭代快照归档见 `iterations/ITER-0048/CHANGELOG.md`；开新迭代时本文件整体覆写为下一迭代热数据。

## ADD

- `.claude/commands/butler/milestone.md` — `/butler:milestone` 薄壳（录入 / `status` 看板，委托 `milestone-schema`）。→ AC1/AC2
- `.claude/commands/butler/upgrade.md` — `/butler:upgrade` 薄壳（当前项目主动升级，委托 `butler-upgrade`）。→ AC1/AC3
- `.claude/commands/butler/ideation.md` — `/butler:ideation` 薄壳（需求脑暴，委托 `ideation-engine §3`）。→ AC1/AC4
- `migrations/v2.8.0.md` — 迁移配方（部署面 `[no-op]`+`[restamp]`；新命令由 R1 目录软链自动托管，无需重跑 setup.sh）。→ AC8

## EDIT

- `Coder/20_Workflow_Lifecycle/butler-upgrade.md` §2 — 触发词 `/butler-upgrade`→`/butler:upgrade`（+ 旧名注 · MILE-0005 R2 迁入命名空间）。→ AC3/AC9
- `Coder/00_System_Prompt/logic-protocol.md` §Butler Upgrade — 触发名迁 `/butler:upgrade`（2 occurrence + 旧名注）。→ AC3
- `Coder/20_Workflow_Lifecycle/migration-schema.md` §4 `[split]` — 正文引用 `/butler-upgrade`→`/butler:upgrade`。→ AC3
- `HUMAN_GUIDE.md` / `.ai/project/architecture.md` / `.ai/project/debt.md` — 三处命令名引用迁 `/butler:upgrade`。→ AC3
- `.ai/project/capabilities.md` 命令表 — `/ideation`·`/milestone`·`/butler-upgrade` 三行转换为 `/butler:*` 一等入口（真源指命令文件）+ **删** `/review` 旧行并入 `/butler:review`。→ AC7
- `README.md` `.claude/commands/butler/` 子树 — 补 milestone/upgrade/ideation 三命令。→ AC7
- 发布层：`VERSION` 2.7.0→2.8.0、`CHANGELOG.md` 顶条 `[2.8.0]`。→ AC8

## DELETE

- 无文件删除（R2 纯新增）。`.ai/project/capabilities.md` 内删掉 1 行 `/review` 冗余表行（并入 `/butler:review`），非文件级删除。→ AC7
