# Goal

- 按 AC-1 / AC-2 方案 A / AC-3 / AC-4 方案 α，对 Bucket A 的 4 条 Should Fix 执行最小范围修复。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 改动点 |
|---|---|---|---|
| 1 | `Coder/00_System_Prompt/logic-protocol.md` | AC-1 | 1 |
| 2 | `HUMAN_GUIDE.md` | AC-1 | 1 |
| 3 | `Coder/README.md` | AC-2 | 2（10 profile 行 + 40 激活段落） |
| 4 | `Coder/architecture-overview.md` | AC-2 | 1（§ 3 整段重写为指针） |
| 5 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md` | AC-3 | 5（标题层级） |
| 6 | `Coder/20_Workflow_Lifecycle/mcv-update.md` | AC-4 | 5（目录示例 × 2 + 说明 × 2 + 新增命名策略段） |

共 6 个文件，约 15 处 edit。

# Interface / Contract

- 引入一条**新规则**（非契约变更，仅显式化隐式约定）：热数据命名策略 — `.ai/` 根下的运行态文件统一带数字前缀；`.ai/archive/` 下的归档文件不强求前缀。
- 其余全是表述对齐，无契约变化。

# State / Boundary

- 修改仅限 6 个规则文本文件，不动 `scripts/`、`templates/`、`Coder/30_Quality_Gate/`、`Coder/10_Domain_Stack_Profiles/`、Extension 目录等。

# Design Decisions

1. **AC-1 SSOT**：`ideation-engine.md` 作为触发词权威源（无需改动），其他两处同步到 4 个词：脑暴 / 完善需求 / 想不清楚 / 还没想好。
2. **AC-2 方案 A**：README 做 SSOT。architecture-overview § 3 完全简化为指针 + 极简概念说明，"40_Context_Management 激活时机"段落的完整语义迁移到 README（吸收 "checkpoint / handoff" 这个 README 原版缺失的关键词）。
3. **AC-3**：5 个 `### N.` 章节全部升为 `## N.`，不引入其他层级调整。
4. **AC-4 方案 α**：热数据区 `CHANGELOG.md` / `BUG_LOG.md` → `01_CHANGELOG.md` / `03_BUG_LOG.md`；`INDEX.md` 保留无前缀（它不在 0/1/2/3 序列里，是索引元文件）；归档示例 `CHANGELOG_2025.md` / `BUG_LOG_v1.md` 保留不变；在 § 3 结尾追加命名策略说明段。

# Execution Steps

全部 15 个 edit 按文件分组，单次消息并发执行（不同文件之间无依赖，同文件 edit 使用精确 old_string 区分）。

## AC-1 同步触发词（2 edits）

- **`logic-protocol.md:77`**
  old: `当用户提到"脑暴"、"完善需求"、"想不清楚"或输入 \`/ideation\` 时开启。`
  new: `当用户提到"脑暴"、"完善需求"、"想不清楚"、"还没想好"或输入 \`/ideation\` 时开启。`

- **`HUMAN_GUIDE.md:114`**
  old: `| **Ideation** | \`/ideation\` 或 "脑暴"、"想不清楚" | 需求脑暴与完善 |`
  new: `| **Ideation** | \`/ideation\` 或 "脑暴"、"完善需求"、"想不清楚"、"还没想好" | 需求脑暴与完善 |`

## AC-2 确立 README 为 SSOT（2 edits）

- **`Coder/README.md` L98**（`## 读取顺序` 第 7 项）：在"与当前项目类型匹配的规则文档"后补"需先在 P1 Analysis 识别项目类型与技术栈后再启用"。
- **`Coder/README.md` L100** 段落：原"40 激活时机"升级为吸收 `checkpoint / handoff` 关键词的完整版。
- **`Coder/architecture-overview.md § 3`** 整段替换为：
  ```
  ## 3. 启用顺序

  具体读取顺序以 `README.md § 读取顺序` 为准。本文件仅负责说明三层分工的职责边界与 profile 条件生效的语义，不重复列出顺序清单，避免多处漂移。
  ```

## AC-3 mcv-deployment.md 标题层级（5 edits）

