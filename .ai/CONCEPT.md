<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0112 · 退役项目知识文件夹与折叠机制（MILE-0016 R1）

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-08-18

## Current Understanding

- **一句话**：`.ai/project/` 里真正烂掉的是抄真源和需要原地重评的那几份，折叠机制只维护得住追加式内容、维护不住回头重评。本轮把烂掉的那部分连同折叠闭环一起删掉，解除两处收口仪式对折叠的强制，并把被证明有效的 `invariants.md` 与 `frontier.md` 原地留着交给 R3 的替代品设计。
- **Goal**：让抄真源的四份、靠原地重评的两块与 `fold-state.json` 从仓库消失，`knowledge-fold` / `drift-check` 两个帮手退役，两处收口仪式第四步不再要求折叠，且删完之后全仓没有指向已删文件的活引用——本轮结束时仓库必须自洽，不能把断指针留给 R2。`invariants.md` 与 `frontier.md` 保留原位不动。
- **现状证据（零消费已坐实）**：MILE-0014 早被评估为「概念空缺真实、当前设计不符合预期」，但 `capabilities.md` 一直挂着「已交付 R1-R5」，这条失真挂了三周没被任何读取发现。追问「过去半年有没有哪次决策因为读了知识文件夹而做出或改变」，答不出来。
- **现状证据（目录实况比范围表大）**：`.ai/project/` 里实际有 9 个文件——`00_INDEX.md`、`identity.md`、`architecture.md`、`capabilities.md`、`invariants.md`、`constraints.md`、`debt.md`、`frontier.md`、`fold-state.json`。里程碑 In Scope 原只点名 5 个，其余 4 个的处置由 §5.4 补齐。
- **现状证据（烂的不是全部，规律很清楚）**：按覆盖到的最新里程碑量四份主题文件——`architecture.md` 成熟度段只写到 MILE-0007，落后 9 个里程碑；`capabilities.md` 覆盖到 MILE-0015 但旧节内容失真（MILE-0014 那条）；`frontier.md` 每次收口整体覆写，当前；`invariants.md` 纯追加条目，当前，其中 38 条带 `*为什么*` 理由、别处无真源。规律是**整体覆写和纯追加都活得下来，需要回头修改旧内容的必烂**——折叠是 delta 驱动的，改了 A 只会去折 A，没有任何动作触发「回头看 B 的旧结论还准不准」。
- **现状证据（需求本身成立）**：`context-persistence.md` 第 136 行原文写着「缺全貌产物时新会话只能从一堆迭代 delta 倒推全貌（管中窥豹）」。现有 112 个迭代、123 份交付，倒推不现实。所以本轮退役的是不匹配的机制，不是全貌观察这个需求；替代品设计归 R3。
- **现状证据（`debt.md` 不能跟着删）**：新读序把 `debt.md` 放在第一顺位（`debt.md` + handoff + 双台账），但它现在就躺在待删目录里。它必须迁位而不是删除，落点建议 `.ai/debt.md`。其余三个是派生摘要，正文各自都写着「真源 X」——`identity.md` 指仓库根 `CLAUDE.md` / `README.md` / `HUMAN_GUIDE.md`，`constraints.md` 每条都指对应 schema，`00_INDEX.md` 是这个文件夹自己的地图，随文件夹一起消失即可。
- **现状证据（退的是两态契约，不是一个目录）**：`project-digest-schema.md` 同时拥有「`.ai/project/` 文件夹态」和「单文件 `.ai/PROJECT.md` 老项目态」两种形态。删掉文件夹等于把这份 schema 整份退役，单文件态的 legacy 支持也一并消失。牵连到 `mcv-deployment.md §2` 的「部署即建空种子」（`.ai/project/` 是唯一一个部署就建的 `.ai/` 子目录例外）、`migration-schema.md §4` 的 `[split]` 标签，以及 `upgrade.py` 里 `--split defer|now` 这个 `apply` 的**必填参数**——后两处的动作面归 R14 / R15，本轮只做登记与去指针。
- **现状证据（改动面）**：全仓检索 `.ai/project` / `project-digest` / `knowledge-fold` / `drift-check` / `fold-state`，除去历史归档与交付存档，命中 **37 份活跃的规则、脚本、工具与模板文件**（含升级器 `upgrade.py` 与其 README）加 **2 份候办草稿**，分布在 `Coder/20_Workflow_Lifecycle/`（6 份）、`Coder/40_Context_Management/`（7 份）、`Coder/62_Extension_Agents/`（3 份）、`Coder/README.md` 与领域两份、模板与 hook 测试（5 份）、`scripts/`（4 份）、`tools/`（4 份）、命令与 skill 入口（2 份）。
- **现状证据（机器门禁会立刻发声）**：`scripts/audit-project-state.py` 现在把 fold receipt 当硬校验跑，`context-persistence.md §6` 第 6 条把「知识文件夹漂移自检」定为条件不变量。删文件而不同批改这两处，audit 会直接红。
- **预期产出**：9 个文件里 6 删、1 迁、2 留；两份帮手定义删除并从名册与 `Coder/README.md` 注销；`project-digest-schema.md` 退役；两处收口仪式第四步重写；audit 与漂移自检对应校验拆除；以及把本轮未处理的升级侧缺口交接给 R14 / R15 的明确登记。
- **项目形态**：Markdown 规则仓，附带 Python / Shell 驻留工具；未命中业务 Domain / Stack Profile，按通用 SOP 与现有仓库门禁推进。

