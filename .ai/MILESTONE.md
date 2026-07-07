# 里程碑：项目知识文件夹升级 + 帮手名册 + 说人话（MILE-0003）

> butler 第三个里程碑。方向性产物，可随推进演进（milestone-schema §7.3），不走 ACK 冻结门。
> 开题 2026-07-05（承 MILE-0002 于 2026-07-03 收口、开题闸解除）。预研总纲见 `docs/research/MILE-0003-preresearch-brief.md`。

## 范围评估

三条线并行：**主体（知识文件夹）+ 子项一（帮手名册）+ 子项二（说人话）**。

### In Scope（版本级）

**主体 · 项目知识文件夹**（`PROJECT.md` → `.ai/project/`）

- 把单文件 `.ai/PROJECT.md` 解构为 `.ai/project/` 主题知识文件夹（`00_INDEX.md` 入口 + 按主题分文件 + 每份边界 + 写作密度口径），改写 `project-digest-schema`。
- 反转维护哲学：从"按需微调"→"每次收口强制按主题折叠 delta"（泛化 `iteration-schema §5.5` / `milestone-schema §7.4`）+ 新增知识文件夹漂移自检不变量（扩冷启动一致性自检）。
- 冷启动读序切换（`context-persistence §6` 第一读改 `project/00_INDEX` + 主题）+ digest-and-point 纪律（已有真源不复制、只摘全貌 + 指针）。
- 部署种子（`mcv-deployment` 带空模板）+ 老项目迁移配方（`PROJECT.md → project/` 的 rename+split+restamp）。
- butler 仓自身 dogfood：用新结构重写自身 `.ai/project/` 并对齐现实。

**子项一 · 帮手名册**（Butler Agent 名册）

- 新建 `Coder/62_Extension_Agents/`：`overview.md` 总述（帮手是啥 + 通用规矩 G1–G4 唯一真源 + 名册表 + 触发式加载）+ 三帮手完整定义（复核 `independent-review` / 更新说明 `knowledge-fold` / 查过时 `drift-check`）。
- 帮手 = 一份中立定义资料、用时读、临时起干净子 agent 执行，**不下发到项目**（同现有 `/review`）。
- 复核帮手三拆：`60_review` 按性质拆（共享审查流程留原地 / 通用规矩提总述 / 复核专有契约进 `independent-review`）；G2 诚实兜底单源回指修正（正文现只在 `review-engine §6.4`，上提总述后 `dangerous §7.3` + `verify-schema §4` 引用改指总述）。

**子项二 · 说人话**（讲人话扩到所有面向人输出）

- 三条硬标准（术语先解释 / 比喻要落地 / 别让英文·变量裸奔）+ 发长文前自检，落进 `presentation-protocol`（对话层）+ `artifact-style`（文档层，从四件套扩到所有面向人输出）。

### Out of Scope（版本级）

- 不改 P1–P5 阶段状态机、四件套字段结构、AC 验收脊柱、迭代/里程碑双层。
- 不把知识文件夹变成变更流（那是 `ITERATIONS`/`CHANGELOG` 的活）；不追细节完整——是广度地图、非疆域百科。
- ❌ 帮手文件下发到每个项目（明确否掉；用时读定义即可）。
- ❌ 完全无人值守的后台自动生成 / 自动跑（"自动化留后续"指的是这个，**不是**收尾唤帮手折叠——后者本轮做）。
- ❌ 权限的"工具层硬拦"（可选增强、留后续；本轮靠契约约定 + G2 诚实兜底兜着）。

### 关键交付目标

- 冷启动"整体"产物从薄索引升级为随迭代越来越完整、AI 读完真懂"项目里有什么"的实体知识库；靠"强制 + 可验证的收口折叠"保证不腐（生死前提，见理解阐释）。
- butler 派出去的帮手从散落 5 文件的"复核"一个，立成名册化三帮手 + 通用规矩唯一真源。
- butler 输出（对话 + 落地文档）不堆术语黑话，可读性成硬纪律、可自检。
- **版本级**：本里程碑重构冷启动核心产物契约 + 读序 + 迁移，按 semver 属 **MAJOR**，收口切 **v2.0.0** + 迁移配方 + tag。

## 理解阐释

### 核心问题

