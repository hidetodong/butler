# Task State

> **无活跃迭代**（`ITERATIONS.current: none`）。里程碑 **MILE-0004** 仍 active，R1 已收口，下一块 R2。

## 当前状态

- `ITERATIONS.current: none`——上一迭代 **ITER-0036**（MILE-0004 R1 · references 索引化基座）已于 2026-07-09 原子收口，交付 `deliveries/ITER-0036-references-index-schema.md`。
- `MILESTONES.current: MILE-0004`（PRD 先行 + references 版本化改版同步，路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`）。R1 已落：新建 `Coder/40_Context_Management/references-schema.md` 契约地基。
- 全貌产物已前滚：`architecture.md` 补 references-schema、`frontier.md` 转 MILE-0004 战线。

## 下一步入口

- 开 MILE-0004 **R2**（PRD 切分机制：按语义/模块边界切 `prd/<slug>.md` 逐字保真 + 写登记表 + 小 PRD 单模块退化态 + soft 对齐拆法）→ 新开迭代号、走 P1–P5、ACK 冻结 AC 后进 P4。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
