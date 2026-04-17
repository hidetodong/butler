# Goal

- 按方案 α（最小必填 2 个字段）新建 `local-constraints-schema.md`，让基地车部署产物链对称；同步更新 `mcv-deployment.md § 4` 与 `Coder/README.md`。

# Files / Modules to Change

| # | 文件 | 动作 | 改动点 |
|---|---|---|---|
| 1 | `Coder/20_Workflow_Lifecycle/local-constraints-schema.md` | Write（新建） | 完整 schema 文件 |
| 2 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 4` | Edit | 1（追加 schema 指针） |
| 3 | `Coder/README.md` | Edit | 2（目录结构 + "其中："说明列表） |

共 3 个文件，4 处改动（1 new + 3 edit）。

# Interface / Contract

- **新 schema 文件**：位置 `Coder/20_Workflow_Lifecycle/`，命名 `local-constraints-schema.md`，与其他四个 schema 风格一致。
- **5 个字段**（2 必填 + 3 可选）：
  - 必填：`Project Type`、`Active Profiles`
  - 可选：`Local Constraints`、`Scope Exceptions`、`External References`
- **frontmatter**：`title: 本地化约束模板` / `audience: AI / 开发者` / `scope: .ai/local-constraints.md 的字段定义、编写口径与最小模板`。
- **五节结构**：目标 / 交付约定 / 标准模板 / 编写规则 / 与执行流程的关系。
- **mcv-deployment § 4 契约**：现有部署语义不变，仅追加指向新 schema 的指针句。
- **向下兼容**：旧 local-constraints.md 可逐步迁移，不阻断现有部署。

# State / Boundary

- 不动其他 schema（concept / acceptance / tech-plan / verify）。
- 不动 lifecycle / mcv-update / maintenance-boundaries / context-persistence / role-switch。
- 不修改 `Coder/README.md` 的"读取顺序"主序列（schema 文件不进主序列；参照其他 schema 的处理方式）。

# Design Decisions

1. **文件位置**：放 `20_Workflow_Lifecycle/` 下，与其他 4 个 schema 同目录。local-constraints 虽然不是 P1-P5 某阶段产物，但它是基地车部署阶段产物，mcv-deployment 也在这个目录下，归属逻辑一致。
2. **命名风格**：`local-constraints-schema.md`（与 `concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 完全对齐）。
3. **字段英文 + 中文说明**：英文字段名便于 AI 识别（和其他 schema 一致），中文说明便于人类。
4. **可选字段三选三保留（不砍）**：Local Constraints / Scope Exceptions / External References 各有独立用途，用不上可省略（方案 α 允许），但保留槽位让 AI 在需要时一眼找到落位。
5. **Coder/README.md 同步**：按 `CLAUDE.md` 第 3 条项目约束（新增规则文件必须在 Coder/README.md 注册），加入目录结构 + "其中："说明列表。

# Execution Steps

## Step 1 — Write 新文件 `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`

内容：

```markdown
---
title: 本地化约束模板
audience: AI / 开发者
scope: .ai/local-constraints.md 的字段定义、编写口径与最小模板
---

# Local Constraints Schema

## 1. 目标

用于记录当前项目相对于 butler 通用 SOP 的本地化适配：启用了哪些 profile、有哪些项目特有的放宽或收紧、哪些区域例外、关联的外部资源指针。

它不是规则复制器 —— 通用规则继续从 butler 仓读取；`.ai/local-constraints.md` 只记录"本项目与通用 SOP 的差异"。

## 2. 交付约定

- 必须产出：`.ai/local-constraints.md`
- 产出时机：基地车部署的 `mcv-deployment.md § 4 本地化适配` 步骤
- 必填字段：`Project Type`、`Active Profiles`
- 可选字段：`Local Constraints`、`Scope Exceptions`、`External References`

## 3. 标准模板

​```md
# Project Type
- 项目类型描述（Web 应用 / CLI / 库 / 规则仓等）
- 主要语言、框架与构建工具

# Active Profiles
- 命中的 Domain / Stack Profiles，按 `10_Domain_Stack_Profiles/` 下实际文件列出
- 若未命中任何 profile，显式写"无，仅按通用 SOP"

# Local Constraints
- 本项目相对于通用 SOP 的放宽或收紧
- 每条附一句原因

# Scope Exceptions
- 不受某类通用规则约束的目录或文件
- 每条附适用的例外规则与原因

