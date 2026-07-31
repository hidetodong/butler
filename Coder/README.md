---
title: Coder 子系统入口
audience: AI / 开发者
scope: Coder 子系统的目录导航、读取顺序与规则分工总览
---

# Coder

`Coder/` 是 butler 体系中的工程开发与 AI 协作子系统入口。

它承载一套**通用需求开发 SOP**，并允许在识别到具体项目类型后，按需叠加对应领域的执行规则。

其中：

- SOP Core 负责通用流程、质量门禁与上下文治理。
- Domain / Stack Profiles 负责特定技术栈或工程形态下的执行细则。
- Business Extension 负责业务侧最高优先级语义约束。

当其他应用或文件需要直接引用开发协作子系统时，应以 `Coder/README.md` 作为主入口。

`architecture-overview.md` 是入口补充说明文档，用于解释规则分层与启用关系；它位于 `Coder/` 根目录，不属于 `99_Business_Extension/`。

## 入口文档

- `README.md`：Coder 子系统主入口。
- `architecture-overview.md`：规则分层与启用关系的补充说明，不属于 Business Extension。
- `domain-model.md`：L1 限界上下文地图；只在跨模块所有权、同名状态或真源冲突等触发条件下读取。
- `domain-glossary.md`：L2 核心术语查询表；只读取当前问题相关行，再沿定义真源下钻。
- `context-map.md`：L2 主交付链转换合同；只在设计或审计 PRD→AC→Plan→Evidence→Goal→Handoff 时读取相关转换块。
- `../AGENTS.md`：Codex 编辑 Butler 仓时的自动发现入口与 `.ai/` 冷启动读序。
- `../docs/codex-compatibility.md`：Claude Code / Codex 共同内核、适配层边界与分阶段支持状态的真源。
- `../docs/workflows.md`：由机器注册表生成的双宿主入口、风险、触发与旧名兼容人读表。
- `../plugins/butler/`：Codex plugin 发布包与 12 个工作流 skill 的实体真源；`../.agents/skills/` 只以软链提供仓库发现。
- `../plugins/butler-pi/`：Pi TypeScript 扩展（`tool_call` / `tool_result` 事件拦截 + Python 门禁调用），安装到 `~/.pi/agent/extensions/`。

宿主入口只负责发现和路由：Claude Code 读根 `CLAUDE.md` 和 `.claude/commands/`，Codex 读根 `AGENTS.md` 与 `plugins/butler/` skills，Pi 读根 `AGENTS.md` 与 `plugins/butler-pi/` 扩展；规则算法仍以本目录为真源。目标项目两模板共同从 `templates/rule-card.md` 注入强制规则，由 `scripts/render-project-entrypoints.py` 在首次部署/升级时幂等维护。完整兼容边界不在本文件复述，统一见 `docs/codex-compatibility.md`。

## 目录结构

```txt
/Coder
  README.md
  architecture-overview.md
  domain-model.md
  domain-glossary.md
  context-map.md

  /00_System_Prompt
    identity.md
    logic-protocol.md
    presentation-protocol.md

  /10_Domain_Stack_Profiles
    vue3-standard.md
    typescript-rules.md
    build-tooling.md

  /20_Workflow_Lifecycle
    lifecycle.md
    goal-contract.md
    goal-calibration.md
    concept-schema.md
    acceptance-schema.md
    tech-plan-schema.md
    verify-schema.md
    human-test-bridge.md
    artifact-style.md
    iteration-schema.md
    changelog-schema.md
    milestone-schema.md
    versioning-schema.md
    migration-schema.md
    local-constraints-schema.md
    delivery-summary.md
    progressive-handoff.md
    mcv-deployment.md
    mcv-update.md
    butler-upgrade.md
    butler-setup.md
    maintenance-boundaries.md
  /30_Quality_Gate
    linting.md
    testing-strategy.md
    review-standard.md
    correction-contract.md
    implementation-discipline.md

  /40_Context_Management
    context-persistence.md
    role-switch.md
    handoff-spec.md
    sidework-receipt.md
    project-digest-schema.md
    references-schema.md
    workspace-scope-schema.md
    inbox-schema.md
    inbox-workflow.md
    prd-split.md
    prd-status.md
    prd-update.md

  /50_Extension_Ideation
    ideation-engine.md

  /55_Extension_ConvergenceLoop
    convergence-loop-engine.md

  /60_Extension_CodeReview
    review-engine.md

  /62_Extension_Agents
    overview.md
    independent-review.md
    knowledge-fold.md
    drift-check.md

  /65_Extension_Dangerous
    dangerous-engine.md

  /70_Extension_Preference
    preference-probe-engine.md

  /99_Business_Extension
    .gitkeep
```

