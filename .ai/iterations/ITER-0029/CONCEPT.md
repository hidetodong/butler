> 分流: 完整 | 命中升级信号: 契约变更、关键路径（活跃收口仪式）、多文件改动、设计取舍（两态兼容）| 2026-07-07 | MILE-0003 R3

# 一句话

R2 只在 `project-digest-schema.md §6` **声明**了知识文件夹的折叠维护模型，把"强制化 + 漂移自检"留给了 R3。这一迭代把它**接线成活跃收口仪式**：①把收口第④步从"按需前滚单文件 `.ai/PROJECT.md`"泛化为"**文件夹态按主题必做折叠 / 单文件暂态前滚**"（泛化 `iteration-schema §5.5` + `milestone-schema §7.4`）；②给冷启动一致性自检加**第 6 条"知识文件夹漂移自检"**（`context-persistence` 真源 + 全仓 5→6 计数同步）。核心设计约束：**两态兼容**——因部署种子（R6）与 butler 自身迁移（R8）都还没落地，此刻绝大多数项目（含 butler 仓自己）仍是单文件 `.ai/PROJECT.md`，新收口步与新不变量**不得砸掉它们的收口**，故"必做折叠 / 漂移自检"只在项目已采用 `.ai/project/` 时生效、单文件态走旧路且第 6 条 N/A。

# Goal

- G1 泛化 `iteration-schema.md §5.5` 收口步④：单文件"按需前滚 PROJECT.md" → 两态（文件夹态=按主题路由 delta 折进 `.ai/project/` 对应文件、**必做**；单文件暂态=前滚 PROJECT.md，保留旧按需语义）。
- G2 泛化 `milestone-schema.md §7.4` 收口步④ 同理（版本级；注明迭代级已增量折叠、里程碑步保版本级全貌一致）。
- G3 在 `context-persistence.md` §冷启动一致性自检（5 不变量真源）新增**第 6 条「知识文件夹漂移自检」**：采用 `.ai/project/` 的项目核对文件夹内容 vs 近期 delta / 现实是否脱节、脱节先暴露；单文件态 N/A（明标条件）。复用 MILE-0001 的自检先例（预研前提 2）。
- G4 全仓「5 条不变量」计数与列举同步 5→6（`lifecycle §收口`、`versioning-schema §切版自检`、`iteration-schema §5.5 步⑤`）——第 6 条带条件标注，防单文件项目假红。
- G5 顺修 R2 遗留漂移：`iteration-schema §5.5` / `milestone-schema §7.4` 里"判据与格式见 `project-digest-schema.md §5`"改指 **§6**（R2 renumber 后 §5=写作密度、§6=折叠模型）。
- G6 把 `project-digest-schema.md §6/§9` 的 R3 前向指针从"**待** R3 接线"翻成"**已**接线（见 iteration-schema §5.5 / context-persistence 第 6 不变量）"，保持产物链引用不悬空；`.ai/PROJECT.md` 按判据前滚（收口仪式 + 一致性自检计数）。

# Current Understanding

