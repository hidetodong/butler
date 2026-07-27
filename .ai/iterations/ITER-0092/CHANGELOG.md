<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# 变更流

## ADD
- AC3: `tools/artifact-pipeline/artifacts.v1.json` / `templates/VERIFY_REPORT.md` — VERIFY 新增固定 `TDD Pair Status` 投影段。
- AC1, AC2, AC4: `tools/goal-assurance/test_goal.py` — 新增 TDD 未启用、有效配对和漂移拒绝测试。

## EDIT
- AC1, AC2: `tools/goal-assurance/goal.py` — 复用 verification-evidence 配对检查并投影 `tdd_pairs_valid`。
- AC3, AC6: `Coder/20_Workflow_Lifecycle/{lifecycle,verify-schema,goal-contract}.md` 与 `templates/rule-card.md` — 接入 P5/Goal TDD 收口义务。
- AC2, AC6: `tools/goal-assurance/README.md` — 记录 opt-in TDD 裁决语义。

## DELETE
- N/A
