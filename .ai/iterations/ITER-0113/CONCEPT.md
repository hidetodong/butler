<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0113 · 冷启动读序正式定义与四载体对齐（MILE-0016 R2）

## Current Understanding

**R1 只改了「第一读指哪」，没改「一共几步、每步干什么」。** 退役知识文件夹时，我把各处读序的第一项从 `.ai/project/00_INDEX.md` 换成 `.ai/debt.md`，让指针不悬空就收手了——那是 R1 的边界。结果现在读序处在一个尴尬状态：指针都对，但**五处载体说的读序互不相同**，而且没有任何机器检查能发现这件事。

**五处载体，五个版本。**

| 载体 | 步数 | 实际内容 |
|---|---|---|
| `context-persistence.md §6 冷启动读序`（真源） | 5 | debt → 双台账（含 state-index 定向读冷分片）→ handoff `check` 后才读 → Goal 状态重算 → 代码 / deliveries |
| butler 仓 `AGENTS.md` | 7 | debt → MILESTONES → ITERATIONS → task-state → handoff → 四件套 → Coder 指针 |
| `templates/AGENTS.md.template`（部署项目 Codex 入口） | 4 | debt → 双台账 → task-state + handoff → 四件套 |
| `Coder/README.md` 第 165 行（散文一段） | 3 | debt → ITERATIONS + handoff → 代码 |
| `templates/CLAUDE.md.template`（部署项目 Claude 入口） | **0** | 完全没有读序 |

这不是措辞差异，是实质差异：

- **真源要求「先 check 再读 handoff」，四个投影没一个照做。** 真源第 3 步写明先跑 `handoff.py check`，`fresh` 才读、`stale` 先 `sync` 重建、`error` 先修权威状态。两份 AGENTS 都写成直接「读 `.ai/02_SESSION_HANDOFF.md`」。rule-card 里倒是有这句 check/sync 纪律，但它在「强制工作流」段落里、不在读序中，宿主照读序走就绕过去了。
- **真源要求台账定向读，投影全都没提。** 真源第 2 步写明只读热表，需要旧身份时沿 `.ai/state-index.json` 用 state-ledger `lookup` 定向读**一个**冷分片，禁止默认读整个 history 目录。四个投影一处都没写这条约束。
- **真源第 4 步的 Goal 状态重算，butler 自己的 `AGENTS.md` 里根本没有。** template 里有，但被放在读序列表**外面**的一段散文里。
- **主力宿主的部署入口没有读序。** Claude 是主力宿主，`templates/CLAUDE.md.template` 通篇只有规则卡 + 深度阅读指针 + 项目特定约束，没有任何「会话起始怎么恢复状态」的段落。这个能力目前只有 Codex 侧有。

**唯一的机器校验只盯一个载体，而且自己就是第六份真源。** `scripts/verify-codex-foundation.sh` 第 45–66 行硬编码了一张 9 项路径列表（`.ai/debt.md` → `MILESTONES` → `ITERATIONS` → `task-state` → handoff → 四件套四份），检查 butler 仓 `AGENTS.md` 里这些路径按行号递增出现。它不看 template、不看 CLAUDE 侧、也不跟 `context-persistence.md` 对账——那张列表是脚本里另抄的一份，改真源不会让它红。

**这套问题 ITER-0111 已经解过一次，办法现成。** L0 渐进读取内核当时也是「一份规则、多处投影、无对账」，做法是用 `butler-context-l0:begin/end` 标记把规则正文圈成一个可投影块，投到三处载体，由 `context_budget.py` 每次 CI 逐字节比对，任一处被单独改动即报 `L0 projection mismatch: <文件>`。实测代价：L0 正文 656 字节、部署入口冷启动多约 234 token（占规则卡全文 3.8%），9 条 fixture。读序是同构问题，同一套办法可以直接搬。

**R1 留的过渡措辞该由 R2 清掉一半。** 两处：`context-persistence.md §6` 第 1 步下的引用块，和 `handoff-spec.md` 第 15 行，都写着「读序由 R2 定、全貌产物形态由 R3 定」。R2 交付后，读序那半话不成立了要删；全貌产物那半留给 R3。

## Scope

**In Scope**

- 在 `context-persistence.md §6` 把冷启动读序改写成正式定义：每步写明**读什么、读之前要先做什么、读到什么程度停**，把散在真源正文里的三条硬约束（handoff 先 check、台账定向读冷分片、Goal 状态重算）收进步骤本身，而不是留在步骤外的散文里。
- 用 `butler-context-order` 标记把读序圈成可投影块（沿用 L0 那套 `begin/end` 标记形态），真源在 `context-persistence.md`。
- 把读序块投到四处载体并逐字节一致：butler 仓 `AGENTS.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`（**新增**，Claude 宿主首次获得读序）、`Coder/README.md`（把第 165 行那段散文换成投影块）。
- `context_budget.py` 增读序投影一致性校验（复用 L0 的 `_l0_block()` 提取与比对路径）+ 负例 fixture：任一载体被单独改动、真源被改、标记缺失三类。
- `scripts/verify-codex-foundation.sh` 那张硬编码列表拆掉：读序内容的正确性交给新的投影校验，该脚本只保留「Codex 入口存在且含读序块标记」这一层，不再自己抄一份路径清单。
- 清掉属于读序的过渡措辞：`context-persistence.md §6` 第 1 步下引用块的读序那半、`handoff-spec.md` 第 15 行的读序那半；全貌产物那半原样留给 R3。
- rule-card 与读序块的分工定死：读序块独占「按什么顺序读哪些文件」，rule-card 第 45 行的 handoff check/sync 纪律独占「handoff 是派生视图、什么时候 sync」，两边互不复述、互相指。

