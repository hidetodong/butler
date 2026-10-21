# ITER-0084 · 长编号与有界双台账

## 本次交付目标

让 ITER/MILE 跨五位边界稳定增长，并把随历史膨胀的两张根台账改成固定热窗口、冷历史和机器索引。

## 已完成内容

- 身份契约升级为至少四位，排序与最大号统一按数字部分。
- 新增 inspect/migrate/check 工具，事务写入热表、冷历史和 state index。
- 状态审计跨热冷全量对账，handoff 与冷启动只消费根热表。
- 完成当前真实仓迁移、五位边界、幂等、重复拒绝和一万行规模验证。

## 关键变更 / 用户可感知变化

- 当前仓 84 条迭代历史中，根热表只留最新 20 条，其余 64 条进入冷历史。
- 完整历史仍可由机器索引追溯，迁移不重编号、不改交付路径。
- 首轮审计/CI 的失败事实保留，修复后最终审计和完整 CI 通过。

## 高层影响范围

- `tools/state-ledger/`
- `.ai/history/`、`.ai/state-index.json`
- ITER/MILE schema、共享 hooks、状态审计、CI 和冷启动文档

## 验证方式与结果摘要

- state-ledger 4/4，长编号 hook 专项 31/31，hooks 总矩阵 197 项。
- 10,000 行 fixture 保持 20 行热表且小于 8 KiB。
- 当前仓 dogfood、最终状态审计、Goal 十项裁决和修复后完整 CI 通过。
- 证据：`.ai/iterations/ITER-0084/evidence/`。

## 已知剩余风险 / 延后事项

- 未提供获授权的外部老项目根，因此没有跨项目写迁移；这项按授权边界记为 N/A。
- 本迭代由模型自主 ACK 并完成 P5 强审；未执行 fresh-context 独立复核。
- 用户要求本轮不切板、不 tag、不推送。

## 引用

- `.ai/iterations/ITER-0084/`
- `.ai/iterations/ITER-0084/evidence/`
- `.ai/state-index.json`
- `tools/state-ledger/`

