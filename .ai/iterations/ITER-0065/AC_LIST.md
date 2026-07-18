---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：模型自主 ACK（ITER-0065，2026-07-18）。

# Goal
- 交付机械拒绝假完成的 Goal completion adjudicator。

# In Scope
- active iteration 完成资格、AC/plan/calibration/evidence/review/blocker 聚合、JSON/退出码、八类负向 oracle、规则接线和证据。

# Out of Scope
- 不自动写台账/收口，不做宿主同步，不裁决 milestone complete。

# Acceptance Checklist
- [ ] AC1：CLI 只读解析 current active iteration，输出 schema/version/iteration/verdict/reasons/checks；eligible=0、ineligible=1、输入错误=2。
- [ ] AC2：要求 AC `ack-frozen` 且 VERIFY `[x]` 覆盖 AC_LIST 全部 AC，缺失/失败不得绿。
- [ ] AC3：要求 TECH_PLAN `pass`、task-state 无 open/blocked calibration、VERIFY `Review Verdict: pass` 与 `Completion Blockers: none`。
- [ ] AC4：校验 hot evidence record hash/outcome、Evidence Index ID 集和 passed AC 覆盖，不接受 reported 命令。
- [ ] AC5：eligible 仅代表可执行收口；complete 仍由 closed + 归档/交付/审计派生，host/tasks 不参与。
- [ ] AC6：R1 GFC-001–008 全部负向拒绝，并有一条全绿正向 fixture；工具项目树保持零写入。
- [ ] AC7：VERIFY schema、lifecycle、Goal Contract、rule-card、README 接线；完整矩阵和强审证据通过。

# Verification Method
- unittest fixture、只读前后 hash、真实本仓 ineligible/eligible 路径、完整 CI 与状态审计经 evidence 捕获。

# Open Questions / Risks
- review/blocker 是规范化人工输入，无法自动证明审查者绝对正确；但未知值 fail-closed。
