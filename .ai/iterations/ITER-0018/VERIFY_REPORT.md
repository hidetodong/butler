# Verification Summary

- 新增 `changelog-schema.md` 把 `.ai/01_CHANGELOG.md` 正式化为严格 ADD/EDIT/DELETE 每迭代对象级变更流，重定义其语义并同步 5 处引用，把搭便车的 Should-Fix 从 3 处迁到 `VERIFY_REPORT.md` 的 `Remaining Risks`，接线收口必产/归档，dogfood 自身 changelog + 回填 ITER-0017 范例。改动集中在 20（生命周期）层 + 60/65 审查引擎接线，未碰四件套字段 schema / hook / 状态机 / 根 CHANGELOG / VERSION。

# AC Status

- [x] AC1 ✓ 新增 `20_Workflow_Lifecycle/changelog-schema.md`，§2 锁定格式：顶部 `> 标题 · 状态 · 日期` + 三段 `## ADD/## EDIT/## DELETE`（严格三类、无内容写"无"不省段）+ 每条 `` `对象 §章节` — 语义 → ACn ``，与 MILE-0001 定调一致。
- [x] AC2 ✓ schema §3 定粒度（文件+章节级、不逐行、rename=DELETE+ADD）+ 噪声地板（跳排版/typo/lint，沿用 maintenance §15）；§1 表 + 末句定与 git（机械全量真源）分工；§6 写作口径指针引用 `artifact-style.md`。
- [x] AC3 ✓ `01_CHANGELOG.md` 语义重定义为"对象级 ADD/EDIT/DELETE 变更流"，同步 mcv-deployment §43 / maintenance §15 / iteration-schema §4.4·§5.5 / lifecycle §165 / mcv-update §5.1；grep 确认无"技术决策/需求增量/决策记录"旧义残留。
- [x] AC4 ✓ Should-Fix 三处全迁：review-engine §71 + dangerous-engine §121 改记入 `VERIFY_REPORT.md` 的 `Remaining Risks`、明文"不写入 01_CHANGELOG"；maintenance §15 删除"Should Fix 条目"输入；verify-schema §4 收端补口径闭合；grep 确认无"Should Fix→01_CHANGELOG"残留。
- [x] AC5 ✓ iteration-schema §5.5 step 1 + lifecycle §165 step ① 明确完整路径收口**必产** `01_CHANGELOG.md` 并归档 `iterations/ITER-NNNN/CHANGELOG.md`（简化路径可省）。
- [x] AC6 ✓ README 目录树（iteration-schema 下）+ 描述块均注册 `changelog-schema.md`。
- [x] AC7 ✓ dogfood：`.ai/01_CHANGELOG.md`（ITER-0018，active）+ `.ai/iterations/ITER-0017/CHANGELOG.md`（回填范例，closed）均按新格式产出、非空、三段齐备。
- [x] AC8 ✓ schema §1「四产物边界」表 + §4「与交付总结分工」：changelog(变更delta) / delivery(人读高层) / ITERATIONS(索引) / PROJECT(状态)，delivery 引用 changelog 不复述，无双重记账；delivery-summary 边界段同步。
- [x] AC9 ✓ rule-card 裁决：changelog 不进强制产物集（同 PROJECT.md，收口产物非阶段门禁）；grep 确认 rule-card 0 处 changelog、文件未改，守"模板单一来源"。
- [x] AC10 ✓ git status 确认未碰 concept/acceptance/tech-plan schema、`templates/hooks`、根 `CHANGELOG.md`、`VERSION`；P1-P5 状态机分流未动（lifecycle 仅触 §165 收口步措辞）；本仓五约束自检通过。

# Verification Results

- AC1/2/8：读 `changelog-schema.md` 核对格式锁定、粒度/噪声地板/四产物分工/写作口径完整。
- AC3/AC4：`grep -rn 01_CHANGELOG`、`grep "Should Fix" | grep 01_CHANGELOG` 全量核对——旧语义零残留、Should-Fix 三处全迁（剩余命中均为新增的"不写入"声明）。
- AC5/AC6：读 iteration-schema/lifecycle 收口步 + README 注册，确认必产/归档与登记到位。
- AC7：查两 changelog 文件存在、非空、合格式。
- AC9/AC10：grep rule-card 0 命中；`git status` 确认不变量文件未出现在改动名单。

# Gate Coverage

- 通用质量门禁：新 schema frontmatter（title/audience/scope）合规、措辞"必须/不得/应"、节号 §1–§7 连续、格式范例与 §2 规则自洽。
- Active Profiles：无（Markdown 规则仓）。
- Tech Plan Alignment：T1–T12 全兑现；Design Decisions Q1（完整路径必产）/Q2（落 Remaining Risks）/Q3（不进硬门禁）/Q4（与 delivery 并存分工）均按方案落地。
- References Compliance：N/A（本轮无 `.ai/references/`）。

# Remaining Risks

- `mcv-update §5.1` 自动化命令仍含"决策快照"措辞，属**老项目**（迭代机制上线前）legacy 兜底语境，已加指针澄清迭代化项目走新 schema、不重写 legacy（边界清晰、非旧义残留）。
- changelog 必产靠收口纪律、无机械门禁（butler 自身不跑 hook）——R2 / ITER-0019 的执行门禁 + 一致性探针拟覆盖。
- 无遗留 Must Fix；无 Should Fix。

# Handoff / Next Step

- ITER-0018 验证闭环，可收口（归档 `iterations/ITER-0018/` 四件套 + 本迭代 `01_CHANGELOG.md` 切片 + `deliveries/ITER-0018-*.{md,html}` + 台账置 closed + `current` 置 none + 按需前滚 PROJECT.md）。
- 后续：R2（ITER-0019 收口门槛）；MILE-0001 待 R2 收口后聚合发布（切版 + 根 CHANGELOG + migrations）。
