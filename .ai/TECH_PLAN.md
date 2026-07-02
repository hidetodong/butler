# TECH_PLAN — ITER-0019

# Goal

- 支撑 AC1–AC10：新增 hook 规则机械拦截"未收口先开新迭代"+ 冷启动一致性自检探针（butler 自身可跑）+ 原子收口仪式清单，且不碰 phase_gate/ledger_status 判据、四件套字段、状态机、根 CHANGELOG。

# Files / Modules to Change

- 新增 `templates/hooks/rules/single_active_iteration.py` —— 新规则（AC1/2）。
- 新增 `templates/hooks/tests/test_single_active_iteration.py` —— pytest（AC4）。
- 改 `templates/hooks/butler_gate.py` —— `RULE_MODULES` 注册（ledger_status 之后、artifact_chain 之前）（AC3）。
- 改 `templates/hooks/README.md` —— 规则清单 + 运行机制描述（AC8）。
- 改 `Coder/40_Context_Management/context-persistence.md` —— 冷启动读序新增「一致性自检」5 不变量（AC5/AC6）。
- 改 `Coder/20_Workflow_Lifecycle/iteration-schema.md` —— §5.1 交叉引用 hook 门禁；§5.5 原子有序清单 + 末尾自检步（AC7/AC8）。
- 改 `Coder/20_Workflow_Lifecycle/lifecycle.md §165` —— 收口步同步自检（AC7）。
- 改 `Coder/20_Workflow_Lifecycle/mcv-deployment.md §5` —— hook 注入规则清单加新规则（AC8）。
- 改 `Coder/README.md` —— hook 描述加新规则（AC8）。
- 评估不改 `templates/rule-card.md` —— 门禁不进强制产物集（AC9）。

# Interface / Contract

- **规则判据**：对 `.ai/ITERATIONS.md` 写入，还原写入后全表，统计 `状态==active` 的 `ITER-NNNN` 行数；> 1 即 `deny`（语义=旧迭代未收口/废弃就开新）。
- **effective-text 还原（AC2）**：
  - `Write`：`content` 即写入后全文，直接解析。
  - `Edit`：读现文件文本，对 `old_string` 首次出现替换为 `new_string`，得写入后全文。
  - `MultiEdit`：读现文件，按序套用各 `(old,new)`。
  - **边界**：现文件读失败 / `old_string` 未命中 / 多处歧义 → 退化为只数 incoming 片段的 active 行；片段内 >1 才 deny，否则 allow（allow-on-uncertainty，避免误杀；残留由 Write 全覆写路径 + 冷启动探针兜底）。与 phase_gate 容忍 legacy 同策略。
- **Decision**：`deny` 文案含 active 行的迭代号 + remediation（先按 iteration-schema §5.4/§5.6 收口或废弃旧迭代再开新）。
- **契约不变**：first-deny-wins、fail-closed（顶层 catch）、bypass（BUTLER_BYPASS + bypass-reason）、零三方依赖。
- **一致性自检 5 不变量（AC5）**：① current↔状态（current=ITER-N→该行 active；current=none→无 active）② 至多一个 active ③ 每个 closed 行有收口日期 + 交付链接且 `deliveries/<链接>` 存在 ④ 每个 closed 行有 `iterations/ITER-N/` 归档 ⑤ 里程碑路线项状态与迭代实际状态对账。

# State / Boundary

- 本迭代 = R2（MILE-0001 收尾）：新增 hook 规则 + prompt 级探针 + 收口清单化。
- 不碰：phase_gate / ledger_status 判据、四件套字段 schema、P1-P5 状态机、版本机制、根 CHANGELOG、bypass 机制。

# Design Decisions

- **Q1 命名/落位（定）**：`single_active_iteration.py`，独立规则（不塞进 ledger_status——后者校验枚举值、前者校验跨行不变量，关注点不同）。
- **Q2 effective-text（定）**：读现文件 + 套用替换还原全表，allow-on-uncertainty 兜底（见 Interface）。
- **Q3 自检落点（定）**：内联 `context-persistence.md` 冷启动段（与 ITER-0017 读序同处，控文件数），不单独立 schema。
- **Q4 /close 命令（定：否）**：本迭代只把 §5.5 清单化 + 加自检步；`/close` 语义命令延后（避免 R2 scope 膨胀，记入剩余事项）。
- **butler 自身验证策略**：butler 不跑自己的 hook，hook 规则以 pytest 充当验证（与 ledger_status 等同策略）；prompt 级探针对 butler 可 dogfood。
- Active profiles：Python（hook 子树，零三方依赖、pytest）。

# Execution Steps

- [ ] T1 写 `rules/single_active_iteration.py`：evaluate + effective-text 还原 + 表解析 + active 计数 → AC1/AC2
- [ ] T2 改 `butler_gate.py`：import + `RULE_MODULES` 注册（ledger_status 后）→ AC3
- [ ] T3 写 `tests/test_single_active_iteration.py`：单/双 active、收口同写、Edit 新增 active、MultiEdit、非台账路径、空表、effective-text 还原、uncertainty 兜底 → AC4
- [ ] T4 跑 `cd templates/hooks && python3 -m pytest tests/` 全绿（含既有套件不回归）→ AC4/AC10
- [ ] T5 改 `context-persistence.md` 冷启动段：加「一致性自检」5 不变量 + 漂移先暴露 → AC5/AC6
- [ ] T6 改 `iteration-schema.md` §5.1 交叉引用门禁 + §5.5 原子清单 + 自检步 → AC7/AC8
- [ ] T7 改 `lifecycle.md §165` 收口步同步自检 → AC7
- [ ] T8 改 `templates/hooks/README.md` + `mcv-deployment.md §5` + `Coder/README.md`：注册/描述新规则 → AC8
- [ ] T9 dogfood：对 butler 自身 `.ai/` 跑一遍 5 不变量自检并记录（预期全绿）→ AC9
- [ ] T10 rule-card 裁决：不进强制产物集 + grep 0 命中 → AC9
- [ ] T11 P5 完整审查（危险模式 §7.3）：多维 review 新 Python 规则 + 全量 grep 不变量 + git diff → AC10
- 粒度说明：T1→T2→T3→T4 有依赖链（代码→注册→测试→跑）；T5–T8 文档可并行；T9–T11 收尾。

# Verification Plan

- 按 `AC_LIST.md` Verification Method 逐项核对；危险模式 P5 升格完整审查（§7.3）：重点审 T1 规则的 effective-text 正确性与误杀边界（AC1/2）、T4 pytest 全绿（AC4）、T9 dogfood 自检全绿（AC9）、T11 不变量 grep + git diff（AC10）。Should Fix（若有）记入 VERIFY_REPORT 的 Remaining Risks（按 ITER-0018 新口径）。

# Risks / Open Questions

- **butler 不跑自身 hook**：门禁无法在 butler 内 live 触发，靠 pytest 验证；prompt 探针补 butler 侧。已知设计约束、非缺陷。
- **effective-text 误杀**：allow-on-uncertainty 兜底 + 仅在能正向判定 >1 active 时 deny，最小化误杀；正常"先收口再开新"流程不触发。
- 无遗留 Must Fix；4 个 P1 开放项已落定。
