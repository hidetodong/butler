# MILESTONE — MILE-0016 · Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器

> 方向性产物（非冻结、不走 ACK）。校准「面向 AI 的规则仓 + 唯一用户是设计者本人」这个组合下积累的过度设计：先退役零消费的机构，再补真实缺口，最后装上使用数据监视器，让 Butler 具备结构性淘汰能力。

## 5.1 范围评估

**In Scope（版本级）**

- 退役 `.ai/project/` 知识文件夹里被证明维护不住的部分——抄真源的四份（`00_INDEX` / `identity` / `constraints` / `architecture` 的模块地图段）与靠原地重评的两块（`architecture` 成熟度段、`capabilities.md` 全文）；连同 `fold-state.json` 回执、`knowledge-fold` 与 `drift-check` 两个帮手一起删除，并解除迭代与里程碑收口仪式里对折叠的强制要求。
- 保留两份被证明有效的产物待迁：`invariants.md` 的 38 条 `*为什么*` 理由（纯追加、无漂移、别处无真源）与 `frontier.md`（每次收口整体覆写、一直准确）；落点由替代品设计决定，不在退役批次里删。
- 重建项目全貌产物：可从机器源头派生的部分改为生成（`workflows/registry.json` 的工作流元数据、`Coder/README.md` 的目录与职责、双台账的里程碑起止、`tools/` 目录清单），手写只留机器算不出来的理由与判断；产物不进折叠机制，避免重蹈原地重评必烂的覆辙。
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
- 扩展升级器的动作类型：现有九种标签里没有任何一种能表达「删目录」和「把仓根目录移进 `.ai/`」，需新增删除与移动两类 typed 标签，同步改 `migration-schema.md §4` 的标签集与 `upgrade.py` 的动作域、字段、前置三张表及路径校验，并各自满足幂等、起始态校验、冲突即停与可回滚。
- 产出 `migrations/v4.0.0.md` 完整迁移配方，覆盖全部移除、改名与迁移动作；本里程碑收口时聚合切版 v4.0.0（MAJOR）。

**Out of Scope（版本级）**

- **不把全貌产物重新接回折叠机制**：替代品的生成部分从机器源头算、手写部分只追加，`knowledge-fold` / `drift-check` / `fold-state.json` 这套写—折—校闭环不复活。
- **不为全貌产物做原地重评**：成熟度这类需要回头修改旧结论的内容，要么由数据派生（R11 的 usage 报告），要么整体覆写，不再靠「收口时补漏」这种没有强制触发的软约定。
- **不做兼容期软链**：`deliveries/` 迁移直接是破坏性变更，不走「先建软链、下个大版本再删」的两阶段。
- **不做隐式 inbox 扫描**：新三层严格靠用户主动 `add`；不扫 `origin/`、不扫对话历史。外部文档引用改走 `.ai/references/`。
- **不重写 evidence 消费方**：`goal.py` 仍是唯一消费者，不给 evidence 加人读摘要或看板。
- **不做 usage 反哺决策自动化**：报告只呈现数据，是否淘汰仍由用户手工判断，不做自动降级或自动砍。
- **不重构 preference 数据回路**：断言实验若结论是反哺无效就整套退役，不走「先大改再验」。
- **不动 MILE-0014 / MILE-0015 已交付的骨架**：Decision Map / Decision Work / Decision Promotion 与领域合同工具全部保留，形态迭代留给未来里程碑。
- **不做根 layout 整理之外的 `.ai/` 结构大改**：`.ai/deliveries/` 沿用现在的扁平布局，不新分迭代子目录。

**关键交付目标**

- 冷启动读序不再涉及 `.ai/project/`；抄真源的四份与靠原地重评的两块从仓库消失，`fold-state.json` 与两个折叠帮手退役，收口仪式不再要求折叠。
- 新全貌产物落地并跑通一次真实冷启动：生成部分能一条命令重算且与机器源头一致，手写部分只有追加操作，读完能回答「这系统整体是什么、为什么长成这样、哪块能动哪块不能动」。
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

