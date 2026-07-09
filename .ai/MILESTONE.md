# MILESTONE — MILE-0004 · PRD 先行 + references 版本化改版同步

> 方向性产物（非冻结、不走 ACK）。给 `.ai/references/` 补上当年只给了 `.ai/project/` 的"索引 + 渐进加载"待遇，并新增 PRD 先行入口与改版同步协议。设计共识见本文件 §5.3 各路线项与 §5.4 演进记录；决策依据＝2026-07-08 grilling 十节点决议（收在 `docs/research/prd-first-design.html` + 本文件）。

## 5.1 范围评估

**In Scope（版本级）**
- `references/` 子系统升级为**支持知识文件夹式索引 + 渐进读**：`references/prd/00_INDEX` 契约 + **模块登记表**（slug ↔ 当前标题/章节 ↔ 首见版本）+ digest-and-point 读纪律。硬区分：**索引可为摘要、PRD 切片必须逐字原文**。
- **PRD 先行入口**：大 PRD 按语义/模块边界切成 `prd/<slug>.md`（无损）；小 PRD 为单模块退化态（同一套模型）。首切并进 `/milestone`（brief → 路线图 + 切片，一份输入喂两个海拔），路线图项 ↔ 模块 slug 交叉指针。
- **AC 钉版**：AC frontmatter 加 `prd_version`，冻结时绑定、之后钉住；引用锚点＝slug + 绑定版本；接进 P2/P3/P5（External References / References Compliance 支持版本化 slug）。
- **改版同步协议**：`/prd update` 重新派生 + 变更检测（修改项清单优先 + diff 兜底 + 对账）+ `.archive/vN/` 全量快照 + 三态影响面报告 + 接 `acceptance-schema §5.3`(amend) 重冻路径；`/prd status` 看登记表/影响面。

**Out of Scope（版本级）**
- **不碰非 PRD 流**（非回归红线）：对话驱动 / origin brief / `/ideation` 一行不动，核心 P1–P5 不改。PRD 先行是 opt-in 加层。
- 不为 PRD 造平行的"里程碑合成"管线——首切复用现有 `/milestone` brief→MILESTONE 合成。
- 不做子项级变更粒度（模块/切片级即止，要精度靠切细）。
- 不真跑端到端老项目升级（那是既有 dogfood 债、另论）。

**关键交付目标**
- 一份 PRD 从导入 → 切片 → 钉版 → 实现 → 验收 → 改版同步，全链路可走：细节逐字保真、跨改版可审计、已冻结/已收口工作不被静默破坏。

## 5.2 理解阐释

- **核心问题**：里程碑是有损路线图，扛不住组件级实现细节（精确文案、校验规则）；而 `references/` 虽是权威真源通道，却从没享受 MILE-0003 给 `.ai/project/` 的索引 + 渐进读待遇，也没有改版（V1.1→V1.2）同步协议。PRD 一改版，切片/引用/已冻结工作全无章可循。
- **背景与价值**：真实项目多为 PRD 驱动、且 PRD 天然按"修改项"迭代改版（用户实例即 "V1.1 修改项"）。补齐后 PRD 先行成为一等入口，改版有确定性协议兜底，组件细节不被里程碑蒸发。
- **整体影响判断**：改动集中在 `40_Context_Management`（references 索引/读纪律）+ `20_Workflow_Lifecycle`（milestone 入口分支、acceptance/tech-plan/verify 的版本化引用、新 `/prd` 命令族薄层）。**几乎全在复用既有仪式**：`/milestone` 录入、`ack-frozen` + `acceptance-schema §5.3`(amend)、closed 不可改 + 变更开新迭代、收口快照。真新增仅：切分机制、模块登记表、`prd_version` 字段、`/prd update`+`status`、变更检测 + 影响面、`.archive/vN/` 快照。无平行机器。

## 5.3 拆分路线图

> 路线项扁平原子（一项 ≈ 一迭代），按依赖排序。「实际 ITER」开启时才绑号、现留空。预计跨度 ITER-0036 ~ ITER-0041（方向性，真源以台账为准）。

| 路线项 | 主题（方向 → 一个迭代） | 实际 ITER |
|---|---|---|
| **R1** | **references 索引化基座**：新建/扩展 references-schema——`prd/00_INDEX` 契约 + 模块登记表（slug 身份）+ digest-and-point 读纪律 + "索引可摘要/切片必原文"硬区分 + live 目录 vs `.archive/vN/` 落盘契约 | ITER-0036 ✅ |
| **R2** | **PRD 切分机制**：按语义/模块边界切 `prd/<slug>.md`（逐字保真）+ 写登记表 + 小 PRD 单模块退化态 + soft 对齐拆法（提议→确认，绝不切碎一条规则） | ITER-0037 ✅ |
| **R3** | **首切入口并进 `/milestone` + 两海拔交叉指针**：milestone 录入认"brief 是大 PRD"分支 → 触发 R2 切分；路线图项 ↔ 模块 slug 互指（焊上里程碑→references 源指针缺口） | — |
| **R4** | **AC 钉版 + P2/P3/P5 接线**：AC frontmatter `prd_version`（冻结绑定、之后钉住）+ 版本化 slug 引用锚点 + 扩展 acceptance/tech-plan/verify（External References 版本化、Compliance 对钉住版核） | — |
| **R5** | **改版同步 `/prd update`**：重新派生 + 变更检测（清单优先 + diff 兜底 + 对账）+ `.archive/vN/` 全量快照 + 三态影响面报告（没开工/进行中/已收口）+ 接 amend 重冻 + `/prd status`；登记表认亲基础态（新增 / 消失） | — |
| **R6** | **登记表认亲边缘 + 非回归 + 收尾**：模块合并/拆分/改名跨版本认亲对账（松边）+ 非回归门（非 PRD 流一行未动的显式验证）+ README 注册 / HUMAN_GUIDE 用法 / 说人话自检 / dogfood | — |

## 5.4 范围演进记录

- 2026-07-08 · 开启 MILE-0004（承 MILE-0003 于 2026-07-08 收口、开题闸解除）。范围与路线图源自当日 PRD 先行设计 grilling 的十节点决议：真源模型 A（源为真、references 可重生投影）/ 全局版本 b（留版本、执行读最新）/ 冻结绑定 ii / 模块粒度粗 / 检测 c（清单优先+diff兜底）/ 三态 a（亮牌不自动默认）/ slug 登记表 b / 混合触发 c（首切并进 milestone、改版走 /prd update）/ 小 PRD 单模块 b / live+快照 a。松边（模块合并/拆分/改名认亲）显式归入 R6。
