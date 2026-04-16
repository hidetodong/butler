# Goal

- 按 B-1 方案 B（扩展 `Gate Coverage` 分 4 类）、B-2（P4 补 `.ai/task-state.md` 同步约束）、B-3 方案 α（P5 对 Delivery Summary 触发条件加指针），对 Bucket B 3 条 Should Fix 执行最小范围修复。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 改动点 |
|---|---|---|---|
| 1 | `Coder/20_Workflow_Lifecycle/verify-schema.md` | B-1 | 2（§ 3 标准模板 + § 4 编写规则） |
| 2 | `Coder/20_Workflow_Lifecycle/lifecycle.md` | B-2 + B-3 | 2（P4 执行原则 + P5 必须产物指针） |

共 2 个文件，4 处 edit。

# Interface / Contract

- **verify-schema.md**：
  - `Gate Coverage` 字段从"通用质量门禁 / Active Profiles" 2 类扩展到"通用质量门禁 / Active Profiles / Tech Plan Alignment / References Compliance" 4 类。
  - 顶级字段列表、`Verification Summary` / `AC Status` / `Verification Results` / `Remaining Risks` / `Handoff / Next Step` 等其他字段**不动**，保持现有产物向下兼容。
- **lifecycle.md**：
  - P4 新增一条执行原则约束（硬约束 `必须`）。
  - P5 必须产物段增加一个显式指针 `delivery-summary.md § 2 触发时机`。

# State / Boundary

- 不动 `delivery-summary.md` 本体（它继续是触发条件 SSOT）。
- 不动 concept-schema / acceptance-schema / tech-plan-schema（Bucket B 不涉及 P1/P2/P3 schema）。
- 不动 `context-persistence.md`（P4 是引用它，不修改它）。

# Design Decisions

1. **B-1 方案 B 落地位置**：在 § 3 标准模板的 `Gate Coverage` 段内列出 4 个子类别；在 § 4 编写规则中加一条说明 4 类的用途。保持字段顺序与现有模板一致，减少读者重新适应成本。
2. **B-2 约束强度与位置**：使用"必须"（硬约束）；插入位置选在 P4 "执行原则" 列表末尾，与同列表的其他"必须"级别约束风格一致。
3. **B-3 指针措辞**：采用"**具体触发条件参考 `delivery-summary.md § 2 触发时机`**"的内嵌式指针（不新增段落），保留 P5 段落的现有结构。
4. **兼容性**：VERIFY_REPORT 新字段对**已存在的 VERIFY_REPORT 产物**是向下兼容的 —— 旧 VERIFY_REPORT 仍然合法，只是缺少新字段；未来 P5 按新 schema 填。本轮 **不**回填 `.ai/VERIFY_REPORT.md`（它是 Bucket B 自己的产物，按新 schema 一次到位即可）。

# Execution Steps

## Edit 1 — `verify-schema.md § 3 标准模板`

扩展 `Gate Coverage` 段示例：

**old**:
```
# Gate Coverage
- 通用质量门禁：已验证项
- Active Profiles：已验证项
```

**new**:
```
# Gate Coverage
- 通用质量门禁：已验证项
- Active Profiles：已验证项（仅命中时填，未命中可省略）
- Tech Plan Alignment：TECH_PLAN 中 Design Decisions 的兑现情况
- References Compliance：.ai/references/ 下已处理参考资料的规格遵守情况（无参考资料时标注 N/A）
```

## Edit 2 — `verify-schema.md § 4 编写规则`

扩展"若存在 active profiles..."这一条为更完整的 Gate Coverage 分类说明：

**old**:
```
- 若存在 active profiles，应区分"通用质量门禁"与"profile 验证依据"。
```

**new**:
```
- `Gate Coverage` 分四类回填：通用质量门禁（始终）、Active Profiles（仅命中时）、Tech Plan Alignment（逐项对照 `TECH_PLAN.md` 中的 Design Decisions 说明是否兑现）、References Compliance（逐项对照 `.ai/references/` 下的参考资料说明规格是否被遵守；本轮无参考资料时标注 N/A）。
```

## Edit 3 — `lifecycle.md` P4 执行原则补 task-state 约束

在 P4 "执行原则" 列表的最后一条（"若缺少明确探测命令或环境能力不足..."）之后追加一条：

**old**（匹配列表最后一条）:
```
- 若缺少明确探测命令或环境能力不足，应先向用户确认验证方式。
```

**new**:
```
- 若缺少明确探测命令或环境能力不足，应先向用户确认验证方式。
- 若任务命中 `40_Context_Management/context-persistence.md` 中定义的激活条件（新项目接入、跨会话继续、多阶段推进、需要等待 ACK 或外部结果、无法单轮闭合等），执行过程中**必须**按其"运行时增量"规则同步 `.ai/task-state.md`，不得仅依赖对话记忆保留阶段状态。
```

## Edit 4 — `lifecycle.md` P5 必须产物段加指针

**old**:
```
**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，并落在项目根目录 `deliveries/` 下。
```

**new**:
```
**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。
```

# Verification Plan

- **B-1**：
  - `grep -n 'Tech Plan Alignment\|References Compliance' verify-schema.md` 至少命中 2 处（模板示例 + 编写规则说明）；
  - 通读 § 3 / § 4，两处用词一致，不出现冲突。
- **B-2**：
  - `grep -n 'task-state' Coder/20_Workflow_Lifecycle/lifecycle.md` 在 P4 章节（L108-140 附近）命中至少一次，带"必须"级别措辞。
- **B-3**：
  - `grep -n 'delivery-summary.md § 2' lifecycle.md` 在 P5 章节（L130-150 附近）命中；
  - 读 P5 段落，能清楚看到触发条件的指针目标文件与章节。
- `git diff --stat` 应仅显示 2 个规则文件变更。

# Risks / Open Questions

- **风险 1**：`Gate Coverage` 新增的 "Tech Plan Alignment / References Compliance" 子类，在**没有** TECH_PLAN 或 references 的简化路径任务中可能显得多余。缓解：§ 4 编写规则明确说"本轮无参考资料时标注 N/A"；简化路径本身已允许省略 VERIFY_REPORT，不受此字段约束。
- **风险 2**：B-3 方案 α 在 P5 内嵌指针，如果读者只扫一眼可能仍错过。缓解：用加粗（`**...**`）提高视觉权重；SSOT 原则下跳转一次是必要成本。
- **开放问题**：无。