预计跨度：15 个迭代承接，分止血（R1–R5）、重造（R6–R10）、治根（R11–R15）三段推进。三段严格串行——止血决定冷启动读序与读什么，重造的新 inbox 与根布局依赖新读序，治根的使用数据才能验证前两段到底砍对没有。实际迭代号在各路线项开启时绑定，本文件不预占。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 止血·退役折叠机制与漂移产物：删 `.ai/project/` 里抄真源的四份与靠原地重评的两块 + `fold-state.json`，退役 `knowledge-fold` 与 `drift-check` 帮手，解除两处收口仪式对折叠的强制；`invariants.md` 与 `frontier.md` 留待 R3 迁移 | ITER-0112 | closed |
| R2 | 止血·冷启动读序改造：改为 `debt.md` + handoff + 双台账，同步两份入口模板、rule-card 与 `context-persistence.md` 的漂移自检 | ITER-0113 | closed |
| R3 | 止血·项目全貌产物重建：生成部分从 `registry.json` / `Coder/README.md` / 双台账 / `tools/` 派生，手写部分承接 `invariants.md` 的 38 条理由与 `frontier.md` 的覆写模式，定落点与重算命令 | ITER-0114 | closed |
| R4 | 止血·砍 `/butler:progress` 全链：命令、skill、规则真源、registry 条目、`docs/workflows.md` 与 rule-card 引用 | ITER-0115 | closed |
| R5 | 止血·`/butler:loop` 降级与候办清理：撤 `upgrade-convergence-engine` 候办、冻结命令演进、登记待定处置 | ITER-0116 | closed |
| R6 | 重造·inbox 三层数据契约与真源：闪念口、孵化区规模字段、执行分流的结构与状态定义 | ITER-0117 | closed |
| R7 | 重造·`/butler:inbox add \| list \| handle` 命令与工具实现，含真实 dogfood 跑通一条闪念到执行 | ITER-0118 | closed |
| R8 | 重造·退役旧 inbox 全链：`tools/inbox/`、SRC-NNNN、双 SHA-256 认亲、scanner 与 `origin/` 目录 | ITER-0119 | closed |
| R9 | 重造·根布局整理：`.ai/milestone-backlog/` 改名 `.ai/backlog/`、`deliveries/` 迁入 `.ai/deliveries/`、全仓引用一次性更新 | — | planned |
| R10 | 重造·hook 拦截审计日志与仓根 meta 逃生舱：`.ai/.hook-blocks.log` 落地 + 白名单文件免 phase_gate 与 workspace-scope | — | planned |
| R11 | 治根·usage instrumentation：全 CLI 入口记录最后调用时间戳，本地状态不进共享仓 | — | planned |
| R12 | 治根·`tools/usage-report/` 与 `usage report --since 90d`：A/B/C/D 分档由数据生成，替代手工回忆 | — | planned |
| R13 | 治根·preference 反哺断言实验与处置，evidence 消费链降维，`/butler:loop` 依数据最终处置 | — | planned |
| R14 | 治根·升级器动作类型扩展：新增删除与移动两类 typed 标签，改 `migration-schema.md §4` 与 `upgrade.py` 三张表及路径校验，补幂等、冲突即停与回滚 | — | planned |
| R15 | 治根·`migrations/v4.0.0.md` 完整配方与已部署项目升级回归，audit 欠债清账，`debt.md` 收尾 | — | planned |

v4.0.0 的聚合切版本身走里程碑收口仪式（`milestone-schema.md §7.4` + `versioning-schema.md §6.3`），不单独占路线项。

## 5.4 范围演进记录