- 现 `.ai/PROJECT.md` 是 ≤1500 tokens 的薄索引（几个关键词 + "细节看代码"），AI 冷启动读完并不真知道"项目里有什么"，容易沦为"说几个关键词假装体系有用"。
- butler 的帮手一直是散的：真正的帮手只有"复核"，其说明摊在 5 个文件各写一遍；MILE-0003 正把帮手从 1 变 3，是立名册最顺的时机。
- butler 输出容易堆术语黑话，看着专业其实难懂——注意"简短"≠"好懂"。

### 背景与价值

- 知识文件夹：把冷启动整体产物从"薄索引"升级为"随迭代越补越全"的知识库，AI 读完真懂项目、少走弯路。代价是更高维护纪律——用"收口强制折叠 + 漂移自检"这笔账换"真能用"。**最大风险**：陈旧的完整比诚实的薄更毒（AI 信滞后内容做错判），整套设计生死系于"强制 + 可验证的收口折叠"。
- 帮手名册：把帮手能力目录化，便于从 1 扩到 3 及以后；更新说明另起干净帮手做（避免主线刚干完活、快没精力时顺手做导致质量差、说明过时）。
- 说人话：让 butler 面向人的输出真好懂，覆盖对话与落地文档（文档措辞再严谨些）。

### 对系统的整体影响

- `40_Context_Management/project-digest-schema.md`：单文件 schema → 文件夹 schema（主题集 / 边界 / INDEX / 密度）。
- `20_Workflow_Lifecycle/iteration-schema.md §5.5` / `milestone-schema.md §7.4`：前滚从"单文件·按需"泛化为"文件夹·按主题·必做"。
- `40_Context_Management/context-persistence.md §6` + 冷启动一致性自检：读序切换 + 扩知识文件夹漂移不变量。
- `20_Workflow_Lifecycle/mcv-deployment.md` + `migrations/`：部署种子 + 迁移配方。
- 新增 `Coder/62_Extension_Agents/`（名册）+ 注册进 `Coder/README.md`。
- `60_Extension_CodeReview/review-engine.md`：复核三拆（带地址的搬家清单）；`65_Extension_Dangerous/dangerous-engine.md §7.3` / `verify-schema.md §4` 的 G2 引用改指总述。
- `00_System_Prompt/presentation-protocol.md` + `20_Workflow_Lifecycle/artifact-style.md`：说人话三条 + 发长文自检。
- 版本：MAJOR（v2.0.0）。**利好**：`PROJECT.md` 不受 hook 门禁（hook 只拦 CONCEPT/AC/TECH_PLAN + 台账），本次无需改 hook，耦合面小于看起来。

## 拆分路线图

预计跨度：约 8 个迭代（ITER-0026 起，一路线项 ≈ 一迭代；实际 ITER 开启时才绑号，见 §5.3 不预占号）。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 帮手名册骨架 + 复核三拆 + 通用规矩单源化：新建 `62_Extension_Agents/`（overview 总述 + independent-review）；G1–G4 提总述当唯一真源、G2 诚实兜底单源回指修正、注册进 `Coder/README`（作知识文件夹"总述+分文件+登记"模式的内部预演） | ITER-0026 | closed |
| R2 | 知识文件夹 schema：`PROJECT.md` 解构为 `.ai/project/`（00_INDEX + 主题集 + 每份边界 + 写作密度口径），改写 `project-digest-schema` | ITER-0028 | closed |
| R3 | 维护回路：收口强制按主题折叠 delta（泛化 `iteration-schema §5.5` / `milestone §7.4`）+ 知识文件夹漂移自检不变量（扩冷启动一致性自检） | ITER-0029 | closed |
| R4 | 更新说明 + 查过时两帮手定义成型 + 接线：住进 `62_Extension_Agents/`、登记总述；接维护回路（收尾唤更新说明折叠）与冷启动 / 收口抽查（查过时） | ITER-0030 | closed |
| R5 | 冷启动读序切换 + digest-and-point 纪律：`context-persistence §6` 第一读改 `project/00_INDEX` + 主题；已有真源不复制 | ITER-0031 | closed |
| R6 | 部署种子 + 迁移配方：`mcv-deployment` 带空模板；老项目 `PROJECT.md → project/` 的 `[rename]`+`[split]`+`[restamp]` 迁移配方 | ITER-0032 | closed |
| R7 | 说人话：三条标准 + 发长文自检落进 `presentation-protocol`（对话）+ `artifact-style`（扩到所有面向人输出） | ITER-0033 | closed |
| R8 | butler 仓自身 dogfood：用新结构重写自身 `.ai/project/` 并对齐现实 + 文档注册（`HUMAN_GUIDE` / `README`）+ 切版 v2.0.0 | — | planned |

