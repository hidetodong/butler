# RUN_LOG — 自治决策与门禁旁路审计账本

> 本文件是危险模式（`/dangerous`）自主决策与 hook bypass 的连续审计账本，跨阶段不净化（见 `Coder/65_Extension_Dangerous/dangerous-engine.md §7.1`）。每条至少含：日期、节点、迭代号、标记、自审结论与一句自决摘要。审计即时落盘，不事后补写。

## ITER-0014 — 版本升级 SOP 化（迁移配方 + upgrade 执行器）

- 2026-06-30 · dangerous-on · ITER-0014 · 用户本会话显式"开启危险模式"。butler 仓自身无 `.ai/local-constraints.md`（规则仓非部署项目，不受自己 hook 管），开关无持久落点；按协议实质执行：本会话自治 + 本账本审计 + 自审门替代 ACK + P5 强审 + git 回滚锚点 + 交付披露。
- 2026-06-30 · iter-open · ITER-0014 · 领号 ITER-0014、置 active、`current` 指向它；北极星=版本升级 SOP 化（单迭代路线图）。回滚锚点=git HEAD（待改的 butler-upgrade / versioning-schema / README 均已提交干净，新增文件未跟踪，`git checkout` + 删新文件即可整体回退；不碰预存的 Coder/40 改动）。
- 2026-06-30 · P2-self-ack · ITER-0014 · dangerous-ack · 自审门（对照 `acceptance-schema.md`）：11 条 AC 均可验证且绑定验证动作，覆盖功能/结构/质量三类；In/Out Scope 清晰（不实际切版、不改 hook 代码划入 Out）；风险已如实暴露（已漂移项目、无版本戳老项目）。无"不可验证 / 范围膨胀 / 隐藏未决项" → 通过，自主 ACK，`AC_LIST.md` 置 `ack-frozen`。
- 2026-06-30 · P3-self-ack · ITER-0014 · dangerous-ack · 自审门（对照 `tech-plan-schema.md` + `AC_LIST.md`）：TECH_PLAN 逐项映射 AC1–AC11；配方格式与执行器输入输出契约、改动边界清晰；未命中影响面失控信号（改动集中在升级 / 版本治理两规则 + 新增一个 schema + 配方数据，无跨模块扩张）；无 active profile 可违背。通过，自主 ACK。
- 2026-06-30 · P5-review · ITER-0014 · dangerous-ack · 强制完整审查（§7.3）升格为独立复核：起一个不带本会话上下文的 general-purpose 子 agent，spec-only 逐 AC 裁决 + 交叉验证三份配方与 CHANGELOG。结论：AC1/2/4/5/6/7 confirm；**AC3 refute=实质 Must Fix**——`migrations/v1.1.0.md` 漏 `[regen-claude]`（独立复核指出 ITER-0008/0009/0010 均改过 rule-card，我用 `git log -- templates/rule-card.md` 复核证实 df46735/5f2eb4e/e2a8cb0 确实在列）；AC8–11 refute 系 P5/收口产物当时尚未产出。处置：Must Fix#1 已修（v1.1.0 补 `[regen-claude]` + 影响段；`migration-schema.md §4` 加"漏判防线"判据防复发）；Must Fix#2/#3 由本 P5 报告 + 收口三步补齐。复查通过，无遗留 Must Fix。
