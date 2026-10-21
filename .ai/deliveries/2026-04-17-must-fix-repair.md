# Butler 规则仓库 Must Fix 修复交付总结

> 日期：2026-04-17
> 任务：修复 Butler 规则全流程审计发现的 7 条 Must Fix 问题
> 状态：已完成，可交付

## 本次交付目标

修复 Butler 规则仓库全流程审计中发现的 7 条阻断级问题，消除自相矛盾、产物链断点、格式损坏与命名不一致，让规则仓库的主链路（产物链 + 扩展模式 + 维护阈值）重新自洽。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | Ideation→P2 产物链断链 | `ideation-engine.md` 明确收敛后必须同步结晶 `.ai/CONCEPT.md`，`lifecycle.md` P2 单入口约定保持不变 |
| 2 | `identity.md` 与 `logic-protocol.md` 缺 frontmatter | 补齐 `title / audience / scope` 三字段 |
| 3 | `Coder/README.md` 列表编号损坏（`95 - / 96 -` 异常数字） | 全部改为普通 `-` bullet |
| 4 | `SESSION_HANDOFF.md` 命名在规则仓中混用 | 统一为 `02_SESSION_HANDOFF.md`（15 个文件共 25 处 edit），与 `00/01/03` 前缀风格一致 |
| 5 | `mcv-deployment.md` 中 `00_IDEATION.md` 时机自相矛盾 | 改为"部署阶段仅创建目录，运行态文件按需产生"的统一口径 |
| 6 | `maintenance-boundaries.md` BUG_LOG 触发阈值缺 Ralph-Loop RCA | 在 BUG_LOG 行补充该触发条目 |
| 7 | `maintenance-boundaries.md` CHANGELOG 触发阈值缺 Review 发现 | 在 CHANGELOG 行补充"Review 审计产出的 Should Fix 条目" |

## 关键变更 / 用户可感知变化

- **Ideation 路径现在明确对接主产物链**：`/ideation` 模式收敛后强制结晶 `.ai/CONCEPT.md`，后续按标准 P2 流程推进，不再依赖对话记忆或额外分支规则。
- **`.ai/` 下的文件命名统一带数字前缀**：规则文本中所有对该文件的引用都用 `02_SESSION_HANDOFF.md`，新人读基地车目录一眼可辨认运行态文件。
- **部署语义更精确**：基地车部署只建目录、不预置 `.md` 文件；所有运行态文件在触发对应条件时按需产生。
- **维护阈值更完整**：BUG_LOG 和 CHANGELOG 的强制更新时机现在覆盖 Review 发现和 Ralph-Loop 熔断两类之前缺口。
- **规则自我约束闭合**：`CLAUDE.md` 要求的 frontmatter 约束现在 100% 满足率（26/26 规则文件）。

## 高层影响范围

**直接修改的 15 个文件**：

- 入口：`Coder/README.md`、`HUMAN_GUIDE.md`
- System Prompt：`Coder/00_System_Prompt/identity.md`、`logic-protocol.md`
- Workflow Lifecycle：`lifecycle.md`、`mcv-deployment.md`、`mcv-update.md`、`maintenance-boundaries.md`、`progressive-handoff.md`、`verify-schema.md`、`delivery-summary.md`
- Context Management：`context-persistence.md`、`handoff-spec.md`、`mode-switch.md`
- Extension：`Coder/50_Extension_Ideation/ideation-engine.md`

**未影响**：`30_Quality_Gate/`、`10_Domain_Stack_Profiles/`、`55_Extension_RalphLoop/`、`60_Extension_CodeReview/`、`scripts/`、`templates/`、`Learner/`、`Composer/`。

**不引入新规则文件、不调整目录结构、不修改运行时行为**。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `grep -l '^---$' Coder/00_System_Prompt/*.md` | 两个文件 ✅ |
| `grep -nE '^[0-9]+ -' Coder/README.md` | 无输出 ✅ |
| 全仓扫描不带前缀的 `SESSION_HANDOFF.md` | 0 处 ✅ |
| 全仓扫描带前缀的 `02_SESSION_HANDOFF.md` | 29 处（全部 `.md` 引用） ✅ |
| 保留简写（概念名，无 `.md`） | 4 处，全部符合预期 ✅ |
| `grep 'Ralph-Loop' maintenance-boundaries.md` | 命中 BUG_LOG 行 ✅ |
| `grep 'Review\|Should Fix' maintenance-boundaries.md` | 命中 CHANGELOG 行 ✅ |
| 通读 `ideation-engine.md § 4` 与 `lifecycle.md P2` 闭合 | ✅ |
| 通读 `mcv-deployment.md § 2` 时机矛盾消除 | ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 🟡 新暴露的 Should Fix（超出本轮范围）

`mcv-update.md § 3` 升级后的目录结构示例出现风格裂痕：`02_SESSION_HANDOFF.md` 带前缀，但同一目录示例中的 `CHANGELOG.md` / `BUG_LOG.md` 无前缀。

**根因**：Butler 规则仓的部署时命名（带前缀）与升级后命名（无前缀）策略不统一。本轮严格执行 AC-4 方案 A 让这一裂痕更明显。

**建议后续独立工单处理**，候选方案：
- α：升级后也保留前缀（改 `mcv-update.md § 3` 示例）
- β：升级后统一去前缀（AC-4 方案需重新讨论）

### ℹ️ 未处理的原审计报告条目

本轮只处理了 7 条 Must Fix；审计报告中还有：
- 10 条 Should Fix（建议分批处理）
- 4 条 Nice to Have（可选）

详见审计对话记录或重跑审计。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`、`.ai/VERIFY_REPORT.md`
- 相关规则：
  - `Coder/20_Workflow_Lifecycle/lifecycle.md`（P1-P5 状态机）
  - `Coder/50_Extension_Ideation/ideation-engine.md`（AC-1 修复点）
  - `Coder/20_Workflow_Lifecycle/maintenance-boundaries.md`（AC-6 / AC-7 修复点）
  - `Coder/40_Context_Management/handoff-spec.md`（AC-4 影响的核心规范文件）
