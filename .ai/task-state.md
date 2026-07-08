# Task State

> 当前**无活跃迭代**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。上一迭代 ITER-0035（补 `[split]` 升级接线缺口）已于 2026-07-08 收口。

## 当前状态

- 无活跃迭代 / 里程碑。等下一个需求录入（工程任务自然触发 P1，或 `/milestone` 录大版本方向、`origin/` 收件箱）。
- 最近收口：ITER-0035 给 `/butler-upgrade` 执行器补齐 `[split]` 迁移标签接线，并定死其为 opt-in（先问再迁、守两态并存）。交付 `deliveries/ITER-0035-split-upgrade-wiring.md`。

## 下一步入口

- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md`（第一读）→ `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` → 本文件 → 代码。
- 悬着的欠债见 `.ai/project/debt.md`：`/butler-upgrade` 从未在真实老项目端到端跑过（含本轮新接的 `[split]` opt-in 路径）。
