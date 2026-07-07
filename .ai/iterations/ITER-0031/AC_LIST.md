---
状态: ack-frozen
ACK 日期: 2026-07-07
迭代: ITER-0031
里程碑: MILE-0003 R5
---

> 监督态自驱：本迭代由用户"继续吧"委托执行（非 `/dangerous`），P1–P3 自驱、不设自审门横幅、不写 RUN_LOG；P5 起独立复核子 agent 守质量（重点：第一读切换是否两态·不砸单文件项目 + 未越 R6/R8 + 不改 R3 强制语义 + digest-and-point 读纪律落位）；用户可随时叫停 / 回退（ITER-0031，2026-07-07）。

# Goal

- 把冷启动"第一读"从写死 `.ai/PROJECT.md` 泛化成两态（文件夹态先读 `00_INDEX` + 按需主题 / 单文件态读 `.ai/PROJECT.md`），并补 digest-and-point 读侧纪律。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- `context-persistence §冷启动读序` 第 1 项两态化 + 收尾互补句同步 + 加读侧 digest-and-point 纪律。
- `project-digest-schema` 介绍段 + §9 的 R5 指针翻"已接线（两态）"。
- `Coder/README.md §读取顺序` 冷启动读序描述两态化。
- `handoff-spec §1` 状态全貌承载产物措辞两态化（仍指 context-persistence §6 为读序真源）。

# Out of Scope

- 不碰 R6：`mcv-deployment`（部署仍种单文件）、`migrations/`。
- 不碰 R8：butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移、`VERSION` / 切版。
- 不碰 R7：`presentation-protocol` / `artifact-style` 说人话。
- 不改 R3 强制语义（折叠必做 / 第 6 不变量）、不改 `.ai/project/` 结构契约（R2 已定）、不改 `logic-protocol §1.1`（SOP 规则加载序、非产物冷启动序）。
- 不动 P1–P5 状态机 / 四件套字段 / hook / 迭代里程碑双层。

# Acceptance Checklist

- [ ] AC1（读序·两态第一读）: `context-persistence §冷启动读序` 第 1 项由写死 `.ai/PROJECT.md` 改为**两态分支**——采用 `.ai/project/` 的项目第一读 `00_INDEX.md` + 按需相关主题；仍单文件 `.ai/PROJECT.md` 的项目（未迁移暂态）第一读 `.ai/PROJECT.md`。两分支均标明"冷启动第一读"、格式指 `project-digest-schema.md`。
- [ ] AC2（读序·digest-and-point 读纪律）: 文件夹态第一读处写明读侧纪律——读 `00_INDEX` 拿全貌与地图 → 按当前任务需要钻相关主题文件（**不必一次性读全部主题**）→ 再按指针钻代码；点明冷启动预算随之有界（读地图 + 定向钻取，不 slurp 整个文件夹）。
- [ ] AC3（读序·互补句同步）: `§冷启动读序` 收尾"PROJECT.md 与 handoff 互补"句改为两态措辞（项目全貌产物无论单文件或文件夹，均与 handoff 互补：前者给系统整体状态、后者给此刻断点），不残留只提 `.ai/PROJECT.md` 的单文件中心表述。
- [ ] AC4（指针·翻 R5 已接线）: `project-digest-schema` 介绍段（"第一读切到 `00_INDEX` 是后续路线项 R5"）+ §9 R5 路线项 + §9 header（"R3 已接线；R5/R6/R8 待实现"）翻为"读序切换已由 R5 接线（两态）"；指向真实落点（`context-persistence §冷启动读序` 两态第 1 项），R6/R8 仍标待实现。
- [ ] AC5（同步·README 读序）: `Coder/README.md §读取顺序` 冷启动读序描述改两态（文件夹态 `00_INDEX` + 按需主题 / 单文件态 `.ai/PROJECT.md`），仍指 `context-persistence.md §6` 为读序细节真源。
- [ ] AC6（顺修·handoff-spec 措辞）: `handoff-spec §1` "项目的状态全貌由 `.ai/PROJECT.md` 承载"改为两态产物措辞（单文件 `.ai/PROJECT.md` 或 `.ai/project/` 知识文件夹），仍指 `context-persistence §6` 为冷启动读序真源、不在此重写读序。
- [ ] AC7（边界·不越 R6/R8/R7 + 不改 R3 语义）: R3 折叠必做 / 第 6 不变量强制性未被改动；`.ai/project/` 结构契约（R2）未改；`mcv-deployment` / `migrations/` / `VERSION` 未改；`logic-protocol §1.1` 未改；butler 自身 `.ai/PROJECT.md` 仍单文件（只字段前滚、未拆文件夹）；`git status` 证明。
- [ ] AC8（合规·守恒·两态兼容）: 措辞必须/不得/应、中文说明英文标识符、跨目录引用带目录前缀、增量不 renumber 既有节；两态第一读的**单文件分支显式保留**（模拟 butler 自身冷启动仍走 `.ai/PROJECT.md`、不被指向不存在的 `00_INDEX`）；`.ai/PROJECT.md` 收口前滚两处（读序两态 + R5 指针）；`git status` 改动集=4 改规则文件（context-persistence/project-digest-schema/README/handoff-spec）+ `.ai/` 台账，无新增规则文件、无 rename、无计划外文件。

# Verification Method

- AC1–AC3: 逐条读改后 `context-persistence §冷启动读序` 正文，确认第 1 项两分支齐、读侧 digest-and-point 纪律在、互补句两态。
- AC4/AC5/AC6: 读 `project-digest-schema` 介绍段/§9、`README §读取顺序`、`handoff-spec §1`，确认 R5 指针翻已接线、README/handoff 两态措辞、指向真源不重写读序。
- AC7/AC8: `git status --short` 证明未触 `mcv-deployment`/`migrations/`/`VERSION`/`logic-protocol`、butler `.ai/project/` 不存在（仍单文件）；grep R3 强制语义（折叠"必做" / 第 6 不变量）未被本轮改动；模拟单文件项目走单文件分支无踩空；改动集守恒、无 rename、无新增规则文件。
- 全程 P5 起独立复核（fresh-context 子 agent，验证者≠实现者）：逐 AC + 预研保真 + 对抗探测（第一读写成无条件 `00_INDEX` 砸单文件项目 / 漏一态 / 越界改 R6 部署或 R8 迁移或切版 / 误改 R3 强制语义 / digest-and-point 读纪律缺失 / R5 指针伪翻未指真实落点）。

# Open Questions / Risks

- 风险（make-or-break）：第一读若写成无条件 `00_INDEX`，会砸掉含 butler 自身在内所有单文件项目的冷启动（指向不存在文件）——AC1/AC8 专项核两态分支 + 单文件分支显式保留。
- 风险：R5 指针只翻一半（§9 翻了、介绍段没翻，同 R3 曾漏 line 9）——AC4 专项核介绍段 + §9 + header 三处齐翻。
- 已定（承 CONCEPT）：两态纪律与 R3 收口步④/第 6 不变量同源；不越 R6/R8/R7；不改 R3 强制语义与 `.ai/project/` 结构。
