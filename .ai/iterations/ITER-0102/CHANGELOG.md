<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0102 变更流

> Explore 与 Decision Map 边界合同（MILE-0014 R1） · closed · 2026-08-01

## ADD

- 无

## EDIT

- `Coder/20_Workflow_Lifecycle/lifecycle.md §1.1`、`Coder/50_Extension_Ideation/ideation-engine.md §2–§6` — 固定 opt-in、suggest 零写、Decision Map 所有权与显式 promotion → AC1、AC2、AC4、AC5
- `Coder/00_System_Prompt/workflow-router.md §Explore opt-in boundary`、`workflows/registry.json §ideation` — 保持统一入口与既有 workflow ID，区分用户探索意图和模型建议 → AC1、AC3、AC6
- `.claude/commands/butler/ideation.md`、`plugins/butler/skills/butler-ideation/` — 将双宿主入口收敛为同一探索真源的薄 Adapter，并统一 P1 交接 → AC3、AC4、AC6
- `Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/README.md`、`README.md`、`HUMAN_GUIDE.md` — 清除 explicit-only 与自动 P2 旧口径，统一用户可读说明 → AC1、AC4、AC5、AC6
- `scripts/test-workflow-registry.py §test_ideation_is_opt_in_explore_and_promotes_only_to_p1` — 增加正向合同与旧语义负向断言，并纳入既有完整 CI → AC1、AC2、AC3、AC4、AC5、AC6

## DELETE

- 无
