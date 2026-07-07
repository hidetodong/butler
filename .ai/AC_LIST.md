---
状态: ack-frozen
ACK 日期: 2026-07-07
迭代: ITER-0029
里程碑: MILE-0003 R3
---

> 监督态自驱：本迭代由用户"继续吧"委托执行（非 `/dangerous`），P1–P3 自驱、不设自审门横幅、不写 RUN_LOG；P5 起独立复核子 agent 守质量（重点：两态兼容不砸单文件项目收口 + 5→6 计数全仓无遗漏 + scope 不越 R5/R6/R8）；用户可随时叫停 / 回退（ITER-0029，2026-07-07）。

# Goal

- 把 R2 在 `project-digest-schema §6` 声明的折叠维护模型**接线成活跃收口仪式**：泛化收口步④（两态）+ 加冷启动一致性自检第 6 条（知识文件夹漂移，带条件）+ 全仓 5→6 计数同步 + 顺修 R2 遗留 §5→§6 引用漂移 + 翻 R3 前向指针。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- 泛化 `iteration-schema §5.5` / `milestone-schema §7.4` 收口步④ 为两态（文件夹态必做折叠 / 单文件暂态前滚）。
- `context-persistence §冷启动一致性自检` 新增第 6 条「知识文件夹漂移自检」（条件适用）。
- `lifecycle §收口` / `versioning-schema §切版自检` / `iteration-schema §5.5 步⑤` 的一致性自检计数 5→6 同步。
- 修 `iteration-schema §5.5` / `milestone-schema §7.4` 的"见 `project-digest-schema.md §5`"→ §6。
- 翻 `project-digest-schema §6/§9` R3 指针（待→已接线）；`.ai/PROJECT.md` 按判据前滚。

# Out of Scope

- 不改冷启动**第一读目标**（仍 `.ai/PROJECT.md`；切到 `00_INDEX` 是 R5）；`context-persistence §冷启动读序` 除加第 6 不变量外不动读序。
- 不加部署种子 / 迁移配方（R6，`mcv-deployment` / `migrations/` 不碰）。
- 不迁移 butler 自身 `.ai/PROJECT.md → .ai/project/` 实体（R8）；不切版、不动 `VERSION`。
- 不做自动化生成 / 自动折叠脚本（本里程碑只定手工回路）。
- 不改 P1–P5 状态机 / 四件套字段 / AC 脊柱 / hook / 迭代里程碑双层 / `.ai/project/` 结构。

# Acceptance Checklist

