# Goal

- 按 N-1 方案 B（§ 3 + § 4 合并 + 序号重排）、N-7 方案 α（task-state 单选 `.md`），以及 N-2 / N-3 / N-4 的推荐方案，对 Bucket F 5 条 Nice to Have 执行最小范围修复。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 改动点 |
|---|---|---|---|
| 1 | `Coder/architecture-overview.md` | N-1 + N-3 | 2（§ 2.2 通用化 + § 3 合并 § 4 重排序号） |
| 2 | `Coder/00_System_Prompt/logic-protocol.md` | N-2 | 1（Fallback 段升 H4） |
| 3 | `HUMAN_GUIDE.md` | N-4 | 1（§ 8 速查图展开 30/40 子目录） |
| 4 | `Coder/40_Context_Management/context-persistence.md` | N-7 | 1（§ 3 载体单选 .md） |

共 4 个文件，5 处 edit。

# Interface / Contract

- 无契约变更。所有改动为表述精简、结构清晰化。
- N-7 把 `task-state` 从"JSON 或 MD 双选"收敛为"单选 MD"，算轻度决策变化，影响面仅 `.ai/task-state.md` 的格式约定；已在 `mcv-deployment.md § 2` 部署规则中以 `.md` 为默认，本改动让规则自洽。

# State / Boundary

- 不动 lifecycle / mcv-deployment / mcv-update / maintenance-boundaries / schema 系列等核心流程文件。
- 不动 templates / scripts / Extension。
- 不重组 `10_Domain_Stack_Profiles/` 目录（N-6，属 Bucket H）。
- 不新建 schema（N-5，属 Bucket G）。

# Design Decisions

1. **N-1 合并后章节编号**：
   - § 3（旧）+ § 4（旧）→ § 3（新）启用顺序与生效规则
   - § 5（旧）→ § 4（新）在生命周期中的作用点
   - § 6（旧）→ § 5（新）判断原则
   - grep 确认无外部引用具体章节序号，序号变化零外部影响。
2. **N-3 清单改描述**：避免枚举具体文件名（未来新增 profile 不必回来改这里）；描述词改为"按当前项目命中的技术栈、语言或构建形态按需启用"。
3. **N-2 H4 层级**：`Fallback（skill 不可用或调用失败时）：` 末尾冒号随 H4 标题去掉（H4 不带冒号更标准）。处理规则段保持无标题（作为表格下的附属说明）。
4. **N-4 速查图子级**：30/40 各列 3 个子文件，每项附一句职责说明，与现有 00/20 两目录的风格一致。
5. **N-7 单选理由**：mcv-deployment 部署只建 `.md`；butler SOP 目前没有自动化机器读取 task-state 的场景；JSON 一旦回退为必需可再加回（可逆决策）。

# Execution Steps

## Edit 1 — `architecture-overview.md § 2.2` 通用化（N-3）

**old**:
```
### 2.2 Domain / Stack Profiles

包含：

- `10_Domain_Stack_Profiles/vue3-standard.md`
- `10_Domain_Stack_Profiles/typescript-rules.md`
- `10_Domain_Stack_Profiles/build-tooling.md`

职责：
```

**new**:
```
### 2.2 Domain / Stack Profiles

包含：

- `10_Domain_Stack_Profiles/` 下的所有 profile 文件，按当前项目命中的技术栈、语言或构建形态按需启用。

职责：
```

## Edit 2 — `architecture-overview.md § 3 + § 4` 合并与序号重排（N-1）

**old**（L65-99 整段）:
```
## 3. 启用顺序

具体读取顺序以 `README.md § 读取顺序` 为准。本文件仅负责说明三层分工的职责边界与 profile 条件生效的语义，不重复列出顺序清单，避免多处漂移。

## 4. 生效规则

- **默认生效**：SOP Core。
- **条件生效**：Domain / Stack Profiles。
- **高优先级业务约束**：Business Extension。

换句话说：

- 先按通用 SOP 定义任务怎么做。
- 再按业务约束决定任务为什么这样做。
- 最后按命中的 profile 细化任务具体怎么落地。

## 5. 在生命周期中的作用点

- **P1 Analysis**：识别项目类型，并决定是否启用 profile。
- **P2 Acceptance**：只把已激活 profile 对应的完成定义纳入 AC。
- **P3 Design**：将已激活 profile 作为设计约束。
- **P4 Execute**：执行时只应用已激活的 profile 细则。
- **P5 Verify**：按"通用质量门禁 + 已激活 profile"进行验证。

## 6. 判断原则
```