## 范围演进记录

- 2026-07-05：**开启 MILE-0003**（承 MILE-0002 于 2026-07-03 收口、开题闸解除）。方向据预研总纲 `docs/research/MILE-0003-preresearch-brief.md` 及两份子设计（`MILE-0003-project-knowledge-folder.html` 主体、`MILE-0003-agent-doc-design.md` 帮手名册）合成。三条线：知识文件夹（主体）+ 帮手名册（子项一）+ 说人话（子项二）。已定关键决策并入路线——帮手=定义资料用时读不下发、三帮手本轮都做、权限靠约定 + G2 诚实兜底（硬拦留后续）、复核三拆、名册落 `62_Extension_Agents/`（开题确认）、说人话落 `presentation-protocol` + `artifact-style`。版本定性 MAJOR（收口切 v2.0.0）。路线图为草案，soft 对齐后仍可演进；实际 ITER 开启时才绑号。
- 2026-07-05：**R1 收口**（ITER-0026，`/dangerous` 危险模式自治，P5 独立复核 8/8 confirm、0 Must Fix）。帮手名册骨架 `62_Extension_Agents/` 立起（overview 总述 + independent-review），G1–G4 通用规矩单源化落定、复核三拆完成、README 注册。名册"总述+分文件+登记"模式预演跑通，为主体（知识文件夹 R2）验证了结构。路线图未演进。北极星=R1 单迭代已达成、交还用户；R2–R8 及 v2.0.0 切版待后续指令。
- 2026-07-06：**开 R2**（ITER-0028，监督态自驱，主体开篇）。知识文件夹 schema 定稿——把 `project-digest-schema.md` 从单文件薄索引契约改写为 `.ai/project/` 知识文件夹契约（00_INDEX 入口 + 推荐核心 topic 集 + 每份边界 + digest-and-point 密度 + 三条矛盾消解 + 折叠模型声明 + 受控扩展登记）。R2 只定 schema；强制折叠+漂移自检（R3）/ 读序切换（R5）/ 部署种子+迁移（R6）/ butler 自身适配（R8）用前向指针标注、本轮不实现。路线图未演进（仅绑号 + R2 转 active）。北极星=R2 单迭代。（注：ITER-0027 系独立迭代[最小实现纪律]、与本里程碑正交、不入含迭代。）
- 2026-07-07：**R2 收口**（ITER-0028，监督态自驱，P5 独立复核 8/8 confirm、0 Must Fix、0 false-green）。知识文件夹 schema 落定——`project-digest-schema.md` 整篇改写为 `.ai/project/` 契约，哲学切换（薄索引→知识地图）+ 三条矛盾消解 + 折叠模型声明（强制留 R3）+ 前向指针 R3/R5/R6/R8 如实标注。scope 守恒：仅改 schema + README 两规则文件，未越界、未 rename、未触 R3/R5/R6/R8 目标文件与 `.ai/PROJECT.md`。路线图未演进。北极星=R2 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R3–R8（v2.0.0 切版在 R8）待后续指令。
- 2026-07-07：**开 R4**（ITER-0030，监督态自驱，承 R1 名册骨架 + R3 回路）。补齐名册另两个帮手——更新说明 `knowledge-fold`（收尾把 delta 折进 `.ai/project/`、只写该目录）+ 查过时 `drift-check`（冷启动/收口对着真实代码抽查说明过时、只读），完整定义 + overview 名册表转 ✅ + 最小回指接线（knowledge-fold 接 R3 收口步④折叠、drift-check 接第 6 漂移不变量）+ README 注册。**定位**：折叠必做（R3）不变，两帮手是推荐唤起的 fresh-context 专职执行者（避免主线疲劳顺手做质量差）、opt-in 非强制，权限靠约定 + G2 诚实兜底（硬拦留后续、承 R1）。R4 不碰 R5/R6/R8、不改 R3 强制语义。路线图未演进（仅绑号 + R4 转 active）。北极星=R4 单迭代。
- 2026-07-07：**R3 收口**（ITER-0029，监督态自驱，P5 独立复核 8/8 confirm、0 Must Fix，两态兼容 5 处逐处 confirm）。维护回路接线落定——收口步④泛化为两态（文件夹态按主题必做折叠 / 单文件暂态按需前滚）+ 冷启动一致性自检加第 6 条「知识文件夹漂移自检」（条件不变量、单文件 N/A）+ 全仓 5→6 计数同步 + 顺修 R2 遗留 §5→§6 及介绍段"强制化"漂移 + 翻 project-digest §6/§9 R3 指针（待→已）。两态兼容硬约束落实：不砸含 butler 自身在内的单文件项目收口。scope 守恒：改 6 规则文件，未越 R5（读序第一读）/R6（部署迁移）/R8（butler 实体迁移）、未 rename、未切版。路线图未演进。北极星=R3 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R4/R5/R6/R7/R8（v2.0.0 切版在 R8）待后续指令。
- 2026-07-07：**R4 收口**（ITER-0030，监督态自驱，P5 独立复核 8/8 confirm、0 Must Fix、0 Should Fix）。帮手名册补齐——新建 `62_Extension_Agents/knowledge-fold.md`（更新说明帮手：收尾把 delta 折进 `.ai/project/`、只写该目录、六段式镜像 independent-review）+ `drift-check.md`（查过时帮手：冷启动/收口对着真实代码抽查说明过时、只读、输出漂移清单落 `.ai/references/`）两份完整定义 + overview 名册表两行转 ✅ 去占位（co-edit）+ 最小回指接线（knowledge-fold 接收口步④折叠 / drift-check 接第 6 漂移不变量）+ README 注册。名册从"1 已立 + 2 占位"成"3 帮手均完整定义"。**核心对抗点（opt-in 非强制）逐处过关**：接线两处均"推荐唤"非"必须唤"、R3 折叠必做 / 第 6 不变量强制语义未削弱、两 §诚实兜底回指 G2（起不了子 agent 主线自做并如实标注、绝不跳过折叠/自检本身）；权限靠约定 + G2（硬拦留后续、承 R1）。scope 守恒：改 2 新增 + 4 编辑（overview/iteration/context-persistence/README），未越 R5（读序第一读仍 PROJECT.md）/R6（mcv+migrations 未碰）/R8（butler 自身仍单文件、`.ai/project/` 不存在）、未 rename、未切版。收口前滚 `.ai/PROJECT.md` 帮手名册条（1→3 帮手）。路线图未演进。北极星=R4 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R5/R6/R7/R8（v2.0.0 切版在 R8）待后续指令。
- 2026-07-07：**开 R3**（ITER-0029，监督态自驱，承 R2 折叠模型声明）。维护回路接线——泛化收口步④为两态（项目采用 `.ai/project/` 则按主题路由 delta 必做折叠 / 仍单文件 `.ai/PROJECT.md` 则按需前滚，泛化 `iteration-schema §5.5` + `milestone §7.4`）+ 冷启动一致性自检加第 6 条「知识文件夹漂移自检」（条件适用、单文件 N/A）+ 全仓 5→6 计数同步 + 顺修 R2 遗留 §5→§6 引用漂移 + 翻 `project-digest §6/§9` R3 指针（待→已）。**关键设计约束=两态兼容**：R6 部署种子 / R8 butler 自身迁移未落地，此刻含 butler 在内多数项目仍单文件，新收口步 + 新不变量不得砸其收口（单文件走旧路、第 6 条 N/A）。R3 不碰读序第一读切换（R5）/ 部署种子迁移（R6）/ butler 实体迁移（R8）/ 切版。路线图未演进（仅绑号 + R3 转 active）。北极星=R3 单迭代。
- 2026-07-07：**开 R5**（ITER-0031，监督态自驱，承 R2 文件夹契约 + R3 两态纪律）。冷启动读序切换——`context-persistence §冷启动读序` 第 1 项从写死 `.ai/PROJECT.md` 泛化为两态（采用 `.ai/project/` 则先读 `00_INDEX` + 按需主题 / 仍单文件则读 `.ai/PROJECT.md`）+ 读侧 digest-and-point 纪律（读地图→按需钻主题、不 slurp→指针钻代码）+ 翻 `project-digest` R5 指针（介绍段/§9/header 待→已）+ README/handoff-spec 两态措辞同步。**关键设计约束=两态兼容**（同 R3）：R6 部署种子 / R8 butler 迁移未落地、此刻含 butler 在内多数项目仍单文件，第一读若写成无条件 `00_INDEX` 会指向不存在文件砸其冷启动——故单文件分支显式保留。R5 不碰部署种子迁移（R6）/ butler 实体迁移（R8）/ 说人话（R7）/ 切版，不改 R3 强制语义与 `.ai/project/` 结构。路线图未演进（仅绑号 + R5 转 active）。北极星=R5 单迭代。
- 2026-07-07：**开 R6**（ITER-0032，监督态自驱，承 R2 文件夹契约 + R5 两态读序）。部署种子 + 文件夹化迁移配方**规则层准备**——`mcv-deployment §2` 全貌产物条两态化（新项目 `.ai/project/` 知识文件夹 / 单文件 `PROJECT.md` 遗留暂态）+ 部署建**空** `.ai/project/` 种子（唯一"部署即建"的 `.ai/` 子目录例外、`00_INDEX` 不 stub·首收口前滚生、冷启动键控入口文件不踩空）+ line 45 老项目升级指针指 R6 配方；`migration-schema §4` 补 `[split]` typed 标签（通用定义 + `PROJECT.md → .ai/project/` 首例 + 起始态校验 + 冲突即停）+ 形态文档化·条件式前向指针指 R8/v2.0.0。**关键设计约束=两态兼容**（承 R3/R5）：块1 只对新部署生效、块2 只在切版消费时跑，均不砸现存单文件项目。**R6/R8 边界**：不写 `migrations/v2.0.0.md` 实例（配方切版时产、`versioning §6.3 步4`、归 R8）、不迁 butler 自身实体、不切版、不改 R3 折叠必做/第 6 不变量、不改 R5 读序第一读、不动 hook。路线图未演进（仅绑号 + R6 转 active）。北极星=R6 单迭代。
- 2026-07-07：**R5 收口**（ITER-0031，监督态自驱，P5 独立复核 8/8 confirm、0 Must Fix）。冷启动读序切换落定——`context-persistence §冷启动读序` 第 1 项泛化为两态（采用 `.ai/project/` 先读 `00_INDEX` + 按需主题 / 仍单文件读 `.ai/PROJECT.md`）+ 读侧 digest-and-point 纪律（读地图 → 按需钻主题、不 slurp → 指针钻代码、预算有界）+ 收尾互补句两态 + 翻 `project-digest` R5 指针三处（介绍段/§9 header/§9 路线项，待→已接线）+ README/handoff-spec 两态措辞同步。**核心对抗点（两态兼容）四处逐处 confirm**：第一读均两态、单文件分支显式（context-persistence 与 project-digest §9 显式含 butler 自身）、全仓无一处无条件 `00_INDEX`——不砸含 butler 在内单文件项目冷启动。scope 守恒：改 4 规则文件，未越 R6（mcv/migrations）/R7（说人话）/R8（butler 实体迁移+切版）、未 rename、无新增规则文件、未切版。收口前滚 `.ai/PROJECT.md` 两处（读序两态 + R5 指针已接线）。路线图未演进。北极星=R5 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R6/R7/R8（v2.0.0 切版在 R8）待后续指令。
- 2026-07-07：**R7 收口**（ITER-0033，监督态自驱，P5 独立复核初判 REQUEST-CHANGES→修 2 Must Fix→AC1–9 全过）。说人话三条硬标准落定——`artifact-style §2` 就地改写为「说人话三条硬标准」（术语先解释 / 比喻要落地[全新·pre-R7 grep 零命中] / 别让英文·变量裸奔），显式声明**跨对话与文档通则 + 单一真源**；`artifact-style` scope 从"四件套字段正文"扩到"所有面向人落地文档"（frontmatter + §1）+ §8 自检扩为"发长文前自检"+ §7 边界消歧（"不管对话层"收窄为"不管对话层呈现结构"+ 三条为显式跨层例外）；`presentation-protocol` 插新 §7 对话层引用节（只引 §2 不重述）+ 顺移 §8/§9 + 内部 § 引用校正；`rule-card` 两条 + `README` 两处同步。**P5 MF 修复**：MF1 VERIFY 重写为 R7；MF2 四件套 dogfood 自身命中的反面词（`BLUF`/`fresh-context 子 agent`/`dogfood`）逐条改。**核心对抗点全过**：单一来源真单一（完整定义只在 `artifact-style §2`、别处引用/压缩指针）、编号顺移后引用不碎、比喻确为新增。scope 守恒：改 4 规则/模板文件（artifact-style / presentation-protocol / rule-card / README）+ `.ai/` 台账与四件套 + `.ai/PROJECT.md` 前滚；未触 identity / delivery-summary 字段 / 四 schema 字段结构 / hook / VERSION / R2·R3·R5·R6 目标 / rename。收口前滚 `.ai/PROJECT.md` 说人话条 R7 待→已。路线图未演进。北极星=R7 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R8（butler 自身 dogfood + 切 v2.0.0）待用户指令。
- 2026-07-07：**开 R7**（ITER-0033，监督态自驱，用户点选 R7；MILE-0003 第三条线·说人话，收尾）。说人话三条硬标准 + 发长文前自检——把散在 `artifact-style §2/§4.3`、且锁死在四件套的"讲人话"收敛成三条有名字的硬标准（术语先解释 / 比喻要落地[新] / 别让英文·变量裸奔），**定义单源落 `artifact-style §2`（跨对话与文档的通则）** + `artifact-style` scope 从"四件套字段正文"扩到"所有面向人落地文档"（交付总结 / 知识文件夹 / handoff 等）+ §8 自检扩为"发长文前自检"；`presentation-protocol` 对话层**引用**同守（不重述定义、单一来源）+ 对话层发长文前自检；`rule-card` / `README` 同步。**关键设计=单一来源**（三条只写一次、承 R1 G1–G4 单源模式）+ **dogfood**（本迭代四件套自身须过三条）。R7 不碰 `identity` / `delivery-summary` 字段、不改四件套字段结构与 presentation-protocol 呈现结构语义、不做 R8、不切版、不动 hook、不碰 R2/R3/R5 目标。路线图未演进（仅绑号 + R7 转 active）。北极星=R7 单迭代。
- 2026-07-07：**R6 收口**（ITER-0032，监督态自驱，P5 独立复核初判 REQUEST-CHANGES→修 1 Must Fix→8/8 AC 过）。部署种子 + 文件夹化迁移配方规则层落定——`mcv-deployment §2` 全貌产物两态化 + 部署建**空** `.ai/project/` 种子（唯一"部署即建"的 `.ai/` 子目录例外、`00_INDEX` 不 stub·首收口前滚生）+ line 45 老项目升级指针指 R6 配方；`migration-schema §4` 补 `[split]` typed 标签（`PROJECT.md → .ai/project/` 首例 + 起始态校验 + 冲突即停）+ §6 形态文档化·实例 `v2.0.0.md` 留 R8 切版产；翻 `project-digest §9` header + R6 待→已（明注实例仍 R8）+ README 补空种子。**P5 MF-1 修复**：R6 新引入的空种子暂态（目录在、`00_INDEX` 未生）会诱导冷启动踩空——救回它的"键控入口文件"澄清原只落 mcv §2，未落冷启动读者实读的 `context-persistence §6`；修复补 `context-persistence §6` line 124 入口文件存在性守卫 + line 130 点名空种子，双向自洽。**边界校正透明记账**：此 touch context-persistence 是为 R6 自身新引入的空种子暂态补冷启动守卫（R5 没预见的第三态），不改 R5 两态第一读语义、非重开 R5。scope 守恒：改 5 规则文件（mcv/migration/context-persistence/project-digest/README），未产 `migrations/v2.0.0.md` 实例（R8 切版产）、未迁 butler 自身、未切版、未改 R3 折叠必做/第 6 不变量、未 rename、未动 hook。收口前滚 `.ai/PROJECT.md` R6 指针（待→已）。路线图未演进。北极星=R6 单迭代已达成、交还用户；MILE-0003 仍 active，剩 R7（说人话）/ R8（butler dogfood + 切 v2.0.0）待后续指令。
