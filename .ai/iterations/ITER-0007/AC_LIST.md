---
状态: ack-frozen
ACK 日期: 2026-06-19
---

# Goal
- 给 butler 规则仓库引入硬版本概念并切出基线 v1.0.0；范围 = 基线 + 接入部署/升级（版本戳进部署产物 + butler-upgrade 版本感知）。

# Acceptance Criteria

## A. 版本载体（基线）
- [ ] **AC1**：仓库根存在 `VERSION` 文件，内容为单行 `1.0.0`（纯文本，无 `v` 前缀、无多余空行），作为版本号机器 SSOT。
- [ ] **AC2**：仓库根存在 `CHANGELOG.md`，含 `## [1.0.0] - 2026-06-19` 基线条目；条目聚合 ITER-0001~ITER-0007、**只引用** `.ai/ITERATIONS.md` 与 `deliveries/`（不逐条复述迭代细节）；顶部说明版本号遵循 semver 并指向 versioning-schema。
- [ ] **AC3**：ITER-0007 收口提交后打 git tag `v1.0.0`（指向发布提交），`git tag` 可见。

## B. 版本治理规则（versioning-schema）
- [ ] **AC4**：新增 `Coder/20_Workflow_Lifecycle/versioning-schema.md`，含合规 frontmatter（audience / scope），定义：① 根 `VERSION` 为版本号 SSOT 及 `MAJOR.MINOR.PATCH` 格式；② 规则仓口径 semver 语义——MAJOR=破坏性（文件重命名/删除、schema 必填字段删改、产物链/hook 契约或命令语义不兼容变更）、MINOR=向后兼容能力新增（新 schema/命令/扩展/功能开关/可选字段）、PATCH=措辞澄清/错字/不改行为的修复。
- [ ] **AC5**：versioning-schema 明确 **CHANGELOG 与 ITER 台账的分工**——ITER 台账=颗粒级开发真源，CHANGELOG=发布级聚合（一版聚合自上次 tag 以来的若干 ITER），CHANGELOG 只引用不复述；并定义 CHANGELOG 格式/位置与 git tag `vX.Y.Z` 约定。
- [ ] **AC6**：versioning-schema 定义**切版流程**（定 bump 级别 → 改 VERSION → 加 CHANGELOG 条目 → 打 tag；按需发布、非每迭代发版）、**部署戳口径**（部署读 VERSION 戳 `{{BUTLER_VERSION}}`）与**升级 gap 口径**（升级读目标戳 vs 仓库 VERSION，版本号为辅、内容差异为主），并说明版本戳语义="规则源版本"而非目标项目业务版本。

## C. 部署接入版本戳
- [ ] **AC7**：`templates/CLAUDE.md.template` 新增 `{{BUTLER_VERSION}}` 占位符，落在 butler 管理区（`<!-- user-managed -->` 保护区之外），并在模板顶部注释中补充该占位符的替换说明。
- [ ] **AC8**：`mcv-deployment.md §3 规则注入` 新增一步——读 `$BUTLER/VERSION` 并替换 `{{BUTLER_VERSION}}`，步骤编号连续无断层。

## D. 升级版本感知
- [ ] **AC9**：`butler-upgrade.md §3 侦察` 新增动作——读取目标 `CLAUDE.md` 的 butler 版本戳与仓库当前 `VERSION`、计算并汇报版本 gap（目标无戳=视为前版本化，按既有首次升级路径处理）。
- [ ] **AC10**：`butler-upgrade.md` §4/§5 升级时把 `{{BUTLER_VERSION}}` 重戳到仓库当前版本，§5 升级清单含版本 gap 项；§7 验证项新增"CLAUDE.md 版本戳已更新到当前 butler 版本"。
- [ ] **AC11**：`butler-upgrade.md §8` 原"版本戳引入：butler 不引入版本戳…"条目被反转——改写为"版本号为辅、内容差异为主"（升级仍以内容差异为准绳，版本 gap 仅作辅助提示与重戳依据，不单凭版本号判定是否升级），并把 §8 中 butler 自身升级的治理指向 versioning-schema 切版流程。

## E. 注册与人类文档
- [ ] **AC12**：`Coder/README.md` 在 `20_Workflow_Lifecycle/` 目录结构清单与规则说明两处注册 `versioning-schema.md`。
- [ ] **AC13**：`HUMAN_GUIDE.md` 新增"版本"小节——说明 VERSION/CHANGELOG/git tag 在哪看、semver 三级含义、部署产物会被戳上 butler 规则源版本、升级会报版本 gap。
- [ ] **AC14**：butler 自身 `CLAUDE.md`（项目说明）的目录结构补充根 `VERSION` 与 `CHANGELOG.md` 两个文件及其职责。

## F. 一致性与零改动护栏
- [ ] **AC15**：`{{BUTLER_VERSION}}` 在 `templates/CLAUDE.md.template`（占位符）、`mcv-deployment.md`（替换步）、`butler-upgrade.md`（重戳）三处口径一致；版本载体处处指向根 `VERSION` 单一真源，无第二处硬编码版本数字。
- [ ] **AC16**：零改动护栏——`templates/rule-card.md`、`templates/hooks/`、`Coder/70_Extension_Preference/`、产物链四 schema（concept/acceptance/tech-plan/verify-schema）、迭代/里程碑台账字段定义未被改动（`git diff` 确认）。
- [ ] **AC17**：未破坏 CLAUDE.md 五约束——分层未混（新增落 20_ + 根载体 + 文档）、产物链未动、新增 versioning-schema 已在 README 注册、模板 SSOT 未手写重复、各规则文件 frontmatter 合规。

## G. 收口
- [ ] **AC18**：ITER-0007 四件套快照归档至 `.ai/iterations/ITER-0007/`，写 `deliveries/ITER-0007-<slug>.md`（引用路径、不嵌全文），台账行置 closed + 收口日期 + 交付链接，`current: none`。
