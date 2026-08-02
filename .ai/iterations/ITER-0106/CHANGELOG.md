<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0106 变更流

## ADD

- `tools/explore-dogfood/` — 新增三个 Decision Module 的内部端到端 harness、单命令零写恢复 inspect、live promotion 拒绝 verifier、README 与 4 项回归测试。
- `docs/explore-dogfood-r5.md` — 固定恢复成本、错误路线、Research 并行效果、Map 维护开销四项观测，并给出外部 tracker `defer` 裁决。
- `.ai/decision-maps/DMAP-0001/`、`.ai/decision-work/DMAP-0001/` — 结构化提问卡片真实 dogfood Map 与两个不可变 Research Attempt；候办仍为 deferred。

## EDIT

- `workflows/{registry,router-examples}.json`、`scripts/{sync-workflow-registry,test-workflow-registry}.py` — 扩充显式 Explore 正例语料、24 个零写 Router 样本与六类快路径契约；对核心样本增加不读取 fixture 预期的 literal-trigger 下界核对。
- `Coder/00_System_Prompt/{workflow-router,logic-protocol}.md`、`Coder/50_Extension_Ideation/ideation-engine.md` — 明确 Router 选择零写、显式正例不是清晰度/体量分类器、轻量 Ideation 不自动持久化。
- `README.md`、`Coder/README.md`、`CONTEXT.md` — 增加 dogfood harness、观测结论和统一领域术语。
- `scripts/verify-dual-host.sh` — 将 dogfood 单测与编译接入完整矩阵。

## DELETE

- N/A
