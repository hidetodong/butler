<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0101

方案状态: pass
方案审查日期: 2026-08-01
方案审查方式: user-execute-intent

## Design Decisions

- 在 `install-codex-plugin.sh` 集中选择 validator runner：uv → 仓库 venv Python → 可导入 yaml 的系统 Python → 明确失败。
- 不创建或安装依赖；只复用已存在的受控运行时。cachebuster / marketplace / `codex plugin add` 流程保持不变。
- `setup.sh` 用 `${rc}` 明确变量边界，保留子安装器真实退出码。

## Failure Paths

- venv 存在但缺 yaml 时继续检查系统 Python；所有候选不可用时在进入 `codex plugin add` 前失败。
- validator 非零仍原样冒泡，由 setup 报告部分完成并停止 Pi 阶段。

## Test Strategy

- 新增 shell 回归测试覆盖三种 runner 分支与 UTF-8 locale 下的退出码回声；运行 installer / setup 专项和完整 CI，最后真实重装。

## References Compliance

- N/A
