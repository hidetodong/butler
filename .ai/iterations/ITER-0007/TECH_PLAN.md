# Goal
- 支撑 AC1–AC18：引入硬版本概念 + 切 v1.0.0（基线 + 接入部署/升级）。下文按文件给出精确改动锚点与内容口径。

# Files / Modules to Change

## 新增文件
### 1. 根 `VERSION` 【AC1】
- 内容：单行 `1.0.0`，无 `v` 前缀、文件尾无多余空行。版本号机器 SSOT。

### 2. 根 `CHANGELOG.md` 【AC2】
- 顶部：标题「更新日志 (Changelog)」+ 一句说明（版本号遵循 semver，详见 `versioning-schema.md`；每版聚合自上次发布以来收口的若干 ITER，只引用 deliveries/台账不复述）。
- `## [1.0.0] - 2026-06-19` 基线条目：一句定性（首个正式版本基线，聚合 ITER-0001~ITER-0007，确立硬版本概念）+「能力基线」要点列表（三层体系 / 五阶段产物链 / 迭代·里程碑 / 控制状态外化含 ACK·分流·功能开关 / 部署升级维护三协议 + hook 门禁 / 扩展模块 / 本版引入版本概念）+ 收尾"聚合迭代见 `.ai/ITERATIONS.md` 与 `deliveries/`"。**不逐条复述各 ITER 细节**（AC2/AC5 纪律）。

### 3. `Coder/20_Workflow_Lifecycle/versioning-schema.md` 【AC4/AC5/AC6】
- frontmatter：`title: 版本治理协议` / `audience: AI / 开发者` / `scope: butler 规则仓库版本号 SSOT、semver 口径、CHANGELOG 与发布、部署版本戳与升级 gap`。
- §1 目标与 SSOT：根 `VERSION` 是版本号唯一机器真源，格式 `MAJOR.MINOR.PATCH`；CHANGELOG/tag/部署戳均与之对齐，不另立第二处版本数字。
- §2 semver 语义（规则仓口径）【AC4】：
  - MAJOR：破坏性——规则文件重命名/删除、schema 必填字段删改、产物链阶段或 hook 拦截契约变更、命令语义不兼容变更（升级目标可能需人工迁移）。
  - MINOR：向后兼容能力新增——新 schema/命令/扩展模块/功能开关、新增可选字段。
  - PATCH：措辞澄清、错字、不改变行为的修复与重排。
- §3 CHANGELOG 与 ITER 台账分工【AC5】：ITER 台账=颗粒级开发真源（每迭代一行）；CHANGELOG=发布级聚合（一版聚合自上次 tag 以来若干 ITER），条目只引用 deliveries/台账链接、不复述。CHANGELOG 格式（按版本倒序、`## [x.y.z] - 日期`）与位置（仓库根）。
- §4 git tag 约定【AC5】：发布提交打 `vX.Y.Z`，与 VERSION 对齐。
- §5 切版流程【AC6】：① 按区间内最高变更级别定 bump → ② 改 `VERSION` → ③ CHANGELOG 加条目（聚合自上次 tag 以来 ITER）→ ④ 打 tag。按需发布、非每迭代发版。
- §6 部署版本戳【AC6】：部署读 `$BUTLER/VERSION` 替换目标 CLAUDE.md `{{BUTLER_VERSION}}`，记录目标"基于哪一版 butler 生成"；戳语义=规则源版本，非目标项目业务版本。
- §7 升级版本 gap【AC6】：butler-upgrade 读目标戳 vs 仓库 VERSION → 报 gap → 升级后重戳。**版本号为辅、内容差异为主**：升级判定以内容差异为准绳，版本 gap 仅辅助提示与重戳依据，不单凭版本号跳过升级（内容可能手工漂移）。
- §8 边界：本协议管 butler 仓自身发布；目标项目升级走 butler-upgrade；目标业务版本与 butler 版本解耦。

## 修改文件
### 4. `templates/CLAUDE.md.template` 【AC7】
- 顶部注释块（行 3–12）追加一条：说明 `{{BUTLER_VERSION}}` 由部署时读 `VERSION` 替换（沿用"注释用文字指代避免被误替换"口径）。
- 在注释块之后、`{{RULE_CARD_CONTENT}}` 之前插入一行可见 blockquote：`> 规则源：butler v{{BUTLER_VERSION}}　·　升级见 butler-upgrade`。落在 butler 管理区（远离 `<!-- user-managed -->`），保证升级可原地重戳。

### 5. `Coder/20_Workflow_Lifecycle/mcv-deployment.md` 【AC8】
- §3 规则注入：在现"步 3 替换 {{BUTLER_PATH}}"与"步 4 填用户区"之间插入新步——"读 `$BUTLER/VERSION`，用其内容替换 `{{BUTLER_VERSION}}` 占位符，标记目标项目所基于的 butler 规则源版本（见 `versioning-schema.md §6`）"；后续步骤顺延重编号（4→5、5→6）。

