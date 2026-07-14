# Task State

> **活跃里程碑 MILE-0005**（butler 命令命名空间系统）· **无活跃迭代**（ITER-0048 已收口切版 v2.8.0）· 下一步待用户放行 R3。标准模式。分支 `feat/mile-0005-butler-command-namespace`。

## MILE-0005 里程碑（active）

把 butler 散在规则正文里的「散文触发词」收敛成一整套 `/butler:xxx` 命名空间真实 slash command——补全菜单可见、全局任意项目可用、`butler:` 前缀隔离撞名。路线图：**R1** 地基（ITER-0047，✅ v2.7.0）→ **R2** 批量补 milestone/upgrade/ideation（ITER-0048，✅ v2.8.0）→ **R3** preference（子命令最多）→ **R4** loop/dangerous（加风险闸）。产物真源 `.ai/MILESTONE.md`。

## 已收口：ITER-0048（R2 批量命令 · v2.8.0）

- 3 薄壳命令落地：`/butler:milestone`（+`status`）、`/butler:upgrade`、`/butler:ideation`，各委托真源、带优雅降级、跨 cwd 路径约定段。
- `/butler-upgrade`→`/butler:upgrade` 全仓 6 处触发名迁移（非算法）；capabilities 三行转换 + 删 `/review` 冗余；README 子树补三命令。
- 隔离 HOME 实跑坐实 **R1 目录软链自动托管新命令**（5/5 可达、`setup.sh` 未改一行）——范式可批量复制得证。
- AC1–AC9 全过，标准模式复核（未升格独立复核）。交付 `deliveries/ITER-0048-namespace-commands-batch.md`。

## 下一步入口

- **待用户放行 R3**（`/butler:preference`：`on`/`off`/`reback`/`distill` 四子命令全走 `$ARGUMENTS` 参数路由，委托 `70_Extension_Preference` 真源）——参数面最宽、单开一迭代把分派写扎实。R4（loop/dangerous 加风险闸）随后。设计未锁，不擅自连跑。
- git 收尾：feat + chore(release) 提交、本地 tag v2.8.0、推分支、PR #3 增长（不合并 main、不推 tag 到远端）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → `.ai/MILESTONE.md` → 代码。
