> ITER-0082 · active · 2026-07-22

## ADD

- `templates/hooks/lib/workspace_scope.py`、`templates/hooks/rules/workspace_scope.py`：共享工作区发现、钉版范围、写计划与逐目标 PreToolUse 门禁。
- `tools/workspace-scope/`：只读 discover/validate/check-plan/check-paths/check-diff CLI 与行为测试。
- `tools/mile0009-e2e/`：跨 inbox/migration/update/status/scope 的单工程回归和真实 apps 临时副本 dogfood runner。
- `templates/hooks/tests/test_workspace_scope_gate.py`、`test_workspace_scope_execution_contract.py`：宿主写前门禁与规则接线合同。

## EDIT

- `Coder/40_Context_Management/workspace-scope-schema.md`、TECH_PLAN/VERIFY/部署/README：补 Path Ownership、Module Workspace Scope、Workspace Write Plan、CLI/hook/diff 与扩张顺序真源。
- `templates/hooks/butler_gate.py`、plugin hooks、Codex 验证/registry：注册 workspace_scope 并覆盖 apply_patch/Edit/Write/MultiEdit。
- `tools/prd-migrate/prd_migrate.py`：兼容真实 legacy 的 `vN` doc revision，并在产品版并存时优先索引“源”行当前 doc version。
- `scripts/verify-ci.sh`：接入 inbox、migration、status、update、workspace 与 MILE-0009 e2e 行为组。

## DELETE

- 无。