5 个独立 Edit：
- `### 0. Butler 路径发现 (Path Discovery)` → `## 0. Butler 路径发现 (Path Discovery)`
- `### 1. 落地前侦察 (Scouting)` → `## 1. 落地前侦察 (Scouting)`
- `### 2. 基础设施展开 (Scaffold)` → `## 2. 基础设施展开 (Scaffold)`
- `### 3. 规则注入 (Rule Injection)` → `## 3. 规则注入 (Rule Injection)`
- `### 4. 本地化适配 (Local Adaptation)` → `## 4. 本地化适配 (Local Adaptation)`

## AC-4 mcv-update.md 修复（5 edits）

- **L43**：目录示例 `  CHANGELOG.md` → `  01_CHANGELOG.md`
- **L45**：目录示例 `  BUG_LOG.md` → `  03_BUG_LOG.md`
- **L52**：说明 `` - `CHANGELOG.md` 只保留热数据 `` → `` - `01_CHANGELOG.md` 只保留热数据 ``
- **L54**：说明 `` - `BUG_LOG.md` 只保留仍然活跃 `` → `` - `03_BUG_LOG.md` 只保留仍然活跃 ``
- **§ 3 末尾追加命名策略段**：
  ```
  - 命名策略：热数据（`.ai/` 根下）统一保留数字前缀（`00_` / `01_` / `02_` / `03_`），与基地车部署命名一致；归档数据（`.ai/archive/` 下）按年份、版本或主题分片，命名可灵活处理，不强求前缀。
  ```

**保留简写位置**（不改）：
- `mcv-update.md:18` `` `CHANGELOG`、`BUG_LOG`、`SESSION_HANDOFF` `` — 概念枚举
- `mcv-update.md:100` `### 5.1 CHANGELOG` — 小节标题
- `mcv-update.md:102/144/153` `` `CHANGELOG` `` — 概念代词
- `mcv-update.md:132` `### 5.3 BUG_LOG` — 小节标题
- `mcv-update.md:134/144/154/178` `` `BUG_LOG` `` — 概念代词

**保留归档示例**（不改）：
- `mcv-update.md:41-42` `CHANGELOG_2025.md` / `BUG_LOG_v1.md` — 归档文件（按方案 α，不强求前缀）

# Verification Plan

- **AC-1**：`grep -nE '脑暴.*完善需求.*想不清楚.*还没想好' Coder/00_System_Prompt/logic-protocol.md Coder/50_Extension_Ideation/ideation-engine.md HUMAN_GUIDE.md` — 三个文件都匹配，关键词顺序一致。
- **AC-2**：`grep -n '## 3\.' Coder/architecture-overview.md` 下面紧接的内容为指针而非清单；`grep -n '^[0-9]\. ' Coder/architecture-overview.md` 无输出（§ 3 下无编号列表）。
- **AC-3**：`grep -nE '^### [0-9]' Coder/20_Workflow_Lifecycle/mcv-deployment.md` 返回空。
- **AC-4**：
  - `grep -nE '^\s+(CHANGELOG\.md|BUG_LOG\.md)$' Coder/20_Workflow_Lifecycle/mcv-update.md` 无输出（目录示例热数据区已改为带前缀）；
  - `grep -n '命名策略' Coder/20_Workflow_Lifecycle/mcv-update.md` 命中新增命名策略段。
- 完整 diff `git diff` 确认仅涉及 6 个文件，无无关改动。

# Risks / Open Questions

- **风险 1**：architecture-overview § 3 大幅重写（从 14 行缩成 3 行），可能让原有读者产生"内容丢失"的错觉。缓解：新版本明确指针"以 README § 读取顺序为准"，迁移链路清晰。
- **风险 2**：AC-4 目录示例里 `INDEX.md` 不加前缀与其他带前缀的热数据视觉不一致。合理化：INDEX 是元数据文件（索引/地图），不参与 00-03 运行态文件序列，保持无前缀更能体现其"元"属性。这个决策应在 `mcv-update.md` 的命名策略段落里隐含体现（通过"00_ / 01_ / 02_ / 03_" 的枚举明示只有这四种带前缀）。
- **开放问题**：无。
