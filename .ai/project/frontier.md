# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.9.0 已切版**——聚合 ITER-0049（MILE-0005 R3 落全批**参数面最宽**的 `/butler:preference` 薄壳：4 子命令 `on`/`off`/`reback on|off`/`distill` + 空参只读状态回声，`reback` 是全批唯一二级嵌套参数 + `/preference`→`/butler:preference` 全仓活文档触发名迁移〔`templates/` 刻意保留旧名〕+ capabilities 行转换），MINOR·新增一命令能力，配方 `migrations/v2.9.0.md` 为部署面 `[no-op]`+`[restamp]`（**新命令由 R1 目录软链自动托管、`setup.sh` 未动、无需重跑**、触发名迁移不碰 templates 故无 `[regen-claude]`）。上一版 v2.8.0 = ITER-0048（MILE-0005 R2 批量补三命名空间命令 + `/butler-upgrade`→`/butler:upgrade` 迁移）；再前：v2.7.0 = ITER-0047（R1 命令命名空间地基）、v2.6.0 = ITER-0046（沟通风格常开正本）、v2.5.0 = ITER-0045（slash 命令全局下发）、v2.4.0 = ITER-0044（首个真命令纳管，即今 `/butler:prd`）、v2.3.0 = ITER-0043、v2.2.0 = ITER-0042、v2.1.0 = MILE-0004、v2.0.0 = MILE-0003 MAJOR。
- **活跃里程碑 MILE-0005（命令命名空间系统）· 无活跃迭代**（`MILESTONES.current: MILE-0005`、`ITERATIONS.current: —`）。R1（ITER-0047·v2.7.0）、R2（ITER-0048·v2.8.0）、R3（ITER-0049·v2.9.0）均已收口，**仅剩 R4 待续**。再往前 ITER-0042~0046 均独立迭代（无所属里程碑）、均已收口切版。
- **butler 命令进入 `/butler:` 命名空间体系（MILE-0005 R1·ITER-0047 起，R2·ITER-0048 批量铺开，R3·ITER-0049 加最宽参数命令）**：`.claude/commands/butler/` 子目录＝冒号前缀（`butler/<name>.md`→`/butler:<name>`），`setup.sh` **软链整个命名空间目录**进 `~/.claude/commands/butler`、**所有项目可用**、加命令自动全局生效（R2/R3 连续实跑坐实：往 `butler/` 丢新 `.md` 无需改 `setup.sh` / 无需重跑即全局可用）。现有 **6 个成员**：`/butler:prd`（PRD 先行三分支）、`/butler:review`（复核，默认自检 / `independent`）、`/butler:milestone`（里程碑录入 / `status` 看板）、`/butler:upgrade`（已部署项目升级，原 `/butler-upgrade`）、`/butler:ideation`（需求脑暴）、`/butler:preference`（偏好探针开关，`on`/`off`/`reback on|off`/`distill` + 空参只读回声，**参数面最宽·唯一二级嵌套参数**，原 `/preference`）。范本＝薄壳路由器（委托真源不复述 + 第 0 步优雅降级 + frontmatter 两行说人话），已证吃得下二级嵌套参数。选型全局软链（与规则全局引用同模型、零漂移），不进 `templates/`、不逐项目部署（个人工具边界沿用 ITER-0044）。
- **个人沟通风格收敛为单一正本 + 常开（ITER-0046）**：过去「怎么跟用户说话」的规矩散在本机 Matrix 输出风格（只有切到才生效）与多个风格记忆文件、说人话还双写；现收敛成 `communication-style.md`（仓根唯一正本），经 `setup.sh` @import 进全局 CLAUDE.md **每会话常开、跨机器同步**。Matrix 输出风格退休（本机删 + 拆 `claudep` 的 `--settings` 参数）、三风格记忆掏成只记来龙去脉的薄壳。与 slash command 同走「全局机器级、不逐项目」模型。
- **PRD 全生命周期子系统成型 + 触发已加固**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步(R5+R6 认亲松边) + ITER-0042 触发加固。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **MILE-0005 命令命名空间系统进行中·仅剩 R4**：R1 地基（ITER-0047·v2.7.0）+ R2 批量命令（ITER-0048·v2.8.0）+ R3 最宽参数命令（ITER-0049·v2.9.0）已收口——命名空间目录 + **6 命令**（prd/review/milestone/upgrade/ideation/preference）+ 目录软链自动托管坐实；**仅剩 R4（loop/dangerous 加风险闸）待续**，范本已固化、批量复制 + 吃二级嵌套参数均得证。R4 收口后可整体收 MILE-0005。
- **PRD 全链首次端到端实战：部分踩过、仍未走完**。ITER-0042 的实战（Confluence+MCP+`/milestone`）暴露并修掉了**触发漏切**，但那次没走到切分/钉版/改版——命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。

## 下一个瓶颈

- **续跑 MILE-0005 R4（最后一路线项）**：范本与地基已就位、R2 证批量可复制、R3 证吃得下二级嵌套参数，下一步把 `/loop`·`/dangerous`（R4 加风险闸）落成 `/butler:*` 薄壳命令（往 `butler/` 丢 `.md` 即全局可用，无需再改分发）——**唯一新面**是命令化不得降低「郑重显式触发」门槛，薄壳要前置风险提示/确认闸、不照抄低风险轻壳。R4 收口即可整体收 MILE-0005。另一候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程）可一并还上"从未真跑"的欠账。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler-upgrade` 从未真跑——**v2.2.0 起该欠债更吃劲**：`migrations/v2.2.0.md` 是首个含真实结构动作（`[sync-hooks]`）的配方，既有部署升级到 v2.2.0 必须真跑一遍拷贝+settings 合并。`[split]` 迁移接线已于 ITER-0035 补齐，仍差真实老项目端到端跑一遍。
