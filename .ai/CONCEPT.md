# CONCEPT — ITER-0019

> 分流：完整路径 | 命中升级信号：跨模块改动（hook 代码 + 多处规则）、新增 hook 规则契约、含可执行代码与测试 | 2026-06-30

## 一句话

收口纪律目前"有规则、无门槛"——`iteration-schema §5.5` 写了收口四步、`§5.1` 写了"上一迭代未收口不得开新"，但全靠 AI 自觉；台账 / 产物 / 交付三者漂移已实际发生过（本会话开局就撞见 v0.2.0 时代的陈旧 handoff）。本迭代给收口加门槛：① 部署项目用 **hook 机械拦截**"上一迭代没收口就开新迭代"；② 给所有项目（含 butler 自身）一个 **冷启动一致性自检探针**，把台账↔产物↔交付的漂移在冷启动 / 收口时主动揪出；③ 把收口固化成 **原子仪式清单**，末尾跑一遍自检，杜绝半途而废。这是 MILE-0001 的收尾路线项 R2。

## 背景与判断

- 这是用户最初提的"事项 2"：迭代做完后没有硬门槛去更新台账 / 产物，更新不及时。R1（PROJECT.md）、R3（changelog）补了"收口该产出什么"，R2 补"怎么保证收口真发生、且一致"。
- butler 仓自身不跑自己的 hook（规则仓非部署项目，长期欠债），所以纯 hook 方案救不了 butler 自己——必须同时有一个 **prompt 级探针**，对 butler 与部署项目都生效。两条腿走路：机械门禁（部署项目）+ 自检探针（人人可跑）。
- hook 体系已成熟（`butler_gate.py` 派发 + `phase_gate` / `ledger_status` 等规则 + pytest 套件 + bypass）。新增"开新迭代门禁"是顺势加一条规则，风险可控、可测。
- 执行门禁的机械判据选**"ITERATIONS 写入后 active 行 ≤ 1"**：开新迭代=新增 active 行，若旧迭代没先收口/废弃，台账就会出现 ≥2 个 active 行——这个不变量确定、可解析、与 §5.1 语义等价。

## 目标（Goal）

- G1：新增 hook 规则拦截"未收口先开新迭代"——`.ai/ITERATIONS.md` 写入后 active 迭代行 > 1 即 deny；注册进派发器、配 pytest（含 Write / Edit / MultiEdit 与 effective-text 还原）。
- G2：定义 **冷启动一致性自检**：台账↔产物↔交付的不变量清单（current↔状态、closed 行须有收口日期+交付链接+归档目录、单 active、里程碑路线项状态对账），落进冷启动读序，漂移则先暴露。
- G3：把收口固化成 **原子仪式**：`§5.5` 强化为有序清单（含 R1 前滚 + R3 changelog），末尾加"收口自检"步跑 G2 探针；评估是否给 `/close` 语义命令。
- G4：接线——hook README / `mcv-deployment §5` / `Coder/README` hook 描述 / `iteration-schema §5.1` 交叉引用新门禁；dogfood：butler 自身跑一遍一致性自检（现状应全绿）。

## 约束（Constraints）

- hook 守现有契约：零三方依赖、fail-closed、first-deny-wins、bypass 机制不变；改 hook 必跑 `pytest tests/`。
- 探针对 butler 自身可跑（不依赖 hook 运行），这是设计硬要求。
- 不改四件套字段结构、AC 脊柱、P1-P5 状态机；不改既有规则（phase_gate / ledger_status）的判据，只新增。
- 守本仓五约束（分层 / 产物链 / 无隐式依赖 / 模板单一来源 / audience 标注）。

## 影响范围（Impact Scope）

- 新增：`templates/hooks/rules/<新规则>.py` + `templates/hooks/tests/test_<新规则>.py`。
- 改（hook）：`butler_gate.py`（注册规则）、`templates/hooks/README.md`（规则清单/运行机制）。
- 改（规则）：`iteration-schema.md`（§5.1 交叉引用门禁、§5.5 原子清单+自检）、`lifecycle.md §165`（收口步同步）、`40_Context_Management/context-persistence.md`（冷启动一致性自检）、`mcv-deployment.md §5`（hook 注入清单）、`Coder/README.md`（hook 描述 + 注册）。
- 评估：是否新增 `/close` 命令（P3 定）；`rule-card`（是否提门禁，倾向不改）。
- 不影响：四件套字段 schema、phase_gate/ledger_status 判据、P1-P5 状态机、版本机制、根 CHANGELOG。

## 项目类型与 Profiles

Markdown 规则仓 + Python hook（零三方依赖、pytest）。Profile：Python（hook 子树）。

## 待澄清（Open Questions）

- Q1：新规则命名与落位（倾向 `single_active_iteration.py` 或 `iteration_open_gate.py`，独立规则而非塞进 ledger_status）。（P3 定）
- Q2：Edit/MultiEdit 的 effective-text 还原——读现文件 + 套用替换后再解析全表（避免 Edit 片段只见新行漏看旧 active）。确认实现口径。（P3 定）
- Q3：一致性自检落点——`context-persistence` 冷启动段内联，还是单独 schema？倾向内联（控文件数、与 ITER-0017 读序同处）。（P3 定）
- Q4：是否新增 `/close` 命令？倾向否（先把 §5.5 清单化 + 自检；命令是后续 polish），避免 R2 scope 膨胀。（P3 定）
