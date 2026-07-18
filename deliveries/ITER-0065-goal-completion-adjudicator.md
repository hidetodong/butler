# ITER-0065 · Goal 完成裁决器

> 2026-07-18 · MILE-0008 R5 · 危险模式自主 ACK / 完整审查

## 目标
用只读程序聚合完成资格事实，拒绝“任务做完但目标未达成”。

## 已完成
- 标准库 CLI，稳定 JSON 与 exit 0/1/2；全量 checks/reasons。
- 聚合 AC、plan、calibration、hot evidence、review/blocker 与 active ledger；不读 host/tasks。
- 正向 eligible、GFC-001–008 全拒绝、未知值 fail-closed、只读 hash 回归。
- VERIFY Completion Inputs 与生命周期/规则卡接线。

## 验证
- 13/13 tests、135 hooks 与完整矩阵通过；本仓真实 evaluate 十项 checks 全绿、verdict=eligible。
- 强审修复 evidence v1 fixture schema 漂移 1 Must Fix，最终清零。

## 风险与下一步
- eligible 不等于 complete；R6 接宿主与部署升级。未执行独立复核。

## 引用
- `.ai/iterations/ITER-0065/`
- `tools/goal-assurance/`
- checkpoint `4357c76`
