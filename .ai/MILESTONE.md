# MILESTONE — MILE-0016 · Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器

> 方向性产物（非冻结、不走 ACK）。校准「面向 AI 的规则仓 + 唯一用户是设计者本人」这个组合下积累的过度设计：先退役零消费的机构，再补真实缺口，最后装上使用数据监视器，让 Butler 具备结构性淘汰能力。

## 5.1 范围评估

**In Scope（版本级）**

- 退役 `.ai/project/` 整个知识文件夹（capabilities / frontier / architecture / invariants / fold-state），连同 `knowledge-fold`、`drift-check` 两个帮手；解除迭代与里程碑收口仪式里对折叠的强制要求。
- 冷启动读序改为「`debt.md` + handoff + `ITERATIONS` / `MILESTONES` 双台账」，不再依赖任何面向人的项目全貌摘要；`context-persistence.md` 的知识文件夹漂移自检随之退役。
- 砍 `/butler:progress` 命令全链：命令目录、skill、规则真源、workflow registry 条目、`docs/workflows.md` 与 rule-card 引用。
- `/butler:loop` 降级：保留代码路径但撤掉 `upgrade-convergence-engine` 候办、命令不再演进；最终去留由本里程碑后段的使用数据决定。
- `/butler:preference` 断言实验：设计并执行「一次反哺是否真的影响 P2/P3 提案排序」的可复现实验；无影响则全套退役，有影响则修回路并写清触发条件。
- 重造需求录入为三层：闪念口 `.ai/INBOX.md` → 孵化区 `.ai/backlog/<slug>.md`（带规模字段 milestone / iteration / undecided）→ 执行。新命令 `/butler:inbox add | list | handle`。
- 退役旧 inbox 全链：`tools/inbox/`、SRC-NNNN 身份、双 SHA-256 认亲、scanner，以及 `origin/` 目录。
- 项目根整理三件：`.ai/milestone-backlog/` 改名 `.ai/backlog/`、`deliveries/` 迁入 `.ai/deliveries/`（扁平布局）、`origin/` 退役；全仓引用一次性更新。
- 新增 hook 拦截审计日志 `.ai/.hook-blocks.log`（追加式、进 gitignore、有限大小），让拦截摩擦事后可追根因。
- 新增仓根 meta 文件逃生舱：README / CHANGELOG / .gitignore / VERSION / LICENSE 等在无 active 迭代时也可直接写入，不再被 phase_gate 与 workspace-scope 拦。
- 新增 usage instrumentation：每个 CLI 入口记录最后调用时间戳（本地状态、进 gitignore、不进共享仓），配 `tools/usage-report/` 提供 `usage report --since 90d`，A/B/C/D 分档由数据自动生成。
- evidence 消费链降维：承认 `goal.py` 是唯一消费者，砍或收窄 `tools/verification-evidence/` 的归档逻辑。
- 产出 `migrations/v4.0.0.md` 完整迁移配方，覆盖全部移除、改名与迁移动作；本里程碑收口时聚合切版 v4.0.0（MAJOR）。

**Out of Scope（版本级）**

- **不重造项目全貌摘要**：`.ai/project/` 砍了就是砍了，本里程碑不设计任何替代品；`debt.md` + handoff + 双台账就是冷启动的全部依据。
- **不做兼容期软链**：`deliveries/` 迁移直接是破坏性变更，不走「先建软链、下个大版本再删」的两阶段。
- **不做隐式 inbox 扫描**：新三层严格靠用户主动 `add`；不扫 `origin/`、不扫对话历史。外部文档引用改走 `.ai/references/`。
- **不重写 evidence 消费方**：`goal.py` 仍是唯一消费者，不给 evidence 加人读摘要或看板。
- **不做 usage 反哺决策自动化**：报告只呈现数据，是否淘汰仍由用户手工判断，不做自动降级或自动砍。
- **不重构 preference 数据回路**：断言实验若结论是反哺无效就整套退役，不走「先大改再验」。
- **不动 MILE-0014 / MILE-0015 已交付的骨架**：Decision Map / Decision Work / Decision Promotion 与领域合同工具全部保留，形态迭代留给未来里程碑。
- **不做根 layout 整理之外的 `.ai/` 结构大改**：`.ai/deliveries/` 沿用现在的扁平布局，不新分迭代子目录。

