# frontier（当前形态 / 活跃战线 / 下一个瓶颈）

> 变得最快的一层。战线收了就覆盖删除，不叠历史。

## 当前形态

- **版本**：**v2.10.0 已切版**——聚合 ITER-0050（MILE-0005 R4 收官落两个高风险命令 `/butler:loop`〔收敛闭环死磕，无参 / 无持久态 / 无 off，跑到全绿或 §6 熔断〕+ `/butler:dangerous`〔无人值守自治，空参=开启 / off / status 只读，持久态外化 `.ai/local-constraints.md`〕，**唯一新面是风险闸**〔命令化不降「郑重显式触发」门槛：frontmatter ⚠️ + 第 0 步风险提醒 + 闸交回引擎不复述护栏〕+ `/loop`·`/dangerous`→`/butler:*` 全仓 22 活文档触发名迁移〔harness 级 `/loop` 精确保留、`templates/` 刻意留旧名〕+ capabilities 两行升级），MINOR·新增两命令能力，配方 `migrations/v2.10.0.md` 为部署面 `[no-op]`+`[restamp]`（新命令由 R1 目录软链自动托管、`setup.sh` 未动、触发名迁移不碰 templates 故无 `[regen-claude]`）。上一版 v2.9.0 = ITER-0049（R3 最宽参数 `/butler:preference` + 二级嵌套参数）；再前：v2.8.0 = ITER-0048（R2 批量三命令）、v2.7.0 = ITER-0047（R1 地基）、v2.6.0 = ITER-0046（沟通风格常开正本）、v2.5.0 = ITER-0045、v2.4.0 = ITER-0044、v2.3.0 = ITER-0043、v2.2.0 = ITER-0042、v2.1.0 = MILE-0004、v2.0.0 = MILE-0003 MAJOR。
- **无活跃里程碑 · 无活跃迭代**（`MILESTONES.current: —`、`ITERATIONS.current: —`）。**MILE-0005（命令命名空间系统）已于 2026-07-14 整体收官**——R1（ITER-0047·v2.7.0）、R2（ITER-0048·v2.8.0）、R3（ITER-0049·v2.9.0）、R4（ITER-0050·v2.10.0）全收口，路线图走完。再往前 ITER-0042~0046 均独立迭代（无所属里程碑）、均已收口切版。butler 处于版本发布后的空档、等下一任务开题。
- **butler 命令进入 `/butler:` 命名空间体系已成体系（MILE-0005 R1–R4 全落）**：`.claude/commands/butler/` 子目录＝冒号前缀（`butler/<name>.md`→`/butler:<name>`），`setup.sh` **软链整个命名空间目录**进 `~/.claude/commands/butler`、**所有项目可用**、加命令自动全局生效（R2–R4 连续实跑坐实：往 `butler/` 丢新 `.md` 无需改 `setup.sh` / 无需重跑即全局可用，末次隔离 HOME 实跑 **8/8** 命令可达）。现有 **8 个成员**：`/butler:prd`（PRD 先行三分支）、`/butler:review`（复核，默认自检 / `independent`）、`/butler:milestone`（里程碑录入 / `status` 看板）、`/butler:upgrade`（已部署项目升级，原 `/butler-upgrade`）、`/butler:ideation`（需求脑暴）、`/butler:preference`（偏好探针开关，`on`/`off`/`reback on|off`/`distill` + 空参只读回声，**参数面最宽·唯一二级嵌套参数**，原 `/preference`）、`/butler:loop`（收敛闭环死磕，无参 / 无持久态 / 无 off，原 `/loop`）、`/butler:dangerous`（无人值守自治，空=开启 / off / status，持久态外化，原 `/dangerous`）。范本＝薄壳路由器（委托真源不复述 + 第 0 步优雅降级 + frontmatter 两行说人话），已证吃得下**二级嵌套参数**（preference）与**风险闸**（loop/dangerous）两种复杂度。高风险命令的风险闸＝frontmatter ⚠️ + 第 0 步风险提醒 + 闸交回引擎（命令化不降「郑重显式触发」门槛、又守 DRY）。选型全局软链（与规则全局引用同模型、零漂移），不进 `templates/`、不逐项目部署（个人工具边界沿用 ITER-0044）。`/butler:loop` 与 Claude Code 自带 `/loop` 靠命名空间前缀消歧、`dangerous-engine.md:21` harness 引用加注澄清。
- **个人沟通风格收敛为单一正本 + 常开（ITER-0046）**：过去「怎么跟用户说话」的规矩散在本机 Matrix 输出风格（只有切到才生效）与多个风格记忆文件、说人话还双写；现收敛成 `communication-style.md`（仓根唯一正本），经 `setup.sh` @import 进全局 CLAUDE.md **每会话常开、跨机器同步**。Matrix 输出风格退休（本机删 + 拆 `claudep` 的 `--settings` 参数）、三风格记忆掏成只记来龙去脉的薄壳。与 slash command 同走「全局机器级、不逐项目」模型。
- **PRD 全生命周期子系统成型 + 触发已加固**：`references-schema`(R1 契约 + §9 非回归门) + `prd-split`(R2 首切) + `/milestone` 大 PRD 并进(R3) + AC 钉版 `prd_version`(R4) + `prd-update` 改版同步(R5+R6 认亲松边) + ITER-0042 触发加固。opt-in 加层，非 PRD 流全程未动。

## 活跃战线

- **无活跃里程碑/迭代**——MILE-0005 收官后 butler 在版本发布空档。下一任务可直接开独立迭代或按需开新里程碑；开题闸已解除（`current` 均为 `—`）。
- **PRD 全链首次端到端实战：部分踩过、仍未走完**。ITER-0042 的实战（Confluence+MCP+`/butler:milestone`）暴露并修掉了**触发漏切**，但那次没走到切分/钉版/改版——命门红线（切片逐字无损、绝不切碎、映射/版本单一真源、亮牌不自动改已冻结、松边不硬认、非回归门 git diff 为空）与 R4 钉版回溯、R5 冻快照仍待真"拿一份大 PRD 走导入→改版全程"检验。

## 下一个瓶颈

- **命名空间里程碑已收，下一步是把命令能力真正跑起来验**：8 命令的**入口**都已落地并结构验证，但运行时行为多数没新验——尤其 `/butler:dangerous`（无人值守自治端到端）、`/butler:upgrade`（真实老项目端到端升级）两笔历史欠债仍悬（见 `debt.md`），命令化只是把它们摆上菜单、没消除欠债。真正的下一个价值点：拿真实场景把这两条端到端跑一遍。
- **PRD 全链真实 dogfood**（拿一份真 PRD 走导入→切分→钉版→改版全程）可一并还上"从未真跑"的欠账——命门红线仍待真实检验。
- **两笔历史欠债仍悬着**（见 `debt.md`）：hook 在 butler 侧不 live、`/butler:upgrade` 从未真跑——`migrations/v2.2.0.md` 起配方含真实结构动作（`[sync-hooks]`），既有部署升级必须真跑一遍拷贝+settings 合并。`[split]` 迁移接线已于 ITER-0035 补齐，仍差真实老项目端到端跑一遍。
