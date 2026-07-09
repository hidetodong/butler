# TECH_PLAN — ITER-0037（MILE-0004 R2 · PRD 切分机制）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档（1 份新机制文档 + 注入表触发 + README 注册 + flip R1 指针）。

## 设计决策（DD）

- **DD1 · `prd-split.md` 结构照 `references-schema`/`project-digest` 分节风格**（frontmatter + 编号小节），置于 `40_Context_Management`、README 结构树里**紧跟 `references-schema.md`**（契约→动作相邻，读者顺藤摸瓜）。
- **DD2 · 契约 vs 动作分离靠"只引用不复述"落地**：`prd-split` 对 slug 身份（§4）/ 无损切片（§6）/ 落盘（§7）/ 结构（§3）/ 两态判据（§2）一律**回指 references-schema**，不抄字段、不改写语义——契约留在 R1、动作留在 R2，任何一方改了不必两头同步。
- **DD3 · soft 对齐写成"提议→确认→落盘"三拍**：程序里显式三步、绝不自动切；措辞**复用** `[split]` opt-in / `[add-field]` 草稿确认的既有信任模型（不另发明范式，守 AI 协作约束"优先复用现有模式"）。
- **DD4 · 触发最小化、判据不双写**：只在 `logic-protocol §外部参考资料注入` 类型表**加一行**（大/结构化 PRD → `prd-split`），"何为大/结构化"的判据**回指 `references-schema §2`**、不在注入表重写；`/milestone` 入口一行不碰（R3）。
- **DD5 · flip 指针用既有手法**（同 ITER-0032/0035 的条件式指针翻牌）：`references-schema §8` R2 行由"待落地前向指针"翻成"已由 `prd-split.md` 落地"，§8 收尾"动作落地前"一句相应对齐。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/40_Context_Management/prd-split.md`（新建） | §1 定位/契约履行分工 · §2 边界识别+不切碎红线 · §3 slug 首切+00_INDEX/登记表 · §4 逐字保真 · §5 小 PRD 退化 · §6 soft 对齐三拍 | AC1–6 |
| `Coder/00_System_Prompt/logic-protocol.md` §外部参考资料注入 | 类型表 +1 行（大 PRD → `prd-split` 切分），判据回指 §2 | AC7 |
| `Coder/40_Context_Management/references-schema.md` §8 | flip R2 前向指针（待→已由 prd-split 落地） | AC8 |
| `Coder/README.md` | 结构树（紧跟 references-schema）+ 规则说明段注册 `prd-split` | AC8 |

**不碰**：`/milestone`（milestone-schema）、acceptance/tech-plan/verify 接线、`project-digest-schema` / `context-persistence` 语义、references 既有扁平用法（`api-`/`design-`/`insight-` 注入照旧）、`mcv-deployment`、hook、`VERSION`、切分之外的钉版/同步/认亲动作。

## Execution Steps（可勾选）

- [x] S1 · 写 `prd-split.md` frontmatter + §1 定位/契约履行（履行 references-schema、契约 vs 动作分工）→ AC1
- [x] S2 · §2 边界识别（按 PRD 自身语义/模块边界切 + **绝不切碎一条规则**红线）→ AC2
- [x] S3 · §3 slug 首切分配 + 写 `00_INDEX`/登记表（字段与规则守 references-schema §3/§4）→ AC3
- [x] S4 · §4 逐字保真（每片原文无损投影、只搬不概括、守 §6 命门）→ AC4
- [x] S5 · §5 小 PRD 单模块退化态（模块数=1 同一套模型、不开特例、守 §2 判据）→ AC5
- [x] S6 · §6 soft 对齐（提议→确认→落盘三拍、复用 [split]/[add-field] 信任模型）→ AC6
- [x] S7 · `logic-protocol` 注入表补行（大 PRD → prd-split，判据回指 §2、不双写）→ AC7
- [x] S8 · `README` 双处注册（结构树紧跟 references-schema + 说明段）+ flip `references-schema §8` R2 指针 → AC8
- [x] S9 · scope 守恒核对（`git status`）+ 说人话三条自检 → AC8/AC9
- [x] S10 · P5 独立复核（APPROVE 干净，四对抗点全过、Nit 已修）→ 收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep` 核守恒。核心对抗点＝**"绝不切碎一条规则"红线够不够硬**（防 AI 硬切）+ **逐字保真守 §6**（防顺手概括）+ **soft 对齐真是"提议→确认"非黑箱**（护栏是否落到程序）+ **契约 vs 动作分离**（prd-split 只引用不复述 references-schema）+ **触发不越界**（只碰注入表、不碰 /milestone 入口 R3）。dogfood：四件套 + prd-split 过说人话三条。无人测道残余。
