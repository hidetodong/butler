# VERIFY_REPORT — ITER-0036（MILE-0004 R1 · references 索引化基座）

> 监督态自驱。全为规则文档新增（1 份新 schema + README 注册），验证 = 读改后正文核契约 + `git grep`/`git status` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余（纯规则、无运行时）。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** 新建 `Coder/40_Context_Management/references-schema.md`，frontmatter 含 `title`/`audience: AI / 开发者`/`scope`。正文两部分：通用（§1 定位 + §2 扁平态 `api-/design-/insight-`，注入真源回指 `logic-protocol`）+ prd/ 知识文件夹态（§3–§7）。
- [x] **AC2 ✓** §3 `prd/00_INDEX` 契约（入口叙述 + 模块登记表，字段 = slug / 标题·章节 / 首见版本 / 当前版本 / 状态 active|removed）；§4 定死 slug **一次分配、终身不变、只增不改**（removed 除外），"身份 vs 门牌"比喻落地。
- [x] **AC3 ✓** §5 digest-and-point 读纪律（地图→按需钻切片→钻源 + 执行读 live 最新）；显式**回指读纪律真源 `context-persistence.md §6`、不重复定义**（并点明 `project-digest §5` 是配套写侧、非读侧），只标 references 两点差异。〔复核 Should Fix 已修：真源原指浅一层的 `project-digest-schema`，已改指读侧真源 `context-persistence.md §6`〕
- [x] **AC4 ✓** §6 无损/有损硬区分成文：`00_INDEX` 可摘要 / 切片必逐字原文；显式对比 `.ai/project`（有损 overwrite）标为命门差异；硬约束"**不得对切片套 overwrite/概括/蒸馏语义**"成文（引用块）。
- [x] **AC5 ✓** §7 落盘契约：live `prd/<slug>.md`（最新、无版本前缀、直读）+ `.archive/vN/` 全量快照（自包含、回溯用）；显式声明"**只定形态、不定何时怎么冻**（冻的动作属 R5）"，且澄清版本维度 ≠ project 两态。
- [x] **AC6 ✓** `Coder/README.md` 双处注册：目录结构树 `/40_Context_Management` 下补 `references-schema.md`；per-file 描述段补一条（定位 + 与 project-digest 分工 + 动作属 R2–R5）。
- [x] **AC7 ✓（scope 守恒）** `git status` 源改动集 = 新建 `references-schema.md` + `Coder/README.md`（注册）；余为 `.ai/` 四件套/台账/里程碑工作区过程件 + 设计记录 `docs/research/prd-first-design.html`。**不写**切分/入口/钉版/同步动作、**不改** references 既有扁平用法 / `acceptance`·`tech-plan`·`verify` 接线 / `project-digest`·`context-persistence` 语义 / `mcv-deployment` / hook / VERSION，**不切版**。
- [x] **AC8 ✓** `references-schema` 属 `40_Context_Management`（SOP Core），未混入 domain/business；§1 分工表与 `project-digest-schema` 职责分明（有损摘要 vs 含无损切片），读纪律回指不双写、无重叠。
- [x] **AC9 ✓（dogfood·说人话）** `slug`（首现"终身身份（英文短横线，如 save-validation）"）/ `digest-and-point`（"地图→按需钻→钻源"）/ `live`·`.archive`（§7 解释）/ 无损（配"少一字验收就错"+ PRD 文案例）均首现带解释；裸英文 `re-derive` 两处已改"重新派生"。

## 独立复核

- **执行**：干净上下文子 agent，验证者≠实现者、只读、对抗式；四个对抗点（无损/有损红线够不够硬 · 读纪律是否双写 · slug 规则能否撑 R5 认亲 · 边界有无越界做动作）逐点核。
- **结论**：**APPROVE-with-nits**。
  - A（无损/有损红线）· C（slug 撑 R5 认亲）· D（边界无越界）**过**。
  - B（读纪律无双写）**未双写、但真源指针指浅一层** → **Should Fix**：§5 原把 digest-and-point 读法真源指向 `project-digest-schema`，而读纪律真源实为 `context-persistence.md §6`（`project-digest §5` 是配套写侧）。
- **Should Fix 处置（已修）**：git grep 核实 `context-persistence.md:124` 定义 digest-and-point 读纪律并注"写侧密度契约见 project-digest §5"、`project-digest-schema.md:9/149` 自认读侧属 context-persistence → 复核属实。已将 §5 真源改指 `context-persistence.md §6`，并并列点出 project-digest §5 为写侧、非读侧。AC3 同步更新。
- **Nit（未改）**：`insight-` 措辞可再收，属可改可不改，本轮不动。

## Remaining Risks

- R1 只是**契约地基**，其正确性最终要等 R2（切分）/ R5（同步）真踩上来才完全证伪——契约设错要到后续迭代才暴露。本轮靠"能否支撑 R2–R6 的动作"做前瞻性对抗核。
- 无损/有损红线（§6）靠规则文字约束、非机器强制；真到 R2 切分时是否严格逐字、不"顺手概括"，取决于执行体遵从（同 project 折叠质量的既有信任模型）。
