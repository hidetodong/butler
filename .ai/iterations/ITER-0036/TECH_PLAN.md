# TECH_PLAN — ITER-0036（MILE-0004 R1 · references 索引化基座）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档新增（1 份新 schema + README 注册）。

## 设计决策（DD）

- **DD1 · schema 结构照 `project-digest-schema` 的分节风格**（frontmatter + 编号小节），保持 `40_Context_Management` 内一致、易读；内容是 references/prd 契约。
- **DD2 · 与 project-digest 的分工写死在 §1，读纪律不双写**：references-schema 只补 references **特有**的东西（无损切片、slug 身份、版本落盘）；digest-and-point 的**读纪律真源在 `context-persistence.md §6`**（`project-digest §5` 是配套写侧），references §读纪律**回指**读侧真源 + 只标"切片按需读、执行读 live 最新"这层差异。〔复核 Should Fix：原文误指 project-digest 为读法真源，已改指 context-persistence §6〕
- **DD3 · slug 身份 + 登记表字段一次定死**（终身、只增不改），是 R5 认亲的锚点；R1 **定规则、不实现认亲动作**。
- **DD4 · 落盘契约 live/`.archive` 是"版本"维度**，与 project 的"文件夹态/单文件态"两态**不是一回事**，schema 里避免措辞混淆（一个是版本快照、一个是产物形态）。
- **DD5 · 边界靠条件式前向指针表达**：R1 定契约处，对"产生/变更动作"显式写"见 R2–R5（MILE-0004 路线图）"，不预先落实现——同 ITER-0032 对 R8 的条件式指针手法。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/40_Context_Management/references-schema.md`（新建） | §1 定位/分工 · §2 两态 · §3 prd 结构+00_INDEX+登记表 · §4 slug 身份 · §5 读纪律 · §6 无损/有损硬区分 · §7 落盘契约 · §8 边界+前向指针 | AC1–5,7,8 |
| `Coder/README.md` | 目录结构 + 读取顺序注册 references-schema | AC6 |

**不碰**：references 既有扁平用法（`logic-protocol` 注入 / `External References` 字段）、`project-digest-schema` / `context-persistence` 语义、`mcv-deployment` 目录定义、hook、VERSION、切分/入口/钉版/同步动作。

## Execution Steps（可勾选）

- [x] S1 · 写 `references-schema.md` frontmatter + §1 定位/职责（与 project-digest 分工）→ AC1/AC8
- [x] S2 · §2 两态（扁平态回指 logic-protocol / 知识文件夹态）+ §3 prd/ 结构 + `00_INDEX` 入口 + 模块登记表字段 → AC1/AC2
- [x] S3 · §4 slug 身份规则（终身 / 只增不改 / 门牌 vs 身份比喻）→ AC2
- [x] S4 · §5 读纪律 digest-and-point（回指 context-persistence §6 为读侧真源、只补 references 差异）→ AC3
- [x] S5 · §6 无损/有损硬区分（对比 `.ai/project` + 硬约束"不得对切片套 overwrite/概括"）→ AC4
- [x] S6 · §7 落盘契约（live 直读最新 + `.archive/vN/` 全量快照；只定形态、前向指针 R5）→ AC5
- [x] S7 · §8 边界 + 条件式前向指针（切分 R2 / 入口 R3 / 钉版 R4 / 同步 R5）→ AC7
- [x] S8 · `Coder/README.md` 注册（目录结构 + 读取顺序）→ AC6
- [x] S9 · scope 守恒核对（`git status`）+ 说人话三条自检 → AC7/AC9
- [x] S10 · P5 独立复核（干净上下文子 agent，对抗式：无损/有损红线是否够硬 / 读纪律无双写 / slug 规则可支撑 R5 认亲 / 边界无越界做动作）→ APPROVE-with-nits，Should Fix 已修，收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep` 核守恒。核心对抗点＝**无损/有损硬区分够不够硬**（防未来拿 project 的 overwrite 套切片）+ **读纪律不双写**（真源回指 project-digest）+ **slug 身份规则能撑起 R5 认亲**（终身不变、只增不改）+ **边界不越界**（R1 不含任何产生动作）。dogfood：四件套 + schema 过说人话三条。无人测道残余。
