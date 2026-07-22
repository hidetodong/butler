# prd-update

指定 `prd_id` 的确定性改版事务。语义切分/认亲先按 `Coder/40_Context_Management/prd-update.md` 对齐，再把确认结果写成 JSON spec；本工具只负责 plan、hash、archive/live/index/receipt 事务、verify 与 rollback。

```bash
python3 tools/prd-update/prd_update.py plan --project-root /project --spec update.json
python3 tools/prd-update/prd_update.py apply --project-root /project --spec update.json
python3 tools/prd-update/prd_update.py verify --project-root /project --prd-id 2026-07-22-login
python3 tools/prd-update/prd_update.py rollback --project-root /project --prd-id 2026-07-22-login
```

plan/verify 零写；0=成功且 apply-ready/已验证，1=合法但未确认、缺处置或无更新，2=输入/现场/事务错误。apply 成功保留 `.ai/references/.prd-update-backups/<update_id>`，rollback 只在整树 hash 未漂移时允许。

Spec v1：

```json
{
  "schema_version": 1,
  "prd_id": "2026-07-22-login",
  "expected_old_version": "v1.0",
  "new_version": "v1.1",
  "confirmed": true,
  "confirmation": {"mode": "user-ack", "at": "2026-07-22T10:00:00+08:00"},
  "active_modules": [
    {"module_slug": "login-flow", "title": "登录流程", "source": "sources/login-flow.md", "origins": ["login-flow"]}
  ],
  "removed_slugs": [],
  "dispositions": [
    {"path": ".ai/iterations/ITER-0001/AC_LIST.md", "decision": "keep-pinned-history", "note": "历史保持旧版"}
  ]
}
```

`source` 相对 spec 文件解析；其 UTF-8 bytes 原样成为 live 切片并进入 receipt hash。每个 impact path 的允许 decision 见规则真源。
