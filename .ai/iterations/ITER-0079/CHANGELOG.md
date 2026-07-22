> ITER-0079 · active · 2026-07-22

## ADD

- `tools/prd-migrate/prd_migrate.py` + README：inspect/plan/apply/verify/rollback/resolve、staging/backup/receipt 与路径边界 → AC3–AC7
- `tools/prd-migrate/tests/test_prd_migrate.py`：11 项多引用、零写、事务、故障恢复、历史解析、坏输入与越界 receipt fixture → AC3–AC7, AC9
- `docs/prd-migration-guide.md`：身份日期证据、MILESTONE/AC、执行、验证、恢复与备份清理指南 → AC8
- `templates/hooks/tests/test_multi_prd_migration_contract.py`：三阶段 schema、迁移/指南结构合同 → AC1, AC2, AC7–AC9

## EDIT

- `acceptance-schema.md`、`tech-plan-schema.md`、`verify-schema.md`：`prd_refs` 多需求钉版与 legacy 单值兼容 → AC1–AC3, AC7
- `references-schema.md`：显式迁移、receipt、resolver 与历史零回写合同 → AC3–AC7
- `HUMAN_GUIDE.md`、`Coder/README.md`：迁移指南和工具入口 → AC8
- `scripts/verify-ci.sh`：收件箱与 PRD 迁移行为测试纳入唯一完整入口 → AC9
- `test_prd_collection_contract.py`：R1 planned 断言翻转为 R5 已交付边界 → AC7, AC9

## DELETE

- 无
