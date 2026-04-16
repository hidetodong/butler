# Goal

- 按方案 Alpha 修复 Bucket C：把 `mode-switch.md` 重命名为 `role-switch.md`，内部 `Mode` → `Role`、`模式` → `角色` 全量替换，并同步 2 处外部文件名引用。

# Files / Modules to Change

| # | 文件/动作 | 涉及 AC | 改动点 |
|---|---|---|---|
| 1 | `Coder/40_Context_Management/mode-switch.md` → `role-switch.md` | C-1 | git mv 重命名 |
| 2 | `Coder/40_Context_Management/role-switch.md` 内部 | C-1 | 2 次 replace_all（Mode → Role；模式 → 角色） |
| 3 | `Coder/40_Context_Management/context-persistence.md:124` | C-2 | 1 处 edit（文件名 + 概念名） |
| 4 | `Coder/README.md:62` | C-2 | 1 处 edit（目录结构） |

共 4 步，涉及 3 个文件。

# Interface / Contract

- **文件名契约**：`Coder/40_Context_Management/` 下新增 `role-switch.md`，删除 `mode-switch.md`。git mv 保留历史血缘。
- **术语契约**：
  - `logic-protocol.md § 4 模块激活感知` 中 Standard/Ideation/Loop/Review "Mode" 术语**保持不变**（运行时能力概念）。
  - 职责切换侧改为：`Architect Role / Coder Role / Reviewer Role / Verifier Role`（中文"角色"）。
- `context-persistence.md § 7` 与本文件的关系声明从"模式切换时的职责边界"改为"角色切换时的职责边界"。

# State / Boundary

- 不动 `logic-protocol.md`、`lifecycle.md`、`handoff-spec.md`、其他 schema、Extension 文件、`templates/`、`scripts/`。
- 不修改 `deliveries/2026-04-17-must-fix-repair.md` 中的历史引用（作为历史记录保留）。

# Design Decisions

1. **使用 `git mv` 重命名**：保留文件历史血缘，便于 `git log --follow` 追溯。
2. **两次 `replace_all` 一把过**：全文审查确认无 "Model"、"mode"（小写）等子串干扰，也无需保留任何"模式"字样作为不相关概念。
3. **`Reviewer / Verifier Mode` 这种合并形式**：`replace_all` 会把 `Reviewer / Verifier Mode` 改成 `Reviewer / Verifier Role`，语义正确，保留合并表达。
4. **frontmatter 不单独处理**：`title: 模式切换规范` 和 `scope: ... 模式职责 ...` 会被 `模式 → 角色` 的 replace_all 捕获，无需额外 edit。

# Execution Steps

## Step 1 — `git mv` 重命名

```bash
git mv Coder/40_Context_Management/mode-switch.md Coder/40_Context_Management/role-switch.md
```

## Step 2 — 新文件内部术语全替换（2 次 replace_all）

对 `Coder/40_Context_Management/role-switch.md`：
- `Mode` → `Role`（替换所有 7 处：H1 标题 1 次 + § 2 子标题 3 次 + § 3 条目 3 次）
- `模式` → `角色`（替换所有 11 处：frontmatter 2 次 + 正文 9 次）

## Step 3 — `context-persistence.md` 引用更新

**old**:
```
- `mode-switch.md` 负责模式切换时的职责边界。
```

**new**:
```
- `role-switch.md` 负责角色切换时的职责边界。
```

## Step 4 — `Coder/README.md` 目录结构更新

**old**（L62 附近的目录结构块）:
```
    mode-switch.md
```

**new**:
```
    role-switch.md
```

# Verification Plan

- **文件系统**：
  - `ls Coder/40_Context_Management/` 包含 `role-switch.md`，不包含 `mode-switch.md`。
  - `git log --follow Coder/40_Context_Management/role-switch.md | head` 能追溯到原 `mode-switch.md` 历史。
- **术语扫描**：
  - `grep -n 'Mode' Coder/40_Context_Management/role-switch.md` 返回 0。
  - `grep -n '模式' Coder/40_Context_Management/role-switch.md` 返回 0。
  - `grep -n 'Role' Coder/40_Context_Management/role-switch.md` 命中至少 7 处。
  - `grep -n '角色' Coder/40_Context_Management/role-switch.md` 命中至少 11 处。
- **引用一致性**：
  - `grep -rn 'mode-switch' Coder/ --include='*.md'` 零命中（排除 `.claude/` 和 `deliveries/`）。
  - `grep -rn 'role-switch' Coder/ --include='*.md'` 命中至少 2 处（context-persistence + README）。
- **保留区**：
  - `grep -n 'Standard Mode\|Ideation Mode\|Ralph-Loop Mode\|Review Mode' Coder/00_System_Prompt/logic-protocol.md` 维持原有命中数（logic-protocol 侧的 Mode 术语未动）。

# Risks / Open Questions

- **风险 1**：`replace_all "Mode" -> "Role"` 若遗漏子串检查会误改 `Model`/`mode` 等词。已手工通读全文确认只有"Architect/Coder/Reviewer/Verifier Mode"和"# Mode Switch"两种形式，无误伤。
- **风险 2**：`replace_all "模式" -> "角色"` 同样通读确认全文 11 处均属职责切换语义，无其他"模式"一词（如"设计模式"、"观察者模式"）。
- **开放问题**：无。
