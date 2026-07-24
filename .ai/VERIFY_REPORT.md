<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0090

## Verification Summary

- 独立 setup 命令、双宿主入口、registry 分发与 init 复用已完成；安装仍由 `scripts/setup.sh` 单一执行，并在临时 HOME 成功/失败矩阵中通过。

## AC Status

- [x] AC1 (auto·可靠): registry 12 workflows / 49 projections、setup skill/command/agents/软链与生成表全绿 ✓
- [x] AC2 (auto·可靠): 双入口只指向 butler-setup 规则与 setup.sh，合同测试证明不复制安装算法 ✓
- [x] AC3 (auto·可靠): 临时 HOME 覆盖无 Codex、Codex 成功、Codex exit 7 部分完成与 Pi 降级分支 ✓
- [x] AC4 (auto·可靠): init 两入口改为委托 setup 规则，项目部署步骤保持原样且双宿主矩阵通过 ✓
- [x] AC5 (auto·可靠): 规则真源、README/HUMAN_GUIDE 均明确首次 bootstrap 边界与 hook trust ✓
- [x] AC6 (auto·可靠): skill validator、registry 9 项、Codex 12 skills、200 hooks 与完整 CI exit 0 ✓

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| setup-command-matrix | AC1, AC2, AC3, AC4, AC5 | captured | passed | `.ai/iterations/ITER-0090/evidence/setup-command-matrix/record.json` |
| full-ci | AC1, AC3, AC4, AC6 | captured | passed | `.ai/iterations/ITER-0090/evidence/full-ci/record.json` |

## Verification Results

- setup 专项矩阵、skill validator、registry、双宿主/安装器隔离矩阵和完整 CI 全部 exit 0。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁、registry 投影、skill/plugin validator、setup 隔离矩阵、双宿主基础、hooks 与 artifact/state/handoff 检查通过。

## References Compliance

- N/A

## Remaining Risks

- Pi TypeScript 验证仍因本机缺少可选模块/类型定义按既有策略 warning skip；不影响 setup 命令合同与现有强制门禁。

## Handoff / Next Step

- 归档证据和五件套，关闭 ITER-0090；不自动提交、切版或推送。
