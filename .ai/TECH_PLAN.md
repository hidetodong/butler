# Goal

- 按 AC-1 方案 A、AC-4 方案 A 与其余 5 条 Must Fix，对 butler 规则仓库执行最小范围、最高一致性的文本修复。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 修改点数 |
|---|---|---|---|
| 1 | `Coder/50_Extension_Ideation/ideation-engine.md` | AC-1 | 1 |
| 2 | `Coder/00_System_Prompt/identity.md` | AC-2 | 1（补 frontmatter） |
| 3 | `Coder/00_System_Prompt/logic-protocol.md` | AC-2 + AC-4 | 2 |
| 4 | `Coder/README.md` | AC-3 + AC-4 | 1（列表编号 + 顺便改 SESSION_HANDOFF） |
| 5 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md` | AC-5 | 1 |
| 6 | `Coder/20_Workflow_Lifecycle/maintenance-boundaries.md` | AC-4 + AC-6 + AC-7 | 2（CHANGELOG + BUG_LOG 两行，顺便 SESSION_HANDOFF） |
| 7 | `Coder/20_Workflow_Lifecycle/lifecycle.md` | AC-4 | 2 |
| 8 | `Coder/20_Workflow_Lifecycle/mcv-update.md` | AC-4 | 3（目录结构、§ 5.2、§ 7） |
| 9 | `Coder/20_Workflow_Lifecycle/verify-schema.md` | AC-4 | 1 |
| 10 | `Coder/20_Workflow_Lifecycle/delivery-summary.md` | AC-4 | 1 |
| 11 | `Coder/20_Workflow_Lifecycle/progressive-handoff.md` | AC-4 | 3 |
| 12 | `Coder/40_Context_Management/handoff-spec.md` | AC-4 | 4（frontmatter + H1 + 两处正文） |
| 13 | `Coder/40_Context_Management/context-persistence.md` | AC-4 | 5 |
| 14 | `Coder/40_Context_Management/mode-switch.md` | AC-4 | 1 |
| 15 | `HUMAN_GUIDE.md` | AC-4 | 2 |

共 15 个文件，约 30 处 edit。

# Interface / Contract

本次修复**不引入新字段、新文件、新目录**。涉及的"契约"变更仅限文件名统一：

- **命名契约**：`SESSION_HANDOFF.md` → `02_SESSION_HANDOFF.md` 作为规范唯一文件名。
- **概念名保留策略**：在表格列名、小节标题、概念枚举中（如 `mcv-update.md § 5.2` 标题），`SESSION_HANDOFF` 作为简写概念名保留，**不**加 `02_` 前缀；只有涉及具体文件路径（带 `.md` 后缀）的引用才统一带前缀。

# State / Boundary

- **修改范围限于规则文本**，不涉及 `scripts/setup.sh`、`templates/`（两个模板目前已用 `02_` 前缀，AC-4 无额外修改）。
- **不涉及 `.claude/worktrees/` 下的历史快照**（由 git ignore 机制管理，非本轮工作对象）。
- **不修改 `.ai/CONCEPT.md` 和 `.ai/AC_LIST.md`**（仅作产物链锚点，保留原貌）。

# Design Decisions

1. **AC-1 方案 A**：在 `ideation-engine.md § 4` 增加一条"收敛后必须同步结晶 `.ai/CONCEPT.md`"，保持 `lifecycle.md` 的 P2 单入口约定不变。
2. **AC-4 方案 A**：统一 `02_SESSION_HANDOFF.md`，与基地车其他运行态文件（`00/01/03`）命名风格一致。
3. **AC-5**：将 `mcv-deployment.md § 2` 的"**运行态文件**（部署时初始化，随会话更新）"改为"**运行态文件**（按需产生，随会话更新）"，并在 § 2 开头明确"部署时仅创建 `.ai/` 与 `deliveries/` 目录，文件按任务推进或触发条件按需产生"。**同时删除** `00_IDEATION.md` 条目中"仅在 /ideation 模式激活后产生"的重复说明（改为与其他按需文件统一口径，仅说明用途）。
4. **AC-6、AC-7**：只在 `maintenance-boundaries.md` 第一个表格补充触发条目，不动其他段落。

# Execution Steps

按依赖顺序执行，避免中间态：

## Phase 1 — 无依赖的原子修复（并行 6 个 Edit）

- Step 1: `identity.md` 补 frontmatter（AC-2）
- Step 2: `logic-protocol.md` 补 frontmatter（AC-2）
- Step 3: `ideation-engine.md § 4` 追加 CONCEPT.md 结晶规则（AC-1）
- Step 4: `mcv-deployment.md § 2` 修正 00_IDEATION.md 时机矛盾（AC-5）
- Step 5: `maintenance-boundaries.md` 表格 CHANGELOG / BUG_LOG 行补充触发（AC-6、AC-7）
- Step 6: `Coder/README.md` 列表编号修复（AC-3）

## Phase 2 — SESSION_HANDOFF 批量重命名（AC-4）

按文件逐一 Edit。总计涉及 13 个文件，每处只改"带 `.md` 后缀的文件路径引用"。改动点逐一列出：

| 文件 | 行号 | 原文片段 | 新文本片段 |
|---|---|---|---|
| `HUMAN_GUIDE.md` | 148 | `SESSION_HANDOFF.md` | `02_SESSION_HANDOFF.md` |
| `HUMAN_GUIDE.md` | 151 | `请生成 SESSION_HANDOFF.md` | `请生成 02_SESSION_HANDOFF.md` |
| `Coder/README.md` | 110 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `Coder/00_System_Prompt/logic-protocol.md` | 19 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `lifecycle.md` | 149 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `lifecycle.md` | 165 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `maintenance-boundaries.md` | 19 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `mcv-update.md` | 44（目录结构）| `SESSION_HANDOFF.md` | `02_SESSION_HANDOFF.md` |
| `mcv-update.md` | 53 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `mcv-update.md` | 165 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `verify-schema.md` | 58 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `delivery-summary.md` | 89 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `progressive-handoff.md` | 13 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `progressive-handoff.md` | 37 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `progressive-handoff.md` | 58 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `handoff-spec.md` | 4（frontmatter）| `SESSION_HANDOFF.md` 的唯一结构定义与字段约束 | `02_SESSION_HANDOFF.md` 的唯一结构定义与字段约束 |
| `handoff-spec.md` | 7（H1）| `# SESSION_HANDOFF.md 格式契约` | `# 02_SESSION_HANDOFF.md 格式契约` |
| `handoff-spec.md` | 9 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `handoff-spec.md` | 13 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `context-persistence.md` | 17 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `context-persistence.md` | 105 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `context-persistence.md` | 115 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `context-persistence.md` | 116 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `context-persistence.md` | 122 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |
| `mode-switch.md` | 70 | `` `SESSION_HANDOFF.md` `` | `` `02_SESSION_HANDOFF.md` `` |

