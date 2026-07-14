# Task State

> **无活跃里程碑 · 无活跃迭代**（`MILESTONES.current: —`、`ITERATIONS.current: —`）。上一个里程碑 **MILE-0005（butler 命令命名空间系统）已于 2026-07-14 整体收官**（R1–R4 全落、8 命令齐），末迭代 **ITER-0050（R4·收官）已收口切 v2.10.0**。butler 处于版本发布后的空档，等下一个任务开题。

## 刚收口：MILE-0005 里程碑（closed·2026-07-14）

把 butler 散在规则正文里的「散文触发词」收敛成一整套 `/butler:xxx` 命名空间真实 slash command、全局任意项目可用。路线图全落：**R1** 地基 + `/butler:prd` 迁移（ITER-0047·v2.7.0）→ **R2** 批量补 milestone/upgrade/ideation（ITER-0048·v2.8.0）→ **R3** 最宽参数 preference〔二级嵌套参数〕（ITER-0049·v2.9.0）→ **R4** loop/dangerous 加风险闸〔收官〕（ITER-0050·v2.10.0）。成果：命名空间目录 + **8 命令**（prd/review/milestone/upgrade/ideation/preference/loop/dangerous）+ `setup.sh` 一条目录软链自动托管全套 + 薄壳路由器范本（已证吃得下二级嵌套参数与风险闸两种复杂度）。聚合交付 `deliveries/milestones/MILE-0005-command-namespace-system.md`；里程碑产物归档 `.ai/milestones/MILE-0005/MILESTONE.md`。

## 待放行 / 待授权

- **本地已切 v2.10.0**（VERSION/CHANGELOG/migrations/v2.10.0.md + 本地 tag）；feat 提交 + 独立 chore(release) 提交已落、分支 `feat/mile-0005-butler-command-namespace` 已推、draft PR #3 增长。**未合并 main、未推 tag v2.10.0 到远端**——两者待用户显式授权。

## 下一步入口（下一任务开题时）

- 无活跃里程碑/迭代，开题闸已解除：新任务可直接开独立迭代，或按需开新里程碑。候选积压见 `.ai/project/frontier.md`「下一个瓶颈」+ `debt.md`（两笔历史欠债仍悬：hook 在 butler 侧不 live、`/butler:upgrade`·`/butler:dangerous` 端到端从未真跑；PRD 全链真实 dogfood 从未走完）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → `.ai/project/frontier.md` → 代码。
