---
状态: ack-frozen
ACK 日期: 2026-06-19
---

# Goal
- 把 butler 的持久运行模式状态外化为**项目级可读可写持久配置**，统一落在 `.ai/local-constraints.md` 新增"Butler 功能开关"段，AI 会话起始读取并据此执行；危险模式按"声明后跨会话自动生效"接入（改写 dangerous-engine §3 的"不续开"）；里程碑"active 自动归属 / closed 不再写入"显式化。

# In Scope
- 扩展 `local-constraints-schema.md`：新增功能开关段（`dangerous`、`independent_review`）+ 读写口径 + preference 排除 + legacy 兼容。
- 接线读取：`logic-protocol.md` 会话起始读取功能开关并激活模式。
- 危险模式跨会话：`dangerous-engine.md §3` 改写为持久态外化 + 声明后自动生效 + 命令回写。
- 部署默认：`mcv-deployment.md §4` 生成含功能开关段、安全默认。
- Ask A 显式化：`lifecycle.md` + `milestone-schema.md` 明确 active 归属 / closed 不写入。
- 传播：`rule-card.md`（SSOT）、`HUMAN_GUIDE.md`、`Coder/README.md`。
- dogfood：ITER-0006 走完整 P1→P5 收口。

# Out of Scope
- preference 引擎数据流与外置存储（`$BUTLER_PREF`）——其 on/off 是跨项目、不纳入项目级配置。
- 已部署旧项目 local-constraints 的批量回填（靠 legacy 兼容，迁移走 `butler-upgrade`）。
- phase_gate hook、iteration-schema 锁定纪律、台账 `current` 真源机制。
- 把里程碑/迭代 active 指针写进 local-constraints（保持台账唯一真源）。

# Acceptance Checklist
- [ ] AC1: `local-constraints-schema.md` 新增"# Butler 功能开关"段（schema 字段 + 模板），含 `dangerous: on|off`（默认 off）与 `independent_review: on|off`（默认 off，整合原独立 `Review Policy` 语义）；§1 目标与 §2 字段清单更新为"本地化适配 + 项目级 butler 功能开关持久配置"。
- [ ] AC2: 同 schema 定义读写口径四条：① AI 会话起始读取功能开关并据此激活持久模式；② 模式命令（`/dangerous on|off`、`/review` 相关）NL 触发时**回写**本段；③ 用户可**手改**；④ `dangerous: on` 跨会话 **announce-on-read + 自动生效**（当回合显式声明后进入，绝不静默）。
- [ ] AC3: schema 显式注明：① preference **不纳入**（跨项目、状态在外置 `$BUTLER_PREF`）；② **legacy 兼容**——旧 local-constraints 无功能开关段时按全 off 处理、独立 `Review Policy: independent_review` 作为该开关的 legacy 形式仍被尊重，不被误判。
- [ ] AC4: `logic-protocol.md §1` 增明确条目：已部署项目（存在 `.ai/local-constraints.md`）**会话起始必须读取其功能开关段并据此激活/抑制持久模式**，不依赖对话记忆。
- [ ] AC5: `logic-protocol.md §4` 更新 Dangerous 条目：持久态外化到 local-constraints `dangerous`，跨会话读到 on → 显式声明后自动生效（替代原"下一会话默认 Standard、不自动续开"表述），`/dangerous on|off` 回写；注明 `independent_review` 落点同在功能开关段。
- [ ] AC6: `dangerous-engine.md §3` 改写跨会话语义：删去/改写"会话结束即回 Standard、不自动续开"，改为——on/off 持久态外化到 `.ai/local-constraints.md` 功能开关；跨会话读到 on → 当回合**显式声明后自动进入**危险模式；`/dangerous on|off` 或手改即写开关并关/开；保留"开关都须对话层回声"。**如实标注**这是相对 §3 原安全冗余的取舍及其风险（announce-on-read 为兜底）。
- [ ] AC7: `mcv-deployment.md §4` 本地化适配生成的 local-constraints 含功能开关段，安全默认 `dangerous: off`、`independent_review: off`。
- [ ] AC8: Ask A 显式化——`lifecycle.md §P1` 与 `milestone-schema.md §7.2`（推进）/`§7.4`（收口）明确：active 里程碑期间开启的迭代**自动归属**之（所属 milestone + 含迭代 + 路线图三处同步）；里程碑 closed（`current: none`）后开启的迭代为**独立迭代、不写入已收口里程碑、不回挂**。
- [ ] AC9: `templates/rule-card.md` 补要点：项目级 butler 功能开关（dangerous / independent_review）持久在 `.ai/local-constraints.md`，会话起始读取并据此执行，`dangerous: on` 跨会话须 announce-on-read。SSOT 单写、模板经占位符继承。
- [ ] AC10: `HUMAN_GUIDE.md` 更新：统一配置落点与用途、两种改法（对话 NL 触发 / 手改）、有哪些开关、`dangerous` 跨会话"声明后自动生效"的行为与风险提示、里程碑 active 自动归属 / closed 不写入。
- [ ] AC11: `Coder/README.md` 中 local-constraints-schema 描述纳入"项目级 butler 功能开关持久配置"。
- [ ] AC12: 不破坏既有——preference 外置数据流与 `$BUTLER_PREF`、phase_gate hook、`iteration-schema.md`、台账 `current` 真源**零改动且不被矛盾**；legacy local-constraints 向后兼容。
- [ ] AC13: dogfood——本迭代 `.ai/CONCEPT.md` 带分流记录、`.ai/AC_LIST.md` 走 draft→ack-frozen、产出 `TECH_PLAN.md`/`VERIFY_REPORT.md`，ITER-0006 按 `iteration-schema.md §5.5` 收口（归档 + `deliveries/ITER-0006-<slug>.md` + 台账置 closed）。

