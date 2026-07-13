# 01_CHANGELOG

> 活跃迭代 ITER-0045（slash command 全局下发目标项目·软链装法）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度。收口时归档至 `iterations/ITER-0045/CHANGELOG.md`。

## ADD

- `scripts/setup.sh` §第 3 步 — 新增「Claude Code 全局 slash 命令」软链步骤：逐文件 `ln -sfn $BUTLER_DIR/.claude/commands/*.md → $HOME/.claude/commands/`；`compgen -G` 空目录守卫走跳过分支；末尾「使用方式」提示补一句命令全局可用。→ AC1、AC2、AC3
- `.claude/commands/butler-prd.md` §开篇后 — 插入 `> **路径约定**` 段：引用的 `Coder/…` 规则相对 `$BUTLER_PATH` 解析（非当前项目路径）、产出的 `.ai/references/prd/…` 落当前项目；使薄壳跨 cwd 成立。路由三分支正文未改。→ AC4

## EDIT

- `README.md` §快速上手 + §目录结构 — 注明 `setup.sh` 现在也把 slash 命令软链装到全局 `~/.claude/commands/`，所有项目可用；结构树补 `.claude/commands/` 一行。→ AC5
- `HUMAN_GUIDE.md` §3 安装 — 「自动完成两件事」改「三件事」，加第 3 条软链命令 + 一句「命令全局可用（所有项目，不再限 butler 本仓）」。→ AC5
- `.ai/project/capabilities.md` §命令 + §部署与维护 — `/butler-prd` 行去掉「仅 butler 自用、未下发」注、改「全局软链下发、所有项目可用」；部署节补「slash 命令全局安装（setup.sh 软链，独立于逐项目基地车）」。收口折叠。→ AC6、AC7
- `.ai/project/frontier.md` — 当前形态刷新至 v2.5.0（聚合 ITER-0045）；战线记「slash command 分发缺口已闭（全局软链）」。收口折叠。→ AC6、AC7

## DELETE

- `.ai/project/debt.md` §第 3 笔 — **删除**「`/butler-prd` 仅 butler 自用、未下发目标项目」欠债：本迭代已通过全局软链还清（还掉的删、不留历史）。→ AC6