## Scope

- **In Scope · 删文件**：删除 `00_INDEX.md`、`identity.md`、`constraints.md`、`capabilities.md`、`architecture.md`、`fold-state.json` 六份——前三份抄真源，`capabilities.md` 与 `architecture.md` 的成熟度段靠原地重评已确认失真，`architecture.md` 去掉成熟度段后只剩指向 `Coder/README.md` 的模块地图、一并删。删 `capabilities.md` 前逐条核，凡本仓别处无真源的判断先迁出。
- **In Scope · 留待 R3**：`invariants.md`（38 条 `*为什么*` 理由、纯追加、无漂移）与 `frontier.md`（每次收口整体覆写、一直准确）原位保留、内容不动，落点由 R3 的替代品设计决定。目录因此不消失，删完加迁走 `debt.md` 后剩这 2 个文件。
- **In Scope · 迁 `debt.md`**：`.ai/project/debt.md` 迁到 `.ai/debt.md`，内容原样保留（两条长期欠债），并把指向旧路径的引用改到新路径。
- **In Scope · 退帮手**：删除 `Coder/62_Extension_Agents/knowledge-fold.md` 与 `drift-check.md`，从 `62_Extension_Agents/overview.md` 名册和 `Coder/README.md` 的目录结构与读取顺序注销；名册从四个帮手缩到两个（`independent-review` / `decision-work`）。
- **In Scope · 解除收口强制**：重写 `iteration-schema.md §5.5 步④` 与 `milestone-schema.md §7.4 步④`，去掉知识文件夹折叠这一必做项及其两态分支，不留「按需前滚」的软化残留。
- **In Scope · 退契约**：删除 `Coder/40_Context_Management/project-digest-schema.md`，并从 `Coder/README.md` 注销；`handoff-spec.md`、`references-schema.md`、`prd-split.md`、`prd-status.md`、`workspace-scope-schema.md`、`artifact-style.md`、`domain-model.md`、`domain-glossary.md` 里指向它或指向知识文件夹的句子同批改到自洽。
- **In Scope · 拆机器校验**：`scripts/audit-project-state.py` 去掉 fold receipt 与知识文件夹相关校验（含 `test-audit-project-state.py` 对应用例）；`context-persistence.md §6` 第 6 条「知识文件夹漂移自检」不变量删除；`tools/context-budget/`、`templates/hooks/`、`tools/workspace-scope/`、`tools/mile0009-e2e/`、`scripts/verify-codex-foundation.sh` 里以 `.ai/project` 为夹具或断言的部分同批调整，`scripts/verify-ci.sh` 全绿。
- **In Scope · 最小去指针**：`AGENTS.md`、`templates/AGENTS.md.template`、`Coder/README.md`、`.claude/commands/butler/init.md`、`plugins/butler/skills/butler-init/SKILL.md`、`mcv-deployment.md` 里已经指不到东西的句子改到自洽——**只做去指针，不做新读序的正面定义**。
- **In Scope · 交接登记**：把本轮不动、但因删除而失去意义的升级侧机构（`migration-schema.md §4` 的 `[split]` 标签、`upgrade.py` 的 `--split` 必填参数与 `project-knowledge-shape-valid` 前置、`mcv-deployment.md §2` 的空种子例外）在 `.ai/MILESTONE.md §5.4` 登记为 R14 / R15 的确定输入。
- **Out of Scope**：不做新冷启动读序的正面定义——「`debt.md` + handoff + 双台账」这套读序怎么写、两份入口模板怎么改，归 R2；本轮只保证旧指针不悬空。
- **Out of Scope**：不改 `upgrade.py` 的动作类型表、路径校验与 CLI 参数，不新增删除 / 移动两类 typed 标签（R14），不写 `migrations/v4.0.0.md`（R15）。
- **Out of Scope**：不动 `/butler:progress`（R4）、`/butler:loop`（R5）、旧 inbox 全链与 `origin/`（R8）、根布局改名与迁位（R9）。
- **Out of Scope**：不设计新的全貌产物——生成部分怎么从 `registry.json` / 双台账 / `Coder/README.md` 派生、手写部分落到哪个文件，归 R3；本轮只负责把烂掉的删干净、把有效的留在原地。
- **Out of Scope**：不改 `.ai/ITERATIONS.md` / `.ai/MILESTONES.md` 双台账的结构与状态值，不动 `.ai/references/` 与 PRD 子系统的自身契约（只改它们里指向知识文件夹的句子）。
- **Out of Scope**：不切版、不发布；v4.0.0 聚合切版归里程碑收口。

