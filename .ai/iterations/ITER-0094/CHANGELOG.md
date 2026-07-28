<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0094 变更流

## ADD

- N/A

## EDIT

- AC1–AC3, AC5, AC6: `tools/project-config/{config.py,README.md,tests/test_config.py}` — 增加 legacy 严格解析、JSON 优先兼容读取、纯迁移计划、部署合同和正负向覆盖。
- AC4, AC6: `tools/butler-upgrade/{upgrade.py,README.md}`、`scripts/test-butler-upgrade.py` — 增加 `migrate_config` 有限 action、当前版漂移检查和事务/恢复测试。
- AC5: `Coder/20_Workflow_Lifecycle/{mcv-deployment,local-constraints-schema,butler-upgrade}.md`、`Coder/README.md`、`templates/rule-card.md` 与 init 双宿主入口 — 切换新部署 JSON 产物与 Markdown 人类职责，保留明确 legacy 边界。

## DELETE

- N/A
