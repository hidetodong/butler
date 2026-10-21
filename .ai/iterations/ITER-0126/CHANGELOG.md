<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0126 变更流

> 写好 v4.0.0 升级配方 · closed · 2026-10-21

## ADD

- `migrations/v4.0.0.md` — 写下从 3.6.0 到 4.0.0 的配方：删知识目录和单文件、搬家 deliveries、卸掉 preference，旧收件箱和仓根 origin 遇到就停 → AC1 / AC2

## EDIT

- `migrations/manifest.json` — 末尾加上 source 3.6.0、target 4.0.0 那一节，八个动作按配方顺序排列 → AC1 / AC2
- `tools/butler-upgrade/upgrade.py` — 队列里有 4.0.0 时，旧收件箱或仓根 origin 在写文件前停下；形状检查整段去掉；`--split` 可带可不带 → AC4 / AC5 / AC6
- `tools/project-config/config.py`、`butler-config.schema.json` — 活字段不再有 preference；读到布尔旧键就从返回值丢掉且不改文件；只有 4.0.0 那次迁移才从磁盘去掉这一键 → AC7
- `tools/project-config/tests/test_config.py`、`test_consumers.py` — 断言跟上卸字段之后的读、写和拒绝 → AC7
- `scripts/test-butler-upgrade.py` — 用临时 butler 根和临时项目锁住配方、清理、旧树停住、形状检查消失和欠债句子 → AC1 / AC3 / AC4 / AC5 / AC6 / AC7 / AC8
- `templates/rule-card.md`、`HUMAN_GUIDE.md`、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`tools/project-config/README.md` — 人读说明不再把 preference 写成还在用的字段 → AC7
- `tools/butler-upgrade/README.md`、`plugins/butler/skills/butler-upgrade/SKILL.md`、`Coder/20_Workflow_Lifecycle/butler-upgrade.md` — apply 不再写必须带 `--split`，并写明旧收件箱或 origin 会先停 → AC6
- `.ai/debt.md` — 去掉「还没有 v4 配方」和「升级不会碰旧收件箱」；人还得自己处理、以及从未在真实项目上跑过，这两句留下 → AC8

## DELETE

- 无
