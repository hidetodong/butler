# Goal

- 修复 Butler Should Fix Bucket B（产物链字段与阶段描述补全）3 条问题：VERIFY_REPORT 没有校验 TECH_PLAN 与 references 是否兑现；P4 阶段没有显式要求长任务同步 `.ai/task-state.md`；P5 Delivery Summary 触发条件只在 `delivery-summary.md` 里完整描述，`lifecycle.md` 读起来信息不够。

# Current Understanding

- 本任务是 Butler 规则仓维护的第四轮。上一轮 Bucket E 已随 commit `8d8d239` 落地。
- Bucket B 3 条都位于**主产物链**上，修完后 CONCEPT → AC_LIST → TECH_PLAN → VERIFY_REPORT 的审计闭环会更严密。
- 其中 2 条（B-1 新字段落位、B-3 lifecycle 里放指针还是内联）存在设计取舍需要用户拍板。B-2 无取舍，直接按规则补。

# Constraints

- 显性约束：
  - 不破坏现有 schema 模板的 frontmatter、标题层级与字段顺序。
  - 不修改 schema 已经约定的字段（`Verification Summary` / `AC Status` 等）的既有语义，仅新增或扩展。
  - 与 Bucket A 确立的 SSOT 原则一致（`delivery-summary.md` 作为 Delivery Summary 的 SSOT）。
- 隐性约束：
  - Markdown 模板字段扩充应控制在"让 AI 和人类都能快速填写"的可读密度内。

# Impact Scope

预计修改文件：
- `Coder/20_Workflow_Lifecycle/verify-schema.md`（B-1：补字段或扩展段落）
- `Coder/20_Workflow_Lifecycle/lifecycle.md`（B-2 P4 + B-3 P5）

不影响：其他 schema（concept-schema / acceptance-schema / tech-plan-schema）、delivery-summary 本身、Extension 目录、templates、scripts。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

- **B-1** `VERIFY_REPORT` 补校验 TECH_PLAN / references 的字段落位方式需要用户拍板（见 AC_LIST）。
- **B-3** `lifecycle.md` P5 的 Delivery Summary 触发条件用指针还是内联需要用户拍板。