- 2026-08-17：由 `/grill-me` 深度审计收敛入候办。依据是对 34 项命令、帮手、工具的 A/B/C/D 使用度标注、三轮针对性追问，以及「过去半年是否因读知识文件夹做过决策」答不出来这一条。同轮定下 `deliveries/` 迁 `.ai/deliveries/`、不留兼容期软链、`.ai/deliveries/` 扁平布局三项边界决策。当时 MILE-0015 仍 active，按单 active 约束先入待办。
- 2026-08-18：MILE-0015 收口并发布 v3.6.0 后，用户确认开工，候办 `butler-slim-down` 提升为正式 MILE-0016。同时按 `milestone-schema.md §5.3`「路线项扁平原子、一项约等于一迭代、不设子项」把草稿里的 3 个大路线项拍平为 13 个平级路线项，内容不变，只是把原先写在段落里的「每个 R 内含 4–5 个迭代」展开成独立行。
- 2026-08-18：补记一项 R1 必须处理的连带改动——迭代收口仪式第四步与里程碑收口仪式第四步当前把知识文件夹折叠写成必做，退役 `.ai/project/` 必须同批解除这两处强制，否则收口规则会指向不存在的目录。
- 2026-08-18：整理路线项时查出升级器缺口——`upgrade.py` 现有九种 typed 标签（`rename` / `split` / `add_field` / `regen_entrypoints` / `regen_claude` / `global_install` / `sync_hooks` / `restamp` / `no_op`）没有一种能表达本里程碑的两类核心动作：删掉 `.ai/project/` 整个目录，以及把仓根的 `deliveries/` 移进 `.ai/`。后者还额外撞上 `rename` 的硬校验——该标签要求源和目标路径第一段都是 `.ai/`，仓根来源直接被拒。故新增独立路线项 R13 承接标签扩展，原 R13 顺延为 R14；路线项总数由 13 增至 14。
- 2026-08-18：修正 R8 的影响面估计。`deliveries/` 迁位不只是改路径字符串：全仓有 46 份规则、脚本、工具与文档提到该目录，`CHANGELOG.md` 里有 71 处引用，`milestone-schema.md §9` 整节在画它的目录树，另有 3 份里程碑交付用 `../ITER-NNNN-*.md` 相对链接指向上级目录、目录一动即失效。R8 的回归预算按此重新估。
- 2026-08-18：切定 R1 与 R2 的边界。路线图字面上把「删文件夹」放 R1、「改冷启动读序」放 R2，但删完文件后 `context-persistence.md §6` 的第一读仍指着 `.ai/project/00_INDEX.md`，迭代必须收口在自洽状态、不能留一整轮的断指针。故 R1 除删除动作外，还包含把因删除而失效的指针改到自洽（只去指针、不定义新读序）；R2 保留新读序的正面定义与两份入口模板改造。R1 实际范围比路线图字面描述略宽，路线项表述不变。
- 2026-08-18：确认退役 `.ai/project/` 等于连单文件 `.ai/PROJECT.md` 的 legacy 形态一起停支持——`project-digest-schema.md` 一份 schema 同时拥有两种形态，退役它两态皆亡。牵连 `mcv-deployment.md §2` 的「部署即建空种子」（`.ai/project/` 是唯一部署即建的 `.ai/` 子目录例外）、`migration-schema.md §4` 的 `[split]` 标签，以及 `upgrade.py` 里 `--split defer|now` 这个 `apply` 的必填参数与 `project-knowledge-shape-valid` 前置。R1 只做去指针与登记，动作面归 R13（标签与动作域改造）与 R14（v4.0.0 配方给老项目一次性交代）。
- 2026-08-18：确定 `debt.md` 迁位而非删除。新冷启动读序把它放在第一顺位，但它现在就躺在待删目录里；落点定为 `.ai/debt.md`。同目录另外三份（`00_INDEX.md` / `identity.md` / `constraints.md`）经核为派生摘要，正文各自都标了真源，随文件夹一起删除。里程碑 In Scope 原只点名 5 个文件，实有 9 个，本条补齐其余 4 个的处置。
- 2026-08-18：修正「不设替代品」这条边界，并新增路线项 R3。原判断建立在「知识文件夹没用」之上，但复盘四份文件的实际状况后发现结论下错了地方：`architecture.md` 的成熟度段落后 9 个里程碑（只写到 MILE-0007）、`capabilities.md` 有覆盖但旧节内容失真，而 `invariants.md`（纯追加）与 `frontier.md`（每次收口整体覆写）一直准确。规律是**整体覆写和纯追加都活得下来，需要回头修改旧内容的必烂**——折叠是 delta 驱动的，没有任何动作会触发「回头重评旧结论」。所以失败的是机制与内容性质不匹配，不是全貌观察这个需求本身；Butler 自己的 `context-persistence.md` 第 136 行也早写着「缺全貌产物时新会话只能从一堆迭代 delta 倒推全貌（管中窥豹）」，现有 112 个迭代、123 份交付，倒推已不现实。故撤掉 Out of Scope 的「不重造任何替代品」，改为「不把全貌产物重新接回折叠机制」与「不为全貌产物做原地重评」两条；In Scope 增列重建条目，可派生部分改为从机器源头生成、手写只留理由与判断。
- 2026-08-18：路线项编号顺延。新 R3（项目全貌产物重建）插在冷启动读序改造之后——读序改完立刻要回答「那读什么」，隔太远会留一段全貌真空；生成所需的 `registry.json`、双台账与 `Coder/README.md` 都是现成的，usage 数据（现 R12）是后续增强而非前置。原 R3–R14 依次后移为 R4–R15，路线项总数由 14 增至 15，三段边界改为止血 R1–R5 / 重造 R6–R10 / 治根 R11–R15。**本文件此前演进记录里提到的编号按旧编号读**：其中「R8 影响面」对应现 R9、「新增 R13 承接标签扩展」对应现 R14、「原 R13 顺延为 R14」对应现 R15。
- 2026-08-18：收窄 R1 的删除清单。`invariants.md` 与 `frontier.md` 从「删」改为「留待 R3 迁移」，落点由替代品设计决定；R1 只删抄真源的四份（`00_INDEX` / `identity` / `constraints` / `architecture` 模块地图段）、靠原地重评的两块（`architecture` 成熟度段、`capabilities.md`）与 `fold-state.json`。此条覆盖同日早前那条「`invariants` / `capabilities` 逐条核后随文件夹删除」的处置——`capabilities.md` 仍删，`invariants.md` 改留。
- 2026-08-18（R1 收口 · 交接登记）：ITER-0112 只做去指针，以下三处的实际改造确定交给 R14 与 R15，按现行编号登记，逐项写明现状与归属。**一、`migration-schema.md §4` 的 `[split]` 标签**：现状是标签仍在文中、语义仍是「把单文件 `.ai/PROJECT.md` 拆成 `.ai/project/` 目录」，本轮只在原处加了退役标注（自 v4.0.0 起不再产生新实例），没有删除——历史配方 v1.6.0 至 v2.2.0 引用了它，`manifest.json` 的一致性校验要求标签定义与配方引用对得上，删了会红。正式的动作类型改造归 **R14**（升级器 typed 标签扩展）。**二、`upgrade.py` 的 `--split defer|now`**：现状是 `apply` 子命令的必填参数，配套 `project-knowledge-shape-valid` 前置校验仍在跑，两者都以 `.ai/project/` 存在为前提，本轮一行未动。参数降级或移除、前置校验的去留归 **R14**。**三、`mcv-deployment.md §2` 的空种子例外**：现状是该节里「部署即建 `.ai/project/` 空种子」的说明与理由已删干净，但老项目磁盘上已经建出来的空目录没人负责清——部署侧不再生成，存量不会自动消失。存量清理与老项目一次性交代归 **R15**（v4.0.0 迁移配方）。
- 2026-08-19（R2 · 发布处置登记）：ITER-0113 改了两份部署入口模板——`templates/AGENTS.md.template` 的读序段整段换成投影块，`templates/CLAUDE.md.template` 新增「会话起始：恢复项目状态」章节并首次带上读序块。按 `migration-schema.md §5` 的领域变更判据，这两份是注入目标项目的载体，故**下个发布版必须含 `[regen-entrypoints]`，不得记 `[no-op]`**。滞后事实一并记明：已部署项目在跑 `/butler:upgrade` 重新生成入口之前，Codex 侧仍是旧的七步读序、Claude 侧仍然完全没有读序；让老项目真正拿到新入口归 **R15**（v4.0.0 迁移配方）。butler 仓自身与新部署项目即时生效，这段不一致是已知且有意接受的过渡代价。
- 2026-08-19（R3 · 前提修正一 · `frontier.md`）：本文件 2026-08-18 那条复盘把 `frontier.md` 判为「每次收口整体覆写、一直准确」，**实测不成立**。ITER-0114 开工前核查：该文件最后一次改动停在 ITER-0111（commit `0cf01e9`），此后两个迭代没动过；正文写「版本 v3.5.1」（实际 3.6.0）、「`current: none`，当前无 active Milestone、无 active Iteration」（实际 MILE-0016 与 ITER-0114 都 active）。根因是整体覆写靠折叠仪式驱动，R1 删掉仪式，覆写随之停止。**修正后的规律**：纯追加不需要驱动，所以活得下来；**整体覆写只在有东西强制触发重写时才活得下来**。R3 据此把可派生部分改为机器生成 + CI 比对，不再依赖任何收口时的自觉动作。
- 2026-08-19（R3 · 前提修正二 · `invariants.md`）：同一条复盘把 `invariants.md` 判为「纯追加、一直准确」，**只对了一半**。47 条里查出两条已假——「收口是原子仪式」仍写五步且第四步是「前滚项目全貌并写 fold receipt」（R1 已改为四步、第四步是自检），「冷启动读序固定」仍写旧四步（R2 已改为五步语义阶段）；另有 16 条完全不带真源指针，读者无从核对。**修正后的规律**：纯追加只保证「新条目不覆盖旧条目」，不保证「旧条目描述的东西没变」——一条不变量只要复述了机制的具体形状（步数 / 清单 / 顺序），机制一改它就假。R3 据此把两条改对、把「只写决策与理由 + 必带真源指针 + 不复述机制形状」写进文件头，并对无指针条目上棘轮（基线 16，只防增量，欠账已记入 `.ai/debt.md`）。
- 2026-08-19（R3 · 发布处置追记）：R3 因读序块第 5 步加按需指针，再次改动 `templates/AGENTS.md.template` 与 `templates/CLAUDE.md.template` 两份部署入口模板。R2 已登记的 `[regen-entrypoints]` 要求不变、不重复开条目；老项目在升级前拿不到新读序与新全貌产物这一滞后事实同样不变，仍归 **R15**。另登记一项本轮有意不做的事：`.ai/project/` 目录在 butler 仓自己已删空移除，但该路径仍是目标项目侧 `workspaces.md` 的规格落点（`workspace-scope-schema.md`），这个名字已名不副实，去留归 **R9**（根布局整理）。
- 2026-08-20（R4 · 路线图点名两项不存在）：路线项 R4 写的是「命令、skill、规则真源、registry 条目、`docs/workflows.md` 与 rule-card 引用」六项，实测只有四项存在。**规则真源**：`workflows/registry.json` 里 progress 的 `rule_source` 直接指向 `.claude/commands/butler/progress.md` 自身，`Coder/` 下从来没有过对应规则文件，删命令即等于删真源，没有第二处要清。**rule-card 引用**：`templates/rule-card.md` 全文未出现 progress，无需改动。两项在 ITER-0115 如实记为不适用，不假装完成。同轮另有三处路线图没写、但属同一条链的处置：`review` 的负向触发词 `项目进度` 与 `project status` 是一对，只为把请求推离 review、推向 progress 而存在，progress 一死两条同删；`workflows/router-examples.json` 那条样例改写为 `not-butler` 而非删除，把这次退役的结果钉成回归断言；`scripts/sync-workflow-registry.py` 文档模板里两处硬编码的工作流个数改成从 registry 派生，属顺手治本。
- 2026-08-20（R4 · 发布处置登记）：ITER-0115 删了 `/butler:progress` 与 `$butler-progress` 两个宿主入口，两侧生效方式不同，必须分开记。**Claude 侧**：全局命令是 `scripts/setup.sh` 建的软链，指向本仓 `.claude/commands/butler/` 目录，删文件即全局立刻生效，迁移配方不需要为它写动作。**Codex 侧**：个人 plugin 是 `scripts/install-codex-plugin.sh` 拷贝出去的副本，用户机器上那份 `butler-progress` skill 不会因仓库删除而消失——在重跑安装前，Codex 里仍能发现并触发它，而它 `SKILL.md` 指的规则文件已经不存在。故 v4.0.0 配方**必须含 `[global-install]`**，归 **R15**。本轮不做兼容降级、不留 deprecated 桩：留桩等于让这条链多活一个版本，与退役目的相反。另按 `migration-schema.md §5` 判过一遍——本轮没动 `templates/rule-card.md` 与两份入口模板，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`，故**不触发 `[regen-entrypoints]`**；R2/R3 已登记的那条要求不变、不重复开条目。

- 2026-08-20（R5 · 路线项把两件事捆在了一起）：R5 的 In Scope 写的是「`/butler:loop` 降级：保留代码路径但撤掉 `upgrade-convergence-engine` 候办、命令不再演进」，读起来像那份候办属于 loop。**实测是名字撞车**：`upgrade-convergence-engine` 讲的是 `/butler:upgrade` 升级器的重写（文件所有权、部署回执、虚拟文件图、结构化诊断），`/butler:loop` 讲的是 P4 执行的高强度纠错升档，唯一的共同点是名字里都有「收敛」；全部 10 份候办里没有任何一份是关于 loop 的。故 ITER-0116 按**两件独立清理**执行，各有各的理由、不互相当依据。撤那份候办的真实理由是升级器**从来没在任何真实已部署项目上跑过**（`.ai/debt.md` 有这条账），给一个还没被真实用过的工具规划三个迭代的重写，正是本里程碑在砍的那类过度设计；重启条件是 R15 的真实老项目升级回归出结论之后。要说明的是 R14 / R15 **并没有覆盖**这份候办的范围（它们只做删除与移动两类新动作标签、加一次真实回归），撤它不是因为「已经有人做了」，而是因为「还没有数据支持现在做」。

- 2026-08-20（R5 · 前提修正 · debt 那条已假）：`.ai/debt.md` 里「危险模式规则真源仍把 P4 与 `/butler:loop` 自动绑定」这条**开工前核查已不成立**。ITER-0110 的提交（`41ad694`，2026-08-17）信息里明写「解除 Dangerous/Loop 错误包含」，同一次提交新建 `Coder/30_Quality_Gate/bounded-convergence.md` 作为两个模式共用的定量熔断真源，`dangerous-engine.md §6` 改成复用它、§9 改成「两者是并列模式，互不激活、互不读写对方状态」。**根因**：这条账是 2026-08-20（ITER-0114）从退役的 `.ai/project/frontier.md` 整批迁进 `debt.md` 的，迁的时候只搬字面、没有回头复核。这是 ITER-0114 自己在本节总结出的那条规律第二次应验——**纯追加只保证新条目不覆盖旧条目，不保证旧条目描述的东西没变**。本轮按 `debt.md` 文件头纪律「还掉的删除、不留历史」清掉，并如实记明是**已还清**而不是本轮修的。

- 2026-08-20（R5 · 冻结的载体选择与它没有兜底）：冻结声明落在规则真源 `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` 的 H1 之后、`## 1. 身份` 之前，写足三要素——冻结含义（代码路径与行为原样保留、`/butler:loop` 照常可用，冻结的是演进）、冻结起始（ITER-0116 / MILE-0016 R5）、解冻条件（R13 依真实使用数据做最终处置）。**否掉的落点是 `workflows/registry.json` 加冻结字段**：`scripts/sync-workflow-registry.py` 用严格字段集校验，加一个字段要连带改 12 个工作流对象、校验常量、生成投影与相关测试，为一条一次性的流程承诺改全局结构不划算；也否掉了写进 frontmatter，因为规则 frontmatter 全仓没有任何机器校验，写了既不被检查也容易在读取时被剥掉。**由此产生的事实要摆明：冻结靠声明与评审自觉，没有任何检查会拦住有人后来又改 loop**——真正能强制的只有删除，而删除正是本轮明确不做的。该缺口已按同口径记入 `.ai/debt.md`，随 R13 的最终处置自然消解。另按 `migration-schema.md §5` 判定本轮**不触发 `[regen-entrypoints]`**：改的三份规则文件里，两份入口模板只引用 `logic-protocol.md` 的路径而不嵌其内容，`templates/rule-card.md` 全文未提收敛闭环，改动没有流进目标项目的 `CLAUDE.md` / `AGENTS.md`。

