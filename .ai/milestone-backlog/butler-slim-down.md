# Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器

候办键: butler-slim-down
候办状态: deferred

## 触发这个方向的真实原因（2026-08-17）

本轮 `/grill-me` 对 butler 「实用性 / 完善性」做了一次深度 audit。作者本人对 34 项命令 / 帮手 / 工具做了 A/B/C/D 使用度标注，并按顺序回答了三轮针对性追问。结论按证据链收敛为四类结构性问题——

**一、面向人的「全貌管理」设计从未被人消费**

`.ai/project/` fold 目录（capabilities.md / frontier.md / architecture.md / invariants.md / fold-state.json）的设计目标是「让下次冷启动的 AI 快速理解项目现在什么形态」，同时作者本人可读可校准。真实状态是：作者亲口确认 fold 文件**一次也没读过**（"这个东西设计出来就是给 AI 看的"），负责校准的 `drift-check` 帮手几乎不触发（B），且 fold 文本本身也是 AI 写的——**AI 自己写、AI 自己校（如果校）、AI 自己读，人在旁边观赏**。

已知失真在实盘上：MILE-0014 已被作者评估为「概念空缺真实、当前设计不符合预期」，但 capabilities.md 仍挂着「已交付 R1-R5」、frontier.md 仍挂着「MILE-0014 已关闭」。**幻觉挂了三周没被发现**。

追问「过去 6 个月有没有任何一次决策是因为读了 capabilities/frontier 才做出/改变」，作者回答**举不出**。

**二、死码残留**

标 C（从没主动用过）：`/butler:inbox`、`/butler:loop`、`tools/inbox/`；标 D（甚至不记得）：`tools/mile0009-e2e/`。其中：

- **inbox 全链未投入生产**：`/butler:inbox`、`tools/inbox/`、`inbox-schema.md`、`inbox-workflow.md` 一整条链自 MILE-0009 起从未在实际迭代中被使用。真实需求录入靠对话直接进 `/butler:milestone` / `/butler:ideation` / `/butler:prd`。
- **`/butler:loop` 从不用但 backlog 挂着「升级收敛引擎」候办**：作者在升级一个自己一次都没用过的功能。
- **`/butler:preference` 开了不工作**：作者亲口承认。反哺回路空转（隐私总开关允许后，实际未观察到反哺影响 P2/P3 提案排序）。
- **`/butler:progress`（B）**：作者查进度直接读 `MILESTONES.md`，progress 命令做的是「给别人看的展示」，但没有别人。

**三、真实缺口未填**

- **闪念口缺失**：作者的真实需求录入路径是「先 ideation 讨论 → 暂时不写的存 milestone-backlog → 想执行时 milestone start」，但 ideation 之前没有轻量「3 秒 dump 一句话」的口子。inbox 当前设计（origin/ + INBOX.md + SRC-NNNN + scanner + 双 SHA-256）**用 100 行需求做出 10,000 行工程**，对不上真实需要。
- **backlog 假设过强**：`.ai/milestone-backlog/` 假设所有条目都是里程碑级，但 ideation 讨论出来的东西更像"候选实现的需求"，粒度可能只是一个迭代。当前把两种状态搅在一起。
- **hook 拦截无审计追溯**：PreToolUse 每次拦截只在当次响应打印，无持久化。作者已无法回忆 Claude 工作目录在 project root 下一级时被拦的具体场景，导致真实摩擦点无法定位、无法回归。
- **仓根 meta-work 无逃生舱**：写 README/CHANGELOG/.gitignore/VERSION 等仓根 meta 文件时会被 phase_gate 拦（无 active iteration 或 iteration 未覆盖该路径），日常摩擦。
- **`deliveries/` 目录使项目根臃肿**：应迁 `.ai/deliveries/`。

**四、无 usage instrumentation**

现有命令 / 帮手 / 工具无使用计数、无最后调用时间戳、无 A/B/C/D 内建标注机制。这次要靠作者手工回忆 34 项才能做出淘汰判断。**淘汰机制缺失是当前形态只加不减、backlog 靠"应该做"直觉长的根因**。

**根因概括**：Butler 是「面向 AI 的规则仓 + 唯一用户是设计者本人」这个组合下**过度设计与自嗨的自然产物**。本 milestone 的所有动作都是校准这个失衡。

## 范围评估

### In Scope（版本级）

