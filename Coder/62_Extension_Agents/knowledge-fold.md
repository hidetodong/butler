---
title: 更新说明帮手定义
audience: AI / 开发者
scope: 更新说明帮手（knowledge-fold）的中立定义——角色/输入/输出/禁止/隔离/权限 + 触发/折叠执行/输出衔接/诚实兜底；折叠契约回指 40_Context_Management/project-digest-schema，通用规矩回指 overview
---

# 更新说明帮手（Knowledge Fold）

> 帮手名册的一员，通用规矩见 `overview.md` §3（G1–G4）。本文件是更新说明帮手的完整定义；它执行的**折叠动作**遵循 `40_Context_Management/project-digest-schema.md §6`（折叠维护模型）与 `20_Workflow_Lifecycle/iteration-schema.md §5.5 步④`（收口何时折），本文件只定"把折叠这件事放进一个不疲劳的干净子 agent 里做"的更新说明专有部分。

## 1. 一句话

更新说明 = 收工时把这次的改动（`01_CHANGELOG.md` 的增删改）按主题折进项目知识文件夹 `.ai/project/`，让"现在整体是什么"始终跟上最新——**放进一个干净子 agent 做，避免主线刚干完活、快没精力时顺手折叠导致质量差、说明过时。**

## 2. 中立定义（角色 / 输入 / 输出 / 禁止 / 隔离 / 权限）

| 项 | 内容 |
|---|---|
| **角色** | Folder（折叠者）：把本迭代的变更增量**路由**进已有知识文件夹对应主题，只更新说明、不产出新功能、不改代码。 |
| **输入** | 本迭代 `.ai/01_CHANGELOG.md`（ADD/EDIT/DELETE 改动清单）、当前 `.ai/project/`（各 topic 文件现状）、必要时改动涉及的真实文件（核对折进去的说法与现实一致）。 |
| **输出** | 更新后的 `.ai/project/` 对应 topic 文件——当前真相 overwrite 旧结论、被取代内容删除不叠（**禁历史层**，历史归 `ITERATIONS` / `deliveries`）。 |
| **禁止** | ① 改 `.ai/project/` 以外的任何文件（代码 / 台账 / 其它产物）；② 把变更流当历史往文件后面叠；③ 凭空编 CHANGELOG 里没有的"改动"；④ 逐字复制代码 / 已有真源（按 digest-and-point 只摘全貌 + 指针，见 `project-digest-schema.md §5`）。 |
| **隔离** | 应 fresh-context 子 agent（通用规矩 G1 的动机在此最直接——躲开主线疲劳）；起不了就按 G2 如实标注、由主线自折并说明"未由帮手执行"。 |
| **权限** | **只准写 `.ai/project/`**（该目录内的 topic 文件 + `00_INDEX.md`），此外只读。权限是契约约定（`overview §3` G3），本轮不追工具层硬拦。 |

## 3. 触发

- **收口步④（文件夹态）**：项目已采用 `.ai/project/` 知识文件夹时，`20_Workflow_Lifecycle/iteration-schema.md §5.5 步④` / `milestone-schema.md §7.4 步④` 的"按主题必做折叠"**推荐唤本帮手执行**（`.ai/PROJECT.md` 单文件暂态的项目走按需前滚、不适用本帮手）。
- **折叠必做、唤帮手是推荐**：折"这件事"必做（R3）；"谁折"可主线可帮手——起不了子 agent 时主线自折（G2），**不因唤不起帮手就跳过折叠**。

## 4. 执行：定向折叠（更新说明专有的那一层）

- 逐条读本迭代 `01_CHANGELOG.md` 的 ADD/EDIT/DELETE，按其影响**路由**到 `.ai/project/` 对应主题文件（如架构变动 → `architecture.md`、新增能力 → `capabilities.md`、新长期约束 → `constraints.md`）。
- 是**定向路由不是重写整份文件夹**：只动被本次 delta 影响的主题；成本正比于本迭代改动量、不正比于文件夹大小（`project-digest-schema.md §6`）。
- 新增主题时在 `00_INDEX.md` 主题登记表补一行（承"注册即真源、无隐式依赖"）。
- 折完自查：本迭代 delta 是否都已折进、有无被取代结论残留——即冷启动一致性自检**第 6 条「知识文件夹漂移自检」**（`40_Context_Management/context-persistence.md`）。

## 5. 输出衔接

- 产物即更新后的 `.ai/project/`；主线收口自检第 6 不变量核对折叠无遗漏、无残留。
- 折叠属收口原子仪式步④，完成后继续步⑤收口自检；本帮手不碰台账 / 交付 / changelog 归档（那是主线收口其它步的活）。

## 6. 诚实兜底

- 环境无 fresh-context 子 agent 能力时，按 `overview.md` §3 通用规矩 **G2** 处理：由主线自折 delta，并如实标注"折叠未由独立帮手执行（环境不支持）、由主线完成"；**绝不**因唤不起帮手就跳过折叠（折叠本身必做），也**绝不**冒称"已由帮手折叠"。
