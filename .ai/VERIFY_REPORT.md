# VERIFY_REPORT — ITER-0037（MILE-0004 R2 · PRD 切分机制）

> 监督态自驱。全为规则文档（1 份新机制文档 + 注入表触发 + flip R1 指针 + README 注册）。验证 = 读改后正文核契约 + `git status`/`git grep` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余（纯规则、无运行时）。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** 新建 `Coder/40_Context_Management/prd-split.md`，frontmatter 含 `title`/`audience: AI / 开发者`/`scope`。§1 开宗定位为**产生动作层**、显式写"履行 `references-schema` 契约、是其 §8 指的 R2"，并用一张表把"契约（结果长什么样）vs 动作（怎么动手做）"分工 + 五处回指真源（§2/§3/§4/§6/§7）列清。
- [x] **AC2 ✓** §2 边界识别成文——"按 PRD 自身结构切、不自造边界"（章节/功能模块/修改项 = 天然切线），一模块=一片=一 slug；**红线"绝不把一条完整规则/校验/文案拦腰切碎跨两片"**成文，配"宁可粗、不可碎"取舍与理由（粗了多读几行、碎了废掉切片权威性）。
- [x] **AC3 ✓** §3 成文首切给每模块分**语义化终身 slug**（配"终身身份证号"比喻 + 示例）+ 写 `00_INDEX`（入口叙述 + 模块登记表）；字段（slug/标题·章节/首见版本=当前 PRD 版/当前版本/状态 active）与 slug 规则**回指 `references-schema §3/§4`**、不复述。
- [x] **AC4 ✓** §4 逐字保真成文——每片=模块原文无损投影、"照搬不概括"，精确文案/校验/字段一字不改，显式**守 `references-schema §6` 命门**、对比禁用 `.ai/project` 的有损 overwrite；唯一可摘要处限 `00_INDEX` 入口叙述。
- [x] **AC5 ✓** §5 小 PRD 单模块退化态成文——模块数=1 走**同一套模型**（`00_INDEX` + 1 片）、不另开特例、不退回扁平态；给出理由（小 PRD 一样改版/钉版/审计，统一模型才无缝接 R4/R5）+ 判据回指 `references-schema §2`。
- [x] **AC6 ✓** §6 soft 对齐成文——"提议→确认→落盘"三拍写死（提议时不写盘 / 用户可调边界与 slug / 确认后才落），"soft 对齐＝不硬切、决策权交回用户"释义落地；显式点明同 `[split]`/`[add-field]` 信任模型；**硬约束引用块"未经确认不得落盘"**成文。
- [x] **AC7 ✓** `logic-protocol.md §外部参考资料注入` 类型表补一行（大/结构化 PRD → 走 `prd-split.md` 切成 `prd/` 知识文件夹态、提议→确认→落盘、小 PRD 单模块退化），与扁平态（`api-`/`design-`/`insight-`）并列；判据回指 `references-schema §2`、不双写。
- [x] **AC8 ✓** README 双处注册（结构树 `references-schema.md` 后补 `prd-split.md`、契约→动作相邻；规则说明段补一条）；`references-schema §8` R2 行 flip 为"**✅ 已由 `prd-split.md` 落地**"。scope 守恒（`git status` 源改动 = 新建 prd-split + 改 logic-protocol/references-schema/README）：**不做** /milestone 并进+交叉指针(R3)/`prd_version` 钉版(R4)/`/prd update` 同步+`.archive` 快照产生(R5)/认亲(R6)，**不改** references 扁平用法/`project-digest`/`context-persistence`/`mcv-deployment`/hook/`VERSION`，**不切版**；`prd-split` 属 `40_Context_Management`（SOP Core），未混入 domain/business。
- [x] **AC9 ✓（dogfood·说人话）** `slug`（首现"英文短横线、见名知意"+"终身身份证号"比喻+示例）/ `soft 对齐`（"＝不硬切、决策权交回用户"）/ 逐字保真（"照搬不概括"+"少一字对不上真源"）/ 单模块退化态（"模块数=1 同一套模型"）均首现带解释；无裸英文/变量。

## 独立复核

- **执行**：干净上下文子 agent，验证者≠实现者、只读、对抗式；四对抗点（切分红线够不够硬 · 契约 vs 动作有无越界复述 · soft 对齐真是提议非黑箱 · 触发不碰 R3 入口）逐点核。
- **结论**：**APPROVE（干净，可收口）**。四对抗点逐一过——① 切分红线是硬约束"绝不…拦腰切碎"+ 宁粗不碎可执行指引（prd-split §2）；② 契约 vs 动作无双写，`removed`/slug 规则只存于 references-schema、prd-split 只回指（`git grep` 证实）；③ soft 对齐三拍完整 + 独立硬约束"未确认不得落盘"、无自动切暗门；④ 触发只碰 logic-protocol 注入表一行，`/milestone`/钉版/同步/认亲零落地、references-schema §8 R3–R6 行未动只 flip R2。交叉引用 §2/§3/§4/§6/§7 逐一对应、§8↔§1 双向自洽。**Must Fix 无 · Should Fix 无 · Nit 1**（§1 slug 首现 gloss 偏简）。
- **Nit 处置（已修）**：§1 回指表 slug 行补内联注解"（模块的终身英文代号，如 `save-validation`）"，首现即带解释，AC9 全闭。

## Remaining Risks

- R2 是**首切机制的规则文字**，其"绝不切碎""逐字保真""提议→确认"三条护栏靠执行体遵从、非机器强制——真到用户丢来一份大 PRD 端到端切一次才完全证伪（同知识文件夹折叠质量、`[split]` 先问再迁的既有信任模型）。
- 触发只接了注入表这一条通用入口；`/milestone` brief 并进（"里程碑就是大 PRD"）尚未接，属 R3——在 R3 落地前，PRD 先行的"一份输入喂两个海拔"闭环未合拢。
