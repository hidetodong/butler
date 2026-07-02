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

## 目录结构

```txt
/Coder
  README.md
  architecture-overview.md

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
    concept-schema.md
    acceptance-schema.md
    tech-plan-schema.md
    verify-schema.md
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
    maintenance-boundaries.md
  /30_Quality_Gate
    linting.md
    testing-strategy.md
    review-standard.md
    correction-contract.md

  /40_Context_Management
    context-persistence.md
    role-switch.md
    handoff-spec.md
    project-digest-schema.md

  /50_Extension_Ideation
    ideation-engine.md

  /55_Extension_ConvergenceLoop
    convergence-loop-engine.md

  /60_Extension_CodeReview
    review-engine.md

  /65_Extension_Dangerous
    dangerous-engine.md

  /70_Extension_Preference
    preference-probe-engine.md

  /99_Business_Extension
    .gitkeep
```

规则目录说明：

- `00_System_Prompt/`：协作身份、总调度协议与对话输出呈现协议（`presentation-protocol.md`：方案 / 分析 / 选项类输出结论先行 + 统一标号 + 表格化）。
- `20_Workflow_Lifecycle/`：通用需求开发 SOP 的阶段状态机、阶段交付约束、四件套书写口径与人类可读交付总结规范。
- `30_Quality_Gate/`：通用质量门禁与验证策略（自动化优先纪律 + 自动道 / 人测道分道口径 + 分级置信「可靠 / 弱 / 待人」+ 代理验证）。
- `40_Context_Management/`：长任务、多阶段任务与交接场景下的上下文治理。
- `50_Extension_Ideation/`：仅在显式 `/ideation` 指令下启用的独立脑暴扩展模块。
- `65_Extension_Dangerous/`：仅在显式 `/dangerous` 指令或对应语义下启用的实验性无人值守长程自治模块。
- `70_Extension_Preference/`：实验性偏好探针模块。**数据回路（采集 + 蒸馏）经一次性同意后默认常驻**，**影响回路（反哺）opt-in 且仅作用于有监督工作、绝不参与 `/dangerous`**；只学真人选择，外置存储、与本仓库解耦。
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

`40_Context_Management/` 默认不是所有任务的前置必读，但在新项目接入 / 基地车部署、明确跨会话继续、需要 checkpoint 或 handoff、多阶段多子任务推进、需要等待用户 ACK 或外部结果，或预计无法单轮闭合时，应立即激活。若开始时未命中这些条件，但执行过程中发现任务会持续积累中间状态、仅靠最终代码无法恢复进度，也应在进入下一阶段前补激活。

冷启动 / clean-slate 重启时，先读项目 `.ai/PROJECT.md`（状态全貌、系统现在整体是什么）建立认知，再读 `.ai/ITERATIONS.md`（变更流时间线）与 `.ai/02_SESSION_HANDOFF.md`（当前断点），最后按指针钻代码；读序细节见 `40_Context_Management/context-persistence.md §6`。

其中：

