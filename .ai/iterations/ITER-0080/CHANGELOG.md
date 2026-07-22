> ITER-0080 · active · 2026-07-22

## ADD

- `Coder/40_Context_Management/prd-status.md`：多 PRD 列表、prd_id/workspace 筛选、legacy 与零写合同 → AC5, AC6
- `tools/prd-status/prd_status.py` + README：标准库只读 CLI、稳定 JSON/退出码、双索引和 workspace map 交叉核验 → AC5, AC6
- `tools/prd-status/tests/test_prd_status.py`：14 项 collection/legacy/filter/zero-write/malformed/symlink fixture → AC5, AC6, AC9
- `templates/hooks/tests/test_prd_split_status_contract.py`：首切、指针、双宿主和 CI 结构合同 → AC1–AC4, AC7–AC9

## EDIT

- `prd-split.md`、`references-schema.md`：身份四态、日期证据、双层索引与 Workspace Scope 一次对齐 → AC1–AC4
- `milestone-schema.md`：新交叉指针升级为 `<prd_id>#<module_slug>`，旧指针只读兼容 → AC7
- `prd-update.md`：显式目标 `prd_id` 前置，status 分工移交；R7 未交付边界亮牌 → AC8
- Claude command、Codex skill、registry/openai projection：统一 split/update/status 参数与薄路由 → AC8
- `Coder/README.md`、`scripts/verify-ci.sh`：注册 status 规则/工具和行为测试 → AC9

## DELETE

- 无