- 2026-08-20（R6 · 路径撞车：新旧两份 inbox 契约共占 `.ai/INBOX.md`）：R6 要定的是新的三层数据契约，但 `.ai/INBOX.md` 这条路径当前被 `inbox-schema.md` 占着，而删旧契约排在 R8。三个选项：①先删旧的再写新的（等于把 R8 提前，牵动 100 行 CI 断言和 `tools/inbox/` 全目录，本轮扛不住）；②新契约先写别的路径、R8 再搬（多一轮改名和一轮全仓引用修正）；③**两份并存，靠声明分工**。选③：新契约落 `Coder/40_Context_Management/intake-schema.md`（永久名，不带版本号后缀），顶部一段引用块写明三件事——两份真源并存、新契约在 R7 前对该路径零写入、遇到格式分歧一律以 `inbox-schema.md` 为准。代价是这条分工**没有任何机器兜底**，靠声明和评审自觉，已同步记进 `.ai/debt.md`。分工只能单向声明（新的指回旧的），因为本轮明确不动旧契约一个字。

- 2026-08-20（R6 · 定序：孵化区目录按现实路径写，不按路线图字面写）：R5.3 路线图里 R6 那条写的是 `.ai/backlog/`，但那个目录到 R9 改名时才存在；当前真实路径是 `.ai/milestone-backlog/`。新契约全篇按**真实路径**写，另在正文里明写一句「R9 会改名、届时本契约同批更新」。不按路线图字面写的理由：契约里出现一条当下不存在的路径，等于写了一句假话，而 butler 已经被这种假条目咬过（`invariants.md` 的假条目、`.ai/debt.md` 里那条已还清却还挂着的欠账）。

