<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0123

## Verification Summary

9 条验收都有通过证据。90 天报告能按最后调用时间把入口分成 A/B/C/D。整仓持续集成退出码 0。审计退出码 0，没有 DRIFT，有 2 条未发布亮牌。

## AC Status

- [x] AC1 (auto·可靠): 默认 90 天，stdout 是带四个档位的 JSON。
- [x] AC2 (auto·可靠): 窗口内为 A，更早为 B，名单里没有记录为 C，名单外为 D。
- [x] AC3 (auto·可靠): `--since 7d` 改边界；`0d`、`1h`、`90` 非 0 退出，stdout 不是成功报告。
- [x] AC4 (auto·可靠): 缺文件或坏文件退出码 0，名单全在 C，D 为空，坏文件字节不变。
- [x] AC5 (auto·可靠): 报告覆盖封闭名单的每一个 id，不多出名单内的活入口。
- [x] AC6 (auto·可靠): `PRODUCT_TOOLS` 含 `usage-report`，目录对账仍绿。
- [x] AC7 (auto·可靠): `debt.md` 没有「还没有 90 天报告和 A/B/C/D 分档」这句。
- [x] AC8 (auto·可靠): usage-report 测试 6 passed；usage 测试 8 passed。
- [x] AC9 (auto·可靠): `bash scripts/verify-ci.sh` 退出码 0。审计 `--allow-unreleased` 退出码 0，没有 DRIFT。

## 人测道小结

- N/A

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| ac-report | AC1, AC2, AC3, AC4, AC5, AC8 | reproduced | passed | .ai/iterations/ITER-0123/evidence/ac-report/record.json |
| ac-usage | AC6, AC8 | reproduced | passed | .ai/iterations/ITER-0123/evidence/ac-usage/record.json |
| ac-debt | AC7 | reproduced | passed | .ai/iterations/ITER-0123/evidence/ac-debt/record.json |
| ac-ci | AC9 | reproduced | failed | .ai/iterations/ITER-0123/evidence/ac-ci/record.json |
| ac-ci-v2 | AC9 | reproduced | failed | .ai/iterations/ITER-0123/evidence/ac-ci-v2/record.json |
| ac-ci-v3 | AC9 | reproduced | passed | .ai/iterations/ITER-0123/evidence/ac-ci-v3/record.json |
| ac-audit | AC9 | reproduced | passed | .ai/iterations/ITER-0123/evidence/ac-audit/record.json |

`ac-ci` 停在本机没有 Codex plugin-creator。脚本按仓库锁定的提交补上之后，`ac-ci-v2` 停在任务状态里还有一条未闭合信号，活文件测试要求那句话还在。信号改成已解决后，`ac-ci-v3` 通过。

## Verification Results

- 报告测试和采集测试是这次重新执行的。
- 持续集成第三次退出码 0。审计退出码 0，2 条 UNRELEASED，0 条 DRIFT。
- P5 简评没有 Must Fix。独立复核未开（项目配置 `independent_review` 为 false）。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- CAL-001：`external-blocker` → 补齐本机 plugin-creator 后回 P5 重跑 → resolved（依据：evidence `ac-ci-v3`）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：`bash scripts/verify-ci.sh` 退出码 0。`python3 scripts/audit-project-state.py --project-root . --allow-unreleased` 退出码 0。
- Workspace Scope：N/A（本轮 AC 没有 `prd_refs`）。
- Tech Plan Alignment：D1 到 D5 都落在 `tools/usage-report/`。只读报告、坏文件不改字节、只按最后调用时间分档、复用封闭名单、不声明 TDD。

## References Compliance

- N/A

## Remaining Risks

- 工作流大多没有进程钩，C 档会偏多。C 不是「已经证实没人用」。
- 真实会话里有没有人看这份报告，本轮不证明。
- 给人读的三份文档里，工作流个数仍然靠手改。
- 本轮不切版、不提交。
- 本机 `~/.codex/skills/.system/plugin-creator/scripts/` 放的是 openai/codex 提交 `5c0e582` 的四个脚本。当前 Codex 技能在另一条路径，没有 cachebuster 和 marketplace 这两个旧脚本。

## Handoff / Next Step

- 证据归档并收口 ITER-0123。
- MILE-0016 下一段是 R13，还没开工。
