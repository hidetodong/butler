<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0120 变更流

> 根布局整理：backlog 与 deliveries 迁入 .ai · closed · 2026-09-14

## ADD

- `.ai/backlog/` — 由 `.ai/milestone-backlog/` 改名而来，10 份候办草稿文件名不变 → AC1
- `.ai/deliveries/` — 由仓根 `deliveries/` 整树搬入，272 个文件，保留 `milestones/` 子目录 → AC4
- `.ai/iterations/ITER-0120/ac-sweep.py` — 本轮路径扫描 → AC12

## EDIT

- `tools/intake/intake.py` — 孵化区相对路径改成 `.ai/backlog` → AC2
- `scripts/audit-project-state.py` — 候办目录与台账交付列按新路径解析 → AC3 / AC5
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` / `mcv-deployment.md` / `iteration-schema.md` / `milestone-schema.md` — 交付落点与部署只建 `.ai/` → AC6
- `Coder/40_Context_Management/context-persistence.md §6` — 读序与 closed 交付自检改指 `.ai/deliveries/`，四处投影同步 → AC7
- `.ai/ITERATIONS.md` 与冷分片 — closed 行交付列改成 `.ai/deliveries/…` → AC5
- `CHANGELOG.md` — 「去哪找文件」的链接改新路径 → AC12
- `.ai/MILESTONE.md` §5.4 — 登记 R9 迁移判定 → AC10
- `tools/context-budget/tests/test_context_budget.py` — `order_bytes` 1284 → 1288 → AC7 / AC11

## DELETE

- `.ai/milestone-backlog/` — 目录改名，旧路径不再存在 → AC1
- 仓根 `deliveries/` — 整树搬走，不留软链 → AC4
