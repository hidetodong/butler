---
状态: ack-frozen
ACK 日期: 2026-06-19
---

# Goal
- 把 preference 接入 `.ai/local-constraints.md`「Butler 功能开关」作为 per-project 抑制开关（默认 on），外置 $PREF 仍为 consent/数据跨项目真源；反转 ITER-0006「preference 不纳入」。

# Acceptance Criteria

## A. schema（SSOT 语义）
- [ ] **AC1**：`local-constraints-schema.md §3` 模板「Butler 功能开关」段新增 `preference: on` 行，注释说明 = 本项目抑制开关、默认 on、on≠强制采集（仍需全局同意）、外置真源。
- [ ] **AC2**：§2 必填字段描述更新——「Butler 功能开关」部署默认改为"dangerous/independent_review 默认 off、preference 默认 on"（不再笼统说"全 off"）。
- [ ] **AC3**：§4.1 原"preference 不纳入"条**反转**为 per-project 抑制开关口径，明确：① 生效条件（全局未 off ∧ 全局 consent=granted ∧ 本项目 preference≠off 三者全真才采集/蒸馏/反哺）；② `preference: off` 只抑制本项目、不改全局 consent/不动 $PREF/不影响他项目；③ 缺字段=视为 on；④ 外置 $PREF 仍是 consent/signals/profile 跨项目唯一真源、本开关不双写。

## B. 引擎
- [ ] **AC4**：`preference-probe-engine.md` 新增项目级抑制开关小节（如 §2.5），定义本项目抑制语义 + 生效优先级（全局 `/preference off` > 全局 consent > 项目 `preference` 开关），并引用 `local-constraints-schema §4.1`。
- [ ] **AC5**：§2.1（数据回路默认常驻）标注"在 butler 托管项目默认运行"**受项目级抑制开关约束**（本项目 `preference: off` 即不在本项目采集），与 §2.5 一致、不矛盾。

## C. 接线
- [ ] **AC6**：`logic-protocol.md §1.3` 会话起始读取「Butler 功能开关」段新增 `preference` 项——`preference: off` → 本项目抑制偏好探针（不采集/蒸馏/反哺）；默认/缺省 on；指明语义以 `local-constraints-schema §4.1` 为准。
- [ ] **AC7**：`logic-protocol.md §4` Preference Mode 条目补一句——per-project 抑制开关持久在 `.ai/local-constraints.md`「Butler 功能开关」`preference`，外置 `$BUTLER_PREF` 仍为跨项目真源。

## D. 部署默认
- [ ] **AC8**：`mcv-deployment.md §4` 生成「Butler 功能开关」段的描述纳入 `preference: on`（默认 on），并说明 on 安全（实际采集仍需全局同意）。

## E. 传播（反转排除措辞）
- [ ] **AC9**：`rule-card.md` 项目级功能开关节原"偏好系统不在此（跨项目、外置 $BUTLER_PREF）"反转为"preference 作 per-project 抑制开关在此，外置仍为跨项目真源"。
- [ ] **AC10**：`HUMAN_GUIDE.md` §5「项目级功能开关」表新增 preference 行；原"（注：偏好探针不在这里……）"更新为"本项目可用 preference 开关抑制，consent/数据仍跨项目外置"。
- [ ] **AC11**：`Coder/README.md` local-constraints-schema 描述中"偏好系统因跨项目不纳入"反转为"preference per-project 抑制开关纳入、外置仍为跨项目真源"。

## F. 一致性与零改动护栏
- [ ] **AC12**：四处旧排除措辞（local-constraints-schema §4.1、rule-card、HUMAN_GUIDE、Coder/README）的"不纳入/不在此/偏好探针不在这里"旧句已消失，新口径一致（全仓 grep 无残留旧排除句）。
- [ ] **AC13**：preference 真源归属表述全仓一致——consent/signals/profile 在外置 $PREF（跨项目）、local-constraints 的 `preference` 仅本项目抑制闸，无任一处把它写成项目级真源或要求双写。
- [ ] **AC14**：零改动护栏——preference 采集/蒸馏/反哺算法（engine §5/§6/§7）、外置存储契约（§4）、§3 安全底线、与 /dangerous 隔离（§9）、`ledger_status` hook、产物链四 schema、versioning-schema 未被改动（`git diff` 确认）。
- [ ] **AC15**：未破坏 CLAUDE.md 五约束——分层未混、产物链未动、无新增规则文件（修改既有，无需 README 新注册）、模板 SSOT 经占位符继承未手写重复、frontmatter 未动。

## G. 收口
- [ ] **AC16**：ITER-0009 四件套快照归档 `.ai/iterations/ITER-0009/`，写 `deliveries/ITER-0009-<slug>.md`，台账置 closed + 收口日期 + 交付链接，`current: none`。
