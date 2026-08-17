<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0111 · 领域治理接线与真实 dogfood（MILE-0015 R5）

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-08-17

## Current Understanding

- **一句话**：R1–R4 已经把领域模型建起来了，但它现在只在 butler 仓自己的一条路径上生效——改了领域定义没人拦，Codex 入口和部署项目根本不知道有这套渐进读取规则，发布时也没说部署项目要不要跟。这一轮把这三处接线补上，然后用本迭代自身量一次成本，回答「这套治理值不值得继续」。
- **Goal**：让领域变更在评审和 CI 两处被抓住；让 L0 渐进读取内核在三个宿主入口口径一致且不双写；让领域变更在发布时有明确的升级处置；并给出 MILE-0015 的继续 / 缩减 / 停止判断。
- **现状证据（接线缺口）**：全仓检索 `domain-model` / `domain-glossary` / `context-map` / `domain-contract` 的引用，命中集中在 `Coder/` 四份规则、`tools/context-budget/`、`tools/domain-contract/` 和历史迭代产物；`AGENTS.md`、`templates/rule-card.md`、`templates/CLAUDE.md.template`、`Coder/30_Quality_Gate/review-standard.md`、`Coder/60_Extension_CodeReview/review-engine.md`、`Coder/20_Workflow_Lifecycle/migration-schema.md` 全部零命中。
- **现状证据（CI 已部分接线）**：`scripts/verify-ci.sh` 已跑 `domain_contract.py check` 与 `context_budget.py check`，本轮不是从零接 CI，而是补一个现在漏掉的门——`domains.v1.json` 里登记的条目可以完全没有断言或关系覆盖，等于登记了却没有任何回归能抓住它变坏。
- **现状证据（投影可行）**：`Coder/README.md` 的 L0 块用 `<!-- butler-context-l0:begin/end -->` 成对标记包住，正文里的规则指针写的是裸文件名（`domain-model.md`），和 `templates/rule-card.md` 引用其他规则的写法一致，因此可以按字节原样投影，不需要为不同宿主改写路径。
- **现状证据（升级面）**：`Coder/` 规则正文由运行时实时读取、不进目标项目，所以领域定义本身改动对部署项目通常无影响；但一旦 L0 进入 `templates/rule-card.md`，它会流进部署项目的 `CLAUDE.md` 与 `AGENTS.md`，发布时就必须显式给出重新生成宿主入口的动作，不能默认 `[no-op]`。
- **预期产出**：一维评审口径 + 一个 CI 覆盖门 + 一份三处一致的 L0 投影及其校验 + 一段升级处置口径 + 一份带数字的成本收益结论。
- **项目形态**：Markdown 规则仓，附带 Python / Shell / TypeScript 驻留工具；未命中业务 Domain / Stack Profile，按通用 SOP 与现有仓库门禁推进。

## Scope

- **In Scope**：`review-standard.md` 新增「领域变更」审计维度，`review-engine.md` 在多维评审列表中登记该维度；四项强制声明为唯一所有者、兼容影响、迁移路径、负向样例。
- **In Scope**：`domain_contract.py` 新增条目覆盖门——每条 `entries[]` 至少被一条 `assertions[]` 或 `relations[]` 覆盖，未覆盖 fail-closed 并给出具体条目 id；补正负 fixture，沿用已在 CI 中的调用点。
- **In Scope**：以 `Coder/README.md` 的 L0 块为唯一真源，字节一致投影到 `AGENTS.md` 与 `templates/rule-card.md`；`context_budget.py` 校验三处一致且预算不超；确认 `scripts/render-project-entrypoints.py` 生成的部署入口随之带上 L0 且现有双宿主验证不破。
- **In Scope**：`migration-schema.md` 补一节「领域变更的升级处置」，说清哪类领域变更对部署项目无影响、哪类必须重新生成宿主入口，并为本次 rule-card 变更产出对应处置结论。
- **In Scope**：把本迭代自身当作一次跨上下文设计样本做 dogfood，记录实际走过的路由层级、读取真源份数、L0/L1/L2 的 token 口径与新增维护成本，把继续 / 缩减 / 停止的结论写回 `.ai/MILESTONE.md`。
- **Out of Scope**：不做运行时加载遥测采集——「哪个宿主实际读了哪层」需要长期埋点，属 `butler-slim-down` 候办的 usage instrumentation，本轮只做一次性人工计量。
- **Out of Scope**：不新增限界上下文、不扩充 20 项术语表条目、不新增领域合同条目（除非接线本身要求）。
- **Out of Scope**：不重构 `Coder/` 目录分层，不改既有命令、文件路径与状态值。
- **Out of Scope**：不吞并 `state-transition-trust-gate`、`butler-slim-down` 等候办；不改动 MILE-0014 的 Decision Map / Work / Promotion 状态机。
- **Out of Scope**：不修 `tech_plan` 的 manifest 与 `tech-plan-schema.md` 段数漂移（ITER-0110 已登记为另开迭代的欠债）。

## Open Questions / Risks

- **待确认 · Pi 是否要投影**：Pi 扩展（`plugins/butler-pi/`）目前只拦截写入调用、不注入任何读取顺序，没有承载 L0 的位置。倾向不投影，只覆盖 `AGENTS.md` 与 `templates/rule-card.md`；若要覆盖 Pi，需要先给它一个规则注入面，范围会明显变大。
- **待确认 · 部署项目多花的 token**：L0 块上限 1600 字节（约 0.4k–0.5k tokens），进 rule-card 后每个部署项目冷启动都要付。当前 rule-card 正文约 3.8k–4.8k tokens，增幅约一成。收益是部署项目也能按分层读领域规则而不是全量吞；代价是所有项目都付这笔钱，包括从不碰领域治理的小项目。
- **风险 · 投影可能只是搬字**：如果三处 L0 只是字节复制而没有任何一处真的改变行为，这条接线就是纯成本。dogfood 阶段必须诚实回答它有没有产生可观察的差别，不能因为做了就写成有效。
- **风险 · 评审维度落不了地**：审计维度写进规则容易，真被执行难。四项声明必须尽量绑到机器可判的落点（覆盖门 + fixture），不能只留一段散文清单。
- **风险 · dogfood 样本偏小**：只用本迭代一个样本量成本收益，代表性有限；结论必须标明样本范围，不得推广成普遍结论。
