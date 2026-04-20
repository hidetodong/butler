# 对话内人话摘要（Chat Recap）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `Coder/20_Workflow_Lifecycle/delivery-summary.md` 新增 §8 对话内人话摘要，并在 `lifecycle.md` P5 段补充对 §8 的显式引用，让 AI 在 Delivery Summary 触发时刻的对话层输出走"讲人话"口径、文件层保持正式结构。

**Architecture:** 纯 Markdown 规则文件改动。单规则文件扩展（§8），外加一处跨文件引用（lifecycle.md P5）。不新增文件、不改目录结构、不改读取顺序。

**Tech Stack:** Markdown + frontmatter。无代码、无测试框架。验证手段为人工阅读 + grep 关键词 + 对照 spec 验收清单。

**Spec 路径：** `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md`

---

## 文件结构

butler 仓库自身遵循 butler SOP，本计划除规则文件改动外，还需按 P1-P5 产物链更新 `.ai/` 与 `deliveries/`：

- **Modify:** `Coder/20_Workflow_Lifecycle/delivery-summary.md`
  - 在 §7 "与执行流程的关系" 之后新增 §8 "对话内人话摘要"
- **Modify:** `Coder/20_Workflow_Lifecycle/lifecycle.md`
  - 在 P5 Verify 段现有 Delivery Summary 描述之后，补一句引用 §8
- **Overwrite:** `.ai/CONCEPT.md`（P1 产物，按 `concept-schema.md` 回填本任务）
- **Overwrite:** `.ai/AC_LIST.md`（P2 产物，按 `acceptance-schema.md` 回填本任务）
- **Overwrite:** `.ai/TECH_PLAN.md`（P3 产物，按 `tech-plan-schema.md` 回填本任务）
- **Overwrite:** `.ai/VERIFY_REPORT.md`（P5 产物，按 `verify-schema.md` 回填本任务）
- **Create:** `deliveries/2026-04-20-chat-recap-style.md`（完整交付总结，按 `delivery-summary.md §4`）

`.ai/*.md` 历史版本已进入 git 历史（上一任务 butler-upgrade 的 4/17 版本），安全覆写。

---

## Task 0: 产出 .ai/ P1–P3 产物（butler 规范对齐）

**Files:**
- Overwrite: `.ai/CONCEPT.md`
- Overwrite: `.ai/AC_LIST.md`
- Overwrite: `.ai/TECH_PLAN.md`

本任务把已经在 `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md` 讨论清楚的内容，按 butler SOP 的 P1-P3 schema 回填到 `.ai/`，作为 butler 规范下的决策记录真源。

- [ ] **Step 1: 回填 `.ai/CONCEPT.md`**

按 `Coder/20_Workflow_Lifecycle/concept-schema.md §3` 模板，写入以下内容：

