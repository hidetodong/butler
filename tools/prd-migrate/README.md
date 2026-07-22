# PRD Migration Tool

标准库工具，用于 legacy 单 PRD 的显式迁移、回滚和钉版引用解析。所有命令都要求唯一 Butler `PROJECT_ROOT`。

```bash
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" inspect --project-root "$PROJECT_ROOT"
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" plan --project-root "$PROJECT_ROOT" --prd-id 2026-07-22-user-login --title "用户登录"
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" apply --project-root "$PROJECT_ROOT" --prd-id 2026-07-22-user-login --title "用户登录"
python3 "$BUTLER_PATH/tools/prd-migrate/prd_migrate.py" verify --project-root "$PROJECT_ROOT"
```

`inspect/plan/verify/resolve` 零写；`apply` 保留 backup 与 receipt；`rollback` 仅在当前集合和 backup hash 都对账时恢复。身份日期必须来自项目证据，工具不会猜。
