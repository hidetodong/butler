<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0100

## Verification Summary

- R2 已把领域知识拆成 L0 README 路由、L1 五上下文地图、L2 20 项术语查询和 L3 历史审计；普通冷启动不再默认读取完整领域地图。
- 预算基线为 L0=694 bytes / 6 非空行 / 2 指针，L1=3,894 bytes / 55 行 / 11 指针；相对 R1 `domain-model.md` 的 12,395 bytes，L1 缩减约 68.6%，且普通任务只承担已在入口中的 L0。
- context-budget CLI、6 组负向测试、20 项名称迁移、链接、artifact、diff、状态审计和完整 CI 最终通过。
- P5 同上下文简评发现 1 个 Must Fix（仓库内真源 symlink 可逃逸到仓库外），已修复并用 `review-*` evidence 定点复查；最终 Must Fix=0、Should Fix=0。

## AC Status

- [x] AC1 (auto·可靠): L0 唯一标记块为 694 bytes / 6 非空行 / 2 指针，三类触发与禁止递归语义齐全 ✓ `review-context-budget-contract`
- [x] AC2 (auto·可靠): L1 为 3,894 bytes / 55 行 / 11 指针，恰好五上下文，已移除 20 项术语表与冲突案例正文 ✓ `review-context-budget-contract`
- [x] AC3 (auto·可靠): L2 恰好 20 项、六列完整、名称集合与 R1 等值，定义真源存在且不能经 symlink 逃逸仓库根 ✓ `term-migration`, `review-context-budget-tests`
- [x] AC4 (auto·可靠): L3 只保留三处显式审计入口，ITER-0099 历史未被改写；普通路径不要求进入 L3 ✓ `review-context-budget-contract`, `review-markdown-links`
- [x] AC5 (auto·弱): 四条路径、每批 3 份和六字段升级回执已形成静态合同；机器能证明合同存在，不能遥测模型运行时真实读量，语义走读结果通过 ✓ `review-context-budget-contract`
- [x] AC6 (auto·可靠): 五份重复候选文档没有复制上下文表或术语表；README/architecture 只保留职责内导航，链接全绿 ✓ `review-context-budget-contract`, `review-markdown-links`
- [x] AC7 (auto·可靠): context-budget CLI fail-closed，6 组测试覆盖预算、标记、上下文、术语、空列、坏真源、重复、递归和 symlink 逃逸，并已接入 CI ✓ `review-context-budget-tests`, `review-full-ci`
- [x] AC8 (auto·可靠): artifact、Markdown、diff、状态审计和完整 CI 最终通过，运行状态、权限与公开命令未改变 ✓ `final-artifact-contract`, `state-audit-active-final`, `review-diff-check`, `review-full-ci`

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| context-budget-contract | AC1–AC7 | captured | passed | `.ai/iterations/ITER-0100/evidence/context-budget-contract/record.json` |
| context-budget-tests | AC1–AC3, AC5–AC7 | captured | passed | `.ai/iterations/ITER-0100/evidence/context-budget-tests/record.json` |
| term-migration | AC3 | captured | passed | `.ai/iterations/ITER-0100/evidence/term-migration/record.json` |
| markdown-links | AC4, AC6, AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/markdown-links/record.json` |
| artifact-contract | AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/artifact-contract/record.json` |
| diff-check | AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/diff-check/record.json` |
| state-audit-active | AC8 | captured | failed | `.ai/iterations/ITER-0100/evidence/state-audit-active/record.json` |
| state-audit-active-final | AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/state-audit-active-final/record.json` |
| full-ci | AC1–AC8 | captured | failed | `.ai/iterations/ITER-0100/evidence/full-ci/record.json` |
| reproduced-full-ci | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/reproduced-full-ci/record.json` |
| review-context-budget-tests | AC1–AC3, AC5–AC7 | reproduced | passed | `.ai/iterations/ITER-0100/evidence/review-context-budget-tests/record.json` |
| review-context-budget-contract | AC1–AC7 | reproduced | passed | `.ai/iterations/ITER-0100/evidence/review-context-budget-contract/record.json` |
| review-diff-check | AC8 | reproduced | passed | `.ai/iterations/ITER-0100/evidence/review-diff-check/record.json` |
| review-markdown-links | AC4, AC6, AC8 | reproduced | passed | `.ai/iterations/ITER-0100/evidence/review-markdown-links/record.json` |
| review-full-ci | AC1–AC8 | reproduced | passed | `.ai/iterations/ITER-0100/evidence/review-full-ci/record.json` |
| final-artifact-contract | AC8 | captured | passed | `.ai/iterations/ITER-0100/evidence/final-artifact-contract/record.json` |

## Verification Results

- AC1–AC2：预算检查输出 `l0_bytes=694`、`l0_nonempty_lines=6`、`l0_pointers=2`、`l1_bytes=3894`、`l1_lines=55`、`l1_pointers=11`、`contexts=5`，全部低于冻结上限。
- AC3：一次性迁移对账确认 20 个名称集合完全相等；L2 行级检查还验证必填列、单一所有者与仓库内真实路径。P5 修复后，指向仓库外的 symlink 也会 fail-closed。
- AC4–AC5：四条路径分别止于 L0、L2、L1→L2 和 L3；“3 份”按批而非总量，进入下一批前必须公开六字段回执。静态工具只证明合同存在，未宣称提供运行时读量遥测。
- AC6：README、architecture-overview 和 project knowledge/debt 均未出现五上下文表或 20 项术语表副本；Markdown 链接检查通过。
- AC7：6 组单元测试全部通过；完整 CI 已运行相同测试和项目基线检查。
- AC8：`review-full-ci` 通过；`state-audit-active-final` 仅保留预期 `UNRELEASED` 亮牌，无状态漂移。规则功能面没有修改生命周期、权限、状态值、hook 或公开命令。

## TDD Pair Status

- N/A — TECH_PLAN 未声明 TDD cycle。

## Goal Calibration

- CAL-001：`state-audit-active` stale handoff → 同步权威状态后重跑 → resolved，依据 `state-audit-active-final`。
- CAL-002：`full-ci` 无法读取沙箱外 uv 缓存 → 获准环境按相同 argv 重跑 → resolved，依据 `reproduced-full-ci`。
- CAL-003：P5 review 发现定义真源 symlink 可逃逸仓库根 → 回 P4 修复共享校验并补负例 → resolved，依据 `review-context-budget-tests`、`review-context-budget-contract`、`review-full-ci`。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：预算/结构合同、负向测试、术语迁移、链接、artifact、diff、状态审计和完整 CI 均有 passed evidence。
- Workspace Scope：N/A — AC_LIST 无 `prd_refs`。
- Active Profiles：项目配置 `profiles=[]`，未命中 Domain / Stack Profile。
- Tech Plan Alignment：T1–T6 均已兑现；P4 功能改动保持在四份 Coder 文档、context-budget 工具/测试和 CI 接线内，project knowledge 等待既有收口折叠。
- Review：同上下文简评最终 verdict=pass，Must Fix=0、Should Fix=0；风险相关检查以 `review-*` evidence 复现。项目配置 `independent_review=false`，未执行 fresh-context 独立复核。

## References Compliance

- `.ai/references/domain-driven-design-fowler.md` 仅支撑领域边界与统一语言导航；没有复制来源大段正文或引入 DDD 战术模式。
- ITER-0099 的冻结 AC、交付和 evidence 保持只读；R2 只重组读取层级。

## Remaining Risks

- **无运行时读量遥测**：当前保证来自入口触发、静态预算门、可见升级回执与 P5 场景走读，不能证明每个宿主模型在所有会话中都严格执行。若未来发现偏离，应在 R3 评估宿主级读追踪；本轮不为此新增 hook 或遥测系统。
- **token 仍是估算**：机器合同使用 bytes、行数和指针数；不同 tokenizer 的实际 token 会变化，不能把 68.6% bytes 缩减直接等同为精确 token 节省。
- **独立性限制**：`independent_review=false`，本轮没有 fresh-context 独立复核；同上下文简评不冒称独立。

## Handoff / Next Step

- 运行 Goal 完成资格裁决；eligible 后归档 evidence 与五件套，生成双格式交付、更新知识折叠并关闭 MILE-0014 R2。
