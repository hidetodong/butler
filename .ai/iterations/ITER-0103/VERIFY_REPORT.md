<!-- butler-artifact-template: 1.0.0 artifact=verify_report -->
# VERIFY_REPORT — ITER-0103

## Verification Summary

- Decision Map state v1、四动作 Interface、依赖/Frontier、Claim Lease、Fog 原子 graduation、operation 幂等、本地并发与跨进程恢复均已通过确定性测试。
- P5 同上下文复核结论：Must Fix 0、Should Fix 0；复核期间加固 schema bool、目录竞态错误映射和多 Map 数字排序后，专项与完整 CI 重新通过。
- 11 条 AC 全部满足，无人测道残余；Goal assurance 返回 `eligible`，evidence 已整包归档并通过 archive verifier。

## AC Status

- [x] AC1 (auto·可靠): 单 Map 单 state、schema/revision 与无全局写索引通过目录/合同测试 ✓
- [x] AC2 (auto·可靠): 封闭枚举、严格字段、规范 ID、悬空/成环/abandoned dependency 均 fail-closed ✓
- [x] AC3 (auto·可靠): 可注入 UTC 下的派生 Frontier 与到期边界重复计算一致，state 不持久化 Frontier ✓
- [x] AC4 (auto·可靠): claim/renew/release/resolve、到期重领与 stale token 拒绝通过 ✓
- [x] AC5 (auto·可靠): DAG 边修改、open dependent abandon 阻断及 closed Map 只读通过 ✓
- [x] AC6 (auto·可靠): 单/多 Decision Fog graduation 与非法候选字节零变化通过 ✓
- [x] AC7 (auto·可靠): Python/CLI 仅四动作，inspect/plan/verify 目录快照零写通过 ✓
- [x] AC8 (auto·可靠): stale base、非阻塞锁、真实双进程竞争、replace/rename 故障与 operation receipt 幂等通过 ✓
- [x] AC9 (auto·可靠): CLI 跨进程恢复、canonical/symlink 防护及机器 verify 错误报告通过 ✓
- [x] AC10 (auto·可靠): 13 个 workflow 集合、唯一 Ideation 入口、opt-in、零写 suggest 与 P1 promotion 合同保持不变 ✓
- [x] AC11 (auto·可靠): 18 项专项、12 项 workflow 合同、链接/diff 与完整固定 CI 全部通过 ✓

## Evidence Index

| Evidence ID | AC | 强度 | Outcome | Record |
|---|---|---|---|---|
| decision-map-tests | AC1–AC9, AC11 | captured | passed | `.ai/iterations/ITER-0103/evidence/decision-map-tests/record.json` |
| workflow-contract | AC10, AC11 | captured | passed | `.ai/iterations/ITER-0103/evidence/workflow-contract/record.json` |
| review-decision-map-risk | AC2–AC6, AC8, AC9 | reproduced | passed | `.ai/iterations/ITER-0103/evidence/review-decision-map-risk/record.json` |
| full-ci | AC1–AC11 | captured | passed | `.ai/iterations/ITER-0103/evidence/full-ci/record.json` |

## Verification Results

- AC1：创建两类持久状态并冷读目录；只有 Map 目录下 canonical state 可写，锁目录不参与状态发现。
- AC2：参数化坏输入和候选全图验证覆盖未知/布尔 schema、非法 ID、悬空、环、open→abandoned dependency，失败前后 tree bytes 相同。
- AC3：同一 state 与 UTC clock 下重复 inspect 得到相同 Frontier；恰好 `now == expires_at` 时 claim 失效。
- AC4：worker A 到期、worker B 重领后，A 的 token 不能完成；有效 owner/token 可续租、释放和完成，未领取 Frontier 可直解。
- AC5：link 造成环、claimed 时改依赖、open dependent 时 abandon、未收敛 close 均拒绝；收敛后 close 且写操作只读阻断。
- AC6：Fog 一次创建内部 DAG 的多个 Decision；非法依赖在 plan 即拒绝，state/revision/Fog 均不变化。
- AC7：Interface/CLI 均只有 inspect、plan、apply、verify；三个只读动作通过全树 digest 证明零写。
- AC8：两进程持同一 base 竞争时只提交一次；stale plan exit 1；replace/rename 故障无半文件/半目录；同 request 重试返回原 token/revision。
- AC9：独立 subprocess plan/apply 后由新进程 inspect/verify 恢复；非 canonical、staging 与 symlink 以机器 code 报错。
- AC10：workflow registry 仍为 Router + 13 workflows，没有 Explore ID/命令；Ideation 只在用户 opt-in 后委托工具，promotion 仍从 Iteration P1。
- AC11：四份 evidence 均经 verifier 核对未截断、exit 0 和日志 SHA-256；完整 `scripts/verify-ci.sh` 在 Python 3.12.12 / uv 0.9.28 下 exit 0。

## TDD Pair Status

- N/A（TECH_PLAN 明确未声明 TDD cycle）。

## Goal Calibration

- P5 简评发现的三项防御性细节（schema bool、目录 rename 竞态码、多 Map 数字排序）均回到 P4 修正，并由 `decision-map-tests` 与 `full-ci` 重新验证为 resolved。
- 当前无未闭合 calibration signal。

## Completion Inputs

- Review Verdict: pass
- Completion Blockers: none

## Gate Coverage

- 通用质量门禁：专项状态/存储/CLI 测试、R1 workflow 合同、Python compileall、Markdown 链接、artifact contract、`git diff --check` 和完整 CI 均通过。
- Workspace Scope：N/A（AC 无 `prd_refs`）。
- Active Profiles：N/A（未激活 Domain / Stack Profile）。
- Tech Plan Alignment：T1–T8 全部兑现；Module、CLI Adapter、测试、规则指针与 CI 接线均在冻结文件范围内，没有新增 workflow、promotion 或远端协调。

## References Compliance

- N/A：本迭代无外部参考资料或 `prd_refs`；R1 现行 Explore 合同作为仓内权威规则继承。

## Remaining Risks

- `applied_operations` 为永久幂等保留 receipt，会随单 Map 操作数增长；R2 有意不做无迁移 compaction。
- 本地 `fcntl`/rename 保证只覆盖 Butler 当前 macOS/Linux 本地文件系统支持矩阵；跨主机和网络文件系统协调不在 R2 范围。
- Claim token 是高熵协调凭据而非权限认证；工具和文档均未把它表述为安全身份边界。

## Handoff / Next Step

- `ITER-0103` 已通过 Goal eligibility 与 evidence archive 校验，可完成台账、交付和项目知识折叠；R3 helper 仍为 planned，不自动开启或预占迭代号。
