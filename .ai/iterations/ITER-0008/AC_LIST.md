---
状态: ack-frozen
ACK 日期: 2026-06-19
---

# Goal
- 把迭代状态枚举固化为封闭三态（active/closed/abandoned），并新增 hook 规则 ledger_status 机械保证台账状态列不取错（如 planned 被拦截）。

# Acceptance Criteria

## A. 枚举固化（spec/SSOT）
- [ ] **AC1**：`iteration-schema.md §4.2` 改写为**封闭枚举**——明文声明迭代行「状态」合法值**仅** `active`/`closed`/`abandoned`，其他值（含 `planned`）对迭代行**非法**；保留三态各自语义说明。
- [ ] **AC2**：§4.2 交叉引用消歧——指明 `planned` 是 `milestone-schema §5.3` 路线图「路线项状态」、非迭代状态；并说明该枚举由部署的 hook（ledger_status）机械校验。

## B. 里程碑侧消歧
- [ ] **AC3**：`milestone-schema.md §5.3` 增明确表述——「路线项状态」（planned/active/closed/abandoned）是路线项自身命名空间，`planned` 路线项「实际 ITER」为 `—`、**不产生迭代台账行**；迭代行状态以 `iteration-schema §4.2` 封闭三态为准（交叉引用）。

## C. 机制：hook 规则 ledger_status
- [ ] **AC4**：新增 `templates/hooks/rules/ledger_status.py`，`RULE_ID = "ledger_status"`，仅当 `target == .ai/ITERATIONS.md` 时生效，其余路径直接 allow；零三方依赖、`from __future__ import annotations` 风格与现有规则一致。
- [ ] **AC5**：规则解析入参文本（Write→`content`、Edit→`new_string`、MultiEdit→各 `edits[].new_string`），逐行识别 `^ITER-\d{4}$` 起头的表数据行，取「状态」单元格（第 3 列），大小写不敏感比对；越界非空值返回 `deny`，`reason` 含违规迭代号与该值、合法枚举，`remediation` 指明三态 + planned 属路线项（引 milestone-schema §5.3）。
- [ ] **AC6**：表头行、分隔行（`|---|`）、空状态单元格、非 ITER 行均不误杀（allow）。
- [ ] **AC7**：`butler_gate.py` 的 import 与 `RULE_MODULES` 接入 `ledger_status`；deny 后仍走 `lib/bypass`（`BUTLER_BYPASS=1` + 非空 `.ai/bypass-reason.md` 可绕过并记 RUN_LOG），退出码契约不变。

## D. 测试
- [ ] **AC8**：新增 `templates/hooks/tests/test_ledger_status.py`，覆盖：合法三态全 allow、`planned` 行 deny（reason/remediation 断言）、`abandoned` allow、非台账路径 allow、Edit/MultiEdit 入参 deny、表头/分隔/空状态 allow、大小写变体 allow。
- [ ] **AC9**：`cd templates/hooks && python3 -m pytest tests/` 全绿（既有用例 + 新用例）。

## E. 传播 / 注册
- [ ] **AC10**：`templates/hooks/README.md` 目录结构与「运行机制」执行顺序补 `ledger_status` 及其职责。
- [ ] **AC11**：`mcv-deployment.md §5` hook 拦截能力描述补"迭代台账状态枚举越界被拦截"。
- [ ] **AC12**：`Coder/README.md` 使用原则/hook 说明补迭代台账状态校验一句；`rule-card.md` 与 `HUMAN_GUIDE.md` 若含 hook 行为概述则各补一句（无则不强加）。

## F. 一致性与零改动护栏
- [ ] **AC13**：hook `VALID_STATES` 与 `iteration-schema §4.2` 封闭三态字面一致（机械镜像，注释互指）。
- [ ] **AC14**：零改动护栏——`phase_gate.py`/`protected_paths.py`/`artifact_chain.py` 行为、`lib/io.py`/`lib/bypass.py`、产物链四 schema、`versioning-schema.md` 未被改动（`git diff` 确认）。
- [ ] **AC15**：未破坏 CLAUDE.md 五约束——分层未混、产物链未动、（无新增规则文件，hook 规则随 rules/ 整目录分发无需 README 单列文件，但行为已在相关文档登记）、模板 SSOT 未手写重复、frontmatter 合规。

## G. 收口
- [ ] **AC16**：ITER-0008 四件套快照归档 `.ai/iterations/ITER-0008/`，写 `deliveries/ITER-0008-<slug>.md`，台账置 closed + 收口日期 + 交付链接，`current: none`。
