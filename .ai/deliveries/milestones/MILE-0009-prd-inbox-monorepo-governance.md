# MILE-0009 · 需求收件箱、多 PRD 与 Monorepo 范围治理

## 本次交付目标

把 Butler 从“单份 PRD 持续改版”升级为“独立需求持续进入、每份需求独立版本化”，并把原始材料、身份、引用、更新与 monorepo 写范围接成可审计闭环。

## 已完成内容

- 建立日期化稳定 `prd_id`、项目级需求集合、单需求模块/归档和多 PRD 独立钉版。
- 建立只读 origin 收件箱、`.ai/INBOX.md` 指纹/状态/派生关系，以及 `/butler:inbox` 分类路由。
- 交付 legacy 三阶段迁移、历史 resolver、人类迁移指南、按 `prd_id` 首切/status 和确定性 update receipt 事务。
- 建立工作区地图、四类 PRD Scope、模块收窄、显式 Path Ownership、TECH_PLAN 写计划、PreToolUse 与 diff 门禁。
- 用单工程组合回归和真实 apps 临时副本证明 R1–R8 能共同工作，且真实样本零写。

## 关键变更 / 用户可感知变化

- 新需求与已有需求新版不再混为一次全局 PRD 升级；每份需求有独立身份、版本、模块和历史。
- 使用者可从原稿追到派生产物，从 AC 精确还原多份需求的冻结版本，也可从 status 按需求或 workspace 查询。
- 改版由显式确认 spec 驱动，先归档再更新，receipt/verify/rollback 不依赖对话记忆。
- monorepo 写入不再仅靠自然语言约束；越界必须先扩 PRD Scope、重冻 AC 并重审方案。

## 高层影响范围

- PRD references、split/status/update/migration 与 inbox 全链路
- AC/TECH_PLAN/VERIFY、里程碑/迭代与项目知识契约
- Claude/Codex 双宿主入口、hooks、驻留工具、插件 registry 和完整 CI

## 拆分路线图回填

| 路线 | 迭代 | 结果 |
|---|---|---|
| R1 需求集合与日期化身份 | ITER-0075 | closed |
| R2 Monorepo 地图与范围契约 | ITER-0076 | closed |
| R3 收件箱数据契约 | ITER-0077 | closed |
| R4 inbox 命令与分类路由 | ITER-0078 | closed |
| R5 多 PRD 引用、迁移与指南 | ITER-0079 | closed |
| R6 首切、状态与命令适配 | ITER-0080 | closed |
| R7 确定性改版与回执 | ITER-0081 | closed |
| R8 范围门禁与端到端验证 | ITER-0082 | closed |

## 验证方式与结果摘要

- 八个承接迭代均有冻结验收、验证报告、evidence、双格式交付和 closed 台账事实。
- 最终完整 CI 在 Python 3.12.12 / uv 0.9.28 下通过；hooks 195 项、六组驻留工具行为与组合 e2e 全绿。
- 真实 apps 只读 dogfood 验证 28 个 workspace、active/queued 里程碑标记、active/closed 引用影响与 legacy migration/rollback；原仓双 hash 不变。

## 已知剩余风险 / 延后事项

- shell 写入仍依赖交付前 `check-diff`，不是 PreToolUse 的覆盖面。
- 旧项目只有在运行迁移/升级后才获得新结构；本里程碑没有静默改写外部仓。
- 未切版、未提交、未推送；Butler 仓状态审计须以 `UNRELEASED` 亮牌通过。
- 未执行 fresh-context 独立复核。

## 引用

- `.ai/milestones/MILE-0009/MILESTONE.md`
- `deliveries/ITER-0075-prd-collection-identity-contract.md`
- `deliveries/ITER-0076-workspace-scope-contract.md`
- `deliveries/ITER-0077-inbox-data-contract.md`
- `deliveries/ITER-0078-butler-inbox-workflow.md`
- `deliveries/ITER-0079-multi-prd-migration.md`
- `deliveries/ITER-0080-prd-split-status.md`
- `deliveries/ITER-0081-prd-update-transaction.md`
- `deliveries/ITER-0082-workspace-scope-gate-e2e.md`
