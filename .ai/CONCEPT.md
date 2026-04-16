# Goal

- 修复 Butler 规则全流程审计中发现的 7 条 Must Fix 问题，消除自相矛盾、产物链断点与格式损坏，让规则仓库的主链路（产物链 + 扩展模式 + 维护阈值）重新自洽。

# Current Understanding

- 本任务是对 butler 规则仓库本身的维护（meta-修改），属于 dogfooding。
- 7 条 Must Fix 均已在审计报告中定位到 `文件:行号`。
- 其中 2 条（Ideation→P2 断链、SESSION_HANDOFF 命名）存在多个候选方案，需在 P2 AC_LIST 中请用户拍板；其余 5 条修改路径明确，无分支。
- 不需要部署 `.ai/` 基地车全量结构（butler 自己只需 P1/P2/P3/P5 产物即可承载本次维护任务）。

# Constraints

- 显性约束：
  - 不破坏三层分工（SOP Core / Domain Profiles / Business Extension）。
  - 不破坏现有产物链（CONCEPT → AC_LIST → TECH_PLAN → VERIFY_REPORT）。
  - 修复后 `Coder/README.md`、`architecture-overview.md`、`HUMAN_GUIDE.md`、`templates/` 需保持相互一致。
  - 遵循 `CLAUDE.md` 项目约束：新增规则必须在 Coder/README.md 注册、frontmatter 必须有 audience/scope、规则之间用文件名引用。
- 隐性约束：
  - Markdown 渲染兼容性（frontmatter、列表、标题层级）。
  - 修复本身不引入新规则文件，仅做表述修正与字段补充。

# Impact Scope

直接修改（最多 8 个文件，具体以 AC-1 / AC-4 方案选择为准）：

- `Coder/README.md`（AC-3 列表编号）
- `Coder/00_System_Prompt/identity.md`（AC-2 frontmatter）
- `Coder/00_System_Prompt/logic-protocol.md`（AC-2 frontmatter）
- `Coder/20_Workflow_Lifecycle/lifecycle.md`（AC-1 方案相关）
- `Coder/20_Workflow_Lifecycle/acceptance-schema.md`（AC-1 方案相关）
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`（AC-4 命名、AC-5 时机）
- `Coder/20_Workflow_Lifecycle/mcv-update.md`（AC-4 命名）
- `Coder/20_Workflow_Lifecycle/maintenance-boundaries.md`（AC-6 BUG_LOG、AC-7 CHANGELOG）
- `Coder/50_Extension_Ideation/ideation-engine.md`（AC-1 方案相关）
- `Coder/40_Context_Management/handoff-spec.md`（AC-4 命名）
- `Coder/40_Context_Management/context-persistence.md`（AC-4 命名）
- `HUMAN_GUIDE.md`（AC-4 命名，如选方案 B）

不影响：`Coder/30_Quality_Gate/`、`Coder/10_Domain_Stack_Profiles/`、`Coder/55_Extension_RalphLoop/`、`Coder/60_Extension_CodeReview/`、`scripts/`、`templates/`。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库（非代码工程）。
- 未命中任何 Domain Profile（不属于 Vue 3 / TypeScript / 前端构建）。
- 仅按通用 SOP 推进。

# Open Questions

- **AC-1** Ideation→P2 断链修复：三个候选方案，需用户拍板（见 AC_LIST.md）。
- **AC-4** SESSION_HANDOFF 命名统一：两个候选方案，需用户拍板（见 AC_LIST.md）。
