# Verification Summary

- 新增 `.ai/PROJECT.md` 全貌产物 + `project-digest-schema.md` 格式契约，接线 6 个规则文件（README / context-persistence / handoff-spec / iteration-schema / milestone-schema / mcv-deployment）并同步 lifecycle 收口步复述，butler 自身落 PROJECT.md 种子 dogfood。改动集中在 40（上下文）/ 20（生命周期）两层 + 文档接线，未碰四件套字段 schema / hook / 状态机分流 / rule-card。

# AC Status

- [x] AC1 ✓ 新增 `40_Context_Management/project-digest-schema.md`；§3 必填 6 字段（目的 / 架构与模块地图 / 关键长期决策与不变量[带为什么] / 现行约束 / 已知长期欠债 / 指针），§1 明文"状态取向、写现在是什么不是变更日志"。
- [x] AC2 ✓ schema §2 定 ≤1500 tokens + 指针化（深内容指向代码 / deliveries / architecture-overview / schema，不内嵌）；§6 写作口径指针引用 `artifact-style.md`，不另起一套。
- [x] AC3 ✓ schema §1「四产物边界」表：PROJECT(状态) / ITERATIONS(变更流) / 02_SESSION_HANDOFF(瞬时) / MILESTONE(版本范围)，职责不重叠。
- [x] AC4 ✓ context-persistence 新增「冷启动读序」（第一读 PROJECT → ITERATIONS → handoff → 代码）；handoff-spec §1 补"状态全貌由 PROJECT 承载、指针引用"；README 40 说明同补。
- [x] AC5 ✓ README §目录结构 40 下注册 `project-digest-schema.md` + 文件说明加一行。
- [x] AC6 ✓ iteration-schema §5.5 + milestone §7.4 收口加第四步「按需前滚 PROJECT.md」+ 判据/成本声明（多数 0-2 行或不动）；lifecycle §165 复述同步（P5 发现的一致性漂移，已修）。
- [x] AC7 ✓ mcv-deployment 运行态文件清单加 PROJECT.md。**设计细化（如实披露）**：按 §2「部署仅创建目录、不预置内容」原则，改为**按需产生**（首次收口前滚落地）而非部署时建空骨架——空项目的全貌摘要无意义；已部署项目补建口径已定（新建 + 首次回填，实际配方聚合发布时写）。
- [x] AC8 ✓ butler 自身 `.ai/PROJECT.md` 已落真内容（6 段填满、贴合现状），dogfood 验证 schema 可用、非空。
- [x] AC9 ✓ rule-card 裁决：不进强制产物集（PROJECT.md 非阶段门禁产物）；grep 确认 rule-card 0 处 `PROJECT`、文件未改动，守住"模板单一来源"。
- [x] AC10 ✓ git status 确认未碰 concept/acceptance/tech-plan/verify-schema、`templates/hooks`、rule-card；P1-P5 状态机分流未动（lifecycle 仅同步收口步复述）；本仓五约束自检通过。

# Verification Results

- 逐文件核对 + `git diff --stat`：改动 6 规则文件 + lifecycle 同步 + 5 个新增（schema / PROJECT.md / MILESTONE(S).md / task-state.md），未外溢。
- 不变量 grep：四件套字段 schema / hook / lifecycle 分流 / rule-card 均未被改（lifecycle 仅触及 §165 收口步复述与 §197 文件清单，非状态机流转）。

# Gate Coverage

- 通用质量门禁：新 schema frontmatter（title/audience/scope）合规、措辞"必须/不得/应"、节号 §1–§7 连续、模板骨架 H1 + 6 H2 与 §3 字段表一致。
- Active Profiles：无（Markdown 规则仓）。
- CLAUDE.md 五约束：①分层不混（新 schema 落 40 上下文层、收口前滚落 20，职责不窜）②产物链不破（四件套字段未动）③无隐式依赖（新 schema 已在 README 注册）④模板单一来源（rule-card 未改）⑤新 schema frontmatter audience+scope 合规。

# Self-Review（P5 默认简评，review-engine）

- 同上下文简评 + dogfood 自检：`PROJECT.md` 与新 schema 自身符合 `artifact-style`（讲人话、bullet、嵌套 ≤2 层、无反面黑话词）；冷启动读序四产物边界自洽；mcv §2 张力**显式化解、非静默降级**。
- 结论：无 Must Fix、无 Should Fix。

# Remaining Risks

- `migration-schema` 无"新建文件"步型，R1 只定补建口径，实际 `[add-file]` 步型是否新增留聚合发布时定。
- PROJECT.md 维护靠收口前滚纪律、无机械门禁（butler 自身不跑 hook）——R2 / ITER-0018 的一致性探针拟补。
- 无遗留 Must Fix。

# Handoff / Next Step

- ITER-0017 验证闭环，可收口（归档 `iterations/ITER-0017/` + `deliveries/ITER-0017-*.{md,html}` + 台账置 closed + `current` 置 none；本迭代恰好改了 PROJECT.md 自身机制，种子已含 dogfood 内容，收口时核对一致即可）。
- 后续：R2（ITER-0018 收口门槛）、R3（ITER-0019 changelog 正式化）；MILE-0001 待三迭代收口后聚合发布。
