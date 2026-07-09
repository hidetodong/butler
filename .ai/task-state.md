# Task State

> **无活跃迭代 / 无活跃里程碑**（`ITERATIONS.current: none`、`MILESTONES.current: none`）。**MILE-0004 已收口 + 随 v2.1.0 发布**（MINOR，聚合 ITER-0035~0041）。等下一个方向。

## 当前状态

- 无进行中工作。MILE-0004"PRD 先行 + references 版本化改版同步"六块齐（R1–R6）已收口，版本级交付 `deliveries/milestones/MILE-0004-prd-first-versioned-references.md`+`.html`，里程碑快照 `.ai/milestones/MILE-0004/MILESTONE.md`。
- **v2.1.0 已切版**：`VERSION=2.1.0`、`CHANGELOG.md [2.1.0]`、`migrations/v2.1.0.md`（`[no-op]`+`[restamp]`，部署面模板零改动）、tag `v2.1.0`。聚合 ITER-0035~0041（ITER-0035 为正交独立迭代，MILE-0004 = ITER-0036~0041）。
- 全貌产物（`frontier.md` / `architecture.md` / `capabilities.md`）已前滚到 v2.1.0 发布态。

## 下一步入口

- **待用户给方向**：新里程碑 / 独立迭代由用户发起。候选——PRD 全链真实 dogfood（拿一份真 PRD 走导入→改版全程），可一并还上"从未真跑"的欠账。
- **推送**：v2.1.0 发布提交 + tag、以及 ITER-0035~0041 全部迭代提交**均在本地 main、未推送**。推送待用户说"推送"（含 `git push && git push --tags`）。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
