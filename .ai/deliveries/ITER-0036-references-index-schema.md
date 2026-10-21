# 给参考资料补上"索引 + 渐进读"的契约地基（references 索引化基座）

> ITER-0036 · 里程碑 MILE-0004 首块（R1）· 收口 2026-07-09 · 监督态自驱（承 2026-07-08 grilling 十节点决议；P5 起独立复核守质量）· 不切版（纯规则新增）

## 本次交付目标

- butler 里有两个"外部资料收件箱"：一个是 `origin/`（人类丢原始概念稿的地方），另一个是 `.ai/references/`（把项目**之外**的权威资料——接口文档、设计稿、PRD——经处理后存进来，供后续阶段按指针引用、不必让用户反复贴）。
- 上一个大版本（MILE-0003）给**项目自身**的全貌产物 `.ai/project/` 升级成了"知识文件夹"待遇：有入口地图（`00_INDEX`）、按主题渐进读、不一次性全部塞进上下文。但 `.ai/references/` **当年没被这套待遇覆盖到**——它有人管注入（`logic-protocol`）、有人管目录（`mcv-deployment`）、有人管"哪些验收源自它"（`External References` 字段），却**从来没有一份 schema** 说清楚：references 内部到底长什么样、该怎么读。
- 新版本 MILE-0004 要做的"PRD 先行 + 版本化改版同步"，全都得踩在"references 有索引、有稳定的模块身份、有版本落盘"这块地基上。本轮（R1）就是**先把这块地基浇好**：新建一份契约文件，把 references 的结构、读法、身份、落盘形态一次定死。**只定契约、不做动作**——真正把 PRD 切成片、从 `/milestone` 触发首切、给验收标准钉版本、改版时同步，都留给后续 R2–R5。

## 已完成内容

- **新建 `Coder/40_Context_Management/references-schema.md`**——`.ai/references/` 子系统的首份结构契约，八节：
  - **§1 定位 + 与 `.ai/project/` 的分工**：一张表钉死两者不重叠——project 存"项目自身全貌"、是**有损摘要**（当前真相覆写旧结论）；references 存"项目之外的权威资料"、**含无损切片**（PRD 原文逐字投影）。一句话记：一个把项目积成有损地图，一个把外部规格无损钉在墙上。
  - **§2 两态**：小而消化过的资料走**扁平态**（`api-` 接口 / `design-` 设计稿 / `insight-` 分析报告，一个文件装下、不建索引）；大而结构化的权威规格（典型即 PRD）走**知识文件夹态** `prd/`（索引 + 渐进读 + 无损切片 + 带版本）。
  - **§3 `prd/` 结构**：`00_INDEX` 入口（叙述 + **模块登记表**）；登记表每模块一行——`slug`（终身身份）↔ 当前标题/章节（会变的门牌）↔ 首见版本 ↔ 当前版本 ↔ 状态（`active`/`removed`）。
  - **§4 slug 身份规则**：`slug`（模块的终身英文代号，如 `save-validation`）**一次分配、终身不变、只增不改**——章节号是会变的门牌、slug 是不变的身份，引用永远指 slug。这是后续 R5/R6 改版"认亲"（新版切片对回旧模块）的锚点。
  - **§5 读纪律 digest-and-point**：读 prd 先读 `00_INDEX` 地图 → 按手头任务只钻用到的那片 `prd/<slug>.md` → 需要更细再顺指针钻源；不一次性读整份 PRD（长 PRD 就是这样省上下文的）。执行默认读 live 最新，回溯才去翻旧版归档。
  - **§6 无损 vs 有损硬区分（命门）**：`00_INDEX`（含登记表）**可以是摘要**（它是找路的地图）；`prd/<slug>.md` 切片**必须逐字原文、无损**（PRD 里的精确文案、精确校验规则，少一个字验收就错）。写成硬约束：**不得对切片套用 `.ai/project/` 那种"当前真相覆写"的概括 / 蒸馏语义**。
  - **§7 落盘契约**：`prd/<slug>.md`（live 目录、最新版、无版本前缀、执行直读）+ `.archive/vN/`（改版时把旧版整份冻进来的全量快照、审计/回溯用）。只定"落盘长什么样"，不定"何时怎么冻"。
  - **§8 边界**：一张前向指针表，把"产生 / 变更动作"（切分 R2 / 入口 R3 / 钉版 R4 / 同步 R5 / 认亲 R6）显式标出、本轮一律不落实现。
