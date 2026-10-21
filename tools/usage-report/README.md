# usage-report

按最后调用时间把入口分成四档。只出报告，不自动淘汰。C 档表示名单里没有记下调用，不是已经证实没人用。

```bash
python3 tools/usage-report/usage_report.py report --project-root .
python3 tools/usage-report/usage_report.py report --project-root . --since 90d
```
