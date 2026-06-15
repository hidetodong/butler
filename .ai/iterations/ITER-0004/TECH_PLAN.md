# Goal
- 支撑 AC1–AC11：把 ACK/冻结状态（D1）与入口分流（D4）外化为产物字段 + hook 可校验状态 + 三档边界与升级转换，并 dogfood 收口 ITER-0004

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/acceptance-schema.md` — §2 必填字段加 `状态`(draft|ack-frozen)+`ACK 日期`；§3 模板顶部加 frontmatter；§4 编写规则加状态语义 + amend 退回 draft；§6 登记 ACK 物化；同时登记"简化路径分流记录写进 AC_LIST 顶部"。〔AC1, AC8〕
- `Coder/20_Workflow_Lifecycle/lifecycle.md` —
  - §2 重写为三档：极小（单文件/纯文案/零契约/单轮闭合 → 免产物、口头说目标+验证、不领迭代号）/ 简化（零信号、非极小 → 合并 AC_LIST）/ 完整（命中任一信号 → 全产物链）；加一行分流记录要求与落点；加"低档→高档"升级转换。〔AC7, AC8, AC9〕
  - P2 强制规则加：AC_LIST 初始 `draft`，用户 ACK 后置 `ack-frozen`+日期方可进 P3，hook 会拦截 draft；`/dangerous` 由自审门置位；amend 须退回 draft 重新 ACK。〔AC2〕
  - §5 小幅修订分流补"状态退回 draft、重新 ACK"。〔AC2/AC3 协同〕
- `Coder/20_Workflow_Lifecycle/iteration-schema.md` — §5.2 把"冻结"物化为 AC_LIST `状态: ack-frozen`；§5.3 amend 加"状态退回 draft 再重新 ACK"。〔AC3〕
- `Coder/00_System_Prompt/logic-protocol.md` — §5 "除极小任务外"对齐新极小边界并引用 `lifecycle.md §2`。〔AC10〕
- `Coder/20_Workflow_Lifecycle/concept-schema.md` — §3 模板顶部加分流记录行（完整路径落点）；§4/§5 登记。〔AC8〕
- `templates/rule-card.md` — 强制工作流段同步三档 + 分流记录 + 升级转换；ACK 文案改为"AC_LIST 置 `ack-frozen` 即冻结"。〔AC6, AC10〕
- `templates/hooks/rules/phase_gate.py` — 三件套存在性循环之后加 AC_LIST 冻结门。〔AC4〕
- `templates/hooks/tests/test_phase_gate.py`（+ `test_integration.py`）— 加 draft→deny / ack-frozen→allow / 无字段 legacy→allow 用例；整合测试加 draft→exit 2。〔AC5〕
- 文档 accuracy 同步：`Coder/README.md` 使用原则的 hook 描述、`Coder/20_Workflow_Lifecycle/mcv-deployment.md §5` 的 hook 描述，补"AC_LIST 冻结门"。〔自洽，支撑 AC4〕
- dogfood：`.ai/VERIFY_REPORT.md`、`.ai/iterations/ITER-0004/`、`.ai/ITERATIONS.md` 收口、`deliveries/ITER-0004-<slug>.md`。〔AC11〕

# Interface / Contract
- AC_LIST 冻结契约：AC_LIST 顶部 `状态 ∈ {draft, ack-frozen}`；draft=写完待 ACK，ack-frozen=用户（或 `/dangerous` 自审门）确认、范围冻结。**无字段=legacy（旧部署），hook 放行**。
- hook 契约扩展：`phase_gate` 在三件套存在且非空的前提下，再校验 AC_LIST 冻结态——draft / 未知值 → deny；ack-frozen / 无字段 → allow。`protected_paths`、`artifact_chain`、bypass（`BUTLER_BYPASS` + `bypass-reason.md`）接线不变。
- 分流契约：每个非极小任务在产物顶部留一行分流记录（信号评估 + 结论 + 日期）；完整→CONCEPT、简化→AC_LIST、极小→口头。
- 升级转换契约：低档任务中途命中升级信号 → 补齐缺失产物 + 按需补领迭代号 + 折叠已做 → 续跑高档，不在错档硬撑。
- 三件套固定路径不变 → 既有 `phase_gate` 存在性逻辑零回归。

# State / Boundary
- 改动集中在"P2 冻结时刻"与"任务入口分流时刻"，不新增阶段、不动状态机骨架。
- hook 仅新增一个判定分支，复用现有 `Decision` / dispatcher / bypass；不解析 YAML，扫描 `状态`/`status` 行。
- 明确不在范围：D2 / D3 / D5 / D6、里程碑机制、Domain/Stack Profiles、旧 AC_LIST 批量回填迁移。

# Design Decisions
- 冻结态解析用"扫描 `状态`/`status` 行 + 取首个匹配"，不引 YAML 依赖：hook 必须零三方依赖、跨 Python 版本稳定；frontmatter 与正文行都能命中。
- 无字段 = legacy 放行而非 deny：硬性向后兼容，已部署项目旧 AC_LIST 不被误杀（`full-artifacts`/`with-bypass-reason` fixture 即此情形，回归不破）。
- 未知值（非 draft/ack-frozen）保守 deny：暴露拼写错误，避免"看似冻结实则没冻结"。
- 三档保留而非收敛（用户决策）：给极小补明确边界，简化/完整阈值不变。
- 升级转换走"补产物 + 补迭代号"而非推翻重来：保留已完成工作。
- 已知局限如实标注，不在本轮假装解决（hook 校验字段 ≠ 校验人；`/dangerous` 自置 ack-frozen）。

# Execution Steps
- Task A（D1 规则层）：`acceptance-schema.md` → `lifecycle.md` P2/§5 → `iteration-schema.md` §5.2/§5.3。
- Task B（D1 hook 层）：`phase_gate.py` → `test_phase_gate.py` / `test_integration.py` → 跑 `pytest`。
- Task C（D4 规则层）：`lifecycle.md §2`（三档 + 分流 + 升级）→ `concept-schema.md` → `logic-protocol.md §5`。
- Task D（SSOT + accuracy）：`rule-card.md` → `README.md` hook 描述 → `mcv-deployment.md §5` hook 描述。
- Task E（验证）：`phase_gate` 手测三态 + `pytest` 全绿 + 交叉读各规则文件自洽。
- Task F（P5 / dogfood）：写 `VERIFY_REPORT.md`、归档、台账收口、交付总结。

# Verification Plan
- AC1/AC2/AC3/AC6/AC7/AC8/AC9/AC10：读各规则文件 diff，逐项核对字段/小节/措辞，并交叉确认产物链与三层分层未破坏。
- AC4：仿 `mcv-deployment.md §5.3`，构造 Edit JSON 喂 `phase_gate.py`/`butler_gate.py`，分别用 draft / ack-frozen / 无字段 AC_LIST，断言 exit 码与 stderr 含 `phase_gate`。
- AC5：`pytest templates/hooks/tests/` 全绿；新增三情形用例通过；既有 `full-artifacts` 等 legacy 用例不回归。
- AC11：检查 `.ai/iterations/ITER-0004/` 快照、`deliveries/ITER-0004-*.md`、`ITERATIONS.md` 该行 `closed` 且 `current: none`。

# Risks / Open Questions
- 解析 `状态` 行的健壮性：只取首个匹配，值不在 {draft, ack-frozen} 即按未冻结处理；本仓库 AC_LIST 字段在顶部 frontmatter，命中明确，正文误命中概率低。
- 已定（原 AC_LIST 待定项收口）：**简化路径 AC_LIST 的 `状态` 字段可选**——省略即 legacy 放行、不被 hook 拦，避免轻量任务被拖累；完整路径必填。
- `rule-card.md` 体量约束（~800 token）：三档与升级转换用最短句登记，避免膨胀。
- README / mcv-deployment 的 hook 描述同步属 accuracy 补丁，非新增隐式依赖。