规则目录说明：

- `domain-model.md` / `domain-glossary.md` / `context-map.md`：分别回答上下文边界、术语消歧与主链跨边界转换；`architecture-overview.md` 继续回答规则如何分层和启用，这些是正交导航。

- `00_System_Prompt/`：协作身份、总调度协议与对话输出呈现协议（`presentation-protocol.md`：方案 / 分析 / 选项类输出结论先行 + 统一标号 + 表格化 + 说人话四条对话层引用[定义真源在 `artifact-style.md §2`]）。
- `20_Workflow_Lifecycle/`：通用需求开发 SOP 的阶段状态机、阶段交付约束、四件套书写口径与人类可读交付总结规范。
- `30_Quality_Gate/`：通用质量门禁与验证策略（自动化优先纪律 + 自动道 / 人测道分道口径 + 分级置信「可靠 / 弱 / 待人」+ 代理验证）+ P4 常驻写码底线（`correction-contract` 纠错、`implementation-discipline` 最小实现）。
- `40_Context_Management/`：长任务、多阶段任务与交接场景下的上下文治理。
- `50_Extension_Ideation/`：仅在显式 `/ideation` 指令下启用的独立脑暴扩展模块。
- `62_Extension_Agents/`：butler 派出去干活的帮手（临时子 agent）的名册 + 通用规矩（唯一真源）+ 各帮手完整定义。**触发式加载、不进冷启动必读**；帮手=一份中立定义资料，用时读、临时起干净子 agent 执行、不下发到项目。当前住册三帮手：复核（`independent-review`，接 P5）、更新说明（`knowledge-fold`，收尾把 delta 折进 `.ai/project/`、只写该目录）、查过时（`drift-check`，冷启动/收口抽查说明过时、只读）；后两者是收口折叠 / 漂移自检的推荐 fresh-context 执行者（opt-in、非强制，折叠必做本身由收口步④定）。
- `65_Extension_Dangerous/`：仅在显式 `/butler:dangerous` 指令或对应语义下启用的实验性无人值守长程自治模块。
- `70_Extension_Preference/`：实验性偏好探针模块。**数据回路（采集 + 蒸馏）经一次性同意后默认常驻**，**影响回路（反哺）opt-in 且仅作用于有监督工作、绝不参与 `/butler:dangerous`**；只学真人选择，外置存储、与本仓库解耦。
- `10_Domain_Stack_Profiles/`：按项目类型选择的 Domain / Stack Profiles，不作为默认前置必读。
- `99_Business_Extension/`：业务侧最高优先级约束目录。

## 读取顺序

建议 AI 或开发者按以下顺序读取：

1. `00_System_Prompt/identity.md`
2. `00_System_Prompt/logic-protocol.md`
3. `00_System_Prompt/presentation-protocol.md`
4. `20_Workflow_Lifecycle/`
5. `30_Quality_Gate/`
6. `40_Context_Management/`（长任务、多阶段任务、上下文压缩前重点读取）
7. `99_Business_Extension/*.md`（如存在，视为最高优先级业务约束）
8. `10_Domain_Stack_Profiles/` 中与当前项目类型匹配的规则文档，需先在 P1 Analysis 识别项目类型与技术栈后启用

