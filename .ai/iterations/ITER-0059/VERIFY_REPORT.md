# Verification Summary

ITER-0059 已交付 manifest 驱动的 Butler 升级器：只读 JSON plan、显式项目 apply、人工 split/机器级 global 分域、lock/backup/journal/故障恢复和历史跨版本回归均已实现。

危险模式完整审查首轮发现仓内 plugin cachebuster 对账失败；冷读审查又发现 manifest 前置条件未显式、受保护 action 路径未封口、当前 stamp 可能掩盖内容漂移及事务准备失败状态不完整。全部退回 P4 修复，并由最终 16 项专项、完整唯一入口与定点风险 evidence 复现通过。

# AC Status（道 + 置信档合并标记）

- [x] AC1 (auto·可靠) ✓ `upgrade-tests-final` 校验 26 份 recipe 连续覆盖、唯一 action ID/type/domain/parameters/preconditions，并拒绝断链、未知字段/类型和坏前置条件；执行器无 Markdown 动作解析路径。
- [x] AC2 (auto·可靠) ✓ `upgrade-tests-final` 真跑 CLI JSON plan，比较目标项目、隔离 HOME 与 Butler 输入摘要前后不变；覆盖 stamped/manual-bootstrap/version drift 状态。
- [x] AC3 (auto·可靠) ✓ `review-manifest-current-drift`、`review-upgrade-safety` 复现 protected path、self-target、symlink、marker、hook、split 部分态、当前内容漂移和计划后并发修改均首写前停机。
- [x] AC4 (auto·可靠) ✓ `upgrade-tests-final` 覆盖 lock、before hash、原子写、逐写点故障恢复和事务准备失败；恢复只触及本次已改文件，不调用破坏性 git 回滚。
- [x] AC5 (auto·可靠) ✓ `upgrade-tests-final` 覆盖双入口、hook/settings、add-field、参数化 rename、restamp/no-op 和第二次 already-current；user-managed/入口外内容逐字保留。
- [x] AC6 (auto·可靠) ✓ `upgrade-tests-final` 覆盖 split 未决/defer/now、无戳 bootstrap 和 global-install 未确认；项目 apply 只列 external pending，不修改 HOME。
- [x] AC7 (auto·可靠) ✓ v1.1 单入口跨 v2.0 split 边界、v2.14、v2.15 和 current fixture 均在 `upgrade-tests-final` 中跑 dry-run/apply/rerun；负向路径与恢复同包覆盖。
- [x] AC8 (auto·可靠) ✓ `upgrade-full-matrix-final` 通过 Claude/Codex 工作流与官方 plugin/skill validators、Markdown 检查；两宿主入口都只路由 `tools/butler-upgrade/upgrade.py`。
- [x] AC9 (auto·可靠) ✓ 最终专项、完整矩阵、diff-check、active state audit 及两组 reproduced 风险复核均有 passed record；失败的首次 `state-audit-active` 原样保留。

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| upgrade-tests | AC1–AC7, AC9 | captured | passed（首版 12 项） | `.ai/iterations/ITER-0059/evidence/upgrade-tests/record.json` |
| upgrade-full-matrix | AC7–AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/upgrade-full-matrix/record.json` |
| diff-check | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/diff-check/record.json` |
| state-audit-active | AC9 | captured | failed（诊断保留：源 plugin cachebuster 漂移） | `.ai/iterations/ITER-0059/evidence/state-audit-active/record.json` |
| state-audit-plugin-fix | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/state-audit-plugin-fix/record.json` |
| review-upgrade-safety | AC3–AC6 | reproduced | passed | `.ai/iterations/ITER-0059/evidence/review-upgrade-safety/record.json` |
| upgrade-tests-after-review | AC1–AC7, AC9 | captured | passed（15 项） | `.ai/iterations/ITER-0059/evidence/upgrade-tests-after-review/record.json` |
| review-manifest-current-drift | AC1, AC3 | reproduced | passed | `.ai/iterations/ITER-0059/evidence/review-manifest-current-drift/record.json` |
| upgrade-full-matrix-after-review | AC1, AC3, AC4, AC7–AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/upgrade-full-matrix-after-review/record.json` |
| diff-check-after-review | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/diff-check-after-review/record.json` |
| state-audit-after-review | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/state-audit-after-review/record.json` |
| upgrade-tests-final | AC1–AC7, AC9 | captured | passed（最终 16 项） | `.ai/iterations/ITER-0059/evidence/upgrade-tests-final/record.json` |
| upgrade-full-matrix-final | AC1–AC4, AC7–AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/upgrade-full-matrix-final/record.json` |
| diff-check-final | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/diff-check-final/record.json` |
| state-audit-final | AC9 | captured | passed | `.ai/iterations/ITER-0059/evidence/state-audit-final/record.json` |

