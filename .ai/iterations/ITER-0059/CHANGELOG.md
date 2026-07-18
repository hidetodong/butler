# 01_CHANGELOG — ITER-0059

## ADD

- `ITER-0059`：开启 MILE-0007 R4 可执行升级器迭代，新增 P1 CONCEPT 与待 ACK 的 P2 验收清单。→ AC1–AC9
- `.ai/local-constraints.md`、`.ai/RUN_LOG.md`：持久开启危险模式并记录自治北极星、P2 自审与自主 ACK。→ AC9
- `migrations/manifest.json`：登记 v1.0.0→v2.16.0 连续机器迁移链、有限 action/domain/参数和历史 hook tree 摘要。→ AC1、AC3、AC5、AC6
- `tools/butler-upgrade/upgrade.py`、`README.md`：新增 inspect/plan/apply/global-install CLI、零写入计划、项目事务、lock/journal/backup/恢复与稳定状态码。→ AC2–AC6
- `scripts/test-butler-upgrade.py`：新增 12 项历史跨版、幂等、split、manifest 负向、漂移、越界、TOCTOU、锁和故障恢复测试。→ AC1–AC7、AC9

## EDIT

- `.ai/ITERATIONS.md`、`.ai/MILESTONES.md`、`.ai/MILESTONE.md`：绑定 R4 到 ITER-0059 并置为 active。→ AC9
- `.ai/task-state.md`、`.ai/02_SESSION_HANDOFF.md`：切换热状态到 R4 P2 等待 ACK。→ AC9
- `.ai/AC_LIST.md`、`.ai/ITERATIONS.md`：危险模式自审冻结 P2，并登记连续完成 R4/R5 的自治路线图。→ AC1–AC9
- `Coder/20_Workflow_Lifecycle/butler-upgrade.md`、`migration-schema.md`、`mcv-deployment.md`：从模型解释 Markdown 切换到 manifest + 程序真源，明确 split/global/恢复边界。→ AC1、AC6、AC8
- `.claude/commands/butler/upgrade.md`、`plugins/butler/skills/butler-upgrade/SKILL.md`：两宿主入口收薄为同一 CLI 路由；plugin cachebuster 按官方更新流程刷新。→ AC8
- `migrations/v2.6.0.md`、`v2.13.0.md`、`v2.14.0.md`：归一历史非标准 global 标签并补缺失迁移步骤/不需要动作章节。→ AC1
- `scripts/verify-dual-host.sh`：把升级器专项与编译检查接入唯一 CI/local 矩阵。→ AC7、AC9
- `README.md`、`HUMAN_GUIDE.md`、`docs/codex-compatibility.md`：登记先计划后事务 apply、人工 split 与独立 HOME 动作。→ AC8
- `.ai/project/architecture.md`、`capabilities.md`、`invariants.md`、`debt.md`、`frontier.md`：收口折入 R4 当前架构/能力/不变量，收敛旧“协议未跑”欠债并推进 R5。→ AC1–AC9

## DELETE

- 无。