- 退役 `.ai/project/` 整个 fold 目录、`knowledge-fold` 帮手、`drift-check` 帮手。冷启动读序改为「debt.md + handoff + ITERATIONS/MILESTONES 台账」，不再依赖任何面向人的项目全貌摘要。
- 砍 `/butler:progress` 命令及其真源 / skill / registry 条目 / docs/workflows.md 引用 / rule-card 引用。
- `/butler:loop` 命令降级：保留代码路径但撤 milestone-backlog 「升级收敛引擎」候办，命令不再演进；R3 根据 usage 数据决定是否彻底砍。
- `/butler:preference` 断言实验：设计并执行「一次反哺是否影响 P2/P3 提案排序」实验；无影响 → 全套退役；有影响 → 修回路并写清楚触发条件。
- 重造 inbox 三层：`INBOX` (`.ai/INBOX.md`) → `BACKLOG` (`.ai/backlog/<slug>.md`，带规模字段 milestone/iteration/undecided) → `ACTIVE`。新命令 `/butler:inbox add | list | handle`。真源改写。
- 根 layout 三件整理：`.ai/milestone-backlog/` → `.ai/backlog/`、`deliveries/` → `.ai/deliveries/`、`origin/` 目录退役。全仓引用一次性更新。
- 退役 `tools/inbox/` + SRC-NNNN + SHA-256 认亲 + scanner。
- 新增 hook 拦截审计日志 `.ai/.hook-blocks.log`（追加式、gitignore、有限大小）。
- 新增仓根 meta-work 逃生舱：白名单 README/CHANGELOG/.gitignore/VERSION/LICENSE 等文件写入免 phase_gate 与 workspace-scope。
- 新增 usage instrumentation：每个 CLI 入口写 last-invoked 到本地状态（gitignore、非 shared repo），`tools/usage-report/` 提供 `usage report --since 90d` 命令。
- evidence 消费链降维：goal.py 仍是唯一消费者，砍或收窄 `tools/verification-evidence/` 的 record archive 逻辑。
- migrations/v4.0.0.md：完整迁移配方，含 `[remove]`（fold / progress / inbox scanner / origin/ / knowledge-fold / drift-check）、`[move]`（deliveries/ → .ai/deliveries/）、`[rename]`（milestone-backlog/ → backlog/）、`[add]`（hook 审计日志 / meta 逃生舱 / usage instrumentation）等 typed 步骤。
- 切版 v4.0.0（MAJOR），CHANGELOG 聚合发布，audit 中识别的所有 debt 一次性清账。

### Out of Scope（版本级）

- **不重造项目全貌摘要**：`.ai/project/` 砍了就是砍了，本 milestone 不设计任何替代品；debt.md + handoff + 台账即冷启动全部依据。
- **不做兼容期软链**：`deliveries/` 迁移直接 BREAKING，不做「v4.0.0 建软链、v5.0.0 再删」的两阶段兼容。
- **不做隐式 inbox scanner**：新 inbox 三层严格用户主动 `add`；不扫 `origin/`、不扫对话历史。origin/ 直接退役，外部文档引用改走 `.ai/references/`。
- **不重写 evidence 消费方**：goal.py 仍是唯一消费者；本 milestone 不给 evidence 加人读摘要或看板（承认「evidence 只是 goal.py 的机器中间件」）。
- **不做 usage 反哺决策自动化**：usage report 只呈现数据，是否淘汰仍由作者按季度手工判断；不做自动降级 / 自动砍。
- **不重构 preference 数据回路**：断言实验若结论是「反哺无效」→ 全套退役；不做「先大改再验」。
- **不动 MILE-0014 / MILE-0015 已交付的骨架**：Decision Map / Decision Work / Decision Promotion / 领域合同工具仍保留，本 milestone 不重设计它们（那是另一个 milestone 的事）。
- **不做 backlog 迁移之外的 `.ai/` 结构大改**：`.ai/deliveries/` 采用扁平布局（跟现在 `deliveries/` 一致），不新分 iteration 子目录。

### 关键交付目标

- 冷启动读序不再涉及 `.ai/project/`；capabilities/frontier/architecture/invariants 从仓库消失。
- `/butler:progress` 从 registry / docs/workflows.md / rule-card / 命令目录全部消失；相关 skill 与真源退役。
- 闪念 → 孵化 → 执行三层链路可跑通一次 dogfood：作者用 `/butler:inbox add` 记录一条闪念，后续 `/butler:inbox handle` 分流到 ideation（成型后落 backlog）或直接 backlog，最后从 backlog 走 milestone start / iteration start 进入执行。
- 根目录只剩必要项：`Coder/` / `tools/` / `templates/` / `scripts/` / `plugins/` / `docs/` / `migrations/` / `workflows/` / `.agents/` / `.ai/` / `CLAUDE.md` / `AGENTS.md` / `README.md` / `CHANGELOG.md` / `VERSION` / `LICENSE` / `SECURITY.md` / `CONTRIBUTING.md` / `HUMAN_GUIDE.md` / `communication-style.md` / `.claude/` / `.github/` / `.gitignore` 等标准配置。`deliveries/` / `origin/` 从根消失。
- `.ai/.hook-blocks.log` 追加式记录 hook 拦截；作者可事后追根因回归 Q7 类摩擦。
- 仓根 meta 文件（README/CHANGELOG/.gitignore/VERSION/LICENSE 等）在无 active iteration 时也可直接写入，不再被 phase_gate 拦。
- `usage report --since 90d` 输出全部 CLI / 帮手 / 工具的最后调用时间戳，A/B/C/D 分档由数据自动生成。
- `preference` 断言实验有结论并落到 debt.md 或直接退役。
- v4.0.0 切版发布，CHANGELOG 聚合三 R 全部产出。
- audit debt 清账完成：debt.md 只剩长期挂账（本次 audit 遗留项全部清零）。

