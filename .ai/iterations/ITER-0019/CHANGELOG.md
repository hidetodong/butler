> 收口门槛：执行门禁 hook + 冷启动一致性自检 + 原子收口仪式 · closed · 2026-06-30

## ADD
- `templates/hooks/rules/single_active_iteration.py` — 新 hook 规则：`.ai/ITERATIONS.md` 写入后 active 行 >1 即 deny（effective-text 还原全表）→ AC1 AC2
- `templates/hooks/tests/test_single_active_iteration.py` — 15 例覆盖 Write/Edit/MultiEdit + 兜底分支 → AC4

## EDIT
- `templates/hooks/butler_gate.py` — RULE_MODULES 注册新规则（ledger_status 之后）→ AC3
- `Coder/40_Context_Management/context-persistence.md §冷启动一致性自检` — 新增台账↔产物↔交付 5 不变量 → AC5 AC6
- `Coder/20_Workflow_Lifecycle/iteration-schema.md §5.1 §5.5` — 交叉引用 hook 门禁 + 收口原子仪式五步（末步自检）→ AC7 AC8
- `Coder/20_Workflow_Lifecycle/lifecycle.md §165` — 收口步同步（原子仪式 + ⑤ 自检）→ AC7
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md §5` — hook 注入描述加新规则 → AC8
- `templates/hooks/README.md` — 规则清单 + 运行机制加新规则 → AC8
- `Coder/README.md` — hook 拦截描述加新规则 → AC8

## DELETE
- 无
