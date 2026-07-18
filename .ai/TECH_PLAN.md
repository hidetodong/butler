> ⚠️ 危险模式：本产物由模型自主 ACK（已过设计自审门），未经用户确认（ITER-0061，2026-07-18）。

# Goal

- 为 AC1–AC6 交付现状基线和可复用失败 fixture，不在 R1 修改目标控制算法。

# Files / Modules to Change

- `docs/research/2026-07-18-goal-system-baseline.md`：人读现状审计、层级边界、宿主能力来源等级、缺口和路线输入。
- `docs/research/goal-failure-cases.v1.json`：后续 Goal 裁决器可直接消费的失败 oracle。
- `.ai/*`：ITER-0061 阶段产物、危险模式审计、证据、归档、交付和台账。
- 不修改 `Coder/**`、`templates/**`、`plugins/**`、`.claude/commands/**` 或 `scripts/**` 的产品行为。

# Interface / Contract

- fixture 根对象严格为 `schema_version`、`purpose`、`cases`。
- 每个 case 严格包含 `id`、`category`、`facts`、`invalid_claim`、`expected_disposition`、`blocking_reasons`、`future_route`。
- `expected_disposition` 本轮仅允许 `revise` 或 `blocked`，因为 fixture 专门描述不得完成的负向样本；最终状态机由 R2 决定，本轮不把该枚举提升为公共规则。
- 报告中的 case ID 与 JSON 一一对应；来源等级只用 `documented-butler`、`observed-current-session`、`unknown`。

# State / Boundary

- milestone 仍是版本方向真源、iteration 仍是单轮范围真源、AC 仍是完成定义真源、TECH_PLAN 仍是方案真源、task-state 仍是执行投影、VERIFY/review 仍是证据与裁决真源。
- R1 只记录“目前缺统一 Goal 完成聚合规则”，不决定未来新增文件还是派生视图。
- 宿主 goal/task 只能被记录为适配载体，不能在本轮晋升为项目状态真源。

# Design Decisions

- 采用“一份人读报告 + 一份严格 JSON fixture”，让 R1 的审计结论既可讨论又能被 R5 复用，不写一次性散文后丢失测试价值。
- fixture 只列负向 oracle，不伪造尚未设计的完整 Goal 状态机；正向完成样本由 R2/R5 在合同确定后补。
- 不新增验证脚本：用内联标准库校验捕获 evidence，避免 R1 为临时 schema 建永久执行器；R5 再把 fixture 接入正式裁决器测试。
- 不改 `Coder/README.md` 注册报告，因为它是研究基线、不是运行规则入口；后续被吸收的规则只注册共同内核真源。

# Execution Steps

- [ ] T1 形成目标载体与权威度盘点矩阵 → AC1、AC4
- [ ] T2 固化层级边界、不替代关系和现有/缺失保障 → AC2
- [ ] T3 编写至少 8 个稳定失败 case，并生成严格 JSON fixture → AC3、AC6
- [ ] T4 映射 R2–R6 输入、依赖和 deferred 决策 → AC5
- [ ] T5 运行结构校验、完整矩阵、状态审计和强制审查，修复发现 → AC1–AC6

# Verification Plan

- 用 Python 标准库加载 JSON，严格检查根/条目 keys、ID 唯一、类别集合、数量、 disposition 和报告 ID 对账。
- 用 `rg` 对照 Butler 真源中的 Goal/AC/plan/task-state/verify/dangerous 语义，人工检查矩阵没有把运行投影写成权威真源。
- 用 verification evidence runner 捕获 fixture contract、`git diff --check`、`bash scripts/verify-ci.sh` 和 active state audit。
- P5 以主 agent 完整多维审查逐 AC 反证；当前协作规则未授权子 agent，因此不冒称 fresh-context 独立复核。

# Risks / Open Questions

- 报告可能把当前实现偶然行为误写成长期合同；来源等级和 unknown 栏用于限制外推。
- R1 不实现拦截，故只能证明问题、不能宣称 Goal 已受保护；交付和 handoff 要明确这一残余。
