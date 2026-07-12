# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**ITER-0043（工程原则增量吸收）已收口、待切 v2.3.0**（MINOR）。v2.2.0 已切版（本地 tag，聚合 ITER-0042，未推送）。等下一个方向。

## ITER-0043 收口小结

- 吸收外部「工程宪法」的 3 条真增量（减法后 13 条留 3）：① Trade-off 普适化（`identity §3.1` 加价值 + `presentation §5` 单方案也须交代取舍）；② KISS 判据（`identity §3.1` 并入「可解释性」条）；③ 伪需求质询（`lifecycle P1` 加第 3 问 + 时序消歧）。③ 只落 lifecycle、不碰 `concept-schema`（守 DRY）。
- 9 条 AC 全过（AC1–8 auto·可靠 + AC9 独立复核 APPROVE-with-nits，0 refute，Should-Fix「要→须」+ Nit「MVP 注解」已改）。改动仅 3 规则文件（6 增 2 删），边界文件全 clean。
- 交付 `deliveries/ITER-0043-engineering-principles-absorption.md`+`.html`，归档 `.ai/iterations/ITER-0043/`。全貌产物已折（`capabilities` P1 行 + `frontier`）。
- **未切版**：`VERSION` 仍 `2.2.0`。ITER-0043 判 MINOR，下次切版 v2.3.0 聚合它（规则正文原则增强、无部署面变化 → 迁移预计 `[no-op]`+`[restamp]`）。

## 背景（近两迭代 + 版本态）

- ITER-0042（PRD 先行触发加固）已收口并**聚合切版 v2.2.0**：`VERSION`=`2.2.0`、`CHANGELOG` 顶条 `## [2.2.0]`、tag `v2.2.0` 在发布提交 `41ee299`、`migrations/v2.2.0.md`（本仓首个 `[sync-hooks]`）。
- ITER-0043（本迭代）已收口、**未切版**（见上方小结）。

## 下一步入口

- **推 v2.2.0 tag**：main 分支已 `git push`（远端已到 `41ee299`）；但 **`v2.2.0` tag 仍未推**（`git push` 不带 tag）。要上远端需 `git push origin v2.2.0`——待用户放行。
- **切 v2.3.0**（待放行）：聚合 ITER-0043（判 MINOR）；迁移预计 `[no-op]`+`[restamp]`（规则正文原则增强、无部署面变化）。可与 ITER-0043 一起或攒后续迭代再发。
- **待用户给方向**：新里程碑 / 独立迭代由用户发起。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程），可一并还上"从未真跑"的欠账。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
