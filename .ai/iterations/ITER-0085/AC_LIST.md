---
状态: ack-frozen
ACK 日期: 2026-07-23
---

# Goal
- 让 ITER/MILE 冷历史真正按固定数字区间分片，并证明定向追溯只读取一个有界分片。

# In Scope
- 固定区间分片、v2 机器索引、lookup 定向查询、跨分片 check/audit、v1 单冷文件迁移、万级 fixture 与当前仓 dogfood。

# Out of Scope
- 不重编号、不改历史交付路径、不重写已归档 ITER-0084/MILE-0010 结论。

# Acceptance Checklist
- [ ] AC1: 冷历史按固定数字区间生成多个文件，任一分片最多含 `shard_size` 个身份。
- [ ] AC2: state index v2 保留 max_used/row_count/hot_count/cold_count/shard_count 与固定路由公式，根 index 大小不随分片数线性增长；每片同名回执记录 start/end/path/count/SHA-256。
- [ ] AC3: lookup ITER-NNNN/MILE-NNNN 只读取有界根 index、根热表以及至多一个命中分片/回执对，返回稳定 JSON 与读取字节数。
- [ ] AC4: check 跨热表与全部分片拒绝重复、缺失、重叠、错路由、坏哈希、孤立分片和坏身份。
- [ ] AC5: migrate 从 v1 单冷文件或未迁移全量表事务升级到 v2，删除旧单冷文件，重复执行字节级幂等。
- [ ] AC6: ITER 与 MILE 共用算法；数量不足时允许零冷分片，超过阈值时自然产生多个分片。
- [ ] AC7: 状态审计通过索引遍历分片，不依赖固定单冷路径，完整对账交付、归属与归档。
- [ ] AC8: 10,000 行 fixture 下每片最多 50 行、根 index 小于 4 KiB，lookup 读取量小于 64 KiB，且只打开根 index、热表与一个冷分片/回执对。
- [ ] AC9: 当前 Butler 仓迁移、handoff、状态审计、完整 CI 与 diff check 通过。

# Verification Method
- AC1–AC6、AC8：隔离单元测试覆盖多片、边界号、幂等、v1 升级、故障和坏索引。
- AC3、AC7、AC9：当前仓 migrate/check/lookup、状态审计与完整 CI。

# External References
- N/A

# Open Questions / Risks
- 固定 50 号区间会让早期小仓产生一个较稀疏分片，但换来路径稳定、无需重平衡和可直接计算路由。

