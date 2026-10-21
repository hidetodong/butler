<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0125 变更流

> 升级器补上删除与移动 · closed · 2026-10-21

## ADD

- 无

## EDIT

- `Coder/20_Workflow_Lifecycle/migration-schema.md` §4 — 在 `[rename]` 后补上 `[delete]` 和 `[move]`，写明起始态、重复执行和冲突即停；`[split]` 整段保留 → AC1
- `tools/butler-upgrade/upgrade.py` — 动作表认识 `delete` 和 `move`，校验路径，按起始态执行，失败能退回目录 → AC2 / AC3 / AC4 / AC5
- `tools/butler-upgrade/README.md` — 项目域那一行写上 `delete/move` → AC2
- `scripts/test-butler-upgrade.py` — 用临时目录覆盖删除、移动、拒绝和回滚，并锁住没有 v4 配方、版本仍是 3.6.0 → AC2 / AC3 / AC4 / AC5 / AC6
- `.ai/debt.md` — 已部署残留那条改成：动作已经有了，配方和真实清理仍在 R15

## DELETE

- 无
