# 01_CHANGELOG

> 活跃迭代 ITER-0044（`/butler-prd` 一等命令入口纳管）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度。收口时归档至 `iterations/ITER-0044/CHANGELOG.md`。

## ADD

- `.claude/commands/butler-prd.md` — 把既成的未跟踪原型正式纳入版本管理，成 butler 第一个真实 Claude Code slash command 文件。frontmatter 两行（菜单可见）：`description`=「把权威 PRD 拆进项目知识库，并随改版保持同步——首次拆分 / 改版对齐 / 只读看板」、`argument-hint`=「[status=只读看板 | update=改版同步 | 贴 PRD 或路径；留空=首次拆分]」（说人话、无内部术语）；正文为薄壳路由器（第 0 步强制读 `references-schema` 契约 → 按 `$ARGUMENTS` 三分支 留空/贴PRD=prd-split·update=prd-update·status=prd-update §7 → 委托真源、声明不复述算法守 DRY）。本迭代不改文件内容、只 `git add` 纳管。→ AC1、AC2、AC3、AC4

## EDIT

- `.ai/project/capabilities.md` §命令 — 命令表新增/标注 `/butler-prd`（首次落为真实 `.claude/commands/` 文件的 butler 命令；PRD 先行薄壳路由，butler 自用未下发）。收口折叠。→ AC5、AC6
- `.ai/project/frontier.md` — 当前形态刷新至 v2.4.0（聚合 ITER-0044）；活跃战线记「butler slash command 首次落真实文件」。收口折叠。→ AC5、AC6
- `.ai/project/debt.md` — 新增一笔：`/butler-prd` 仅 butler 自用、未进 `templates/`、未下发目标项目（下发待独立决策）。收口折叠。→ AC5

## DELETE

- 无。
