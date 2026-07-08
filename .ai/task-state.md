# Task State

> 无活跃迭代 · dormant（`ITERATIONS.current: none`）。ITER-0034 段A（MILE-0003 R8 dogfood 迁 `.ai/project/` + 对齐现实）已收口。**待用户放行段B**——v2.0.0 切版 + 收口 MILE-0003。

## 当前状态

- 无活跃迭代。ITER-0034 段A 已收口（`.ai/project/` 8 文件建齐、旧 `.ai/PROJECT.md` 已删、3 规则文件对齐、独立复核 APPROVE、`feat` 提交）。butler 自身**现为文件夹态**。
- MILE-0003 仍 active——R1–R8 段A 全落，**剩段B 发布动作收尾整个里程碑与大版本**。
- **动手闸**：段B `git tag v2.0.0` 不可逆、对外发布锚点，执行前另请用户明确放行。

## 下一步入口

- **段B（切 tag 前请用户放行）**：`git log v1.7.0..HEAD` 核 hooks/schema 变更 → VERSION 1.7.0→2.0.0 + CHANGELOG `[2.0.0]` 聚合 ITER-0026~0034 + 产 `migrations/v2.0.0.md`（`[split]`+`[regen-claude]`+`[restamp]`）→ 收口 MILE-0003（MILESTONE 快照 + 聚合交付 + MILESTONES closed）→ 切版前 6 不变量预检 → `chore(release)` 提交 + `git tag v2.0.0` → 切版后三处版本载体对齐。
- 冷启动读序（butler 自身**现为文件夹态**）：`.ai/project/00_INDEX.md`（第一读，拿地图 → 按需钻主题）→ `.ai/ITERATIONS.md` / `.ai/MILESTONE.md` → 本文件 → 代码。
