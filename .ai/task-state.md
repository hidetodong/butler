# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**ITER-0045 已收口**，正在切版 **v2.5.0**（聚合 ITER-0045·slash command 全局下发）。前一版 v2.4.0（ITER-0044·`/butler-prd` 纳管）。

## ITER-0045 收口小结

- 闭掉分发缺口：让 butler slash 命令在**任意目标项目**可用，走**全局软链**装法。`scripts/setup.sh` 加第 3 步——逐文件把 `.claude/commands/*.md` 软链进 `~/.claude/commands/`（幂等 `ln -sfn`、空目录 `compgen` 守卫跳过、逐文件不接管整目录）。命令正文加「`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目」路径约定，路由三分支不动。README + HUMAN_GUIDE 注册全局命令安装。
- 7 条 AC 全过；AC1–AC5 隔离 HOME 端到端实跑 setup.sh（**P5 抓修一个真 bug**：`$CLAUDE_CMD_DIR（` 全角括号触发 `set -u` unbound → 加 `${...}` 花括号消歧）。未触发独立复核（幂等 bash + 文档，无契约面）。
- 交付 `deliveries/ITER-0045-slash-command-global-distribution.md`+`.html`，归档 `.ai/iterations/ITER-0045/`。全貌产物已折：`capabilities`（`/butler-prd` 全局下发 + setup 全局安装能力）、`frontier`（v2.5.0 + 分发缺口已闭）、`debt`（**删**第 3 笔「未下发」欠债）。
- **切版 v2.5.0 判 MINOR**（新增分发能力）；`migrations/v2.5.0.md` 就目标项目 `.ai/` 部署面给 `[no-op]`+`[restamp]`，注明机器级动作「重跑 `./scripts/setup.sh`」。发布提交独立于迭代 feat 提交。

## 下一步入口

- **待用户给方向**：候选——① PRD 全链真实 dogfood（还「从未真跑」欠账）；② slash command 成体系化（分发链路已通、`/butler-prd` 是范本，续落 `/milestone`·`/prd`·`/review` 等真实 `butler-*` 命令文件，随 setup.sh 自动全局可用）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