## Open Questions / Risks

- **待确认 · R1 / R2 的边界切在哪**：路线图把「删文件夹」放 R1、「改冷启动读序」放 R2，但删完文件后 `context-persistence.md §6` 的第一读还指着 `.ai/project/00_INDEX.md`。迭代必须收口在自洽状态，不能留一整轮的断指针。倾向按上面 Scope 的切法——R1 做去指针到自洽，R2 做新读序的正面定义与模板改造。这会让 R1 比路线图字面描述略宽，需要在 `.ai/MILESTONE.md §5.4` 补一条演进记录。
- **待确认 · 单文件 `.ai/PROJECT.md` 老项目怎么办**：`project-digest-schema.md` 一份 schema 管两态，退役它等于连 legacy 单文件态一起停支持。已部署的老项目里可能还有 `.ai/PROJECT.md`。倾向本轮直接停止支持、在 R15 的 v4.0.0 配方里给出「自行保留或删除，Butler 不再读」的一次性交代，而不是在规则里留一条只为老项目活着的分支。
- **待确认 · `debt.md` 落到 `.ai/debt.md` 还是别处**：`.ai/` 根目前放的是四件套、双台账、handoff 与 task-state，都是流程产物；`debt.md` 是长期事实，性质不同。倾向仍放 `.ai/debt.md`（新读序第一顺位，路径要短好记），但这条会决定 R2 写读序时的措辞，越早定越好。
- **风险 · 删除会连带删掉唯一真源**：`invariants.md` 有 19KB、`capabilities.md` 有 27KB，绝大部分是指向真源的摘要，但不排除个别条目是只在这里写过的判断。删之前必须逐条过一遍，凡是本仓别处没有的长期决策，要么找到真正的归属文件迁过去，要么明确判定为可弃。这是本轮最容易出事的一步，不能整目录一把 `rm`。
- **风险 · 机器门禁比预想的黏**：audit、context-budget、hook 测试、workspace-scope 测试、codex 基线脚本五处都拿 `.ai/project` 当夹具或断言。改动散在测试里，容易改一半留一半，表现为 CI 局部绿、局部红。必须以 `scripts/verify-ci.sh` 一次全绿为收口判据，不接受单点跑过。
- **风险 · 删了才发现有人在读**：本轮论证的是「没有证据证明它被消费」，不是「已证明它从未被消费」。真正的确定性数据要等 R11 的 usage instrumentation。若删除后冷启动质量明显下降，回滚成本是一次 `git revert` 加一轮读序回退——代价可接受，但要在验证阶段诚实记录冷启动体感，不能因为删了就写成没影响。
- **风险 · 折叠历史随 `fold-state.json` 一起消失**：这份 37KB 的回执记录了历次折叠参与的文件与 hash。删掉后，历史迭代「有没有正确折叠」将无法再机器验证。判断是这本身就是自证式的账，留着也只服务于即将退役的机制；但要在交付里写明这条信息确实丢了，不装作无损。
