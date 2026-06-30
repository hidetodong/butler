# 更新日志 (Changelog)

本文件记录 butler 规则仓库的发布历史。版本号遵循[语义化版本](Coder/20_Workflow_Lifecycle/versioning-schema.md)：`MAJOR.MINOR.PATCH`。

每个版本聚合自上次发布以来收口的若干迭代（ITER），**只引用** `.ai/ITERATIONS.md` 与 `deliveries/`，不复述迭代细节。版本号机器真源是仓库根 `VERSION` 文件。

## [1.5.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0015 ~ ITER-0016（自 v1.4.0 起新收口），两个迭代均为向后兼容的规则正文新增 / 既有字段口径强化，无破坏性变更，按 semver 取区间最高级别为 MINOR。

### 本版新增

- **handoff 格式契约补全（ITER-0015）**：`Coder/40_Context_Management/handoff-spec.md` 新增 §4 模板骨架（H1 锁死 `# Session Handoff` + 6 个固定顺序 H2 + 模板规则）与 §5 蒸馏生成流程（5 步不得跳步 + 4 条反模式）；`context-persistence.md §6` 补一行指针指向骨架与流程。补全此前"有字段、无骨架、无步骤"的半截契约，字段语义与 hook 未动。详见 `deliveries/ITER-0015-handoff-template-and-flow.md`。
- **tasks 步骤轻量引入 · 方案 A（ITER-0016）**：参照 SDD（Specify → Plan → Tasks → Implement）评估后不引入强制第五件套，而是强化 `tech-plan-schema.md` 既有 `Execution Steps` 字段——升级为可勾选 / 绑 AC / 可标依赖与并行（`[P]`）的任务清单，粒度随迭代大小；`context-persistence.md §4` 补 `task-state.md` 任务镜像作 P4 活进度板并声明 AC 仍是验收脊柱；`artifact-style.md` 新增 §5 任务清单书写口径。四件套字段结构 / hook / rule-card / README 零改动。本迭代 P2 用户 ACK、自 P3 起 `/dangerous` 自治，P5 独立复核 6/6 confirm。详见 `deliveries/ITER-0016-tasks-step-lite.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.5.0]: 自 v1.4.0 起聚合 ITER-0015 ~ ITER-0016

## [1.4.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0014（自 v1.3.0 起新收口），向后兼容新增，按 semver 为 MINOR。

### 本版新增

- **版本升级 SOP 化（ITER-0014）**：新增 `Coder/20_Workflow_Lifecycle/migration-schema.md` 定义"迁移配方"格式——配方落仓库根 `migrations/vX.Y.Z.md`、用 typed 标签（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`）列出已部署项目升级到该版的幂等步骤，附"先校验起始态、漂移退回 ACK"契约，并回填 `migrations/v1.1.0 ~ v1.3.0`；`butler-upgrade.md` 由"现场推导差异"改为"按版本区间收集配方、按序幂等执行"（含 `.claude/hooks/` 副本同步，补 `mcv-deployment.md §5.4` 缺口），无版本戳老项目保留全量首次升级兜底；`versioning-schema.md §5` 切版流程新增"写迁移配方"必做步（无影响也写 `[no-op]`）。本迭代在 `/dangerous` 危险模式下自治完成，P5 独立复核查出并修复 v1.1.0 漏 `[regen-claude]`。详见 `deliveries/ITER-0014-migration-ledger.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.4.0]: 自 v1.3.0 起聚合 ITER-0014

## [1.3.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0012 ~ ITER-0013（自 v1.2.0 起新收口），两个迭代均为向后兼容新增，按 semver 为 MINOR。

### 本版新增

- **四件套讲人话 + 反啰嗦（ITER-0012）**：新增 `Coder/20_Workflow_Lifecycle/artifact-style.md` 作为四件套字段正文书写口径单一来源——正文须让不懂内部机制者也读得懂（反黑话）、一律 bullet / 嵌套 ≤2 / 不复述 / 宁缺毋滥（反注水），VERIFY 用 `[x] ACn ✓ 一句话证据` 紧凑式；接线四 schema 编写规则 + `rule-card` + `Coder/README`。字段结构未动。详见 `deliveries/ITER-0012-artifact-plain-language.md`。
- **CONCEPT 分层 / 渐进展开（ITER-0013）**：`artifact-style.md` 增「渐进展开与分层」节（顶部一句话意图 + 一行一意 / 拆箭头链 + 承重引用首次解释 + 散文层与精度层不串味 + 不啰嗦 ≠ 极限压缩）；`concept-schema` 模板顶部增「一句话」块（散文意图速览，与 `Goal` 分工、向后兼容 legacy）。把「对人友好 / 对 AI 友好」统一为同一目标，唯一偏差用分层吸收。详见 `deliveries/ITER-0013-concept-layering.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.3.0]: 自 v1.2.0 起聚合 ITER-0012 ~ ITER-0013

