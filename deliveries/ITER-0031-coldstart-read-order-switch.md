# 冷启动读序切换 + digest-and-point 读纪律（两态第一读）

> ITER-0031 · 迭代交付（小版本）· 收口 2026-07-07 · MILE-0003 R5 · 监督态自驱（用户"继续吧"委托，非 /dangerous；P5 起独立复核守质量）

## 本次交付目标

- R2 立了 `.ai/project/` 知识文件夹契约、R3 把折叠维护 + 漂移自检接成活跃仪式、R4 补齐了执行帮手；但**冷启动到底先读哪个文件**至今写死在 `context-persistence §冷启动读序` 指 `.ai/PROJECT.md`（R2/R3/R4 都明确留给 R5）。知识文件夹再全，AI 冷启动不去读 `00_INDEX` 就白搭。
- R5 补这一环：把"第一读"泛化成**两态**——采用 `.ai/project/` 的项目先读 `00_INDEX` 拿地图、按需钻主题；仍单文件的项目照旧读 `.ai/PROJECT.md`。**这是"知识地图真被用起来"的最后一段接线**。**边界**：R6（部署种子/迁移）、R8（butler 自身迁移 + 切版）仍留后续。

## 已完成内容

- **`context-persistence §冷启动读序` 第 1 项两态化**（主改动）：从写死 `.ai/PROJECT.md` 拆成两个显式分支——采用 `.ai/project/` → 第一读 `00_INDEX.md` + 按需相关主题；仍单文件 `.ai/PROJECT.md`（未迁移暂态，**含 butler 仓自身**）→ 读 `.ai/PROJECT.md`。收尾"互补"句同步两态（项目全貌产物无论文件夹或单文件，均与 handoff 互补）。
- **读侧 digest-and-point 纪律**（读侧对齐写侧）：文件夹态第一读写明"读 `00_INDEX` 拿地图 → 只钻与当前任务相关的主题（**不必一次性读全部**）→ 再按指针钻代码"，点明冷启动预算随文件夹越补越全仍**有界**（读地图 + 定向钻取，不 slurp 整个文件夹）；写侧密度契约仍以 `project-digest-schema §5` 为真源、回指不重抄。
- **翻 `project-digest-schema` R5 指针三处**（一次齐翻，吸取 R3 曾只翻 §9 漏介绍段的教训）：介绍段 line 9 + §9 header（"R3 / R5 已接线；R6 / R8 待实现"）+ §9 R5 路线项（"✅ 已接线"+ 指向真实落点），从"待实现/后续路线项 R5"翻成已接线。
- **README + handoff-spec 两态措辞同步**（只同步措辞、不重写读序）：`README §读取顺序` 冷启动读序描述两态、仍指 `context-persistence §6` 为真源；`handoff-spec §1` "状态全貌由 `.ai/PROJECT.md` 承载"改为两态产物（单文件或 `.ai/project/` 文件夹）。

## 关键变更 / 用户可感知变化

- 采用 `.ai/project/` 知识文件夹的项目，冷启动**从此先读 `00_INDEX` 地图、按需钻主题**——R2 定的文件夹读法从纸面契约变成活跃读序，知识地图真正被用起来。
- **两态兼容是核心设计约束**（同 R3、不是可选优化）：R6 部署种子 / R8 butler 迁移都没落地，此刻含 butler 仓自己在内的绝大多数项目仍是单文件 `.ai/PROJECT.md`、根本没有 `.ai/project/` 目录。冷启动读序是**活规则**（butler 读这些规则冷启动自己）——若把第一读**无条件**改成 `00_INDEX`，单文件项目会被指去读一个**不存在的文件**、当场踩空。故第一读一律**只在项目采用 `.ai/project/` 时切到 `00_INDEX`**，单文件项目继续读 `.ai/PROJECT.md`、不踩空。
- 读纪律让冷启动预算**有界**：知识文件夹随项目越长越全，但冷启动只读地图 + 定向钻取、不 slurp 全部主题。
- 向后兼容：未加部署种子（R6）、未迁移 butler 自身实体（R8）、未改 R3 折叠必做 / 第 6 不变量、未改 `.ai/project/` 结构（R2）、未切版；未动状态机 / 四件套 / hook / 迭代里程碑双层 / `logic-protocol §1.1` 规则加载序。