# Verification Results

- `upgrade-tests-final`：16/16。包含真实 CLI `--json`、零写入摘要、v1.1→v2.16、split defer/now、global confirmation、manifest 负向、protected path、current drift、TOCTOU、lock、准备失败和写中故障恢复。
- `upgrade-full-matrix-final`：固定 Python 3.12.12 / uv 0.9.28 环境通过 renderer 8、root resolver 7、installer 16、upgrade 16、evidence 11、auditor 12、Markdown 3、CI contract 5、官方 validators、8 skills 和 127 hook tests。
- `review-upgrade-safety`：复现故障恢复、symlink/self-target、计划后修改和 marker/hook/split drift。
- `review-manifest-current-drift`：复现坏 preconditions/protected action、当前版本内容漂移和事务准备失败零目标写入。
- `state-audit-active` 的失败诊断没有覆盖；修正仓内 plugin 版本后，`state-audit-plugin-fix`、`state-audit-after-review`、`state-audit-final` 连续通过并保留 `[UNRELEASED]` 真相。

# Gate Coverage

- 通用质量门：路径/软链/所有权、marker、版本链、有限 schema、零写入 plan、并发/TOCTOU、事务恢复、用户区保护、幂等、宿主路由和固定依赖均有机器测试。
- Active Profiles：无；`.ai/local-constraints.md` 的 dangerous 护栏已执行 P2/P3 自审、checkpoint、RUN_LOG、evidence 和完整审查。
- Tech Plan Alignment：T1–T7 均兑现；未引入自动语义 split、通用 shell action 或项目内 HOME 事务。
- References Compliance：N/A；未使用 `.ai/references/` 外部规格。

# Independent Review

- 未执行 fresh-context 独立复核：本会话的协作约束未明确授权启动子 agent。未冒称独立。
- 主 agent 按危险模式执行全维冷读审查。共发现 3 组 Must Fix：①仓内 plugin cachebuster 破坏版本对账；②manifest 缺显式 preconditions/protected path 封口；③当前 stamp 掩盖内容漂移和事务准备失败状态。均已修复并由 `state-audit-plugin-fix`、`review-manifest-current-drift`、最终完整矩阵复现关闭。
- 最终 Must Fix 0，Should Fix 0。

# Remaining Risks

- `[split] --split now` 仍停在有人语义迁移交接点，这是保护任意用户知识不被粗暴自动拆分的有意边界，不是假绿。
- `global-install` 修改 HOME，必须单独显式确认；项目升级成功可能同时报告 `external_pending`。
- `SIGKILL` 可能留下 lock；程序会阻止后续 plan，恢复需按 journal/restore/backup 人工审阅，不会偷删锁。
- 真实 GitHub Linux/macOS workflow 仍需推送后才会运行；本轮本机 Darwin 完整矩阵可靠，双 runner 运行态沿用 R3 的外部 pending 限制。

# Handoff / Next Step

- 归档证据与四件套、生成 MD/HTML 交付、前滚项目知识并关闭 ITER-0059；危险模式随后自动开启 MILE-0007 R5 / ITER-0060。
