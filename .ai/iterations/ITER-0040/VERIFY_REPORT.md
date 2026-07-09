# VERIFY_REPORT — ITER-0040（MILE-0004 R5 · 改版同步 `/prd update`）

> 监督态自驱。全为规则文档接线（新建 `prd-update.md` + 接线 4 处 + flip references §7/§8）。验证 = 读改后正文核契约 + `git diff` 核非回归 + `git status` 核守恒，确定性可复现（**auto·可靠**）· 无人测道残余。

## 验收结果（逐 AC · auto·可靠）

- [x] **AC1 ✓** 新建 `Coder/40_Context_Management/prd-update.md`，§1 定位镜像 `prd-split`——契约 vs 动作 + **回指表**（结构/slug/逐字/落盘/边界一律回指 references-schema 与 prd-split、不复述）+ 显式分工"`prd-split` 管首切、`prd-update` 管改版（V→V+1）"+ "改版走本机制非重新注入"。
- [x] **AC2 ✓** §2 变更检测三步成文——**清单优先**（用户修改项清单为主）→ **diff 兜底**（旧版 live 切片 vs 新版 PRD 逐字比对防漏）→ **对账**（清单∪diff，清单没提但 diff 检出的必须亮出来问、**不静默采信任一方**）；产出受影响模块清单。对应决议 c。
- [x] **AC3 ✓** §3 重新派生按 `prd-split §2/§4` 复用（不复述算法）；落盘**硬顺序红线成文**——`.archive/v<旧版>/` 全量快照**必须在 live 覆盖之前**冻好（否则旧版原文没了、R4 回溯读落空）+ 再更 live + bump 全局版本；落盘形态回指 `references-schema §7`。对应决议 live+快照 a、全局版本 b。
- [x] **AC4 ✓** §4 登记表认亲基础态——新增→发新 slug/首见版本=新版/`active`；消失→置 `removed`、slug 不回收（守 `references-schema §4`）；用现有登记表字段、**未加列**；模块合并/拆分/改名认亲**显式声明留 R6**。
- [x] **AC5 ✓** §5 三态影响面报告——没开工/进行中/已收口分类表（判定挂 `ITERATIONS` 台账）+ **硬约束"亮牌不自动默认"**成文（只把三态摆台面让用户定夺、绝不静默改已冻结/已收口工作）。对应决议 a。
- [x] **AC6 ✓** §6 受影响路由——进行中→amend 重冻（**回指 `iteration-schema §5.3`+`acceptance-schema §4`**）/ 已收口→closed 不可改、开新迭代承接（**回指 `iteration-schema §5.4`**）/ 没开工→无动作；明写"只回指路由、不改写 amend/扩张仪式本身"。
- [x] **AC7 ✓** §7 `/prd status` 只读看板（当前全局版本 + 登记表 active/removed + 最近改版三态影响面）+ §8 soft 对齐硬约束（改版同 split 提议→确认→落盘，未经确认不得覆盖 live/冻快照/重冻 AC）；status 明定"只读、非改版入口、与 `/milestone status` 同类"。
- [x] **AC8 ✓** 接线四处 + flip：`logic-protocol` 注入表大 PRD 行补"改版走 `/prd update` 非重新注入"；`acceptance §4` "属 `/prd update`"补指 `prd-update.md`；`references §7` 快照产生动作 bullet flip 已落地 + `§8` R5 行 flip **✅ 已由 `prd-update.md` 落地**；`README` 结构树 + 说明段注册 `prd-update.md`。
- [x] **AC9 ✓（守恒 + 非回归 + 分层）** 源改动集 = 新增 `prd-update.md` + 改 `logic-protocol` / `acceptance-schema §4` / `references-schema §7·§8` / `README`（`git status` 佐证）。**非回归红线**：`git diff` 4 处删除均系 flip/append **行替换**（首切行为、`prd_version` 语义、§7/§8 旧文本全保留、只增补），无纯删除、无内容丢失；非 PRD 流（Confluence/MasterGo/insight/其他文档注入行）一字未动。**不做** 合并/拆分/改名认亲(R6)；**不改** `references-schema §3` 登记表字段（未加列）/`prd-split` 切分算法/`prd_version` 钉版字段/核心 P1–P5 与 amend·扩张仪式本身（只回指）/`project-digest`/`context-persistence`/hook/`VERSION`；**不切版**。改动在 SOP Core（`00`/`20`/`40`）+ README，分层未破坏。
- [x] **AC10 ✓（dogfood·说人话）** 改版同步（"PRD 出新版怎么同步"）/ 重新派生（"按新版原文重切受影响模块"）/ 冻旧版快照（"旧版整份复制冻存"）/ 三态影响面（表 + 每态一句）/ 亮牌（"亮出来给人看、等人拍板，不是检测到就自动改"）/ 认亲（"新版模块对回旧版是谁"）/ `/prd update`·`/prd status`（首现带释义）均带解释；英文命令有中文语境包裹、无裸变量残留。

## 独立复核

- **执行**：干净上下文子 agent，验证者≠实现者、只读、对抗式；核心对抗点（亮牌不自动/不静默改已冻结 · 落盘先冻后更 · 复用不造轮子只回指 · 契约动作分离 · 不越界做 R6/不改契约结构/钉版字段/核心仪式）逐点核。
- **结论**：**APPROVE**（clean，无 Must/Should/Nit）。八对抗点全过——① 亮牌不自动双重钉死（§5「绝不静默替用户改已冻结/已收口」+ §8「不得自动重冻任何 AC」）；② 落盘先冻后更硬顺序成文、明写颠倒后果（旧版原文丢失废掉 R4 回溯）；③ 切分复用 prd-split 不抄算法、重冻/扩张回指 `iteration-schema §5.3(Amend)/§5.4(Escalate)`、落盘回指 references §7，被回指目标全部真实且语义对得上；④ §1 回指表未复述契约、§7/§8 flip 正确指向 prd-update；⑤ 认亲只做新增/消失、R6 显式留、references §3 登记表未加列、§8 R6 行未 flip、prd-split/钉版字段 diff 空、非 PRD 注入四行一字未动。AC1–AC10 逐条 confirm。**悬空指针专查**：16 处 §-引用逐个核实真实存在，无 ITER-0035/0039 那类把有序列表项写成不存在子节号的问题。Must/Should/Nit 均无。

## Remaining Risks

- **改版协议成文、但从未真跑**：`/prd update` 全套（检测→重新派生→冻快照→三态影响面→路由）靠执行遵从，真到用户端到端拿一份 PRD 改一次版才第一次实战检验——这也是 R4 钉版回溯路径的首次兑付点。
- **三态判定依赖引用可发现**：进行中/已收口判定靠"迭代 AC 引用了变更 slug"——若某迭代引用了 PRD 却没在 `External References`/frontmatter 如实标 slug 与 `prd_version`，影响面扫描可能漏判。取决于 R4 钉版纪律的执行遵从。
- **认亲只到新增/消失**：模块改名/合并/拆分在本轮会被误判为"旧的消失 + 新的新增"（两条独立记录），真正的跨版本身份延续待 R6 认亲对账。