```md
# Goal
- 为 Delivery Summary 触发时刻定义对话层风格约束，让 AI 在对话框内给出 3–6 句人话摘要，`deliveries/` 文件层仍按正式结构产出

# Current Understanding
- 现状：`Coder/20_Workflow_Lifecycle/delivery-summary.md` 仅规定 `deliveries/*.md` 的 7 小节文件结构，未约束对话层表达
- AI 倾向于把文件结构原样复述到对话，输出冗长、官方、缺乏判断
- 预期产出：在 `delivery-summary.md` 新增 §8 定义对话层风格；在 `lifecycle.md` P5 段补引用；同时产出 butler SOP 所需的 `.ai/` 决策记录与 `deliveries/` 交付总结

# Constraints
- 显性约束：
  - 不新增规则文件，不改目录结构与读取顺序
  - 不改 Delivery Summary 触发条件（§2 沿用）
  - 不改文件层最小结构（§4 沿用）
  - 不回溯历史 deliveries
- 隐性约束：
  - 对话层规则必须自包含，仅读 `delivery-summary.md` 就能理解两种表达
  - 反模糊口径必须显式（无风险时不得用"一切顺利"替代）

# Impact Scope
- 影响：`Coder/20_Workflow_Lifecycle/delivery-summary.md`、`Coder/20_Workflow_Lifecycle/lifecycle.md`、`.ai/*.md`、`deliveries/2026-04-20-chat-recap-style.md`
- 不影响：`Coder/README.md`、`templates/rule-card.md`、`Coder/CLAUDE.md`、其他 schema、hook 配置

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）
- 未命中任何 `10_Domain_Stack_Profiles/` profile，仅按通用 SOP 推进

# Open Questions
- 无未决问题（需求边界已在 brainstorming 阶段全部澄清）
```

- [ ] **Step 2: 回填 `.ai/AC_LIST.md`**

按 `Coder/20_Workflow_Lifecycle/acceptance-schema.md §3` 模板，写入以下内容：

```md
# Goal
- 为 Delivery Summary 触发时刻新增对话层风格约束，同时保持文件层正式结构不变

# In Scope
- 在 `Coder/20_Workflow_Lifecycle/delivery-summary.md` 新增 §8 对话内人话摘要
- 在 `Coder/20_Workflow_Lifecycle/lifecycle.md` P5 Verify 段补一句对 §8 的引用
- 按 butler SOP 产出 `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md`
- 本次交付生成 `deliveries/2026-04-20-chat-recap-style.md`，并按新 §8 给对话摘要（dogfood 首次应用）

# Out of Scope
- 不新建独立规则文件（如 `chat-recap.md`）
- 不改 `Coder/README.md` 目录结构与读取顺序
- 不改 `templates/rule-card.md` 浓缩规则卡
- 不改 `Coder/CLAUDE.md` 协作约定
- 不回溯 / 不迁移历史 `deliveries/*.md`
- 不下沉对话层风格到 P2 ACK / P3 ACK / 阶段 checkpoint

# Acceptance Checklist
- [ ] AC1: `delivery-summary.md` 出现 §8 节，子节覆盖：8.1 触发 / 8.2 形式 / 8.3 内容核心 / 8.4 收尾引用 / 8.5 与 §4 的关系
- [ ] AC2: §8.2 明确包含三条硬约束：3–6 句中文散文、禁止编号小节标题、禁止铺排长 bullet
- [ ] AC3: §8.3 列出三项必覆盖内容（做了什么 / 风险 / 下一步），对"无风险"场景显式写出"本轮无剩余风险"反模糊口径
- [ ] AC4: §8.4 给出固定引用格式 `正式版：deliveries/YYYY-MM-DD-<slug>.md`
- [ ] AC5: `lifecycle.md` P5 Verify 段出现对 `delivery-summary.md § 8` 的显式引用
- [ ] AC6: `Coder/README.md`、`templates/rule-card.md`、`Coder/CLAUDE.md`、目录结构、读取顺序均未改动
- [ ] AC7: 仅阅读 `delivery-summary.md` 单文件即可同时理解文件层（§2–§7）与对话层（§8）两种表达
- [ ] AC8: `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md` 按对应 schema 全字段回填
- [ ] AC9: `deliveries/2026-04-20-chat-recap-style.md` 存在且结构符合 `delivery-summary.md §4`
- [ ] AC10: 本轮 P5 结束时，对话框内输出的收尾摘要符合新 §8 风格（首次 dogfood 验证）

# Verification Method
- AC1: grep `delivery-summary.md` 中 `## 8.`、`### 8.1`–`### 8.5` 子节标题
- AC2: grep `delivery-summary.md` 中关键词 `3–6 句`、`禁止输出任何编号小节标题`、`禁止铺排长 bullet`
- AC3: grep `delivery-summary.md` 中关键词 `本轮无剩余风险`，并人工确认三项内容核心均存在
- AC4: grep `delivery-summary.md` 中固定格式 `正式版：deliveries/YYYY-MM-DD-<slug>.md`
- AC5: grep `lifecycle.md` 中 `delivery-summary.md § 8`
- AC6: `git diff HEAD~N -- Coder/README.md templates/rule-card.md Coder/CLAUDE.md` 输出为空
- AC7: 人工通读 `delivery-summary.md`，确认自包含
- AC8: 人工对照各 schema §2 必填字段清单
- AC9: 人工对照 `delivery-summary.md §4` 七个小节
- AC10: 人工对照 §8.2 / §8.3 / §8.4 对本次收尾摘要逐项核查

# Open Questions / Risks
- 风险：AI 可能把"讲人话"误解为"可以省略风险声明"。已通过 AC3 反模糊口径兜底
- 风险：`delivery-summary.md` 从 7 节扩到 8 节，文件变长。若未来对话层约束继续增加（≥ 3 条），应评估拆分到独立文件
- 无未决问题
```

- [ ] **Step 3: 回填 `.ai/TECH_PLAN.md`**

按 `Coder/20_Workflow_Lifecycle/tech-plan-schema.md §3` 模板，写入以下内容：

```md
# Goal
- 支撑 AC1–AC10：新增 §8 对话层风格规则、补 lifecycle 引用、按 butler SOP 全链路产出 `.ai/` 与 `deliveries/`

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` — 追加 §8 对话内人话摘要，含 5 个子节
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — P5 Verify 段"必须产物"条目后追加一句 §8 引用
- `.ai/CONCEPT.md` — 本任务 P1 决策记录（覆写）
- `.ai/AC_LIST.md` — 本任务 P2 决策记录（覆写）
- `.ai/TECH_PLAN.md` — 本任务 P3 决策记录（即本文件）
- `.ai/VERIFY_REPORT.md` — 本任务 P5 验证结果（覆写）
- `deliveries/2026-04-20-chat-recap-style.md` — 本任务 Delivery Summary（新建）

# Interface / Contract
- `delivery-summary.md §8` 对外承诺：任何 Delivery Summary 触发时刻，AI 的对话回应必须同时满足 §8.2 形式、§8.3 内容核心、§8.4 收尾引用三组约束
- `lifecycle.md` P5 段承诺：生成 Delivery Summary 的场景下，AI 对话层输出受 §8 约束，不只受 §4 约束
- `.ai/*.md` 承诺：严格符合各自 schema §2 必填字段清单
- `deliveries/<date>-<slug>.md` 承诺：严格符合 `delivery-summary.md §4` 七小节结构

# State / Boundary
- 状态边界：§8 仅在 Delivery Summary 触发时生效；不触发时沿用既有 checkpoint / handoff 口径
- 模块职责边界：§8 管对话层、§4 管文件层，两者同源不同表达，不得互相替代
- 不在范围内：P2 / P3 ACK、阶段 checkpoint、handoff、VERIFY_REPORT 本身的对话层风格

# Design Decisions
- 选择 A（§8 扩节）而非 B（delivery-summary.md 整体重构为对话层 + 文件层二分）或 C（新建 `chat-recap.md`）：改动成本最低、职责同源集中、不破坏既有锚点。若未来对话层约束 ≥ 3 条，再评估拆分到独立文件
- 硬上限 "3–6 句" 而非 "≤ 150 字"：句数约束更贴合散文节奏，用户已在 brainstorming 阶段显式确认
- "反模糊口径"（无风险必须显式写"本轮无剩余风险"）作为兜底，防止"讲人话"被误用为"可以不说风险"
- 未命中任何 Domain / Stack Profile；仅按通用 SOP 推进

# Execution Steps
- Task 0: 产出 .ai/ P1–P3 产物（本文件 + CONCEPT + AC_LIST）
- Task 1: 在 `delivery-summary.md` 追加 §8 完整内容，grep 验证字段覆盖，commit
- Task 2: 在 `lifecycle.md` P5 段追加 §8 引用句，grep 验证，commit
- Task 3: 产出 `.ai/VERIFY_REPORT.md` 与 `deliveries/2026-04-20-chat-recap-style.md`，按新 §8 输出对话摘要，commit

# Verification Plan
- AC1–AC4：grep `delivery-summary.md` 的 §8 字段、关键词、固定格式（Task 1 Step 3 / Step 4）
- AC5：grep `lifecycle.md` 的 §8 引用（Task 2 Step 3 / Step 4）
- AC6：`git diff` 未改动文件（Task 3 Step 1）
- AC7：人工通读 `delivery-summary.md`（Task 3 Step 2）
- AC8：对照各 schema §2 逐项核查 `.ai/` 四份文件（Task 3 Step 4）
- AC9：对照 `delivery-summary.md §4` 核查 deliveries 文件（Task 3 Step 5 前置）
- AC10：对照 §8 核查本轮对话摘要（Task 3 Step 5 收尾时）

# Risks / Open Questions
- 覆写 `.ai/` 会丢失 4/17 butler-upgrade 任务的产物内容，但 git 历史保留
- 规则密度增长：`delivery-summary.md` 从 7 节扩到 8 节；通过 §8 紧凑编号（5 子节）控制
- 无未决问题
```

- [ ] **Step 4: 对照 schema 自查必填字段**

逐项核对：

- `CONCEPT.md`：Goal / Current Understanding / Constraints / Impact Scope / Project Type / Active Profiles / Open Questions — 6 项
- `AC_LIST.md`：Goal / In Scope / Out of Scope / Acceptance Checklist / Verification Method / Open Questions / Risks — 6 项
- `TECH_PLAN.md`：Goal / Files / Modules to Change / Interface / Contract / State / Boundary / Design Decisions / Execution Steps / Verification Plan / Risks / Open Questions — 8 项

任一字段缺失则回到对应 Step。

- [ ] **Step 5: Commit**

```bash
git add .ai/CONCEPT.md .ai/AC_LIST.md .ai/TECH_PLAN.md
git commit -m "$(cat <<'EOF'
docs(.ai): crystallize P1-P3 artifacts for chat-recap-style task

按 butler SOP 的 concept / acceptance / tech-plan schema 回填 .ai/ 下
三份决策记录，对齐超级力量（superpowers）spec 与 plan 的内容。
EOF
)"
```

预期：commit 成功，`git log -1` 显示新 commit 动了 `.ai/` 下 3 个文件。

---

## Task 1: 在 delivery-summary.md 新增 §8

**Files:**
- Modify: `Coder/20_Workflow_Lifecycle/delivery-summary.md`（在文件末尾追加一节）

- [ ] **Step 1: 读取当前文件，定位 §7 末尾**

Read `Coder/20_Workflow_Lifecycle/delivery-summary.md`。当前文件末尾（第 107–111 行）为：

```markdown
## 7. 与执行流程的关系

- 生命周期阶段仍保持 `P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify`
- Delivery Summary 不是新阶段，只是 P5 完整交付后的收尾产物
- `VERIFY_REPORT.md` 继续作为验证真源
- Delivery Summary 应基于已确认的 AC、方案与验证结论进行人类可读汇总
```

预期：确认 §7 最后一行是第 110 行的 "Delivery Summary 应基于已确认的 AC、方案与验证结论进行人类可读汇总"，文件无尾部空节。

- [ ] **Step 2: 在 §7 之后追加 §8 完整内容**

使用 Edit 工具，将 §7 的最后一行作为 `old_string` 锚点，替换为"原内容 + §8 完整内容"。

`old_string`:
```
- Delivery Summary 应基于已确认的 AC、方案与验证结论进行人类可读汇总
```

`new_string`:
```
- Delivery Summary 应基于已确认的 AC、方案与验证结论进行人类可读汇总

## 8. 对话内人话摘要

### 8.1 触发

与 §2 相同时机。若不满足 §2 触发条件（中途暂停、等待 ACK、等待外部结果、只是 checkpoint、只是跨会话恢复），也不生成本节规定的对话摘要，继续使用 checkpoint / handoff 口径。

### 8.2 形式

- 必须是 3–6 句中文散文。
- 禁止输出任何编号小节标题，不得复述 §4 的 4.1 / 4.2 结构。
- 禁止铺排长 bullet 清单；若非用 bullet 不可，至多 2 条，且每条不得超过 1 句。
- 措辞应口语化、可带判断词（如"基本没风险"、"建议下一步"），避免"已完成 / 已交付 / 已闭环"等模版套话单独出现。

### 8.3 内容核心

每段对话摘要必须同时覆盖以下三项，缺一不可：

1. **做了什么**：用户视角的最终结果，一句话说清。
2. **有没有风险 / 延后事项**：有就明说有；没有必须显式声明"本轮无剩余风险"，不得用"一切顺利"、"已完成"、"已闭环"等模糊套话替代。
3. **建议下一步**：例如"交付即止"、"需要你 ACK"、"建议后续迭代 X"。

### 8.4 收尾引用

对话摘要最后必须单独一行，按以下固定格式引用正式版文件：

```
正式版：deliveries/YYYY-MM-DD-<slug>.md
```

路径应指向本轮实际写入的 Delivery Summary 文件，不得省略、不得改写格式。

### 8.5 与 §4 的关系

- §4 定义 `deliveries/` 文件的书面结构（文件层）。
- §8 定义对话框内的收尾表达（对话层）。
- 两者同源、同触发，但风格分层：文件正式、对话口语。
- 不得用文件结构覆盖对话风格，也不得用对话口吻替代文件结构。
- 结论真源以 `deliveries/` 文件为准，对话摘要只是其口语化投影。
```

- [ ] **Step 3: 验证 §8 字段完整性**

Grep 以下关键字，确认均已出现在 `delivery-summary.md`：

```
## 8. 对话内人话摘要
### 8.1 触发
### 8.2 形式
### 8.3 内容核心
### 8.4 收尾引用
### 8.5 与 §4 的关系
3–6 句中文散文
本轮无剩余风险
正式版：deliveries/YYYY-MM-DD-<slug>.md
```

预期：9 个关键字全部命中。任一缺失则回到 Step 2 修正。

- [ ] **Step 4: 对照 spec 验收标准 1–4 自查**

对照 `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md` §5 验收标准：

- 验收 1（§8 出现，字段覆盖：触发、形式、内容核心、收尾、与 §4 关系）→ 对应 8.1 / 8.2 / 8.3 / 8.4 / 8.5。
- 验收 2（形式含 "3–6 句"、"禁止编号小节标题"、"禁止铺排长 bullet" 三条硬约束）→ 8.2 三条均存在。
- 验收 3（内容核心 3 项，对"无风险"有反模糊口径）→ 8.3 三项齐全，显式写"本轮无剩余风险"。
- 验收 4（末尾固定引用格式）→ 8.4 给出固定路径格式。

任一未命中则回到 Step 2 修正。

- [ ] **Step 5: Commit**

```bash
git add Coder/20_Workflow_Lifecycle/delivery-summary.md
git commit -m "$(cat <<'EOF'
docs(delivery-summary): add §8 对话内人话摘要 风格约束

在 Delivery Summary 触发时刻新增对话层风格规则：3–6 句中文散文、
禁止复述文件层小节标题、必须覆盖"做了什么/风险/下一步"三项，
并以固定格式引用 deliveries/ 正式版路径。对应 spec:
docs/superpowers/specs/2026-04-20-chat-recap-style-design.md
EOF
)"
```

预期：commit 成功，`git log -1` 显示新 commit 只动了 `delivery-summary.md` 一个文件。

---

## Task 2: 在 lifecycle.md P5 段补充对 §8 的引用

**Files:**
- Modify: `Coder/20_Workflow_Lifecycle/lifecycle.md`（P5 Verify 段，约第 134–151 行）

- [ ] **Step 1: 读取并定位 P5 段现有 Delivery Summary 描述**

Read `Coder/20_Workflow_Lifecycle/lifecycle.md`。当前第 136 行为：

```
**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。
```

预期：确认该句为 P5 段"必须产物"条目的第一行，且完整包含"**具体触发条件参考 `delivery-summary.md § 2 触发时机`**"这一内嵌子句。

- [ ] **Step 2: 在该句之后追加一句 §8 引用**

使用 Edit 工具，在现有整句末尾追加一句新句。

`old_string`:
```
**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。
```

`new_string`:
```
**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。生成 Delivery Summary 时，P5 对话回应必须同时遵守 `delivery-summary.md § 8` 的对话层风格约束，不得把文件层的编号小节结构原样复述到对话框内。
```

- [ ] **Step 3: 验证引用句已落位**

Grep `lifecycle.md` 是否出现：

```
delivery-summary.md § 8
```

预期：命中 1 次，且位于 P5 Verify 段的"必须产物"条目。

- [ ] **Step 4: 对照 spec 验收标准 5 自查**

spec §5 验收 5："`lifecycle.md` P5 Verify 段出现对 `delivery-summary.md §8` 的显式引用。"

确认 Step 3 的 grep 命中且上下文为 P5 段。未命中则回到 Step 2。

- [ ] **Step 5: Commit**

```bash
git add Coder/20_Workflow_Lifecycle/lifecycle.md
git commit -m "$(cat <<'EOF'
docs(lifecycle): P5 引用 delivery-summary §8 对话层风格约束

在 P5 Verify 段 Delivery Summary 描述之后追加一句，要求 AI 生成
Delivery Summary 时对话回应同时遵守新增的 §8 风格约束，避免把
文件层编号结构原样复述到对话框内。
EOF
)"
```

预期：commit 成功，`git log -1` 显示只动了 `lifecycle.md` 一个文件。

---

## Task 3: 终审 + VERIFY_REPORT + Delivery Summary

**Files:**
- Read: `Coder/README.md`
- Read: `templates/rule-card.md`
- Read: `Coder/CLAUDE.md`
- Read: `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md`
- Overwrite: `.ai/VERIFY_REPORT.md`
- Create: `deliveries/2026-04-20-chat-recap-style.md`

- [ ] **Step 1: 验证未改动项（spec 验收 6）**

运行：

```bash
git diff HEAD~2 -- Coder/README.md templates/rule-card.md Coder/CLAUDE.md
```

预期：输出为空（三个文件相对于两次 commit 之前均未改动）。

同时验证目录结构与读取顺序未改：

```bash
git diff HEAD~2 -- Coder/README.md
```

预期：同样输出为空。

若有任何 diff，说明误改，需回滚相关文件改动后重新提交。

- [ ] **Step 2: 单文件可读性验证（spec 验收 7）**

Read `Coder/20_Workflow_Lifecycle/delivery-summary.md` 全文。

自查：只阅读本文件，是否能同时理解以下两点？

1. `deliveries/*.md` 文件该怎么写（§2–§7 覆盖）。
2. 对话框内的收尾摘要该怎么说（§8 覆盖）。

若第 2 点需要跳到其他文件才能理解，说明 §8 自包含度不足，回到 Task 1 Step 2 补充。

- [ ] **Step 3: 跨文件一致性 grep**

运行：

```bash
git grep -n "delivery-summary.md" Coder/
```

预期：至少出现以下 3 类引用：

- `Coder/README.md`（原有目录结构与职责说明）
- `Coder/20_Workflow_Lifecycle/lifecycle.md`（§2 触发 + §8 对话风格，共 2 处）

确认所有引用路径正确、无拼写错误（如 `delivery_summary.md`、`delivery-summary.MD` 等变体）。

- [ ] **Step 4: 对照 `.ai/AC_LIST.md` 回填 `.ai/VERIFY_REPORT.md`**

按 `Coder/20_Workflow_Lifecycle/verify-schema.md §3` 模板写入 `.ai/VERIFY_REPORT.md`，内容如下：

```md
# Verification Summary
- 本次验证覆盖范围：`Coder/20_Workflow_Lifecycle/delivery-summary.md` §8 新增、`Coder/20_Workflow_Lifecycle/lifecycle.md` P5 引用句补丁、butler SOP 全链路产物（`.ai/*.md` 与 `deliveries/*.md`）
- 总体验收结论：AC1–AC10 全部满足，任务闭合，可交付

# AC Status
- [x] AC1: §8 五个子节齐全（8.1 触发 / 8.2 形式 / 8.3 内容核心 / 8.4 收尾引用 / 8.5 与 §4 关系）
- [x] AC2: §8.2 三条硬约束全部落地
- [x] AC3: §8.3 三项内容核心 + 反模糊口径"本轮无剩余风险"
- [x] AC4: §8.4 固定引用格式 `正式版：deliveries/YYYY-MM-DD-<slug>.md`
- [x] AC5: `lifecycle.md` P5 段已出现 `delivery-summary.md § 8` 引用
- [x] AC6: README / rule-card / CLAUDE.md / 目录结构 / 读取顺序未改动
- [x] AC7: `delivery-summary.md` 单文件自包含验证通过
- [x] AC8: `.ai/` 四份产物按 schema 全字段回填
- [x] AC9: `deliveries/2026-04-20-chat-recap-style.md` 结构符合 §4 七小节
- [x] AC10: 本轮对话收尾摘要符合 §8 风格

# Verification Results
- AC1: grep `delivery-summary.md` 命中 `## 8.`、`### 8.1`–`### 8.5` 全部 5 个锚点
- AC2: grep 命中 `3–6 句`、`禁止输出任何编号小节标题`、`禁止铺排长 bullet` 三条硬约束文本
- AC3: grep 命中 `本轮无剩余风险`；人工核查 §8.3 三项内容均存在
- AC4: grep 命中固定引用格式字面量
- AC5: grep `lifecycle.md` 命中 `delivery-summary.md § 8`，上下文位于 P5 Verify 段"必须产物"条目
- AC6: `git diff HEAD~<N> -- Coder/README.md templates/rule-card.md Coder/CLAUDE.md` 输出为空
- AC7: 人工通读 `delivery-summary.md`，只读本文件即可理解文件层与对话层两种表达
- AC8: 人工对照 concept/acceptance/tech-plan/verify schema §2 必填字段清单，逐项命中
- AC9: 人工对照 `delivery-summary.md §4` 七个小节，逐项命中
- AC10: 本轮 P5 收尾对话摘要将在 Step 6 输出，届时对照 §8 三组约束逐项核查

# Gate Coverage
- 通用质量门禁：规则仓库无单元测试门禁，采用 grep + 人工核查 + schema 对齐三组手段
- Active Profiles：未命中任何 profile，N/A
- Tech Plan Alignment：TECH_PLAN.md 中 Design Decisions 全部兑现（选方案 A、3–6 句硬上限、反模糊口径、未命中 profile）
- References Compliance：本轮无外部参考资料，N/A

# Remaining Risks
- 规则密度：`delivery-summary.md` 从 7 节扩到 8 节，文件偏长但职责聚合。若未来对话层约束继续增加（≥ 3 条），应评估拆分到独立文件
- 误用风险：§8.3 反模糊口径兜底"无风险必须显式声明"，但仍需观察实际 AI 输出是否守约

# Handoff / Next Step
- 本轮任务已闭合，无跨会话接力需求
```

- [ ] **Step 5: 核对 `.ai/VERIFY_REPORT.md` 必填字段**

对照 `verify-schema.md §2`：Verification Summary / AC Status / Verification Results / Gate Coverage / Remaining Risks / Handoff / Next Step — 6 项全部存在。

- [ ] **Step 6: 生成 `deliveries/2026-04-20-chat-recap-style.md`（dogfooding 首次应用）**

本次改动本身构成一次完整交付，且满足 `delivery-summary.md §2` 的四个触发条件（主要目标完成、验收达成、有明确验证结论、已闭环）。按 `delivery-summary.md §4` 正式结构写入 `deliveries/2026-04-20-chat-recap-style.md`：

模板骨架（实际落盘时按本次真实交付填充）：

```md
# Chat Recap Style 交付总结 — 2026-04-20

## 1. 本次交付目标
- 为 Delivery Summary 触发时刻新增对话层风格约束
- 让 AI 对话框输出"讲人话"，`deliveries/` 文件层保持正式结构

## 2. 已完成内容
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` 新增 §8 对话内人话摘要（5 子节）
- `Coder/20_Workflow_Lifecycle/lifecycle.md` P5 Verify 段补一句 §8 引用
- 按 butler SOP 全链路产出 `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md`
- 本交付总结自身作为新 §8 规则的首次 dogfood 应用

## 3. 关键变更 / 用户可感知变化
- Delivery Summary 触发时，AI 对话层输出从"复述 7 小节文件结构"切换为"3–6 句中文散文 + 正式版路径引用"
- 文件层 `deliveries/*.md` 结构不变
- §8 明确禁止编号小节标题与长 bullet 铺排，并要求显式声明"本轮无剩余风险"

## 4. 高层影响范围
- 规则文件：`Coder/20_Workflow_Lifecycle/delivery-summary.md`、`Coder/20_Workflow_Lifecycle/lifecycle.md`
- 决策记录：`.ai/CONCEPT.md`、`.ai/AC_LIST.md`、`.ai/TECH_PLAN.md`、`.ai/VERIFY_REPORT.md`
- 交付文件：`deliveries/2026-04-20-chat-recap-style.md`
- 未影响：`Coder/README.md`、`templates/rule-card.md`、`Coder/CLAUDE.md`、目录结构、读取顺序

## 5. 验证方式与结果摘要
- grep 验证：§8 五个子节锚点、三条硬约束关键词、反模糊口径、固定引用格式均命中
- grep 验证：`lifecycle.md` P5 段 `delivery-summary.md § 8` 引用命中
- git diff 验证：README / rule-card / CLAUDE.md 未改动
- 人工验证：`delivery-summary.md` 单文件自包含可读
- schema 验证：`.ai/` 四份文件按 concept/acceptance/tech-plan/verify schema 全字段回填
- 详见 `.ai/VERIFY_REPORT.md`，AC1–AC10 全部满足

## 6. 已知剩余风险 / 延后事项
- 规则密度：`delivery-summary.md` 从 7 节扩到 8 节。若未来对话层约束继续增加（≥ 3 条），应评估拆分到独立 `chat-recap.md`
- 误用观察：§8.3 反模糊口径已兜底"无风险必须显式声明"，但实际 AI 输出守约程度仍需后续观察

## 7. 可选引用
- spec: `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md`
- plan: `docs/superpowers/plans/2026-04-20-chat-recap-style.md`
- AC 清单: `.ai/AC_LIST.md`
- 技术方案: `.ai/TECH_PLAN.md`
- 验证报告: `.ai/VERIFY_REPORT.md`
- 相关 commits: 见 `git log feat/chat-recap-style`
```

- [ ] **Step 7: 最终 commit（.ai/VERIFY_REPORT.md + deliveries/*.md）**

```bash
git add .ai/VERIFY_REPORT.md deliveries/2026-04-20-chat-recap-style.md
git commit -m "$(cat <<'EOF'
docs(p5): verify report + delivery summary for chat-recap-style

按 verify-schema 回填 AC1-AC10 验证结果；按新 §4 结构写交付总结；
dogfood 首次按新 §8 规则输出对话层收尾摘要。
EOF
)"
```

- [ ] **Step 8: 输出对话层收尾摘要（§8 首次实战）**

在对话框内输出一段 3–6 句的中文散文，严格遵守 §8.2 / §8.3 / §8.4：

- 覆盖做了什么、有没有风险、建议下一步
- 无编号小节、无长 bullet 铺排
- 若无剩余风险，显式说 "本轮无剩余风险"
- 最后一行引用 `正式版：deliveries/2026-04-20-chat-recap-style.md`

若输出违反 §8，说明规则措辞不够强，需回到 Task 1 Step 2 加强约束词。

预期：全部交付闭环，可向用户交付。

---

## Self-Review 记录

已自审（含 butler 产物链扩展后的重新核查）：

- **Spec 覆盖**：spec §4.2 / §4.3 / §5 全部条目映射到 Task 1 / Task 2 / Task 3。§6 风险"规则密度"通过 §8 紧凑编号（5 个子节）控制；"被误用"通过 8.3 反模糊口径兜底；"双写漂移"通过 8.5 明确"结论真源以文件为准"。
- **butler 产物链覆盖**：Task 0 按 concept/acceptance/tech-plan schema 产出 P1-P3 产物；Task 3 Step 4 按 verify schema 产出 P5 产物；Task 3 Step 6 按 delivery-summary §4 产出最终交付总结。覆盖 `.ai/CONCEPT.md` / `.ai/AC_LIST.md` / `.ai/TECH_PLAN.md` / `.ai/VERIFY_REPORT.md` / `deliveries/<date>-<slug>.md` 全链路。
- **占位符扫描**：无 TBD / TODO / "类似 Task N" 等。所有 §8 节内容与 `.ai/` 模板内容均以完整 Markdown 片段给出，可直接粘贴。
- **类型一致性**：§8 子节编号（8.1–8.5）与 Task 1 Step 3 grep 清单一一对应；`delivery-summary.md § 8` 引用在 Task 2 / Task 3 中保持同一格式（带反引号、带空格）。
- **路径一致性**：`deliveries/YYYY-MM-DD-<slug>.md` 在 spec、§8.4、Task 0 AC_LIST、Task 3 Step 6 多处格式完全一致。
- **AC 与 Verification 对齐**：AC1–AC10 与 Task 3 Step 4 VERIFY_REPORT 中的 AC Status 一一对应。

---

## 执行交接

计划已保存到 `docs/superpowers/plans/2026-04-20-chat-recap-style.md`。两种执行方式二选一：

1. **Subagent-Driven（推荐）** — 每个 Task 派一个新 subagent 执行，Task 间做 review，迭代快。
2. **Inline Execution** — 在当前会话内直接按 Task 顺序执行，检查点处你过目。

你选哪个？
