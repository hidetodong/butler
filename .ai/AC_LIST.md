# Goal

- 修复 Bucket F（低风险 Nice to Have 批处理）5 条问题。

# In Scope

- N-1: `architecture-overview § 3` 空旷处理。
- N-2: `logic-protocol § 4.2` 拆 H4 子标题。
- N-3: `architecture-overview § 2.2` 硬编码 profile 文件名通用化。
- N-4: `HUMAN_GUIDE` 第 8 节规则速查图扩展（展开 30/40 子目录）。
- N-7: `context-persistence § 3` task-state 单选 `.md` 还是保留双选。

# Out of Scope

- N-5（local-constraints schema 新增）— Bucket G。
- N-6（Domain_Stack_Profiles 目录重组）— Bucket H。

# Acceptance Checklist

- [ ] **N-1** `architecture-overview § 3` 不再是 3 行空旷段，方案待拍板
- [ ] **N-2** `logic-protocol § 4.2` 的 Fallback 段升级为 `#### Fallback（skill 不可用或调用失败时）` H4 标题
- [ ] **N-3** `architecture-overview § 2.2` 的 profile 文件清单改为通用描述（"按 `10_Domain_Stack_Profiles/` 下实际命中的 profile 启用"）
- [ ] **N-4** `HUMAN_GUIDE § 8` 速查图展开 `30_Quality_Gate/` 与 `40_Context_Management/` 的子文件
- [ ] **N-7** `context-persistence § 3` 状态载体的 JSON/MD 双形式处理，方案待拍板

# Verification Method

- **N-1**：通读 architecture-overview.md，无单独 3 行的空旷章节；指针/合并/改名等动作均使读者能直接定位读取顺序的 SSOT（README）。
- **N-2**：`grep -n '^#### Fallback' Coder/00_System_Prompt/logic-protocol.md` 命中。
- **N-3**：`grep -n 'vue3-standard\|typescript-rules\|build-tooling' Coder/architecture-overview.md` 在 § 2.2 范围零命中（具体文件名不再出现）。
- **N-4**：HUMAN_GUIDE 第 8 节的目录树包含 `linting.md` / `testing-strategy.md` / `review-standard.md`（30 子）以及 `context-persistence.md` / `handoff-spec.md` / `role-switch.md`（40 子）。
- **N-7**：根据方案决定 — 若单选则 § 3 只提 `task-state.md`；若保留双选则补充明确的"何时用 JSON / 何时用 MD"判断条件。

# Open Questions / Risks

## ❓ 待拍板 - N-1 方案选择

`architecture-overview.md § 3` 当前内容（Bucket A 后）：

```
## 3. 启用顺序

具体读取顺序以 `README.md § 读取顺序` 为准。本文件仅负责说明三层分工的职责边界与 profile 条件生效的语义，不重复列出顺序清单，避免多处漂移。
```

只剩 3 行，结构空旷。

### 方案 A — 删除 § 3，把指针句作为 § 2 末尾的引导

- 删除 `## 3. 启用顺序` 整段。
- 把指针句移到 § 2 三层分工说明结尾，作为"了解具体读取顺序请见 README"的桥梁。
- 后续章节序号上移（§ 4 → § 3、§ 5 → § 4、§ 6 → § 5）。
- **优点**：彻底消除空旷段；章节连贯。
- **缺点**：序号变化，引用本文件章节的地方需同步（实际上没有外部引用 architecture-overview 的某具体章节）。

### 方案 B（推荐）— 把 § 3 与 § 4 合并为"启用顺序与生效规则"

- 章节标题改为 `## 3. 启用顺序与生效规则`。
- 内容：先一句指针（"具体读取顺序以 README 为准"），然后接 § 4 现有的"默认生效 / 条件生效 / 高优先级业务约束"内容。
- 章节数减 1（§ 3 + § 4 合并），后续序号上移。
- **优点**：两个相邻章节在语义上本就紧密（启用顺序 + 生效规则都是讲规则如何加载与作用）；合并后内容更紧凑。
- **缺点**：合并后的章节略长（约 15 行）。

### 方案 C — 重命名 § 3 为"与 README 的关系"

- 标题改为 `## 3. 与 README 读取顺序的关系`，正文不变。
- **优点**：标题更精准。
- **缺点**：3 行的空旷感仍在。

---

## ❓ 待拍板 - N-7 方案选择

`context-persistence.md § 3` 当前内容：

```
## 3. 状态载体

推荐载体：`.ai/task-state.json` 或 `.ai/task-state.md`。

按任务复杂度与协作方式选择 JSON 或 Markdown。载体的目标是保留**当前有效结论**，不是完整思考过程。
```

### 方案 α（推荐）— 单选 `.md`

- 改为"载体：`.ai/task-state.md`。按任务复杂度调整内容粒度，但格式保持 Markdown 以保证人类与 AI 双向可读"。
- **理由**：`mcv-deployment.md § 2` 部署时只建 `task-state.md`；butler SOP 当前没有自动化机器处理 task-state 的需求；统一格式降低跨项目认知成本。
- **代价**：丢失"复杂任务用 JSON"的潜在用法（但当前没有实际 JSON 使用案例）。

### 方案 β — 保留双选，补充明确的判断条件

- 改为"默认载体：`.ai/task-state.md`；当任务存在大量结构化字段、需要被工具脚本读取时，可改为 `.ai/task-state.json`"。
- **优点**：保持灵活性。
- **缺点**：判断条件依然主观；很可能没有任务真的用 JSON。

### 方案 γ — 两选保留但不补判断（即不动）

- 不推荐 — 等于不修复。

---

## 推荐方案（无取舍 3 条直接执行）

- **N-2**：把 `Fallback（skill 不可用或调用失败时）：` 改为 `#### Fallback（skill 不可用或调用失败时）`（升级为 H4 标题）；其他段不动。
- **N-3**：`architecture-overview § 2.2 包含：` 列表改为单一指针："`10_Domain_Stack_Profiles/` 下的所有 profile 文件，按当前项目命中的技术栈、语言或构建形态按需启用"。
- **N-4**：`HUMAN_GUIDE § 8` 速查图扩展 30 子（linting / testing-strategy / review-standard）和 40 子（context-persistence / handoff-spec / role-switch）。

---

## 风险

- 全是文档级改动，无运行时影响。
- N-1 章节序号变化的影响面经 grep 确认为零（无外部引用 architecture-overview 的某序号章节）。
- N-7 方案 α 把 JSON 选项移除，未来如真有 JSON 需求可重新加回（属可逆决策）。

---

# 请回复

1. **N-1 方案**：A / B / C
2. **N-7 方案**：α / β / γ

其余 N-2 / N-3 / N-4 默认按推荐方案执行。两个拍板后我进 P3。
