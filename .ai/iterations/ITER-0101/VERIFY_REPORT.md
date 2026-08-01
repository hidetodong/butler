<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0101

## Verification Summary

- 安装器与 setup 两类根因已修复，双宿主矩阵和最终完整 CI 通过。用户确认后的第三次真实 setup 整体 exit 0，Codex plugin 已安装启用，Claude 与 Pi 的机器级入口均刷新成功。

## AC Status

- [x] AC1 (auto·可靠): 无 uv 的隔离安装测试通过仓库 `.venv` 官方 validator。
- [x] AC2 (auto·可靠): 隔离 fixture 证明所有 PyYAML runtime 不可用时明确 exit 2。
- [x] AC3 (auto·可靠): C.UTF-8 下 Codex exit 7 与 Pi 成功回声均通过双宿主矩阵。
- [x] AC4 (auto·可靠): 最终完整 CI、真实 `scripts/setup.sh` 与 `codex plugin list` 均通过；Butler `3.3.0+codex.20260801061356` installed/enabled。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| full-ci | AC1,AC2,AC3,AC4 | captured | failed | `.ai/iterations/ITER-0101/evidence/full-ci/record.json`（暴露 task-state 缺段） |
| full-ci-final | AC1,AC2,AC3,AC4 | captured | failed | `.ai/iterations/ITER-0101/evidence/full-ci-final/record.json`（暴露当前状态缺 N/A 行） |
| full-ci-final2 | AC1,AC2,AC3,AC4 | reproduced | pass | `.ai/iterations/ITER-0101/evidence/full-ci-final2/record.json` |

## Verification Results

- `verify-dual-host.sh` 通过：覆盖 venv validator、无 runtime 拒绝、UTF-8 Codex 失败回声和 Pi 成功回声。
- 最终固定工具链 `verify-ci.sh` 通过；两次诊断失败证据保留。
- 真实状态：`scripts/setup.sh` 整体 exit 0；Butler plugin `3.3.0+codex.20260801061356` installed/enabled；Claude 命令与 Pi 软链均指向当前仓。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 自动化与真实机器级安装路径均已覆盖。

## References Compliance

- N/A

## Remaining Risks

- 本轮无剩余已知风险；新 Codex 会话才会加载刚安装的 plugin 版本。

## Handoff / Next Step

- ITER-0101 满足收口条件，进入 completion candidate。
