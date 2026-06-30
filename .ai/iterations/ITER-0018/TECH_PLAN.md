# TECH_PLAN — ITER-0018

# Goal

- 支撑 AC1–AC10：新增 `changelog-schema.md` 把 `01_CHANGELOG.md` 正式化为严格 ADD/EDIT/DELETE 每迭代变更流 + 同步所有引用语义 + Should-Fix 迁 VERIFY_REPORT + 收口产出/归档接线 + dogfood，且不碰四件套字段/AC 脊柱/状态机/hook/根 CHANGELOG。

# Files / Modules to Change

- 新增 `Coder/20_Workflow_Lifecycle/changelog-schema.md` —— `01_CHANGELOG.md` 的格式契约（落 20：它是迭代生命周期产物，与 iteration-schema 同族）（AC1/2/8）。
- 新增 `.ai/01_CHANGELOG.md`（ITER-0018 自身，dogfood）+ `.ai/iterations/ITER-0017/CHANGELOG.md`（回填范例）（AC7）。
- 改 `mcv-deployment.md §43` —— 01_CHANGELOG 语义从"技术决策与需求增量"→"对象级变更 ADD/EDIT/DELETE，见 changelog-schema"（AC3）。
- 改 `maintenance-boundaries.md §15` —— CHANGELOG 行重定义为 ADD/EDIT/DELETE 触发口径 + **删除 "Should Fix 条目"**（AC3/AC4）。
- 改 `iteration-schema.md` §4.4 / §5.5 —— §84 过程细节→对象级变更记录；§5.5 收口步：完整路径**必产** 01_CHANGELOG + 归档（AC3/AC5）。
- 改 `lifecycle.md §165` —— 收口 step ① 措辞：完整路径必产的 01_CHANGELOG 切片（AC3/AC5）。
- 改 `mcv-update.md §5.1` —— 加一行：迭代化项目 changelog 格式/语义以 `changelog-schema.md` 为准（消"决策快照"旧义残留）（AC3）。
- 改 `review-engine.md §71` + `dangerous-engine.md §121` —— Should Fix 改记入 `VERIFY_REPORT.md` 的 `Remaining Risks`，不再写 01_CHANGELOG（AC4）。
- 改 `verify-schema.md §4` —— 收端补一行：Review/自评的 Should Fix（不阻断项）记入 `Remaining Risks`、不写 changelog（AC4 契约闭合）。
- 改 `delivery-summary.md` —— 边界段指向 changelog-schema + 明确 delivery 高层/changelog 细粒度分工（AC8）。
- 改 `README.md` —— 目录树 + 描述块注册 `changelog-schema.md`（AC6）。
- 评估不改 `templates/rule-card.md` —— changelog 不进强制产物集（AC9）。

# Interface / Contract

- **格式（锁定，MILE-0001 定调）**：顶部 `> <标题> · <active|closed> · <收口日期>`；三段 `## ADD` / `## EDIT` / `## DELETE`，严格三类、无内容写"无"不省段；每条 `` `对象 §章节` — 一句话语义 → ACn ``。
- **粒度**：文件 + 章节级，不逐行；rename = 一条 DELETE + 一条 ADD。
- **噪声地板**：跳纯排版 / typo / lint（沿用 `maintenance-boundaries §15`）。
- **分工（四产物边界）**：changelog=对象级变更流（绑 AC）；delivery=人读高层散文；ITERATIONS=迭代索引；PROJECT=状态全貌。git=机械全量真源，changelog=精选语义。
- **何时写**：P4 期间内存累积（合 maintenance-boundaries 批处理），收口 finalize；完整路径**必产**、简化路径可省；开新迭代 overwrite-reset。
- **Should-Fix 落点**：`VERIFY_REPORT.md` 的 `Remaining Risks`（不再入 changelog）。

# State / Boundary

- 本迭代 = R3：纯 markdown 契约 + 接线 + dogfood。
- 不做（归 R2/ITER-0019）：收口执行门禁、一致性探针、原子收口命令。
- 不碰：四件套字段结构、AC 脊柱、P1-P5 状态机、hook 代码、版本机制、根 `CHANGELOG.md`。

