# Goal

- 修复 Butler Nice to Have Bucket G（N-5）：`.ai/local-constraints.md` 在其他产物（CONCEPT/AC_LIST/TECH_PLAN/VERIFY_REPORT）都有 schema 的情况下缺失 schema；新建 `local-constraints-schema.md` 让基地车部署产物链对称，为 AI 部署时填写 local-constraints 提供字段骨架。

# Current Understanding

- 本任务是 Butler 规则仓第八轮维护（v0.0.9 Bucket F 之后）。
- `mcv-deployment.md § 4 本地化适配` 当前只有一句描述 + 一个示例，缺少字段定义。AI 部署时靠自由发挥填写 `.ai/local-constraints.md`。
- 其他四个主要产物都有对应的 `*-schema.md` 文件（`concept-schema.md`、`acceptance-schema.md`、`tech-plan-schema.md`、`verify-schema.md`），位于 `Coder/20_Workflow_Lifecycle/`。
- local-constraints 的性质与上述产物不同：
  - 它不是 P1-P5 某阶段的产物，而是基地车部署时的一次性产物 + 任务执行中的增量更新。
  - 它不是严格契约，而是"本项目相对于通用 SOP 的差异记录"。
  - schema 应偏向轻量（必填字段少），避免让 AI 部署陷入过度填写负担。
- 1 个主要设计取舍：**必填字段集**（最小 vs 中等）。

# Constraints

- 显性约束：
  - 新建文件必须在 `Coder/README.md` 的目录结构与读取顺序中注册（`CLAUDE.md` 第 3 条项目约束）。
  - frontmatter 必须含 `audience` 与 `scope`（`CLAUDE.md` 第 5 条）。
  - 不破坏 `mcv-deployment.md § 4` 现有描述的语义。
  - 不引入新的目录层级。
- 隐性约束：
  - schema 命名风格与其他四个一致（`local-constraints-schema.md`）。
  - 字段命名使用英文（与其他 schema 一致）。

# Impact Scope

预计修改文件：
- **新建** `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 4`（补一个指向 schema 的指针）
- `Coder/README.md`（目录结构注册新文件）

不影响：其他 schema、lifecycle、其他规则文件、templates、scripts。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

- **G-1** 必填字段集需用户拍板（最小 2 个 vs 中等 3 个）。
- 可选字段、字段命名、schema 骨架均按推荐方案执行（详见 AC_LIST）。
