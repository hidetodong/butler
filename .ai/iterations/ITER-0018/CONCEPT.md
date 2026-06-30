# CONCEPT — ITER-0018

> 分流：完整路径 | 命中升级信号：契约变更（重定义 `01_CHANGELOG.md` 语义 + 新增 schema）、多文件跨模块影响 | 2026-06-30

## 一句话

butler 现在没有"每个迭代精确改了什么"的结构化记录——规则里有个 `01_CHANGELOG.md` 影子，但取向是"决策 / 增量日志"、没 schema、从未真正产出过；事实上的变更记录只活在 `deliveries/` 的散文里。本迭代把 `01_CHANGELOG.md` 正式化为**严格 ADD / EDIT / DELETE 的每迭代变更流**（活跃期 `.ai/01_CHANGELOG.md`、收口归档 `iterations/ITER-NNNN/CHANGELOG.md`），给它真 schema、收编半成品、并把搭便车的 Should-Fix 留痕迁出。

## 背景与判断

- 现状有三处"changelog"，无一满足需求：根 `CHANGELOG.md`（人读发布史、按版本聚合）、`.ai/01_CHANGELOG.md`（半成品决策日志、无 schema、未 dogfood）、`deliveries/`（散文事实记录）。都不是"随迭代、严格三类操作"的精确变更流。
- 格式已在 MILE-0001 范围演进记录定调（经四方案对比后用户选回当前提案），本迭代不再改格式，只把它落成 schema + 接线。
- 落点已定：复用 `01_CHANGELOG.md` → `iterations/ITER-NNNN/CHANGELOG.md` 槽位（用户倾向），把它从"决策日志"**重定义**为"变更流"。
- 必须 reconcile 一个搭便车副作用：当前 Should-Fix 留痕写入 `01_CHANGELOG.md`（review-engine §71 / dangerous-engine §121）。重定义后 Should-Fix 无处可去，需迁新家，不能静默丢弃。

## 目标（Goal）

- G1：新增 `changelog-schema.md`——定义每迭代 changelog 的格式（锁定的操作分组三段 + 每条绑 AC + 顶部元信息）、粒度、噪声地板、与 git / delivery 的分工、何时写。
- G2：把 `01_CHANGELOG.md` 语义从"决策 / 增量日志"**重定义**为"严格 ADD/EDIT/DELETE 变更流"，并同步所有引用它的规则到一致语义。
- G3：Should-Fix 迁新家——review-engine / dangerous-engine 不再写 `01_CHANGELOG.md`，改落 VERIFY_REPORT。
- G4：收口接线——完整路径迭代收口产出 changelog 并归档；delivery 与 changelog 分工明确、不重复记账。
- G5：dogfood——ITER-0018 自身按新格式产出 `.ai/01_CHANGELOG.md`；并回填 `iterations/ITER-0017/CHANGELOG.md` 作具体范例。

## 约束（Constraints）

- 严格三类 ADD / EDIT / DELETE，格式以 MILE-0001 定调为准，本迭代不再改格式。
- 不双重记账：changelog（精确变更流）≠ delivery（人读散文）≠ ITERATIONS（迭代索引）≠ PROJECT（状态全貌），各管一轴。
- R3 纯 markdown：不动四件套字段结构、AC 脊柱、P1-P5 状态机、hook 代码（执行门禁 / 探针归 R2）。
- 守本仓五约束（分层 / 产物链 / 无隐式依赖 / 模板单一来源 / audience 标注）。

## 影响范围（Impact Scope）

- 新增：`Coder/20_Workflow_Lifecycle/changelog-schema.md`；`.ai/01_CHANGELOG.md`（dogfood）、`.ai/iterations/ITER-0017/CHANGELOG.md`（回填范例）。
- 改：`mcv-deployment.md`（01_CHANGELOG 语义描述）、`iteration-schema.md`（§5.1 reset + §5.5 收口产出/归档）、`lifecycle.md`（§165 收口步措辞）、`maintenance-boundaries.md`（§15 CHANGELOG 口径）、`review-engine.md §71` + `dangerous-engine.md §121`（Should-Fix 迁新家）、`README.md`（注册新 schema）；评估 `delivery-summary.md`（与 changelog 分工）、`rule-card.md`。
- 不影响：四件套字段 / AC 脊柱 / 状态机 / hook 代码 / 版本机制 / 根 `CHANGELOG.md`（发布史）。

## 项目类型与 Profiles

Markdown 规则仓，无技术栈 Profile。

## 待澄清（Open Questions）

- Q1：changelog 是否为完整路径"必产"收口物？倾向是（完整路径必产、简化路径可省）。（P3 定）
- Q2：Should-Fix 落 VERIFY_REPORT 哪一段？倾向复用其「Remaining Risks / Should Fix」段，不新增文件。（P3 定）
- Q3：是否进 hook / rule-card 硬门禁？倾向否（同 PROJECT.md，靠收口纪律 + R2 探针）。（P3 定）
- Q4：delivery「已完成内容」改为引用 changelog 还是并存？倾向并存但 delivery 高层化、细粒度让位 changelog（避免重复）。（P3 定）
