# usage

记下 Butler CLI 入口的最后调用时间。数据在项目 `.ai/.usage.json`，进 gitignore。90 天分档报告在 `tools/usage-report/`。

```bash
python3 tools/usage/usage.py record --project-root . --id tool:intake
python3 tools/usage/usage.py show --project-root .
python3 tools/usage/usage.py catalog
```

未知 id 拒绝写入。写盘失败不影响原命令。
