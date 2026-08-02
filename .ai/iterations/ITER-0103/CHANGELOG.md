<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0103 变更流

> Decision Map 本地合同与确定性状态机（MILE-0014 R2） · closed · 2026-08-01

## ADD

- `tools/decision-map/engine.py §Public Interface / state reducer / storage` — 新增四动作深 Module、封闭状态机、DAG/Frontier、Claim Lease、幂等 receipt 与本地原子发布 → AC1–AC9
- `tools/decision-map/decision_map.py §CLI Adapter`、`tools/decision-map/README.md §工具合同` — 新增单 JSON CLI 和人机共读合同，不暴露浅层 operation 命令 → AC7–AC10
- `tools/decision-map/tests/ §专项测试` — 新增状态、存储、真实双进程竞争和跨进程 CLI 恢复矩阵 → AC1–AC11
- `CONTEXT.md §Language` — 固定 Explore、Decision Map、Decision、Fog、Dependency、Frontier、Claim Lease 与 Promotion 的领域含义 → AC1–AC10

## EDIT

- `Coder/50_Extension_Ideation/ideation-engine.md §4` — 将结构化 Explore 状态统一委托 Decision Map 工具，并禁止按模型内部大小/清晰度判断自动建 Map → AC10
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md §6`、`Coder/README.md`、`README.md` — 注册驻留工具及其所有权、支持矩阵和非 promotion 边界 → AC9–AC11
- `scripts/test-workflow-registry.py §Explore contract`、`scripts/verify-dual-host.sh §resident tool matrix` — 延续 R1 单入口断言并将专项测试/编译纳入完整 CI → AC10、AC11

## DELETE

- 无
