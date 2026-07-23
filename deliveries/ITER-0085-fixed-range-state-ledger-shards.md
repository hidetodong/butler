# ITER-0085 · 真正的 ITER/MILE 区间分片纠偏

## 本次交付目标

补上上一轮遗漏的真正分片能力：让 ITER/MILE 历史、根导航和单号追溯都保持有界，同时保留完整可审计历史。

## 已完成内容

- 双台账旧行按固定 50 号区间写入独立 Markdown 冷片，每片配同名 JSON 校验回执。
- 根 state index 改为固定路由公式，不再逐片追加目录；支持 inspect、migrate、check、lookup。
- v1 单冷文件可事务迁移，重复执行字节幂等，故障恢复旧状态。
- 状态审计跨全部冷片对账，日常追溯只读取一个命中片。
- 当前仓 85 条 ITER 已迁移为 20 条热记录和 65 条冷记录（2 片）。

## 关键变更 / 用户可感知变化

- 查旧 ITER/MILE 不再读取整份无限增长冷文件；编号可直接计算命中片。
- 根 index 当前为 941 字节，10,000 行 fixture 下仍小于 4 KiB。
- 非规范零号、过度补零、热表/冷片/回执漂移会明确拒绝，不返回不可信结果。
- ITER-0084 与 MILE-0010 的旧归档保持原样；本交付如实作为独立纠偏记录。

## 高层影响范围

- `tools/state-ledger/`：分片、路由、回执、事务迁移与查询实现。
- `scripts/audit-project-state.py`：v2 分片全量审计。
- `Coder/`、规则卡和人类指南：双台账复合真源、冷启动与身份分配口径。
- `.ai/history/`、`.ai/state-index.json`：当前仓真实迁移结果。

## 验证方式与结果摘要

- state-ledger 最终 12/12，状态审计测试 24/24。
- 10,000 行 fixture 生成 200 个冷片；每片最多 50 行，单次 lookup 读取量小于 64 KiB。
- 当前仓 check、冷号 lookup、handoff 与完整 `scripts/verify-ci.sh` 最终通过。
- 失败证据保留：首次完整 CI 暴露 task-state 投影回归；active 审计记录了收口前 fold receipt 必然陈旧，均按契约纠正或在收口后复核。

## 已知剩余风险 / 延后事项

- 无阻断风险。固定区间允许稀疏片，这是稳定路径与直接路由的明确权衡。
- 按用户要求，本轮不提交、不打 tag、不推送。

## 引用

- `.ai/iterations/ITER-0085/CONCEPT.md`
- `.ai/iterations/ITER-0085/AC_LIST.md`
- `.ai/iterations/ITER-0085/TECH_PLAN.md`
- `.ai/iterations/ITER-0085/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0085/evidence/`

