> handoff 确定性可信闭环 · active · —

## ADD
- `tools/handoff/` — 新增状态快照、固定渲染、receipt、sync/check 与故障回滚测试 → AC1–AC5, AC7–AC8
- `templates/hooks/rules/handoff_freshness.py` — 权威状态写后注入新鲜度提醒 → AC6
- `templates/hooks/tests/test_handoff_freshness.py` — 覆盖提醒目标与静默边界 → AC6

## EDIT
- `Coder/40_Context_Management/handoff-spec.md §1/§5` — handoff 改为工具生成的派生视图并定义 check/sync 消费协议 → AC2, AC5
- `Coder/40_Context_Management/context-persistence.md §6` — 冷启动先检新鲜度，stale 先重建 → AC5
- `Coder/20_Workflow_Lifecycle/maintenance-boundaries.md §1/§2` — 固定 handoff 更新时机，禁止自由手写 → AC5
- `templates/hooks/butler_advisor.py`、`templates/hooks/README.md` — 注册 freshness advisory → AC6
- `scripts/audit-project-state.py`、`scripts/test-audit-project-state.py` — receipt 存在时机械核 handoff，新旧项目兼容 → AC7, AC9
- `scripts/verify-ci.sh`、`Coder/README.md`、`HUMAN_GUIDE.md`、`README.md`、`templates/rule-card.md` — 接入完整 CI、规则导航与使用入口 → AC9

## DELETE
- 无

