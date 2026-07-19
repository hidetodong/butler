# Verification Summary

- ITER-0068 已把里程碑讨论稿与正式编号拆层：暂缓内容可恢复但不占号，开工才领号。
- 状态审计 18 项、workflow registry 对账、Markdown 链接、147 hooks 与完整 CI 通过。
- 强审与收口裁决共发现 3 个 Must Fix，均已修复并重跑证据；当前无完成阻塞。

# AC Status

- [x] AC1 (auto·可靠): 录入/讨论与正式开启已拆开 ✓
- [x] AC2 (auto·可靠): 台账待办索引与独立草稿一一对账 ✓
- [x] AC3 (auto·可靠): `start <候办键>` 提升后才按正式表领号 ✓
- [x] AC4 (auto·可靠): 只有最新且零历史引用的误开项可退回 ✓
- [x] AC5 (auto·可靠): 已绑迭代/归档/交付的号永不回收 ✓
- [x] AC6 (auto·可靠): 候办不参与 current、Goal、迭代归属或收口 ✓
- [x] AC7 (auto·可靠): 审计器拒绝缺号、畸形 ID、缺失/孤立草稿和伪装键 ✓
- [x] AC8 (auto·可靠): 真源、双宿主投影、registry、规则卡与完整 CI 对账 ✓

# Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| auditor-tests | AC3–AC8 | captured | passed | `.ai/iterations/ITER-0068/evidence/auditor-tests/record.json` |
| registry-check | AC1–AC3, AC6, AC8 | captured | passed | `.ai/iterations/ITER-0068/evidence/registry-check/record.json` |
| diff-check | AC8 | captured | passed | `.ai/iterations/ITER-0068/evidence/diff-check/record.json` |
| full-ci | AC1–AC8 | captured | failed (sandbox diagnostic) | `.ai/iterations/ITER-0068/evidence/full-ci/record.json` |
| full-ci-retry | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0068/evidence/full-ci-retry/record.json` |
| final-full-ci | AC1–AC8 | captured | passed | `.ai/iterations/ITER-0068/evidence/final-full-ci/record.json` |

# Verification Results

- AC1–AC3：`milestone-schema.md` 定义候办入库/正式提升，Claude 命令和 Codex skill 均由 registry 对账。
- AC4–AC5：退回必须同时满足最新号、零迭代、零归档、零交付；否则只能 closed/abandoned。
- AC6：`goal-contract.md`、`lifecycle.md`、规则卡和双宿主入口一致声明候办不是正式里程碑。
- AC7：18 项状态审计回归全过，且畸形正式 ID 稳定报漂移而非抛堆栈。
- AC8：Goal 判定已允许保留失败诊断、但只用 passed record 覆盖 AC；修复后的最终完整 CI 通过。首次失败 record 仅保留为 uv 缓存权限诊断，不作绿色依据。

# Goal Calibration

- CAL-001：workflow registry 拒绝手改 Claude 受管投影 → 回 P4 修改 `workflows/registry.json` 并重生成 → resolved（registry-check）。
- CAL-002：旧 brief 文案会让候办期真源身份冲突 → P4 改为随阶段切换唯一真源 → resolved（full-ci-retry）。
- CAL-003：畸形正式号可能让审计器抛异常 → P4 先验证 ID 再计算序列 → resolved（auditor-tests）。
- CAL-004：完整 CI 证据首跑被沙箱禁止访问 uv 缓存 → 按宿主授权在沙箱外重跑 → resolved（full-ci-retry）。
- CAL-005：Goal adjudicator 与“失败证据必须保留”契约冲突 → 回 P3/P4 拆分 record 完整性与 passed AC 覆盖 → resolved（final-full-ci）。

# Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

# Gate Coverage

- 通用质量门禁：状态审计、registry 投影、Markdown 链接、双宿主地基、147 hooks 与完整 CI 均通过。
- Tech Plan Alignment：台账待办索引 + 独立草稿、开工才领号、四条退回预检和状态审计均按方案落地。
- References Compliance：N/A，本轮无外部规格资料。

# Review

- 方式：危险模式同上下文完整强审；未触发 opt-in 独立复核。
- 首轮 Must Fix：2 项；收口裁决追加发现 1 项；3 项均已修复并重跑专项与完整证据。
- 最终结论：Must Fix 0，Should Fix 0，pass。

# Remaining Risks

- 本轮无未关闭实现风险。
- 候办入库/提升仍由 AI 按文档契约执行，不是独立事务 CLI；状态审计能发现集合漂移，但不替代宿主对单次多文件写的原子性。

# Handoff / Next Step

- 可进入 Goal adjudicator 和 ITER-0068 原子收口；本轮不发布、不推送、不升级外部项目。
