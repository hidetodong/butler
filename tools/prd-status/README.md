# prd-status

Butler 多 PRD 的确定性只读查询器。规则真源是 `Coder/40_Context_Management/prd-status.md`。

```bash
python3 tools/prd-status/prd_status.py status --project-root /path/to/project
python3 tools/prd-status/prd_status.py status --project-root /path/to/project --prd-id 2026-07-22-user-login
python3 tools/prd-status/prd_status.py status --project-root /path/to/project --workspace @acme/web
```

退出码：0=有结果，1=合法查询但无匹配，2=输入或落盘合同错误。所有路径只读，不创建缓存或 receipt。