# Design Decisions

- **Q1 必产口径（定）**：完整路径迭代收口**必产** `01_CHANGELOG.md` 并归档；简化路径可省。理由：用户要"随迭代严格 changelog"，完整路径才有足量对象级变更。
- **Q2 Should-Fix 落点（定）**：`VERIFY_REPORT.md` 的 `Remaining Risks` 段（既有字段，语义=不阻断但须记录），收端在 verify-schema §4 补口径闭合。不新增文件。
- **Q3 不进硬门禁（定）**：changelog 不进 hook `phase_gate`、不进 rule-card 强制产物集——同 PROJECT.md，是收口产物非阶段门禁产物；靠收口纪律 + R2 探针兜底。rule-card 不改（守"模板单一来源"）。
- **Q4 与 delivery 分工（定）**：并存不替代。delivery「已完成内容」写高层人话，changelog 写细粒度对象级 ADD/EDIT/DELETE；delivery 可引用 changelog 不复述。schema §4 写清边界。
- **落位（定）**：schema 放 `20_Workflow_Lifecycle`（迭代生命周期族），非 40（40 是上下文/冷启动族）。
- Active profiles：无（Markdown 规则仓）。

# Execution Steps

- [ ] T1 写 `20_Workflow_Lifecycle/changelog-schema.md`：定位/格式/粒度/噪声地板/四产物分工/何时写/写作口径，含范例 → AC1/2/8
- [ ] T2 改 `mcv-deployment.md §43` 语义重定义 → AC3
- [ ] T3 改 `maintenance-boundaries.md §15` 重定义 + 删 Should Fix → AC3/AC4
- [ ] T4 改 `iteration-schema.md` §4.4 措辞 + §5.5 必产/归档 → AC3/AC5
- [ ] T5 改 `lifecycle.md §165` 收口步措辞 → AC3/AC5
- [ ] T6 改 `mcv-update.md §5.1` 加 changelog-schema 指针 → AC3
- [ ] T7 改 `review-engine.md §71` + `dangerous-engine.md §121` + `verify-schema.md §4`：Should-Fix 迁 VERIFY_REPORT Remaining Risks → AC4
- [ ] T8 改 `delivery-summary.md` 边界段：分工 + 指针 → AC8
- [ ] T9 改 `README.md` 目录树 + 描述块注册 schema → AC6
- [ ] T10 dogfood：写 `.ai/01_CHANGELOG.md`（ITER-0018）+ `.ai/iterations/ITER-0017/CHANGELOG.md`（回填范例）→ AC7
- [ ] T11 rule-card 裁决：不进强制产物集 + grep 确认 0 处变更 → AC9
- [ ] T12 收口前自检：grep 全量 01_CHANGELOG / Should Fix 残留；git diff 确认四件套字段/hook/状态机/根 CHANGELOG 未碰；五约束自检 → AC10
- 粒度说明：多文件 reconcile，展开到任务级；T2–T9 相互独立可并行推进，T10 依赖 T1，T11/T12 收尾。

# Verification Plan

- 按 `AC_LIST.md` Verification Method 逐项核对；重点：T1 schema 完整性（AC1/2/8）、T7 三处 Should-Fix 全迁（AC4，grep 兜底）、T10 dogfood 两文件合格式（AC7）、T12 残留与不变量 grep（AC3/AC10）。

# Risks / Open Questions

- **mcv-update 旧义残留**：§5.1 line 159 自动化命令含"决策快照"措辞，属**老项目**（迭代机制上线前）兜底语境，本迭代加指针澄清迭代化项目走新 schema，不重写 legacy 兜底（边界清晰、非残留）。
- **Should-Fix 迁移遗漏**：用 grep 全量核对 `Should Fix` / `01_CHANGELOG` 三处全覆盖（AC4/AC12 自检）。
- 无遗留 Must Fix；4 个 P1 开放项已在 Design Decisions 落定。