<!-- butler-context-l0:begin -->
### 核心概念渐进读取（L0）

- 普通单模块任务：停在本入口，直接读取目标专项规则；不得默认加载领域地图。
- 已知术语需要消歧：只查 `domain-glossary.md` 的相关行，再读取首批最多 3 份直接真源。
- 涉及跨模块所有权、同名状态、真源冲突或新增核心术语：先读 `domain-model.md` 定位上下文，再按需查术语和真源。
- 3 份是每批预算而非总上限；续批前先压缩已知结论，并公开记录问题、缺口、已读来源、下一批来源与选择理由。
- 只有显式完整领域审查才进入历史证据层；任何路径都不得递归追随引用或整目录读取。
<!-- butler-context-l0:end -->

`40_Context_Management/` 默认不是所有任务的前置必读，但在新项目接入 / 基地车部署、明确跨会话继续、需要 checkpoint 或 handoff、多阶段多子任务推进、需要等待用户 ACK 或外部结果，或预计无法单轮闭合时，应立即激活。若开始时未命中这些条件，但执行过程中发现任务会持续积累中间状态、仅靠最终代码无法恢复进度，也应在进入下一阶段前补激活。

冷启动 / clean-slate 重启时，先读项目**状态全貌产物**（系统现在整体是什么）建立认知——两态：采用 `.ai/project/` 知识文件夹的项目先读 `.ai/project/00_INDEX.md` 拿地图、按需钻相关主题；仍单文件的项目读 `.ai/PROJECT.md`。再读 `.ai/ITERATIONS.md`（变更流时间线）与 `.ai/02_SESSION_HANDOFF.md`（当前断点），最后按指针钻代码；读序细节（含两态第一读与 digest-and-point 读纪律）见 `40_Context_Management/context-persistence.md §6`。

其中：

