<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0094

## Verification Summary

- 新部署合同、legacy 解析/回退、JSON 优先冲突报告和 upgrader 双文件事务 action 已完成；迁移后 Markdown 只保留人类可读约束。
- P5 强审修复 1 个 Must Fix：已升级到含 `migrate_config` 的当前版本后若配置被删，upgrader 原本会因“版本已当前”跳过检查；现按已发布 action 检测配置漂移并 fail-closed。

## AC Status

- [x] AC1 (auto·可靠): legacy 三开关、profiles、缺段默认与模糊/冲突负向解析通过 ✓
- [x] AC2 (auto·可靠): JSON 优先、legacy 回退、缺失默认和结构化冲突列表通过 ✓
- [x] AC3 (auto·可靠): 迁移生成规范 JSON，只删除三个机器段并保留其余人类正文 bytes ✓
- [x] AC4 (auto·可靠): `migrate_config` action 的零写 plan、双文件事务、注入失败恢复和当前版漂移检查通过 ✓
- [x] AC5 (auto·可靠): 新部署、rule-card 与 init 入口均改为 JSON 初始化，Markdown 不再双写 ✓
- [x] AC6 (auto·可靠): 匹配 JSON 幂等收窄；冲突/损坏/symlink/模糊 legacy 首写前拒绝 ✓
- [x] AC7 (auto·可靠): project-config 27 项、upgrader 18 项、完整 CI 与 diff check 通过 ✓

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| project-config-migration-tests | AC1–AC3, AC5–AC7 | captured | passed | `.ai/iterations/ITER-0094/evidence/project-config-migration-tests/record.json` |
| upgrader-config-migration-tests | AC4, AC6, AC7 | captured | passed | `.ai/iterations/ITER-0094/evidence/upgrader-config-migration-tests/record.json` |
| full-ci | AC1–AC7 | captured | failed | `.ai/iterations/ITER-0094/evidence/full-ci/record.json` |
| full-ci-reproduced | AC1–AC7 | reproduced | passed | `.ai/iterations/ITER-0094/evidence/full-ci-reproduced/record.json` |
| review-project-config-tests | AC1–AC3, AC5–AC7 | reproduced | passed | `.ai/iterations/ITER-0094/evidence/review-project-config-tests/record.json` |
| review-upgrader-config-tests | AC4, AC6, AC7 | reproduced | passed | `.ai/iterations/ITER-0094/evidence/review-upgrader-config-tests/record.json` |
| diff-check | AC7 | captured | passed | `.ai/iterations/ITER-0094/evidence/diff-check/record.json` |
| final-full-ci | AC1–AC7 | captured | failed | `.ai/iterations/ITER-0094/evidence/final-full-ci/record.json` |
| final-full-ci-reproduced | AC1–AC7 | reproduced | passed | `.ai/iterations/ITER-0094/evidence/final-full-ci-reproduced/record.json` |

## Verification Results

- project-config 最终 27/27、upgrader 18/18；覆盖 legacy 两种 review 字段冲突、未知/重复值、正文保真、事务应用/恢复和 current-version drift。
- 两次沙箱内完整 CI 仅因用户级 `uv` 缓存权限失败，失败 record 保留；相同命令在宿主权限下两次 reproduced 通过。
- 工作流 registry、Markdown 链接、artifact/state 合同和 `git diff --check` 通过。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用门禁：两组专项、完整 CI（含 200 个 hook 测试与全部行为组）、registry/链接/artifact/state 和 diff check 通过。
- 迁移安全：plan 零写、before hash、backup/restore/journal、symlink/冲突/模糊输入 fail-closed 均有负向覆盖。
- Domain Profile：N/A（本迭代未激活领域 profile）。

## References Compliance

- N/A

## Remaining Risks

- `migrate_config` action 能力已实现并验证，但真实版本链 action 按边界留给 R3 与发布接线一起登记；R2 不冒称 3.2.0 老项目已可自动触发该 action。
- 项目 `independent_review` 为 off，未执行 fresh-context 独立复核；本结论来自同上下文危险模式完整强审。

## Handoff / Next Step

- 运行 Goal 完成资格裁决；eligible 后收口 ITER-0094，并继续 MILE-0013 R3。
