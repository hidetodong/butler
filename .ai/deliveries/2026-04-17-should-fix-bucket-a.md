# Butler 规则仓库 Should Fix Bucket A 交付总结

> 日期：2026-04-17
> 任务：修复 Should Fix Bucket A（命名与读取顺序一致性）4 条问题
> 状态：已完成，可交付

## 本次交付目标

修复 Butler Should Fix 清单中 Bucket A 的 4 条命名与读取顺序一致性问题，降低规则文档跨文件漂移风险，把隐式约定显式化。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | `/ideation` 触发词在 logic-protocol / ideation-engine / HUMAN_GUIDE 三处不一致 | 以 `ideation-engine.md` 为 SSOT，另两处同步到 4 个触发词 |
| 2 | `Coder/README.md` 读取顺序与 `architecture-overview.md § 3` 启用顺序冗余且有微差 | README 做 SSOT，吸收原 architecture-overview 的 checkpoint/handoff 补充；architecture-overview § 3 简化为 3 行指针 |
| 3 | `mcv-deployment.md` 5 个章节用 `### N.`，与其他规则文件 `## N.` 不一致 | 全部升级为 `## N.` |
| 4 | `mcv-update.md § 3` 升级后目录示例风格裂痕（CHANGELOG/BUG_LOG 无前缀，SESSION_HANDOFF 带前缀） | 热数据区 `CHANGELOG.md` → `01_CHANGELOG.md`、`BUG_LOG.md` → `03_BUG_LOG.md`；归档示例保留不变；新增命名策略段作为显式规则 |

## 关键变更 / 用户可感知变化

- **Ideation 触发词四元组稳定**：`"脑暴"、"完善需求"、"想不清楚"、"还没想好"` 在 AI 规则、入口文件、用户指南三处完全一致。
- **读取顺序只认一个 SSOT**：今后修改读取顺序只需改 `Coder/README.md § 读取顺序`，architecture-overview 不再承担同步负担。
- **`mcv-deployment.md` 标题层级对齐仓库通用风格**，Markdown 渲染视觉统一。
- **显式化命名策略**：`.ai/` 热数据带数字前缀、`.ai/archive/` 归档灵活 —— 这个此前隐式的惯例现已作为规则正文存在于 `mcv-update.md § 3`。

## 高层影响范围

**直接修改 6 个规则文件**：

- `Coder/00_System_Prompt/logic-protocol.md`
- `Coder/README.md`
- `Coder/architecture-overview.md`
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`
- `Coder/20_Workflow_Lifecycle/mcv-update.md`
- `HUMAN_GUIDE.md`

**未影响**：`00_System_Prompt/identity.md`、`10_Domain_Stack_Profiles/`、`30_Quality_Gate/`、`40_Context_Management/`、`50/55/60_Extension_*/`、`templates/`、`scripts/`、`Learner/`、`Composer/`、`20_Workflow_Lifecycle/` 的其他 schema / lifecycle 文件。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `grep -cE '脑暴.*完善需求.*想不清楚.*还没想好'` 三文件 | 均命中 1 次 ✅ |
| `grep -nE '^[0-9]\.' architecture-overview.md` | 零匹配（§ 3 已去清单） ✅ |
| `grep -n 'checkpoint 或 handoff' README.md` | L100 命中 ✅ |
| `grep -nE '^### [0-9]' mcv-deployment.md` | 零匹配 ✅ |
| `grep -nE '^## [0-9]' mcv-deployment.md` | 5 行命中（L9/19/28/63/72） ✅ |
| `grep -nE '^\s\s(CHANGELOG\.md\|BUG_LOG\.md)$' mcv-update.md` | 零匹配 ✅ |
| `grep -n '命名策略' mcv-update.md` | L56 命中 ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 🔍 Nice to Have（可选，不阻断）

- `architecture-overview.md § 3` 简化后只剩 3 行，结构略空旷。可考虑后续合并到 § 2 的"三层分工"中，或改名为"与 README 读取顺序的关系"。本次保留现有结构，降低本轮重构面。

### 未处理的 Should Fix（7 条）

- Bucket B（产物链字段补全，3 条）
- Bucket C（Mode 术语消歧，1 条）
- Bucket D（模板重复消除，1 条）
- Bucket E（setup.sh 跨平台 + skill 回退，2 条）

建议下一步优先推进 Bucket E（低风险、独立性强）。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `Coder/README.md § 读取顺序`（本轮确立的 SSOT）
  - `Coder/20_Workflow_Lifecycle/mcv-update.md § 3`（新增命名策略段）
- 上一轮交付：`deliveries/2026-04-17-must-fix-repair.md`（Must Fix 修复）