- `20_Workflow_Lifecycle/mcv-deployment.md` 负责基地车部署协议；§0.1 先用 `scripts/resolve-project-root.py` 区分会话启动目录与实际施工项目根，用户点名路径优先、歧义时零写入。部署时只在已解析项目根创建 `.ai/`（含空 `.ai/project/` 知识文件夹种子，MILE-0003 R6 起——新项目采用文件夹态全貌产物）、`deliveries/` 与 `origin/`（人类原始概念输入收件箱，AI 只读，与 AI 处理注入的 `.ai/references/` 区分）。§6 另定义 **butler 驻留工具调用**（工具不拷进目标项目、按 `$BUTLER` 调用）：自动道证据 `tools/verification-evidence/` + 人测回传桥 `tools/delivery-selftest/`。
- `tools/state-ledger/` 负责 ITER/MILE 双台账的确定性热冷迁移、固定数字区间分片与定向 lookup：根热表与 `.ai/state-index.json` 都有界，index 只保存固定路由公式；`.ai/history/{iterations,milestones}/` 的每个有界冷片由同名 `.json` 独立记录范围/路径/数量/哈希。身份至少四位并按数字部分排序。
- `tools/artifact-pipeline/` 是五件套结构的机器 SSOT：versioned manifest 唯一定义 live 产物路径、阶段、H2 顺序、固定表头/状态字段和条件段，canonical templates 与其机械对账；新标记产物 strict，legacy 归档只读不追罚。
- `20_Workflow_Lifecycle/mcv-update.md` 负责基地车维护文件的升级迁移协议。
- `20_Workflow_Lifecycle/goal-contract.md` 是非极小任务 Goal 的共同合同真源：不新增 GOAL 台账，而从 milestone/CONCEPT、AC、TECH_PLAN、task-state、VERIFY/review 与收口事实派生 `active / at-risk / blocked / completion-candidate / complete / abandoned`；宿主 Goal/Task 只能做可重建投影。
- `20_Workflow_Lifecycle/goal-calibration.md` 管 P4/P5 新事实回流：六类信号投影到 task-state，再按事实性质回 P1–P5 或诚实停；open/blocked 信号不能被 tasks done 或风险措辞覆盖。
- `20_Workflow_Lifecycle/butler-upgrade.md` 负责已部署项目到当前 butler 仓库最新版的主动升级协议（`/butler-upgrade`）；版本感知，以 `migrations/` 下的迁移配方为主干、按版本区间收集后按序幂等执行（不再现场推导差异），并随升级同步 `.claude/hooks/` 副本。
- `20_Workflow_Lifecycle/butler-setup.md` 负责 `/butler:setup` / `$butler-setup` 的机器级安装语义：解析可信 Butler 根、亮明用户目录影响、确认后只委托 `scripts/setup.sh`，并分别汇报 Claude/Codex/Pi 结果；不替代项目 init/upgrade。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
- `30_Quality_Gate/correction-contract.md`（纠错收口契约）是 P4 默认常驻的底线纪律——修到真过、探测绑 AC、禁止降级修复、诚实停，无需触发、每次迭代生效。
- `30_Quality_Gate/implementation-discipline.md`（最小实现纪律）是与纠错契约并列的 P4 常驻底线——写新码爬「最小实现阶梯」（YAGNI→复用→标准库→平台原生→已装依赖→一行→最小新代码）、有意简化用 `butler-min:` 注释标天花板 + 升级路径、修 bug 挖根因不打症状补丁；但信任边界校验 / 安全 / 无障碍 / 用户明确要求不得砍、绝不对理解问题偷懒。无需触发、每次迭代生效；随 `30_Quality_Gate/` 常规读、不单列冷启动必读。
- `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 只在显式 `/butler:loop` 指令或语义触发下启用，是 P4 纠错的高强度升档（叠在常驻纠错收口契约之上），负责死磕式闭环与定量熔断规则。
- `65_Extension_Dangerous/dangerous-engine.md` 只在显式 `/butler:dangerous` 指令或语义触发下启用，是实验性无人值守长程自治外壳：自主拆迭代连续推进、P2/P3 用户 ACK 由自审门替代、P4 复用收敛闭环，附审计、回滚与 P5 强制完整审查护栏；无人值守下人测残余按 §7.4 依赖感知准入闸处置（不阻塞入账 / 弱验证顶 / 卡下游不硬闯 / 绝不假绿）。
- `70_Extension_Preference/preference-probe-engine.md` 是实验性偏好探针：**采集 + 蒸馏经一次性同意后默认常驻**、**反哺 opt-in 仅作用于有监督工作（P2/P3 提案 / 选项排序）、绝不参与 `/butler:dangerous`**；只学真人选择（模型自决不采集）；数据外置（`$BUTLER_PREF`，与本仓库解耦）、先验非权威、绝不侵入迭代数据流。命令：`/butler:preference on`/`off`（隐私总开关）、`reback on`/`off`（反哺）、`distill`（手动蒸馏）。
- `20_Workflow_Lifecycle/concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 分别定义 P1 / P2 / P3 / P5 的必须产物、必填字段与交付模板；VERIFY 含 Evidence Index、Goal Calibration 和 Completion Inputs。完整路径先由 verification evidence 生成 record，再由 `tools/goal-assurance/goal.py` 只读裁决 close eligibility；无证据或任一 blocker 不打绿。
- `20_Workflow_Lifecycle/human-test-bridge.md` 定义 P5 人测道残余的**等待-回收-续跑闭环**：有人场次触发条件 → 生成 manifest → `run_in_background` 起 butler 驻留「交付自测桥」（`tools/delivery-selftest/`）→ 阻塞等待桥进程自退 → 读 `results.json` → **四态路由**（通过=收口 / 未通过=进 `correction-contract` 纠错 / 延后=入账不阻塞 / 跳过=N/A）；无人值守（`/butler:dangerous`）不起桥、改走 `65_Extension_Dangerous/dangerous-engine.md §7.4` 准入闸。桥体输入 / 输出契约以 `tools/delivery-selftest/README.md` 为真源，本协议只接下游消费、不重抄字段。
- `20_Workflow_Lifecycle/artifact-style.md` 定义**所有面向人落地文档**（四件套 + 交付总结 + 知识文件夹 + handoff 等，四件套只是其一）的书写口径，并是**说人话四条硬标准**（术语先解释 / 比喻要落地 / 别让英文·变量裸奔 / 说中文不写翻译腔，跨对话与文档的通则）的单一真源（讲人话、反啰嗦、分层渐进展开——顶部一句话意图、一行一意、精度单独成层，同时对人和 AI 友好）；与四个 schema 分工：schema 管填哪些字段、本文件管字段里的话怎么写；四个 schema 的编写规则均指针引用它（单一来源），`presentation-protocol` 对话层引用其四条、rule-card 同步收录紧凑口径。
- `20_Workflow_Lifecycle/iteration-schema.md` 定义迭代号分配、`.ai/ITERATIONS.md` 台账字段、工作区/归档/交付三层落盘关系与"固定需求"锁定纪律。
- `20_Workflow_Lifecycle/changelog-schema.md` 定义 `.ai/01_CHANGELOG.md` 的格式契约：每迭代严格 ADD/EDIT/DELETE 对象级变更流（绑 AC、文件+章节级粒度、完整路径收口必产并归档），并厘清与 delivery / ITERATIONS / PROJECT 四产物分工。
- `20_Workflow_Lifecycle/milestone-schema.md` 定义里程碑号分配、未编号待办区、`.ai/MILESTONES.md` 看板字段、`.ai/MILESTONE.md` 范围/路线图产物、启动与版本级交付纪律。讨论好但尚未开工的多个独立方向必须拆成平级候办块，一方向一个键、一行索引、一份 `.ai/milestone-backlog/<slug>.md`，均不占 `MILE-NNNN`；明确推进某块时才从正式表领下一个连续号。录入支持对话 / `origin/` 两通道；`/milestone`、`/milestone start <候办键>` 与 `/milestone status` 分别负责录入/开启、候办提升和只读看板（§6.4–§6.5）。
- `20_Workflow_Lifecycle/versioning-schema.md` 定义 butler 规则仓库的**提交规约与硬版本概念**：提交 message 格式（`type(scope): 中文描述 (ITER-NNNN)`、发布用 `chore(release)`、非 hook 门禁、`Co-Authored-By` 署名 trailer）、仓库根 `VERSION` 为版本号机器 SSOT（`MAJOR.MINOR.PATCH`）、规则仓口径的 semver 语义（MAJOR 破坏性 / MINOR 兼容新增 / PATCH 澄清修订）、`CHANGELOG.md` 发布史与 ITER 台账的分工（发布聚合迭代、只引用不复述）、切版 git 仪式（切版前预检 → 定 bump / 改 VERSION / 加 CHANGELOG / 写 migration → `chore(release)` commit + tag + push → 切版后自检）与 git tag `vX.Y.Z` 约定、部署版本戳（`{{BUTLER_VERSION}}`）与升级版本 gap（版本号为辅、内容差异为主）。
- `20_Workflow_Lifecycle/migration-schema.md` 定义"迁移配方"格式：每个发布版一份 `migrations/vX.Y.Z.md`，用 typed 步骤（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`）列出已部署项目升级到该版要做的幂等动作；切版时产出（`versioning-schema.md §5` 必做步），升级时由 `butler-upgrade.md` 按版本区间收集执行。配方落仓库根 `migrations/`（与 `deliveries/`、`CHANGELOG.md` 同级的发布元数据）。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `.ai/local-constraints.md` 的人类可读字段与 legacy 兼容边界；新部署的机器配置改由 `.ai/butler.config.json` 承载，schema/严格读写/legacy 投影以 `tools/project-config/` 为真源。旧 Markdown 机器段只在 JSON 缺失时回退，升级由 `migrate_config` action 事务迁移并收窄本文件职责。
- `20_Workflow_Lifecycle/delivery-summary.md` 负责完整交付后的人类可读交付总结规范，含 §9「固定格式 HTML 阅读视图」（收口时与 `.md` 并列产出同名 `.html`，模板 SSOT 为 `templates/delivery.html.template`）。
- `40_Context_Management/handoff-spec.md` 负责 `02_SESSION_HANDOFF.md` 的固定结构与派生视图契约；`tools/handoff/handoff.py` 从权威状态执行 inspect/sync/check，receipt 陈旧时冷启动先重建再读取。
- `40_Context_Management/sidework-receipt.md` 负责用户主动发起的旁路工作回钩：旁路执行者在 `.ai/sidework/` 写一份短回执并返回路径，用户显式交给主 Agent 定向续接；不建立模型审批状态，不自动扫描，也不允许旁路执行者改主线权威状态。
- `40_Context_Management/project-digest-schema.md` 定义 `.ai/project/` 知识文件夹（项目常驻全貌知识地图、状态取向、整体积分）的格式契约——`00_INDEX` 入口、主题边界、digest-and-point、收口折叠与 `fold-state.json` 机器 receipt；receipt 只证文件/hash 参与，不替代语义漂移复核。它是冷启动第一读。
- `40_Context_Management/references-schema.md` 定义 `.ai/references/` 参考资料子系统的结构契约——扁平资料保持单文件；PRD 采用项目级需求总索引 + 日期化稳定 `prd_id` + 单需求模块索引 / 无损切片 / 独立 `.archive/vN/` 的两层集合结构。它区分全新需求、新版、重复与身份歧义，并接通多 PRD 钉版、legacy 迁移、split/status、确定性 update 与范围门禁。
- `40_Context_Management/workspace-scope-schema.md` 定义项目工作区地图与需求级代码范围：`.ai/project/workspaces.md` 用稳定 workspace key 映射当前路径并声明共享/生成路径 owner，单需求 PRD 以 primary/supporting/read-only/excluded 四类集合声明边界；模块只能收窄，TECH_PLAN 写计划、PreToolUse 与 diff 对账共用同一钉版解析器，越界先走扩张审查。
- `40_Context_Management/inbox-schema.md` 定义需求收件箱数据合同：`.ai/INBOX.md` 以稳定 `SRC-NNNN`、observed/processed 双 SHA-256、封闭状态和独立派生关系表追踪文件/对话/外部文档；同源变化、跨源重复和失败均 fail-closed，`origin/` 始终用户自管零写入。
- `40_Context_Management/inbox-workflow.md` 是收件箱动作层：确定性 scanner 登记来源事实，模型逐项分类，standard 确认或 dangerous 自审后委托 PRD/ideation/milestone 等既有规则；活工作区冲突按项等待，独立 sibling 继续。
- `../docs/prd-migration-guide.md` 是 legacy 单 PRD → 需求集合的人类操作指南：日期身份取证、零写 plan、事务 apply、历史引用解析、verify/rollback 与 backup 清理；执行真源是 `tools/prd-migrate/prd_migrate.py`。
- `40_Context_Management/prd-split.md` 是 PRD **首切动作层**：身份四态和日期证据先于写盘，按原文边界切模块，并把 `prd_id`、Workspace Scope 与切片方案一次 soft 对齐后写入独立需求目录。
- `40_Context_Management/prd-status.md` 是多 PRD **只读查询动作层**：项目级列表、按 `prd_id` 下钻、按稳定 workspace key 筛选，legacy 退化可读，坏布局 fail-closed；机械实现位于 `tools/prd-status/`。
- `40_Context_Management/prd-update.md` 是指定 `prd_id` 的**确定性改版动作层**：语义层确认最终模块/认亲/三态处置，`tools/prd-update/` 负责零写 plan、先冻后更的整 collection 事务、持久 receipt、幂等、verify/rollback；不自动改 active/closed 工作。
- `50_Extension_Ideation/ideation-engine.md` 只在显式 `/ideation` 指令下启用，不属于默认执行主线。
- `60_Extension_CodeReview/review-engine.md`：P5 默认同上下文简评；审查证据强度明确分 `reported/captured/reproduced`，未重跑不得称复现。独立复核由 `/review` 或 project-config `independent_review=true` 触发，fresh-context 逐 AC 核对（refute 即阻断）。
- `62_Extension_Agents/overview.md` 是帮手名册总述（帮手是什么 + 通用规矩 G1–G4 唯一真源 + 名册表 + 触发式加载）；`independent-review.md` / `knowledge-fold.md` / `drift-check.md` 分别是复核 / 更新说明 / 查过时三帮手的完整定义。名册**触发式加载、不进冷启动读序**；复核的共享审查流程仍以 `60_Extension_CodeReview/review-engine.md` 为真源、更新说明的折叠契约回指 `40_Context_Management/project-digest-schema.md §6`、查过时的漂移核对回指 `context-persistence.md` 第 6 不变量，各帮手文件回指对应真源不重写。三帮手 G1–G4 均回指 overview §3。
- `10_Domain_Stack_Profiles/` 只在识别到对应技术栈或工程形态后启用，不默认视为通用硬约束。

## 使用原则

- 默认按通用需求开发 SOP 执行。
- 若 `99_Business_Extension/` 下存在业务文档，则将其视为最高优先级业务约束。
- 所有非极小任务默认遵循 `P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify` 流程。
- P1-P3 产物存在性（`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`）在部署后由 Claude/Codex 共享 PreToolUse hook 机械拦截；此外 `AC_LIST.md` 须为 `状态: ack-frozen`，TECH_PLAN 显式状态须为 `方案状态: pass`，否则拦截源码写（两字段缺失的旧产物按 legacy 放行，新产物不得省略）。这套 hook 是**项目流程门禁，不是第二套文件权限**：能归属 Butler / Git 项目的目标按实际项目根校验，真实项目外路径退出判定并交宿主授权；坏输入仍 fail-closed；跨项目 patch 逐根校验且任一拒绝即整次拒绝。迭代台账非法状态值由 `ledger_status` 拦截，≥2 个 `active` 行由 `single_active_iteration` 拦截。详见 `20_Workflow_Lifecycle/mcv-deployment.md §5 Hook 注入`；流程绕过需 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空），正常项目外授权不走 bypass。此外另有一套 **PostToolUse 提醒 hook**（`butler_advisor.py`，advisory-only、fail-open、**绝不拦截**）：写 `.ai/MILESTONE.md` 时若 `.ai/references/prd/` 不存在，经 `additionalContext` 注入"PRD 先行自检"提醒（兜 PRD 切分软触发被绕过的漏切，`prd_split_reminder` 规则）。
- `20_Workflow_Lifecycle/` 负责流程推进、交付节奏、基地车部署约束，以及完整交付后的人类可读总结规则。
- `40_Context_Management/` 负责长上下文、状态同步、阶段快照、交接规范与模式切换治理。
- 旁路工作回执按 `40_Context_Management/sidework-receipt.md` **触发式读取**：用户发起旁路工作或显式给出 `.ai/sidework/` 回执路径时才读；不进入默认冷启动读序，不扫描目录猜待办。
- `10_Domain_Stack_Profiles/` 中的规则仅在当前项目类型命中后作为执行 profile 生效。
- 质量校验必须可验证、可追踪、可回溯到验收项。