**关键交付目标**

- 冷启动读序不再涉及 `.ai/project/`；capabilities / frontier / architecture / invariants 从仓库消失，且收口仪式不再要求折叠。
- `/butler:progress` 从命令目录、registry、`docs/workflows.md`、rule-card 全部消失，相关 skill 与真源退役。
- 闪念 → 孵化 → 执行三层能跑通一次真实 dogfood：用 `/butler:inbox add` 记一条闪念，`handle` 分流到 ideation 或直接进 backlog，最后从 backlog 走里程碑或迭代启动。
- 项目根不再有 `deliveries/` 与 `origin/`，`.ai/backlog/` 取代 `.ai/milestone-backlog/`，全仓无残留旧引用。
- `.ai/.hook-blocks.log` 能追溯拦截历史；仓根 meta 文件在无 active 迭代时可直接写。
- `usage report --since 90d` 输出全部命令、帮手、工具的最后调用时间，淘汰判断第一次有确定性数据可依。
- preference 断言实验有明确结论并落到 `debt.md` 或直接退役。
- v4.0.0 切版发布，本轮 audit 识别的欠债一次清账，`debt.md` 只剩长期挂账。

## 5.2 理解阐释

Butler 走到 v3.6.0，规则文件 30 多份、驻留工具 20 多个、命令 10 多条、帮手 4 个、支持三个宿主。规模上已经到了个人规则仓的极致，但增长机制一直是只加不减：每次审计都能发现有能力躺着不用、有折叠在自转、有工具在生成没人看的产出。根因是缺淘汰机制——没有使用数据就没有淘汰依据，没有淘汰依据 backlog 就只能靠「应该做」的直觉长，功能只增不减，认知负担线性爬升。

最刺眼的一条是 `.ai/project/` 知识文件夹。它的设计目标是让下次冷启动的 AI 快速理解项目形态，同时人可读可校准。真实情况是 AI 自己写、AI 自己校（如果校）、AI 自己读，人在旁边观赏。实盘上已经出过事：MILE-0014 早被评估为「概念空缺真实、当前设计不符合预期」，但 `capabilities.md` 一直挂着「已交付 R1-R5」，这个失真三周没人发现。被问到过去半年有没有哪次决策是因为读了它才做出或改变，答案是举不出。

本里程碑的动作分三类。**先破**——退役已确认零消费、零校准的机构（知识文件夹、两个折叠帮手、progress 命令、旧 inbox 全链、`origin/`），顺带把项目根和 `.ai/` 的布局一次理顺。**再立**——补上审计里识别出的真实缺口：3 秒记一句话的闪念口、hook 拦截的审计追溯、仓根 meta 文件的逃生舱。这些是真需求过去没被识别，不是再加一层规则。**最后装监视器**——加使用数据采集，让下一次以及以后每一次审计都有确定性数据可查，Butler 从此具备结构性淘汰能力。

有两处判断要写清楚。一是 MILE-0014 / MILE-0015 交付的骨架保留：Decision Map 那套概念上确实填了探索期结构化决策的空缺，只是当前设计要在未来迭代形态，本里程碑不动它们。二是 preference 的处置以断言实验结论为准，不提前判死；实验必须设计成可检验、可复现，确认反哺无效再退役。

系统影响面预计涉及冷启动读序与两份入口模板、迭代与里程碑的收口仪式、命令目录与 workflow registry、hook 门禁、`.ai/` 与项目根布局、升级器迁移配方，以及 Butler 自身的 dogfood 状态。这是一次破坏性版本：知识文件夹消失、progress 命令消失、两个帮手消失、`.ai/milestone-backlog/` 改名、`deliveries/` 迁位、`origin/` 消失、旧 inbox scanner 消失，全部要在 `migrations/v4.0.0.md` 里给已部署项目留完整迁移路径，且不留兼容期软链。

