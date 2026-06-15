---
状态: ack-frozen
ACK 日期: 2026-06-15
---

# Goal
- 把 ACK/冻结状态（D1）与入口分流判定（D4）从对话内的隐性控制决策，变成 AC_LIST 产物里可观测、hook 可校验的外化状态，并补齐三档分流边界与"低档→高档"升级转换

# In Scope
- D1：AC_LIST 增加冻结状态字段（`状态` + `ACK 日期`）；`lifecycle.md` / `iteration-schema.md` / `acceptance-schema.md` / `templates/rule-card.md` 登记其语义与状态机（含 amend 退回 draft）；扩展 `phase_gate.py` 在 draft 时拦截源码写、对无字段旧文件 legacy 放行；补 hook 测试。
- D4：`lifecycle.md §2` 显式定义 极小/简化/完整 三档边界；要求一行分流记录（落点：完整→CONCEPT、简化→AC_LIST、极小→口头）；定义"低档→高档"升级转换；`logic-protocol.md §5` 与 `templates/rule-card.md` 同步。
- dogfood：本迭代 CONCEPT 带分流记录、AC_LIST 带状态字段并走 draft→ack-frozen，ITER-0004 正常收口。

# Out of Scope
- D2 / D3 / D5 / D6 四条 review 缺陷（本轮不动）。
- 里程碑机制、Domain/Stack Profiles、Composer / Learner 子系统。
- 旧已部署项目 AC_LIST 的批量回填状态字段（靠 legacy 放行兼容，不强制迁移）。

# Acceptance Checklist
- [ ] AC1: `acceptance-schema.md` 的 AC_LIST 必填字段与模板含 `状态`(draft|ack-frozen) 与 `ACK 日期`，并说明语义：draft = 写完待 ACK、ack-frozen = 已确认冻结。
- [ ] AC2: `lifecycle.md` P2 强制规则写明：AC_LIST 初始 `draft`，用户 ACK 后置 `ack-frozen` + 日期方可进 P3；`/dangerous` 模式由自审门替代后由模型置位；迭代内 amend 须把状态退回 `draft` 再重新 ACK。
- [ ] AC3: `iteration-schema.md §5.2 冻结` 把"冻结"物化为 AC_LIST `状态: ack-frozen`，§5.3 amend 同步要求状态退回 `draft`。
- [ ] AC4: `phase_gate.py` 在 AC_LIST 存在且 `状态` 字段值为 `draft` 时 deny 源码写（reason / remediation 指向"AC_LIST 待 ACK 冻结"）；AC_LIST 无 `状态` 字段时按 legacy 放行（向后兼容）。
- [ ] AC5: `templates/hooks/tests/` 覆盖三种情形——draft→deny、ack-frozen→allow、无字段 legacy→allow；既有 full-artifacts 等无字段 fixture 仍 allow（回归不破）。
- [ ] AC6: `templates/rule-card.md` 的 ACK 文案同步为"AC_LIST 置 `ack-frozen` 即冻结"。
- [ ] AC7: `lifecycle.md §2` 显式定义三档边界——极小（单文件 / 纯文案 / 零契约 / 单轮闭合）免产物但仍口头说目标 + 验证、不领迭代号；简化（零升级信号、非极小）合并 AC_LIST；完整（命中任一信号）走全产物链。
- [ ] AC8: `lifecycle.md §2` 要求一行分流记录（评估了哪些信号 + 结论 + 日期），落点：完整→CONCEPT 顶部、简化→AC_LIST 顶部、极小→口头免记录；`concept-schema.md` 与 `acceptance-schema.md` 各自登记该记录位。
- [ ] AC9: `lifecycle.md` 定义"低档→高档"升级转换：简化 / 极小 路径中途命中升级信号时，须补齐缺失产物、按需补领迭代号、把已做内容折叠进新产物后继续，不得原档硬撑。
- [ ] AC10: `logic-protocol.md §5` 的"除极小任务外"与新定义的极小边界对齐并引用 §2；`templates/rule-card.md` 的强制工作流段同步三档与升级转换。
- [ ] AC11: 本迭代 `.ai/CONCEPT.md` 带分流记录、`.ai/AC_LIST.md` 带 `状态` 字段并经历 draft→ack-frozen；ITER-0004 按 `iteration-schema.md` 收口（归档 + `deliveries/` + 台账置 closed）。

# Verification Method
- AC1 / AC2 / AC3 / AC6 / AC7 / AC8 / AC9 / AC10：阅读对应规则文件 diff，确认字段 / 小节 / 措辞按 AC 落地，且产物链与三层分层未被破坏（grep 关键字段名 + 人工 review）。
- AC4：构造 JSON 喂 `phase_gate.py`（仿 `mcv-deployment.md §5.3` 验证命令），分别用 draft / ack-frozen / 无字段 的 AC_LIST，断言 exit 码与 stderr。
- AC5：`pytest templates/hooks/tests/` 全绿，新增用例覆盖三情形，旧用例不回归。
- AC11：检查 `.ai/iterations/ITER-0004/` 快照、`deliveries/ITER-0004-*.md`、`ITERATIONS.md` 该行 `closed`。

# Open Questions / Risks
- 风险：`phase_gate` 解析 `状态` 字段的方式要稳健（frontmatter 或正文行均能命中），避免把 legacy 旧文件误判为 draft；具体解析口径在 P3 TECH_PLAN 定。
- 风险：`/dangerous` 模式下"模型自置 ack-frozen"会削弱 hook 意义（模型自校验自己写的字段）——已知局限，本轮接受并在文案如实标注，不在本迭代解决。
- 待定（P3 定稿）：简化路径 AC_LIST 是否强制 `ack-frozen`？倾向"状态字段对简化路径可选，省略即 legacy 放行、不被拦"，避免轻量任务被 hook 拖累。