**new**:
```
## 3. 启用顺序与生效规则

具体读取顺序以 `README.md § 读取顺序` 为准；本文件仅负责说明三层分工的职责边界与 profile 条件生效的语义。生效规则：

- **默认生效**：SOP Core。
- **条件生效**：Domain / Stack Profiles。
- **高优先级业务约束**：Business Extension。

换句话说：

- 先按通用 SOP 定义任务怎么做。
- 再按业务约束决定任务为什么这样做。
- 最后按命中的 profile 细化任务具体怎么落地。

## 4. 在生命周期中的作用点

- **P1 Analysis**：识别项目类型，并决定是否启用 profile。
- **P2 Acceptance**：只把已激活 profile 对应的完成定义纳入 AC。
- **P3 Design**：将已激活 profile 作为设计约束。
- **P4 Execute**：执行时只应用已激活的 profile 细则。
- **P5 Verify**：按"通用质量门禁 + 已激活 profile"进行验证。

## 5. 判断原则
```

注：原 § 6 判断原则的标题由 `## 6.` 改为 `## 5.`；其内容（第 91-99 行）不动，但章节序号改变，需要一次 Edit 覆盖这一行（或随大块 Edit 一起处理）。

## Edit 3 — `logic-protocol § 4.2` Fallback 升 H4（N-2）

**old**:
```
Fallback（skill 不可用或调用失败时）：

- 若目标 skill 未安装、认证失败或调用超时，**不得**自行使用 WebFetch 等工具越权访问外部资源。
```

**new**:
```
#### Fallback（skill 不可用或调用失败时）

- 若目标 skill 未安装、认证失败或调用超时，**不得**自行使用 WebFetch 等工具越权访问外部资源。
```

## Edit 4 — `HUMAN_GUIDE § 8` 速查图展开 30/40（N-4）

**old**（L182-183）:
```
├── 30_Quality_Gate/           # 质量门禁
├── 40_Context_Management/     # 上下文治理（长任务必读）
```

**new**:
```
├── 30_Quality_Gate/           # 质量门禁
│   ├── linting.md             # 提交前自检清单
│   ├── testing-strategy.md    # 测试分层与验收映射
│   └── review-standard.md     # 通用审计准则
├── 40_Context_Management/     # 上下文治理（长任务必读）
│   ├── context-persistence.md # 状态外化与阶段结晶
│   ├── handoff-spec.md        # 02_SESSION_HANDOFF.md 格式契约
│   └── role-switch.md         # Architect/Coder/Reviewer 角色切换
```

## Edit 5 — `context-persistence § 3` 单选 .md（N-7）

**old**:
```
## 3. 状态载体

推荐载体：`.ai/task-state.json` 或 `.ai/task-state.md`。

按任务复杂度与协作方式选择 JSON 或 Markdown。载体的目标是保留**当前有效结论**，不是完整思考过程。
```

**new**:
```
## 3. 状态载体

载体：`.ai/task-state.md`。按任务复杂度调整内容粒度，但格式保持 Markdown 以保证人类与 AI 双向可读。载体的目标是保留**当前有效结论**，不是完整思考过程。
```

# Verification Plan

- **N-1**：
  - `grep -nE '^## [0-9]\.' Coder/architecture-overview.md` 返回 5 个章节（1/2/3/4/5），无 6。
  - § 3 标题包含 "启用顺序与生效规则"；章节内容包含 `README.md § 读取顺序` 指针和三层"默认生效/条件生效/高优先级"枚举。
- **N-2**：`grep -nE '^#### Fallback' Coder/00_System_Prompt/logic-protocol.md` 命中 1 处。
- **N-3**：`grep -nE 'vue3-standard\|typescript-rules\|build-tooling' Coder/architecture-overview.md` 返回 0 命中（具体文件名已去除）。
- **N-4**：`grep -n 'linting.md\|testing-strategy.md\|review-standard.md\|context-persistence.md\|handoff-spec.md\|role-switch.md' HUMAN_GUIDE.md` 在 § 8 范围全部命中。
- **N-7**：
  - `grep -n 'task-state\.json' Coder/40_Context_Management/context-persistence.md` 在 § 3 范围返回 0；
  - `grep -n 'task-state\.md' Coder/40_Context_Management/context-persistence.md` 在 § 3 范围命中 1 处。
- `git diff --stat` 应仅显示 4 个规则文件变更。

# Risks / Open Questions

- **风险 1**：N-1 大段 Edit（覆盖 35 行）需要精确 old_string；同文件另一个 Edit (N-3) 改的是更前的行，两者不重叠，但 Edit 工具对同文件多个 edit 会串行处理，需保证顺序（先做 N-3 还是先做 N-1 都可以，因为位置不重叠）。本 TECH_PLAN 按"先 N-3 再 N-1"顺序执行。
- **风险 2**：N-7 删除 JSON 选项后，如未来有自动化脚本读取 task-state，需要重新评估。属可逆决策。
- **开放问题**：无。
