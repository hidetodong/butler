# 项目全貌（生成物）

> 本页由 `VERSION`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`、`Coder/README.md`、`workflows/registry.json`、`tools/` 通过 `python3 scripts/sync-project-overview.py --write` 生成，请勿手改。
> 只装可从机器源头派生的事实；长期决策与理由见 `.ai/invariants.md`，会过期的判断见 `.ai/debt.md`。

## 版本与当前状态

- 规则源版本：**3.6.0**
- 当前 active 里程碑：MILE-0016
- 当前 active 迭代：none
- 累计里程碑 16 个、迭代 114 个（台账热表各留 16 / 20 行，其余在 `.ai/history/` 冷分片）

## 里程碑时间线

| 里程碑 | 标题 | 状态 | 起 | 止 | 含迭代 |
|---|---|---|---|---|---|
| MILE-0016 | Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器 | active | 2026-08-18 | — | 3 |
| MILE-0015 | Butler 领域模型治理：统一语言、限界上下文与可执行边界 | closed | 2026-07-31 | 2026-08-17 | 5 |
| MILE-0014 | Butler Explore 决策地图接入：把持久化决策探索衔接到 Milestone 与 Iteration | closed | 2026-08-01 | 2026-08-02 | 5 |
| MILE-0013 | 项目级 Butler 配置结构化：从本地约束中拆出扁平 JSON 配置 | closed | 2026-07-28 | 2026-07-28 | 3 |
| MILE-0012 | 轻量 TDD 配对证据：复用现有 evidence 记录同一测试命令先失败、后通过并接入收口检查 | closed | 2026-07-24 | 2026-07-26 | 2 |
| MILE-0011 | 确定性五件套产物链：固定结构、阶段生成与机械校验 | closed | 2026-07-23 | 2026-07-23 | 4 |
| MILE-0010 | Butler 长期规模治理：可信 handoff、长编号与有界双台账 | closed | 2026-07-22 | 2026-07-22 | 2 |
| MILE-0009 | 需求收件箱、多 PRD 与 Monorepo 范围治理 | closed | 2026-07-22 | 2026-07-22 | 8 |
| MILE-0008 | Butler 目标可信闭环：让 Goal 从“任务做完”升级为经方案准入、执行校准、证据与反证审查后才可完成的可审计承诺 | closed | 2026-07-18 | 2026-07-18 | 6 |
| MILE-0007 | Butler 规则仓工程化加固：安全安装、状态自证、持续验证、可执行升级与双宿主治理收敛 | closed | 2026-07-18 | 2026-07-18 | 5 |
| MILE-0006 | Codex 双宿主兼容层：保留 Claude Code 能力，同时让规则注入、命令工作流、hooks 与部署升级在 Codex 中原生可用 | closed | 2026-07-17 | 2026-07-17 | 4 |
| MILE-0005 | butler 命令命名空间系统：把散落的散文触发词收敛成 `/butler:xxx` 一整套真实 slash 命令、全局任意项目可用（薄壳路由器 + 命名空间隔离撞名） | closed | 2026-07-14 | 2026-07-14 | 4 |
| MILE-0004 | PRD 先行 + references 版本化改版同步：给参考资料补索引/渐进读待遇 + PRD 切分/钉版 + `/prd update` 改版同步协议 | closed | 2026-07-08 | 2026-07-09 | 6 |
| MILE-0003 | 项目知识文件夹升级 + 帮手名册 + 说人话：PROJECT.md → .ai/project/ 主题文件夹 + 帮手名册（复核 / 更新说明 / 查过时）+ 讲人话扩到所有面向人输出 | closed | 2026-07-05 | 2026-07-08 | 8 |
| MILE-0002 | 自动化测试最大化 + 人测 web 回环：竭尽自动化 + JSON 驱动的 butler 驻留人测桥 + 后台等待续跑 | closed | 2026-07-02 | 2026-07-03 | 5 |
| MILE-0001 | 冷启动可恢复性与收口知识固结：补全"项目全貌"产物 + 给收口加门槛 | closed | 2026-06-30 | 2026-07-02 | 3 |

## 规则体系目录与职责

| 目录 | 规则文件数 | 职责 |
|---|---|---|
| `00_System_Prompt/` | 4 | 协作身份、总调度协议与对话输出呈现协议（`presentation-protocol.md`：方案 / 分析 / 选项类输出结论先行 + 统一标号 + 表格化 + 说人话四条对话层引用[定义真源在 `artifact-style.md §2`]）。 |
| `10_Domain_Stack_Profiles/` | 3 | 按项目类型选择的 Domain / Stack Profiles，不作为默认前置必读。 |
| `20_Workflow_Lifecycle/` | 23 | 通用需求开发 SOP 的阶段状态机、阶段交付约束、四件套书写口径与人类可读交付总结规范。 |
| `30_Quality_Gate/` | 6 | 通用质量门禁与验证策略（自动化优先纪律 + 自动道 / 人测道分道口径 + 分级置信「可靠 / 弱 / 待人」+ 代理验证）+ P4 常驻写码底线（`correction-contract` 纠错、`implementation-discipline` 最小实现）+ 供 opt-in 模式共享的定量熔断纪律（`bounded-convergence`）。 |
| `40_Context_Management/` | 11 | 长任务、多阶段任务与交接场景下的上下文治理。 |
| `50_Extension_Ideation/` | 1 | Butler 内建但 opt-in 的 Explore / Ideation 模块；用户主动探索或接受带具体阻塞理由的建议后启用，位于 P1→P5 之外。 |
| `55_Extension_ConvergenceLoop/` | 1 | 仅在 `/butler:loop` 激活时生效的 P4 高强度纠错升档；在常驻纠错契约之上叠加执行-探测-反思-修正闭环与定量熔断，熔断纪律与 `30_Quality_Gate/bounded-convergence.md` 共用。 |
| `60_Extension_CodeReview/` | 1 | 共享审查流程真源（多维评审 / 评级 / 闭环 / P5 同上下文简评）；把这套流程放进隔离上下文跑的复核帮手定义在 `62_Extension_Agents/independent-review.md`。 |
| `62_Extension_Agents/` | 3 | butler 专门 worker 的名册 + 通用规矩（唯一真源）+ 各帮手完整定义。**触发式加载、不进冷启动必读**；帮手是一份中立定义资料，用时按合同选择 fresh-context、串行或 HITL 执行，不把定义下发到项目。当前住册两帮手：复核（`independent-review`，接 P5）、Decision Work（`decision-work`，Explore 中处理已显式领取的 Decision、零项目写）；执行形态和接线以名册为准。 |
| `65_Extension_Dangerous/` | 1 | 仅在显式 `/butler:dangerous` 指令或对应语义下启用的实验性无人值守长程自治模块。 |
| `70_Extension_Preference/` | 1 | 实验性偏好探针模块。**数据回路（采集 + 蒸馏）经一次性同意后默认常驻**，**影响回路（反哺）opt-in 且仅作用于有监督工作、绝不参与 `/butler:dangerous`**；只学真人选择，外置存储、与本仓库解耦。 |
| `99_Business_Extension/` | 0 | 业务侧最高优先级约束目录。 |

## 工作流清单

- 语义入口 Router：`/butler` / `$butler-router`，不路由到自身。

| ID | Claude | Codex | 风险 | 规则真源 |
|---|---|---|---|---|
| inbox | `/butler:inbox` | `$butler-inbox` | normal | `Coder/40_Context_Management/inbox-workflow.md` |
| prd | `/butler:prd` | `$butler-prd` | normal | `Coder/40_Context_Management/references-schema.md` |
| review | `/butler:review` | `$butler-review` | normal | `Coder/60_Extension_CodeReview/review-engine.md` |
| milestone | `/butler:milestone` | `$butler-milestone` | normal | `Coder/20_Workflow_Lifecycle/milestone-schema.md` |
| upgrade | `/butler:upgrade` | `$butler-upgrade` | normal | `Coder/20_Workflow_Lifecycle/butler-upgrade.md` |
| init | `/butler:init` | `$butler-init` | normal | `Coder/20_Workflow_Lifecycle/mcv-deployment.md` |
| setup | `/butler:setup` | `$butler-setup` | normal | `Coder/20_Workflow_Lifecycle/butler-setup.md` |
| ideation | `/butler:ideation` | `$butler-ideation` | normal | `Coder/50_Extension_Ideation/ideation-engine.md` |
| preference | `/butler:preference` | `$butler-preference` | normal | `Coder/70_Extension_Preference/preference-probe-engine.md` |
| loop | `/butler:loop` | `$butler-loop` | high | `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` |
| dangerous | `/butler:dangerous` | `$butler-dangerous` | high | `Coder/65_Extension_Dangerous/dangerous-engine.md` |
| progress | `/butler:progress` | `$butler-progress` | normal | `.claude/commands/butler/progress.md` |
| iteration | `/butler:iteration` | `$butler-iteration` | normal | `Coder/20_Workflow_Lifecycle/iteration-intake.md` |

## 驻留工具清单

| 工具 | 用途 |
|---|---|
| `tools/artifact-pipeline/` | artifact-pipeline |
| `tools/butler-upgrade/` | Butler Upgrade Executor |
| `tools/codex-validators/` | Pinned Codex validators |
| `tools/context-budget/` | context-budget |
| `tools/decision-map/` | decision-map |
| `tools/decision-promotion/` | decision-promotion |
| `tools/decision-work/` | decision-work |
| `tools/delivery-selftest/` | delivery-selftest — 交付自测桥 |
| `tools/domain-contract/` | domain-contract |
| `tools/explore-dogfood/` | explore-dogfood |
| `tools/goal-assurance/` | Goal Assurance |
| `tools/handoff/` | Handoff Tool |
| `tools/inbox/` | Butler Inbox Scanner |
| `tools/iteration-intake/` | — |
| `tools/mile0009-e2e/` | MILE-0009 End-to-End |
| `tools/prd-migrate/` | PRD Migration Tool |
| `tools/prd-status/` | prd-status |
| `tools/prd-update/` | prd-update |
| `tools/project-config/` | project-config |
| `tools/state-ledger/` | state-ledger |
| `tools/verification-evidence/` | Verification Evidence |
| `tools/workspace-scope/` | Workspace Scope Tool |
