# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.6.0 已切版**——聚合 ITER-0046（个人沟通风格常开正本 `communication-style.md` + `setup.sh` @import + Matrix 输出风格退休），MINOR·新增常开能力，配方 `migrations/v2.6.0.md` 为 `[no-op]`+`[restamp]`（目标项目 `.ai/` 部署面零变化，升级多一个机器级动作「重跑 `setup.sh` 装上 @import」+ 本机一次性清理 Matrix/claudep）。上一版 v2.5.0 = ITER-0045（slash command 全局下发·软链）；再前：v2.4.0 = ITER-0044（`/butler-prd` 纳管）、v2.3.0 = ITER-0043（工程原则吸收）、v2.2.0 = ITER-0042（PRD 触发加固，首个含 `[sync-hooks]`）、v2.1.0 = MILE-0004、v2.0.0 = MILE-0003 MAJOR。
- **无活跃里程碑 / 无活跃迭代**（`MILESTONES.current: none`、`ITERATIONS.current: none`）。近五迭代 ITER-0042/0043/0044/0045/0046 均独立迭代（无所属里程碑）、均已收口切版。
- **butler slash command 分发缺口已闭（ITER-0045）**：`/butler-prd`（ITER-0044 落为 butler 第一个真命令文件）现经 `setup.sh` **全局软链**进 `~/.claude/commands/`、**所有项目可用**；命令正文加「`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目」路径约定跨 cwd 成立。选型全局软链（与规则全局引用同模型、零漂移），不进 `templates/`、不逐项目部署。
- **个人沟通风格收敛为单一正本 + 常开（ITER-0046）**：过去「怎么跟用户说话」的规矩散在本机 Matrix 输出风格（只有切到才生效）与多个风格记忆文件、说人话还双写；现收敛成 `communication-style.md`（仓根唯一正本），经 `setup.sh` @import 进全局 CLAUDE.md **每会话常开、跨机器同步**。Matrix 输出风格退休（本机删 + 拆 `claudep` 的 `--settings` 参数）、三风格记忆掏成只记来龙去脉的薄壳。与 slash command 同走「全局机器级、不逐项目」模型。
- **PRD 全生命周期子系统成型 + 触发已加固**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步(R5+R6 认亲松边) + ITER-0042 触发加固。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **无进行中战线**——ITER-0046 已收口并切版（v2.6.0）；等下一个方向（新里程碑 / 独立迭代由用户发起）。
- **PRD 全链首次端到端实战：部分踩过、仍未走完**。ITER-0042 的实战（Confluence+MCP+`/milestone`）暴露并修掉了**触发漏切**，但那次没走到切分/钉版/改版——命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。

## 下一个瓶颈

- **无既定下一步**：待用户给方向。候选——① PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程）可一并还上"从未真跑"的欠账；② slash command **成体系化**——分发链路（全局软链）已由 ITER-0045 打通、`/butler-prd` 是范本，可续把 `/milestone`·`/prd`·`/review` 等散文命令逐个落成真实 `butler-*` 命令文件（都随 `setup.sh` 自动全局可用，无需再改分发）。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑——**v2.2.0 起该欠债更吃劲**：`migrations/v2.2.0.md` 是首个含真实结构动作（`[sync-hooks]`）的配方，既有部署升级到 v2.2.0 必须真跑一遍拷贝+settings 合并。`[split]` 迁移接线已于 ITER-0035 补齐，仍差真实老项目端到端跑一遍。
