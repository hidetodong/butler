<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0124 变更流

> preference 实验、evidence 降维与 loop 处置 · closed · 2026-10-20

## ADD

- `tools/preference-experiment/` — 只回答仓库里有没有重排函数。没有就打出排序没变，不写仓库外的偏好目录 → AC1 / AC2

## EDIT

- `workflows/registry.json`、`scripts/sync-workflow-registry.py`、`docs/workflows.md`、`workflows/router-examples.json` — 去掉 preference 这条业务工作流和路由示例，校验仍通过，实验工具留下 → AC3
- `Coder/README.md`、`HUMAN_GUIDE.md`、`README.md`、`Coder/00_System_Prompt/logic-protocol.md`、`templates/rule-card.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`scripts/setup.sh`、`scripts/preference-init.sh`、`templates/preference/`、`tools/project-config/tests/test_consumers.py` — 机器入口改为已退役；项目配置里的 preference 布尔保留，不再启动采集 → AC3
- `HUMAN_GUIDE.md`、`Coder/README.md`、`docs/codex-compatibility.md` — 业务工作流个数从 12 改成 11，和 registry 条数一致 → AC4
- `scripts/test-workflow-registry.py`、`scripts/test-goal-host-wiring.py`、`tools/codex-validators/test_vendored_validators.py` — 个数断言跟着 registry 走 → AC4
- `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` — 冻结段写成最终处置是保持冻结；命令和引擎正文不改 → AC5
- `tools/verification-evidence/test_evidence.py` — 锁住五个子命令，以及谁可以读 `record.json` → AC7
- `tools/usage/usage.py`、`scripts/verify-ci.sh`、`.ai/OVERVIEW.md` — 实验工具进产品名单、持续集成和全貌 → AC9

## DELETE

- `Coder/70_Extension_Preference/`、`.claude/commands/butler/preference.md`、`plugins/butler/skills/butler-preference/`、`.agents/skills/butler-preference` — preference 机器入口的规则、命令、skill 和软链 → AC3
- `.ai/debt.md` — 删掉「随 MILE-0016 R13 对 loop 做最终处置」 → AC6