**Out of Scope**

- 不定义全貌产物的形态、派生源与落点（R3）。`.ai/project/` 剩下的 `invariants.md` 与 `frontier.md` 本轮不动。
- 不改 `handoff-spec.md` 的 `02_SESSION_HANDOFF.md` 格式契约，不改双台账结构与 `state-index.json` 路由公式，不改 `handoff.py` / `state_ledger.py` 的行为。
- 不改冷启动一致性自检那 5 条不变量的判定口径（它们是台账↔产物↔交付↔证据对账，与读序是两件事）。
- 不动 `/butler:progress`（R4）、`/butler:loop`（R5）、旧 inbox 全链（R8）、根布局改名与迁位（R9）。
- 不改升级器动作类型（R14），不写 `migrations/v4.0.0.md`（R15）；本轮只登记「改了部署入口模板、下个发布版必须含 `[regen-entrypoints]`」。
- 不切版、不发布。

**影响面清点（预估 12 份文件）**

- 规则真源 3：`context-persistence.md`、`handoff-spec.md`、`Coder/README.md`
- 入口与模板 3：`AGENTS.md`、`templates/AGENTS.md.template`、`templates/CLAUDE.md.template`
- 规则卡 1：`templates/rule-card.md`（只改分工指针，不放读序块——理由见下）
- 机器侧 4：`tools/context-budget/context_budget.py` 及其测试、`scripts/verify-codex-foundation.sh`、`Coder/domain-glossary.md`（若新增术语则条数变，机器校验的精确条数同步改）
- 台账与登记 1：`.ai/MILESTONE.md`（R2 收口与 `[regen-entrypoints]` 登记）

## Open Questions / Risks

- **待定 · 读序块要不要进 rule-card**：rule-card 是注入到部署项目 `CLAUDE.md` 顶层的那份浓缩规则，两份入口模板都通过 `{{RULE_CARD_CONTENT}}` 引它。读序块若放进 rule-card，两份模板自动都有、无需各投一次；但 rule-card 现在 13457 字节，是**每次会话必进上下文**的东西，读序块塞进去等于给所有项目的每次会话加成本。倾向是**不放 rule-card、各模板独立投一次**——两份模板本来就各有自己的「会话起始」章节位置（Codex 侧有、Claude 侧要新建），投影校验能保证它们一致，代价是多一处投影点。这条我打算按倾向做，P3 定稿前若你有不同意见可以推翻。
- **风险 · 读序块进 Claude 入口是净新增上下文**：这是 Claude 宿主第一次拿到读序，不是改写而是新增。L0 的实测是 656 字节 / 约 234 token，读序块步骤更多、约束更细，估计要 800–1200 字节。需要在 P3 给出明确上限并在 P5 实测，不能让它无声膨胀。参照 L0 上限是 1600 字节 / 18 非空行 / 4 个指针。
- **风险 · 拆 `verify-codex-foundation.sh` 的列表可能拆掉真覆盖**：那张 9 项列表虽然是抄的，但它确实在守「AGENTS.md 的读序顺序没被改乱」。换成投影校验后，守的变成「四处逐字节相同」——如果真源本身被改错了，投影校验只会说「四处一致」，不会说「顺序不对」。这是覆盖面的**真实变化**，不是等价替换。P3 要明确：顺序正确性由谁守（倾向是给读序块加结构断言，比如步骤编号连续、每步必须含一个 `.ai/` 路径），不能只靠一致性。
- **风险 · 已部署项目要重新生成入口才拿得到新读序**：改了两份模板，老项目在跑 `/butler:upgrade` 之前仍是旧入口。这是已知滞后，跟 ITER-0111 改 rule-card 时同一性质；本轮只负责登记 `[regen-entrypoints]`，实际配方归 R15。
- **待定 · 读序真源该 5 步还是展开**：真源现在 5 步（抽象、每步一个语义阶段），butler 仓 `AGENTS.md` 是 7 步（展开、每步一个文件）。投影的消费者是 AI 宿主不是人，展开式更可直接执行；但步数一多，投影块体量就上去，跟上一条的预算风险冲突。倾向是**按语义阶段分步、每步内列具体文件**，既保住可执行性又压住步数。P3 定稿。
- **风险 · 改读序等于改所有会话的起手式，改错的代价是全局的**：读序是每个新会话第一件事，写坏了不会当场报错，只会让后续判断都建立在错的上下文上。本轮没有运行时观测能证明宿主真按读序走了——这跟 ITER-0111「证明不了宿主真的按 L0 分层读了」是同一个缺口，确定性数据同样要等 R11 的使用监视器。验证阶段要如实记这一条，不能因为四处字节一致就写成「读序生效了」。
