# 对话内人话摘要（Chat Recap）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `Coder/20_Workflow_Lifecycle/delivery-summary.md` 新增 §8 对话内人话摘要，并在 `lifecycle.md` P5 段补充对 §8 的显式引用，让 AI 在 Delivery Summary 触发时刻的对话层输出走"讲人话"口径、文件层保持正式结构。

**Architecture:** 纯 Markdown 规则文件改动。单规则文件扩展（§8），外加一处跨文件引用（lifecycle.md P5）。不新增文件、不改目录结构、不改读取顺序。

**Tech Stack:** Markdown + frontmatter。无代码、无测试框架。验证手段为人工阅读 + grep 关键词 + 对照 spec 验收清单。

**Spec 路径：** `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md`

---

## 文件结构

本计划只修改两个既有文件，不新建任何文件：

- **Modify:** `Coder/20_Workflow_Lifecycle/delivery-summary.md`
  - 在 §7 "与执行流程的关系" 之后新增 §8 "对话内人话摘要"
- **Modify:** `Coder/20_Workflow_Lifecycle/lifecycle.md`
  - 在 P5 Verify 段现有 Delivery Summary 描述之后，补一句引用 §8

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

## Task 3: 终审与未改动项确认

**Files:**
- Read: `Coder/README.md`
- Read: `templates/rule-card.md`
- Read: `Coder/CLAUDE.md`
- Read: `docs/superpowers/specs/2026-04-20-chat-recap-style-design.md`

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

- [ ] **Step 4: 对照 spec §5 验收清单做最终勾选**

逐项核对 spec §5 的 7 条验收标准：

1. §8 出现且字段完整 → Task 1 Step 3/4 已验。
2. 3 条硬约束（3–6 句、禁止编号小节标题、禁止长 bullet） → Task 1 Step 3 已验。
3. 3 项内容核心 + 反模糊口径 → Task 1 Step 3 已验。
4. 固定引用格式 → Task 1 Step 3 已验。
5. lifecycle.md P5 引用 §8 → Task 2 Step 3/4 已验。
6. README / rule-card / CLAUDE.md / 目录结构 / 读取顺序未改 → Task 3 Step 1 已验。
7. 单文件可读懂两种表达 → Task 3 Step 2 已验。

7 项全部命中则任务闭环。任一未命中，回到对应 Task。

- [ ] **Step 5: 生成本轮 Delivery Summary（dogfooding 首次应用）**

本次改动本身构成一次完整交付，且满足 `delivery-summary.md §2` 的四个触发条件（主要目标完成、验收达成、有明确验证结论、已闭环）。因此应按**新规则**自行产出一次 Delivery Summary：

- 在项目根目录 `deliveries/` 下新建 `deliveries/2026-04-20-chat-recap-style.md`，按 `delivery-summary.md §4` 正式结构填写。
- 在对话框内同步输出符合 §8 的 3–6 句人话摘要，末尾引用该文件路径。

这一步既是交付、也是对新规则的首次实际演练。若此处产出的对话摘要仍带编号小节或长 bullet，说明规则措辞不够强，需回到 Task 1 Step 2 加强约束词。

- [ ] **Step 6: 最终 commit（Delivery Summary 文件）**

```bash
git add deliveries/2026-04-20-chat-recap-style.md
git commit -m "$(cat <<'EOF'
docs(deliveries): add 2026-04-20 chat recap style delivery summary

dogfood 首次按新规则产出 Delivery Summary，验证 §4 文件层
结构与 §8 对话层风格可并行落地。
EOF
)"
```

预期：commit 成功。至此全部交付闭环。

---

## Self-Review 记录

已自审：

- **Spec 覆盖**：spec §4.2 / §4.3 / §5 全部条目映射到 Task 1 / Task 2 / Task 3。§6 风险"规则密度"通过 §8 紧凑编号（5 个子节）控制；"被误用"通过 8.3 反模糊口径兜底；"双写漂移"通过 8.5 明确"结论真源以文件为准"。
- **占位符扫描**：无 TBD / TODO / "类似 Task N" 等。所有 §8 节内容以完整 Markdown 片段给出，可直接粘贴。
- **类型一致性**：§8 子节编号（8.1–8.5）与 Task 1 Step 3 grep 清单一一对应；`delivery-summary.md § 8` 引用在 Task 2 / Task 3 中保持同一格式（带反引号、带空格）。
- **路径一致性**：`deliveries/YYYY-MM-DD-<slug>.md` 在 spec、§8.4、Task 3 Step 5 三处格式完全一致。

---

## 执行交接

计划已保存到 `docs/superpowers/plans/2026-04-20-chat-recap-style.md`。两种执行方式二选一：

1. **Subagent-Driven（推荐）** — 每个 Task 派一个新 subagent 执行，Task 间做 review，迭代快。
2. **Inline Execution** — 在当前会话内直接按 Task 顺序执行，检查点处你过目。

你选哪个？
