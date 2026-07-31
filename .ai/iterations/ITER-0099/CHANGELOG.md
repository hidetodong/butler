<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# 变更流

## ADD

- `tools/butler-upgrade/upgrade.py`：新增非部署 hook 文件集合与统一过滤函数，供源侧、目标侧共同调用（AC1、AC2）。
- `scripts/test-butler-upgrade.py`：新增过滤口径一致性、历史摘要可复算和篡改拒绝回归测试（AC2、AC3、AC6、AC7）。

## EDIT

- `migrations/manifest.json`：按统一部署文件口径重算历史 hook 树摘要白名单（AC3）。

## DELETE

- N/A
