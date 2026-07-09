# Task State

> **无活跃迭代**（`ITERATIONS.current: none`）。里程碑 **MILE-0004** 路线图 R1–R6 **六块齐**，R6（ITER-0041）已收口——**MILE-0004 收官，待收口里程碑 + 切版（发布动作、待放行）**。

## 当前状态

- `ITERATIONS.current: none`。ITER-0041（MILE-0004 R6·收官）已收口：认亲松边（`prd-update §4.2`）+ 非回归门（`references-schema §9`）+ 收尾（HUMAN_GUIDE PRD 用法节 / flip §4·§8 / 说人话自检）全落地，独立复核 APPROVE-with-nits（Must/Should Fix 均已整改），6 不变量已过。
- `MILESTONES.current: MILE-0004`（active，路线图 R1–R6 见 `.ai/MILESTONE.md §5.3`，六项全 ✅）。PRD 全生命周期链成文：导入(R1/R2)→挂里程碑(R3)→钉版(R4)→改版同步(R5)→认亲边缘+非回归门+收尾(R6)。
- 全貌产物（`frontier.md` / `architecture.md` / `capabilities.md`）已前滚到 R6 收口态（六块齐、战线转收口+切版）。

## 下一步入口

- **收口 MILE-0004 + 切版（待用户放行、非自动）**：六块齐后可收口里程碑（`MILESTONES.md` 翻 closed + 版本级交付 `deliveries/milestones/MILE-0004-<slug>.md`+`.html`）+ 独立 `chore(release)` 切版（聚合 ITER-0036~0041，VERSION/CHANGELOG/migrations/tag）。同 MILE-0003 v2.0.0 分开走的先例，**待用户明确放行**。
- **六提交未推**：ITER-0036~0041 六个迭代提交均在本地 main、**未推送**（a9dd72d / 2d19d92 / 002839d / 3f9bb9c / 02c1c3d / 本次 R6）。推送待用户说"推送"。
- 冷启动读序（butler 文件夹态）：`.ai/project/00_INDEX.md` → `.ai/MILESTONES.md` / `.ai/MILESTONE.md` / `.ai/ITERATIONS.md` → 本文件 → 代码。
