# TECH_PLAN — ITER-0038（MILE-0004 R3 · 首切入口并进 /milestone + 两海拔交叉指针）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档接线（改 3 份 + flip 1 指针）。

## 设计决策（DD）

- **DD1 · 加分支不改主干（非回归第一）**：`milestone-schema §6.4` 合成协议的现有五步**原样保留**，"大 PRD 并进"作为**新增一步（步 6）+ 分支条件**挂在其后；普通 brief 走到步 6 判定"非大 PRD"直接跳过。这样非 PRD 流的字面路径零改动，是 AC7 非回归红线的结构保证。
- **DD2 · 触发靠引用、判据靠回指**：分支正文只写"触发 `prd-split.md` 切成 `references/prd/`"，切分算法（边界/逐字/soft 对齐）**不抄**；"何为大 PRD"**回指 `references-schema §2`**、不在 milestone 侧重写判据。
- **DD3 · 合并对齐写进步 6**：PRD 触发时，步 5（方向 soft 对齐）与 prd-split §6 的切分提议→确认**合并为一次呈交**——在步 6 显式写"路线图 + 切分方案一并给用户确认，不分两轮"。
- **DD4 · 交叉指针双向、映射单一真源**：方向→细节放 `§5.3` 路线图（路线项**可选**列"相关 slug"）；细节→方向放 `prd-split §3`（`00_INDEX` 入口叙述记 owning 里程碑号 + 回指 §5.3 映射、**不重列**）。映射真源单一在路线图，`00_INDEX` 只反向指路——防两头漂移（同 R1/R2 回指不复述纪律）。
- **DD5 · flip 用既有翻牌手法**：`references-schema §8` R3 行由待落地 → **✅ 已由 `milestone-schema §6.4/§5.3` 落地**，与 R1(ITER-0036)/R2(ITER-0037) 翻 §8 指针一致。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| `Coder/20_Workflow_Lifecycle/milestone-schema.md` | §6.4 合成协议加步 6"大 PRD 并进分支"（触发 prd-split + 合并对齐）· §6.4 brief 定位补"PRD 喂两海拔"段 · §5.3 路线图路线项可选标注"相关 slug" | AC1–4 |
| `Coder/40_Context_Management/prd-split.md` §3 | `/milestone` 触发首切时 `00_INDEX` 入口叙述记 owning 里程碑号 + 回指 §5.3 映射（不重列） | AC5 |
| `Coder/40_Context_Management/references-schema.md` §8 | flip R3 前向指针（待→已由 milestone-schema 落地） | AC6 |

**不碰**：§6.4 现有五步的字面内容、`prd-split` 切分算法（§2/§4/§6）、`references-schema` 登记表字段（§3 不加列）、R2 注入表手动入口（`logic-protocol` 大 PRD 行）、acceptance/tech-plan/verify 接线、`project-digest` / `context-persistence`、hook、`VERSION`、`prd_version` 钉版/同步/认亲动作。

## Execution Steps（可勾选）

- [x] S1 · `milestone-schema §6.4` 合成协议加**步 6 大 PRD 并进分支**（判据回指 references-schema §2、触发 prd-split 不复述算法、普通 brief 跳过）→ AC1
- [x] S2 · `§6.4` 合并对齐写进步 6（路线图 + 切分方案一次呈交确认）→ AC3
- [x] S3 · `§6.4 brief 定位`补"PRD 喂两海拔"段（origin PRD 喂 brief + 派生 references/prd、生命周期独立、origin 只读）→ AC2
- [x] S4 · `§5.3` 拆分路线图路线项加**可选"相关模块 slug"标注**（方向→细节指针，非 PRD 里程碑不需要）→ AC4
- [x] S5 · `prd-split §3` 补"/milestone 触发首切时 00_INDEX 记所属里程碑号 + 回指 §5.3 映射、不重列"（细节→方向指针）→ AC5
- [x] S6 · flip `references-schema §8` R3 指针为 ✅ 已落 → AC6
- [x] S7 · scope 守恒核对（`git status`）+ **非回归核对**（`git diff` 零删除，非 PRD brief 五步字面未动）+ 说人话三条自检（去裸英文 owning）→ AC7/AC8
- [x] S8 · P5 独立复核（APPROVE-with-nits，四对抗点全过、Should Fix README 漂移已修）→ 收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep`/`git diff` 核守恒。核心对抗点＝**非回归**（非 PRD brief 合成路径字面逐字不变、分支纯增量）+ **引用不复述**（milestone 分支不抄 prd-split 算法、判据回指 §2）+ **交叉映射单一真源**（模块↔路线项只存路线图、00_INDEX 只回指不重列）+ **不越界**（只接 milestone 入口，不做钉版/同步/认亲）。dogfood：四件套 + 改动正文过说人话三条。无人测道残余。
