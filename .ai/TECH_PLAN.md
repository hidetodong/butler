# Goal

- 按方案 Y 修复 Bucket D：`templates/CLAUDE.md.template` 改造为骨架 + 占位符（强制约束段替换为 `{{RULE_CARD_CONTENT}}`），`templates/rule-card.md` 保持作 SSOT 不动；同步更新 `mcv-deployment.md § 3` 的部署描述与 `CLAUDE.md` 的"保持模板同步"约束。

# Files / Modules to Change

| # | 文件 | 涉及 AC | 改动方式 |
|---|---|---|---|
| 1 | `templates/CLAUDE.md.template` | D-1 | Write 整体重写（删除强制约束段，替换为占位符；更新顶部注释） |
| 2 | `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3` | D-2 | Edit 重写规则注入流程为 5 步 |
| 3 | `CLAUDE.md`（butler 项目根） | D-3 | Edit 第 20 行约束改为"模板单一来源" |

不动：`templates/rule-card.md`（仍为浓缩规则 SSOT）、其他规则文件、scripts、Extension。

# Interface / Contract

- **新模板契约**：`CLAUDE.md.template` 包含两个占位符：
  - `{{RULE_CARD_CONTENT}}`：部署时由 AI 用 `rule-card.md` 中 `## 角色` 起的章节内容替换（去掉 rule-card 的 H1 `# Butler 浓缩规则卡` 和顶部 `> 约 800 tokens...` 引述）。
  - `{{BUTLER_PATH}}`：部署时由 AI 用 butler 仓库的绝对路径替换。
- **部署流程契约**：mcv-deployment.md § 3 从"两部分组成"改为"5 步生成"，所有步骤显式可枚举。
- **同步契约**：CLAUDE.md（butler 项目根）的"保持模板同步"约束改为"模板单一来源"，明确不再需要手工双写。

# State / Boundary

- 部署后目标项目 CLAUDE.md 的**最终内容**与现行版本等价（占位符替换后所有段落齐全：角色 / 强制工作流 / 回退规则 / 基地车部署 / 执行纪律 / 完整规则参考 / 项目特定约束）。
- 不引入 markdown include 等非标准机制 —— 仅靠简单字符串占位符替换实现。
- rule-card.md 的内部结构（H1 + 引述 + H2 章节）不动，部署时 AI 按规则跳过 H1 和引述。

# Design Decisions

1. **占位符位置**：`{{RULE_CARD_CONTENT}}` 直接放在 `# 项目工程协作规则` H1 之下，不外包一层 `## 强制约束（内联规则卡）` H2。这样 rule-card 的 H2（`## 角色 / ## 强制工作流` 等）替换进来后自然作为 H2 顶级章节，与"完整规则参考""项目特定约束"等同级，结构平铺。
2. **rule-card 文件不动**：保留独立可读性（H1 标题 + tokens 提示），AI 在部署时按规则跳过这两行；规则在 mcv-deployment § 3 第 2 步显式说明。
3. **mcv-deployment § 3 改写为 5 步**：每步动作可独立检查，AI 部署时能逐步推进；末尾"已存在 CLAUDE.md 不覆盖"的兜底规则保留。
4. **CLAUDE.md（butler 项目根）约束更名**：从"保持模板同步"改为"模板单一来源"，更准确反映新机制。
5. **Write vs Edit**：CLAUDE.md.template 改动幅度大（删除约 30 行重复内容 + 加占位符注释 + 改顶部说明），用 Write 整体重写；其他两个文件用 Edit 局部修改。

# Execution Steps

## Step 1 — Write `templates/CLAUDE.md.template` 整体重写

新文件内容如下（约 32 行，对比原 70 行）：

```markdown
# 项目工程协作规则

<!--
  本文件是 AI 部署基地车时生成 CLAUDE.md 的参考模板。
  正常流程下由 AI 在 mcv-deployment.md § 3 规则注入步骤中自动生成：
  - 用 templates/rule-card.md 中 ## 角色 起的章节内容替换下方 {{RULE_CARD_CONTENT}} 占位符
  - 用实际路径替换 {{BUTLER_PATH}} 占位符
  - 根据侦察结果填写「项目特定约束」章节

  人类通常不需要手动编辑此模板。修改强制约束规则只需更新 templates/rule-card.md。
-->

{{RULE_CARD_CONTENT}}

## 完整规则参考（深度阅读）

当需要查阅完整规则细节时，按以下顺序读取：

1. `{{BUTLER_PATH}}/Coder/00_System_Prompt/identity.md`
2. `{{BUTLER_PATH}}/Coder/00_System_Prompt/logic-protocol.md`
3. `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/lifecycle.md`
4. `{{BUTLER_PATH}}/Coder/30_Quality_Gate/`
5. `{{BUTLER_PATH}}/Coder/40_Context_Management/`（长任务时）
6. `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/mcv-deployment.md`（新项目接入时）

阶段产物模板：
- P1: `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/concept-schema.md`
- P2: `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/acceptance-schema.md`
- P3: `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/tech-plan-schema.md`
- P5: `{{BUTLER_PATH}}/Coder/20_Workflow_Lifecycle/verify-schema.md`

## 项目特定约束

<!-- 在这里补充本项目的特定约束，例如：-->
<!-- - 本项目使用 Vue 3 + TypeScript，启用对应 Domain Profile -->
<!-- - 本项目的 API 文档在 Confluence: https://... -->
<!-- - /legacy 目录下的旧代码允许局部放宽类型检查 -->
```

