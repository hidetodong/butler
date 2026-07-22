# MILE-0009 End-to-End

在单一临时工程中串联 inbox、legacy PRD migration、多 PRD/status、确定性 update receipt 与 workspace scope/diff 门禁。测试只写临时目录，不修改样本仓。

```bash
python3 -m unittest discover -s tools/mile0009-e2e/tests -v
```

真实样本只读 dogfood 用 `apps_dogfood.py`：它复制 `.ai` 与 workspace manifests 到系统临时目录，完成 discover + migration 全回路，自动清理副本，并以 Git status/PRD tree 双 hash 证明原样本零写。
