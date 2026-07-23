# MILE-0010 · Butler 长期规模治理

## 本次交付目标

让 Butler 在历史持续增长后仍能可靠交接、稳定编号，并以有界上下文恢复当前状态。

## 已完成内容

- R1 交付由权威状态确定性生成、可验鲜、陈旧可重建的 handoff。
- R2 统一至少四位且自然增长的 ITER/MILE 数字身份。
- R3 把双台账拆为有界热表、冷历史和机器索引。
- R4 交付幂等迁移、当前仓 dogfood 和万级规模验证。

## 关键变更 / 用户可感知变化

- handoff 不再靠 AI 记得手写，篡改或来源变化都会被识别。
- 冷启动读取量由全量历史降为固定 20 行热窗口；完整历史仍可追溯。
- `ITER-9999 → ITER-10000` 与 MILE 对应边界有机器回归。
- 独立的“确定性五件套产物链”已落 backlog，未混入本里程碑。

## 高层影响范围

- handoff、context persistence、iteration/milestone schema
- `tools/handoff/`、`tools/state-ledger/`
- hooks、状态审计、CI、项目知识与运行态台账

## 拆分路线图回填

| 路线 | 迭代 | 结果 |
|---|---|---|
| R1 可信 handoff | ITER-0083 | closed |
| R2 长编号身份 | ITER-0084 | closed |
| R3 双台账热冷分层 | ITER-0084 | closed |
| R4 迁移与规模验证 | ITER-0084 | closed |

## 验证方式与结果摘要

- ITER-0083：工具 6 项、hooks 197 项、完整 CI 与 Goal 裁决通过。
- ITER-0084：state-ledger 4 项、长编号 hook 31 项、万行 fixture、当前仓迁移、最终审计和完整 CI 通过。
- 所有失败诊断记录均保留，最终修复记录独立捕获。

## 已知剩余风险 / 延后事项

- 外部老项目未提供具体授权根，未执行跨项目写迁移；工具、当前真实仓和万级 fixture 已完成。
- fresh-context 独立复核因当前协作约束未执行，两个迭代均做了危险模式完整自审。
- 本地改动按用户要求不切板、不打 tag、不推送。

## 引用

- `.ai/milestones/MILE-0010/MILESTONE.md`
- `deliveries/ITER-0083-trusted-handoff.md`
- `deliveries/ITER-0084-scalable-state-ledgers.md`
- `.ai/state-index.json`

