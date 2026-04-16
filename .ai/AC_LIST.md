# Goal

- 修复 Bucket B（产物链字段与阶段描述补全）3 条 Should Fix。

# In Scope

- B-1: `verify-schema.md` 补足对 TECH_PLAN（Design Decisions）与 references（规格）是否被落实的验证口径。
- B-2: `lifecycle.md` P4 章节显式补充"长任务必须同步 `.ai/task-state.md`"的触发约束。
- B-3: `lifecycle.md` P5 章节明确 Delivery Summary 的触发判断，与 `delivery-summary.md § 2` 保持单一来源。

# Out of Scope

- Bucket C（Mode 术语消歧）与 Bucket D（模板重复消除）。
- 不修改 delivery-summary.md 本体（它继续是触发条件的 SSOT）。
- 不新增 `.ai/` 目录下的运行态文件类型。

# Acceptance Checklist

- [ ] **B-1** `verify-schema.md` 新增或扩展字段明确覆盖 "TECH_PLAN Design Decisions 是否兑现" 与 "references 的规格是否遵守"，方案待拍板
- [ ] **B-2** `lifecycle.md` P4 段落显式要求"命中 `40_Context_Management/context-persistence.md` 触发条件时必须同步 `.ai/task-state.md`"
- [ ] **B-3** `lifecycle.md` P5 段落明确 Delivery Summary 触发判断，方案待拍板（指针 vs 内联）

# Verification Method

- **B-1**：
  - 通读 `verify-schema.md`，确认有字段或小节专门要求回答 "Design Decision 是否落实" 与 "references 规格是否兑现"；
  - `grep -n 'Design Decision\|Plan Alignment\|References Compliance' verify-schema.md` 命中新字段。
- **B-2**：
  - `grep -n 'task-state' Coder/20_Workflow_Lifecycle/lifecycle.md` 在 P4 章节（L108-132 附近）有命中，措辞为"必须 / 应"级别的硬约束。
- **B-3**：
  - `grep -nE 'delivery-summary\.md|Delivery Summary' lifecycle.md` 在 P5 章节附近有清晰的触发条件表述（指针或内联），不再让读者猜测。

# Open Questions / Risks

## ❓ 待拍板 - B-1 方案选择

**问题**：`verify-schema.md` 当前必填字段是 `Verification Summary / AC Status / Verification Results / Gate Coverage / Remaining Risks / Handoff / Next Step`。要让 VERIFY_REPORT 也校验 TECH_PLAN 的 Design Decisions 与 references 的规格，字段如何落位？

### 方案 A — 新增两个顶级字段：`Plan Alignment`、`References Compliance`

- schema 顶层字段数从 6 增加到 8。
- **优点**：语义最清晰，字段名见名知义。
- **缺点**：模板变沉；AI 在 P5 填写时模板更重。

### 方案 B（推荐）— 扩展 `Gate Coverage`，加两个子类

- 保持 6 个顶级字段不变。
- 将 `Gate Coverage` 的分类从"通用质量门禁 / Active Profiles"扩展为"通用质量门禁 / Active Profiles / Tech Plan Alignment / References Compliance"四类。
- **优点**：顶级字段不膨胀；`Gate Coverage` 语义原本就是"验证覆盖性"，新增类别天然契合。
- **缺点**：`Gate Coverage` 一词从"门禁"语义略微扩展到"对齐"，但不冲突。

### 方案 C — 在 `Verification Results` 里逐项标注

- 每个 AC 的 verification result 下要求分别回答"对应 Design Decision 是否兑现""对应 references 规格是否遵守"。
- **优点**：最小改动；细粒度追踪。
- **缺点**：结果分散，没有汇总视图；当某些 AC 不涉及 Design Decision 或 references 时产生冗余。

---

## ❓ 待拍板 - B-3 方案选择

**问题**：`lifecycle.md` P5 章节目前只有一句"若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结"。AI 需要跳转到 `delivery-summary.md § 2` 才能看到完整 5 条触发条件。

### 方案 α（推荐）— 显式指针

- `lifecycle.md` P5 改为："具体触发条件参考 `delivery-summary.md § 2`"。
- **优点**：SSOT 归 delivery-summary；和 Bucket A 的 SSOT 原则一致；避免将来两处漂移。
- **缺点**：AI 读 lifecycle 时还要一次跳转。

### 方案 β — 内联 5 条触发条件

- 把 delivery-summary.md § 2 的 5 条触发条件完整抄到 lifecycle.md P5。
- **优点**：lifecycle 自给自足，不用跳转。
- **缺点**：两处维护，未来可能漂移。

### 方案 γ — 在 lifecycle 给关键摘要 + 指针细节

- 内联 2-3 句关键判据（"已完成主要目标、已达可验收、有明确验证结论"），后接指针"完整 5 条判断见 delivery-summary.md § 2"。
- **优点**：平衡自给自足与 SSOT。
- **缺点**：轻度重复风险；"关键摘要"这个折中在规则维护上偏软。

---

## 风险

- 改动均为 schema / lifecycle 文本，无运行时行为变更。
- B-1 方案 B 需要 `verify-schema.md § 3 标准模板` 与 § 4 编写规则同步更新，确保模板示例与字段描述一致。

---

# 请回复

1. **B-1 方案选择**：A / B / C
2. **B-3 方案选择**：α / β / γ

B-2 无设计取舍，按 `必须 / 应` 级别的硬约束直接补充。两个方案都拍板后我进 P3。
