# 工程原则增量吸收：把外部「工程宪法」减到骨头，只吸收 3 条真增量

> ITER-0043 · 独立迭代（无所属里程碑）· 收口 2026-07-12 · dogfood butler 自身 · 独立复核 APPROVE-with-nits（P5 验证者≠实现者）· 不切版（判 MINOR·v2.3.0，发布待放行）

## 本次交付目标

- 用户提供了一份外部「工程宪法」prompt（奥卡姆 / KISS / YAGNI / DRY / 高内聚低耦合 / Trade-off / 需求质询 / 极简输出等约 13 条），希望吸收其中有用的规则。
- 直接照搬会**违反这份宪法自己的 DRY 原则**——butler 早已覆盖其中大半。本次交付的核心动作是**先做减法**：逐条比对后判定 13 条里 butler 已有 10 条，只有 3 条是真增量，把这 3 条各归其位地落进规则。这次迭代本身就是「对宪法用奥卡姆剃刀」的一次示范。

## 已完成内容

- **减法核证（不落文件、落在决策）**：已有、不吸收的 10 条各有真源——奥卡姆/YAGNI（`implementation-discipline §2` 最小实现阶梯）、DRY/SSOT（butler 骨架 + `identity §1`）、高内聚低耦合（`identity §3.2`）、极简/结构化/表格（`presentation §3–§5` + `artifact-style §2`）、代码注释 Why-not-What（`review-standard §2.3`）、边界/异常（AC/verify）。照搬即双写，一律不加。
- **增量①·Trade-off 意识普适化**：`identity.md §3.1` 新增第 5 条价值「任何方案都须交代取舍成本与潜在技术债——没有免费的架构」；`presentation-protocol.md §5` 把「代价·取舍」从「仅 ≥2 方案对比时列表格」松绑为「给任何方案都须交代取舍/代价、不得只报优点」。哲学层立价值 + 呈现层给动作，一呼一应。
- **增量②·KISS 可操作判据**：`identity.md §3.1`「可解释性高于魔法」条尾并入一把落地尺子——「复杂到一句话讲不清的方案就该重构（KISS）」。补齐旧口径「只有精神、没有判据」的缺。
- **增量③·剥离伪需求 / MVP 质询**：`lifecycle.md` P1 Analysis「AI 必须回答」新增第 3 问（有没有伪需求 / 低 ROI / 该缩到 MVP 或提替代），把 P1 从被动理解升级为主动质询；并加一段消歧，写清质询在 P1、与 P2 冻结后的「固定需求锁定」不冲突。

## 关键变更 / 用户可感知变化

- **提方案的姿态变了**：AI 今后给任何方案（哪怕只有一个）都必须交代代价与技术债，不再只报优点——Trade-off 从「多方案对比才有」变成「哲学层常驻价值」。
- **P1 会主动质疑需求**：给需求时 AI 会先问「这里面有没有伪需求、投入产出比过低的部分、能不能缩到 MVP」，而不是照单全收；但这只发生在 P1（冻结前），P2 ACK 之后仍守「固定需求锁定」——不会出现「冻结了还乱推翻」。
- **哲学层多了两把尺子**：KISS「一句话讲不清就重构」和 Trade-off「没有免费的架构」进了 `identity`，所有任务读它时都受这两条约束。
- **不用这些的人无感**：改的是既有规则正文的口径增强，无新命令、无新产物、无部署面变化。

## 高层影响范围

- 规则正文（3 文件，6 insertions / 2 deletions）：`Coder/00_System_Prompt/identity.md §3.1`、`Coder/00_System_Prompt/presentation-protocol.md §5`、`Coder/20_Workflow_Lifecycle/lifecycle.md` P1。
- 没碰（守 DRY + 最小影响面）：`concept-schema.md`（③ 决策只落 lifecycle 一处）、`templates/rule-card.md`、`templates/CLAUDE.md.template`、`templates/hooks/**`、四件套 schema 字段结构、命令语义、核心 P1–P5 状态机流转、`VERSION`——逐个 `git diff --quiet` 全 clean。**不切版**。

## 验证方式与结果摘要

- **9 项验收（AC1–AC9）全过**，AC1–AC8 均 **auto·可靠**：改动落位经 `git diff` 逐处核对、影响面守恒经边界文件 `git diff --quiet` 机器核（仅 3 规则文件正文变更）、DRY 守恒经逐条比对减法表 + 全仓 grep（伪需求质询除新行外零命中）。
- **独立复核 APPROVE-with-nits**（fresh-context 子 agent、验证者≠实现者、只读、对抗式）：9/9 AC confirm、0 refute、无 Must-Fix。对抗点全过——DRY 不双写（增量与 `implementation-discipline` YAGNI 属不同海拔 P1 vs P4）、影响面守恒、AC5 决策合理（质询是 P1 姿态非 CONCEPT 字段）、AC4 时序与 `iteration-schema §5.2/§5.3` 一致（「擅自」二字精准无矛盾）。1 Should-Fix（措辞「要→须」）+ 1 Nit（MVP 加中文注解）已顺手改，1 Nit（技术债定义）判同句已点明义、不改。

## 已知剩余风险 / 延后事项

- **改哲学底座影响面无形**：`identity` 被所有任务读，加价值有膨胀成口号堆的风险——已靠独立复核 +「融入不堆砌」（并入而非另起小节、与现有价值同段）+ DRY 守恒三重兜底，本轮确认无膨胀；后续新增哲学条目仍须守同一底线。
- **切版待放行**：判 MINOR（兼容的规则正文原则增强），本迭代不切版；聚合发布待用户放行（预留 v2.3.0）。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0043/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动产物：`Coder/00_System_Prompt/identity.md §3.1`、`Coder/00_System_Prompt/presentation-protocol.md §5`、`Coder/20_Workflow_Lifecycle/lifecycle.md` P1 Analysis
- 减法对照的既有真源：`Coder/30_Quality_Gate/implementation-discipline.md §2`、`Coder/30_Quality_Gate/review-standard.md §2.3`、`Coder/20_Workflow_Lifecycle/artifact-style.md §2`、`Coder/20_Workflow_Lifecycle/iteration-schema.md §5`
