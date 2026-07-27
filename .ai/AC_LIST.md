---
状态: ack-frozen
ACK 日期: 2026-07-26
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0092

> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户确认（ITER-0092，2026-07-26）

## Goal

- 让显式采用 TDD 的迭代只有在 P5 拿出有效 Red→Green 配对后才能通过 Goal 完成资格裁决，同时保持未启用 TDD 的现有流程不变。

## In Scope

- Goal 裁决接线、VERIFY 投影合同、pytest Red/Green 真实 dogfood、正负向测试、规则/说明/CI 同步。

## Out of Scope

- 不证明代码修改时序、Red 失败原因、测试未被改弱；不增新 evidence schema、sidecar、adapter 或 PreToolUse 硬门。

## Acceptance Checklist

- [ ] AC1: `goal.py evaluate` 对未声明 TDD 的 TECH_PLAN 保持 N/A/pass，对声明 TDD 但 Red/Green 配对无效的项目 fail-closed。
- [ ] AC2: Goal 裁决复用 verification-evidence 的唯一配对算法，支持 Butler 工具根与目标 `PROJECT_ROOT` 分离，且保持只读和 stdout 单 JSON 合同。
- [ ] AC3: `VERIFY_REPORT.md` 必须有 TDD 配对状态投影；已声明 cycle 未通过时，Completion Inputs 不得写 blockers=none。
- [ ] AC4: goal-assurance 测试覆盖未启用 N/A、有效配对、缺失/漂移配对和 CLI JSON/只读非回归；verification-evidence 现有行为继续全绿。
- [ ] AC5: ITER-0092 用同一条 pytest argv/cwd 生成 `tdd-goal-gate-red` 失败 record 和 `tdd-goal-gate-green` 通过 record，`check-tdd` 机械确认配对。
- [ ] AC6: Goal/VERIFY/生命周期真源、工具 README 与双宿主浓缩规则对这一 opt-in 收口义务表达一致，未声明时零行为变化。
- [ ] AC7: 专项测试、五件套合同、状态审计、完整 CI 与 `git diff --check` 通过。

## Verification Method

- AC1–AC4：`tools/goal-assurance/test_goal.py` 正负向 fixture 与 CLI 断言。
- AC5：verification evidence 生成的 Red/Green record + `check-tdd`。
- AC6：规则/模板/工具文档对账检查。
- AC7：专项 pytest、artifact/state/handoff 审计、`scripts/verify-ci.sh` 和 diff check。

## External References

- N/A

## Open Questions / Risks

- N/A
