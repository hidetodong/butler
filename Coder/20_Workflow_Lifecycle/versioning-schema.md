---
title: 提交与版本治理协议
audience: AI / 开发者
scope: butler 规则仓库的提交规约（commit message 格式）、版本号 SSOT、semver 口径、CHANGELOG、切版 git 仪式、部署版本戳与升级版本 gap
---

# 提交与版本治理协议 (Commit & Versioning)

## 1. 目标与单一真源 (SSOT)

butler 规则仓库引入硬版本概念，让"当前规则源是哪一版"成为机器可读、人类可读、可比较的事实。

- **版本号机器真源**：仓库根 `VERSION` 文件，内容为单行 `MAJOR.MINOR.PATCH`（纯文本，无 `v` 前缀）。
- 其余一切版本载体——`CHANGELOG.md`、git tag、部署到目标项目的版本戳——都**从 `VERSION` 派生或与之对齐**，不得另立第二处版本数字。
- 修改版本号 = 修改 `VERSION`，其他载体随发布流程（§6）同步。

## 2. semver 语义（规则仓口径）

本仓库是 Markdown 规则仓库而非软件包，semver 三级按"对规则契约的影响"定义：

- **MAJOR（破坏性变更）**：规则文件重命名 / 删除；schema 必填字段删除或语义改写；产物链阶段重排；hook 拦截契约变更；命令语义不兼容变更。此类变更可能要求已部署目标项目人工迁移。
- **MINOR（向后兼容的能力新增）**：新增 schema / 命令 / 扩展模块 / 功能开关；新增可选字段；新增不影响既有契约的规则。
- **PATCH（不改变行为的修订）**：措辞澄清、错字订正、排版与交叉引用修复。

判定一次发布的 bump 级别：取该发布聚合的迭代区间内**最高**的变更级别。

## 3. CHANGELOG 与 ITER 台账的分工

两侧各自单一真源，互不复述：

- **`.ai/ITERATIONS.md`（ITER 台账）**：颗粒级开发真源，每个迭代一行（号 / 标题 / 状态 / 开启收口 / 交付链接）。
- **`CHANGELOG.md`（发布史）**：发布级聚合，每个版本一条，聚合自上次 tag 以来收口的若干 ITER。条目**只引用** `deliveries/` 与 ITER 台账链接，**不复述**迭代细节。

CHANGELOG 格式：位于仓库根；条目按版本倒序；每条以 `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD` 起头；顶部声明版本号遵循本协议并指向 `VERSION`。

## 4. git tag 约定

每次发布在发布提交上打 `vX.Y.Z` 形式的 tag（带 `v` 前缀），其数字部分必须与当时的 `VERSION` 一致。tag 是发布锚点，便于回溯"某一版规则源的确切提交"。

## 5. 提交规约 (Commit)

git 提交是迭代产物落盘的最小动作。本仓提交遵循统一 message 格式，使"某次提交对应哪个迭代、属哪类改动"一眼可读、可追溯。

### 5.1 message 格式

```
type(scope): 中文描述 (ITER-NNNN)

<body：可选；bullet 列关键改动 / 收口结论，引用 deliveries 与台账，不复述细节>

Co-Authored-By: <署名> <邮箱>
```

- **type**（借鉴 Conventional Commits，**非严格遵循其全套规范**，只借用 `type(scope):` 前缀形态）：
  - `feat` 新增能力 / 规则 / schema · `fix` 修缺陷 · `docs` 纯文档 · `refactor` 不改行为的重构 · `chore` 杂务 / 发布 · `test` 测试 · `style` 纯格式。
- **scope**（可选但鼓励）：本次改动的规则模块或区域名，小写，取文件 / 目录语义名——如 `hook`、`lifecycle`、`versioning`、`handoff`、`readme`、`release`、`preference`。
- **中文描述**：一句话说清这次干了什么，动词开头，句末不加句号。
- **`(ITER-NNNN)` 尾注**：把提交绑回迭代号；一次提交聚合多个迭代时并列 `(ITER-A, ITER-B, ITER-C)`。无对应迭代的杂务提交（如仓库脚手架）可省尾注。
- **body**（可选）：bullet 列关键改动或收口结论；**引用** `deliveries/ITER-*.md` 与 `.ai/ITERATIONS.md`，**不复述**迭代细节（与 `changelog-schema.md §4` 同一分工——细粒度对象级变更在 `01_CHANGELOG.md`、人读高层在 delivery、commit body 只做索引式概述）。
- **署名 trailer**：末行附 `Co-Authored-By:` 署名（本仓历史提交全带），为标准尾注。

### 5.2 发布专用形态

聚合发布（切版，§6）的提交固定用 `chore(release)`：

```
chore(release): vX.Y.Z — 聚合 ITER-A~ITER-B (级别)

<body：定 bump 依据 + 版本级改动摘要（VERSION / CHANGELOG / migration）>

Co-Authored-By: ...
```

- `级别` = `MAJOR` / `MINOR` / `PATCH`（本次 bump 级别，判定见 §2）。
- 区间用 `~`（`ITER-0015~0016`）或并列列举；body 写 bump 依据与迁移配方要点。

### 5.3 何时提交 / 一次装什么

- **提交单元 = 迭代收口**：迭代走到收口（`iteration-schema.md §5.5`）是提交主节奏；一次提交装该迭代的规则改动 + 其 `.ai/` 产物（归档四件套、交付、台账更新）。
- 多个迭代同批收口可合并为一次提交，尾注并列各 ITER 号（如历史 `(ITER-0017, ITER-0018, ITER-0019)`）。
- 过程中的 WIP 提交允许，但迭代收口是语义提交点——收口提交须让 message 能独立说清这轮交付。
- **发布提交独立**：切版只提交发布元数据（`VERSION` / `CHANGELOG.md` / `migrations/vX.Y.Z.md` + 里程碑收口产物），不与迭代内容提交混在一起（迭代内容应已随各自收口提交）。

