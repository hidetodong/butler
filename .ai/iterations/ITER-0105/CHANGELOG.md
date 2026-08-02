<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0105 变更流

## ADD

- `tools/decision-promotion/` — 新增 resolved Decision slice 到既有 Milestone route / 新 Iteration P1 的确定性交接引擎、CLI、README 与 18 个回归测试；包含项目根 inode guard 和强杀残留 pending journal。

## EDIT

- `Coder/20_Workflow_Lifecycle/{lifecycle,milestone-schema,iteration-schema,mcv-deployment}.md` — 接入显式 promotion、所有权和冻结后变更分流。
- `Coder/50_Extension_Ideation/ideation-engine.md`、`tools/decision-{map,work}/README.md` — 明确 Explore→Delivery 两个 adapter 与相邻模块边界。
- `README.md`、`Coder/README.md`、`CONTEXT.md` — 增加 Decision Promotion 能力与统一术语。
- `scripts/{verify-dual-host.sh,test-workflow-registry.py}` — 把新模块测试、编译和边界断言接入 CI。

## DELETE

- N/A
