<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0121

## Verification Summary

10 条 AC 全绿。自动道证据里通过的 record 覆盖 AC1–AC10。`verify-ci.sh` 退出码 0。状态审计在交接文件同步之后 0 DRIFT、2 条 UNRELEASED（未切版，预期内）。

最终 deny 会写 `.ai/.hook-blocks.log`；bypass 成功仍只写 `RUN_LOG.md`。没有 active 迭代时，五份仓根 meta 能过 `phase_gate` 和 `workspace_scope`。hook 树摘要已登记进 `known_hook_tree_digests`。欠账「hook 树一改就必须跟切版绑在一起」已删。

## AC Status

- [x] AC1 (auto·可靠): 最终 deny 追加一行拦截日志；allow 不建该文件；bypass 成功只写 RUN_LOG。
- [x] AC2 (auto·可靠): 本仓 `.gitignore` 含 `.ai/.hook-blocks.log`；hook README 写明目标项目应忽略。
- [x] AC3 (auto·可靠): 超 256KB 丢最旧行；日志路径是目录时 dispatcher 仍 exit 2。
- [x] AC4 (auto·可靠): 无台账时 README 对 phase_gate allow；`docs/README.md` 仍 deny。
- [x] AC5 (auto·可靠): scoped 项目 `current: none` 时 README/CHANGELOG allow，`packages/api/...` 仍 workspace_scope deny。
- [x] AC6 (auto·可靠): `current: ITER-0001` 且缺四件套时 README 仍 phase_gate deny。
- [x] AC7 (auto·可靠): 升级器测试改为 tag 或白名单；历史 checkpoint 仍在白名单。
- [x] AC8 (auto·可靠): 当前摘要 `6005f4d5a4090f39acd5637420df27f0e5cebdda5bc08816e2562dee9f0fe2a4` 已登记；hook pytest 211 passed；升级器 22 passed。
- [x] AC9 (auto·可靠): MILESTONE 2026-09-14 R10 登记 `[sync-hooks]`；debt 该条已删。
- [x] AC10 (auto·可靠): `verify-ci.sh` 退出码 0；审计 0 DRIFT、2 UNRELEASED。

## 人测道小结

- N/A（本轮无 human·待人 档 AC）。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-hooks-v2 | AC1, AC3, AC4, AC6 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-hooks-v2/record.json |
| ac-workspace-v2 | AC5 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-workspace-v2/record.json |
| ac-docs | AC2, AC9 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-docs/record.json |
| ac-digest-v2 | AC7, AC8 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-digest-v2/record.json |
| ac-ci | AC10 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-ci/record.json |
| ac-audit-v2 | AC10 | 可靠 | passed | .ai/iterations/ITER-0121/evidence/ac-audit-v2/record.json |
| ac-hooks | AC1, AC3, AC4, AC6 | 可靠 | launch_error | .ai/iterations/ITER-0121/evidence/ac-hooks/record.json |
| ac-workspace | AC5 | 可靠 | launch_error | .ai/iterations/ITER-0121/evidence/ac-workspace/record.json |
| ac-digest | AC7, AC8 | 可靠 | launch_error | .ai/iterations/ITER-0121/evidence/ac-digest/record.json |
| ac-audit | AC10 | 可靠 | failed | .ai/iterations/ITER-0121/evidence/ac-audit/record.json |

前三次 launch_error 是命令行把 `UV_NO_SYNC=1` 当成了可执行文件。`ac-audit` 第一次失败是 handoff 陈旧，sync 之后重录。

## Verification Results

- hook pytest 211 passed。升级器测试 22 passed。
- 逃生舱只认仓根单段文件名；`docs/README.md` 仍拦。
- 写拦截日志失败（把 `.hook-blocks.log` 建成目录）dispatcher 仍 exit 2。
- CI 全绿。审计需在 handoff sync 之后才 0 DRIFT。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- `bash scripts/verify-ci.sh` 退出码 0。
- `python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0，`[DRIFT]` 0，`[UNRELEASED]` 2。
- P5 简评复跑 hook pytest 与升级器测试，没有 Must Fix。独立复核未跑。

## References Compliance

- N/A

## Remaining Risks

- butler 仓自己不跑 live hook，拦截日志和逃生舱只在 pytest 里为真。
- 已部署项目要等到 v4.0.0 `[sync-hooks]` 才会拿到新 dispatcher。
- `references/raw/` 只读门禁仍没有机器兜底。
- 本轮不切版、不提交。

## Handoff / Next Step

- 实现和验证做完了。要收口说一声。
