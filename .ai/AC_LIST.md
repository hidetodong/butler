# Goal

- 修复 Bucket C（Mode 术语双关消歧）1 条 Should Fix。

# In Scope

- `Coder/40_Context_Management/mode-switch.md` 中 "Mode" 术语的改名（或文件改名）。
- 同步更新 `context-persistence.md` 和 `Coder/README.md` 中的文件名引用（若重命名）。

# Out of Scope

- `logic-protocol.md § 4 模块激活感知` 的 Standard/Ideation/Loop/Review Mode 术语保持不变（该处 Mode 术语与命令绑定深入）。
- lifecycle.md 的 P1-P5 阶段定义不动。

# Acceptance Checklist

- [ ] **C-1** `mode-switch.md` 内部 "Mode" 术语消歧，方案待拍板
- [ ] **C-2** 所有对该文件的引用（文件名、概念名）全部同步到新术语，无遗漏

# Verification Method

- **C-1**：根据选定方案，`grep 'Architect Mode\|Coder Mode\|Reviewer Mode\|Verifier Mode' Coder/40_Context_Management/*` 返回 0 命中（旧术语全部替换）。
- **C-2**：`grep -rn 'mode-switch' Coder/ --include='*.md'` 返回的引用数与新文件名一致；若重命名则 `grep 'mode-switch\.md'` 除历史 `deliveries/` 外零命中活跃文件。

# Open Questions / Risks

## ❓ 待拍板 - 方案选择

两个维度的决策组合：**(A)新术语中文 + (B)是否重命名文件**。

### 方案 Alpha（推荐）— 角色切换 + 重命名为 `role-switch.md`

- 术语：英文 `Role Switch` / 中文 "角色切换"；三个子 Mode 改为 `Architect Role / Coder Role / Reviewer Role`。
- 重命名：`mode-switch.md` → `role-switch.md`。
- 同步更新：`context-persistence.md:124`、`Coder/README.md:62`。
- **优点**：一次彻底消除术语与文件名歧义；"角色"与"帽子切换"直觉一致。
- **代价**：4 处改动（文件重命名 + 内部术语 + 2 处引用）。

### 方案 Beta — 角色切换 + 文件名不动（`mode-switch.md` 保留）

- 术语与 Alpha 相同。
- 文件名保留 `mode-switch.md`，但文件内容明确说"本文件定义 Role Switch（历史原因保留 mode-switch 文件名）"。
- **优点**：改动小，无 broken link 风险。
- **缺点**：文件名继续误导读者（看文件名以为是 Extension Mode 切换）；术语一致性打折。

### 方案 Gamma — 帽子切换（Hat Switch）+ 重命名为 `hat-switch.md`

- 术语：英文 `Hat Switch` / 中文 "帽子切换"；三个子 Mode 改为 `Architect Hat / Coder Hat / Reviewer Hat`。
- **优点**：比喻生动直白；"戴不同帽子做不同事"的概念易懂。
- **缺点**：偏俚语，正式度略低；"帽子"作为技术术语较非主流。

### 方案 Delta — 两侧 Mode 都保留，加修饰词区分

- `logic-protocol` 的 Mode 改称 `Extension Mode`，`mode-switch` 的 Mode 改称 `Role Mode`。
- **优点**：不伤及现有术语词根。
- **缺点**：认知负担仍在（读者要记两种 Mode）；名字更长。

---

## 风险

- 若选 Alpha 或 Gamma（重命名）：`Coder/README.md` 的目录结构展示需要同步；历史 `deliveries/*.md` 中的旧文件名引用保留不改（作为历史记录）。
- `mode-switch.md` 的 frontmatter `title` 和 `scope` 字段也需同步更新术语。

---

# 请回复

1. **方案选择**：Alpha / Beta / Gamma / Delta

拍板后进 P3 出具体 edit 清单。
