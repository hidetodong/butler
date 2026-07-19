> 里程碑候办区与延迟编号 · active · —

## ADD

- `Coder/20_Workflow_Lifecycle/milestone-schema.md §4.5/§7.6` — 新增未编号候办索引、草稿落盘和开启前退回契约 → AC1–AC6
- `scripts/test-audit-project-state.py` — 新增正式号缺口、畸形 ID、候办缺失/孤立/伪装和双宿主接线回归 → AC7, AC8
- `deliveries/ITER-0068-milestone-backlog-numbering.md`、同名 `.html` — 生成双格式迭代交付 → AC1–AC8

## EDIT

- `Coder/20_Workflow_Lifecycle/milestone-schema.md §2/§6.4–§7.1` — 把 brief 讨论与正式领号拆开，只有明确开工才提升 → AC1–AC6
- `Coder/20_Workflow_Lifecycle/lifecycle.md`、`goal-contract.md`、`mcv-deployment.md`、`Coder/README.md`、`templates/rule-card.md` — 同步候办不占号、不派生 Goal 与历史不回收边界 → AC1–AC6, AC8
- `.claude/commands/butler/milestone.md`、`plugins/butler/skills/butler-milestone/`、`workflows/registry.json`、`docs/workflows.md` — 双宿主增加候办入库、`start` 提升和待办看板路由 → AC1–AC3, AC6, AC8
- `scripts/audit-project-state.py` — 机械核对正式号连续性、候办路径/标记/集合与非软链草稿 → AC3–AC7
- `tools/goal-assurance/goal.py`、`test_goal.py` — 保留并校验失败诊断证据，但只让通过记录计入 AC 覆盖，消除收口契约冲突 → AC8
- `.ai/MILESTONES.md` — 增加空的未编号待办区作为本仓可直接使用的台账入口 → AC1, AC2
- `.ai/project/capabilities.md`、`invariants.md`、`frontier.md` — 折叠命令能力、长期编号不变量与当前形态 → AC1–AC8

## DELETE

- 无