- 2026-08-20（R6 · 孵化区规模分档的连带影响，以及索引为什么不加列）：给候办草稿加 `规模` 三档，连带要改 `milestone-schema.md §4.5` 的编写规则两条（草稿头部标记由两项扩为三项、「沿用 §5 四段结构」改为按档），并回填 9 份存量草稿的 `规模: milestone`（每份恰 1 增 0 删）。P2 原本还写了「给 `.ai/MILESTONES.md` 待办区索引加一列」，P3 撤回：明面成本是审计脚本把候办表写死成 5 列、要动 3 处代码加 11 行测试夹具；真正劝退的是**规模会同时躺在草稿头部和索引行，造出第二个真源**，而防漂移得再加一条一致性断言，恰是本轮 Out of Scope 明写不做的。已按 `iteration-schema.md §5.3` 走 amend，索引一字未改。将来按规模筛选时从 9 份小文件头部读即可。

- 2026-08-20（R7 · 复用 `inbox` 这个 id，不新开工作流）：新命令的语义（记闪念 / 看两层 / 执行处置）跟旧的收件箱扫描已经不是一回事，直觉上该新开一个 id。**否掉的理由是代价不对称**：`scripts/sync-workflow-registry.py` 把工作流 id 集合写死在 `EXPECTED_IDS` 里，加一个 id 会让业务工作流从 12 变 13，而「12 个工作流」这个数字散落在多份人读文档里、**没有任何机器检查兜底**（同一件事已在 `.ai/debt.md` 有账）。复用 id 只需改字段——`rule_source` 改指新动作层、两处 description 与语义触发词改写、去掉 `scan origin` / `处理 origin` 这类已经不存在的行为字样——命令文件集合、skill 集合、软链集合、散文计数全都不动。顺带修掉一处会说假话的地方：`workflows/router-examples.json` 里 inbox 那条示例请求原文是「处理 origin 里的需求收件箱」，描述的是一个即将不存在的行为，改成「先把这个想法记进闪念口，回头再说」。

