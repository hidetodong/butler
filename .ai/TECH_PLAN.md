# Goal
- 支撑 AC1–AC7：新增迭代机制 SSOT 并把迭代号 / 台账 / 归档 / 收口纪律织进 SOP，再在 butler 自身 dogfood 验证

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/iteration-schema.md` — 新建：迭代号、台账字段、三层落盘、锁定纪律（机制 SSOT）
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — P1 开启、P2 ACK 冻结、§4 工作区/归档关系、P5 收口三步、§5 修订 vs 扩张分流
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — §2 把 `ITERATIONS.md` 列入运行态文件、四件套标注当前迭代工作区、`iterations/` 归档目录按需产生
- `Coder/20_Workflow_Lifecycle/delivery-summary.md` — §3 命名带迭代号、§7 收口联动、§8.4 引用格式
- `Coder/README.md` — 目录结构树 + 读取顺序说明注册 `iteration-schema.md`
- `templates/rule-card.md` — 新增"迭代化需求"精简段
- dogfood：`.ai/ITERATIONS.md`（新建）、`.ai/iterations/ITER-0001/`（归档 chat-recap-style）、`.ai/iterations/ITER-0002/`（归档本迭代）、`deliveries/ITER-0002-iteration-requirement-mgmt.md`（新建）、`.ai/{CONCEPT,AC_LIST,TECH_PLAN,VERIFY_REPORT}.md`（覆写为本迭代）

# Interface / Contract
- `iteration-schema.md` 对外承诺：迭代号格式 `ITER-NNNN`、台账 `current` 指针 + 状态机（active/closed/abandoned）、收口三步（快照 + 交付 + 台账）
- 工作区四件套路径契约不变：`.ai/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`，保证 hook `phase_gate` 零改动
- `.ai/ITERATIONS.md` 承诺：`current` 与状态列一致、迭代号单调不复用

# State / Boundary
- 状态边界：迭代是套在 P1–P5 外层的需求锁定单元，不新增阶段
- 模块职责边界：`iteration-schema.md` 管机制定义，`lifecycle.md` 管阶段接入点，二者引用不复制
- 不在范围内：hook 体系、其他 schema、历史 deliveries 重命名、`CLAUDE.md.template` 骨架（占位符自动透传 rule-card）

# Design Decisions
- 落盘选"工作区 + 收口归档"而非"迭代目录即工作区"：保固定路径 → hook 一行不改，契合现有"热数据 + 冷归档"哲学（`mcv-update.md`）
- 编号选递增零填充 `ITER-NNNN`：单调、可排序、无歧义，台账记号→标题映射
- 锁定纪律选"允许修订、扩张才开新迭代"：迭代内小幅改 AC 重新 ACK + 修订记录；命中回退/升级信号的扩张才强制开新迭代
- dogfood 把现有 chat-recap-style 归档为 ITER-0001、本次为 ITER-0002，验证机制端到端自洽
- 未命中任何 Domain / Stack Profile；仅按通用 SOP 推进

# Execution Steps
- Task 1: 新建 `iteration-schema.md`（SSOT）
- Task 2: 改 `lifecycle.md`（P1/P2/§4/P5/§5 五处接入）
- Task 3: 改 `mcv-deployment.md §2`
- Task 4: 改 `delivery-summary.md`（§3/§7/§8.4）
- Task 5: 改 `README.md`（树 + 说明列表）
- Task 6: 改 `rule-card.md`（迭代化需求段）
- Task 7: dogfood — 归档 ITER-0001、覆写工作区为 ITER-0002、建台账、归档 ITER-0002、写交付、收口

# Verification Plan
- AC1–AC5: 逐文件阅读核对新增/修改段落与 AC 映射
- AC6: `git status -- templates/hooks/` 无改动；复核 `lib/io.py` `GATED_BLACKLIST`
- AC7: 列 `.ai/iterations/` 目录树，比对 `ITERATIONS.md` 与 `deliveries/`

# Risks / Open Questions
- 覆写工作区四件套会丢失 chat-recap-style 工作区内容，但已先快照到 ITER-0001 且 git 历史保留
- 台账长期增长需后续按 `mcv-update.md` 归档冷行；本迭代仅 2 行，暂不触发
- 无未决问题
