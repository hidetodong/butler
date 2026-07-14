# Task State

> **活跃里程碑 MILE-0005**（butler 命令命名空间系统，仍 active）· **无活跃迭代**（ITER-0049 已收口 R3、`current: —`）· 下一步 **R4（`/butler:loop` + `/butler:dangerous` 加风险闸）待开题**。标准模式。分支 `feat/mile-0005-butler-command-namespace`。切版 v2.9.0 已本地提交 + 打 tag，**tag 未推远端**（待用户授权）。

## MILE-0005 里程碑（active·剩最后一路线项）

把 butler 散在规则正文里的「散文触发词」收敛成一整套 `/butler:xxx` 命名空间真实 slash command。路线图：**R1** 地基（ITER-0047，✅ v2.7.0）→ **R2** 批量补 milestone/upgrade/ideation（ITER-0048，✅ v2.8.0）→ **R3** preference（ITER-0049，✅ v2.9.0）→ **R4** loop/dangerous 加风险闸（未开题）。产物真源 `.ai/MILESTONE.md`。

## ITER-0049（closed·R3 最宽参数命令）

- **已交付**：`/butler:preference` 薄壳——全批**参数面最宽**：4 子命令 `on`/`off`（隐私总开关）、`reback on|off`（影响回路、**唯一二级嵌套参数**）、`distill`（手动蒸馏）+ 空参只读状态回声。委托 `preference-probe-engine` 真源、不复述算法、收尾回声状态。`/preference`→`/butler:preference` 全仓活文档迁移，`templates/` 刻意保留旧名（DD5 边界）。
- **AC1–AC9 全过**；隔离 HOME 实跑 6/6 命令经 R1 目录软链可达、`setup.sh` 未改一行、`templates/` 与 `scripts/` 边界零改动。判 MINOR·切 v2.9.0。
- 归档 `.ai/iterations/ITER-0049/`（五件套）；交付 `deliveries/ITER-0049-preference-namespace-command.md`+`.html`。

## 下一步入口

- **R4 开题**（`/butler:loop` + `/butler:dangerous`）：高风险命令加闸——命令薄壳前置风险提示与确认闸，委托 `55_Extension_ConvergenceLoop` / `65_Extension_Dangerous` 真源；单独设计以确保命令化**不降低**「郑重显式触发」门槛（不照抄低风险轻壳）。R4 收口后可整体收 MILE-0005。设计未锁，开题走 P1。
- **待用户授权动作**：push tag `v2.9.0`（连同 R1/R2 的 v2.7.0/v2.8.0）到远端 github；合并 PR #3 到 main。均**未授权**、不擅自做。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → `.ai/MILESTONE.md`（MILE-0005 §5.3 路线图 R4）→ 代码。
