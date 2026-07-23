---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal
- 用一个标准库工具和一个可选提醒层兑现 AC1–AC9，handoff 的可信性不依赖模型自觉或任一宿主私有能力。

# Files / Modules to Change
- `tools/handoff/`：状态快照、固定渲染、receipt、sync/check CLI 与专项测试。
- `Coder/40_Context_Management/handoff-spec.md`、`context-persistence.md`、`Coder/20_Workflow_Lifecycle/maintenance-boundaries.md`：把手写蒸馏改为派生视图协议。
- `templates/hooks/rules/handoff_freshness.py`、`butler_advisor.py` 与测试：权威状态写后提醒。
- `scripts/audit-project-state.py`、审计测试、`scripts/verify-ci.sh`：存在 receipt 时机械校验。
- `Coder/README.md`、`HUMAN_GUIDE.md`、`templates/rule-card.md`：注册冷启动和使用入口。

# External References
- N/A

# Interface / Contract
- `python3 tools/handoff/handoff.py inspect --project-root ROOT`：零写输出当前快照与来源集合。
- `... sync ...`：从快照渲染固定正文并更新 `.ai/handoff-state.json`；成功 exit 0。
- `... check ...`：fresh exit 0，stale exit 1，非法输入 exit 2；stdout 始终为稳定 JSON。
- receipt schema v1：`sources[{path, sha256}]`、`handoff_sha256`、`snapshot`；不保存时间戳，保证同状态幂等。

# State / Boundary
- 权威输入固定为 task-state、两张热台账（存在时）、active MILESTONE 和当前阶段所需四件套；选择逻辑封装为布局适配层，R3 可换后端。
- handoff 与 receipt 是派生产物，任何来源 hash 或正文 hash 不一致即 stale；check 绝不相信 handoff 自述。
- 输出目标和所有输入必须是项目根内普通文件，不跟随 symlink。

# Design Decisions
- 采用 sidecar receipt，不把机器 hash 混进人读正文；正文保持 handoff-spec 固定结构。
- 不让 PostToolUse 自动写 handoff。自动写会在任意编辑后制造额外工作树改动，也无法保证同时捕获语义结晶；advisory 只提醒，冷启动 check/sync 才是正确性底线。
- 不把 git status 纳入来源指纹，避免 handoff 自身写入导致即时自陈旧；“环境脏点”固定指向 `git status --short` 现场检查。
- 决策/风险摘要从当前阶段产物的固定章节有界抽取，抽取失败则给指针，不自由总结。

# Plan Admission
- AC Coverage：AC1–AC9 均映射到工具、advisory、审计或规则接线。
- Assumptions：项目重要状态已先落权威文件；通过负向用例验证缺文件/坏状态不会伪造 handoff。
- Alternatives / Trade-offs：否决纯 prompt 维护（会忘）和 hook 自动改写（隐式副作用、宿主不齐）；采用派生工具 + 提醒 + 消费前检查。
- Failure Modes：覆盖半写、source/正文篡改、symlink、非法编码、current 漂移、receipt 损坏和无 active 退化。
- Impact / Scope Challenge：R1 不引入通用状态数据库，也不提前拆台账；只建立可替换读取适配层。
- Verification Blind Spots：无法恢复从未落盘的聊天决定；规则明确要求重要决定先结晶，此限制不得写成已解决。
- Verdict：`pass` — 边界明确、失败路径可机械验证，无已知 Must Fix。

# Execution Steps
- [ ] T1 实现有界快照、固定渲染、receipt 与 inspect/sync/check CLI → AC1–AC5, AC7–AC8
- [ ] T2 增加工具正负向与幂等测试 → AC1–AC5, AC7–AC8
- [ ] T3 增加 PostToolUse freshness advisory 与测试 → AC6
- [ ] T4 接入状态审计、CI、规则与部署文档 → AC5, AC7, AC9
- [ ] T5 本仓 sync/check dogfood，完整审查与完整 CI → AC1–AC9

# Verification Plan
- 专项 unittest 覆盖 CLI 退出码、JSON、hash、原子性、symlink/坏输入和无 active。
- hook pytest 覆盖来源目标与非目标、Codex apply_patch 多目标去重、异常 fail-open。
- audit tests 覆盖 fresh/stale/legacy N/A；最后运行固定完整 CI。

# Risks / Open Questions
- 无开放设计问题。实现若发现 handoff-spec 的 500 token 上限无法用确定性近似验证，只限制字节/行数并保留人读审查，不伪称精确 token 计数。

