---
title: 迭代变更日志格式契约
audience: AI / 开发者
scope: .ai/01_CHANGELOG.md 的定位、ADD/EDIT/DELETE 格式、粒度与噪声地板、四产物分工、产出与归档时机
---

# Changelog Schema

> 结构机器真源：`tools/artifact-pipeline/artifacts.v1.json` + `templates/01_CHANGELOG.md`。本文件解释 delta 语义；新 live 产物固定 ADD/EDIT/DELETE 三段，无变更写 N/A，legacy 归档不追溯改写。

## 1. 定位

`.ai/01_CHANGELOG.md` 是**每迭代的对象级变更流**：本迭代到底新增 / 修改 / 删除了哪些文件与章节，每条绑回它兑现的 AC。它是**变更取向**（写"这一轮改了什么 delta"），与 `PROJECT.md`（状态取向，写"系统现在是什么"）相对。

- 作用域 = 当前活跃迭代（热数据）。开新迭代时随四件套 overwrite-reset（见 `iteration-schema.md §5.1`）。
- 收口时其切片归档为 `iterations/ITER-NNNN/CHANGELOG.md`，全局文件随之收敛（见 `iteration-schema.md §5.5`）。

### 四产物边界（各管一轴，不重复记账）

| 产物 | 轴 | 写什么 | 粒度 |
|---|---|---|---|
| `01_CHANGELOG.md` | 变更（delta） | 本迭代 ADD/EDIT/DELETE 了哪些对象 | 文件 + 章节级、绑 AC |
| `deliveries/ITER-*.md` | 交付（人读） | 这次交付目标 / 价值 / 影响的散文总结 | 高层、面向人 |
| `ITERATIONS.md` | 索引 | 迭代号 / 标题 / 状态 / 交付链接 | 一行一迭代 |
| `PROJECT.md` | 状态（积分） | 系统现在整体是什么、长期约束与欠债 | 全貌、常驻 |

与 git 的分工：git diff 是**机械全量**真源（每一行）；changelog 是**精选语义**——只记有意义的对象级变更并绑 AC，不与 git 比全。

## 2. 格式（锁定）

顶部一行元信息，其后严格三段，顺序固定：

```md
> <迭代标题> · <active|closed> · <收口日期或 —>

## ADD
- `对象 §章节` — 一句话语义 → ACn

## EDIT
- `对象 §章节` — 一句话语义 → ACn

## DELETE
- 无
```

- **严格三类**：只有 `ADD` / `EDIT` / `DELETE` 三段，不增设其它分类。
- **不省段**：三段都必须在场；某类无内容写一条 `- 无`，不得删段。
- **每条结构**：`` `对象 §章节` `` + ` — ` + 一句话语义 + ` → ACn`（该变更兑现的 AC；纯支撑性、无对应 AC 的可省 `→ ACn`）。
- 对象用反引号包路径 / 文件名；涉及具体章节时带 `§N`。

## 3. 粒度与噪声地板

- **粒度**：文件 + 章节级，**不逐行**。同一文件多处相关改动归一条（带主章节）；跨章节的独立改动可分条。
- **rename**：记为一条 `DELETE`（旧名）+ 一条 `ADD`（新名），不另设 rename 类。
- **噪声地板**：跳过纯排版 / typo / lint / 格式化等无语义改动（沿用 `maintenance-boundaries.md §15` 低价值边界）。changelog 记"值得追溯的变更"，不是 git 的复刻。

## 4. 与交付总结的分工

`01_CHANGELOG.md` 与 `deliveries/ITER-*.md` **并存不替代**：

- delivery 写**高层人话**（目标 / 价值 / 用户可感知变化），面向人；
- changelog 写**细粒度对象级** ADD/EDIT/DELETE，面向追溯；
- delivery 的「已完成内容 / 高层影响范围」可**引用** changelog，不逐条复述（避免双重记账）。

## 5. 产出与归档时机

- **何时写**：P4 实现期间在内存累积变更感知，不实时落盘（合 `maintenance-boundaries.md §2` 批处理）；收口时一次性 finalize。
- **必产口径**：完整路径迭代收口**必产** `01_CHANGELOG.md` 并归档 `iterations/ITER-NNNN/CHANGELOG.md`；简化路径（无完整四件套）可省。
- **收敛**：收口后全局 `01_CHANGELOG.md` 收敛为只含开放迭代热数据（已归档切片不再留在全局文件）。
- **不进硬门禁**：changelog 是收口产物、非阶段门禁产物，不进 hook `phase_gate`、不进 `rule-card.md` 强制产物集；存在性靠收口纪律兜底。

## 6. 写作口径

字段正文讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）。一句话语义要让人不读 diff 也懂这条改了什么、为什么。

## 7. 与其他规则的关系

- 作用域 / reset / 归档机制：`iteration-schema.md §5.1 / §5.5`。
- 更新触发与低价值边界：`maintenance-boundaries.md §15`。
- 部署期文件登记：`mcv-deployment.md`。
- Review / 自评产出的 Should Fix（不阻断项）**不写本文件**，记入 `VERIFY_REPORT.md` 的 `Remaining Risks`（见 `verify-schema.md §4`、`60_Extension_CodeReview/review-engine.md §71`）。