### 6. `Coder/20_Workflow_Lifecycle/butler-upgrade.md` 【AC9/AC10/AC11】
- §3 侦察：在动作 3（读 butler 仓最新状态）后增动作——读目标 `CLAUDE.md` 的 `butler v…` 版本戳与 `$BUTLER_PATH/VERSION`，计算并汇报版本 gap；目标无戳=视为前版本化（按 §4 首次升级路径）。
- §4 首次升级 步2/步5：生成新草稿/写入时戳上当前 butler 版本（老项目原无戳）。
- §5 常规升级 步2：生成新框架时把 `{{BUTLER_VERSION}}` 重戳为仓库当前版本；步4 升级清单新增"版本 gap：vX → vY"项。
- §7 验证：新增一条"`CLAUDE.md` 版本戳已更新到当前 butler 版本"。
- §8 边界：把"butler 仓库自身的升级…由 audit 流程管理"改为"…由 `versioning-schema.md` 切版流程管理（VERSION/CHANGELOG/tag）"；把"版本戳引入：butler 不引入版本戳…"整条**反转**为"版本号为辅、内容差异为主：升级以文件内容差异为准绳，版本 gap 仅作辅助提示与升级后重戳依据，不单凭版本号判定是否升级"。

### 7. `Coder/README.md` 【AC12】
- 目录结构 `20_Workflow_Lifecycle` 清单：在 `milestone-schema.md` 后、`local-constraints-schema.md` 前（或紧邻 butler-upgrade）插入 `versioning-schema.md`。
- 规则说明区：新增一条 `versioning-schema.md` 描述（版本号 SSOT/semver 口径/CHANGELOG 与发布/部署戳与升级 gap）。

### 8. `HUMAN_GUIDE.md` 【AC13】
- 新增"版本"小节：VERSION/CHANGELOG/git tag 在哪看；semver 三级含义一句话；部署产物 CLAUDE.md 会被戳上 butler 规则源版本；`/butler-upgrade` 会报版本 gap。措辞面向人类、简洁。

### 9. butler 根 `CLAUDE.md`（项目说明）【AC14】
- "目录结构与职责"列表补两条：`VERSION` — 版本号机器 SSOT；`CHANGELOG.md` — 人读发布史（聚合 ITER）。

# Design Decisions
1. **VERSION 单一真源**：版本数字只此一处，其余派生（AC15 一致性据此验证）。
2. **版本戳落 butler 管理区**：保证 butler-upgrade 常规升级能原地重戳，不触碰用户保护区（AC7/AC10 协同）。
3. **版本为辅、内容为主**：反转 §8 但保留诚实底线，不引入"凭版本号跳升级"捷径（AC11）。
4. **CHANGELOG 只引用不复述**：与 ITER 台账双真源解耦，规避产物链/单一来源约束（AC2/AC5）。
5. **不改 rule-card**：版本戳与 `{{BUTLER_PATH}}` 同类（部署替换值），直接落模板，不进浓缩规则卡（AC16 SSOT 护栏）。
6. **tag 在收口提交后打**：v1.0.0 = ITER-0007 收口状态快照，含本迭代自身（AC3）。

# Test / Verify Strategy
- AC1：`cat VERSION` = `1.0.0`，单行。
- AC2/AC5：grep CHANGELOG 含 `## [1.0.0]`、含 ITER-0001/ITER-0007 引用、含台账/deliveries 指针；目视确认无逐迭代复述。
- AC3：收口提交后 `git tag v1.0.0` + `git tag -l` 可见（P5 收口环节执行）。
- AC4/AC6：grep versioning-schema 含 MAJOR/MINOR/PATCH 定义、切版流程、部署戳、升级 gap、"内容差异为主"。
- AC7：grep `{{BUTLER_VERSION}}` 命中 template，且位置在 `<!-- user-managed -->` 之前；注释含其说明。
- AC8：grep mcv-deployment §3 含读 VERSION + 替换 {{BUTLER_VERSION}}；步骤编号连续。
- AC9/AC10/AC11：grep butler-upgrade 含版本 gap/重戳/§7 验证项；§8 旧"不引入版本戳"句已消失、新"内容差异为主"句存在。
- AC12/AC13/AC14：grep README/HUMAN_GUIDE/根 CLAUDE.md 命中各自落点。
- AC15：grep `{{BUTLER_VERSION}}` 三文件一致；全仓 grep 确认除 VERSION 外无第二处硬编码 `1.0.0` 版本数字（CHANGELOG/tag 的 1.0.0 是发布记录，非真源副本，允许）。
- AC16：`git diff --name-only` 确认 rule-card / hooks / preference / 四 schema / 台账字段未在改动名单（台账仅 current 与 ITER-0007 行变更属正常）。
- AC17：人工核对五约束。
- AC18：归档/delivery/台账核对。

# Rollback
- 纯文档/模板新增与改写，无运行态副作用。回退 = `git revert` 本迭代提交；tag 误打 = `git tag -d v1.0.0`。