## [1.2.0] - 2026-06-22

向后兼容能力新增版。聚合 ITER-0011（自 v1.1.0 起新收口），按 semver 为 MINOR。

### 本版新增

- **对话输出呈现协议（ITER-0011）**：新增 `Coder/00_System_Prompt/presentation-protocol.md`，把 P1-P3 方案 / 分析 / 选项类对话输出统一为「结论先行 + 统一标号 + 选项表格 + 结尾下一步」，默认固定 + 弹性、仅管较长输出；接线至 `identity` / `logic-protocol` / `rule-card`（高注意力区）/ `Coder/README`，与 `delivery-summary §8`（P5 交付摘要散文化）分场景共存。详见 `deliveries/ITER-0011-presentation-protocol.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.2.0]: 自 v1.1.0 起聚合 ITER-0011

## [1.1.0] - 2026-06-22

向后兼容能力新增版。聚合 ITER-0008 ~ ITER-0010——三个迭代均为向后兼容新增（无破坏性变更），按 semver 取区间最高级别为 MINOR。

### 本版新增

- **迭代状态封闭三态 + 机械门禁（ITER-0008）**：迭代台账状态固化为 `active` / `closed` / `abandoned` 封闭枚举，新增 `ledger_status` hook 拦截越界值（`planned` 等里程碑路线项不得写入迭代台账）。详见 `deliveries/ITER-0008-iteration-status-enum-lockdown.md`。
- **preference 项目级抑制开关（ITER-0009）**：`.ai/local-constraints.md`「Butler 功能开关」新增 `preference: on|off`（默认 on）作 per-project 采集闸；consent / 数据真源仍外置 `$BUTLER_PREF`（跨项目唯一真源），本开关不双写。详见 `deliveries/ITER-0009-preference-per-project-toggle.md`。
- **交付总结固定格式 HTML 阅读视图（ITER-0010）**：迭代 / 里程碑收口在 `.md` 之外并列产出同名 `.html`（固定格式模板 SSOT `templates/delivery.html.template`、单文件自包含、双击可离线打开）；`.md` 仍为引用真源，HTML 同守只引用不嵌入。详见 `deliveries/ITER-0010-delivery-html-view.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.1.0]: 自 v1.0.0 起聚合 ITER-0008 ~ ITER-0010

## [1.0.0] - 2026-06-19

首个正式版本基线。聚合 ITER-0001 ~ ITER-0007，为 butler 规则仓库确立硬版本概念（VERSION / CHANGELOG / git tag），并把版本接入部署产物与升级协议。

### 能力基线（本版已具备）

- **三层规则体系**：SOP Core（00/20/30/40）+ Domain / Stack Profiles（10）+ Business Extension（99），职责分明不混层。
- **五阶段产物链**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P4 Execute → P5 VERIFY_REPORT，阶段间经文件传递、不依赖对话记忆。
- **迭代化需求管理**：ITER-NNNN 台账 + 工作区/归档/交付三层落盘 + "固定需求"锁定纪律；**里程碑**（MILE-NNNN）作为松耦合、可选、方向性不冻结的大版本范围层，支持对话 / `origin/` 双通道录入与 `/milestone` 命令。
- **控制状态外化**：ACK 冻结门禁、入口分流可审计、项目级 butler 功能开关（`dangerous` / `independent_review`）统一落 `.ai/local-constraints.md` 并跨会话持久。
- **基地车生命周期三协议**：部署（mcv-deployment）/ 升级（butler-upgrade）/ 维护（mcv-update），配合 PreToolUse hook 机械门禁（产物缺失 / AC 未冻结拦截源码写）。
- **扩展模块**：ideation（脑暴）/ convergence-loop（死磕闭环）/ code-review（含 opt-in 独立复核，验证者≠实现者）/ dangerous（无人值守长程自治）/ preference（偏好探针，外置存储）。
- **本版新增（ITER-0007）**：硬版本概念落地——根 `VERSION` 为版本号 SSOT、`CHANGELOG.md` 为人读发布史、git tag `vX.Y.Z` 为发布锚点；部署把规则源版本戳进目标 `CLAUDE.md`（`{{BUTLER_VERSION}}`）；`butler-upgrade` 升级为版本感知（读目标戳 vs 仓库 VERSION 报 gap、升级后重戳，版本号为辅、内容差异为主）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.0.0]: 基线版本（无前序版本可比较）
