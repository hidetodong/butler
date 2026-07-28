<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0093 变更流

## ADD

- AC1–AC6: `tools/project-config/config.py` — 新增项目级 Butler 配置的严格读取、默认探测、原子初始化和受限字段更新内核。
- AC1: `tools/project-config/butler-config.schema.json` — 固定 schema v1 的五字段扁平 JSON 合同。
- AC1–AC7: `tools/project-config/tests/test_config.py` — 覆盖正负向校验、路径安全、冲突写入和发布前故障恢复。
- AC1–AC6: `tools/project-config/README.md` — 登记配置格式、CLI、退出码和能力边界。

## EDIT

- N/A

## DELETE

- N/A
