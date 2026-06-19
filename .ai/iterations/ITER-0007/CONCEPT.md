> 分流: 完整 | 命中升级信号: 多文件改动(≥3) / 新增契约(版本号 SSOT + semver 口径 + 部署版本戳契约) / 跨模块影响(模板·部署·升级·README·人类文档) / 设计取舍(版本载体选型·版本与 ITER 台账分工·版本戳归宿·升级版本 gap 与内容差异的主从) / 反转既有规则(butler-upgrade §8「不引入版本戳」) | 2026-06-19

# Goal
- 给 butler 规则仓库引入**硬版本概念**并切出首个正式基线 **v1.0.0**，让"规则源现在是哪一版"成为机器可读、人类可读、可比较的事实，而非只活在 git 历史里。
- 范围（用户拍板）= **基线 + 接入部署/升级**：不只在仓内立一个版本号，还要把版本**戳进部署产物**、并让 **butler-upgrade 变成版本感知**（读目标戳 vs 仓库 VERSION → 报 gap → 升级后重戳）。

# Background / 为什么现在做
- butler 已连续收口 ITER-0001~0006，规则体系（三层 / 五阶段产物链 / 迭代·里程碑 / 控制状态外化 / 部署升级生命周期 / hook 门禁 / 扩展模块）已成形且自洽，具备"切基线"的条件——用户判断"已经可以有一个版本概念了"。
- 现状的洞：`butler-upgrade.md §8` 明文写"butler 不引入版本戳；升级靠文件内容差异检测，不靠版本号比较"。这是一条**有意为之的旧设计**，本轮按用户决策**反转**它——但保留"内容差异为主、版本号为辅"的诚实底线（版本戳不能假装等于内容未漂移）。
- 部署产物（目标项目 `CLAUDE.md`）目前只戳了 `{{RULE_CARD_CONTENT}}` 与 `{{BUTLER_PATH}}`，**无从得知自己是基于哪一版 butler 生成的**，升级时只能纯靠内容比对，缺一个粗粒度路标。

# Scope
## In
1. **版本载体三件**：仓库根 `VERSION`（机器 SSOT，纯文本 `MAJOR.MINOR.PATCH`）+ 根 `CHANGELOG.md`（人读发布史，按版本聚合 ITER、只引用不复述）+ git tag `v1.0.0`（发布锚点）。
2. **版本治理规则**：新增 `Coder/20_Workflow_Lifecycle/versioning-schema.md`——定义 VERSION 的 SSOT 地位与格式、规则仓口径下的 semver 语义（MAJOR/MINOR/PATCH 各对应哪类规则变更）、CHANGELOG 格式与位置、**版本与 ITER 台账的分工**（ITER 台账=颗粒级开发真源；CHANGELOG=发布级聚合，一版聚合自上次 tag 以来的若干 ITER）、切版流程、部署戳与升级 gap 的口径、版本戳语义边界。
3. **部署接入版本戳**：`templates/CLAUDE.md.template` 新增 `{{BUTLER_VERSION}}` 占位符（落在 butler 管理区，升级时可重戳）；`mcv-deployment.md §3` 增加"读 `$BUTLER/VERSION` → 替换 `{{BUTLER_VERSION}}`"的注入步。
4. **升级版本感知**：`butler-upgrade.md` §3 侦察增"读目标戳 vs 仓库 VERSION → 报版本 gap"，§4/§5 升级时重戳到当前版本，§7 验证增版本戳项，§8 反转"不引入版本戳"为"版本号为辅、内容差异为主"。
5. **注册与人类文档**：`Coder/README.md` 注册 versioning-schema.md（目录结构 + 说明）；`HUMAN_GUIDE.md` 增"版本"小节（VERSION/CHANGELOG/tag 在哪看、semver 含义、部署产物被戳版本、升级报 gap）；butler 自身 `CLAUDE.md`（项目说明）目录结构补 `VERSION` 与 `CHANGELOG.md` 两个根文件。
6. **切 v1.0.0**：写 `VERSION=1.0.0`、`CHANGELOG.md` 写入 1.0.0 基线条目（聚合 ITER-0001~0007）、收口后打 git tag `v1.0.0`。

## Out（非本轮）
- 不做自动化版本 bump 工具 / CI 校验（切版按规则人工触发）。
- 不为已部署的存量旧项目批量回填版本戳（属 butler-upgrade 触发时按需补，legacy 无戳=视为前版本化）。
- 不改 `templates/rule-card.md`（版本戳是部署替换值，与 {{BUTLER_PATH}} 同类，直接落模板，不进浓缩规则卡 SSOT）。
- 不改 hook 体系、不改 preference 数据流、不改产物链阶段定义、不改迭代/里程碑台账字段。
- 目标项目自身的业务版本与 butler 版本无关，本轮不涉及。

# Key Design Decisions（待 P3 细化，先定方向）
1. **VERSION 是唯一机器真源**：版本号只写在根 `VERSION`，CHANGELOG/tag/部署戳都从它派生或与它对齐，不另立第二处版本数字。
2. **版本与 ITER 台账双真源、互不复述**：ITER 台账记每个迭代（颗粒）、CHANGELOG 记每个发布（聚合区间），CHANGELOG 条目只引用 deliveries/台账链接。避免与"不破坏产物链 / 单一来源"约束冲突。
3. **版本号为辅、内容差异为主**：升级判定仍以文件内容差异为准绳，版本 gap 只作辅助提示与"升级后重戳"的依据——反转 §8 但不神化版本号（内容可能已手工漂移）。
4. **版本戳落 butler 管理区**：`{{BUTLER_VERSION}}` 戳在 CLAUDE.md 的 butler 区（非 `<!-- user-managed -->` 保护区），这样 butler-upgrade 常规升级能原地重戳而不碰用户内容。
5. **基线即现状快照**：v1.0.0 = ITER-0007 收口时仓库的能力全集，不追溯重构历史；ITER-0001 的回溯补号性质沿用台账既有备注口径。
6. **切版按需、非每迭代发版**：发布是对若干 ITER 的聚合动作，bump 级别由区间内最高变更级别决定（本轮初版直接定 1.0.0，用户指定）。

# Risks / Open Questions
- 版本戳靠规则纪律在部署/升级时维护（无 hook 强制），与现有"会话起始必读"同源同险——可接受，文档如实标注。
- 反转 §8 削弱"纯内容差异"的旧简洁性，换来粗粒度路标；以"内容为主、版本为辅"的措辞兜底，不引入"仅凭版本号跳过升级"的危险捷径。
- CHANGELOG 与 ITER 台账存在信息重叠风险——以"只引用不复述"纪律 + schema 明确分工规避。

# 影响文件（预估）
- 新增：根 `VERSION`、根 `CHANGELOG.md`、`Coder/20_Workflow_Lifecycle/versioning-schema.md`。
- 改：`templates/CLAUDE.md.template`、`Coder/20_Workflow_Lifecycle/mcv-deployment.md`、`Coder/20_Workflow_Lifecycle/butler-upgrade.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、butler 根 `CLAUDE.md`。
- 收口动作：git tag `v1.0.0`。
- 零改动护栏：`templates/rule-card.md`、`templates/hooks/`、`70_Extension_Preference/`、产物链四 schema（concept/acceptance/tech-plan/verify）、迭代/里程碑台账字段。
