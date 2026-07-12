# 01_CHANGELOG

> 活跃迭代 ITER-0043（工程原则增量吸收）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度。收口时归档至 `iterations/ITER-0043/CHANGELOG.md`。

## EDIT

- `Coder/00_System_Prompt/identity.md` §3.1 目标优先 — 新增第 5 条价值 bullet「任何方案都须交代取舍成本与潜在技术债——没有免费的架构」（Trade-off 意识普适化）；「可解释性高于魔法式实现」条尾并入 KISS 可操作判据「复杂到一句话讲不清的方案就该重构（KISS）」。→ AC1、AC3
- `Coder/00_System_Prompt/presentation-protocol.md` §5 选项表格化 — 「单一方案或无需对比时」bullet 补约束「但仍必须交代该方案的取舍 / 代价（呼应 `identity.md §3.1`），不得只报优点」；把「代价·取舍」从「仅 ≥2 方案对比时列」松绑为「给任何方案都须交代」。§5 表格骨架与 §9 样例未动。→ AC2
- `Coder/20_Workflow_Lifecycle/lifecycle.md` P1 Analysis — 「AI 必须回答」列表新增第 3 问「需求里有没有伪需求、投入产出比过低或不合逻辑的部分？该剥离、缩到 MVP（最小可用版本），还是提替代方案？」（剥离伪需求 / MVP 质询）；其后新增 blockquote 消歧「质询在 P1、固定需求锁定在 P2 ACK 冻结后生效——P1 质询 → P2 冻结 → 之后守住，三个先后动作、不矛盾」。→ AC4

## ADD

- 无（本迭代不新增文件；③ 决策只落 lifecycle、不碰 `concept-schema.md`，守 DRY）。

## DELETE

- 无。
