# Task State

> **无活跃迭代**（`ITERATIONS.current: none`）。里程碑 **MILE-0004** 仍 active，R1/R2 已收口，下一块 R3。

## 当前状态

- `ITERATIONS.current: none`——上一迭代 **ITER-0037**（MILE-0004 R2 · PRD 切分机制）已于 2026-07-09 原子收口，交付 `deliveries/ITER-0037-prd-split-mechanism.md`。
- `MILESTONES.current: MILE-0004`（PRD 先行 + references 版本化改版同步，路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`）。已落：R1 契约地基（`references-schema.md`）+ R2 切分机制（`prd-split.md` + 注入表触发）。
- 全貌产物已前滚：`architecture.md` 补 prd-split（动作层）、`frontier.md` 转 R3 战线。

## 下一步入口

- 开 MILE-0004 **R3**（首切入口并进 `/milestone` + 两海拔交叉指针：milestone 录入认"brief 是大 PRD"分支 → 触发 R2 切分机制；路线图项 ↔ 模块 slug 互指）→ 新开迭代号、走 P1–P5、ACK 冻结 AC 后进 P4。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
