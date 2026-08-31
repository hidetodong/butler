# invariants（关键长期决策与不变量）

> 只放「跨迭代仍成立、动它就动全局」的硬决策，附一句「为什么」。一次性变更归 `ITERATIONS`、不进这里。

**写作纪律**（ITER-0114 起，违反即视为把这份文件变回会烂的那类）：

1. **只写决策与理由，不复述机制的具体形状**——步数、清单、顺序都归真源。复述了形状，机制一改这条就假；实测第 42、47 两条就是这么假掉的。
2. **每条至少带一个反引号真源指针**，让读者能当场核对。
3. **还成立才留，作废即删**，不留历史（历史归 `ITERATIONS` 与 `deliveries`）。

无真源指针的历史条目当前 16 条，由 `scripts/sync-project-overview.py --check` 卡住不许再增。**16 是欠账不是允许额度**，见 `.ai/debt.md`。

- **handoff 是可验鲜派生视图**：重要决定先落权威状态，`.ai/02_SESSION_HANDOFF.md` 只由工具生成；receipt 存在时冷启动先 `check`，陈旧先重建。*为什么*：人工 handoff 会漏写，也会在状态变化后继续冒充真相。
- **主链转换只做最小保真翻译**：PRD→AC→TECH_PLAN→Evidence→Goal→Handoff 每段都必须声明输入、输出、保真、失效、责任方、权威关系和直接真源；只读相关块并首批展开至多 3 份真源，证据不足可续批。权威事实、受控投影、派生视图、叙述摘要只能沿声明方向流动，修复回唯一真源。*为什么*：跨上下文不能靠会话记忆粘合，也不能为完整感复制各 schema 或让摘要反写真相。
- **旁路回执由用户显式回钩，不是模型审批或写入授权**：旁路执行者只在 `.ai/sidework/` 留最终结论与成果指针，用户给出路径后主 Agent 才定向续接；不自动扫描、不改主线权威状态，也不借回执绕过宿主/Butler 范围。*为什么*：用户主动发起的工作不需要模型替他接受或拒绝，而另一条执行线也不能污染主线断点与权限边界。
- **双台账热冷分层**：根 ITERATIONS/MILESTONES 只承载 current、近期热行与待办；有界 state index 保存固定区间路由公式，每个冷片以同名 receipt 自校验。AI 默认只定向读一片，机器审计必须跨热冷。*为什么*：冷启动成本和根导航都不能随历史线性增长，但历史追溯不能丢。
- **ITER/MILE 是自然增长数字身份**：至少四位、永不重编号，比较与分配只取数字部分。*为什么*：字符串排序在 9999→10000 边界不可靠。
- **五件套结构由机器合同固定**：新 live CONCEPT/AC/TECH/VERIFY/CHANGELOG 的段落、顺序、状态字段和表头以 artifact manifest 为准；条件段 N/A 不删除，legacy 归档不追改。*为什么*：容器若靠模型临场解释，就会逐轮产生细微但不可解析的漂移。
- **项目机器配置采用严格扁平 JSON**：`.ai/butler.config.json` schema v1 只含版本、三个布尔开关与 profiles；存在即必须完整合法，未知字段/版本 fail-closed。所有消费端统一经 `resolve` 读取，持久修改只经 JSON `set` 写入；兼容期只在 JSON 缺失时严格回退旧 Markdown，迁移由 upgrader 单事务创建 JSON 并移除机器段，禁止长期双写。自然语言约束、运行状态和外置偏好数据不进入该文件。*为什么*：机器开关不能继续依赖模型解析 Markdown，同时第一版字段很少，不值得提前建设嵌套总配置中心。
- **领域知识渐进加载，导航不做第二真源**：普通冷启动只读 `Coder/README.md` 的 L0 路由；跨上下文任务再读 `domain-model.md` L1，术语歧义定向查询 `domain-glossary.md` L2，历史审计才进入归档 L3。首批最多展开 3 份直接真源；不足时必须给出已读、缺口、下一批及理由的可见回执后续批。字段、封闭枚举和算法仍由所指 schema / manifest / registry / 规则正文拥有。L0 内核以 `Coder/README.md` 为唯一真源，字节投影到 `AGENTS.md` 与 `templates/rule-card.md`，三处必须严格相等并由 `tools/context-budget/` 校验；改 L0 就必须重新生成已部署项目的入口。*为什么*：把完整审计常驻或递归展开指针会吞噬初始上下文，复制执行合同会制造双写漂移，而两个宿主入口若各写一份 L0，分层纪律就只在其中一处成立。
- **Dangerous 与 Loop 并列，人测段结构单一所有者**：Dangerous Mode 与 Convergence Loop 是并列模式，各自显式触发、互不读写激活状态，只共用 `30_Quality_Gate/bounded-convergence.md` 的有界收敛纪律；VERIFY「人测道小结」结构只归 artifact manifest + canonical template 拥有，verify-schema 只解释触发/回填，delivery-selftest README 继续独占四态机器码与桥 JSON。机器合同 `tools/domain-contract/` 以负例防复制型合同与旧包含措辞回潮，并要求每条登记条目至少被一条断言或关系锚住——登记了却没有回归能抓即视为失败。领域概念、上下文关系或状态转换发生变更时，评审必须声明唯一所有者、兼容影响、迁移路径和负向样例，缺一条按 Must Fix 处理。*为什么*：模式包含会混淆「全生命周期无人值守」与「P4 高强度纠错」，结构双写会制造「写了判错、不写违规」的死锁。

