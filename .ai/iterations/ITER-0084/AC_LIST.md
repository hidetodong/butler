---
状态: ack-frozen
ACK 日期: 2026-07-22
---

# Goal
- 让 ITER/MILE 身份跨五位边界稳定增长，并让双台账在历史增长后仍以固定热窗口冷启动、完整机器追溯。

# In Scope
- 至少四位身份、数字排序、双台账热冷分层、机器索引、事务迁移、跨分片审计、当前仓 dogfood 与万级 fixture。

# Out of Scope
- 不重编号、不改历史交付路径；没有具体项目根授权时不写外部老项目。

# Acceptance Checklist
- [ ] AC1: ITER/MILE 接受至少四位并按数字部分排序，9999→10000 成立。
- [ ] AC2: 两张根台账迁移后各自最多保留配置的热行数。
- [ ] AC3: 冷历史与机器索引保存全部身份、最大号、行数、路径和哈希。
- [ ] AC4: 跨热冷重复、坏身份或索引漂移 fail-closed。
- [ ] AC5: 迁移成组事务写入、重复执行字节级幂等。
- [ ] AC6: 状态审计跨分片对账，冷启动与 handoff 只消费有界热表。
- [ ] AC7: 万行 fixture 的热台账体积有界。
- [ ] AC8: 当前真实仓迁移、check、完整 CI 与 diff check 通过。
- [ ] AC9: 外部老项目在获得具体项目根授权后才允许写迁移；本轮无授权时 N/A。

# Verification Method
- AC1–AC7：state-ledger 隔离单元测试与万行 fixture。
- AC2–AC6、AC8：当前仓 migrate/check、状态审计和完整 CI。
- AC9：授权边界人工核对。

# External References
- N/A

# Open Questions / Risks
- 外部老项目未给出具体根路径，不能用危险模式或 bypass 扩张项目级写权限。

