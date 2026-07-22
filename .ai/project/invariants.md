# invariants（关键长期决策与不变量）

> 只放"跨迭代仍成立、动它就动全局"的硬决策，附一句"为什么"。一次性变更归 `ITERATIONS`、不进这里。

- **三层分层不混**：SOP Core / Domain / Business 职责不互窜。*为什么*：分层一乱，通用规则就会被某个栈 / 某桩业务污染，失去可复用性。
- **产物链不依赖对话记忆**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P5 VERIFY，每阶段只从上一阶段的**文件**读。*为什么*：换会话就断片，只有落盘产物能跨会话恢复。
- **迭代 / 里程碑双层**：迭代（ITER-NNNN）是固定需求的 P1–P5 闭环单元；里程碑（MILE-NNNN）是套在其上的版本范围单元，松耦合可选。台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 是号与状态的真源。
- **里程碑开工才领号，候办一方向一文件**：只讨论或暂缓的多个可独立启动方向先拆成平级候办块，每块以稳定候办键连接 `.ai/MILESTONES.md` 一行索引和 `.ai/milestone-backlog/` 一份草稿；正式开工才按最大已用号 +1 提升。只有最新且零迭代、零归档、零交付的误开项可退回，任何历史引用存在时编号永久保留。*为什么*：编号应表达真实开工顺序，候办边界应能独立推进，同时不能为整理队列改写历史身份。
- **AC 是验收脊柱**：贯穿 P2→P4→P5；tasks（执行步骤 + task-state）只是执行侧的投影，不取代 AC。*为什么*：验收标准若被执行清单顶替，就会"做完了"却没人对着标准验。
- **Goal 是派生视图，不是第二台账**：objective/scope/AC/plan/progress/proof/verdict 各守既有真源；tasks done 最多进入 `completion-candidate`，只有证据、审查和收口事实闭合才能派生 complete。宿主 Goal/Task 只投影 `.ai/`，冲突时项目真相优先。*为什么*：再建 GOAL 文件会复制阶段事实并产生新的漂移源。
- **P3 方案必须显式准入**：TECH_PLAN 自身保存 `draft / pass / revise / blocked` 单一 verdict，并用 Plan Admission 反证 AC 覆盖、假设、替代/取舍、失败路径、影响面和验证盲区；只有 `pass` 可进入 P4，实质改方案必须退 `draft` 重审。*为什么*：文件存在或任务全勾不能证明方案获准，独立审批台账又会双写漂移。
- **运行时坏消息必须回流**：六类 calibration signal 只在 task-state 做活跃投影，事实仍守既有阶段真源；按事实性质回 P1–P5 或诚实停，open/blocked 不得被任务进度或风险备注覆盖。*为什么*：发现方案/验收已错却沿旧计划做完，是 Goal 假完成的核心路径；另建 issue 台账又会漂移。
- **完成资格由只读裁决器聚合**：active iteration 只有在 AC、plan、calibration、evidence、review、blocker 与台账全部一致时才 eligible；host/tasks 不作绿依据，eligible 不等于 complete。*为什么*：任何单一信号都可能制造假完成，程序必须 fail-closed 汇总事实。
- **宿主 Goal/Task 只单向薄投影**：两端只显示 objective/state/reason/next，方向 project→host；能力缺失就 `.ai/` 降级，host complete 永不反写。*为什么*：宿主能力可变且会话态可丢，项目真相必须跨宿主稳定。
- **模板单一来源（SSOT）**：强制约束只改 `templates/rule-card.md` 一处，`CLAUDE.md.template` 与 `AGENTS.md.template` 都用占位符注入、不手工双写。同理各规则的定义只放一处、别处只引用回指。
- **共同内核 + 宿主薄适配**：`Coder/`、`.ai/`、规则卡和共享判断算法属于共同内核；Claude Code 与 Codex 的入口、命令/skills、hook 配置只做协议适配，不复制规则正文。*为什么*：双写会让两个宿主的规则逐渐漂移。
- **Codex skill 单一实体源**：10 个 skill 的实体只在 `plugins/butler/skills/`；`.agents/skills/` 必须保持相对软链，不能复制 SKILL.md。*为什么*：repo discovery 与 plugin 分发若各存一份会漂移。
- **工作流元数据单一注册源**：十工作流的宿主名称/路径、风险/隐式策略、触发/旧名和分发声明只在 `workflows/registry.json` 维护；`docs/workflows.md` 与入口元数据是生成投影。loop/dangerous 永远显式调用，旧名不得生成碰撞实体。*为什么*：人工同步多宿主和多文档会漂移，尤其可能无声降低高风险门槛。
- **双入口共同渲染**：目标项目 CLAUDE.md/AGENTS.md 必须由 `render-project-entrypoints.py` 从两模板 + 单一 rule-card 同步产生；管理区外原文、两份 user-managed 区各自保留，marker 异常 fail-closed。*为什么*：手工分别更新会漂移或覆盖用户内容。
- **项目根先于任何台账写入**：会话 cwd 只是发现起点，用户点名路径优先；否则只接受最近已部署 Butler 根或 Git 根。无法唯一证明时不创建 `.ai/`、不扫子目录猜测。*为什么*：多仓聚合目录是会话容器，不是其中每个项目的共享台账根。
- **全局用户配置先验安全**：安装器必须先完整校验 marker、有效 export 与命令软链所有权，再逐对象同目录暂存并原子替换；证据不足时 fail-closed，跨组件部分成功必须如实回声。*为什么*：全局配置属于用户资产，幂等便利不能凌驾于不丢数据和不误接管。
- **文档有界、历史横向归档**：单份产物只装当前迭代的真相，历史靠 `iterations/ITER-NNNN/` 横向铺开，禁止在一份文件里纵向堆历史。
- **PRD 是需求集合，不是项目唯一文档**：项目级 `prd/00_INDEX.md` 只登记独立需求；每份需求以首次进入本项目的日期化 `prd_id` 占一个目录，自己维护模块和版本历史。首切必须先过 new/new-version/duplicate/ambiguous 四态，日期有证据，身份/模块/Workspace Scope 一次对齐；status 以总索引发现并交叉核验目录与 active workspace map，只读零缓存。AC 用 `prd_refs` 逐需求钉 `prd_id + version + modules`，legacy 单值只读兼容；旧结构只能由显式身份驱动事务迁移，closed 历史靠 receipt/resolver 解析、绝不回写。改版必须指定 `prd_id` 和已确认 spec，先做零写 plan，再在整 collection 事务中 archive-first、更新 live/index/receipt；所有影响都有处置，verify/rollback 受 pre/post/archive/backup hash 约束。*为什么*：否则第二份需求会与第一份混装版本/模块，改版也无法确定在改谁；目录扫描、猜日期或半事务写入会制造幽灵真源与不可恢复中间态，为搬目录或追新版改历史会让冻结失去意义。
- **需求用稳定工作区键限制代码范围**：`.ai/project/workspaces.md` 保存当前 key→path 和共享/生成路径唯一 owner，PRD 只保存 primary/supporting/read-only/excluded 键集合，模块只能收窄；TECH_PLAN 再列本迭代写路径。允许写入必须同时满足 owner 唯一、钉版 PRD 可写、Write Plan 命中；PreToolUse 逐目标拒绝，shell 由 P5 diff 对账。目录移动只改地图，越界先扩 PRD Scope、重冻 AC、重审 P3。*为什么*：路径会变，历史不能跟着重写；没有默认拒绝和计划交集，monorepo 范围会悄悄膨胀成全仓。
- **收件箱只记回执，origin 永远用户自管**：来源用稳定 `SRC-NNNN`，内容用 observed/processed 双 SHA-256，派生走独立多对多表；确定性 scanner 只管来源事实，AI 分类必须经 standard 确认或 dangerous 自审，真正派生委托既有规则；`.ai/INBOX.md` 不复制原文，AI 不改、不移动、不归档 `origin/`。*为什么*：hash 不是来源身份，语义判断也不能冒充机械事实，处理便利更不能侵犯用户原稿所有权。
- **hook 管项目流程，宿主管文件权限**：PreToolUse 对能归属 Butler/Git 项目的目标拦跳阶段 / 未冻结 AC / 显式非 pass / 业务扩展保护 / 双 active / 台账非法状态；真实项目外路径退出 Butler 判定，坏输入仍 fail-closed，多项目 patch 逐根 first-deny-wins。Claude/Codex 共用规则模块。*为什么*：hook 看不到可信的用户授权，不能复制宿主权限系统；正常跨目录写入也不该伪装成 bypass。
- **冷启动读序固定 + 第一读两态**：项目全貌产物 → `ITERATIONS.md`（变更流）→ handoff / task-state（断点）→ 代码。第一读**两态**（MILE-0003 R5 起）——采用 `.ai/project/` 的项目先读 `00_INDEX` + 按需主题（读地图→定向钻取，不 slurp），仍单文件的老项目读 `.ai/PROJECT.md`。**butler 自身现已是文件夹态**（本轮 R8 迁毕）。真源 `context-persistence.md §6`。
- **自动道无证据不打绿**：完整路径的自动验证先由 `tools/verification-evidence/` 生成真实 argv/exit/log/hash record，VERIFY 按 AC 引用；失败记录保留为纠错轨迹，只有 passed record 能覆盖绿 AC。*为什么*：对话或 Markdown 中手写“已通过”仍只是模型自述。
- **本地/CI 单入口且验证依赖固定**：完整矩阵只由 `scripts/verify-ci.sh` 进入，workflow 不复制命令；Python/uv lock、Actions 完整 SHA 与 OpenAI Codex validator commit/hash/license 都必须显式固定，缺失或漂移 fail-closed。workflow 提供 check 不等于远端 required 已启用。*为什么*：否则同一提交会因时间、HOME 或操作者不同得到不同覆盖，还可能把未配置的远端保护口头打绿。
- **升级以机器 manifest + 程序为真源**：`migrations/manifest.json` 决定连续版本/action 链，`tools/butler-upgrade/upgrade.py` 决定计划与事务；Markdown recipe 只给人读。项目动作、split 决策、HOME 安装分域，默认先零写入 plan，冲突首写前停、失败只恢复本次触及文件。*为什么*：模型解释散文不可复现，把外部动作塞进项目事务会产生覆盖与假成功。
- **收口是原子仪式**：`iteration-schema §5.5` 五步——①校验并整包归档 evidence，再归档四件套 + changelog 切片 ②交付 md+html ③翻台账 + 收编 01_CHANGELOG ④前滚项目全貌并写 fold receipt（**文件夹态按主题必做折叠** / 单文件态按需前滚）⑤先跑 state auditor 再查语义漂移；前三必做、缺一不可。
- **一致性自检 6 不变量**：冷启动读序末 + 收口末步各跑一遍——current↔状态一致 / 至多一个 active 迭代 / closed 有交付且文件在 / closed 有归档 / 里程碑路线项对账 / **知识文件夹漂移**（第 6 条，条件不变量：采用 `.ai/project/` 的项目适用、单文件项目 N/A；MILE-0003 R3 起）。**butler 自身现已进第 6 条适用范围**。
- **每迭代对象级变更流**：`01_CHANGELOG.md` 记本迭代 ADD/EDIT/DELETE（绑 AC、文件 + 章节级），收口归档 `iterations/ITER-NNNN/CHANGELOG.md`。Review / 自评的 Should Fix 归 `VERIFY_REPORT.md` 的 Remaining Risks，不入 changelog。
- **帮手名册（MILE-0003 R1/R4）**：butler 派出去的"帮手"= 一份中立定义资料、用时读、临时起干净子 agent 执行、**不下发到项目**；总述 `62_Extension_Agents/overview.md` 是名册 + 通用规矩 G1–G4（干净上下文 / 叫不起来如实说绝不假装做过 / 权限约定 / 定义用时读不下发）的唯一真源。折叠必做（收口步④定），唤帮手 opt-in 非强制（起不了子 agent 则主线自做并如实标注）。
- **冷启动全貌产物 = 知识文件夹（MILE-0003 R2 起）**：`project-digest-schema.md` 把全貌产物从"单文件薄索引"升级为 `.ai/project/` 知识文件夹（`00_INDEX` + 推荐主题集 + digest-and-point 密度 + 收口折叠 + overwrite 禁历史层）。哲学=越补越全的知识地图，最大风险=陈旧的完整比诚实的薄更毒，故生死系于强制 + 可验证的收口折叠。
- **输出说人话（MILE-0003 R7 起）**：面向人的输出（对话 + 落地文档）守说人话三条硬标准——术语先解释 / 比喻要落地 / 别让英文·变量裸奔；真源 `artifact-style.md §2`，对话层 `presentation-protocol.md §7` 引用不重述。
