# Task State

> **无活跃迭代**（`ITERATIONS.current: none`）。里程碑 **MILE-0004** 仍 active，R1–R3 已收口，下一块 R4。

## 当前状态

- `ITERATIONS.current: none`——上一迭代 **ITER-0038**（MILE-0004 R3 · 首切入口并进 /milestone + 两海拔交叉指针）已于 2026-07-09 原子收口，交付 `deliveries/ITER-0038-milestone-prd-entry.md`。
- `MILESTONES.current: MILE-0004`（路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`）。已落：R1 契约（`references-schema`）+ R2 切分机制（`prd-split`）+ R3 `/milestone` 并进入口 + 两海拔交叉指针。"一份输入喂两个海拔"闭环成型、但未版本化。
- 全貌产物已前滚：`frontier.md` 转 R4 战线、`capabilities.md` `/milestone` 补 PRD 并进。

## 下一步入口

- 开 MILE-0004 **R4**（AC 钉版 + P2/P3/P5 接线：AC frontmatter 加 `prd_version` 冻结绑定、版本化 slug 引用锚点 + 扩展 acceptance/tech-plan/verify 的 External References 版本化、Compliance 对钉住版核）→ 新开迭代号、走 P1–P5、ACK 冻结后进 P4。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
