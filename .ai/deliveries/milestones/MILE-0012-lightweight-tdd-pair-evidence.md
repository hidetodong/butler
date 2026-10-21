# MILE-0012 · 轻量 TDD 配对证据

## 本次交付目标

用现有 evidence record 建立最小可用的 TDD 纪律：明确选择 TDD 的任务必须交回同一测试命令先失败、后通过的机器证据。

## 已完成内容

- R1 建立 TECH_PLAN cycle 声明、稳定 evidence ID 和 Red/Green 配对检查器。
- R2 把配对接入 P5/Goal 完成门，增加 VERIFY 投影并用 pytest 真实 dogfood。
- 未启用 TDD 的项目和旧产物保持 N/A/零行为变化。

## 关键变更 / 用户可感知变化

AI 不能再只写“按 TDD 开发”；已声明 cycle 必须有经完整性校验的 Red/Green record，否则 Goal 不允许收口。

## 高层影响范围

verification evidence CLI、Goal 完成裁决、P5/VERIFY 合同、artifact pipeline、规则真源和双宿主规则卡。

## 验证方式与结果摘要

R1 与 R2 都已收口；R2 真实 Red→Green 配对通过，最终完整 CI 通过，Goal 裁决为 `eligible`。

## 已知剩余风险 / 延后事项

- 更强的过程证明，包括防测试改弱、有效 Red 分类、跨语言 adapter 和 diff 对账，仍在 `tdd-evidence-hardening` 候办中。
- 两个迭代均为危险模式自主 ACK，已执行 P5 强审，未执行 fresh-context 独立复核。

## 引用

- `.ai/milestones/MILE-0012/MILESTONE.md`
- `deliveries/ITER-0091-lightweight-tdd-pair-checker.md`
- `deliveries/ITER-0092-tdd-goal-gate-dogfood.md`

## 拆分路线图回填

| 路线项 | 迭代 | 结果 | 交付 |
|---|---|---|---|
| R1 轻量配对合同与检查器 | ITER-0091 | closed | `deliveries/ITER-0091-lightweight-tdd-pair-checker.md` |
| R2 生命周期接线与 pytest dogfood | ITER-0092 | closed | `deliveries/ITER-0092-tdd-goal-gate-dogfood.md` |
