> ITER-0034 · MILE-0003 R8 段A（dogfood 迁 .ai/project/ + 对齐现实）· 收口即归档

本文件是**当前活跃迭代**的对象级变更流（ADD/EDIT/DELETE）。段A（迁移 + 对齐）的切片如下；段B（切 v2.0.0 发布）为独立 `chore(release)` 动作，其记录入 `CHANGELOG.md` + `migrations/v2.0.0.md`，不进本迭代变更流。收口时本切片归档至 `iterations/ITER-0034/CHANGELOG.md`。

## ADD

- `.ai/project/00_INDEX.md` — butler 知识文件夹入口，R2 §8 三块（一段话是什么 + 读序地图 + 7 主题登记表）。→ AC1
- `.ai/project/identity.md` — 定位 / 目的 / 使用者 / 边界（迁自旧单文件"目的"段）。→ AC2
- `.ai/project/architecture.md` — 三层模块地图 + 成熟度层，目录树 / 分层指 README 不抄。→ AC2/AC3
- `.ai/project/capabilities.md` — 现状能力（命令 / P1–P5 SOP / 驻留工具 / 帮手），R2 新增层。→ AC2
- `.ai/project/invariants.md` — 关键长期决策与不变量（迁自旧"不变量"段 + butler 转文件夹态）。→ AC2
- `.ai/project/constraints.md` — 现行约束（迁自旧"约束"段）。→ AC2
- `.ai/project/debt.md` — 已知长期欠债（迁自旧"欠债"段）。→ AC2
- `.ai/project/frontier.md` — 当前形态 / 活跃战线 / 下一瓶颈，R2 新增层。→ AC2

## EDIT

- `.ai/task-state.md` — 冷启动入口 `.ai/PROJECT.md` → `.ai/project/00_INDEX.md`、butler 自身描述转文件夹态。→ AC6
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md §2`（line 47）— 单文件全貌产物形态例子去掉"R8 前 butler 仓自身"、注明 butler 已迁；单文件分支保留给老项目。→ AC7
- `Coder/40_Context_Management/context-persistence.md §6`（line 125）— 单文件第一读分支去"含 butler 仓自身"、注 butler 走文件夹分支；分支逻辑保留。→ AC7
- `Coder/40_Context_Management/project-digest-schema.md §9`（line 147/149/151/152）— 路线状态 R8 待实现→已接线（ITER-0034）、暂态说明改两态并存说明。→ AC7

## DELETE

- `.ai/PROJECT.md` — 内容已按主题迁入 `.ai/project/`（`[split]` 作用于 butler 自身）；全仓无 butler 自身全貌产物的踩空活引用。→ AC5
