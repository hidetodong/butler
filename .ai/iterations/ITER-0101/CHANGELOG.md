<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0101 变更流

## ADD

- N/A

## EDIT

- `scripts/install-codex-plugin.sh`：保留 uv 首选路径，并在无 uv 时安全复用仓库 `.venv` 或系统 PyYAML runtime；全部不可用时明确失败（AC1、AC2）。
- `scripts/setup.sh`、`scripts/verify-dual-host.sh`：修复 UTF-8 文案后的 shell 变量边界，补齐真实错误码与 Pi 成功回声回归（AC3、AC4）。
- `tools/iteration-intake/intake.py`、`tools/iteration-intake/test_intake.py`：补回新建 task-state 的 Goal Calibration 固定段及结构回归断言（AC4）。

## DELETE

- N/A