- [ ] AC1（收口步·iteration 两态）: `iteration-schema §5.5` 步④ 改为两态——项目已采用 `.ai/project/` 则"按主题路由本迭代 CHANGELOG delta 折进对应 topic 文件、**必做**（有 delta 即折、非按需）"；仍单文件 `.ai/PROJECT.md` 则按旧"按需前滚"；措辞明写两分支 + 成本口径（路由非重推导、∝改动量）；该步内"判据/格式"引用改指 `project-digest-schema.md §6`。
- [ ] AC2（收口步·milestone 两态）: `milestone-schema §7.4` 步④ 同样两态泛化；注明迭代级已在各迭代收口增量折叠、里程碑步只保**版本级全貌一致**不重折；引用改指 `project-digest-schema.md §6`。
- [ ] AC3（自检·第 6 不变量）: `context-persistence §冷启动一致性自检` 在第 5 条后追加**第 6 条「知识文件夹漂移自检」**——采用 `.ai/project/` 的项目核对"近期 CHANGELOG delta 是否都已折进对应 topic、有无被取代结论残留"，脱节先暴露；**明标条件**"仅采用知识文件夹的项目适用；仍单文件 PROJECT.md 的项目 N/A"；给可操作核法（非自动化脚本）；不 renumber 前 5 条。
- [ ] AC4（计数·5→6 全仓同步）: `iteration-schema §5.5 步⑤`、`lifecycle §收口 步⑤`、`versioning-schema §切版自检` 三处的"5 条/5 不变量"同步为 6（含第 6 条条件标注 + 列举补第 6 项）；`/usr/bin/grep` 全仓无残留把一致性自检说成"5 条"的地方（`preference-probe §8 五条隔离` 属无关、不动）。
- [ ] AC5（两态兼容·不砸单文件）: 新收口步 + 新不变量对"仍单文件 `.ai/PROJECT.md` 的项目（含 butler 仓自身）"无损——单文件态显式走旧按需前滚、第 6 不变量显式 N/A；论证 butler 自身**下一次收口**仍能跑通（不被要求折叠进不存在的 `.ai/project/`、第 6 条不假红）；无"要求折叠进空文件夹"的悬空。
- [ ] AC6（产物链·指针不悬空）: `project-digest-schema §6` 折叠模型段与 `§9` R3 前向指针从"**待** R3 接线 / 本轮不实现"翻为"**已**接线"并指向真实落点（`iteration-schema §5.5` / `context-persistence` 第 6 不变量）；全文无"待 R3"与"已接线"自相矛盾的残留。
- [ ] AC7（边界·不越 R5/R6/R8）: `context-persistence §冷启动读序` 第一读仍 `.ai/PROJECT.md`（未切 `00_INDEX`）；`mcv-deployment` / `migrations/` 未改；butler 自身 `.ai/PROJECT.md` 仍单文件结构（只前滚字段、未拆文件夹）；`VERSION` 未动；`git status` 证明这些未在改动集或仅限允许的字段级前滚。
- [ ] AC8（合规·守恒·前滚）: 措辞必须/不得/应、中文说明英文标识符、跨目录引用带目录前缀、增量不 renumber 既有步/不变量号；`.ai/PROJECT.md` 三处前滚到位（收口仪式步④两态 / 一致性自检 5→6 / 知识文件夹 R3 已接线）；`git status` 改动集=6 规则文件 + `.ai/` 台账 + PROJECT.md，无计划外文件、无 rename。

# Verification Method

- AC1–AC2: 逐条读改后 `iteration-schema §5.5` / `milestone-schema §7.4` 步④，确认两分支齐、必做/按需语义清、引用指 §6。
- AC3–AC4: 读 `context-persistence` 第 6 不变量措辞 + 条件标注；`/usr/bin/grep -rn "5 条不变量\|5 不变量" Coder/ templates/ .ai/` 核残留=0（除无关的 preference §8）。
- AC5: 读两态分支 + 第 6 条 N/A 标注，模拟 butler 自身（单文件）收口走位确认不假红、不悬空。
- AC6: 读 `project-digest-schema §6/§9` 确认指针已翻、指向真实落点；grep "待 R3" 无矛盾残留。
- AC7: `git status --short` + 读 `context-persistence §冷启动读序` / `mcv-deployment` / `.ai/PROJECT.md` 结构，证明 R5/R6/R8 未越界。
- AC8: 读措辞 + PROJECT.md 前滚 + `git status` 核守恒、无 rename。
- 全程 P5 起独立复核（fresh-context 子 agent，验证者≠实现者）：逐 AC + 预研保真 + 对抗探测（两态漏一态砸单文件 / 5→6 漏改处 / 越界改读序或部署 / 折叠模型伪接线 / 引用漂移未修）。

# Open Questions / Risks

- 风险：5→6 计数散在多文件，漏改一处即产生"5/6 不一致"新漂移——AC4 专项 grep 全仓兜底。
- 风险：两态里"文件夹态必做"若措辞绝对，会被读成"所有项目都必做"从而砸单文件项目——AC5 专项核 N/A/按需分支显式。
- 已定（承 CONCEPT）：两态兼容为硬约束、非选项；第 6 条带条件；不越 R5/R6/R8；顺修 §5→§6 漂移。
