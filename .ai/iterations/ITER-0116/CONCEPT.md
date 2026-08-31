<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0116 · loop 降级与候办清理（MILE-0016 R5）

## Current Understanding

路线项 R5 点名三个动作：撤 `upgrade-convergence-engine` 候办、冻结 `/butler:loop` 的命令演进、登记待定处置。三个都能做，但开工前核查发现路线项的措辞里有一处把两件不相干的事捆在了一起，另有两条前提要更正。

**一、候办和 loop 没有关系，是名字撞车。**

MILE-0016 的 In Scope 写的是「`/butler:loop` 降级：保留代码路径但撤掉 `upgrade-convergence-engine` 候办、命令不再演进」，读起来像是那份候办属于 loop。实测不是：`upgrade-convergence-engine` 讲的是 `/butler:upgrade` 升级器的重写（文件所有权、部署回执、虚拟文件图、结构化诊断），`/butler:loop` 讲的是 P4 执行的高强度纠错升档，两者唯一的共同点是名字里都有「收敛」。全部 10 份候办里没有任何一份是关于 loop 的。

所以这一轮实际是**一次迭代里做两件独立的清理**，各有各的理由，不能互相当依据：

| 动作 | 真实理由 |
|---|---|
| 撤 `upgrade-convergence-engine` 候办 | 升级器**从来没在任何真实已部署项目上跑过**（`.ai/debt.md` 有这条账）。给一个还没被真实用过的工具规划三个迭代的重写，正是 MILE-0016 在砍的那类过度设计。R15 会做第一次真实老项目升级回归，那之后才有数据说这个重写该不该做 |
| 冻结 `/butler:loop` 演进 | 保留代码路径，停止投入；最终去留由 R13 的使用数据决定 |

要说清楚的是 R14 / R15 **并没有覆盖**这份候办的范围（它们只做删除与移动两类新动作标签、加一次真实回归），撤它不是因为「已经有人做了」，而是因为「还没有数据支持现在做」。

**二、`.ai/debt.md` 里「危险模式仍把 P4 与 `/butler:loop` 自动绑定」这条已经不成立。**

那条账写的是「用户已明确两者正交，但 `dangerous-engine.md` 与 `logic-protocol.md` 口径不一致，需要一次独立纠偏迭代」。实测早就修好了——ITER-0110 的提交（`41ad694`，2026-08-17）信息里明写「解除 Dangerous/Loop 错误包含」，同一次提交新建了 `Coder/30_Quality_Gate/bounded-convergence.md` 作为两个模式共用的定量熔断真源，`dangerous-engine.md §6` 改成复用它、§9 改成「两者是并列模式，互不激活、互不读写对方状态」。

这条账是 2026-08-20（ITER-0114）从退役的 `frontier.md` 整批迁进 `debt.md` 的，迁的时候只搬字面、没有回头复核。这正是 ITER-0114 自己在 `.ai/MILESTONE.md §5.4` 总结出来的那条规律第二次应验：**纯追加只保证新条目不覆盖旧条目，不保证旧条目描述的东西没变**。本轮把它清掉，并如实记明是「已还清」而不是「本轮修的」。

**三、真正还在给 loop 拉客的是另一处，路线项没点到。**

`Coder/00_System_Prompt/logic-protocol.md` 结尾有一句：「若检测到任务复杂度极高（如核心算法、大规模重构），应主动询问：检测到逻辑复杂，是否需要开启收敛闭环模式进行高强度迭代验证？」

这句和降级的方向正相反。`workflows/registry.json` 给 loop 标的是 `allow_implicit_invocation: false`（高风险、必须显式点名），而这句让模型凭自己对「复杂度」的内部判断去兜售它。对比同一份文件里 Explore / Ideation 那条的写法——「模型不得用内部判断静默切换」——loop 这句是同一份规则里的双标。更要紧的是：它制造的正是 R13 要拿来判 loop 生死的那份使用数据。冻结一个命令的同时还留着自动推销它的话术，冻结就是空的。

**四、还有一处残留指针，不是耦合但要拆。**

