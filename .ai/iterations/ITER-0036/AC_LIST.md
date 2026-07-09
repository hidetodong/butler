---
状态: ack-frozen
ACK 日期: 2026-07-08
迭代: ITER-0036
里程碑: MILE-0004（R1）
---

# AC_LIST — ITER-0036（MILE-0004 R1 · references 索引化基座）

> 监督态自驱。全为规则文档新增（1 份新 schema + README 注册），验证 = 读改后正文核契约 + `git grep` 核守恒，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · references-schema 骨架

- **AC1**：新建 `Coder/40_Context_Management/references-schema.md`，frontmatter 标 `audience` / `scope`（守 CLAUDE.md 约束 5）。正文含两部分——**通用**（references/ 子系统定位 + 既有扁平单文件 `api-`/`design-`/`insight-` 归入"扁平态"、注入真源仍回指 `logic-protocol`）+ **prd/ 知识文件夹态**（AC2–AC5）。

## 块2 · prd/ 契约核心

- **AC2**：`references/prd/00_INDEX` 契约成文——入口（这份 PRD 是什么 + 模块地图）+ **模块登记表**，每行含 `slug` / 当前标题·章节 / 首见版本 / 当前版本 / 状态（`active`|`removed`）。显式定死 **slug 一次分配、跨改版不变、只增不改**（模块真 `removed` 除外），并说明"slug 是终身身份、章节号是会变的门牌"。
- **AC3**：digest-and-point 读纪律成文——读序（先读 `00_INDEX` 地图 → 按需钻 `prd/<slug>.md` → 指针钻源）+ 执行默认读 **live 最新**。读法与 `project-digest-schema` 同构，**回指其为来源、不重复定义**（守单一来源）。
- **AC4**：**"索引可摘要 / 切片必逐字原文"硬区分**成文——`00_INDEX`（含登记表）可为摘要/路由；`prd/<slug>.md` 切片**必须逐字原文、无损**。显式对比 `.ai/project`（全有损 overwrite）标出这是命门差异，并写成硬约束：**不得对 prd 切片套用 overwrite / 概括 / 蒸馏语义**。

## 块3 · 落盘契约

- **AC5**：落盘契约成文——live 目录 `references/prd/<slug>.md`（最新版、无版本前缀、执行直读）+ `.archive/vN/` **全量快照**（自包含、回溯用）；`prd_version` 仅回溯时去 `.archive` 找。**显式声明 R1 只定形态、不定"何时怎么冻"**（冻的产生动作归 R5）。

## 块4 · 边界 · 注册 · 守恒

- **AC6**：README 注册——`references-schema.md` 登进 `Coder/README.md` 目录结构 + 读取顺序，位置在 `40_Context_Management` 下、与 `project-digest-schema` / `context-persistence` 并列合理。
- **AC7**：scope 守恒——改动集限于 **新建 `references-schema.md`** + `Coder/README.md` 注册 +（若需）最小交叉引用；**不写**切分算法 / 入口触发 / 钉版 / 同步动作，**不改** references 既有扁平用法（`api-`/`design-`/`insight-` 注入）、**不动**非 PRD 流、**不改** `project-digest-schema` / `context-persistence` 语义、**不切版**。
- **AC8**：不破坏分层——`references-schema` 属 `40_Context_Management`（SOP Core），不混入 domain/business；与 `project-digest-schema` 职责分明（一个管项目全貌**有损摘要**、一个管外部参考**含无损切片**），不重叠、不双写。
- **AC9（dogfood·说人话）**：本迭代四件套 + `references-schema` 正文按说人话三条自检（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；`slug` / `digest-and-point` / `live` / `.archive` 等首现带一句解释或比喻。