# Verification Method
- AC1/AC2/AC3：读 `local-constraints-schema.md` diff，确认功能开关段字段/模板/读写四条/preference 排除/legacy 兼容齐全且仍守"配置非规则复制"定位。
- AC4/AC5：读 `logic-protocol.md` diff，确认会话起始读取条目 + Dangerous 条目改写 + independent_review 落点注明。
- AC6：读 `dangerous-engine.md §3` diff，确认"不续开"被改写为"声明后自动生效"、命令回写、风险如实标注。
- AC7：读 `mcv-deployment.md §4` diff，确认生成含功能开关段 + 安全默认。
- AC8：读 `lifecycle.md`/`milestone-schema.md` diff，确认 active 归属 / closed 不写入显式化、与台账 current 一致。
- AC9：对比 `rule-card.md` 与 `CLAUDE.md.template`，确认 SSOT 单写。
- AC10/AC11：读 `HUMAN_GUIDE.md`/`README.md` diff，确认用法、风险、注册到位。
- AC12：`git diff --name-only` 确认 `preference-probe-engine.md`、`templates/hooks/`、`iteration-schema.md` 零改动；grep 确认台账 current 真源、preference 外置存储表述未被矛盾。
- AC13：检查 `.ai/iterations/ITER-0006/` 快照、`deliveries/ITER-0006-*.md`、`ITERATIONS.md` 该行 `closed`、`current: none`。

# Open Questions / Risks
- 风险（已知并接受）：危险模式跨会话自动生效削弱了 dangerous-engine §3 原"不自动续开"的安全冗余；以 announce-on-read（每会话起始显式声明、可 `/dangerous off`）兜底，并在 §3 与 HUMAN_GUIDE 如实标注。用户知情拍板。
- 风险：功能开关为语义约定，AI 会话起始"必须读"靠规则纪律保证（无 hook 强制）；与现有"读取顺序"同源同险。
- 待 ACK：以上为最终设计，无遗留待决项（前置三问已定稿）。
