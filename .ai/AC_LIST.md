---
状态: ack-frozen
ACK 日期: 2026-07-09
迭代: ITER-0038
里程碑: MILE-0004（R3）
---

# AC_LIST — ITER-0038（MILE-0004 R3 · 首切入口并进 /milestone + 两海拔交叉指针）

> 监督态自驱。全为规则文档接线（改 milestone-schema + prd-split + flip references-schema §8 指针），验证 = 读改后正文核契约 + `git grep` 核守恒 + 非回归核对，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · 大 PRD 并进分支

- **AC1**：`milestone-schema.md §6.4` 合成协议加一条**"大 PRD 并进"分支**——当 brief / `origin/` 材料是大 PRD（逐字权威规格，判据**回指 `references-schema §2`**、不重写）时，在合成 MILESTONE 三段之外**额外触发 `prd-split.md`** 切成 `references/prd/`。分支只**调用**机制、**不复述**切分算法。现有 brief→MILESTONE 五步**一字不动**。
- **AC2**：`§6.4 brief 定位`补一段——`origin/` 里的 PRD **既喂 brief**（方向层、有损合成路线图）**又经 `prd-split` 派生 `references/prd/` 切片**（细节层、无损）；`origin/` 文件仍用户自管、AI 只读不归档，`references/prd/` 是 AI 派生的权威投影，两者**生命周期独立**（区分回指 `mcv-deployment §2` / `references-schema §1`）。

## 块2 · 合并对齐 + 两海拔交叉指针

- **AC3**：**两次 soft 对齐合并成一次**成文——PRD 触发时，milestone 方向对齐（路线图）与 prd-split 的切分提议→确认（模块清单 + slug + 边界）**并作一次呈交**给用户确认，不让用户点两轮。
- **AC4（方向 → 细节）**：`milestone-schema §5.3` 拆分路线图，路线项**可选标注"相关模块 slug"**（里程碑由 PRD 派生时，路线项 → 它实现的 `prd/<slug>`）——里程碑方向下钻 references 细节的指针；标注为**可选**（非 PRD 里程碑不需要）。
- **AC5（细节 → 方向）**：`prd-split §3` 成文——由 `/milestone` 触发首切时，写 `00_INDEX` 入口叙述**记 owning 里程碑号**（"本 PRD 服务 `MILE-NNNN`，模块↔路线项映射见其 §5.3"）；**只回指、不重列映射**（映射真源单一在路线图，防两头漂移）。

## 块3 · flip · 守恒 · 说人话

- **AC6**：flip `references-schema §8` 前向指针表 R3 行（"从 `/milestone` **触发**首切 + 路线图项 ↔ 模块 slug 交叉指针"）为 **✅ 已落地**（指向 milestone-schema §6.4 / §5.3）。
- **AC7（scope 守恒 + 非回归 + 分层）**：改动集限于 `milestone-schema.md`（§6.4 分支 + brief 定位 + §5.3 slug 标注）+ `prd-split.md §3`（owning 里程碑记法）+ `references-schema.md §8`（flip R3 指针）。**不做** `prd_version` 钉版(R4) / `/prd update` 同步(R5) / 认亲(R6)；**不改** R2 注入表手动入口（`logic-protocol` 大 PRD 行）/ `prd-split` 切分算法（§2/§4/§6）/ `references-schema` 登记表字段（§3 不加列）/ `project-digest` / `context-persistence` / hook / `VERSION`；**不切版**。**非回归红线**：非 PRD 里程碑 brief 合成路径**逐字不变**（分支为纯增量 opt-in）。分层不破坏（改动仍在 SOP Core `20`/`40`）。
- **AC8（dogfood·说人话）**：本迭代四件套 + 改动正文按说人话三条自检（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；"一份输入喂两个海拔" / owning 里程碑 / 交叉指针等首现带一句解释或比喻。
