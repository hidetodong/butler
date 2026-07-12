> 分流: 完整 | 命中升级信号: 改规则底座（identity 哲学层）、跨 ≥3 规则文件 | 2026-07-12

# 一句话
- 用户给了一份外部「工程宪法」prompt（奥卡姆/KISS/YAGNI/DRY/高内聚低耦合/Trade-off + 需求质询 + 极简输出），想吸收有用的规则。
- 先用**奥卡姆剃刀做减法**：13 条里 butler 已有 10 条，照搬就是违反它自己的 DRY——只把 **3 条真增量**吸收进哲学层与 P1 口径。这次迭代本身就是「对宪法用宪法」的示范。

# Goal
- 补齐 butler 哲学层（`identity`）与 P1 分析口径的 3 处短板，来源是外部工程宪法里 butler 尚缺 / 偏弱的原则：
  1. **Trade-off 意识普适化**——任何方案都要交代取舍成本 / 技术债，不只在「≥2 方案对比」时。
  2. **KISS 可操作判据**——给「可解释性高于魔法」补一把落地尺子：复杂到一句话讲不清，就该重构。
  3. **剥离伪需求 / MVP 质询**——P1 主动质疑需求合理性、指出低 ROI 项、提替代，而非被动接收。

# Current Understanding
- **减法结论（已核证据）**：
  - 已有、不吸收（照搬=双写）：奥卡姆/YAGNI（`implementation-discipline §2` 最小实现阶梯）、DRY/SSOT（butler 骨架 + `identity §1`）、高内聚低耦合（`identity §3.2` + `architecture-overview`）、极简/结构化/表格（`presentation-protocol §3–§5` + `artifact-style §2`）、代码注释 Why-not-What（`review-standard.md:23` 已有）、边界/异常（AC/verify + testing-strategy）、方案对比表格（`presentation §5`）。
  - 真增量、值得吸收（就这 3 条）：见 Goal。
- **3 条缺口的证据**：
  1. Trade-off：`presentation §5` 只在「≥2 方案对比」时强制列「代价·取舍」；`ideation` 提过技术债——但**单一方案时不强制讲缺点**，`identity` 哲学层也没把「交代妥协成本」立为价值。
  2. KISS 判据：`identity §3.1` 有「可解释性高于魔法」的**精神**，无**判据**（多复杂算复杂）。
  3. 伪需求质询：`lifecycle P1「AI 必须回答」`偏「理解目标/约束/影响面」，是被动理解；`ideation` 是发散不是质询。主动剥离伪需求的姿态 butler 弱。
- **落点方向**：① → `identity §3` + `presentation §5`；② → `identity §3`；③ → `lifecycle P1` +（可能）`concept-schema`。
- **与「固定需求锁定」的关系**：③ 的质询发生在 **P1**（理解阶段），「固定需求锁定」是 **P2 ACK 冻结之后**的纪律——时序不同、不冲突；正文须写清，避免 AI 把「P1 该质疑」误读成「冻结后还能推翻」。

# Constraints
- **DRY 铁律**：只加 3 条真增量，已有的 10 条一字不加、不换个说法重写。
- **最小实现 + 不扩部署面**：改动只限规则正文（`identity` / `presentation-protocol` / `lifecycle` / `concept-schema`）；**不动** `templates/rule-card.md`、`templates/CLAUDE.md.template`、任何 hook、四件套 schema 字段结构、命令语义。
- **守既有分层**：3 条各归其位——价值观进哲学层、呈现口径进 presentation、P1 姿态进 lifecycle/concept-schema，不混层。
- **融入不堆砌**：加进 `identity §3` 要与现有 4 条价值同风格，不是硬凑列表。
- **输入不落 references**：本次输入是对话粘贴的「理念/方法论」文本，非需逐字保真回溯的权威规格（按 ITER-0042 内容路由：理念类已消化即用），不建 `references/`。
- **切版待放行**：判 MINOR（兼容的规则正文原则增强），本迭代不切版；发布聚合待用户放行（预留 v2.3.0）。

# Impact Scope
- 改动（4 文件规则正文）：
  - `Coder/00_System_Prompt/identity.md §3` — 加 Trade-off 价值 + KISS 判据。
  - `Coder/00_System_Prompt/presentation-protocol.md §5` — 代价列口径松绑（给方案就交代取舍）。
  - `Coder/20_Workflow_Lifecycle/lifecycle.md P1 Analysis` — 「AI 必须回答」加一条伪需求质询。
  - `Coder/20_Workflow_Lifecycle/concept-schema.md` — 编写口径补伪需求剥离一句（待 P3 定是否需要，避免与 lifecycle 双写）。
- 明确不影响：`templates/rule-card.md`、`templates/CLAUDE.md.template`、`templates/hooks/**`、四件套 schema 字段结构、`.ai/` 契约、命令语义、核心 P1–P5 状态机（只在 P1 加质询口径、不改阶段流转）、`VERSION`。

# Project Type / Active Profiles
- butler 规则仓库自身 dogfood——编辑规则本身，非用规则开发软件。
- 无 Domain / Stack Profile 命中；按通用 SOP + 仓库 `CLAUDE.md` 编辑约定（不破坏分层 / 产物链 / 隐式依赖、模板单一来源、audience 标注、措辞用「必须/不得/应」）推进。

# Open Questions
- ③ 的落点：只落 `lifecycle P1`，还是 `lifecycle` + `concept-schema` 各一句？倾向只落 lifecycle（P1 姿态的真源）、concept-schema 至多一句指针，避免双写——P3 定。
- KISS 判据：并入现有「可解释性高于魔法」那条，还是单列一条？倾向并入强化（少一条、更内聚）——P3 定。
- 是否要 opt-in 独立复核？倾向要（`identity` 是哲学底座，改它值得验证者≠实现者把关）。
