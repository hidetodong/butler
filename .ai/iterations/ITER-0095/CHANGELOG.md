<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0095 变更流

## ADD

- AC4: `.ai/butler.config.json` — 以原有真实值完成 Butler 仓自身配置迁移，危险模式继续为 true。
- AC1–AC5, AC8: `tools/project-config/tests/test_consumers.py` — 新增活消费端统一读写、进度版本来源与本仓迁移状态的结构回归。
- AC6: `migrations/v3.3.0.md` — 增加 3.2.0→3.3.0 项目配置迁移配方。

## EDIT

- AC1–AC3, AC5: `Coder/00_System_Prompt/logic-protocol.md`、危险/复核/偏好引擎、Claude commands、Codex skills、`templates/rule-card.md` — 统一 `resolve` 读取、JSON-only `set` 回写、source/conflict 与 fail-closed 语义。
- AC3, AC5: `README.md`、`HUMAN_GUIDE.md`、`Coder/README.md`、project-config README — 更新项目配置、版本来源、兼容迁移和人类操作说明。
- AC4: `.ai/local-constraints.md` — 删除 Active Profiles 与机器开关段，只保留人类可读项目约束。
- AC5: `workflows/registry.json` — 把 `/butler:preference project on|off` 纳入元数据真源并保持投影一致。
- AC6, AC8: `migrations/manifest.json`、`scripts/test-butler-upgrade.py`、`scripts/verify-ci.sh` — 登记真实 `migrate_config` action，并把配置/升级专项纳入完整 CI。
- AC7: `VERSION`、插件 manifest、README badge、根 `CHANGELOG.md` — 对齐 v3.3.0 本地 UNRELEASED 发布候选元数据。

## DELETE

- AC4: `.ai/local-constraints.md` 中 legacy Active Profiles、Butler 功能开关与 Review Policy 机器段（本仓无 Review Policy 段）。
