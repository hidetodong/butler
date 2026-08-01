<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0100

## Verification Summary

- Registry v2、Router / iteration 双宿主投影、事务执行器、安装器与完整 CI 均通过仓内自动化验证。真实 Claude 命令发现和 ChatGPT App `@Butler` 选择行为没有可用宿主会话证据，按弱验证保留，不冒充端到端通过。

## AC Status

- [x] AC1 (auto·可靠): 两个适配器仅引用 Coder 真源；registry 投影检查通过。
- [x] AC2 (auto·可靠): 严格字段、优先级、自路由、未知关系、冲突对称、前置环和投影闭集测试通过。
- [x] AC3 (auto·弱): 根命令 / 命名空间文件与双软链安装矩阵通过；未在真实 Claude Code 中做发现交互。
- [x] AC4 (auto·弱): Router Skill 官方结构校验、隐式元数据和直接 Skill 边界通过；未在真实 ChatGPT App 做 `@Butler` 交互。
- [x] AC5 (auto·可靠): 共享 fixture 覆盖 13 个业务工作流且只声明一个 primary。
- [x] AC6 (auto·可靠): loop / dangerous 显式限定、元数据和负向样例通过。
- [x] AC7 (auto·可靠): 四态枚举与 fixture 闭集通过。
- [x] AC8 (auto·可靠): iteration 注册、两端入口、Skill 元数据与投影通过。
- [x] AC9 (auto·可靠): 结晶分类、未知字段拒绝、plan 零写和不持久化 transcript 测试通过。
- [x] AC10 (auto·可靠): 下一号、里程碑路线、五件套、task-state、同步入口和故障回滚测试通过。
- [x] AC11 (auto·可靠): 真实仓 active probe 返回 `active-exists` 且 writes 为空；fixture 证明不分配第二个 active。
- [x] AC12 (auto·可靠): 同步幂等、官方 validators、`git diff --check` 与固定 Python 3.12.12 / uv 0.9.28 完整 CI 通过。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| router-registry | AC1,AC2,AC5,AC6,AC7,AC8,AC12 | reproduced | pass | `.ai/iterations/ITER-0100/evidence/router-registry/record.json` |
| global-install | AC3,AC12 | reproduced | pass | `.ai/iterations/ITER-0100/evidence/global-install/record.json` |
| iteration-intake | AC9,AC10,AC11 | reproduced | pass | `.ai/iterations/ITER-0100/evidence/iteration-intake/record.json` |
| full-ci | AC1,AC2,AC3,AC4,AC5,AC6,AC7,AC8,AC9,AC10,AC11,AC12 | reproduced | pass | `.ai/iterations/ITER-0100/evidence/full-ci/record.json` |

## Verification Results

- 完整 CI：Claude/Codex 矩阵通过，hook pytest 200 passed，其余 ledger、artifact、Goal、PRD、workspace 与 Pi 回归均通过；Pi TypeScript 依赖不可用的既有检查仍按脚本设计警告后跳过，不属于本迭代 Router 声明。
- 官方 `skill-creator` quick validator：`butler-router`、`butler-iteration` 均 `Skill is valid!`。
- `git diff --check`：通过。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 自动道覆盖 registry / projections / installer / iteration transaction / rollback / full CI；真实 Claude 与 ChatGPT App 发现交互待安装后人测。

## References Compliance

- N/A（无 PRD 引用；共同内核与宿主薄适配边界已对账）。

## Remaining Risks

- Claude 是否同时展示 `/butler` 与 `/butler:*`、ChatGPT App 是否在用户选择 Butler 后稳定隐式注入 Router，仍受真实宿主版本和安装刷新影响；仓内只能给出弱验证。

## Handoff / Next Step

- 实现与仓内验证已完成，可进入收口；安装 / 刷新机器级 Butler 需用户另行显式执行 setup。
