# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.4.0 已切版**——聚合 ITER-0044（`/butler-prd` 一等命令入口纳管），MINOR·本仓新增命令，配方 `migrations/v2.4.0.md` 为 `[no-op]`+`[restamp]`（命令住 butler 自身 `.claude/`、未下发目标项目，零部署面变化）。上一版 v2.3.0 = ITER-0043（工程原则增量吸收）；再前：v2.2.0 = ITER-0042（PRD 触发加固，首个含 `[sync-hooks]`）、v2.1.0 = MILE-0004、v2.0.0 = MILE-0003 MAJOR。
- **无活跃里程碑 / 无活跃迭代**（`MILESTONES.current: none`、`ITERATIONS.current: none`）。近三迭代 ITER-0042/0043/0044 均独立迭代（无所属里程碑）、均已收口切版。
- **butler slash command 首次落为真实文件（ITER-0044）**：`.claude/commands/butler-prd.md` 从未跟踪原型纳入版本管理，补齐历史「命令只是散文触发词、菜单零存在感」的缺——`/butler-prd` 是 butler 第一个真命令。**仅 butler 自用、未进 `templates/`、未下发目标项目**（见 `debt`）。
- **PRD 全生命周期子系统成型 + 触发已加固**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步(R5+R6 认亲松边) + **ITER-0042 触发加固**（注入表内容路由 + §6.4 分类闸前移 + PostToolUse 落盘自检）。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **无进行中战线**——ITER-0042/0043/0044 均已收口并切版（v2.2.0 / v2.3.0 / v2.4.0）；等下一个方向（新里程碑 / 独立迭代由用户发起）。
- **PRD 全链首次端到端实战：部分踩过、仍未走完**。ITER-0042 的实战（Confluence+MCP+`/milestone`）暴露并修掉了**触发漏切**（软触发被绕过），但那次没走到切分/钉版/改版——命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。

## 下一个瓶颈

- **无既定下一步**：待用户给方向。候选——① PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程）可一并还上"从未真跑"的欠账；② slash command 成体系化（`/butler-prd` 已开真实文件先例，可续把 `/milestone`·`/prd` 等散文命令落文件、并评估是否进 `templates/` 下发目标项目）。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑——**v2.2.0 起该欠债更吃劲**：`migrations/v2.2.0.md` 是首个含真实结构动作（`[sync-hooks]`）的配方，既有部署升级到 v2.2.0 必须真跑一遍拷贝+settings 合并，不再是 v2.1.0 那种 `[no-op]`+`[restamp]` 的零风险升级。`[split]` 迁移接线已于 ITER-0035 补齐，仍差真实老项目端到端跑一遍。