# External References
- 外部资源指针（API 文档平台、设计稿、issue tracker 等）
- 此处仅做高层指针；实际参考资料提取产物在 `.ai/references/` 下
​```

## 4. 编写规则

- **不复制通用规则**：通用 SOP 继续从 butler 仓读取，`local-constraints.md` 只记"与通用 SOP 的差异"。
- **放宽/收紧必须附原因**：例如"`/legacy` 目录允许 `any`，原因：旧代码迁移中，阶段性降低类型门禁"。
- **引用而非复制**：profile 用文件名引用（如 `typescript-rules`），不复制 profile 内容。
- **适度松散**：可选字段无内容时可省略；`Active Profiles` 未命中 profile 时写"无"，不强行凑内容。
- **更新而非追加**：任务执行中发现新 local 约束或例外时应回到此文件更新，不得仅在对话中声明。

## 5. 与执行流程的关系

- **基地车部署时**：按 `mcv-deployment.md § 4 本地化适配` 生成初版，必填字段须完整。
- **任务执行中**：若发现新 local 约束或例外区域，应回到此文件更新，再继续推进。
- **P2 AC_LIST / P3 TECH_PLAN**：若任务命中某 local 约束，相关 AC / Design Decisions 应显式引用本文件中的对应条目。
- **P5 VERIFY_REPORT**：`Gate Coverage` 的 Active Profiles / Tech Plan Alignment 子项验证时，应与本文件的 Active Profiles / Local Constraints 对齐。
```

> 注：上述模板里的代码块栅栏用了零宽 `​` 占位，实际 Write 时用标准三反引号 ` ``` ` 即可。我在 P4 执行时用标准 markdown 代码块语法。

## Step 2 — Edit `mcv-deployment.md § 4`

**old**:
```
## 4. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`。
- **逻辑：** 不要复制通用规则，而是通过"指针"引用。例如："本项目遵循通用需求开发 SOP，并启用 TypeScript profile；针对 `/legacy` 目录下的旧代码，允许局部放宽类型检查。"
```

**new**:
```
## 4. 本地化适配 (Local Adaptation)

- 生成 `.ai/local-constraints.md`，字段定义与最小模板参考 `local-constraints-schema.md`。
- **逻辑：** 不要复制通用规则，而是通过"指针"引用。例如："本项目遵循通用需求开发 SOP，并启用 TypeScript profile；针对 `/legacy` 目录下的旧代码，允许局部放宽类型检查。"
```

## Step 3 — Edit `Coder/README.md` 目录结构

在目录结构块中，`20_Workflow_Lifecycle` 目录下 `verify-schema.md` 之后加入 `local-constraints-schema.md`。

**old**（目录结构中的片段）:
```
    concept-schema.md
    acceptance-schema.md
    tech-plan-schema.md
    verify-schema.md
    delivery-summary.md
```

**new**:
```
    concept-schema.md
    acceptance-schema.md
    tech-plan-schema.md
    verify-schema.md
    local-constraints-schema.md
    delivery-summary.md
```

## Step 4 — Edit `Coder/README.md` "其中：" 说明列表

在该段列出各文件角色的位置（现有对 schema 四合一说明之后），加入新 schema 的说明。

**old**:
```
- `20_Workflow_Lifecycle/concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 分别定义 P1 / P2 / P3 / P5 的必须产物、必填字段与交付模板。
- `20_Workflow_Lifecycle/delivery-summary.md` 负责完整交付后的人类可读交付总结规范。
```

**new**:
```
- `20_Workflow_Lifecycle/concept-schema.md` / `acceptance-schema.md` / `tech-plan-schema.md` / `verify-schema.md` 分别定义 P1 / P2 / P3 / P5 的必须产物、必填字段与交付模板。
- `20_Workflow_Lifecycle/local-constraints-schema.md` 定义 `.ai/local-constraints.md` 的字段与最小模板，在基地车部署的本地化适配步骤产出。
- `20_Workflow_Lifecycle/delivery-summary.md` 负责完整交付后的人类可读交付总结规范。
```

# Verification Plan

- **G-1 新 schema 文件**：
  - `ls Coder/20_Workflow_Lifecycle/local-constraints-schema.md` 存在。
  - `grep -c '^---$' local-constraints-schema.md` = 2（frontmatter 两条分隔线）。
  - `grep -nE '^## [0-9]\.' local-constraints-schema.md` 命中 5 章（目标 / 交付约定 / 标准模板 / 编写规则 / 与执行流程的关系）。
  - `grep -nE '^# (Project Type|Active Profiles|Local Constraints|Scope Exceptions|External References)' local-constraints-schema.md` 命中 5 字段。
- **G-2 mcv-deployment § 4 指针**：`grep -n 'local-constraints-schema' Coder/20_Workflow_Lifecycle/mcv-deployment.md` 命中 § 4 范围。
- **G-3 Coder/README.md 注册**：
  - `grep -n 'local-constraints-schema' Coder/README.md` 命中 2 处（目录结构 + "其中："说明）。
- `git status` 显示 1 新文件 + 2 个 M 文件（除 `.ai/` 产物链 + deliveries）。

# Risks / Open Questions

- **风险 1**：schema 可选字段三个中有无冗余（Scope Exceptions 与 Local Constraints 边界）。缓解：Local Constraints 聚焦"本项目相对通用 SOP 的放宽/收紧"，Scope Exceptions 聚焦"不受某类通用规则约束的目录或文件"；前者是**规则层面**的差异，后者是**代码位置层面**的差异。边界清晰。
- **风险 2**：新 schema 发布后已部署项目的 local-constraints.md 不强制回填。后续若 AI 在某项目检测到 local-constraints 缺字段，应主动建议迁移但不阻断。（本轮不落地迁移规则，避免扩张。）
- **开放问题**：无。
