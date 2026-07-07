> 分流: 完整 | 命中升级信号: 新增契约文件、多文件改动、设计取舍（帮手强制度 / 接线粒度）| 2026-07-07 | MILE-0003 R4

# 一句话

R1 把帮手名册骨架立起来了（`62_Extension_Agents/overview.md` 总述 + 复核帮手 `independent-review.md`），名册表里"更新说明""查过时"两行还是 🔜 R4 占位。这一迭代把这两个帮手**补成完整定义并接线**：**更新说明**（`knowledge-fold`）= 收尾时把本迭代 delta 折进 `.ai/project/` 知识文件夹；**查过时**（`drift-check`）= 冷启动 / 收口时对着真实代码抽查说明有没有过时。两者都接到 R3 刚建的回路上——knowledge-fold 接收口步④折叠、drift-check 接第 6 条漂移自检。**定位**：折叠本身 R3 已定为**必做**，这两个帮手是"**推荐唤起的 fresh-context 专职帮手**"（避免主线跑完迭代快没精力时顺手折叠 / 自查，质量差、说明过时）——opt-in 增强、非强制，同复核帮手。

# Goal

- G1 新建 `Coder/62_Extension_Agents/knowledge-fold.md`（更新说明帮手完整定义，镜像 `independent-review.md` 格式：角色/输入/输出/禁止/隔离/权限 + 触发 + 执行 + 输出衔接 + 诚实兜底）；**权限=只准写 `.ai/project/`**，别的不碰。
- G2 新建 `Coder/62_Extension_Agents/drift-check.md`（查过时帮手完整定义，同款格式）；**权限=只看不改**（读 + 搜，输出"哪几处对不上"）。
- G3 `overview.md §2` 名册表：更新说明 / 查过时两行状态 🔜 R4 → ✅ 本轮立；去掉 §2 占位说明句（co-edit：同一次编辑改总述 + 两定义文件）。
- G4 接线到 R3 回路（最小回指）：`iteration-schema §5.5 步④` 文件夹态折叠处注明"可唤 `knowledge-fold` 帮手 fresh-context 执行"；`context-persistence §冷启动一致性自检 第 6 条` 注明"可唤 `drift-check` 帮手抽查"。折叠**必做**语义（R3）不变，唤帮手是推荐执行方式。
- G5 `Coder/README.md` 注册两新文件（目录树 + 分文件说明）。
- G6 两帮手回指 `overview.md §3` 通用规矩 G1–G4（干净上下文 / 叫不起来如实说 / 权限约定 / 中立定义），不重写；权限声明与名册表一致（overview §5 名册自检兜底）。

# Current Understanding

- **设计基准**（预研 `MILE-0003-agent-doc-design.md` §表 + §107/108）：三帮手本轮都做（R1 复核已立，R4 补更新说明 + 查过时）。更新说明"每次收工且动了结构时"把改动清单折进 `.ai/project/`、只改该目录；查过时"冷启动/收工抽查"、只看不改、报哪几处对不上。**为什么非子 agent**：Skill 在同对话跑给不了干净新脑子，检查/折叠图的就是隔离 + 避免主线疲劳。
- **两帮手 = R3 回路的"专职执行者"**：R3 已把"收口折叠"（步④文件夹态必做）和"漂移自检"（第 6 不变量）定成规则；R4 不改这两条的**强制性**，只补"这活推荐派谁做"——knowledge-fold 做折叠、drift-check 做抽查。主线自己做也行（G2：起不了子 agent 就主线做并如实标注），但推荐 fresh-context 帮手做（质量更高）。
- **R4 边界**（据 `.ai/MILESTONE.md` 路线图）：本轮=两帮手定义成型 + 登记 + 接线。**不碰**：冷启动读序第一读切换（R5）、部署种子 + 迁移（R6）、butler 自身实体迁移（R8）、说人话（R7）；不改 R3 折叠必做 / 第 6 不变量的强制语义；不追工具层权限硬拦（承 R1：契约约定 + G2 兜底，硬拦留后续）。

# Constraints

- 遵守 butler 编辑规则（`CLAUDE.md`）：新增规则文件必须在 `Coder/README.md` 注册；frontmatter 标 audience / scope；三层分工不混（帮手名册属扩展模块 62，不混入 SOP Core）。
- **帮手不下发到项目**（承 G4 中立定义）：定义只放 `62_Extension_Agents/`，目标项目用时读、不拷副本。
- **不改 R3 的强制语义**：折叠仍是收口步④"文件夹态必做"、漂移仍是第 6 条不变量；两帮手是"推荐执行方式"，接线用"可唤 / 推荐唤"措辞，不写成"必须唤帮手"（否则起不了子 agent 的环境会卡死收口，违 G2）。
- **权限靠约定 + G2 诚实兜底**：knowledge-fold 只写 `.ai/project/`、drift-check 只读，写进各自定义；本轮不做工具层硬拦（可选增强、留后续）。
- 增量编辑、不 renumber overview 既有节；文件名互引不写绝对路径、跨目录带目录前缀。

# Impact Scope

- 新增：`Coder/62_Extension_Agents/knowledge-fold.md`、`Coder/62_Extension_Agents/drift-check.md`。
- 改（章节级）：`overview.md §2`（名册表两行 + 去占位）、`iteration-schema §5.5 步④`（一句回指 knowledge-fold）、`context-persistence §冷启动一致性自检 第 6 条`（一句回指 drift-check）、`Coder/README.md`（注册两文件）。
- 明确不影响：R3 折叠必做 / 第 6 不变量强制语义、P1–P5 状态机、四件套字段、hook、迭代/里程碑双层、`.ai/project/` 结构、冷启动读序第一读（R5）、部署种子迁移（R6）、butler 自身实体迁移（R8）、`VERSION`。

# Project Type / Active Profiles

- 项目形态：Markdown 规则仓库（butler 自身），非应用代码工程。未命中任何 `10_Domain_Stack_Profiles/`；按通用 SOP + butler 编辑约束推进。

# Open Questions

- 接线粒度：iteration §5.5 步④ + context-persistence 第 6 条各加一句回指是否够？（倾向够——主接线在帮手 §3 触发，schema 侧只需一句可发现性回指，不重复帮手正文。milestone §7.4 步④ 是否也加待 P2 定，倾向由 knowledge-fold 触发覆盖收工不单独加。）
- drift-check 输出落哪？（倾向落 `.ai/references/`，同复核帮手 `insight-*`；待 P2 定。）
- 两帮手"推荐 vs 必须"措辞：确认 opt-in（非强制），承复核帮手先例。
