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
    iteration-schema.md
    milestone-schema.md
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

  /40_Context_Management
    context-persistence.md
    role-switch.md
    handoff-spec.md

  /50_Extension_Ideation
    ideation-engine.md

  /55_Extension_RalphLoop
    ralph-loop-engine.md

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

- `00_System_Prompt/`：协作身份与总调度协议。
- `20_Workflow_Lifecycle/`：通用需求开发 SOP 的阶段状态机、阶段交付约束与人类可读交付总结规范。
- `30_Quality_Gate/`：通用质量门禁与验证策略。
- `40_Context_Management/`：长任务、多阶段任务与交接场景下的上下文治理。
- `50_Extension_Ideation/`：仅在显式 `/ideation` 指令下启用的独立脑暴扩展模块。
- `65_Extension_Dangerous/`：仅在显式 `/dangerous` 指令或对应语义下启用的实验性无人值守长程自治模块。
- `70_Extension_Preference/`：仅在显式 `/preference` 指令下启用的实验性偏好探针模块，采集决策信号、蒸馏跨项目通识并反哺无监督自决；外置存储、与本仓库解耦，默认关。
- `10_Domain_Stack_Profiles/`：按项目类型选择的 Domain / Stack Profiles，不作为默认前置必读。
- `99_Business_Extension/`：业务侧最高优先级约束目录。

## 读取顺序

建议 AI 或开发者按以下顺序读取：

1. `00_System_Prompt/identity.md`
2. `00_System_Prompt/logic-protocol.md`
3. `20_Workflow_Lifecycle/`
4. `30_Quality_Gate/`
5. `40_Context_Management/`（长任务、多阶段任务、上下文压缩前重点读取）
6. `99_Business_Extension/*.md`（如存在，视为最高优先级业务约束）
7. `10_Domain_Stack_Profiles/` 中与当前项目类型匹配的规则文档，需先在 P1 Analysis 识别项目类型与技术栈后启用

`40_Context_Management/` 默认不是所有任务的前置必读，但在新项目接入 / 基地车部署、明确跨会话继续、需要 checkpoint 或 handoff、多阶段多子任务推进、需要等待用户 ACK 或外部结果，或预计无法单轮闭合时，应立即激活。若开始时未命中这些条件，但执行过程中发现任务会持续积累中间状态、仅靠最终代码无法恢复进度，也应在进入下一阶段前补激活。

其中：

- `20_Workflow_Lifecycle/mcv-deployment.md` 负责基地车部署协议。
- `20_Workflow_Lifecycle/mcv-update.md` 负责基地车维护文件的升级迁移协议。
- `20_Workflow_Lifecycle/butler-upgrade.md` 负责已部署项目到当前 butler 仓库最新版的主动升级协议（`/butler-upgrade`）。
- `20_Workflow_Lifecycle/maintenance-boundaries.md` 负责维护成本与批处理边界。
- `55_Extension_RalphLoop/ralph-loop-engine.md` 只在显式 `/loop` 指令或语义触发下启用，负责 P4 的自主纠错闭环与熔断规则。
- `65_Extension_Dangerous/dangerous-engine.md` 只在显式 `/dangerous` 指令或语义触发下启用，是实验性无人值守长程自治外壳：自主拆迭代连续推进、P2/P3 用户 ACK 由自审门替代、P4 复用 Ralph-Loop，附审计、回滚与 P5 强制完整审查护栏。
- `70_Extension_Preference/preference-probe-engine.md` 只在显式 `/preference` 指令下启用，是实验性偏好探针：采集高信号决策、按跨情境一致蒸馏为跨项目通识、反哺 `/dangerous` 自审门；数据外置（`$BUTLER_PREF`，与本仓库解耦）、先验非权威、绝不侵入迭代数据流，默认关。
- `20_Workflow_Lifecycle/concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 分别定义 P1 / P2 / P3 / P5 的必须产物、必填字段与交付模板。
- `20_Workflow_Lifecycle/iteration-schema.md` 定义迭代号分配、`.ai/ITERATIONS.md` 台账字段、工作区/归档/交付三层落盘关系与"固定需求"锁定纪律。
- `20_Workflow_Lifecycle/milestone-schema.md` 定义里程碑号分配、`.ai/MILESTONES.md` 台账字段、`.ai/MILESTONE.md` 范围评估/理解阐释/拆分路线图产物、启动信号与版本级交付纪律；里程碑是套在迭代之上、松耦合可选、方向性不冻结的大版本范围单元。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `.ai/local-constraints.md` 的字段与最小模板，在基地车部署的本地化适配步骤产出。
- `20_Workflow_Lifecycle/delivery-summary.md` 负责完整交付后的人类可读交付总结规范。
- `40_Context_Management/handoff-spec.md` 负责 `02_SESSION_HANDOFF.md` 的高密度结构约束。
- `50_Extension_Ideation/ideation-engine.md` 只在显式 `/ideation` 指令下启用，不属于默认执行主线。
- `60_Extension_CodeReview/review-engine.md` 在显式 `/review` 指令下执行完整审计，在 P5 交付阶段默认触发简要自评。
- `10_Domain_Stack_Profiles/` 只在识别到对应技术栈或工程形态后启用，不默认视为通用硬约束。

## 使用原则

- 默认按通用需求开发 SOP 执行。
- 若 `99_Business_Extension/` 下存在业务文档，则将其视为最高优先级业务约束。
- 所有非极小任务默认遵循 `P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify` 流程。
- P1-P3 产物存在性（`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`）在部署后由 Claude Code PreToolUse hook 机械拦截，详见 `20_Workflow_Lifecycle/mcv-deployment.md §5 Hook 注入`；绕过需 `BUTLER_BYPASS=1` + `.ai/bypass-reason.md`（非空）。
- `20_Workflow_Lifecycle/` 负责流程推进、交付节奏、基地车部署约束，以及完整交付后的人类可读总结规则。
- `40_Context_Management/` 负责长上下文、状态同步、阶段快照、交接规范与模式切换治理。
- `10_Domain_Stack_Profiles/` 中的规则仅在当前项目类型命中后作为执行 profile 生效。
- 质量校验必须可验证、可追踪、可回溯到验收项。
