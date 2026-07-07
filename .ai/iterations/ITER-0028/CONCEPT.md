> 分流: 完整 | 命中升级信号: 契约变更、关键路径、设计取舍 | 2026-07-06 | MILE-0003 R2

# 一句话

butler 冷启动读的"项目整体"产物现在是单文件 `.ai/PROJECT.md`——一份 ≤1500 tokens 的**薄索引**（几个关键词 + "细节看代码"），AI 读完并不真懂"项目里有什么"。这一迭代把它的**格式契约**（`project-digest-schema.md`）从"单文件薄索引"改写成"**知识文件夹** `.ai/project/`"：一个 `00_INDEX.md` 入口 + 按主题分文件（identity / architecture / capabilities / invariants / constraints / debt / frontier）+ 每份边界 + 写作密度口径。这是 MILE-0003 主体的开篇（哲学切换：薄索引 → 随迭代越补越全的知识地图），**本轮只定 schema**，强制折叠接线（R3）/ 读序切换（R5）/ 部署迁移（R6）/ butler 自身转换（R8）都留后续路线项。

# Goal

- G1 改写 `Coder/40_Context_Management/project-digest-schema.md`：从 `.ai/PROJECT.md` 单文件契约 → `.ai/project/` 知识文件夹契约。
- G2 定文件夹结构 + `00_INDEX.md` 入口契约 + 推荐核心 topic 集 + 每份边界（有界、可整篇读完、满则拆新文件）+ 写作密度口径（digest-and-point：每项 + 干什么 + 真源，已有真源不复制）。
- G3 钉哲学切换的三条矛盾消解（防"完整"变成"腐坏的谎"）：完整=广度覆盖≠细节深度、体积∝项目复杂度不∝迭代数、overwrite 当前真相禁历史层。
- G4 声明维护折叠模型 + 受控扩展登记（新 topic 登记进 00_INDEX，承"注册即真源、无隐式依赖"老不变量）；强制接线指明由后续路线项落、不在本轮实现。
- G5 更新 `Coder/README.md` 对本 schema 的描述行（反映文件夹契约），保持注册准确。

# Current Understanding

- 现 schema（`project-digest-schema.md`）的明文价值本轮要**有意反转**：`≤1500 tokens`「摘要不是百科」→ 越补越全；「指针化·深内容不内嵌」→ 装消化过的真内容；「多数迭代只动 0-2 行·避免维护膨胀」→ 每次收口按主题折叠。这不是"切几块"，是从薄索引到实体知识库的**哲学切换**（预研 `MILE-0003-project-knowledge-folder.html §3`）。
- 设计已在预研拍板（该 HTML §5 四前提 + §7 结构/密度样例 + `preresearch-brief §5`）：topic 集与密度以 HTML 草案为基础定稿；本轮把草案坐实进 schema。
- **最大风险**（预研 §8）：陈旧的完整比诚实的薄更毒——立志完整却没严格维护的知识库会变成"自信的谎"。整套设计生死系于"强制 + 可验证的收口折叠"（预研前提 2）。但那条**强制接线是 R3**，本轮 schema 只**声明**折叠模型、把强制化留给 R3，故本轮 schema 必须写清"模型在此、强制在 R3"，不制造"schema 要求了但没人强制"的假象——用"待后续路线项接线"如实标注。
- R2 边界（据 `.ai/MILESTONE.md` 路线图）：本轮=**改写 schema 文档**一件事。R3=维护回路强制化 + 漂移自检不变量；R5=冷启动读序切换 + digest-and-point 接进 context-persistence；R6=部署种子 + 迁移配方；R8=butler 自身 `.ai/project/` 重写 + 切版。四者本轮**都不碰**。

# Constraints

- 遵守 butler 编辑规则（`CLAUDE.md`）：不破坏三层分工；schema 文件已在 `Coder/README.md` 注册（改描述、不新增文件）；frontmatter 标 audience / scope。
- **文件名不改**（沿用 `project-digest-schema.md`，"digest" 为旧名）：改名会连锁 5+ 处跨文件引用（README / iteration-schema / milestone-schema / context-persistence / mcv-deployment）失效；按最小实现纪律不 rename、只改内容，rename 留后续顺手 tidy。
- **不动** `.ai/PROJECT.md`（butler 自身仍单文件，转换是 R8）、`iteration-schema §5.5`、`milestone-schema §7.4`、`context-persistence §6`、`mcv-deployment`、`migrations/`——这些是 R3/R5/R6/R8。
- 四产物边界不越位：`.ai/project/`（状态积分）vs `ITERATIONS`（变更流 delta）vs `handoff`（瞬时断点）vs `MILESTONE`（版本范围）——知识文件夹**不得**变成变更流。
- 措辞面向 AI 执行：必须 / 不得 / 应；中文说明、标识符与文件名用英文；文件名互引不写绝对路径。

# Impact Scope

- 改写：`Coder/40_Context_Management/project-digest-schema.md`（单文件契约 → 文件夹契约，整篇重写）。
- 改（一行）：`Coder/README.md` 分文件说明里 project-digest-schema 的描述（反映文件夹）。
- 收口前滚：`.ai/PROJECT.md`「关键长期决策与不变量」按需记"知识文件夹契约已定（R8 自身适配）"（close 步④按判据）。
- 明确不影响：P1–P5 状态机、四件套（CONCEPT/AC/TECH/VERIFY）字段、AC 脊柱、hook、迭代/里程碑双层、`.ai/PROJECT.md` 现结构、iteration/milestone/context-persistence/mcv-deployment 正文、`VERSION`。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自身），非应用代码工程。
- 未命中任何 `10_Domain_Stack_Profiles/`；按通用 SOP + butler 自身编辑约束（`CLAUDE.md`）推进。

# Open Questions

- topic 集定几个、名字？（倾向照预研 §7 草案：`00_INDEX` + identity/architecture/capabilities/invariants/constraints/debt/frontier，标"推荐核心集、可受控扩展"。待 P2 定。）
- schema 里维护折叠模型写多深？（倾向只**声明**折叠模型 + 明标"强制化 + 漂移自检接线由 R3 落"，不写具体收口步改动。待 P2 定。）
- 文件是否顺手改名 `project-knowledge-schema.md`？（倾向**不改**——连锁引用失效、违最小实现纪律；留后续。待 P2 定。）
