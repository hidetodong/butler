# TECH_PLAN — ITER-0033（MILE-0003 R7）

> 监督态自驱（非 `/dangerous`）：用户点选 R7 + "继续"ACK，模型自驱产出，P5 起独立复核守质量（ITER-0033，2026-07-07）。目标见 CONCEPT，不重述。

## 设计决策（DD）

- **DD1 · 三条定义单一真源放 `artifact-style §2`**（主决策，AC1/AC5）：`artifact-style` 本就是书写纪律真源（`§2` 讲人话 + `§4.3` 承重引用已含三条里的两条），三条是它的自然扩充——放这里是**最小改动 + 不搬家**，承 R1 的 G1–G4 单源模式。`presentation-protocol` 只**引用**（声明对话层同守 + 给指针），**不复制**定义，避免"对话一套、文档一套"漂移。
- **DD2 · `§2` 原地改写、不新增段**（AC1/AC2）：把三条落进现有 `§2`（讲人话 / 反黑话）就地重构，保 `§3–§8` 编号稳定、内部 `§` 引用不碎。三条承接 `§2` 现有内容（判据 / 反面词 / 结构锚点归**标准一 & 三**）+ `§4.3`；全仓真正**新增**的只有**标准二·比喻要落地**。`§8` 现有"命中第 2 节反面词"引用仍解析（反面词留在 `§2` 标准一名下）。
- **DD3 · `presentation-protocol` 插新 `§7` + 顺移编号**（AC5）：说人话是"规则"类、归 `§3–§6` 规则簇，插为新 `§7`「对话也说人话」，把原 `§7` 弹性条款→`§8`、原 `§8` 边界→`§9`。**必须同步校正**内部 `§` 引用：`§7`(原)"默认按 §3–§6"→"§3–§7"、`§8`(原)样例注"遵守 §3–§6"→"§3–§7"、`§2` 豁免"(见 §8)"→"(见 §9)"。新节只引用 `artifact-style §2`、不重述三条（守 DD1 单一来源）。
- **DD4 · scope 扩措辞、不碰字段结构**（AC3/AC8）：`artifact-style` frontmatter + `§1` 把适用面从"四件套字段正文"扩到"所有面向人落地文档"（明列四件套 + 交付总结正文 + 知识文件夹 + handoff）；但 `§7` 边界"不改字段结构——四件套字段以四个 schema 为准"**保留**——扩的是"这套书写纪律管哪些文档"，不是"给四件套加字段"。
- **DD5 · dogfood 自检（自己先照三条写）**（AC9）：本迭代四件套 + 交付总结自身收口前逐条过三条硬标准（写"说人话"的迭代不许自己说黑话），VERIFY 记录扫查结论。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `20_Workflow_Lifecycle/artifact-style.md` frontmatter + `§1` | scope 从"四件套字段正文"扩到"所有面向人落地文档" + `§1` 定位重写（三条为跨层通则真源） | AC3 |
| `artifact-style.md §2` | 改写为「说人话三条硬标准」——承 `§2/§4.3` 去重 + 新增标准二·比喻要落地 | AC1/2 |
| `artifact-style.md §8` | "收口前自检"扩为"发长文 / 收口前自检"（含逐条扫三条） | AC4 |
| `00_System_Prompt/presentation-protocol.md` frontmatter + 新 `§7` + 顺移 `§8/§9` | 对话层引用节（只引 `artifact-style §2` 不重述）+ 内部 `§` 引用校正 | AC5 |
| `templates/rule-card.md`（`artifact-style` 紧凑条） | 同步收录三条（与 `§2` 一致、压缩不新增语义） | AC6 |
| `Coder/README.md`（`§目录说明` 两处） | `presentation-protocol` 增说人话应用、`artifact-style` 改"面向人落地文档 + 三条真源" | AC7 |
| `.ai/PROJECT.md`（收口前滚） | 说人话 / 输出可读性条 R7 待→已（R8 仍待） | 收口·AC8 |

**不碰**：`identity.md`（已指 `presentation-protocol`、本轮不扩正文）、`delivery-summary.md`（`§8` 散文口径与字段）、四件套字段结构（四 schema）、hook、`VERSION`/`CHANGELOG`（切版 R8）、`project-digest-schema` 结构契约（R2）/ 读序（R5）/ 维护回路（R3）、rename。

## Execution Steps（可勾选）

- [x] S1 · `artifact-style §2` 改写为说人话三条硬标准（承 `§2/§4.3`、新增比喻落地；保 `§3–§8` 编号）→ AC1/AC2
- [x] S2 · `artifact-style` frontmatter + `§1` scope 扩到所有面向人落地文档 → AC3
- [x] S3 · `artifact-style §8` 扩为"发长文 / 收口前自检"（含三条扫查）→ AC4
- [x] S4 · `presentation-protocol` 插新 `§7` 对话层引用节 + 顺移 `§8/§9` + 校正内部 `§` 引用（§3–§6→§3–§7、(见 §8)→(见 §9)）→ AC5
- [x] S5 · `templates/rule-card.md` `artifact-style` 条同步收录三条 → AC6
- [x] S6 · `Coder/README.md` 两处 scope 描述同步 → AC7
- [x] S7 · dogfood 扫本迭代四件套过三条（AC9，命中 `BLUF`/`fresh-context 子 agent`/`dogfood` 已改）+ scope 守恒核对（`git status`：仅 4 规则文件 + `.ai/`；无 `identity`/`delivery-summary`/hook/`VERSION`/rename）→ AC8
- [x] S8 · P5 独立复核（干净上下文的子 agent[不带本轮记忆去复核]，对抗式：三条无双写·单一来源 / 比喻落地确为新增 / scope 扩不破字段结构 / `presentation` `§` 引用无悬空 / rule-card 与 `§2` 不漂移）→ REQUEST-CHANGES→修 MF1/MF2→AC1–9 过
- [ ] S9 · 原子收口 5 步（归档 + 交付 md+html + 翻台账 + `.ai/PROJECT.md` 前滚 R7→已 + 6 不变量自检[单文件态第 6 条 N/A]）

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git diff`/`grep` 核守恒。核心对抗点＝**单一来源不双写**（三条只在 `artifact-style §2`、`presentation` 只引用）+ **scope 扩不误改字段结构**（DD4）+ **`presentation` 顺移编号后内部引用不碎**（DD3）。dogfood：四件套自身过三条。无人测道残余。
