---
方案状态: pass
方案审查日期: 2026-07-18
方案审查方式: dangerous-self-review
---

> ⚠️ 危险模式：结构化自审 verdict=`pass`（ITER-0065，2026-07-18）。

# Goal
- 用 Python 标准库只读 CLI 组合完成资格事实。

# Files / Modules to Change
- `tools/goal-assurance/goal.py`、`test_goal.py`、README；VERIFY/Goal/lifecycle/rule-card/README；`verify-ci.sh`。

# Interface / Contract
- `python3 tools/goal-assurance/goal.py evaluate --project-root .`；stdout 单一 JSON，exit 0/1/2。
- VERIFY 新增 `# Completion Inputs` 两行：`Review Verdict: pass|must-fix|not-run`、`Completion Blockers: none|present`。

# State / Boundary
- 只裁 active iteration 的 close eligibility；closed complete 继续交给 state auditor。

# Design Decisions
- 复用 verification evidence record schema并自行只读验 hash/集合，避免 shell 命令字符串；不复用整个 state auditor，因为 active 证据尚在 hot。
- checks 全量执行并汇总 reasons，不首错即停，方便一次修齐。

# Plan Admission
- AC Coverage：pass；AC1–AC7 均有 CLI/fixture/规则/证据映射。
- Assumptions：VERIFY/AC/TECH_PLAN/task-state 已按 R2–R4 合同存在；缺失即 fail-closed。
- Alternatives / Trade-offs：否决 hook 自动 close（高风险写状态）；否决只读 Markdown 散文猜 review。
- Failure Modes：reported 假证据、漏 AC、must-fix、open signal、host/tasks 假绿、工具写入；均有独立负向测试。
- Impact / Scope Challenge：只做 iteration eligibility，不抢跑 R6/milestone adjudication。
- Verification Blind Spots：结构化 review input 仍依赖真实审查；危险模式强审和 evidence 提供外部约束。
- Verdict：pass；无已知 Must Fix。

# Execution Steps
- [ ] T1 CLI 与 schema → AC1–AC5
- [ ] T2 正向 + GFC-001–008 + 只读测试 → AC6
- [ ] T3 规则接线与固定 CI → AC7
- [ ] T4 evidence、强审、归档和收口 → AC1–AC7

# Verification Plan
- unittest 至少 10 项；完整矩阵；本仓 completion fixture 由测试生成，不用当前未完成状态伪装 eligible。

# Risks / Open Questions
- R6 前宿主不会自动调用 CLI，但规则已要求 P5 收口前运行。
