# invariants（关键长期决策与不变量）

> 只放"跨迭代仍成立、动它就动全局"的硬决策，附一句"为什么"。一次性变更归 `ITERATIONS`、不进这里。

- **三层分层不混**：SOP Core / Domain / Business 职责不互窜。*为什么*：分层一乱，通用规则就会被某个栈 / 某桩业务污染，失去可复用性。
- **产物链不依赖对话记忆**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P5 VERIFY，每阶段只从上一阶段的**文件**读。*为什么*：换会话就断片，只有落盘产物能跨会话恢复。
- **迭代 / 里程碑双层**：迭代（ITER-NNNN）是固定需求的 P1–P5 闭环单元；里程碑（MILE-NNNN）是套在其上的版本范围单元，松耦合可选。台账 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 是号与状态的真源。
- **AC 是验收脊柱**：贯穿 P2→P4→P5；tasks（执行步骤 + task-state）只是执行侧的投影，不取代 AC。*为什么*：验收标准若被执行清单顶替，就会"做完了"却没人对着标准验。
- **模板单一来源（SSOT）**：强制约束只改 `templates/rule-card.md` 一处，`CLAUDE.md.template` 与 `AGENTS.md.template` 都用占位符注入、不手工双写。同理各规则的定义只放一处、别处只引用回指。
- **共同内核 + 宿主薄适配**：`Coder/`、`.ai/`、规则卡和共享判断算法属于共同内核；Claude Code 与 Codex 的入口、命令/skills、hook 配置只做协议适配，不复制规则正文。*为什么*：双写会让两个宿主的规则逐渐漂移。
- **文档有界、历史横向归档**：单份产物只装当前迭代的真相，历史靠 `iterations/ITER-NNNN/` 横向铺开，禁止在一份文件里纵向堆历史。
- **hook 机械门禁（部署项目侧）**：PreToolUse hook 拦跳阶段 / 未冻结 AC 写源码 / 越界写 / 双 active 迭代 / 台账非法状态值。*注*：butler 仓自身不跑自己的 hook（规则仓非部署项目），改由 prompt 级一致性自检兜底（见 `debt.md`）。
- **冷启动读序固定 + 第一读两态**：项目全貌产物 → `ITERATIONS.md`（变更流）→ handoff / task-state（断点）→ 代码。第一读**两态**（MILE-0003 R5 起）——采用 `.ai/project/` 的项目先读 `00_INDEX` + 按需主题（读地图→定向钻取，不 slurp），仍单文件的老项目读 `.ai/PROJECT.md`。**butler 自身现已是文件夹态**（本轮 R8 迁毕）。真源 `context-persistence.md §6`。
- **收口是原子仪式**：`iteration-schema §5.5` 五步——①归档四件套 + changelog 切片 ②交付 md+html ③翻台账 + 收编 01_CHANGELOG ④前滚项目全貌产物（**文件夹态按主题必做折叠** / 单文件态按需前滚）⑤收口自检；前三必做、缺一不可，末步强制跑一致性自检。
- **一致性自检 6 不变量**：冷启动读序末 + 收口末步各跑一遍——current↔状态一致 / 至多一个 active 迭代 / closed 有交付且文件在 / closed 有归档 / 里程碑路线项对账 / **知识文件夹漂移**（第 6 条，条件不变量：采用 `.ai/project/` 的项目适用、单文件项目 N/A；MILE-0003 R3 起）。**butler 自身现已进第 6 条适用范围**。
- **每迭代对象级变更流**：`01_CHANGELOG.md` 记本迭代 ADD/EDIT/DELETE（绑 AC、文件 + 章节级），收口归档 `iterations/ITER-NNNN/CHANGELOG.md`。Review / 自评的 Should Fix 归 `VERIFY_REPORT.md` 的 Remaining Risks，不入 changelog。
- **帮手名册（MILE-0003 R1/R4）**：butler 派出去的"帮手"= 一份中立定义资料、用时读、临时起干净子 agent 执行、**不下发到项目**；总述 `62_Extension_Agents/overview.md` 是名册 + 通用规矩 G1–G4（干净上下文 / 叫不起来如实说绝不假装做过 / 权限约定 / 定义用时读不下发）的唯一真源。折叠必做（收口步④定），唤帮手 opt-in 非强制（起不了子 agent 则主线自做并如实标注）。
- **冷启动全貌产物 = 知识文件夹（MILE-0003 R2 起）**：`project-digest-schema.md` 把全貌产物从"单文件薄索引"升级为 `.ai/project/` 知识文件夹（`00_INDEX` + 推荐主题集 + digest-and-point 密度 + 收口折叠 + overwrite 禁历史层）。哲学=越补越全的知识地图，最大风险=陈旧的完整比诚实的薄更毒，故生死系于强制 + 可验证的收口折叠。
- **输出说人话（MILE-0003 R7 起）**：面向人的输出（对话 + 落地文档）守说人话三条硬标准——术语先解释 / 比喻要落地 / 别让英文·变量裸奔；真源 `artifact-style.md §2`，对话层 `presentation-protocol.md §7` 引用不重述。