- 2026-08-20（R7 · 必须动 R6 声明不碰的 `test_inbox_workflow.py`，边界划在哪）：R6 的 Out of Scope 写着旧链一字不动，`templates/hooks/tests/test_inbox_workflow.py` 也在那份清单里。**但它不是一份纯粹的旧链测试**——三个用例里有两个断言的是**当前活着的接线**（注册表 inbox 条目的 `rule_source`、两份薄壳正文必须提到的字样），活接线一改指新契约，这两个用例必红。所以本轮把这份文件拆成两半：`test_inbox_workflow_route_and_safety_contract` 断言的是旧规则文件 `inbox-workflow.md` 自身的内容，**原样不动**，随 R8 与那份文件一起退役；另外两个用例改指 `intake-workflow.md` / `intake-schema.md` / `tools/intake/`，并删掉 `origin/` 那条断言——新薄壳不扫 `origin/`，留着断言等于逼薄壳写假话。边界是硬的：`inbox-schema.md`、`inbox-workflow.md`、`test_inbox_contract.py`、`tools/inbox/` 全目录逐字节未动，有开工前哈希为证。文件名也不改：它测的仍是 inbox 这个工作流，改名对目录发现式测试没有收益。

- 2026-08-20（R7 · 执行分流两条出口在自己仓里跑不通，只能沙箱证）：`promote`（提升为里程碑）与 `iterate`（开为迭代）都要求对应台账的 `current` 是 `none`，而 butler 仓现在 MILE-0016 与 ITER-0118 都 active——**这两条出口在本轮的真实环境里根本没法跑**。折衷是在临时项目根上造一个 `current: none` 的沙箱各跑一遍（脚本留在 `.ai/iterations/ITER-0118/sandbox-dogfood.py`，可重跑），并额外跑一组对照：把 `current` 改成非 `none`，断言两条出口都被拦下且草稿仍在。**这一档要跟真实 dogfood 分开读**：沙箱证明的是代码路径通，证明不了真实使用下好用。本轮真实用上的只有 `add` 与 `handle --to incubated` 这一段（记下「交付页渲染器只活在会话临时目录里」这条真闪念，孵化成候办 `delivery-renderer-in-repo`，候办由 9 增为 10）。剩下四条动作路径（`done` / `dropped` / 两条出口）的真实使用要等后续迭代自然发生。

