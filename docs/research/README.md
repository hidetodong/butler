# docs/research/ — 预研区

本目录存放**尚未进入体系**的探索性记录：概念讨论、early-stage 想法、不成熟或风险未收敛的设计。它是 `specs/` 的「上游候选区」，但**本身不在落地管线里**。

## 与 docs/superpowers/ 的区别

| 目录 | 定位 | 是否进体系 |
|---|---|---|
| `docs/superpowers/specs/` | 设计取舍（D1–Dn），已决定落地 | 是，配 `plans/` 推进 |
| `docs/superpowers/plans/` | 实施计划 | 是 |
| `docs/research/`（本目录） | 预研：概念/想法，尚未拍板 | **否** |

## 约束

- 本目录的文档**不被 butler 体系引用**：不进 `Coder/` 规则链、不在 `Coder/README.md` 读取顺序里注册、不排 plan。
- 一份预研要转正，须另起 `docs/superpowers/specs/` 设计取舍 spec + `plans/` 计划，届时从本目录迁出或留档。
- 文件命名沿用 `YYYY-MM-DD-<topic>.md`。

## 当前条目

- `2026-06-16-parallel-iteration-concept.md` — 并行迭代增强模式概念。**暂缓**（2026-06-29 拍板）：概念尚不成熟、有并行串扰串行核心的风险，暂不进入体系。
- `MILE-0003-preresearch-brief.md` — **MILE-0003 预研总纲 + 交接简报（入口，先读这份）**。把主体（知识文件夹）+ 两个子项（帮手名册、说人话）+ 已定/待定/不做 + 换电脑起步步骤收在一处，自包含、供另一台电脑接手。2026-07-03。
- `MILE-0003-project-knowledge-folder.html` — MILE-0003 方向性预研：项目知识文件夹（`PROJECT.md` → `.ai/project/`）。**讨论中，结论未冻结**；MILE-0002 已收口，开题闸已解除。
- `MILE-0003-agent-doc-design.md` — MILE-0003 子设计：Butler Agent 文档（复核 / 更新说明 / 查过时三帮手的名册 + 通用规矩；帮手=一份定义资料、用时读、不下发）。**讨论中，未冻结**，随 MILE-0003 一并转正。2026-07-03 按三项决策重写；配套 `MILE-0003-agent-doc-audit.html`（审计）与 `MILE-0003-next-steps.html`（待办）。
