# TECH_PLAN — ITER-0043（工程原则增量吸收）

# Goal
- 支撑 AC1–AC9：把 3 条真增量（Trade-off 普适化 / KISS 判据 / 伪需求质询）落进 4 候选文件中**实际需要的 3 个**，DRY 不双写、不扩部署面、说人话。

# Files / Modules to Change
- `Coder/00_System_Prompt/identity.md §3.1` — 加 Trade-off 价值（新 bullet）+ KISS 判据（并入「可解释性高于魔法」条）。支撑 AC1、AC3。
- `Coder/00_System_Prompt/presentation-protocol.md §5` — 单方案口径松绑：给方案就交代取舍/代价。支撑 AC2。
- `Coder/20_Workflow_Lifecycle/lifecycle.md P1 Analysis` — 「AI 必须回答」加伪需求质询条 + P1 质询 vs P2 锁定时序消歧句。支撑 AC4。
- **不改** `concept-schema.md`（见 Design Decisions 决策 1）。

# Interface / Contract
- 无接口 / 数据契约变更。纯规则正文（自然语言口径）增补，不涉及字段、hook、命令、schema 结构。

# State / Boundary
- 只改上述 3 文件的指定小节正文；其余全文一字不动。
- 明确不在范围：`rule-card.md`、`CLAUDE.md.template`、`templates/hooks/**`、四件套 schema 字段结构、命令语义、P1–P5 状态机流转、`VERSION`、`references/`。

# Design Decisions
- **决策 1：③ 只落 `lifecycle.md P1`，不碰 `concept-schema.md`（关 Open Question 1）**。理由：伪需求质询是 P1 的**行为姿态**（AI 在分析时该做什么），真源在 `lifecycle P1「AI 必须回答」`；`concept-schema` 管的是产物 `CONCEPT.md` 的字段模板，质询结论天然落在既有 `Open Questions` 字段、无需新增口径。只落一处即满足 AC5「能只落一处则只落一处」，避免双写。
- **决策 2：② KISS 判据并入「可解释性高于魔法式实现」条，不单列（关 Open Question 2）**。理由：二者同源（都反对「聪明但难懂」），并入更内聚、不给 §3.1 堆第 6 条口号。满足 AC3「并入或紧邻、不新增独立小节」。
- **决策 3：① Trade-off 作为 §3.1 新增独立 bullet**（与并入的 ② 不同）。理由：「交代取舍/技术债」是一条独立价值主张（关于「怎么提方案」），与现有 4 条（关于「怎么实现」）平级并列最自然；且 `presentation §5` 的松绑是它在对话呈现层的落地,两处一呼一应（哲学层立价值 + 呈现层给动作）。
- **决策 4：presentation §5 松绑用「加约束」而非「改骨架」**。只在「单一方案」那条补「仍须交代取舍/代价」，不动 §5 表格固定列与 §9 标准骨架样例——满足 AC2「不破坏骨架/样例一致性」。

# Execution Steps
- [ ] T1 改 `identity.md §3.1`：加 Trade-off bullet + KISS 判据并入「可解释性」条 → AC1、AC3
- [ ] T2 [P] 改 `presentation-protocol.md §5`：单方案条补「仍须交代取舍/代价」+ 回指 `identity §3.1` → AC2
- [ ] T3 [P] 改 `lifecycle.md P1`：加伪需求质询条 + 时序消歧句 → AC4
- [ ] T4 收口核对：`git diff` 核影响面（AC7）、逐条比对无双写（AC6）、读新增正文核说人话+措辞（AC8）、确认 concept-schema 未改（AC5）
- [ ] T5 P5 起 fresh-context 子 agent 独立复核逐 AC（AC9）

# Verification Plan
- AC1/AC3：读 `identity §3.1` 核 Trade-off 条 + KISS 判据落位、风格一致、未堆口号。
- AC2：读 `presentation §5`+§9 核松绑且样例未破。
- AC4：读 `lifecycle P1` 核质询条 + 时序消歧句。
- AC5：`git diff --quiet Coder/20_Workflow_Lifecycle/concept-schema.md` 应无输出（未改），并在 VERIFY 说明只落 lifecycle 的理由。
- AC6：新增文本逐条比对 CONCEPT 减法表，确认非已有 10 条的重复。
- AC7：`git diff --stat` 仅 3 文件；`git diff --quiet` 核 rule-card / CLAUDE.md.template / hooks / schema 字段 / VERSION 全 clean。
- AC8：读新增正文核说人话三条 + 「必须/不得/应」措辞。
- AC9：fresh-context 子 agent spec-only 逐 AC 复核，无 refute。

# Risks / Open Questions
- 两个 Open Question 已在本阶段关闭（决策 1、2）。
- 残余风险：改 `identity`（哲学底座、所有任务读）影响面无形——靠 AC9 独立复核 + AC6 DRY 守恒 +「融入不堆砌」三重兜底。
- 判 MINOR·v2.3.0，切版待放行（不在本迭代）。
