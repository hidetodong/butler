# Butler 规则仓库 Nice to Have Bucket G 交付总结

> 日期：2026-04-17
> 任务：修复 Nice to Have Bucket G（N-5 local-constraints schema 新增）1 条问题
> 状态：已完成，可交付

## 本次交付目标

让基地车部署产物链对称：在 CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT 四个产物都有 schema 的情况下，补齐 `.ai/local-constraints.md` 缺失的 schema，避免 AI 部署时靠自由发挥填写本地化约束。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| N-5 | `.ai/local-constraints.md` 缺 schema，AI 部署时字段结构不稳定 | 新建 `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`（方案 α：2 必填 + 3 可选）；`mcv-deployment.md § 4` 追加 schema 指针；`Coder/README.md` 双处注册 |

## 关键变更 / 用户可感知变化

- **产物链对称完成**：basecamp 部署产物现在全部有 schema 支撑（`concept-schema` / `acceptance-schema` / `tech-plan-schema` / `verify-schema` / `local-constraints-schema` / `delivery-summary`）。
- **新项目部署时有骨架可参考**：AI 执行 `mcv-deployment § 4 本地化适配` 时，不再靠自由发挥，而是按 5 字段模板填写（Project Type + Active Profiles + 可选 3 项）。
- **字段边界清晰**：
  - `Local Constraints`：**规则层面**的本地差异（如"某目录允许 any"）
  - `Scope Exceptions`：**位置层面**的例外（如"`/legacy` 不受某规则约束"）
  - `External References`：外部资源指针（与 `.ai/references/` 实际产物区分）
- **字段弹性**：Active Profiles 未命中时显式写"无，仅按通用 SOP"；Local Constraints / Scope Exceptions / External References 三项可省略，小项目不必硬填。

## 高层影响范围

**新建 1 个文件**：
- `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`（与其他四个 schema 同目录，命名风格一致）

**修改 2 个文件**：
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 4`（追加 schema 指针）
- `Coder/README.md`（目录结构 + "其中："说明列表双处注册）

**未影响**：其他 schema、lifecycle、Extension、templates、scripts、Domain Profiles、已部署项目的 local-constraints.md。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `ls local-constraints-schema.md` | 文件存在（2751 字节） ✅ |
| frontmatter 分隔线 | 2 ✅ |
| 五节章节 | L9/15/22/46/54 齐全 ✅ |
| 5 个字段 | L25/29/33/37/41 齐全 ✅ |
| `grep 'local-constraints-schema' mcv-deployment.md` | L77 命中 ✅ |
| `grep 'local-constraints-schema' Coder/README.md` | L50 + L110 双处命中 ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 向下兼容

已部署项目的 `local-constraints.md` 无强制回填要求。后续若某项目检测到字段缺失，AI 应主动建议迁移但不阻断当前任务。本轮未落地"自动迁移"规则以避免扩张。

### Nice to Have 剩余（1 条）

- **N-6** `10_Domain_Stack_Profiles/` 三个 profile 不同级（vue3 框架 / typescript 语言 / build-tooling 构建形态）— Bucket H，按既定策略延后（当前只有 3 个 profile，强行分层会产生只有 1 个文件的空子目录，ROI 不够；等 profile 数量到 5-6 个再做）。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 新增规则：`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`
- 关联修改：
  - `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 4`（schema 指针）
  - `Coder/README.md`（目录结构 + 说明列表）
- 前 7 份交付（6 次审计修复 + 本次）：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-a.md`
  - `deliveries/2026-04-17-should-fix-bucket-e.md`
  - `deliveries/2026-04-17-should-fix-bucket-b.md`
  - `deliveries/2026-04-17-should-fix-bucket-c.md`
  - `deliveries/2026-04-17-should-fix-bucket-d.md`
  - `deliveries/2026-04-17-nice-to-have-bucket-f.md`
- 当前 milestone：`v0.0.8`（Must Fix + Should Fix 全闭环）