- 2026-08-20（R7 · `milestone-schema.md §7.6` 改指工具后变成两次调用）：§7.6「普通暂缓」原来的第 3、4 步是让模型照文字手工写草稿文件和索引行，本轮合并成一步调工具。**执行时才发现形状不对**：工具的 `handle --to incubated` 要求先有一条闪念行，而 §7.6 是从 `/milestone` 的对话里进来的，那个方向不一定进过闪念口。两种改法——给工具开一条「直接建草稿、不要闪念行」的旁路，或者让 §7.6 明写两次调用（先 `add` 记一条闪念拿到键，再 `handle` 孵化它）。**选后者**：旁路等于给孵化区开第二个入口，而三层契约的整个意义就是所有东西从闪念口进；多一次调用换来的是「这个方向什么时候第一次出现」有据可查。代价是暂缓一个方向要敲两条命令，写进 §7.6 明说清楚。另按 `migration-schema.md §5` 判过一遍，本轮没动 `templates/rule-card.md` 与两份入口模板，**不触发 `[regen-entrypoints]`**。

- 2026-08-21（R8 · `origin/` 退役后原件放哪，为什么是目录不是文件名前缀）：开工时的方案是「用户点名任意路径」，用户当场否掉，定成**所有外部资料引用统一收进 `.ai/references/`**，不再另开通道。落地形态是在它下面开 `raw/` 子目录专放用户原件——**用目录而不是文件名前缀承载身份**，因为路径前缀能被 hook 与工具机械判定，而文件名约定只能靠人自觉。代价说清楚：`.ai/references/` 原本的定位是「外部权威资料的落盘区」，里面清一色是 AI 派生的受控投影，现在要容纳一类 AI 一个字都不许动的原件，`references-schema.md` 的 §1 定位段和 §2 资料分类都得改写，并且必须在正文里点破一件事——**「引用了 `.ai/references/` 里的东西」不再等于「引用了权威投影」**，验收要对账的指针必须落在 `raw/` 之外。顺带修掉 §1 那张还拿已退役的 `.ai/project/` 做对照的表。

