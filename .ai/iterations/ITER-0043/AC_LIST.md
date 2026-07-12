---
状态: ack-frozen
ACK 日期: 2026-07-12
prd_version: —
---

# Goal
- 把外部工程宪法的 3 条真增量（Trade-off 意识普适化 / KISS 可操作判据 / 剥离伪需求-MVP 质询）落进 butler 对应规则文件，补齐哲学层与 P1 分析口径，且不双写已有原则、不扩部署面。

# In Scope
- `identity.md §3` 增 Trade-off 价值 + KISS 判据。
- `presentation-protocol.md §5` 代价列口径松绑。
- `lifecycle.md P1` 增伪需求质询姿态（含与「固定需求锁定」时序的消歧）。
- `concept-schema.md` 至多一句 P1 质询口径 / 指针（避免与 lifecycle 双写）。

# Out of Scope
- 已有的 10 条宪法原则一律不重写（DRY）。
- 不动 `rule-card.md` / `CLAUDE.md.template`（不扩部署面）、不改任何 hook、四件套 schema 字段结构、命令语义、核心 P1–P5 状态机流转。
- 不建 `references/`（理念类输入已消化）。
- 不切版（判 MINOR，v2.3.0 发布待放行）。

# Acceptance Checklist
- [ ] AC1: `identity.md §3.1` 新增一条「Trade-off 意识」价值——任何方案都须交代取舍成本 / 潜在技术债，与现有 4 条价值同风格融入（非硬凑列表）。
- [ ] AC2: `presentation-protocol.md §5` 代价口径松绑——从「仅 ≥2 方案对比时列代价」扩为「给出任何方案都须交代取舍/代价」，且不破坏 §5 表格骨架与 §9 标准骨架样例的一致性。
- [ ] AC3: `identity.md §3` 补 KISS 可操作判据「复杂到一句话讲不清就该重构」，并入或紧邻现有「可解释性高于魔法」，不新增独立小节堆砌。
- [ ] AC4: `lifecycle.md P1 Analysis` 的「AI 必须回答」新增一条主动质询——需求里有无伪需求 / 低 ROI 项、是否该提替代（MVP）；正文显式写清质询在 P1、与 P2 冻结后的「固定需求锁定」时序不同、不冲突。
- [ ] AC5: 若 ③ 同时触及 `concept-schema.md`，只加一句口径或指针、不与 `lifecycle` 重复表述；能只落一处则只落一处。
- [ ] AC6: DRY 守恒——3 条均为 CONCEPT 已核的真增量，不与 butler 已有原则（奥卡姆/YAGNI/DRY/高内聚低耦合/极简/注释 Why-not-What/边界异常）重复；已有 10 条正文一字未加。
- [ ] AC7: 最小影响面守恒——`git diff` 核对：改动仅落在 `identity` / `presentation-protocol` / `lifecycle` / `concept-schema` 四文件正文；`rule-card.md`、`CLAUDE.md.template`、`templates/hooks/**`、四件套 schema 字段结构、`VERSION` 全部无改动。
- [ ] AC8: 新增正文守 `artifact-style.md §2` 说人话三条 + 不啰嗦；措辞用「必须/不得/应」（butler 规则写作风格）。
- [ ] AC9: opt-in 独立复核通过——验证者≠实现者、fresh-context、逐 AC 核对，无 refute 阻断（`identity` 是哲学底座，改它必过独立复核）。

# Verification Method
- AC1: 读 `identity.md §3.1` 核新价值条目存在、语义正确、风格一致。
- AC2: 读 `presentation-protocol.md §5`+§9 核口径已松绑且样例未破。
- AC3: 读 `identity.md §3` 核 KISS 判据落位、未另起冗余小节。
- AC4: 读 `lifecycle.md P1` 核质询条 + 时序消歧句存在。
- AC5: 读 `concept-schema.md` 核（若改）单句无双写；未改则说明只落 lifecycle 的理由。
- AC6: 逐条比对新增文本 vs CONCEPT 减法表，确认无重复；`git diff` 核已有条目未动。
- AC7: `git diff --stat` + 对边界文件 `git diff --quiet` 核影响面。
- AC8: 读新增正文核说人话三条 + 措辞。
- AC9: 起 fresh-context 子 agent 独立复核（spec-only 逐 AC）。

# Open Questions / Risks
- ③ 落点（lifecycle 单点 vs lifecycle+concept-schema）与 KISS 判据（并入 vs 单列）在 P3 定；已在 AC3/AC5 用「并入优先/只落一处优先」约束倾向，降低发散。
- 风险：改哲学层（`identity`）影响面无形（所有任务读它）——用 AC9 独立复核 + AC6 DRY 守恒 + AC1/AC3「融入不堆砌」共同兜底，防止哲学层膨胀成口号堆。
