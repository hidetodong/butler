<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0104 变更流

## ADD

- `tools/decision-work/engine.py`、`decision_work.py`、`README.md`：新增四动作深 Module、不可变 Task/Result sidecar、Research batch、派生状态与显式 R2 absorb 合同。→ AC1–AC12
- `tools/decision-work/tests/`：新增 Interface、存储/真实双进程竞争与 CLI 冷启动恢复矩阵。→ AC1–AC12、AC14
- `Coder/62_Extension_Agents/decision-work.md`：新增一个 host-neutral Decision Work 帮手定义，以四种模式共享一套输入输出和权限边界。→ AC8、AC13

## EDIT

- `Coder/62_Extension_Agents/overview.md`、`Coder/README.md`：名册扩为四帮手，并区分 fresh-context、serial 与 HITL 执行形态。→ AC8、AC13
- `Coder/50_Extension_Ideation/ideation-engine.md`：接入显式 Frontier 选择、逐项 claim、prepare/record/absorb 链，固定“并行求证、单写 Map”。→ AC6–AC8、AC10、AC11、AC13
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`README.md`、`CONTEXT.md`：登记驻留工具并统一 Attempt、Task Packet、Result Envelope、Needs Input、Absorb 词义。→ AC3–AC5、AC13
- `scripts/test-workflow-registry.py`、`scripts/verify-dual-host.sh`：固定 Router + 13 workflows 边界，并将 Decision Work 专项和 compileall 接入唯一完整验证矩阵。→ AC13、AC14

## DELETE

- N/A
