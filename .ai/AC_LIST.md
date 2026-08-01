---
状态: ack-frozen
ACK 日期: 2026-08-01
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0101

## Goal

- 让无全局 uv / PyYAML 的开发机也能复用仓库锁定环境校验并刷新 Butler plugin，同时保留真实错误码。

## In Scope

- 插件 validator Python 运行时选择、setup 错误码回声、相应回归测试与真实重装。

## Out of Scope

- 不跳过官方 validator；不自动安装全局依赖；不修改 Router 业务逻辑或基础版本号。

## Acceptance Checklist

- [x] AC1: 有 uv 时继续使用 `uv run --with pyyaml`；无 uv 时优先使用仓库 `.venv/bin/python`，仅在可导入 yaml 时调用 validator。
- [x] AC2: 仓库 venv 与系统 Python 都不能导入 yaml 时，安装器给出明确错误并失败，不能跳过 validator。
- [x] AC3: Codex installer 失败时 setup 准确回显其退出码，不再因 UTF-8 后缀触发未绑定变量。
- [x] AC4: 专项测试、完整 CI 和真实 `scripts/setup.sh` 均通过；`codex plugin list` 显示新版 Butler 已安装启用。

## Verification Method

- AC1–AC3: 隔离 PATH / fake runtime 回归和 shell 静态检查。
- AC4: 完整 CI、真实 setup 输出与 plugin list 版本对账。

## External References

- N/A

## Open Questions / Risks

- N/A