### 5.4 非机械门禁

commit message 格式**不进 hook 机械门禁**——PreToolUse hook 拦截的是文件写操作，管不到 `git commit`；且 butler 仓自身不跑自己的 hook（规则仓非部署项目）。提交规约靠**纪律 + 收口自检**兜底，与"会话起始必读""切版靠纪律"同源同险（§9）。

## 6. 切版流程（发布）

发布是对若干迭代的**聚合动作**，按需触发——**不是每个迭代都发版**。

### 6.1 提交 ≠ 切版（两条路径）

- **日常路径**：迭代收口 → 一次 `type(scope): … (ITER-NNNN)` 提交 + push；**不切 tag、不改 `VERSION`**。多数迭代走这条。
- **发布路径**：按需把自上次 tag 以来若干已收口迭代**聚合切版**，走 §6.2-§6.4 仪式。切版是聚合动作，非每迭代触发。

### 6.2 切版前预检

切版前先确认状态一致、无悬挂：

1. **定区间**：`git tag` 取最近发布 tag，对照 `.ai/ITERATIONS.md` 列出自那以来 `closed` 的迭代——这是本次聚合区间。
2. **跑一致性自检**：执行 `context-persistence.md` 冷启动一致性自检 5 不变量（current↔状态 / 至多一个 active / closed 有交付且文件存在 / closed 有归档 / 里程碑路线项对账）；**有漂移先修，不带病切版**。
3. **无悬挂 active**：区间内不得有未收口的 `active` 迭代（要么收口、要么按 `iteration-schema.md §5.6` 废弃）；迭代内容应已随各自收口提交，工作区无未提交的迭代产物遗留。

### 6.3 切版步骤（语义 + git 操作）

语义 5 步（定 bump / 改 VERSION / 加 CHANGELOG / 写 migration / 打 tag）落到具体动作：

1. **定 bump**：审视区间迭代，按 §2 取最高变更级别决定 MAJOR / MINOR / PATCH。
2. **改 `VERSION`**：写入新版本号（纯 `MAJOR.MINOR.PATCH`，无 `v` 前缀）。
3. **加 CHANGELOG 条目**：`CHANGELOG.md` 顶部加 `## [X.Y.Z] - YYYY-MM-DD`，聚合区间迭代、只引用不复述（§3）。
4. **写迁移配方**：产出 `migrations/vX.Y.Z.md`（格式与 typed 标签见 `migration-schema.md`）；对部署项目无结构影响也**必须**写一条 `[no-op]` 配方——"无影响"是显式结论，不是漏记。这是 `butler-upgrade.md` 升级执行器的输入。
5. **（若发布里程碑）收口里程碑**：本次发布聚合的是一个里程碑时，按 `milestone-schema.md` 的里程碑收口机制处理其台账 / 归档 / 版本级交付，不在此重写。
6. **git 序列**（按序执行）：

   ```
   git add VERSION CHANGELOG.md migrations/vX.Y.Z.md   # + 里程碑收口产物（如有）
   git commit -m "chore(release): vX.Y.Z — 聚合 ITER-A~B (级别)" -m "<body>"
   git tag vX.Y.Z                                       # 打在发布提交上，数字须 == VERSION
   git push && git push --tags                          # 或 git push origin <branch> vX.Y.Z
   ```

### 6.4 切版后自检

发布提交后核对三处版本载体对齐（§1 SSOT 要求）：

- `VERSION` 的数字 == tag `vX.Y.Z` 的数字 == `CHANGELOG.md` 顶条 `## [X.Y.Z]`，三者一致。
- `git tag --points-at HEAD` 含 `vX.Y.Z`（tag 确在发布提交上）。
- 任一不齐即就地修正，不留待下次发现。

## 7. 部署版本戳

基地车部署目标项目时（见 `mcv-deployment.md §3`）：

- 读 `$BUTLER/VERSION`，用其内容替换目标 `CLAUDE.md` 模板中的 `{{BUTLER_VERSION}}` 占位符。
- 占位符落在 `CLAUDE.md` 的 butler 管理区（`<!-- user-managed -->` 保护区之外），使后续升级可原地重戳。
- **版本戳语义 = 目标项目所基于的"规则源版本"**，与目标项目自身的业务版本无关，二者解耦。

## 8. 升级版本 gap

`butler-upgrade.md` 升级为版本感知：

- 侦察阶段读目标 `CLAUDE.md` 的版本戳与仓库当前 `VERSION`，计算并汇报版本 gap（目标无戳=视为前版本化）。
- **据版本 gap 收集并执行迁移配方**：取 `migrations/` 下区间内（目标戳 < vV ≤ `VERSION`）的配方按序执行（§6 在切版时已产出它们）——这把升级从"现场推导差异"变成"照配方执行"。
- 升级完成后把版本戳重戳到仓库当前版本。
- **版本号为辅、内容差异为主**：升级判定仍以文件内容差异为准绳，版本 gap 与配方仅给出确定步骤，每步仍先校验起始态、漂移即停退回 ACK，**不单凭版本号判定是否需要升级**（目标内容可能已手工漂移，版本号无法反映）。

## 9. 边界

- 本协议管 **butler 仓库自身**的提交规约、版本与发布；**目标项目**到最新 butler 的同步走 `butler-upgrade.md`。
- 提交规约默认约束 butler 仓自身提交；目标项目的提交规约推广不在本协议范围。
- 目标项目自身的业务版本独立演进，不由本协议管理。
- 提交规约、切版与版本戳维护均靠规则纪律执行（§5.4），无 hook 强制——与现有"会话起始必读"同源同险。