- **`Coder/README.md` 双处注册**：目录结构树 `40_Context_Management` 下补 `references-schema.md`；规则说明段补一条（定位 + 与 project-digest 的分工 + 动作属 R2–R5）。守"新增规则文件必须注册"的仓库约束。

## 关键变更 / 用户可感知变化

- **references 从此有了"内部长什么样"的说明书**：以前 AI 往 `.ai/references/` 存资料，只知道"往这放"，不知道大资料该怎么组织、怎么读；现在有了明确契约——大 PRD 该切片、该建索引地图、该逐字保真、该带版本落盘。
- **本轮对日常使用暂无可感知的新动作**：R1 是**纯契约地基**，没有新命令、没有新交互。真正能"把一份 PRD 导进来自动切片、钉版、改版同步"要等 R2–R5 逐块落地。本轮的价值是**让后面几块有确定的地基可踩**，而不是现在就能用。
- **一条贯穿整个 MILE-0004 的红线被先立住了**：PRD 切片必须逐字原文、绝不能被"顺手概括"。一旦有人拿项目摘要那套有损压缩去套 PRD 切片，PRD 里精确的文案和校验规则就废了——这条红线现在写成了 schema 里的硬约束。

## 高层影响范围

- 新增（1 份规则文件）：`Coder/40_Context_Management/references-schema.md`（八节契约，约 110 行）。
- 改（1 份）：`Coder/README.md`（目录结构树 + 规则说明段各补一条注册）。
- 没碰（守边界）：references 既有扁平用法（`api-`/`design-`/`insight-` 注入照旧、`logic-protocol` 注入真源不动、`External References` 字段不动）、`project-digest-schema` / `context-persistence` 语义、`mcv-deployment` 目录定义、hook、`VERSION`。**不写**任何切分 / 入口 / 钉版 / 同步的产生动作（留 R2–R5），**不切版**。

## 验证方式与结果摘要

- **9 项验收（AC1–9）全过**，全 **auto·可靠**（纯规则文档：读改后正文核契约 + `git grep` 核守恒，确定性可复现），无人测残余。
- **独立复核 APPROVE-with-nits**（另起干净上下文子 agent、验证者≠实现者、只读、对抗式挑毛病）：四个对抗重点——"无损/有损红线够不够硬""读纪律有没有和 project-digest 双写""slug 规则能不能撑起 R5 认亲""边界有没有越界去做动作"——A/C/D 三点过。复核挑出并**已修** 1 处 Should Fix：§5 把"digest-and-point 读法的真源"指向了 `project-digest-schema`，指浅了一层——读纪律的真源其实是 `context-persistence.md §6`（`project-digest §5` 是配套的**写侧**密度契约、非读侧）。已改指读侧真源，并并列点出写侧归属，与 project-digest 自身的分工口径对齐；AC3、01_CHANGELOG、TECH_PLAN 同步更新。

## 已知剩余风险 / 延后事项

- **契约地基的正确性要等后续真踩上来才完全证伪**：R1 只是契约，它设得对不对，最终要到 R2（真切分）/ R5（真同步）踩上来才彻底验证。本轮靠"能不能支撑 R2–R6 的动作"做前瞻性对抗核，但契约若有隐性设计缺陷，可能要到后续迭代才暴露。
- **无损/有损红线靠规则文字约束、非机器强制**：真到 R2 切分时是否严格逐字、不"顺手概括一下"，取决于执行的 AI 遵从——和知识文件夹折叠质量、`[add-field]` 草稿值确认属同一套信任模型。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0036/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动产物：`Coder/40_Context_Management/references-schema.md`（新建，§1–§8）、`Coder/README.md`（目录结构 + 规则说明注册）
- 里程碑与设计依据：`.ai/MILESTONE.md`（MILE-0004 §5.3 路线图 R1–R6）、`docs/research/prd-first-design.html`（十节点 grilling 决议可视化）
- 相关契约（分工对照）：`project-digest-schema.md`（`.ai/project/` 写侧密度契约）、`context-persistence.md §6`（digest-and-point 读侧真源）、`logic-protocol.md`（references 注入真源）
