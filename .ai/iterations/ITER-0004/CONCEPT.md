> 分流: 完整路径 | 命中升级信号: 多文件改动 / 契约变更 / 跨模块影响 / 设计取舍 | 2026-06-15

# Goal
- 把生命周期里两个最关键、却唯一没有外化的"控制决策"补成可观测、可审计的产物：① ACK/冻结状态（D1）② 入口分流判定（D4），堵上"内容全外化、控制状态只活在对话里"这个与系统根本原则矛盾的漏洞

# Current Understanding
- review 结论：butler 把"想了什么"（理解/验收/方案）全外化成产物，却没把三个最关键的"控制决策"外化——分流判定、ACK/冻结、收口完成。这三者一旦丢失恰恰无法从产物重建，违反系统自己"不依赖对话记忆"的立身原则。本迭代只做其中两条：D1、D4。
- D1（ACK/冻结状态外化）：`lifecycle.md` 的 P2→P3 / P3→P4 与 `iteration-schema.md §5.2` 的迭代"冻结"是锁定范围的枢纽，但 `phase_gate.py` 只校验产物存在且非空，`acceptance-schema.md` 的 AC_LIST 模板没有任何 ACK 状态字段。后果：会话恢复 / handoff 后无法判断当前 AC_LIST 是"已冻结"还是"等 ACK 的草稿"，hook 也拦不住"一口气写完三件套就改源码、全程零 ACK"。
- D4（入口分流可审计 + 升级转换 + 档位收敛）：完整 vs 简化全靠 AI 自评 6 条升级信号且**不留任何记录**；其中"≥3 文件""跨模块影响"需在分析前估算、易误判；缺"简化→完整"的升级转换定义；存在 极小/简化/完整 三档却只定义了"简化 vs 完整"一个阈值，"极小"是无界逃生口。
- 预期产出：给 AC_LIST 增加冻结状态字段并在生命周期/迭代/规则卡登记；让入口分流落一行可审计记录、定义"简化→完整"升级转换、收敛档位边界；按选定强度决定是否扩展 hook。

# Constraints
- 显性约束：
  - 不破坏既有产物链与三层分层（SOP Core / Domain / Business）。
  - 工作区四件套固定路径不变，保证 `phase_gate` 校验路径零改动。
  - 模板 SSOT 是 `templates/rule-card.md`，凡改强制约束必须同步它（卡片已含 ACK 门与升级信号文案）。
  - 新增 AC_LIST 状态字段须向后兼容：已部署项目的旧 AC_LIST 无该字段时不得被 hook 误杀。
- 隐性约束：
  - 若 D1 选 hook 强制，须同步改 `phase_gate.py`（或激活 `artifact_chain.py`）+ 对应 tests + bypass 叙述；且要诚实认识 hook 只能校验"字段是否标记 frozen"，不能校验"人是否真的 ACK"——其价值在于卡住"忘了等 ACK"的纪律失误，而非防欺骗。
  - 分流记录不得给简化路径增加过重负担，否则简化路径失去存在意义。

# Impact Scope
- 规则层（确定改）：`lifecycle.md`、`acceptance-schema.md`、`iteration-schema.md`、`logic-protocol.md`、`templates/rule-card.md`。
- 规则层（D4 相关）：`concept-schema.md`（完整路径分流记录落点之一）。
- hook 层（取决于 D1 强度选择）：`templates/hooks/rules/phase_gate.py` 或 `artifact_chain.py` + `templates/hooks/tests/`。
- 文档层（按需）：`README.md` / `HUMAN_GUIDE.md` 仅在措辞涉及时同步。
- dogfood：覆写 `.ai/` 四件套为 ITER-0004、收口归档 `.ai/iterations/ITER-0004/`、台账置 closed、`deliveries/ITER-0004-<slug>.md`。
- 明确不影响：里程碑机制、Domain/Stack Profiles、Composer / Learner 子系统、其余三条 review 缺陷（D2/D3/D5/D6 本轮不动）。

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）。
- 未命中任何 Domain / Stack Profile，仅按通用 SOP 推进。

# Open Questions
- Q1（D1 强度）：仅"AC_LIST 加状态字段 + 规则纪律记录 ACK"，还是再加 `phase_gate` hook 强制（`status != ack-frozen` 时拦截源码写操作）？后者更强但要改 hook 代码 + 测试。
- Q2（D4 档位）：把"极小"并入简化路径、收敛为两档（单一阈值）+ 一行轻量分流记录，还是保留三档并各自定义边界？
- Q3（默认方案，可推翻）：分流记录落点——完整路径写进 `CONCEPT.md` 顶部、简化路径写进 `AC_LIST.md` 顶部；ACK 状态用 AC_LIST 顶部 `状态: draft | ack-frozen` + `ACK 日期` 字段表达。