- **三层分层不混**：SOP Core / Domain / Business 职责不互窜。*为什么*：分层一乱，通用规则就会被某个栈 / 某桩业务污染，失去可复用性。
- **产物链不依赖对话记忆**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P5 VERIFY，每阶段只从上一阶段的**文件**读。*为什么*：换会话就断片，只有落盘产物能跨会话恢复。
- **迭代 / 里程碑双层**：迭代（ITER-NNNN）是固定需求的 P1–P5 闭环单元；里程碑（MILE-NNNN）是套在其上的版本范围单元，松耦合可选。台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 是号与状态的真源。
- **里程碑开工才领号，候办一方向一文件**：只讨论或暂缓的多个可独立启动方向先拆成平级候办块，每块以稳定候办键连接 `.ai/MILESTONES.md` 一行索引和 `.ai/milestone-backlog/` 一份草稿；正式开工才按最大已用号 +1 提升。只有最新且零迭代、零归档、零交付的误开项可退回，任何历史引用存在时编号永久保留。*为什么*：编号应表达真实开工顺序，候办边界应能独立推进，同时不能为整理队列改写历史身份。
- **AC 是验收脊柱**：贯穿 P2→P4→P5；tasks（执行步骤 + task-state）只是执行侧的投影，不取代 AC。*为什么*：验收标准若被执行清单顶替，就会"做完了"却没人对着标准验。
- **Goal 是派生视图，不是第二台账**：objective/scope/AC/plan/progress/proof/verdict 各守既有真源；tasks done 最多进入 `completion-candidate`，只有证据、审查和收口事实闭合才能派生 complete。宿主 Goal/Task 只投影 `.ai/`，冲突时项目真相优先。*为什么*：再建 GOAL 文件会复制阶段事实并产生新的漂移源。
- **P3 方案必须显式准入**：TECH_PLAN 自身保存 `draft / pass / revise / blocked` 单一 verdict，并用 Plan Admission 反证 AC 覆盖、假设、替代/取舍、失败路径、影响面和验证盲区；只有 `pass` 可进入 P4，实质改方案必须退 `draft` 重审。*为什么*：文件存在或任务全勾不能证明方案获准，独立审批台账又会双写漂移。
- **运行时坏消息必须回流**：六类 calibration signal 只在 task-state 做活跃投影，事实仍守既有阶段真源；按事实性质回 P1–P5 或诚实停，open/blocked 不得被任务进度或风险备注覆盖。*为什么*：发现方案/验收已错却沿旧计划做完，是 Goal 假完成的核心路径；另建 issue 台账又会漂移。
- **完成资格由只读裁决器聚合**：active iteration 只有在 AC、plan、calibration、evidence、已声明 TDD 配对、review、blocker 与台账全部一致时才 eligible；host/tasks 不作绿依据，eligible 不等于 complete。*为什么*：任何单一信号都可能制造假完成，程序必须 fail-closed 汇总事实。
- **宿主 Goal/Task 只单向薄投影**：两端只显示 objective/state/reason/next，方向 project→host；能力缺失就 `.ai/` 降级，host complete 永不反写。*为什么*：宿主能力可变且会话态可丢，项目真相必须跨宿主稳定。
- **模板单一来源（SSOT）**：强制约束只改 `templates/rule-card.md` 一处，`CLAUDE.md.template` 与 `AGENTS.md.template` 都用占位符注入、不手工双写。同理各规则的定义只放一处、别处只引用回指。
- **共同内核 + 宿主薄适配**：`Coder/`、`.ai/`、规则卡和共享判断算法属于共同内核；Claude Code 与 Codex 的入口、命令/skills、hook 配置只做协议适配，不复制规则正文。*为什么*：双写会让两个宿主的规则逐渐漂移。
- **Codex skill 单一实体源**：Router 与全部业务 skill（名单以 `workflows/registry.json` 为准）的实体只在 `plugins/butler/skills/`；`.agents/skills/` 必须保持相对软链，不能复制 SKILL.md。*为什么*：repo discovery 与 plugin 分发若各存一份会漂移。
- **工作流元数据单一注册源**：Router 元入口与全部业务工作流的宿主名称/路径、风险/隐式策略、触发/排除/冲突/前置和分发声明只在 `workflows/registry.json` 维护；`docs/workflows.md` 与入口元数据是生成投影。Router 不路由到自身，显式具体入口绕过 Router，loop/dangerous 永远显式调用。*为什么*：人工同步多宿主和多文档会漂移，尤其可能无声降低高风险或机器级写入门槛。
- **Router corpus 是合同下界，不是第二分类器**：机器检查可以锁定显式 trigger、代表 status 和零写边界，但任意自然语言含义仍由宿主模型按共同 Router 合同理解；不得为了让测试看似更确定而新增关键词分类引擎。*为什么*：有限词表既无法解决语义判断，又会与 Router 正文形成第二算法真源。
- **Explore opt-in 且只从 P1 交付**：用户主动探索或接受带具体 blocker 的零写建议才进入既有 Ideation；Decision Map 只拥有探索决策状态，显式 promotion 后降为参考并从 Iteration P1 接回，不直入 P2、不覆盖 Milestone 或冻结 AC。*为什么*：让模型自行判定清晰度/大小并静默建状态，会把整个确定性生命周期建立在脆弱入口上；新增 Explore workflow 又会制造第二真源。
- **Decision Map 状态由确定性 Module 独占**：每张 Map 只有 canonical `state.json` 可写，Frontier 只从依赖与状态派生；helper 不得绕过 `inspect / plan / apply / verify` 直接改 JSON，目录级全局索引也不得成为第二写真源。*为什么*：并行领取、幂等恢复和跨会话继续只有在所有转换共用同一校验与提交边界时才可信。
- **决策求证可并行，Map 吸收必须单写**：Decision Work 只发布不可变 Task/Result，只有显式选择并逐项 claim 的 Research 可多项 batch；helper 完成、record 或 absorbable 都不等于 resolved，协调器必须显式 absorb 且只经 Decision Map Module 提交。*为什么*：把求证吞吐与状态所有权拆开，才能获得并行收益而不把最终决策交给 helper 或模型置信度。
- **Decision Promotion 只做显式、可重放的交接**：调用方必须指定 resolved Decision roots 与 `route-reference` / `iteration-start`；前者只引用既有 planned 路线，后者只复用 iteration-intake 从 P1 开始。source/target digest、不可变 receipt 与 pending journal 共同 fail-closed，工具不得创建路线、自动选路或跳 P2。*为什么*：Decision Map 应是参考来源而非第二交付真源，交接边界也不能重新依赖模型对清晰度、大小或目标容器的临场判断。
- **双入口共同渲染**：目标项目 CLAUDE.md/AGENTS.md 必须由 `render-project-entrypoints.py` 从两模板 + 单一 rule-card 同步产生；管理区外原文、两份 user-managed 区各自保留，marker 异常 fail-closed。*为什么*：手工分别更新会漂移或覆盖用户内容。
- **项目根先于任何台账写入**：会话 cwd 只是发现起点，用户点名路径优先；否则只接受最近已部署 Butler 根或 Git 根。无法唯一证明时不创建 `.ai/`、不扫子目录猜测。*为什么*：多仓聚合目录是会话容器，不是其中每个项目的共享台账根。
- **全局用户配置先验安全**：安装器必须先完整校验 marker、有效 export 与命令软链所有权，再逐对象同目录暂存并原子替换；证据不足时 fail-closed，跨组件部分成功必须如实回声。*为什么*：全局配置属于用户资产，幂等便利不能凌驾于不丢数据和不误接管。
- **文档有界、历史横向归档**：单份产物只装当前迭代的真相，历史靠 `iterations/ITER-NNNN/` 横向铺开，禁止在一份文件里纵向堆历史。
- **PRD 是需求集合，不是项目唯一文档**：项目级 `prd/00_INDEX.md` 只登记独立需求；每份需求以首次进入本项目的日期化 `prd_id` 占一个目录，自己维护模块和版本历史。首切必须先过 new/new-version/duplicate/ambiguous 四态，日期有证据，身份/模块/Workspace Scope 一次对齐；status 以总索引发现并交叉核验目录与 active workspace map，只读零缓存。AC 用 `prd_refs` 逐需求钉 `prd_id + version + modules`，legacy 单值只读兼容；旧结构只能由显式身份驱动事务迁移，closed 历史靠 receipt/resolver 解析、绝不回写。改版必须指定 `prd_id` 和已确认 spec，先做零写 plan，再在整 collection 事务中 archive-first、更新 live/index/receipt；所有影响都有处置，verify/rollback 受 pre/post/archive/backup hash 约束。*为什么*：否则第二份需求会与第一份混装版本/模块，改版也无法确定在改谁；目录扫描、猜日期或半事务写入会制造幽灵真源与不可恢复中间态，为搬目录或追新版改历史会让冻结失去意义。
- **需求用稳定工作区键限制代码范围**：`.ai/project/workspaces.md` 保存当前 key→path 和共享/生成路径唯一 owner，PRD 只保存 primary/supporting/read-only/excluded 键集合，模块只能收窄；TECH_PLAN 再列本迭代写路径。允许写入必须同时满足 owner 唯一、钉版 PRD 可写、Write Plan 命中；PreToolUse 逐目标拒绝，shell 由 P5 diff 对账。目录移动只改地图，越界先扩 PRD Scope、重冻 AC、重审 P3。*为什么*：路径会变，历史不能跟着重写；没有默认拒绝和计划交集，monorepo 范围会悄悄膨胀成全仓。
- **录入分三层，闪念口只记去向，用户原稿永远用户自管**：需求从产生到开工过三层——闪念口 `.ai/INBOX.md`、孵化区 `.ai/milestone-backlog/`、执行分流；三层的结构、状态与合法转移只有一份真源 `Coder/40_Context_Management/intake-schema.md`，写盘者只有 `tools/intake/intake.py` 一家。闪念用 `YYYY-MM-DD-<kebab 短句>` 作键（不设递增号池、不做内容指纹认亲），状态是 `new` / `incubated` / `done` / `dropped` 四态封闭枚举。闪念口是转运站不是仓库——只记一句话摘要、状态与去向指针，不复制原文，真正的落地委托既有规则；`.ai/references/raw/` 里的材料归用户，AI 只读、不写不改不重命名不移动不归档不删除。*为什么*：复制原文就多出一份会跟原件分叉的真源；递增号池和内容认亲要有人维护「下一个号是几」和「这条是不是变过」，为一句随口记下的话建这套账本，正是 MILE-0016 在砍的那类过度设计；而处理便利不能侵犯用户原稿所有权。
- **hook 管项目流程，宿主管文件权限**：PreToolUse 对能归属 Butler/Git 项目的目标拦跳阶段 / 未冻结 AC / 显式非 pass / 业务扩展保护 / 双 active / 台账非法状态；真实项目外路径退出 Butler 判定，坏输入仍 fail-closed，多项目 patch 逐根 first-deny-wins。Claude/Codex 共用规则模块。*为什么*：hook 看不到可信的用户授权，不能复制宿主权限系统；正常跨目录写入也不该伪装成 bypass。
- **冷启动读序固定且只有一处真源**：步骤与顺序以 `Coder/40_Context_Management/context-persistence.md §6` 的读序块为准，其余载体只能是它的字节投影。*为什么*：读序固定才能保证任何会话从零接手都走同一条恢复路径，不靠对话记忆；而多处各写一份必然分叉——实测曾有五份不同版本共存，没有任何机器检查能发现。
- **自动道无证据不打绿**：完整路径的自动验证先由 `tools/verification-evidence/` 生成真实 argv/exit/log/hash record，VERIFY 按 AC 引用；失败记录保留为纠错轨迹，只有 passed record 能覆盖绿 AC。*为什么*：对话或 Markdown 中手写“已通过”仍只是模型自述。
- **显式 TDD 只复用 evidence v1 做最小配对**：TECH_PLAN 声明 cycle 后，固定 Red/Green ID 必须证明同一 argv/cwd/AC 先 failed、后 passed；未声明时零行为。不增 sidecar、第二台账，也不把这条轻量记录夸成代码时序或有效 Red 的完整证明。*为什么*：先验证最小纪律收益，避免在真实痛点出现前建设 baseline、adapter、哈希和 diff 审计平台。
- **本地/CI 单入口且验证依赖固定**：完整矩阵只由 `scripts/verify-ci.sh` 进入，workflow 不复制命令；Python/uv lock、Actions 完整 SHA 与 OpenAI Codex validator commit/hash/license 都必须显式固定，缺失或漂移 fail-closed。workflow 提供 check 不等于远端 required 已启用。*为什么*：否则同一提交会因时间、HOME 或操作者不同得到不同覆盖，还可能把未配置的远端保护口头打绿。
- **升级以机器 manifest + 程序为真源**：`migrations/manifest.json` 决定连续版本/action 链，`tools/butler-upgrade/upgrade.py` 决定计划与事务；Markdown recipe 只给人读。项目动作、split 决策、HOME 安装分域，默认先零写入 plan，冲突首写前停、失败只恢复本次触及文件。*为什么*：模型解释散文不可复现，把外部动作塞进项目事务会产生覆盖与假成功。
- **收口是原子仪式**：步骤、顺序与哪几步必做以 `Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5` 为准。*为什么*：收口若可以挑着做，台账、交付、证据与归档就会各自停在不同时点，冷启动再也拼不回一致的事实。
- **一致性自检 5 不变量**：冷启动读序末 + 收口末步各跑一遍——current↔状态一致 / 至多一个 active 迭代 / closed 有交付且文件在 / closed 有归档 / 里程碑路线项对账。*为什么*：这五条是台账↔产物↔交付↔证据的机器可判对账，漂移必须在动手前暴露、不留到冷启动才发现。*ITER-0112 修订*：原第 6 条「知识文件夹漂移」随该机制退役删除，由 6 条减为 5 条。
- **每迭代对象级变更流**：`01_CHANGELOG.md` 记本迭代 ADD/EDIT/DELETE（绑 AC、文件 + 章节级），收口归档 `iterations/ITER-NNNN/CHANGELOG.md`。Review / 自评的 Should Fix 归 `VERIFY_REPORT.md` 的 Remaining Risks，不入 changelog。
- **帮手是中立 worker 定义，不等于一律起子 agent**：总述 `62_Extension_Agents/overview.md` 是名册 + 通用规矩 G1–G4 的唯一真源；检查类必须 fresh-context，Decision Work 按 research/serial/HITL 合同执行并如实回传实际模式，定义本身不下发到项目。*为什么*：隔离要求应服务于角色，不能为统一术语伪造宿主能力或把真人问答后台化。
- **全貌产物不靠 delta 折叠维护（ITER-0112 起）**：知识文件夹（MILE-0003 R2–R8）已退役。*为什么*：折叠是 delta 驱动的，只维护得住追加式与整体覆写的内容，维护不住需要回头重评旧结论的内容——实测 `architecture.md` 的成熟度段落后 9 个里程碑、`capabilities.md` 旧节失真，而纯追加的本文件与整体覆写的 `frontier.md` 一直准确。「陈旧的完整比诚实的薄更毒」这条判断成立，错的是用强制折叠去防它。新全貌产物由 MILE-0016 R3 设计：可派生的部分从机器源头生成、手写只留理由与判断。
- **输出说人话（MILE-0003 R7 起）**：面向人的输出（对话 + 落地文档）守说人话三条硬标准——术语先解释 / 比喻要落地 / 别让英文·变量裸奔；真源 `artifact-style.md §2`，对话层 `presentation-protocol.md §7` 引用不重述。