## 5.3 拆分路线图

预计跨度：13 个迭代承接，分止血、重造、治根三段推进。三段严格串行——止血决定冷启动读序，重造的新 inbox 与根布局依赖新读序，治根的使用数据才能验证前两段到底砍对没有。实际迭代号在各路线项开启时绑定，本文件不预占。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 止血·退役知识文件夹：删 `.ai/project/`、退役 `knowledge-fold` 与 `drift-check` 帮手、解除迭代与里程碑收口仪式对折叠的强制 | — | planned |
| R2 | 止血·冷启动读序改造：改为 `debt.md` + handoff + 双台账，同步两份入口模板、rule-card 与 `context-persistence.md` 的漂移自检 | — | planned |
| R3 | 止血·砍 `/butler:progress` 全链：命令、skill、规则真源、registry 条目、`docs/workflows.md` 与 rule-card 引用 | — | planned |
| R4 | 止血·`/butler:loop` 降级与候办清理：撤 `upgrade-convergence-engine` 候办、冻结命令演进、登记待定处置 | — | planned |
| R5 | 重造·inbox 三层数据契约与真源：闪念口、孵化区规模字段、执行分流的结构与状态定义 | — | planned |
| R6 | 重造·`/butler:inbox add \| list \| handle` 命令与工具实现，含真实 dogfood 跑通一条闪念到执行 | — | planned |
| R7 | 重造·退役旧 inbox 全链：`tools/inbox/`、SRC-NNNN、双 SHA-256 认亲、scanner 与 `origin/` 目录 | — | planned |
| R8 | 重造·根布局整理：`.ai/milestone-backlog/` 改名 `.ai/backlog/`、`deliveries/` 迁入 `.ai/deliveries/`、全仓引用一次性更新 | — | planned |
| R9 | 重造·hook 拦截审计日志与仓根 meta 逃生舱：`.ai/.hook-blocks.log` 落地 + 白名单文件免 phase_gate 与 workspace-scope | — | planned |
| R10 | 治根·usage instrumentation：全 CLI 入口记录最后调用时间戳，本地状态不进共享仓 | — | planned |
| R11 | 治根·`tools/usage-report/` 与 `usage report --since 90d`：A/B/C/D 分档由数据生成，替代手工回忆 | — | planned |
| R12 | 治根·preference 反哺断言实验与处置，evidence 消费链降维，`/butler:loop` 依数据最终处置 | — | planned |
| R13 | 治根·`migrations/v4.0.0.md` 完整配方与已部署项目升级回归，audit 欠债清账，`debt.md` 收尾 | — | planned |

v4.0.0 的聚合切版本身走里程碑收口仪式（`milestone-schema.md §7.4` + `versioning-schema.md §6.3`），不单独占路线项。

## 5.4 范围演进记录

- 2026-08-17：由 `/grill-me` 深度审计收敛入候办。依据是对 34 项命令、帮手、工具的 A/B/C/D 使用度标注、三轮针对性追问，以及「过去半年是否因读知识文件夹做过决策」答不出来这一条。同轮定下 `deliveries/` 迁 `.ai/deliveries/`、不留兼容期软链、`.ai/deliveries/` 扁平布局三项边界决策。当时 MILE-0015 仍 active，按单 active 约束先入待办。
- 2026-08-18：MILE-0015 收口并发布 v3.6.0 后，用户确认开工，候办 `butler-slim-down` 提升为正式 MILE-0016。同时按 `milestone-schema.md §5.3`「路线项扁平原子、一项约等于一迭代、不设子项」把草稿里的 3 个大路线项拍平为 13 个平级路线项，内容不变，只是把原先写在段落里的「每个 R 内含 4–5 个迭代」展开成独立行。
- 2026-08-18：补记一项 R1 必须处理的连带改动——迭代收口仪式第四步与里程碑收口仪式第四步当前把知识文件夹折叠写成必做，退役 `.ai/project/` 必须同批解除这两处强制，否则收口规则会指向不存在的目录。
