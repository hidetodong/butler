<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0122

## Verification Summary

10 条 AC 全绿。产品驻留 CLI 调用后会在 `.ai/.usage.json` 记下最后时间；未知 id 拒绝写入；写失败 fail-open。工作流薄壳有 `usage.py record workflow:<id>`。CI 退出码 0。

## AC Status

- [x] AC1 (auto·可靠): schema 为 version 1 + entries.last_used；gitignore 含 `.ai/.usage.json`。
- [x] AC2 (auto·可靠): record 写入并覆盖；show 能读出。
- [x] AC3 (auto·可靠): 未知 id 非 0、零写入。
- [x] AC4 (auto·可靠): tools 子目录集合等于产品名单并上跳过名单；registry 12 个工作流 + router 都在 catalog。
- [x] AC5 (auto·可靠): intake / handoff / goal-assurance 三个真实 CLI 调用后对应 tool:* 在文件里。
- [x] AC6 (auto·可靠): 无 `.ai/` 不造文件；目录不可写时 record 退出码 0。
- [x] AC7 (auto·可靠): 12 个工作流薄壳 + router 的 Claude 命令与 Codex skill 都有 `usage.py record` 与对应 id。
- [x] AC8 (auto·可靠): debt 改为采集已落地、报告归 R12。
- [x] AC9 (auto·可靠): usage pytest 8 passed；被打点工具既有测试绿。
- [x] AC10 (auto·可靠): verify-ci.sh 退出码 0；审计 0 DRIFT、2 UNRELEASED。

## 人测道小结

- N/A

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-usage | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9 | 可靠 | passed | .ai/iterations/ITER-0122/evidence/ac-usage/record.json |
| ac-docs | AC1, AC8 | 可靠 | passed | .ai/iterations/ITER-0122/evidence/ac-docs/record.json |
| ac-ci-v3 | AC10 | 可靠 | passed | .ai/iterations/ITER-0122/evidence/ac-ci-v3/record.json |
| ac-audit-v2 | AC10 | 可靠 | passed | .ai/iterations/ITER-0122/evidence/ac-audit-v2/record.json |
| ac-ci | AC10 | 可靠 | failed | .ai/iterations/ITER-0122/evidence/ac-ci/record.json |
| ac-ci-v2 | AC10 | 可靠 | failed | .ai/iterations/ITER-0122/evidence/ac-ci-v2/record.json |

`ac-ci` 是升级器零写入测试被 `.usage.json` 污染；`ac-ci-v2` 是 OVERVIEW 未重算。修完后 `ac-ci-v3` 绿。

## Verification Results

- usage 测试 8 passed。verify-ci 全绿。
- 若干工具测试的树哈希和 workspace-scope check-diff 忽略 `.usage.json`，避免把采集当成业务写入。
- P5 简评没有 Must Fix。独立复核未跑。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- `bash scripts/verify-ci.sh` 退出码 0。
- `python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0。

## References Compliance

- N/A

## Remaining Risks

- 工作流打点靠薄壳自觉，没有宿主进程钩。
- 已部署项目不会自动 gitignore `.ai/.usage.json`，除非自己加一行。
- 90 天报告仍未做（R12）。
- 本轮不切版、不提交。

## Handoff / Next Step

- 实现和验证做完了。要收口说一声。
