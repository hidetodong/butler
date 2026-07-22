# Butler Inbox Scanner

确定性扫描项目根 `origin/`，维护 `.ai/INBOX.md` managed block；不读取语义、不分类、不修改来源文件。

```bash
python3 "$BUTLER_PATH/tools/inbox/inbox.py" scan --project-root <PROJECT_ROOT>
python3 "$BUTLER_PATH/tools/inbox/inbox.py" scan --project-root <PROJECT_ROOT> --apply
python3 "$BUTLER_PATH/tools/inbox/inbox.py" status --project-root <PROJECT_ROOT>
```

- `scan` 默认 plan，JSON 报告 added/changed/unchanged/missing/rejected，零写入。
- `--apply` 只原子更新 `.ai/INBOX.md` 的 `butler-inbox:managed` 块。
- managed marker 外内容逐字保留；marker 重复、残缺或表头漂移时 exit 2 且零写入。
- `origin/` 不存在按空收件箱处理，不创建；符号链接不跟随并列入 rejected。
- 语义分类、确认和派生路由见 `Coder/40_Context_Management/inbox-workflow.md`。