## 理解阐释

Butler 走到 v3.5.1，规则文件 30+、驻留工具 20+、命令 10+、帮手 4 个、支持三宿主。规模上已经达到"个人规则仓的极致"，但增长机制是**只加不减**——每次 audit 都发现有能力躺着不用、有 fold 在自转、有工具在生成没人看的产出。根本原因是缺淘汰机制：没有 usage 数据，就没有淘汰依据；没有淘汰依据，backlog 就只能靠"应该做"的直觉长，功能只增不减，认知负担线性爬升。

本 milestone 的动作可分三类。**先破**——退役已确认零消费/零校准的机构（fold + drift-check + knowledge-fold + progress + 旧 inbox + origin/），直接瘦身 20% 起步，同时把 `.ai/` 与项目根 layout 一次性理顺（backlog 改名 + deliveries 迁进 `.ai/`）。**再立**——填补 audit 中识别的真实缺口（闪念口 / hook 拦截审计 / 仓根 meta 逃生舱），这些是**真需求过去没被识别**、不是"再加一层规则"。**最后装监视器**——加 usage instrumentation，让下一次 audit（以及未来的所有 audit）有确定性数据可查，Butler 从此**具备结构性淘汰能力**，不再只加不减。

关键判断：**MILE-0014 / MILE-0015 已交付的骨架保留**——Decision Map / Decision Work / Decision Promotion 概念上填了真实空缺（探索期结构化决策），只是当前设计需要在未来 milestone 里迭代形态；本 milestone 不动它们。**preference 的处置留断言实验为准**——不做提前判死；实验设计上要确保「反哺链是否影响提案排序」是可检验、可复现的，无影响再退役。

版本影响：v4.0.0（MAJOR）。破坏性变更清单包括 fold 目录消失、progress 命令消失、drift-check / knowledge-fold 帮手消失、`.ai/milestone-backlog/` 改名、`deliveries/` 从根迁到 `.ai/deliveries/`、origin/ 消失、旧 inbox scanner 消失。为已部署项目（含 butler 自身 dogfood）提供完整 migration 配方，无兼容期软链。

## 拆分路线图

预计 3 个路线项、13 个迭代承接；实际迭代号在启动时绑定。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 止血：砍 fold + 死码。退役 `.ai/project/`、`knowledge-fold` / `drift-check` 帮手、`/butler:progress` 全链、`/butler:loop` 降级 + 撤「升级收敛引擎」候办；冷启动读序改造；模板与 migration 收尾；CI 全绿 | — | planned |
| R2 | 重造：inbox 三层 + 根 layout 整理 + hook 逃生舱。inbox 三层数据契约与真源、`/butler:inbox add/list/handle` CLI、根 layout 三件整理（backlog 改名 + deliveries 迁 `.ai/` + origin/ 退役 + 全仓引用一次性更新）、v4.0.0 migration 配方与已部署项目升级回归、hook 拦截审计日志、仓根 meta 逃生舱 | — | planned |
| R3 | 治根：装监视器 + preference 断言 + evidence 降维 + audit debt 清账 + v4.0.0 切版。usage instrumentation 全 CLI 接入 + `usage report` 工具、preference 反哺断言实验与处置、evidence 消费链降维、`/butler:loop` 最终处置、debt.md 收尾、`chore(release): v4.0.0` 聚合发布 | — | planned |

R1 内部预计 4 个迭代、R2 内部预计 5 个迭代（含根 layout 大整理）、R3 内部预计 4 个迭代。三个 R 严格串行：R1 决定冷启动读序，R2 的新 inbox 与根 layout 依赖新读序，R3 的 instrumentation 才能验证 R1/R2 到底砍对没。iteration 号在开启时按台账连续分配，本 brief 不预占。

## 范围演进记录

- 2026-08-17：由本轮 `/grill-me` audit 收敛入候办。基于作者对 34 项能力的 A/B/C/D 使用度标注 + 三轮针对性追问 + Q20「过去 6 个月是否因读 fold 做过决策」回答「举不出」，锁定 (c) 止损方案（砍 `.ai/project/` fold 机制）。同轮采纳 `deliveries/` 迁 `.ai/deliveries/` + 不留兼容期软链 + `.ai/deliveries/` 扁平布局的边界决策。当前 MILE-0015 仍 active（R1-R4 已 closed、R5 挂着），按单 active 约束先入待办；MILE-0015 R5 按原计划继续，收口后再从待办提升本条为正式 MILE-NNNN。