## Step 2 — Edit `mcv-deployment.md § 3` 重写流程

**old**（L63-70）:
```
## 3. 规则注入 (Rule Injection)

在目标项目根目录生成 `CLAUDE.md`（或目标 AI 工具对应的配置文件），内容由两部分组成：

1. **内联规则卡**：从 butler 仓库的 `templates/rule-card.md` 读取浓缩规则，直接写入文件正文。内联而非引用，确保 AI 在高注意力区域读到核心约束。
2. **完整规则指针**：附上 butler 仓库的绝对路径，列出深度阅读的文件清单（identity.md、logic-protocol.md、lifecycle.md 等）。路径在部署时由 AI 根据实际环境自动填入，不使用占位符。

若目标项目已存在 `CLAUDE.md`，不得覆盖，应将规则卡追加到现有内容末尾，并用分隔线标记 butler 规则区块。
```

**new**:
```
## 3. 规则注入 (Rule Injection)

在目标项目根目录生成 `CLAUDE.md`（或目标 AI 工具对应的配置文件）。流程：

1. 读取模板骨架 `templates/CLAUDE.md.template`。
2. 用 `templates/rule-card.md` 中 `## 角色` 起的章节内容替换 `{{RULE_CARD_CONTENT}}` 占位符（不包含 rule-card.md 的 H1 与顶部引述）；这是浓缩规则卡的内联，确保 AI 在高注意力区域读到核心约束。
3. 用 butler 仓库的绝对路径替换 `{{BUTLER_PATH}}` 占位符，让深度阅读指针指向真实路径。
4. 在"项目特定约束"段填入侦察结果（识别到的技术栈、project 类型、特殊约束等）。
5. 写入目标项目根目录 `CLAUDE.md`。

若目标项目已存在 `CLAUDE.md`，不得覆盖，应将以上生成的内容追加到现有内容末尾，并用分隔线标记 butler 规则区块。
```

## Step 3 — Edit butler 仓根 `CLAUDE.md` 第 20 行

**old**:
```
4. **保持模板同步**：修改核心流程后检查 `templates/` 下的浓缩规则卡是否需要同步更新。
```

**new**:
```
4. **模板单一来源**：浓缩规则的 SSOT 是 `templates/rule-card.md`；`templates/CLAUDE.md.template` 通过 `{{RULE_CARD_CONTENT}}` 占位符引用 rule-card，无需手工双写。修改强制约束只需更新 `templates/rule-card.md`。
```

# Verification Plan

- **D-1（去重）**：
  - `wc -l templates/CLAUDE.md.template` 显著缩短（约 70 → 约 32 行）。
  - `grep -c '强制工作流\|回退规则\|执行纪律' templates/CLAUDE.md.template` 返回 0（重复内容已删除）。
  - `grep -c 'RULE_CARD_CONTENT' templates/CLAUDE.md.template` 返回 1（占位符就位）。
- **D-2（部署描述对齐）**：
  - `grep -n 'RULE_CARD_CONTENT\|CLAUDE.md.template' Coder/20_Workflow_Lifecycle/mcv-deployment.md` 在 § 3 内命中，描述与 templates 实际状态一致。
  - 通读 § 3 五步，可独立执行。
- **D-3（同步约束更新）**：
  - `grep -n '模板单一来源' CLAUDE.md` 命中。
  - 旧措辞 `保持模板同步` 在 CLAUDE.md 中零命中。
- **整体内容等价性**：手工对照部署后效果（rule-card.md 的 ## 角色起章节 + CLAUDE.md.template 的剩余结构）= 现行 CLAUDE.md.template 内容。

# Risks / Open Questions

- **风险 1**：占位符替换是字符串机械替换，rule-card.md 内容若包含特殊字符（如 `{{...}}` 或 markdown 语法歧义），可能影响替换。审查 rule-card 当前内容，无此类风险。
- **风险 2**：mcv-deployment § 3 第 2 步要求 AI "去掉 rule-card.md 的 H1 与顶部引述"，对 AI 是显式可执行的指令，但若 rule-card 未来增加更多元数据（如 frontmatter），这条规则需要同步更新。当前 rule-card 没有 frontmatter，本轮无需处理。
- **开放问题**：无。
