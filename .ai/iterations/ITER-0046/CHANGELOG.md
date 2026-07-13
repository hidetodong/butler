# 01_CHANGELOG

> 活跃迭代 **ITER-0046**。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度，仅承载**当前开放迭代**的热数据。开新迭代时整体覆写；收口时归档至 `iterations/ITER-0046/CHANGELOG.md`。

## ADD

- `communication-style.md`（仓根，新增）— 个人沟通风格**唯一正本**：开篇定位块 + 8 节（基调 / 详略〔含「话砍到骨头」〕/ 抓重点 / 说人话〔4 条各一对 ❌/✅〕/ 别急着抛选择菜单〔新增〕/ 格式 / 结尾决策块 / 边界）→ AC1
- `scripts/setup.sh` §受管 heredoc — 加一行 `@$BUTLER_DIR/communication-style.md`，把正本 @import 进全局 `~/.claude/CLAUDE.md` 常开 → AC2/AC3
- `migrations/v2.6.0.md`（发布层，新增）— `[no-op]`+`[restamp]` + 机器级重跑 setup + 本机手动清理清单 → AC7

## EDIT

- `README.md` §目录结构 — 登记 `communication-style.md`（个人全局配置、经 setup @import 常开、不进 Coder SOP 阅读顺序）→ AC4
- `HUMAN_GUIDE.md` §安装 — 点明重跑 setup 装上全局常开沟通风格配置 → AC4
- `.ai/project/capabilities.md` — 加「个人沟通风格全局常开正本 + setup @import 能力」（收口折叠）→ AC8
- `.ai/project/frontier.md` — 刷 v2.6.0 + 战线（收口折叠）→ AC8
- `VERSION` — 2.5.0 → 2.6.0（发布层）→ AC8
- `CHANGELOG.md` — 顶条 `## [2.6.0]`（发布层）→ AC8
- **本机迁移（不进仓 diff）**：`~/.config/fish/config.fish` + `~/.zshrc` 两处 `claudep` 去 `--settings '{"outputStyle":"Matrix"}'`；记忆 `style-concise`/`style-plain-language`/`discussion-mode-no-forced-menus` 掏薄壳；`MEMORY.md` 三索引行改薄壳描述 → AC5/AC6

## DELETE

- **本机迁移（不进仓 diff）**：`~/.claude/output-styles/matrix.md`（过渡产物退休，规矩已并入正本）→ AC5
