---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 以单一 inbox schema 落地 AC1–AC7，既能给 R4 行为消费，又不把原文或命令算法塞进 ledger。

# Files / Modules to Change

- `Coder/40_Context_Management/inbox-schema.md`：数据契约真源。
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`：origin 与 INBOX 职责指针。
- `Coder/README.md`、`HUMAN_GUIDE.md`：导航与人读定位。
- `templates/hooks/tests/test_inbox_contract.py`：结构合同测试。
- `.ai/*`：状态、归档与交付。

# Interface / Contract

- `.ai/INBOX.md`：Sources 表 + Derivations 表。
- `source_id`：`SRC-NNNN` 单调稳定身份。
- 双指纹：`observed_sha256` / `processed_sha256`。
- 状态：unprocessed/analyzed/awaiting-confirmation/routed/ignored/source-changed/failed。
- locator：origin 相对路径、conversation turn ref、外部稳定 URL/document ID。

# State / Boundary

- INBOX 是可重建处理回执，不是内容真源；origin/外部文档/对话仍是来源。
- R4 才实现状态转移动作，R3 只定义合法形态。
- AI 对 `origin/` 零写入；INBOX 只能写 `.ai/`。

# Design Decisions

- source_id 与 hash 分离，才能表达同源改版和跨来源重复候选。
- 使用双指纹而非单 hash：一个表示现在看到什么，一个表示上次成功处理什么，二者不同即 source-changed。
- 派生关系独立表，避免在来源行塞逗号列表并支持多对多。
- 状态封闭枚举；ignored/failed 不等于完成路由。

# Plan Admission

- AC Coverage：schema 覆盖 AC1–AC6，三处接线 + 测试/CI 覆盖 AC7。
- Assumptions：所有来源至少有一种稳定 locator；没有则动作层必须先分配 source_id 并记录会话位置，不能伪造路径。
- Alternatives / Trade-offs：内容 hash 作主键能去重但会把同源新版拆成新来源；把原文复制进 INBOX 可复现但侵犯 origin 所有权并使 ledger 膨胀。选择稳定 ID + 双 hash + 指针。
- Failure Modes：mtime 伪指纹、不同 locator 自动合并、processed hash 在失败时推进、ignored 写成 routed、关系丢多对多、摘要泄露敏感数据。逐项禁止。
- Impact / Scope Challenge：不创建命令和 registry，保持 R3 数据层单一。
- Verification Blind Spots：结构测试不能证明实际扫描幂等；R4 必须用文件 fixture 做行为测试。
- Verdict：pass。AC 全覆盖，无已知 Must Fix。

# Execution Steps

- [x] T1 盘点 origin 与 milestone 现行入口 → AC1, AC6, AC7
- [x] T2 设计来源身份、双指纹、状态和关系 → AC1–AC6
- [x] T3 完成危险模式 P2/P3 自审 → AC1–AC7
- [ ] T4 新增 inbox schema 并接线 → AC1–AC7
- [ ] T5 新增测试并运行证据矩阵 → AC1–AC7
- [ ] T6 强审、Goal 裁决与原子收口 → AC1–AC7

# Verification Plan

- `python3 -m unittest templates.hooks.tests.test_inbox_contract -v`
- `bash scripts/verify-ci.sh`、`git diff --check`、Goal/state audit。

# Risks / Open Questions

- R4 需选择实际 Markdown 行更新策略和事务边界；本轮不抢跑实现。
