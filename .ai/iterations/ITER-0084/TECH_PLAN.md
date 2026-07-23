# TECH_PLAN — ITER-0084

方案状态: pass
方案审查: dangerous-self-review

## 设计

1. `tools/state-ledger/state_ledger.py` 统一解析两张台账，身份正则至少四位，排序只取数字部分。
2. `migrate` 原子写根热表、`.ai/history/*.cold.md` 与 `.ai/state-index.json`；失败回滚。
3. `check` 重新计算全量视图，对比索引并核热表上限；状态审计存在索引时调用它，并跨热冷合并机器对账。
4. 根热表保留 current、说明和待办区，只把旧正式行移入冷文件；handoff 输入仍限定根热表。
5. 单元测试覆盖幂等、五位号、跨分片重复与一万行体积；当前仓 dogfood 证明真实迁移。

## 反证

- 字符串排序会在位数边界出错：明确转整数。
- 单文件写成功、另一文件失败会撕裂：临时文件 + 备份回滚。
- 只检查热表会漏重复：inspect 总是合并冷行。
- 外部项目未获路径授权：不擅自写入，AC9 N/A 并在里程碑交付披露。

