---
状态: ack-frozen
ACK 日期: 2026-07-09
迭代: ITER-0040
里程碑: MILE-0004（R5）
---

# AC_LIST — ITER-0040（MILE-0004 R5 · 改版同步 `/prd update`）

> 监督态自驱。全为规则文档接线（新建 `prd-update.md` + 接线 4 处 + flip references §7/§8），验证 = 读改后正文核契约 + `git grep`/`git diff` 核守恒 + 非回归核对，确定性可复现（auto·可靠）。**待 ACK 冻结后方可进 P4。**

## 块1 · 动作层新建 + 变更检测

- **AC1（新建动作层·镜像 split·契约动作分离）**：新建 `Coder/40_Context_Management/prd-update.md`，定位为改版同步**动作层**——`prd/` 结构/slug 身份/切片逐字/落盘形态一律**回指 `references-schema`、不复述不改写**（同 `prd-split` 手法）；成文分工"`prd-split` 管首切、`prd-update` 管改版（导入后每次 V→V+1）"。
- **AC2（变更检测：清单优先 + diff 兜底 + 对账）**：`prd-update.md` 写死检测协议——以用户**修改项清单**为主 + old/new PRD **diff 兜底** + 两者**对账**（清单没提但 diff 检出的变更必须亮出来问，不静默采信任一方）。对应 grilling 决议 c。

## 块2 · 重新派生落盘 + 登记表认亲基础态

- **AC3（重新派生 + 冻旧版 + 更新 live + bump 版本）**：受影响模块按 `prd-split` 切分机制**重新派生**（复用、不复述算法）；**先冻旧版整份进 `.archive/v<旧版号>/`**（全量快照、自包含）再更新 live 切片到新版；全局版本号 bump（一份 PRD 一个号）。落盘形态**回指 `references-schema §7`**。对应决议 live+快照 a、全局版本 b。
- **AC4（登记表认亲基础态：只做新增 / 消失）**：`prd-update.md` 成文——新版**新增**模块 → 发新 slug、首见版本 = 新版号、状态 `active`；**消失**模块 → 状态置 `removed`、slug 不回收（守 `references-schema §4`）。**显式声明**模块合并/拆分/改名认亲对账**留 R6、本轮不做**。

## 块3 · 三态影响面 + 受影响路由

- **AC5（三态影响面报告·亮牌不自动默认）**：`prd-update.md` 定义改版后扫"哪些工作引用了变更切片"，按三态分类亮牌——**没开工**（未来迭代/路线项）/ **进行中**（active 迭代已引用）/ **已收口**（closed 迭代按旧版验收过）；**只报告、不自动改任何已冻结工作**（"亮牌"＝摆台面让用户定夺、绝不静默默认动作）。对应决议 a。
- **AC6（受影响工作路由·接既有仪式不改流程）**：进行中 → 接 amend 重冻（**回指 `iteration-schema §5.3` + `acceptance-schema §4`** `prd_version` 重绑）；已收口 → closed 不可改、建议开新迭代承接（**回指 `iteration-schema §5.4`** 扩张转迭代）；没开工 → 无需动作。R5 **只回指路由、不改写 amend/扩张仪式本身**。

## 块4 · status · 接线 · flip · 守恒 · 说人话

- **AC7（`/prd status` 只读看板）**：`prd-update.md`（或同文件内一节）定义 `/prd status`——不改盘、只汇总当前 PRD 全局版本 + 登记表（active/removed）+ 最近一次改版三态影响面；定位为只读，与 `/milestone status` 同类。
- **AC8（接线 + flip 收口指针）**：`logic-protocol` 注入表首切行补"改版走 `/prd update`、非重新注入"；`acceptance-schema §4` 那句"属 `/prd update`"补指 `prd-update.md`；`references-schema §7`（快照产生动作）+ `§8` R5 行 flip 为 **✅ 已由 `prd-update.md` 落地**；`README` 结构树 + 说明段注册 `prd-update.md`。
- **AC9（scope 守恒 + 非回归 + 分层）**：改动集限于**新增** `prd-update.md` + **接线** `logic-protocol.md` / `acceptance-schema.md §4` / `references-schema.md §7·§8` / `README.md`。**不做** 模块合并/拆分/改名认亲(R6)；**不改** `references-schema` 契约结构（§3 不加列）/ `prd-split` 切分算法 / `prd_version` 钉版字段 / 核心 P1–P5 与 amend/扩张仪式本身（只回指）/ `project-digest` / `context-persistence` / hook / `VERSION`；**不切版**。**非回归红线**：非 PRD 流一行不动。分层不破坏（改动在 SOP Core `00`/`20`/`40` + README）。
- **AC10（dogfood·说人话）**：本迭代四件套 + `prd-update.md` 正文按说人话三条自检（术语先解释 / 比喻落地 / 别让英文·变量裸奔）；改版同步 / 重新派生 / 冻旧版快照 / 三态影响面 / 亮牌 / 认亲 / `/prd update`·`/prd status` 等首现带一句解释或比喻。
