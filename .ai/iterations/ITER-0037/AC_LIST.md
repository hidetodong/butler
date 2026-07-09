---
状态: ack-frozen
ACK 日期: 2026-07-09
迭代: ITER-0037
里程碑: MILE-0004（R2）
---

# AC_LIST — ITER-0037（MILE-0004 R2 · PRD 切分机制）

> 监督态自驱。全为规则文档新增（1 份新机制文档 + 注入表触发 + README 注册 + flip R1 指针），验证 = 读改后正文核契约 + `git grep` 核守恒，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · prd-split 机制骨架

- **AC1**：新建 `Coder/40_Context_Management/prd-split.md`，frontmatter 标 `audience` / `scope`（守 CLAUDE.md 约束 5）。开宗写明本文件是**产生动作层**、**履行** `references-schema.md` 契约（是其 §8 指的 R2），并说清"契约（references-schema 声明式）vs 动作（prd-split 程序式）"的分工——引用契约、不复述、不改写。

## 块2 · 切分核心

- **AC2（边界识别）**：成文"怎么切"——按 PRD **自身**的语义/模块边界（章节 / 功能模块 / "修改项"分组）切，一个模块 = 一片 = 一个 slug。显式立**红线：绝不把一条完整规则 / 校验 / 文案拦腰切碎跨两片**（宁可粗、不可碎）。
- **AC3（slug + 00_INDEX）**：成文首切给每模块分**语义化终身 slug** + 写 `00_INDEX`（入口叙述 + 模块登记表）；登记表字段（slug / 标题·章节 / 首见版本 / 当前版本 / 状态）与 slug 规则**守 `references-schema §3/§4`**（首见版本=当前 PRD 版本、状态 `active`、slug 一次分配终身不变）。
- **AC4（逐字保真）**：成文每片 `prd/<slug>.md` 是模块原文的**无损投影**——只搬运不概括，`00_INDEX` 可摘要 / 切片不可；显式**守 `references-schema §6` 命门硬约束**（不得对切片套 overwrite/概括/蒸馏）。
- **AC5（小 PRD 退化）**：成文模块数=1 走**同一套模型**（`00_INDEX` + 1 片），不为小 PRD 另开特例、不退回扁平态（守 `references-schema §2` 判据）。
- **AC6（soft 对齐）**：成文切分**非全自动黑箱**——AI 先**提议**切分方案（模块清单 + 每模块 slug + 边界依据）给用户，确认/调整后才落盘；绝不擅自猜边界硬切、绝不静默切碎。显式点明与 `[split]` opt-in / `[add-field]` 草稿确认**同一信任模型**。

## 块3 · 触发 · 注册 · 守恒

- **AC7（触发接线）**：`logic-protocol.md §外部参考资料注入` 类型表补一行——"大/结构化 PRD（逐字权威规格）→ 走 `prd-split.md` 切成 `prd/` 知识文件夹态"，与扁平态（`api-`/`design-`/`insight-`）并列；判据回指 `references-schema §2`，不双写判据。
- **AC8（注册 + flip 指针 + 守恒 + 分层）**：README 双处注册 `prd-split.md`（目录结构 + 读取顺序）；flip `references-schema §8` R2 前向指针（"切成 prd/<slug>.md" → 已由 `prd-split.md` 落地）。scope 守恒——**不做** /milestone brief 并进 + 交叉指针（R3）/ `prd_version` 钉版（R4）/ `/prd update` 同步 + `.archive` 快照产生（R5）/ 认亲（R6），**不改** references 既有扁平用法 / `project-digest` / `context-persistence` 语义 / hook / `VERSION`，**不切版**；`prd-split` 属 `40_Context_Management`（SOP Core），不混入 domain/business。
- **AC9（dogfood·说人话）**：本迭代四件套 + `prd-split` 正文按说人话三条自检（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；`slug` / 逐字保真 / soft 对齐 / 单模块退化态等首现带一句解释或比喻。
