<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0105

## Verification Summary

- ITER-0105 已实现 resolved Decision slice 到既有 Milestone route 或新 Iteration P1 的确定性交接。最终机器验证覆盖 source closure、两个 adapter、fail-closed、幂等、stale/并发、rollback/强杀检测、生命周期接线与完整仓库回归。
- P5 同上下文审查首轮发现 2 个 Must Fix；经项目根 inode guard、pending journal 和定点复查后均关闭。当前 Must Fix 0、Should Fix 0，AC1–AC10 全部满足。

## AC Status

- [x] AC1 (auto·可靠): source roots/传递闭包、partial Map、empty evidence 与未 resolved 拒绝均由 `decision-promotion-tests-r2` 通过。
- [x] AC2 (auto·可靠): 严格 request、两个封闭 target、四动作及零写门由新模块测试与 `full-ci-r3` 通过。
- [x] AC3 (auto·可靠): route-reference 只写 receipt、路线/Map/Iteration hash 不变且 inspect 可反查；由 r2 定点复查复现。
- [x] AC4 (auto·可靠): milestone/standalone iteration-start 均复用真实 intake，从 P1 开启并注入 Source Reference；由 r2 定点复查复现。
- [x] AC5 (auto·可靠): 坏 ID/字段、symlink、未 resolved、错误 Milestone/route/active 状态全部 fail-closed。
- [x] AC6 (auto·可靠): receipt canonical、ID+digest 幂等、ID 冲突和 source tampering 检测通过。
- [x] AC7 (auto·可靠): source/target digest、统一 stale、跨进程单提交、项目根 guard 与 `.ai` 锁连续性通过。
- [x] AC8 (auto·可靠): atomic receipt、intake rollback、pending crash journal 与 incomplete detection 通过；失败注入无半写。
- [x] AC9 (auto·可靠): Map close 正交、P2 amend/escalate 和三方所有权已写入生命周期真源并由 contract test 通过。
- [x] AC10 (auto·可靠): README、部署、CI、R2/R3/intake 回归及完整 `verify-ci.sh` 均通过。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| decision-promotion-tests | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0105/evidence/decision-promotion-tests/record.json` |
| workflow-contract | AC9, AC10 | captured | passed | `.ai/iterations/ITER-0105/evidence/workflow-contract/record.json` |
| markdown-links | AC9, AC10 | captured | passed | `.ai/iterations/ITER-0105/evidence/markdown-links/record.json` |
| review-promotion-risk | AC3, AC4, AC6–AC8 | reproduced | passed | `.ai/iterations/ITER-0105/evidence/review-promotion-risk/record.json` |
| full-ci | AC1–AC10 | captured | passed | `.ai/iterations/ITER-0105/evidence/full-ci/record.json` |
| decision-promotion-tests-r2 | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0105/evidence/decision-promotion-tests-r2/record.json` |
| review-promotion-risk-r2 | AC3, AC4, AC6–AC8 | reproduced | passed | `.ai/iterations/ITER-0105/evidence/review-promotion-risk-r2/record.json` |
| full-ci-r2 | AC1–AC10 | captured | failed | `.ai/iterations/ITER-0105/evidence/full-ci-r2/record.json` |
| full-ci-r3 | AC1–AC10 | captured | passed | `.ai/iterations/ITER-0105/evidence/full-ci-r3/record.json` |

## Verification Results

- AC1–AC2：18 个模块测试验证 closure digest 只覆盖 roots/依赖闭包、开放无关项不阻塞；严格 JSON、未知字段/target、plan→apply 和零写动作均有负例。
- AC3–AC4：真实临时 Butler 项目分别验证 route-reference 与 iteration-start；后者使用 iteration-intake 的台账、路线绑定、活产物和 rollback，不复制实现。
- AC5–AC6：坏 Map/Decision/route/ID、重复 roots、symlink、receipt tampering 与 promotion ID 冲突均返回稳定机器错误；相同请求重放只有一份 receipt。
- AC7–AC8：跨进程竞争只提交一个 receipt；项目根 inode guard 在 `.ai` rollback 域之外维持锁连续性；pending journal 让 callback 前强杀窗口可检测，sync/receipt 失败均无业务半写。
- AC9–AC10：workflow contract、Markdown links 与 pinned `uv 0.9.28 / Python 3.12.12` 完整 CI 通过。`full-ci-r2` 的唯一失败是修复后仍误留 open calibration 投影；纠正运行态后同一完整入口 `full-ci-r3` 通过。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- CAL-001：review-finding（`.ai` rollback 期间锁 inode 连续性）→ P4 → resolved；依据 `review-promotion-risk-r2` 的 project-root guard 定点复查。
- CAL-002：review-finding（callback 前强杀无可检测意图）→ P4 → resolved；依据 pending journal/incomplete detection 定点复查。
- CAL-003：verification-failure（`full-ci-r2` 发现已解决 finding 仍投影为 open）→ P5 proof correction → resolved；依据运行态纠正与 `full-ci-r3` passed。
- 当前无未闭合运行时信号。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：严格边界校验、状态一致性、非阻塞锁、原子发布、回滚、并发、symlink 与篡改检查均有机器证据。
- Workspace Scope：N/A；本迭代无 `prd_refs`。
- Active Profiles：N/A；项目配置 profiles 为空。
- Tech Plan Alignment：T1–T6 全部完成；唯一计划内盲点“SIGKILL 只能检测”已由 pending journal 落实，未扩张为自动恢复。
- P5 Review：同上下文简评，配置 `independent_review=false`；首轮 Must Fix 2/Should Fix 0，定点复查后 Must Fix 0/Should Fix 0。未执行独立复核，也未冒称独立。

## References Compliance

- 外部参考资料 N/A。内部实现遵守 Decision Map、iteration-intake、Milestone/Iteration schema 的既有所有权合同。

## Remaining Risks

- 进程被强杀后可能保留 pending journal，需要人工检查并按既有恢复/废弃流程处置；系统会 fail-closed，不自动猜测或补写。
- 同一 slice 可被用户显式引用到多个 route，这是已确认的复用语义，不是唯一归属保证。

## Handoff / Next Step

- Goal Assurance 通过后归档 evidence 与五件套、生成 ITER-0105 delivery、关闭 MILE-0014 R4；R5 保持 planned，不自动开启。
