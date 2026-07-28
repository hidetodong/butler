<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0095

## Verification Summary

- 自动道达到可靠档：project-config 32 项、upgrader 19 项、完整唯一 CI、当前仓 resolve、版本一致性与 diff check 均通过。
- P5 危险模式完整强审发现 1 个 Must Fix：直接修改 `preference.md` frontmatter 绕过 workflow registry 真源；已改为更新 registry 并重生成，随后完整 CI 复现通过。最终 Must Fix 0、Should Fix 0。

## AC Status

- [x] AC1 (auto·可靠): 冷启动、危险、复核、偏好、profiles 的活入口均由 consumer matrix 锁定 project-config `resolve`；错误语义 fail-closed。
- [x] AC2 (auto·可靠): 三个项目布尔开关只经 `set` 写 JSON，legacy/missing 明确先 upgrade/init，旧 Markdown 写法被负向扫描禁止。
- [x] AC3 (auto·可靠): Claude/Codex progress 复用一次 resolve，展示 source/conflicts/switches/profiles；版本改读双入口 stamp 或 VERSION。
- [x] AC4 (auto·可靠): 本仓 resolve 返回 `dangerous=true`、`independent_review=false`、`preference=true`、`profiles=[]`、source=config、冲突为空；Markdown 人类约束保留，机器段清除。
- [x] AC5 (auto·可靠): 活规则、模板、命令、skills、README/HUMAN_GUIDE 与 workflow registry 已统一；Markdown links 与 12 skills/plugin 验证通过。
- [x] AC6 (auto·可靠): v3.3.0 manifest 顺序为 global_install → migrate_config → regen_entrypoints → restamp；真实 3.2→3.3 迁移、事务/冲突/current drift 回归 19 项通过。
- [x] AC7 (auto·可靠): VERSION、插件、README badge、根 CHANGELOG、migration recipe 对齐 3.3.0；审计明确保持 UNRELEASED，交付路径已固定。
- [x] AC8 (auto·可靠): 专项、完整 CI、artifact/registry/双宿主矩阵和 diff check 全绿；强审最终无 finding，独立复核关闭事实已披露。

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| project-config-tests | AC1,AC2,AC3,AC4,AC5,AC8 | captured | failed | `.ai/iterations/ITER-0095/evidence/project-config-tests/record.json` |
| reproduced-project-config-tests | AC1,AC2,AC3,AC4,AC5,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/reproduced-project-config-tests/record.json` |
| upgrader-tests | AC4,AC6,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/upgrader-tests/record.json` |
| full-ci | AC1,AC2,AC3,AC4,AC5,AC6,AC8 | captured | failed | `.ai/iterations/ITER-0095/evidence/full-ci/record.json` |
| reproduced-full-ci | AC1,AC2,AC3,AC4,AC5,AC6,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/reproduced-full-ci/record.json` |
| review-project-config-tests | AC1,AC2,AC3,AC4,AC5,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/review-project-config-tests/record.json` |
| review-full-ci | AC1,AC2,AC3,AC4,AC5,AC6,AC7,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/review-full-ci/record.json` |
| diff-check | AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/diff-check/record.json` |
| state-audit-active | AC7,AC8 | captured | failed | `.ai/iterations/ITER-0095/evidence/state-audit-active/record.json` |
| state-audit-active-final | AC7,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/state-audit-active-final/record.json` |
| state-audit-closed | AC7,AC8 | reproduced | passed | `.ai/iterations/ITER-0095/evidence/state-audit-closed/record.json` |

## Verification Results

- 首条 project-config evidence 因沙箱禁止访问用户级 uv cache 而失败；同命令在获准宿主环境复跑 32/32，通过记录覆盖功能结论，失败记录保留环境事实。
- 完整 CI 首轮在 workflow registry check 发现 `preference.md` frontmatter drift；修复单一真源后 `reproduced-full-ci` 与 `review-full-ci` 均 exit 0。
- 3.3.0 元数据对齐后 upgrader 19/19，实际从 3.2.0 计划包含 `migrate_config`，迁移后配置缺失会触发 current-version drift。
- active state audit 的唯一失败为 handoff 在 P5 文档继续变化后陈旧；release 四载体均对齐且正确标为 UNRELEASED。最终 handoff sync 后 active 与 closed 两次审计均为绿色。
- 最终 active state audit 在同步 handoff/state index 后通过；仅保留预期的 UNRELEASED 亮牌。

## TDD Pair Status

- N/A（TECH_PLAN 未声明 TDD cycle）。

## Goal Calibration

- 当前无未闭合运行时信号（N/A）。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用门禁：唯一完整 CI exit 0；200 个 hooks、双宿主 setup/entrypoint、Pi 扩展、workflow registry、Markdown links、artifact/state/Goal 与各行为组通过。
- Active Profiles：project-config `profiles=[]`，无领域 profile。
- Tech Plan Alignment：resolve-only read、JSON-only set、consumer matrix、dogfood 保值迁移、未来 manifest 先登记再对齐版本元数据均已兑现。
- 配置安全：坏 JSON/legacy 歧义/symlink/冲突/事务故障/current drift 均有负向测试。

## References Compliance

- N/A（本迭代无外部参考资料）。

## Remaining Risks

- v3.3.0 目前只是本地 UNRELEASED 候选：没有 commit、tag 或 push，本报告不把它称为已发布。
- Pi 的可选 tsc 检查仍因本机缺宿主模块/Node types 只给警告；既有 Pi 契约验证完成，非本轮新增回归。
- 项目 `independent_review=false`，未执行 fresh-context 独立复核；本结论来自同上下文危险模式完整强审，未冒称独立。

## Handoff / Next Step

- Goal adjudicator eligible 后执行迭代/里程碑收口、双格式交付、知识折叠与关闭态完整验证。
