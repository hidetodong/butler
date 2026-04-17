# Goal

- 修复 Bucket G（local-constraints schema 新增）1 条 Nice to Have。

# In Scope

- 新建 `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`。
- `mcv-deployment.md § 4 本地化适配` 加一个指向新 schema 的指针。
- `Coder/README.md` 目录结构与读取顺序注册新文件。

# Out of Scope

- Bucket H（N-6 Domain_Stack_Profiles 目录重组）。
- 其他 schema 的字段调整。
- 不修改 `mcv-deployment.md § 4` 的部署语义本身。

# Acceptance Checklist

- [ ] **G-1** 新建 `local-constraints-schema.md`，字段集按拍板方案；含 frontmatter（audience / scope）与完整五节结构（目标 / 交付约定 / 标准模板 / 编写规则 / 与执行流程的关系），风格与其他 schema 一致
- [ ] **G-2** `mcv-deployment.md § 4` 在现有描述后追加指针句，引用新 schema
- [ ] **G-3** `Coder/README.md` 目录结构包含新文件；读取顺序不变（schema 是被产物引用的模板，不进读取顺序主序列）

# Verification Method

- **G-1**：`ls Coder/20_Workflow_Lifecycle/local-constraints-schema.md` 存在；`grep -n '^---$' local-constraints-schema.md` 返回 2 行 frontmatter；`grep -nE '^## [0-9]\.' local-constraints-schema.md` 至少 5 章（目标 / 交付约定 / 标准模板 / 编写规则 / 与执行流程的关系）。
- **G-2**：`grep -n 'local-constraints-schema' mcv-deployment.md` 命中。
- **G-3**：`grep -n 'local-constraints-schema' Coder/README.md` 命中目录结构块。

# Open Questions / Risks

## ❓ 待拍板 - G-1 必填字段集

### 方案 α（推荐）— 最小必填：2 个字段

- 必填：
  - `Project Type`（项目类型、主要语言与框架）
  - `Active Profiles`（命中的 Domain / Stack Profiles，按 `10_Domain_Stack_Profiles/` 下实际文件列出；未命中时写"无，仅按通用 SOP"）
- 可选：
  - `Local Constraints`（本项目相对通用 SOP 的放宽 / 收紧，每条附原因）
  - `Scope Exceptions`（不受某类通用规则约束的目录或文件）
  - `External References`（高层指针：Confluence / 设计平台 / issue tracker 等）
- **理由**：local-constraints 本质是"差异记录"，新项目接入时未必有 local 约束或例外；让 Local Constraints 等三项保持可选，避免 AI 硬填无意义内容。

### 方案 β — 中等必填：3 个字段

- 必填多加 `Local Constraints`（至少填一条"无"或"本项目暂无本地化约束，完全按通用 SOP"）。
- **理由**：强迫 AI 在部署时主动思考"有没有 local 约束"。
- **缺点**：多数小项目会填"无"，字段膨胀。

### 方案 γ — 严格必填：5 个字段全部必填

- 不推荐 — local-constraints 应偏轻量。

---

## 推荐的非取舍项（直接执行）

- **字段命名**：英文（与其他 schema 一致，方便 AI 识别）；中文说明。
- **frontmatter**：`title: 本地化约束模板` / `audience: AI / 开发者` / `scope: .ai/local-constraints.md 的字段定义、编写口径与最小模板`。
- **五节结构**：目标 / 交付约定 / 标准模板 / 编写规则 / 与执行流程的关系（与其他 schema 一致）。
- **mcv-deployment § 4 指针**：追加一句"字段定义与最小模板参考 `local-constraints-schema.md`"。
- **Coder/README.md 注册**：在目录结构 `/20_Workflow_Lifecycle` 下加入 `local-constraints-schema.md`，并在读取顺序说明中明确"schema 文件是产物模板，不进主读取序列，按需引用"。

---

## 风险

- 本轮全是文档级改动，无运行时影响。
- 新 schema 文件对已部署项目无强制回填要求（旧 local-constraints.md 可逐步迁移到新字段集，不阻断）。

---

# 请回复

1. **G-1 方案**：α / β / γ

拍板后我进 P3 出具体 schema 骨架与 edit 清单。
