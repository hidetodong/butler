# TECH_PLAN — ITER-0040（MILE-0004 R5 · 改版同步 `/prd update`）

> 监督态自驱。目标见 CONCEPT、验收见 AC_LIST，不重述。全为规则文档接线（新建 1 + 接线 4 + flip，无代码）。

## 设计决策（DD）

- **DD1 · 镜像 `prd-split` 的动作层骨架**：`prd-update.md` frontmatter + §1 定位（契约 vs 动作、回指表、split=首切/update=改版分工）严格对照 `prd-split.md` 写，读者一眼看出两者同族。回指 `references-schema` 的规矩沿用 split 的回指表，不复述契约。
- **DD2 · 检测协议成文为"三步"**：清单优先（读用户修改项清单）→ diff 兜底（old live 切片 vs new PRD 对应段）→ 对账（清单∪diff，差集亮出来问）。不写具体 diff 工具命令（规则层不绑实现），只定"清单为主、diff 防漏、分歧必亮"的口径。
- **DD3 · 落盘顺序写死"先冻后更"**：`.archive/v<旧版>/` 全量快照**必须在** live 更新**之前**冻好（否则旧版原文被覆盖就冻不出了）——这是 AC3 的硬顺序。快照形态/live 形态回指 `references-schema §7`，不复述。切分复用 `prd-split`、只写"按 split 重新派生受影响模块"，不抄算法。
- **DD4 · 认亲基础态挂登记表状态字段**：新增/消失只动 `00_INDEX` 登记表的 `状态`（active/removed）+ 新增行的 `首见版本`——用的是 `references-schema §3` 已有字段，**不加列**（守 AC9）。合并/拆分/改名显式一句"留 R6"。
- **DD5 · 三态判定靠台账、路由靠回指**：三态用现成台账判（没开工=路线项/无引用；进行中=`ITERATIONS` active 迭代引用了变更 slug；已收口=closed 迭代引用了）。路由到 amend（`iteration §5.3`）/ 扩张（`iteration §5.4`）/ acceptance §4 重绑，全**回指、不改写**那些仪式。"亮牌不自动"写成硬约束句。
- **DD6 · `/prd status` 定位只读**：与 `/milestone status` 同类，明确"不改盘、只读汇总"，避免被误用为改版入口。
- **DD7 · 接线最小侵入 + flip 用既有翻牌手法**：`logic-protocol` 首切行**尾部加一句**（不动首切主体）；`acceptance §4` 那句"属 `/prd update`"**补个指针**（不改语义）；`references §7` 快照产生动作 bullet + `§8` R5 行由待→✅（同 R1–R4 翻牌）；`README` 结构树 + 说明段各加一行。

## 影响面（章节级）

| 文件 | 改动 | AC |
|---|---|---|
| **新增** `Coder/40_Context_Management/prd-update.md` | frontmatter + §1 定位（契约vs动作/回指表/split·update 分工）+ §2 变更检测（清单优先+diff兜底+对账）+ §3 重新派生+落盘（先冻旧版快照再更 live、复用 split、回指 §7）+ §4 登记表认亲基础态（新增/消失、合并拆分改名留 R6）+ §5 三态影响面（亮牌不自动）+ §6 受影响路由（回指 amend/扩张）+ §7 `/prd status` 只读 + §8 soft 对齐硬约束 | AC1–7 |
| `Coder/00_System_Prompt/logic-protocol.md` | 注入表首切行尾补"改版走 `/prd update`（见 prd-update.md）、非重新注入" | AC8 |
| `Coder/20_Workflow_Lifecycle/acceptance-schema.md §4` | `prd_version` bullet 那句"属 `/prd update`"补指 `prd-update.md` | AC8 |
| `Coder/40_Context_Management/references-schema.md §7·§8` | §7 快照产生动作 bullet flip 已落地 + §8 R5 行 flip ✅（指 prd-update.md） | AC8 |
| `Coder/README.md` | 结构树 + 说明段注册 `prd-update.md` | AC8 |

**不碰**：`references-schema §3` 登记表字段（不加列）、`prd-split` 切分算法、`prd_version` 钉版字段与解析、`milestone-schema`、核心 P1–P5 与 amend/扩张仪式本身（只回指）、`project-digest`、`context-persistence`、hook、`VERSION`；不做合并/拆分/改名认亲(R6)；不切版。

## Execution Steps（可勾选）

- [ ] S1 · 新建 `prd-update.md` frontmatter + §1 定位（镜像 prd-split：契约vs动作 + 回指表 + split首切/update改版分工）→ AC1
- [ ] S2 · §2 变更检测（清单优先 → diff 兜底 → 对账，分歧必亮、不静默采信）→ AC2
- [ ] S3 · §3 重新派生 + 落盘（**先冻旧版 `.archive/v<旧版>/` 全量快照再更 live**、复用 prd-split 切分不复述、bump 全局版本、回指 references §7）→ AC3
- [ ] S4 · §4 登记表认亲基础态（新增发新 slug/首见版本、消失置 removed、slug 不回收；合并/拆分/改名留 R6）→ AC4
- [ ] S5 · §5 三态影响面（没开工/进行中/已收口分类 + **亮牌不自动默认**硬约束）→ AC5
- [ ] S6 · §6 受影响路由（进行中→amend 回指 iteration §5.3 + acceptance §4 / 已收口→扩张回指 iteration §5.4 / 没开工→无动作，不改仪式）→ AC6
- [ ] S7 · §7 `/prd status` 只读看板 + §8 soft 对齐硬约束（改版同 split 提议→确认→落盘）→ AC7
- [ ] S8 · 接线：`logic-protocol` 注入表 + `acceptance §4` 补指针 + `references §7·§8` flip + `README` 注册 → AC8
- [ ] S9 · scope 守恒（`git status`）+ 非回归核对（`git diff` 非 PRD 流未动、契约结构/切分算法/钉版字段未碰）+ 说人话三条自检 → AC9/AC10
- [ ] S10 · P5 独立复核（干净上下文子 agent、对抗式）→ 收口

## 验证策略

全 auto·可靠（规则文档）：每 AC 读改后正文确认 + `git grep`/`git diff` 核守恒。核心对抗点＝**亮牌不自动**（三态只报告、不静默改已冻结工作）+ **落盘先冻后更**（旧版快照在 live 更新前冻好）+ **复用不造轮子**（切分复用 split、重冻/扩张复用既有仪式只回指）+ **契约动作分离**（update 回指 references 契约不复述）+ **不越界**（认亲只到新增/消失、不做 R6，不改契约结构/钉版字段/核心仪式）。dogfood：四件套 + prd-update 正文过说人话三条。无人测道残余。
