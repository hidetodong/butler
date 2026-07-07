---
状态: ack-frozen
ACK 日期: 2026-07-07
迭代: ITER-0030
里程碑: MILE-0003 R4
---

> 监督态自驱：本迭代由用户"继续吧"委托执行（非 `/dangerous`），P1–P3 自驱、不设自审门横幅、不写 RUN_LOG；P5 起独立复核子 agent 守质量（重点：两帮手 opt-in 非强制不砸起不了子 agent 的环境 + 不改 R3 折叠必做语义 + scope 不越 R5/R6/R8 + 名册 co-edit 一致）；用户可随时叫停 / 回退（ITER-0030，2026-07-07）。

# Goal

- 把帮手名册的另两个帮手（更新说明 `knowledge-fold` / 查过时 `drift-check`）补成完整中立定义 + 登记 + 接线到 R3 回路（折叠 / 漂移自检）。目标细节见 `CONCEPT.md`，不重述。

# In Scope

- 新建 `knowledge-fold.md`（更新说明帮手：收尾把 delta 折进 `.ai/project/`、只写该目录）+ `drift-check.md`（查过时帮手：抽查说明是否过时、只读）完整定义。
- `overview.md §2` 名册表两行 🔜→✅ + 去占位；co-edit 保持总述↔定义文件一致。
- 最小回指接线：`iteration §5.5 步④` 可唤 knowledge-fold、`context-persistence 第 6 条` 可唤 drift-check。
- `Coder/README.md` 注册两新文件。

# Out of Scope

- 不改 R3 强制语义：折叠仍是收口步④"文件夹态必做"、漂移仍是第 6 条不变量；两帮手是**推荐执行方式**，不写"必须唤帮手"。
- 不追工具层权限硬拦（承 R1：契约约定 + G2 诚实兜底，硬拦留后续）。
- 不做完全无人值守后台自动生成 / 自动跑（本里程碑只做"收尾唤帮手折叠"的定义 + 接线）。
- 不碰冷启动读序第一读切换（R5）、部署种子 + 迁移（R6）、butler 自身实体迁移（R8）、说人话（R7）。
- 不改 P1–P5 状态机 / 四件套字段 / hook / 迭代里程碑双层 / `.ai/project/` 结构 / `VERSION`。

# Acceptance Checklist

- [ ] AC1（帮手·knowledge-fold 定义）: 新建 `Coder/62_Extension_Agents/knowledge-fold.md`，含 §1 一句话 + §2 中立定义表（角色=折叠者/输入=本迭代 CHANGELOG delta + 当前 `.ai/project/`/输出=更新后的说明文件/禁止/隔离=fresh-context/**权限=只准写 `.ai/project/`**）+ §触发（每次收工且动了结构）+ §执行（按主题路由折叠、overwrite 禁历史层、承 `project-digest-schema §6`）+ §输出衔接 + §诚实兜底（回指 `overview §3` G2）；通用规矩 G1–G4 回指 overview 不重写。
- [ ] AC2（帮手·drift-check 定义）: 新建 `Coder/62_Extension_Agents/drift-check.md`，同款结构；角色=查过时者、输入=`.ai/project/` 说明 + 真实代码、输出=哪几处对不上（漂移清单）、**权限=只看不改**、隔离=fresh-context；§触发（冷启动 / 收口抽查，接第 6 不变量）；§输出衔接（落 `.ai/references/`）；G1–G4 回指 overview。
- [ ] AC3（名册·overview co-edit）: `overview.md §2` 名册表更新说明 / 查过时两行状态 🔜 R4 → ✅ 本轮立，"只准碰"列与定义文件权限一致；删 §2 占位说明句（"随 R4 补完整定义…占位"）；同一次编辑完成（co-edit）。
- [ ] AC4（接线·最小回指）: `iteration-schema §5.5 步④` 文件夹态折叠处加一句"（可唤 `62_Extension_Agents/knowledge-fold.md` 帮手 fresh-context 执行）"；`context-persistence §冷启动一致性自检 第 6 条` 加一句"（可唤 `62_Extension_Agents/drift-check.md` 帮手抽查）"；两处**折叠必做 / 漂移强制**语义保持不变（未被改写成"必须唤帮手"）。
- [ ] AC5（定位·不下发 + opt-in）: 两帮手定义只在 `62_Extension_Agents/`、无下发到项目的动作；接线措辞为"可唤 / 推荐"非"必须"；两定义 §诚实兜底均回指 G2（起不了子 agent 则主线做并如实标注"未由帮手执行"，绝不假称）。
- [ ] AC6（规矩·权限约定单源）: 两帮手权限声明（knowledge-fold 只写 `.ai/project/` / drift-check 只读）与 overview 名册表"只准碰"列一致；G1–G4 只回指 `overview §3`、不在两定义里重写；本轮无工具层硬拦（契约约定 + G2）。
- [ ] AC7（边界·不越 R5/R6/R8 + 不改 R3 语义）: R3 的收口步④"文件夹态必做折叠"与第 6 不变量的强制性未被削弱（只加"可唤帮手"选项）；`context-persistence §冷启动读序` 第一读仍 `.ai/PROJECT.md`（未切 00_INDEX）；`mcv-deployment` / `migrations/` / `VERSION` 未改；butler 自身 `.ai/PROJECT.md` 仍单文件；`git status` 证明。
- [ ] AC8（合规·守恒·注册）: 两新文件 frontmatter 标 audience/scope；措辞必须/不得/应、中文说明英文标识符、跨目录引用带目录前缀、增量不 renumber overview 既有节；`Coder/README.md` 注册两文件（目录树 + 分文件说明）；名册自检 3 帮手 ↔ 3 定义文件 ↔ 权限一致（overview §5）；`git status` 改动集=2 新增 + overview/iteration/context-persistence/README + `.ai/` 台账，无 rename、无计划外文件。

# Verification Method

- AC1–AC2: 逐条读两新定义文件确认要素齐（六项中立定义 + 触发 + 执行 + 衔接 + 兜底）、格式与 `independent-review.md` 对齐、权限正确。
- AC3/AC6: 读 `overview.md §2` 名册表核状态/权限一致、占位句已删；grep 两帮手文件确认 G1–G4 回指不重写。
- AC4/AC5/AC7: 读 iteration/context-persistence 两处回指确认"可唤"措辞 + R3 强制语义未变；`git status --short` 证明未触 R5/R6/R8 目标（读序第一读 / mcv / migrations / VERSION / butler PROJECT.md 结构）。
- AC8: 读 frontmatter + README 注册 + overview §5 名册自检（3↔3↔权限）；`git status` 核改动集守恒、无 rename。
- 全程 P5 起独立复核（fresh-context 子 agent，验证者≠实现者）：逐 AC + 预研保真 + 对抗探测（帮手写成"必须唤"砸无子 agent 环境 / 削弱 R3 折叠必做 / 越界 R5/R6/R8 / 权限声明与名册表不一致 / G1–G4 被重写破坏单源 / 帮手定义暗含下发）。

# Open Questions / Risks

- 风险：接线措辞若写成"必须唤帮手折叠"，会让起不了子 agent 的环境卡死收口——AC4/AC5 专项核"可唤"+ G2 兜底。
- 风险：两帮手权限声明与名册表"只准碰"列漂移——AC6 + overview §5 名册自检兜底。
- 已定（承 CONCEPT）：折叠必做（R3）不变、唤帮手 opt-in；权限靠约定 + G2（硬拦留后续）；不越 R5/R6/R8。
