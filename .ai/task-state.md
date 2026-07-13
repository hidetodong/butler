# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**ITER-0046 已收口**，正在切版 **v2.6.0**（聚合 ITER-0046·个人沟通风格常开正本）。前一版 v2.5.0（ITER-0045·slash command 全局下发）。

## ITER-0046 收口小结

- 把散在本机 Matrix 输出风格与多个记忆文件的「怎么跟用户说话」规矩，收敛成 butler 仓根**唯一正本** `communication-style.md`（8 节：基调/详略含话砍到骨头/抓重点/说人话4条各带例/别急着抛选择菜单/格式/结尾决策块/边界；随 git 跨机器同步）。`scripts/setup.sh` 受管 heredoc 加一行 `@$BUTLER_DIR/communication-style.md`，把正本 @import 进全局 `~/.claude/CLAUDE.md` **每会话每项目常开**。README + HUMAN_GUIDE 注册。
- Matrix 输出风格**退休**（本机一次性迁移，不进仓提交）：删 `~/.claude/output-styles/matrix.md` + 拆 fish/zsh 两处 `claudep` 的 `--settings '{"outputStyle":"Matrix"}'` 参数 + 查 settings.json 无残留；三风格记忆（style-concise/style-plain-language/discussion-mode-no-forced-menus）掏薄壳、只留来龙去脉 + 指向正本，MEMORY.md 索引同步改。
- 8 条 AC 全过；AC1–AC6 实测（隔离 HOME 端到端实跑 setup.sh 核 @import 行恒=1 + 幂等 + 抽路径 test -f；迁移前逐节核 matrix→正本无遗漏 21 锚点、迁移后读文件核）。未触发独立复核（幂等 bash + 手写正本 + 文档，无契约面）。
- 交付 `deliveries/ITER-0046-communication-style-voice-file.md`+`.html`，归档 `.ai/iterations/ITER-0046/`。全貌产物已折：`capabilities`（沟通风格全局常开正本 + setup @import 能力）、`frontier`（v2.6.0 + 沟通风格收敛单一正本）。
- **切版 v2.6.0 判 MINOR**（新增常开能力）；`migrations/v2.6.0.md` 就目标项目 `.ai/` 部署面给 `[no-op]`+`[restamp]`，注明机器级动作「重跑 `setup.sh` 装 @import」+ 本机一次性清理 matrix/claudep 可选手动步。发布提交独立于迭代 feat 提交。

## 下一步入口

- **待用户给方向**：候选——① PRD 全链真实 dogfood（还「从未真跑」欠账）；② slash command 成体系化（分发链路已通、`/butler-prd` 是范本，续落 `/milestone`·`/prd`·`/review` 等真实 `butler-*` 命令文件，随 setup.sh 自动全局可用）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
