<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0099

## Verification Summary

- hook 树摘要的源侧与目标侧已收敛为同一过滤函数；历史摘要白名单按实际部署文件集重算为 10 项。
- 升级器 22 项测试与仓库完整 CI 均在 ITER-0099 下重新执行并通过；完整 CI 使用钉版 uv 0.9.28 与 Python 3.12.12。
- 六项目只读矩阵确认五个 Butler 管理的 hook 树命中白名单，`claude-skills` 的项目自有 hook 保持拒绝；butler-radar 的 plan 当前为 `already-current` 且无冲突。
- P5 同上下文简评结论为 pass，无 Must Fix；保留历史部署覆盖面与旧部署凭据两项非阻断风险。

## AC Status

- [x] AC1 (auto·可靠): `skip_hook_file()` 是唯一过滤定义，源侧与目标侧收集器共同调用 ✓
- [x] AC2 (auto·可靠): 测试覆盖顶层 pytest 脚手架、缓存、测试目录及子目录同名文件，两个收集器返回同一文件集与摘要 ✓
- [x] AC3 (auto·可靠): 10 项白名单覆盖代表性历史 tag，并补齐 v2.18.0、v3.0.0、v3.1.0 ✓
- [x] AC4 (auto·弱): 本机六项目只读矩阵机械断言五项命中、`claude-skills` 不命中；该结论受本机样本范围限制 ✓
- [x] AC5 (auto·可靠): butler-radar 的只读 plan exit 0，状态 `already-current`，`conflicts` 为空 ✓
- [x] AC6 (auto·可靠): 两类篡改 fixture 均仍抛 `UpgradeError`，拒绝路径零写入 ✓
- [x] AC7 (auto·可靠): `scripts/test-butler-upgrade.py` 共 22 项全部通过 ✓
- [x] AC8 (auto·可靠): `bash scripts/verify-ci.sh` 使用仓库钉版工具链完整通过 ✓

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| upgrader-tests | AC1, AC2, AC3, AC6, AC7 | reproduced | passed | `.ai/iterations/ITER-0099/evidence/upgrader-tests/record.json` |
| full-ci | AC8 | reproduced | passed | `.ai/iterations/ITER-0099/evidence/full-ci/record.json` |
| radar-plan | AC5 | reproduced | passed | `.ai/iterations/ITER-0099/evidence/radar-plan/record.json` |
| deployed-hook-matrix | AC4 | diagnostic | failed | `.ai/iterations/ITER-0099/evidence/deployed-hook-matrix/record.json` |
| deployed-hook-matrix-final | AC4 | reproduced | passed | `.ai/iterations/ITER-0099/evidence/deployed-hook-matrix-final/record.json` |

## Verification Results

- AC1 / AC2 / AC6：`upgrader-tests` 对统一过滤入口、部署文件集相等及真实篡改拒绝做确定性断言；内容修改与项目独有文件两种偏差都不会被白名单放过。
- AC3：同一测试从 Git 历史复算代表性 tag，确认 manifest 的新口径摘要可追溯；当前源与已发布 tag 的摘要一致。
- AC4：第一次矩阵诊断因 Python 3.14 动态导入未登记 `sys.modules` 而失败；修正诊断脚本后，`deployed-hook-matrix-final` 输出五项 `true`、`claude-skills=false` 并通过精确断言。失败 record 保留为纠错轨迹。
- AC5：butler-radar 已在此前独立动作中升级，因此本次 plan 返回 `already-current`，同时 `conflicts=[]`、`changes=[]`；证明当前摘要守门不再产生 hook 树冲突。
- AC7：升级器入口 22 项全部通过，新增测试与既有回归同一命令运行。
- AC8：完整 CI 成功准备 Python 3.12.12，覆盖双宿主、Codex plugin/hooks、artifact、state ledger、升级器、PRD 与 workspace-scope 等仓库检查；Pi TypeScript 仅报告既有依赖不可解析警告，验证脚本按既定契约继续并最终 exit 0。

## TDD Pair Status

- N/A — TECH_PLAN 未声明 TDD cycle。

## Goal Calibration

- CAL-001：旧证据属于冲突编号 ITER-0096 → 不改号复用，移动到临时备份并在 ITER-0099 全量重跑 → resolved。
- CAL-002：本机矩阵诊断首次动态导入失败 → 修正 `sys.modules` 登记后用新 Evidence ID 重跑 → resolved。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：五件套结构、22 项升级器测试、完整 CI 与 evidence 完整性均有机器结果。
- Workspace Scope：N/A — 本迭代没有 `prd_refs`；写入范围限于三处实现文件和 Butler 收口产物，六个目标项目仅只读。
- Active Profiles：项目配置 `profiles=[]`，未命中领域 Profile。
- Tech Plan Alignment：统一过滤定义、历史白名单重算、负向守门和回归入口均按方案落地；没有修改 hook 运行时规则、split 或配置迁移语义。

## References Compliance

- N/A — 无 `.ai/references/` 外部参考资料。

## Remaining Risks

- 本机六个项目不能穷尽其他机器上的历史部署裁剪变体；未来若出现新文件集差异，应考虑部署侧机械文件清单或逐路径历史内容集合。
- v1.0.0 时代没有部署时凭据，“现有九文件与 v1.0.0 逐字一致”是事后比对，不是原始部署记录。
- `claude-skills` 把项目自有 hook 放在 `.claude/hooks/`，当前守门正确拒绝覆盖；兼容项目自有 hook 属独立需求。
- 本次按配置 `independent_review=false` 执行同上下文简评，未做 fresh-context 独立复核。

## Handoff / Next Step

- 运行 Goal 完成资格裁决；若 eligible，则归档 evidence 与五件套，生成双格式交付、更新台账和知识文件夹后提交。
