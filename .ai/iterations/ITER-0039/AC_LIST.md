---
状态: ack-frozen
ACK 日期: 2026-07-09
迭代: ITER-0039
里程碑: MILE-0004（R4）
---

# AC_LIST — ITER-0039（MILE-0004 R4 · AC 钉版 + P2/P3/P5 接线）

> 监督态自驱。全为规则文档接线（扩展 acceptance/tech-plan/verify 三 schema + flip references-schema §7/§8 指针，无新文件），验证 = 读改后正文核契约 + `git grep`/`git diff` 核守恒 + 非回归核对，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · AC 钉版字段（frontmatter）

- **AC1**：`acceptance-schema.md` 给 AC_LIST 顶部 frontmatter 增**可选字段** `prd_version`——语义为"引用 `references/prd/` 切片时，记 **ACK 冻结那一刻 PRD 的全局版本号**（如 `v1.1`），冻结绑定、之后钉住"。**全局**（一份 PRD 一个版本号，非逐片编版）+ **可选**（非 PRD / 对话驱动 / 普通 references 迭代不带此字段、frontmatter 逐字不变）两点均显式成文。§2 交付约定 + §3 标准模板 frontmatter 同步体现（模板加 `prd_version: —` 行 + 注释）。
- **AC2（版本单一真源 + 解析锚点）**：`acceptance-schema` 显式写死——版本化引用锚点 = **slug + frontmatter 的全局 `prd_version`**，**版本号只存 frontmatter 一处**，正文引用 `prd/<slug>.md` 不逐条重复版本号（解析时用 frontmatter 补齐）。解析规则成文：PRD 仍在该版 → live 切片即钉住版；PRD 已改版超过 → 读 `.archive/v<prd_version>/<slug>.md`（回指 `references-schema §7` 全量快照、不复述落盘契约）。

## 块2 · P2/P3/P5 三 schema 接线

- **AC3（P2 冻结语义）**：`acceptance-schema §4` 冻结状态字段补一条 `prd_version` 绑定语义——冻结时绑当前全局版、之后钉住；**amend 重冻可重绑**（`iteration-schema §5.3` 退回 draft 重新 ACK 时，PRD 若已改版可随重冻重绑到新当前版；只加"重绑"一句、不改 amend 流程，改版同步完整协议属 R5）。§5 编写规则补"引用 prd 切片时版本取 frontmatter、不逐条重复 + 标哪些 AC 源自哪个 slug"。
- **AC4（P3 继承钉住版）**：`tech-plan-schema` 的 `External References`（§2/§3/§4）接线——引用 prd 切片时**继承 AC 钉住的 `prd_version`**（技术方案跟 AC 走、不自立版本），版本口径**回指 `acceptance-schema`**、不重写。
- **AC5（P5 对钉住版核 · 核心兑付点）**：`verify-schema` 的 `References Compliance`（§3 模板 + §4 编写规则）接线——逐项对照 prd 切片时**对着 AC frontmatter 钉住的 `prd_version` 核**，非对 live 最新核。成文口径：同一迭代内 live 即钉住版（读 live 即可）；仅**回溯复核历史迭代**（PRD 此后已改版）才按 `prd_version` 读 `.archive/vN/` 核。读侧规则回指 `references-schema §5 步骤 2`、不复述。

## 块3 · flip · 守恒 · 说人话

- **AC6（flip 收口指针）**：`references-schema §7` 落盘契约里"`prd_version` 如何在 AC 里记 / 绑定——属 R4"那条 flip 为**已落地**（指 `acceptance-schema`）；`references-schema §8` 前向指针表 R4 行 flip 为 **✅ 已落地**（指 acceptance/tech-plan/verify 三 schema）。
- **AC7（scope 守恒 + 非回归 + 分层）**：改动集限于 `acceptance-schema.md`（§2/§3/§4/§5）+ `tech-plan-schema.md`（§2/§3/§4）+ `verify-schema.md`（§3/§4）+ `references-schema.md`（§7/§8 flip）。**不做** `/prd update` 同步 / 变更检测 / `.archive` 快照产生(R5) / 认亲(R6)；**不改** R3 入口（`milestone-schema §6.4/§5.3`）/ `prd-split` 切分算法 / `references-schema` 契约结构（§3 登记表不加列）/ `logic-protocol` / `project-digest` / `context-persistence` / hook / `VERSION`；**不切版**。**非回归红线**：非 PRD 迭代 AC_LIST frontmatter **逐字不变**（`prd_version` 为纯增量 opt-in 字段），hook 不校验它。分层不破坏（改动仍在 SOP Core `20`/`40`）。
- **AC8（dogfood·说人话）**：本迭代四件套 + 改动正文按说人话三条自检（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；`prd_version` / 钉版 / 钉住 / 锚点 / 全局版本等首现带一句解释或比喻，英文字段名（`prd_version`）在中文语境里有释义包裹。