- `20_Workflow_Lifecycle/mcv-deployment.md` 负责基地车部署协议；部署时在项目根创建 `.ai/`、`deliveries/` 与 `origin/`（人类原始概念输入收件箱，AI 只读，与 AI 处理注入的 `.ai/references/` 区分）。
- `20_Workflow_Lifecycle/mcv-update.md` 负责基地车维护文件的升级迁移协议。
- `20_Workflow_Lifecycle/butler-upgrade.md` 负责已部署项目到当前 butler 仓库最新版的主动升级协议（`/butler-upgrade`）；版本感知，以 `migrations/` 下的迁移配方为主干、按版本区间收集后按序幂等执行（不再现场推导差异），并随升级同步 `.claude/hooks/` 副本。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
- `30_Quality_Gate/correction-contract.md`（纠错收口契约）是 P4 默认常驻的底线纪律——修到真过、探测绑 AC、禁止降级修复、诚实停，无需触发、每次迭代生效。
- `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 只在显式 `/loop` 指令或语义触发下启用，是 P4 纠错的高强度升档（叠在常驻纠错收口契约之上），负责死磕式闭环与定量熔断规则。
- `65_Extension_Dangerous/dangerous-engine.md` 只在显式 `/dangerous` 指令或语义触发下启用，是实验性无人值守长程自治外壳：自主拆迭代连续推进、P2/P3 用户 ACK 由自审门替代、P4 复用收敛闭环，附审计、回滚与 P5 强制完整审查护栏；无人值守下人测残余按 §7.4 依赖感知准入闸处置（不阻塞入账 / 弱验证顶 / 卡下游不硬闯 / 绝不假绿）。
- `70_Extension_Preference/preference-probe-engine.md` 是实验性偏好探针：**采集 + 蒸馏经一次性同意后默认常驻**、**反哺 opt-in 仅作用于有监督工作（P2/P3 提案 / 选项排序）、绝不参与 `/dangerous`**；只学真人选择（模型自决不采集）；数据外置（`$BUTLER_PREF`，与本仓库解耦）、先验非权威、绝不侵入迭代数据流。命令：`/preference on`/`off`（隐私总开关）、`reback on`/`off`（反哺）、`distill`（手动蒸馏）。
- `20_Workflow_Lifecycle/concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 分别定义 P1 / P2 / P3 / P5 的必须产物、必填字段与交付模板；其中 `verify-schema.md` 的 VERIFY_REPORT 含自动道 / 人测道**分道回填**并叠**分级置信**（`(auto·可靠)` / `(auto·弱)` / `(human·待人)` 标记 + 人测道小结），口径见 `30_Quality_Gate/testing-strategy.md §3`（代理验证见 §3.1）。
- `20_Workflow_Lifecycle/artifact-style.md` 定义四件套字段正文的通用书写口径（讲人话、反啰嗦、分层渐进展开——顶部一句话意图、一行一意、精度单独成层，同时对人和 AI 友好），与四个 schema 分工：schema 管填哪些字段、本文件管字段里的话怎么写；四个 schema 的编写规则均指针引用它（单一来源），rule-card 同步收录紧凑口径。
- `20_Workflow_Lifecycle/iteration-schema.md` 定义迭代号分配、`.ai/ITERATIONS.md` 台账字段、工作区/归档/交付三层落盘关系与"固定需求"锁定纪律。
- `20_Workflow_Lifecycle/changelog-schema.md` 定义 `.ai/01_CHANGELOG.md` 的格式契约：每迭代严格 ADD/EDIT/DELETE 对象级变更流（绑 AC、文件+章节级粒度、完整路径收口必产并归档），并厘清与 delivery / ITERATIONS / PROJECT 四产物分工。
- `20_Workflow_Lifecycle/milestone-schema.md` 定义里程碑号分配、`.ai/MILESTONES.md` 台账字段、`.ai/MILESTONE.md` 范围评估/理解阐释/拆分路线图产物、启动信号与版本级交付纪律；里程碑是套在迭代之上、松耦合可选、方向性不冻结的大版本范围单元。录入支持两通道（对话 / 项目根 `origin/` 收件箱的原始概念文件），由模型据 brief 合成概述与路线图（§6.4）；显式命令 `/milestone`（开启录入）与 `/milestone status`（只读看板）与语义触发等价（§6.5）。
- `20_Workflow_Lifecycle/versioning-schema.md` 定义 butler 规则仓库的**提交规约与硬版本概念**：提交 message 格式（`type(scope): 中文描述 (ITER-NNNN)`、发布用 `chore(release)`、非 hook 门禁、`Co-Authored-By` 署名 trailer）、仓库根 `VERSION` 为版本号机器 SSOT（`MAJOR.MINOR.PATCH`）、规则仓口径的 semver 语义（MAJOR 破坏性 / MINOR 兼容新增 / PATCH 澄清修订）、`CHANGELOG.md` 发布史与 ITER 台账的分工（发布聚合迭代、只引用不复述）、切版 git 仪式（切版前预检 → 定 bump / 改 VERSION / 加 CHANGELOG / 写 migration → `chore(release)` commit + tag + push → 切版后自检）与 git tag `vX.Y.Z` 约定、部署版本戳（`{{BUTLER_VERSION}}`）与升级版本 gap（版本号为辅、内容差异为主）。
- `20_Workflow_Lifecycle/migration-schema.md` 定义"迁移配方"格式：每个发布版一份 `migrations/vX.Y.Z.md`，用 typed 步骤（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`）列出已部署项目升级到该版要做的幂等动作；切版时产出（`versioning-schema.md §5` 必做步），升级时由 `butler-upgrade.md` 按版本区间收集执行。配方落仓库根 `migrations/`（与 `deliveries/`、`CHANGELOG.md` 同级的发布元数据）。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `.ai/local-constraints.md` 的字段与最小模板，在基地车部署的本地化适配步骤产出；它也是**项目级 butler 功能开关的统一持久落点**——「Butler 功能开关」段（`dangerous` / `independent_review` 默认 off、`preference` 默认 on）承载持久模式状态，AI 会话起始读取并据此执行、命令回写或用户手改（§4.1）；其中 `preference` 是 **per-project 抑制开关**（本项目采集闸），consent/数据真源仍在外置 `$BUTLER_PREF`（跨项目），本开关不双写。
- `20_Workflow_Lifecycle/delivery-summary.md` 负责完整交付后的人类可读交付总结规范，含 §9「固定格式 HTML 阅读视图」（收口时与 `.md` 并列产出同名 `.html`，模板 SSOT 为 `templates/delivery.html.template`）。
- `40_Context_Management/handoff-spec.md` 负责 `02_SESSION_HANDOFF.md` 的高密度结构约束。
- `40_Context_Management/project-digest-schema.md` 定义 `.ai/PROJECT.md`（项目常驻全貌摘要、状态取向）的格式契约——字段、有界、指针化、收口前滚维护与四产物边界；它是冷启动第一读。
- `50_Extension_Ideation/ideation-engine.md` 只在显式 `/ideation` 指令下启用，不属于默认执行主线。
- `60_Extension_CodeReview/review-engine.md`：P5 默认触发同上下文简要自评；**独立复核（opt-in·fresh-context 子 agent·验证者≠实现者）**由手动 `/review` 或项目 `.ai/local-constraints.md` 的 `Review Policy: independent_review: on` 触发，spec-only 输入逐 AC 独立核对作者断言（refute 即阻断收口）。
- `10_Domain_Stack_Profiles/` 只在识别到对应技术栈或工程形态后启用，不默认视为通用硬约束。

## 使用原则

- 默认按通用需求开发 SOP 执行。
- 若 `99_Business_Extension/` 下存在业务文档，则将其视为最高优先级业务约束。
- 所有非极小任务默认遵循 `P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify` 流程。
- P1-P3 产物存在性（`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`）在部署后由 Claude Code PreToolUse hook 机械拦截；此外 `AC_LIST.md` 须为 `状态: ack-frozen`，未冻结的 `draft` 同样拦截源码写（无该字段的旧产物按 legacy 放行）；迭代台账 `.ai/ITERATIONS.md` 状态列若出现封闭枚举（active/closed/abandoned）外的值（如误把里程碑路线项的 `planned` 写入），由 `ledger_status` 规则拦截；写入后若出现 ≥2 个 `active` 迭代行（上一迭代未收口就开新），由 `single_active_iteration` 规则拦截。详见 `20_Workflow_Lifecycle/mcv-deployment.md §5 Hook 注入`；绕过需 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空）。
- `20_Workflow_Lifecycle/` 负责流程推进、交付节奏、基地车部署约束，以及完整交付后的人类可读总结规则。
- `40_Context_Management/` 负责长上下文、状态同步、阶段快照、交接规范与模式切换治理。
- `10_Domain_Stack_Profiles/` 中的规则仅在当前项目类型命中后作为执行 profile 生效。
- 质量校验必须可验证、可追踪、可回溯到验收项。