**保留简写的位置（不改）**：
- `maintenance-boundaries.md:16` 表格列名 `**SESSION_HANDOFF**`
- `mcv-update.md:18` "如何区分 `CHANGELOG`、`BUG_LOG`、`SESSION_HANDOFF` 的迁移方式"（概念枚举）
- `mcv-update.md:115` `### 5.2 SESSION_HANDOFF`（小节标题）
- `mcv-update.md:117` "`SESSION_HANDOFF` 永远不应演化为长历史日志"（概念代词）

这些位置在语义上指代**概念名**而非**文件路径**，保留简写更易读。

# Verification Plan

- **AC-1**：通读 `ideation-engine.md § 4`，语义闭合，且在 `acceptance-schema.md § 6` 和 `lifecycle.md P2` 不需要任何补丁即可与之自洽。
- **AC-2**：`grep -l '^---$' Coder/00_System_Prompt/*.md` 返回两个文件。
- **AC-3**：`grep -E '^[0-9]+ -' Coder/README.md` 无输出（不再有 `95 - / 96 -` 这类行）。
- **AC-4**：`grep -rn 'SESSION_HANDOFF\.md' Coder/ HUMAN_GUIDE.md` 所有命中行都是 `02_SESSION_HANDOFF.md`（带前缀）；不带前缀的 `SESSION_HANDOFF.md` 零命中。
- **AC-5**：通读 `mcv-deployment.md § 2` 开头与 `00_IDEATION.md` 条目描述，"部署时初始化"与"仅在 /ideation 激活后产生"的表面矛盾被消除。
- **AC-6**：`grep -n 'Ralph-Loop 熔断' Coder/20_Workflow_Lifecycle/maintenance-boundaries.md` 命中 BUG_LOG 行。
- **AC-7**：`grep -n 'Review' Coder/20_Workflow_Lifecycle/maintenance-boundaries.md` 命中 CHANGELOG 行。

# Risks / Open Questions

- **风险 1**：批量 SESSION_HANDOFF 改名可能漏掉某处非标准引用。**缓解**：P5 用 grep 全仓扫描验证。
- **风险 2**：`handoff-spec.md` H1 标题 `# 02_SESSION_HANDOFF.md 格式契约` 带数字前缀读起来略怪。**缓解**：可接受，为了命名一致性牺牲一点标题美观度；若后续觉得突兀，可把 H1 改为 `# 交接文件格式契约`（更抽象），单独作为 Nice to Have 处理，不在本轮范围。
- **风险 3**：`.ai/CONCEPT.md` 和 `.ai/AC_LIST.md` 本身包含 `SESSION_HANDOFF` 字样，不改动（产物锚点原貌保留），grep 验证时需要排除 `.ai/`。
- **开放问题**：无。
