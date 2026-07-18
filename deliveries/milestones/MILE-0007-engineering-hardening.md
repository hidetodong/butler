# MILE-0007 · Butler 规则仓工程化加固

> 里程碑交付（大版本） · 2026-07-18 · ITER-0056–ITER-0060 · UNRELEASED

## 本次交付目标

把已经成形的 Butler 规则、安装、状态、验证、升级和双宿主适配，从“操作者按文档应该做对”推进为程序能拒绝危险输入、机器能留下证据、CI 能拦漂移、升级能确定执行的工程系统。

## 已完成内容

- R1 安装器事务安全：全量预检 marker/export/软链所有权，用户配置原子更新，跨组件部分成功如实回声。
- R2 验证证据与状态自证：真实 argv/exit/log/hash record、整包归档和版本/台账/交付/fold receipt 审计。
- R3 持续验证：固定 Python/uv/lock/official validators，单一 local/CI 入口、Markdown 门禁和 Ubuntu/macOS workflow 合同。
- R4 可执行升级：连续机器 manifest、零写入 plan、项目事务 apply、split/global 分域、历史/漂移/恢复专项。
- R5 工作流治理：八 workflow registry、33 个窄投影、高风险显式门、唯一人读表和 plugin/distribution 边界。

## 关键变更 / 用户可感知变化

- 全局安装遇到残缺 marker、伪 export 或命令目录冲突时先停，不再覆盖用户资产或假报总成功。
- “测试通过”必须能追到机器 evidence；状态审计会机械发现发布、台账、归档、交付和知识折叠不一致。
- 本地与 CI 共用一条固定验证入口；依赖和官方 validator 来源可复现。
- Butler 升级先展示结构化计划，显式 apply 后才事务写入，冲突首写前停，失败恢复本次触及文件。
- Claude/Codex 工作流元数据只在 registry 维护，高风险策略和分发状态不再靠多份文档人工同步。

## 高层影响范围

- 新增/增强 `scripts/`、`tools/verification-evidence/`、`tools/butler-upgrade/`、`migrations/manifest.json`、`.github/workflows/`、`workflows/`、plugin 元数据与生成文档。
- P1–P5、迭代/里程碑核心语义和业务工作流算法没有重写。
- 当前全部改动位于隔离分支；VERSION 仍为 v2.16.0，尚未执行发布/tag/push。

## 拆分路线图回填

| 路线 | ITER | 结果 | 交付 |
|---|---|---|---|
| R1 安装器事务安全 | ITER-0056 | closed | [`deliveries/ITER-0056-global-installer-transaction-safety.md`](../../deliveries/ITER-0056-global-installer-transaction-safety.md) |
| R2 证据链与状态审计 | ITER-0057 | closed | [`deliveries/ITER-0057-verification-evidence-state-audit.md`](../../deliveries/ITER-0057-verification-evidence-state-audit.md) |
| R3 CI 与可复现验证 | ITER-0058 | closed | [`deliveries/ITER-0058-ci-reproducible-verification.md`](../../deliveries/ITER-0058-ci-reproducible-verification.md) |
| R4 可执行升级器 | ITER-0059 | closed | [`deliveries/ITER-0059-executable-upgrader.md`](../../deliveries/ITER-0059-executable-upgrader.md) |
| R5 工作流注册与分发 | ITER-0060 | closed | [`deliveries/ITER-0060-workflow-registry-distribution.md`](../../deliveries/ITER-0060-workflow-registry-distribution.md) |

## 验证方式与结果摘要

- 五个迭代均有独立 VERIFY、机器 evidence、四件套/CHANGELOG 归档、MD/HTML 交付和 fold receipt。
- R5 最终专项 8/8，完整固定工具链矩阵通过，含安装/升级/证据/审计/Markdown/CI contract、官方 plugin/8 skill validators 与 127 hook tests。
- 强复核的真实失败与修复轨迹均保留；MILE-0007 最终路线无 planned/active 项。

## 已知剩余风险 / 延后事项

- GitHub workflow 尚未推送，真实 Linux/macOS run 缺失；私有仓库当前套餐的 required API 为 403。
- team/public marketplace 未配置；个人 plugin 已装不等于团队可用。
- 可执行升级器尚缺真实外部老项目 dogfood，首次使用应保留 backup/journal 并人工审阅 diff。
- 本里程碑已收口但未发布；若切版，应按 MINOR 独立走 VERSION/CHANGELOG/migration/release commit/tag/push。

## 引用（只引用，不嵌入）

- `.ai/milestones/MILE-0007/MILESTONE.md`
- `.ai/ITERATIONS.md`
- `.ai/MILESTONES.md`
- `deliveries/ITER-0056-global-installer-transaction-safety.md`
- `deliveries/ITER-0057-verification-evidence-state-audit.md`
- `deliveries/ITER-0058-ci-reproducible-verification.md`
- `deliveries/ITER-0059-executable-upgrader.md`
- `deliveries/ITER-0060-workflow-registry-distribution.md`
