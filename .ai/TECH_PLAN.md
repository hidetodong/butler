> ⚠️ 危险模式：本产物由模型自主 ACK（已过设计自审门），未经用户确认（ITER-0062，2026-07-18）。

# Goal

- 以单一规则真源定义派生 Goal Contract，并用窄接线和结构测试防漂移。

# Files / Modules to Change

- `Coder/20_Workflow_Lifecycle/goal-contract.md`：合同与状态机 SSOT。
- `Coder/README.md`、`lifecycle.md`、`concept-schema.md`、`acceptance-schema.md`、`milestone-schema.md`、`context-persistence.md`：只加职责指针。
- `scripts/test-goal-contract.py`、`scripts/verify-ci.sh`：结构合同测试与完整入口接线。

# Interface / Contract

- 状态集合固定六项；派生优先级固定 `abandoned > blocked > at-risk > completion-candidate > active > complete`，但 closed/complete 作为终态先由 ledger 识别，具体算法正文必须消歧。
- Goal view 不落独立持久文件；字段来自既有真源。

# State / Boundary

- R2 规范状态语义，不执行宿主同步或 P5 裁决。

# Design Decisions

- 选择派生视图，代价是消费者需按规则组合多文件；收益是零双写漂移。R5 可提供统一 reader/CLI 降低消费成本。
- `complete` 不是模型主动选择，而是收口后的派生终态。
- `blocked` 只表示真正无法安全前进；有问题但仍可修是 `at-risk`。

# Execution Steps

- [ ] T1 写 Goal Contract 和状态优先级 → AC1–AC4
- [ ] T2 以窄指针接入既有规则 → AC5
- [ ] T3 增加结构合同测试并接 CI → AC6
- [ ] T4 证据、强审、归档与收口 → AC1–AC6

# Verification Plan

- unittest 检查章节、状态、真源映射、禁止项和所有接线；完整矩阵验证非回归。

# Risks / Open Questions

- 状态优先级若把 complete 放错位置会产生 closed 项仍 at-risk 的矛盾；实现时必须先处理终态，再对非终态应用风险优先级。
