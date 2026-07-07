# TECH_PLAN — ITER-0029（MILE-0003 R3）

> 监督态自驱（非 `/dangerous`）：本产物由用户"继续吧"委托、模型自驱产出，P5 起独立复核守质量（ITER-0029，2026-07-07）。

# Goal

- 支撑 AC1–AC8：把 R2 声明的折叠模型接线成活跃收口仪式——泛化收口步④（两态）+ 加第 6 不变量（条件）+ 全仓 5→6 同步 + 修 §5→§6 漂移 + 翻 R3 指针 + PROJECT.md 前滚。

# Files / Modules to Change

**改（章节级，6 规则文件）**

1. `Coder/20_Workflow_Lifecycle/iteration-schema.md` — §5.5 步④ 改两态（文件夹态按主题折 delta 必做 / 单文件暂态前滚，引用改 §6）；步⑤ 计数 5→6 + 列举补第 6 条（带条件）。→ AC1/AC4/AC5
2. `Coder/20_Workflow_Lifecycle/milestone-schema.md` — §7.4 步④ 两态泛化（注明迭代级已增量折、里程碑保版本级全貌，引用改 §6）。→ AC2/AC5
3. `Coder/40_Context_Management/context-persistence.md` — §冷启动一致性自检 第 5 条后加**第 6 条「知识文件夹漂移自检」**（条件适用 + N/A 标注 + 可操作核法）；不动 §冷启动读序第一读目标。→ AC3/AC5/AC7
4. `Coder/20_Workflow_Lifecycle/lifecycle.md` — §迭代收口段 步④ 语义对齐两态 + 步⑤ 5→6。→ AC4
5. `Coder/20_Workflow_Lifecycle/versioning-schema.md` — §切版自检（当前"5 不变量"）5→6 + 列举补第 6 条（条件）。→ AC4
6. `Coder/40_Context_Management/project-digest-schema.md` — §6 折叠模型段 + §9 R3 前向指针：待→已接线，指向真实落点（iteration-schema §5.5 / context-persistence 第 6 不变量）。→ AC6

**收口前滚（close 步④）**

- `.ai/PROJECT.md` — 「关键长期决策与不变量」：收口仪式 bullet（步④两态语义）+ 冷启动读序 bullet（一致性自检 5→6）+ 知识文件夹 bullet（R3 已接线）。→ AC8

# Design Decisions

- **DD1 两态措辞用显式分支**：步④写"若项目已采用 `.ai/project/`（知识文件夹）：…必做折叠；若仍单文件 `.ai/PROJECT.md`（未迁移暂态）：…按需前滚"，两分支并列可见，不用"泛化后按需即必做"这类会被误读成无条件的写法。（对 AC1/AC2/AC5）
- **DD2 第 6 不变量定为条件不变量**：不做无条件 5→6。第 6 条正文首句即"（条件：项目采用 `.ai/project/` 知识文件夹时适用；仍单文件 PROJECT.md 的项目 N/A）"。计数处统一写"6 条（第 6 条为知识文件夹漂移，采用知识文件夹的项目适用）"。（对 AC3/AC4/AC5）
- **DD3 第 6 不变量放 context-persistence 真源、其余处引用计数**：定义只在 `context-persistence §冷启动一致性自检` 一处写全（DRY）；`iteration-schema/lifecycle/versioning` 只同步"6 条"计数 + 一句列举，不重抄核法。（对 AC4，最小实现纪律 §4 修根因/单源）
- **DD4 §5→§6 引用顺修、不扩范围**：只把两处"project-digest-schema.md §5"改成 §6，不重写这两步的其它内容。（对 AC1/AC2）
- **DD5 R3 指针翻面不删声明**：`project-digest-schema §6` 保留折叠模型正文，只把"待 R3 接线 / 本 schema 不实现 / 在 R3 接线前…"这几句改成"R3 已接线（见 …）"；§9 R3 条同改。不动 R5/R6/R8 指针（仍"待"）。（对 AC6/AC7）
- **DD6 读序第一读不碰**：`context-persistence §冷启动读序` 的 1. `.ai/PROJECT.md` 第一读**保持不变**（切 00_INDEX 是 R5）；只在其下方 §冷启动一致性自检加第 6 条。（对 AC7）

# Execution Steps（镜像到 task-state）

- [ ] T1 改 `iteration-schema §5.5`：步④两态 + §5→§6 + 步⑤ 5→6 → AC1/AC4/AC5
- [ ] T2 改 `milestone-schema §7.4`：步④两态 + §5→§6 → AC2/AC5
- [ ] T3 改 `context-persistence §冷启动一致性自检`：加第 6 条（条件 + 核法）→ AC3/AC5
- [ ] T4 改 `lifecycle §收口` + `versioning-schema §切版自检`：5→6 同步 → AC4
- [ ] T5 翻 `project-digest-schema §6/§9` R3 指针（待→已）→ AC6
- [ ] T6 自检：`grep` 全仓 5→6 无残留 + §5→§6 已修 + git status 证明未越 R5/R6/R8 → AC4/AC7/AC8
- [ ] T7 P5 独立复核子 agent（两态兼容 + 计数守恒 + scope 边界 + 预研保真）

# Test / Verify Strategy

- 全 AC 属文档类：读改后正文确认要素齐 + `/usr/bin/grep` 核计数守恒（`auto·可靠`，确定性可复现）。
- 关键对抗核：模拟 butler 自身（单文件）走新收口步④ + 第 6 不变量，确认命中"单文件暂态/N/A"分支、不假红、不悬空。
- `git status --short` 证明改动集=6 规则文件 + `.ai/` 台账 + PROJECT.md，无 rename、未触 `mcv-deployment`/`migrations/`/`VERSION`、`context-persistence` 读序第一读未改。

# Risks / Rollback

- 风险：5→6 漏改一处 → T6 全仓 grep 兜底。
- 风险：两态漏写单文件分支 → AC5 + P5 专项。
- 回滚：全为文本增量改动，`git checkout -- <file>` 可逐文件回退；未切版、未动 hook/桥。