- **设计基准**（预研 `MILE-0003-project-knowledge-folder.html §5 前提2 + §6 维护回路`）：delta 按主题路由**必做**（非按需）+ 漂移自检不变量（文件夹 vs 现实脱节先暴露）+ 成本∝改动量不∝文件夹大小（收口是路由不是重推导）+ 落点明写 `iteration-schema §5.5 step④` / `milestone §7.4`。R3 忠实接线，不加自动化（预研 §Out of Scope：本里程碑只定 schema + 手工折叠回路）。
- **两态兼容是 make-or-break**（非选择题）：R3 改的是**活跃收口路径**，它立刻管每个部署项目、也管 butler 仓自己下一次收口（butler 冷启动读这些规则并执行）。而 R6 部署种子 / R8 butler 迁移未落地——此刻含 butler 在内多数项目仍单文件。若把折叠/漂移做成**无条件必做**，单文件项目会被要求"折叠进不存在的 `.ai/project/`"、并在第 6 不变量上永久假红。故两态兼容是硬约束，非可选优化。
- **R2 遗留漂移**：R2 把 schema 从单文件改文件夹时 renumber 了段号（旧 §5 维护前滚 → 新 §6 折叠模型；新 §5 = 写作密度），但 R2 scope 明令不碰 iteration/milestone 收口步，导致这两处"见 §5"现在指错段。R3 重写这两步时一并修正（顺路、零额外风险）。
- **R3 边界**（据 `.ai/MILESTONE.md` 路线图）：本轮=收口回路强制化 + 漂移自检不变量。**不碰**：冷启动读序第一读切到 `00_INDEX`（R5，`context-persistence §冷启动读序` 保持指 PROJECT.md）；部署种子 + 迁移配方（R6）；butler 自身 `.ai/PROJECT.md → .ai/project/` 实体迁移（R8）；说人话（R7）；更新说明 / 查过时帮手（R4）。

# Constraints

- 遵守 butler 编辑规则（`CLAUDE.md`）：不破坏三层分工；不新增规则文件（只改既有）；改动的 schema frontmatter 已合规、不动 audience/scope。
- **两态兼容硬约束**：新收口步 + 新不变量对"仍用单文件 `.ai/PROJECT.md` 的项目（含 butler 自身）"必须无损——单文件态走旧按需前滚、第 6 不变量 N/A；不得让单文件项目收口自检假红或要求折叠进空文件夹。
- **不做无条件 5→6**：第 6 条不变量带条件标注（采用 `.ai/project/` 时适用），计数处如实写"6 条（第 6 条知识文件夹漂移，采用知识文件夹的项目适用）"，不伪装成所有项目都硬跑 6 条。
- **不越 R5/R6/R8**：不改冷启动第一读目标（仍 PROJECT.md）、不加部署种子、不迁移 butler 自身实体、不切版。
- 增量编辑、不 renumber 既有步/不变量号（第 6 条追加在第 5 条后）；文件名互引不写绝对路径、跨目录带目录前缀。

# Impact Scope

- 改（章节级）：`Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5`（步④泛化 + 步⑤ 6 不变量 + §5→§6 修正）、`Coder/20_Workflow_Lifecycle/milestone-schema.md §7.4`（步④泛化 + §5→§6 修正）、`Coder/40_Context_Management/context-persistence.md §冷启动一致性自检`（加第 6 条）、`Coder/20_Workflow_Lifecycle/lifecycle.md §收口`（步④/⑤ 同步）、`Coder/20_Workflow_Lifecycle/versioning-schema.md §切版自检`（5→6）、`Coder/40_Context_Management/project-digest-schema.md §6/§9`（R3 指针 待→已）。
- 收口前滚：`.ai/PROJECT.md`「关键长期决策与不变量」的收口仪式 bullet（步④语义）+ 冷启动读序 bullet（一致性自检 5→6）+ 知识文件夹 bullet（R3 已接线）。
- 明确不影响：P1–P5 状态机、四件套字段、AC 脊柱、hook（收口非 hook 门禁）、迭代/里程碑双层、`.ai/project/` 结构（R2 已定不改）、冷启动第一读目标（R5）、部署种子/迁移（R6）、butler 自身实体迁移（R8）、`VERSION`。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自身），非应用代码工程。未命中任何 `10_Domain_Stack_Profiles/`；按通用 SOP + butler 编辑约束推进。

# Open Questions

- 第 6 不变量的检法写多细？（倾向：给"怎么核"的可操作判据——近期 CHANGELOG delta 是否都已折进对应 topic、有无被取代结论未删——但不写自动化脚本，手工/prompt 级核对。待 P2 定。）
- milestone §7.4 步④ 与 iteration §5.5 步④ 是否完全对称？（倾向：语义对称但注明迭代级已增量折叠、里程碑级只保版本级全貌一致，不重折。待 P2 定。）