`dangerous-engine.md §8` 熔断交还那段把 RCA 格式指向 `convergence-loop-engine.md §7`，而 `§7` 自己又转指 `bounded-convergence.md §3`。多绕一跳，不影响正确性，但它让 dangerous 模式对 loop 的规则文件产生了一条纸面依赖。loop 既然被冻结、将来可能被删，这一跳现在拆掉最省事，否则 R13 动 loop 会连带打断 dangerous 的 RCA 指针。

## Scope

**In Scope**

- 撤 `upgrade-convergence-engine` 候办：处置 `.ai/milestone-backlog/upgrade-convergence-engine.md` 与 `.ai/MILESTONES.md` 待办区那一行，并写明撤的理由与重启条件（R15 的真实升级回归出结论之后）。
- 冻结 `/butler:loop` 命令演进：在规则真源 `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` 写明冻结状态、冻结含义（代码路径保留、行为不变、不再接受演进）与解冻条件（R13 依使用数据最终处置）。
- 删掉 `logic-protocol.md` 那句主动询问，让 loop 的触发面收敛为「显式点名」，与 registry 的 `allow_implicit_invocation: false` 对齐。
- 把 `dangerous-engine.md §8` 的 RCA 指针从 `convergence-loop-engine.md §7` 改为直指 `bounded-convergence.md §3`，解除 dangerous 对 loop 规则文件的纸面依赖。
- 清掉 `.ai/debt.md` 里那条已不成立的「危险模式仍把 P4 与 loop 自动绑定」，按 debt 文件头的纪律「还掉的删除、不留历史」。
- 在 `.ai/MILESTONE.md §5.4` 登记三条：候办与 loop 是名字撞车不是同一件事、debt 那条已假的发现与根因、冻结的载体选择与它没有机器兜底这个事实。

**Out of Scope**

- **不删 `/butler:loop`**。命令、skill、registry 条目、规则文件、软链全部原样保留，行为一字不改。删不删是 R13 依使用数据决定的事，本轮只停投入。
- 不改 `bounded-convergence.md` 的熔断纪律本身，也不动 `correction-contract.md` 的常驻「诚实停」。
- 不动 `/butler:dangerous` 的激活语义、自审门与护栏，只改它那一条 RCA 指针。
- 不给 registry 加「冻结」字段——代价与收益见 P3；本轮若不加，缺口如实登记。
- 不处置另外 9 份候办。它们各有各的暂缓理由，本轮没有重新评估的依据。
- 不装使用数据采集（R11）、不做 loop 的最终去留判断（R13）。
- 不切版、不发布。

## Open Questions / Risks

- **冻结这件事没有天然的机器载体**。`workflows/registry.json` 是工作流元数据真源，但 `scripts/sync-workflow-registry.py` 用 `exact_keys` 严格校验字段集，加一个 `frozen` 字段要同时改 12 个工作流对象、校验常量、生成投影与相关测试。收益是冻结状态机器可读，代价是为一条一次性的流程承诺改动全局 schema。倾向是**不加**，把冻结写进规则真源并在 `.ai/debt.md` 登记「无机器兜底」，与 ITER-0115 对散文计数的处置口径一致；最终在 P3 定。
- **撤候办没有 schema 支持**。`milestone-schema.md` 只定义了 `候办状态: deferred` 一个取值，没有「撤回」这一态。要么删文件把理由留在台账与 §5.4，要么给 schema 加一个状态值。前者信息会散，后者动规则。P3 定。
- **撤候办是判断，不是数据**。依据是「升级器从没在真实项目上跑过，现在做重写没有依据」，这个判断本身也没有使用数据支撑（装监视器是 R11）。如果 R15 的真实回归暴露出升级器确实卡得很死，这份候办要重开——重开的是新候办，不是复活旧文件里那份 2026-08-04 的范围评估。
- **冻结靠自觉**。没有任何机器能拦住「有人后来又去改 loop 的规则或命令」。真正的强制只有删除，而删除恰恰是本轮明确不做的事。
