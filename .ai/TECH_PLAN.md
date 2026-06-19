# Goal
- 支撑 AC1–AC13：把 butler 持久运行模式外化为 `.ai/local-constraints.md`「Butler 功能开关」段（dangerous / independent_review），接线会话起始读取，改写 dangerous-engine §3 跨会话语义为"声明后自动生效"，显式化里程碑 active 归属 / closed 不写入，并经 SSOT 传播。

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/local-constraints-schema.md` — §1 目标 + §2 字段 + §3 模板新增「Butler 功能开关」+ §4 读写规则 + §5 流程联动。【AC1/AC2/AC3】
- `Coder/00_System_Prompt/logic-protocol.md` — §1 增会话起始读取功能开关；§4 Dangerous 条目改写 + independent_review 落点。【AC4/AC5】
- `Coder/65_Extension_Dangerous/dangerous-engine.md` — §3 改写跨会话语义。【AC6】
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — §4 local-constraints 生成含功能开关段 + 安全默认。【AC7】
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — §P1 里程碑段补 closed 不写入。【AC8】
- `Coder/20_Workflow_Lifecycle/milestone-schema.md` — §7.2 推进补"自动归属无需逐次确认"、§7.4 收口补"closed 后新迭代独立不写入"。【AC8】
- `templates/rule-card.md` — 补功能开关持久落点 + dangerous announce-on-read。【AC9】
- `HUMAN_GUIDE.md` — 新增「项目级功能开关」子节 + dangerous 跨会话行为/风险 + 自动归属。【AC10】
- `Coder/README.md` — local-constraints-schema 描述纳入功能开关。【AC11】
- `.ai/`（dogfood）— ITER-0006 四件套 + 收口归档 + 台账 + `deliveries/ITER-0006-<slug>.md`。【AC13】
- **零改动（守 AC12）**：`Coder/70_Extension_Preference/preference-probe-engine.md`、`templates/hooks/**`、`iteration-schema.md`。

# External References
- 无（`.ai/references/` 下无参考资料）。

# Interface / Contract
- **功能开关配置契约**（`.ai/local-constraints.md` 新增段）：
  - 段标题 `# Butler 功能开关`，字段 `dangerous: on|off`（默认 off）、`independent_review: on|off`（默认 off）。
  - 读：AI 会话起始（已部署项目）读取并据此激活/抑制持久模式。
  - 写：模式命令（`/dangerous on|off`、`/review` 项目级开关）NL 触发回写；用户可手改。
  - dangerous 跨会话：读到 on → 当回合显式声明后**自动生效**（announce-on-read + auto-apply）。
  - 排除：preference 不纳入（跨项目、状态在 `$BUTLER_PREF`）。
  - legacy：旧文件无本段 → 全 off；独立 `Review Policy: independent_review` → independent_review 的 legacy 形式仍尊重。
- **dangerous-engine §3 新语义**：开/关写 local-constraints `dangerous`；跨会话读到 on 声明后自动进入；显式 off / 手改 off 关闭；开关均对话层回声。
- **Ask A 归属契约**：active 里程碑（台账 `current=MILE-NNNN`）期间开启的迭代一律自动归属（三处同步）；`current: none` 后开启的迭代独立、不写入已收口里程碑、不回挂（除非按 §6.3 显式回挂到另一 active 里程碑）。台账 `current` 仍是 active 唯一真源。

# State / Boundary
- local-constraints 仍是"配置/差异"非"规则复制器"：功能开关是配置项，不复制引擎逻辑。
- 里程碑/迭代 active 指针**不进** local-constraints（台账唯一真源，零第二真源）。
- preference 外置数据流、phase_gate、iteration 锁定纪律不在本次范围。
- 危险模式跨会话自动生效是**有意降低** §3 安全冗余的取舍，必须 announce-on-read 兜底并如实标注风险。

# Design Decisions
- **整合而非并列**：`# Review Policy` 模板块并入统一 `# Butler 功能开关`，independent_review 作为其一项；旧独立字段保留 legacy 兼容，避免已部署项目断裂。
- **读取接线写进 logic-protocol §1**（会话起始读取协议），而非只在 schema 自述——否则"写了没人读"=无效外化。
- **dangerous 持久但每会话亮明**：以 announce-on-read 替代 §3 原"不续开"的安全角色——可见性换冗余，绝不静默进入无人值守。
- **preference 排除**：跨项目语义，放项目级配置会制造"每项目一份偏好开关"的错觉，明确排除并注明其外置归宿。
- **Ask A 仅澄清不改机制**：active 归属 / closed 不写入本就是现有行为（lifecycle L86 + §7.2 仅"若存在 active"），本轮只把 closed 边界写明，不引入新机制。
- **rule-card 增量克制**：只加一句功能开关落点 + dangerous 亮明，控 token，模板占位符自动继承。

# Execution Steps
1. `local-constraints-schema.md`：§1/§2/§3/§4/§5 落功能开关段与读写口径。【AC1-3】
2. `logic-protocol.md`：§1 读取接线 + §4 Dangerous/Review 条目。【AC4-5】
3. `dangerous-engine.md §3`：改写跨会话语义 + 风险标注。【AC6】
4. `mcv-deployment.md §4`：生成含功能开关段 + 安全默认。【AC7】
5. `lifecycle.md` + `milestone-schema.md`：Ask A 显式化。【AC8】
6. `rule-card.md` / `HUMAN_GUIDE.md` / `README.md`：传播。【AC9-11】
7. 一致性自检（grep 交叉引用、SSOT 单写、AC12 零改动）。【AC12】
8. P5：dogfood 收口 ITER-0006。【AC13】

# Verification Plan
- AC1/2/3：读 `local-constraints-schema.md` diff——功能开关段字段/模板/读写四条/preference 排除/legacy 兼容。
- AC4/5：读 `logic-protocol.md` diff——会话起始读取条目 + Dangerous 改写 + Review 落点。
- AC6：读 `dangerous-engine.md §3` diff——"不续开"改写为"声明后自动生效" + 命令回写 + 风险标注。
- AC7：读 `mcv-deployment.md §4` diff——功能开关段 + 安全默认。
- AC8：读 `lifecycle.md`/`milestone-schema.md` diff——active 归属 / closed 不写入显式、与台账一致。
- AC9：对比 `rule-card.md` 与 `CLAUDE.md.template`——SSOT 单写。
- AC10/11：读 `HUMAN_GUIDE.md`/`README.md` diff。
- AC12：`git diff --name-only` 确认 preference-probe-engine / hooks / iteration-schema 零改动；grep 台账 current 真源与 preference 外置表述未被矛盾。
- AC13：检查 `.ai/iterations/ITER-0006/`、`deliveries/ITER-0006-*.md`、台账 `closed` + `current: none`。

# Risks / Open Questions
- 危险跨会话自动生效削弱 §3 安全冗余——announce-on-read 兜底 + 文档如实标注，用户知情拍板。
- 功能开关靠规则纪律保证"会话起始必读"（无 hook 强制），与现有读取顺序同源同险。
- 无其它未决项。