## 高层影响范围

- 改（章节级，4 规则文件）：`40_Context_Management/context-persistence.md §冷启动读序`、`project-digest-schema.md`（介绍段 + §9）、`Coder/README.md §读取顺序`、`40_Context_Management/handoff-spec.md §1`。
- 收口前滚（本迭代自身，butler 单文件态按需）：`.ai/PROJECT.md` 两处——「冷启动读序固定」条改两态（butler 自身走单文件分支）+ 知识文件夹条 R5 指针翻已接线。
- 没碰（R5 边界）：`mcv-deployment` / `migrations/`（R6）、butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移 + `VERSION` 切版（R8）、`presentation-protocol` / `artifact-style`（R7）、`logic-protocol §1.1`（SOP 规则加载序、正交）、R3 强制语义（折叠必做 / 第 6 不变量）、`.ai/project/` 结构契约。

## 验证方式与结果摘要

- **8/8 AC 通过**，全 **auto·可靠**（规则文档：读正文确认 + `git`/`grep` 核守恒，确定性可复现）；无人测道残余。
- P5 **独立复核**（fresh-context 子 agent，验证者≠实现者）：**核心对抗点（两态兼容）四处逐处 confirm**——context-persistence / project-digest §9 / README / handoff 第一读均两态、单文件分支显式（前两处显式含 butler 自身）、全仓无一处无条件 `00_INDEX`；R5 指针三处齐翻、指真实落点；R3 折叠必做 + 第 6 不变量 + `logic-protocol §1.1` 均不在 diff（一字未动）；scope 未越 R6/R7/R8——**APPROVE，0 Must Fix**。
- 1 Should Fix（收口守门项）：`.ai/PROJECT.md` line 25 读序 + line 29 R5 指针须前滚，否则收口后 line 29 残留"R5 待接线"、line 25 与新两态规则自相矛盾——**已在收口步④落地**。1 Nit（不阻断）：handoff/README 单文件分支未点名 butler（语义完整、不踩空，不改）。
- 守恒核对：`git status` 改动集=4 改规则文件（context-persistence/project-digest-schema/README/handoff-spec）+ `.ai/` 台账 + PROJECT.md 前滚，无新增规则文件、无 rename、未触 `mcv`/`migrations`/`VERSION`/`logic-protocol`。

## 已知剩余风险 / 延后事项

- **两态兼容依赖措辞纪律**（承 R3）：暂态靠"文件夹态第一读 `00_INDEX` / 单文件态第一读 `.ai/PROJECT.md`"显式分支兜住；R6 部署种子 / R8 butler 迁移落地后单文件分支才逐步退场。此前任何改动误把第一读写成无条件 `00_INDEX` 即会砸单文件项目冷启动——已由本轮四处显式分支 + P5 对抗核过兜底。
- **知识文件夹读法尚无真实项目验证**：R5 定的文件夹态第一读要到 R6（部署种子建 `.ai/project/`）/ R8（butler 自身迁移）后才有真项目走这条分支；在此之前含 butler 在内所有项目都走单文件分支，文件夹态读序属"已定义未实跑"。
- 本轮按惯例收口即提交，**未推送、未切版**；MILE-0003 仍 active，剩 R6/R7/R8（v2.0.0 切版在 R8），待用户指令。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 切片：`.ai/iterations/ITER-0031/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 改动：`Coder/40_Context_Management/context-persistence.md`、`project-digest-schema.md`、`handoff-spec.md`、`Coder/README.md`
- 相关契约：`Coder/40_Context_Management/project-digest-schema.md §5`（写侧 digest-and-point 密度真源）、`§6`（折叠模型）
