# 给收口加门槛：执行门禁 hook + 冷启动一致性自检 + 原子收口仪式

> ITER-0019 · 迭代交付（小版本）· 收口 2026-06-30 · 所属 MILE-0001（R2）· /dangerous 危险模式自治执行

## 本次交付目标

- 补用户最初提的"事项 2"：迭代做完后没有硬门槛更新台账 / 产物，收口纪律"有规则、无门槛"，台账↔产物↔交付漂移已实际发生。
- R1（PROJECT.md）、R3（changelog）补了"收口该产出什么"，本轮 R2 补"怎么保证收口真发生、且不漂移"——两条腿：机械门禁（部署项目）+ 一致性自检（人人可跑，含 butler 自身）。

## 已完成内容

- 新增 hook 规则 `templates/hooks/rules/single_active_iteration.py`：写 `.ai/ITERATIONS.md` 后 active 迭代行 >1 即 deny（=上一迭代未收口就开新）；用 effective-text 还原 Write/Edit/MultiEdit 写入后全表，Edit/MultiEdit 无法可靠还原时 allow-on-uncertainty 不误杀。
- 新增 `tests/test_single_active_iteration.py`（15 例），注册进 `butler_gate.py`；`pytest tests/` = 97 passed（原套件无回归）。
- 定义冷启动一致性自检 5 不变量（`context-persistence.md`）：current↔状态 / 至多一个 active / closed 有交付且文件存在 / closed 有归档 / 里程碑路线项对账；落进冷启动读序，漂移先暴露。
- 收口强化为原子仪式：`iteration-schema §5.5` 五步（前三必做 + 第四按需前滚 PROJECT + 第五收口自检），`lifecycle §165` 同步。
- 接线：`iteration-schema §5.1` 交叉引用门禁 + hook README / `mcv-deployment §5` / `Coder/README` 注册描述。

## 关键变更 / 用户可感知变化

- 部署项目里"上一迭代没收口就开新迭代"会被 hook 当场拦下（写台账时机械兜底），不再靠自觉。
- 所有项目（含不跑自身 hook 的 butler）冷启动 + 收口时都跑一遍一致性自检，台账 / 产物 / 交付漂移主动暴露而非事后踩坑。
- 收口从"三步/四步"升级为"五步原子仪式"，最后一步强制自检——收口不再容易半途而废。
- 向后兼容：新增规则 + 文档接线，未动 phase_gate/ledger_status 判据、四件套字段、状态机、根 CHANGELOG。

## 高层影响范围

- 新增：`templates/hooks/rules/single_active_iteration.py`、`templates/hooks/tests/test_single_active_iteration.py`。
- 改（hook）：`butler_gate.py`、`templates/hooks/README.md`；（20/40 层）：iteration-schema、lifecycle、mcv-deployment、context-persistence、Coder/README。
- 没碰：phase_gate/ledger_status 判据、四件套字段 schema、rule-card、P1-P5 状态机、版本机制、根 CHANGELOG。

## 验证方式与结果摘要

- 10 条 AC 全部满足（逐项见 VERIFY_REPORT）；危险模式 §7.3 P5 升格完整多维审查（非简评）：逻辑 / 健壮性 / 安全 / 一致性四维，无 Must Fix。
- `pytest tests/` = 97 passed（新增 15 例 + 原套件零回归）。
- dogfood：对 butler 自身 `.ai/` 跑 5 不变量全绿（唯一 active、18 closed 全有归档 + 交付文件全存在、路线项对账一致）。
- git diff 核对：concept/acceptance/tech-plan/verify schema、根 CHANGELOG、VERSION、rule-card、phase_gate、ledger_status 均未改。

## 已知剩余风险 / 延后事项

- Should Fix（不阻断）：Edit/MultiEdit 在 old_string 未命中现文件时退化为片段计数，可能漏判隐蔽双 active——有意的 allow-on-uncertainty（避免误杀），由 Write 全覆写 + 冷启动自检兜底。
- butler 仓自身不跑 hook → 门禁靠 pytest 验证 + prompt 级自检覆盖 butler 侧（已知设计约束）。
- `/close` 原子收口命令未做（Q4 延后）；收口仪式已清单化 + 自检，命令化留后续 polish。
- 本轮按用户指令只提交推送、不切版；MILE-0001 三路线项已全 closed，聚合发布（切版 + 根 CHANGELOG + migrations）留作后续。

## 引用

- 归档四件套 + 切片：`.ai/iterations/ITER-0019/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 新增代码：`templates/hooks/rules/single_active_iteration.py`、`templates/hooks/tests/test_single_active_iteration.py`
- 改动：`templates/hooks/butler_gate.py`、`templates/hooks/README.md`、`Coder/20_Workflow_Lifecycle/iteration-schema.md`、`lifecycle.md`、`mcv-deployment.md`、`Coder/40_Context_Management/context-persistence.md`、`Coder/README.md`
- 里程碑：`.ai/MILESTONE.md`（MILE-0001 R2，收尾路线项）
