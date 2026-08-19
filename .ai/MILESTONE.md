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
| R3 | 止血·项目全貌产物重建：生成部分从 `registry.json` / `Coder/README.md` / 双台账 / `tools/` 派生，手写部分承接 `invariants.md` 的 38 条理由与 `frontier.md` 的覆写模式，定落点与重算命令 | — | planned |
| R4 | 止血·砍 `/butler:progress` 全链：命令、skill、规则真源、registry 条目、`docs/workflows.md` 与 rule-card 引用 | — | planned |
| R5 | 止血·`/butler:loop` 降级与候办清理：撤 `upgrade-convergence-engine` 候办、冻结命令演进、登记待定处置 | — | planned |
| R6 | 重造·inbox 三层数据契约与真源：闪念口、孵化区规模字段、执行分流的结构与状态定义 | — | planned |
| R7 | 重造·`/butler:inbox add \| list \| handle` 命令与工具实现，含真实 dogfood 跑通一条闪念到执行 | — | planned |
| R8 | 重造·退役旧 inbox 全链：`tools/inbox/`、SRC-NNNN、双 SHA-256 认亲、scanner 与 `origin/` 目录 | — | planned |
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