- 2026-08-21（R8 · 原件只读的 hook 门禁撤出本轮，条件写死）：查证发现「AI 只读用户原件」这条纪律**从来没有机器兜底**（整个 `templates/hooks/` 对 `origin` 零命中，唯一一处是 `bypass.py` 注释里的英文单词 original）。所以本轮原计划顺手给新位置加一条 PreToolUse 规则，免得把散文换个地方再写一遍。**实测撞死**：`scripts/test-butler-upgrade.py` 有一条断言要求工作区 `templates/hooks/` 的树摘要等于当前 `VERSION` 对应 tag 的摘要，而 `VERSION` 是 3.6.0、`v3.6.0` 已打 tag，加任何非测试的 hook 文件都会让它红（探针实测 `bd92a614…` != `84a3c089…`）；抬 `VERSION` 绕不开，反而从 1 个失败变成 1 个失败加 4 个错误。与本轮 Out of Scope 的「不切版」不可兼得，按 `iteration-schema.md §5.3` 退回 draft 撤回该条并重新 ACK。**恢复条件写死**：下次切版之后的任意一轮。已在 `.ai/debt.md` 双条记账——一条记纪律无兜底，一条记那条断言把「未发布的 hook 改动」误判成「白名单不可信」。

- 2026-08-21（R8 · 按 `migration-schema.md §5` 的迁移判定，四条结论逐条落地）：①改了 `templates/rule-card.md`（两处 `origin/` 措辞），按 §5 的硬规矩，`migrations/v4.0.0.md` 的配方**必须含 `[regen-entrypoints]`**；②`templates/hooks/` 的非测试文件零改动，树摘要与开工前逐字相同，**不需要 `[sync-hooks]`**（本轮只删了 `tests/` 下一份合同测试，而 `skip_hook_file()` 本来就把 `tests` 排除在摘要之外）；③`.ai/` 下产物结构没有新增必填字段，**不需要 `[add-field]`**；④`origin/` 目录的删除与内容搬迁**没有任何 typed 动作能表达**——升级器只有 rename / split / add-field / regen-entrypoints / sync-hooks / restamp / no-op 这七种，既没有删除也没有移动，要等 R14 补上这两类标签之后才写得出来。§5 那句「未提到 ≠ 已确认无影响」要求逐条列明，所以四条全部登记，不省略判否的。

- 2026-08-21（R8 · 已部署项目侧做不干净的部分，明确指向 R14 / R15）：本轮对别人硬盘上的项目，最多只能做到「butler 不再创建、不再读、不再教」。两样东西留在原地：**残留的 `origin/` 目录**（升级器没有删除与移动动作，归 R14；好在它本来就是用户自管、AI 零写入，留着不构成漂移）和**旧格式 `.ai/INBOX.md`**（R8 删掉上一代契约与 `tools/inbox/` 之后，仓里连一个认识旧格式的工具都没有，**没有降级读法可退**）。后者的兜底是 fail-closed：新工具碰到旧格式直接报错停下、一个字节都不写，本轮新加的 `TestLegacyInboxIsRefusedNotRewritten` 四个用例把这个行为锁死。真正的迁移配方归 R15 的 `migrations/v4.0.0.md`。这两笔都在 `.ai/debt.md` 有账，不靠「以后都用新地方」了事。

- 2026-08-21（R8 · 本轮没有 TDD 配对，理由说在前面）：AC11 原定写成「先红后绿」的配对——拿旧格式 `.ai/INBOX.md` 喂 `add` / `list` / `handle`，期望先看到工具把旧文件写坏或误读，再修成拒绝。**P3 探针实测三个子命令都已经是正确行为**：都以退出码 1 停下、都报「表头必须逐字是 `| 闪念键 | 记于 | 一句话 | 状态 | 去向 |`」、都零字节写入。行为本来就对，写出来就是绿的，**没有真实的红**。硬造一个红（比如先把校验删掉再加回来）是伪造配对证据，比不做更坏。所以降级为回归防线：断言这个行为存在并锁死，`.ai/TECH_PLAN.md` 里明写本轮不声称 TDD 配对。
