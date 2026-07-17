# 01_CHANGELOG

> ITER-0051 · MILE-0006 R1 · Codex 兼容地基对象级变更流。

## ADD

- `AGENTS.md`（AC1/AC2）：Butler 仓库的 Codex 原生发现入口与固定冷启动读序。
- `templates/AGENTS.md.template`（AC3）：未来目标项目 Codex 入口模板，规则卡由占位符注入。
- `docs/codex-compatibility.md`（AC4/AC5）：双宿主架构、阶段矩阵、hook 诚实边界与安全边界。
- `scripts/verify-codex-foundation.sh`（AC3/AC8）：零依赖、任意 cwd 可运行的结构回归脚本。
- `deliveries/ITER-0051-codex-compatibility-foundation.{md,html}` 与 `.ai/iterations/ITER-0051/**`：交付和归档。
- `migrations/v2.12.0.md`（AC9）：`[no-op]` + `[restamp]` 迁移配方。

## EDIT

- `README.md`、`Coder/README.md`、`HUMAN_GUIDE.md`（AC5/AC6）：短注册 Codex R1 支持并统一回指架构说明。
- `.ai/project/{frontier,architecture,capabilities,invariants,constraints}.md`：前滚双宿主当前形态、能力、长期边界与后续路线。
- `.ai/{MILESTONE,MILESTONES,ITERATIONS,task-state,02_SESSION_HANDOFF}.md`：关闭 R1/ITER-0051，保持 MILE-0006 active 并指向 R2。
- `VERSION`、`CHANGELOG.md`（AC9）：发布元数据前滚到 v2.12.0。

## DELETE

- 无。
