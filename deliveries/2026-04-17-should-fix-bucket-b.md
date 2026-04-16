# Butler 规则仓库 Should Fix Bucket B 交付总结

> 日期：2026-04-17
> 任务：修复 Should Fix Bucket B（产物链字段与阶段描述补全）3 条问题
> 状态：已完成，可交付

## 本次交付目标

修复 Butler Should Fix Bucket B 的 3 条问题：`VERIFY_REPORT` 未覆盖对 TECH_PLAN（Design Decisions）和 references（规格）的校验；P4 执行阶段未显式要求长任务同步 `.ai/task-state.md`；P5 Delivery Summary 的触发条件只在 `delivery-summary.md § 2` 完整列出，`lifecycle.md` 读起来信息不够。

## 已完成内容

| # | 问题 | 修复方式 |
|---|---|---|
| 1 | VERIFY_REPORT 漏校验 TECH_PLAN Design Decisions 与 references 规格 | `verify-schema.md § 3 模板`扩展 `Gate Coverage` 分 4 类（新增 Tech Plan Alignment / References Compliance）；§ 4 编写规则同步添加四类回填说明 |
| 2 | P4 没有显式要求长任务同步 `.ai/task-state.md` | `lifecycle.md` P4 "执行原则"列表末尾追加一条**必须**级别硬约束，枚举激活条件并指向 `context-persistence.md` |
| 3 | P5 Delivery Summary 触发条件在 `lifecycle.md` 不明显 | `lifecycle.md` P5 必须产物段加粗内嵌指针 → `delivery-summary.md § 2 触发时机`（SSOT 原则，与 Bucket A 一致） |

## 关键变更 / 用户可感知变化

- **P5 验证现在要求回填 4 类 Gate Coverage**：通用质量门禁、Active Profiles（仅命中时）、**Tech Plan Alignment**（Design Decisions 是否兑现）、**References Compliance**（参考资料规格是否遵守）。简化路径或无 references 的任务可标 "N/A"，不增加冗余负担。
- **P4 阶段长任务硬性要求外化状态**：AI 在命中 `context-persistence.md` 激活条件时，必须把阶段状态写入 `.ai/task-state.md`，不得仅靠对话记忆推进。
- **P5 读 `lifecycle.md` 时能直接跳到 Delivery Summary 触发条件**：不再需要先读 lifecycle、再读 delivery-summary 才能判断是否该生成交付总结。

## 高层影响范围

**直接修改 2 个规则文件**：

- `Coder/20_Workflow_Lifecycle/verify-schema.md`（§ 3 模板 + § 4 编写规则）
- `Coder/20_Workflow_Lifecycle/lifecycle.md`（P4 执行原则 + P5 必须产物）

**未影响**：`delivery-summary.md`（保持作为触发条件 SSOT）、其他 schema 文件、Extension 目录、templates、scripts、`context-persistence.md`（本轮只引用，不修改）。

**向下兼容性**：既有 VERIFY_REPORT 产物仍合法，仅缺少新字段；本轮 `.ai/VERIFY_REPORT.md` 已按新 schema 填写（含 4 类 Gate Coverage），完成 dogfooding 自举验证。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `grep 'Tech Plan Alignment\|References Compliance' verify-schema.md` | 3 处命中（模板 × 2 + 规则 × 1） ✅ |
| `grep 'task-state' lifecycle.md` | P4 L132 命中**必须**级别硬约束 ✅ |
| `grep 'delivery-summary.md § 2' lifecycle.md` | P5 L136 加粗指针就位 ✅ |
| 本轮 VERIFY_REPORT 自举验证 | 已按 4 类 Gate Coverage 填写 ✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### 未处理的 Should Fix（2 条）

- Bucket C（Mode 术语消歧，1 条）— 相对独立，改动小
- Bucket D（模板重复消除，1 条）— 需设计新的引用机制，建议最后处理

建议下一步 Bucket C。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 关联规则：
  - `Coder/20_Workflow_Lifecycle/verify-schema.md`（Gate Coverage 扩展）
  - `Coder/20_Workflow_Lifecycle/lifecycle.md`（P4 + P5 补充）
  - `Coder/20_Workflow_Lifecycle/delivery-summary.md § 2`（P5 触发条件 SSOT，本轮指针目标）
  - `Coder/40_Context_Management/context-persistence.md`（P4 新硬约束的依赖）
- 前三轮交付：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-a.md`
  - `deliveries/2026-04-17-should-fix-bucket-e.md`
