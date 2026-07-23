---
状态: ack-frozen
ACK 日期: 2026-07-22
---

# Goal
- 让 `.ai/02_SESSION_HANDOFF.md` 成为从权威项目状态确定性生成、可校验新鲜度并能安全重建的跨会话入口。

# In Scope
- 有界状态快照、固定结构渲染、来源/正文指纹、原子同步、零写检查、陈旧拒绝与重建。
- 权威状态变化后的跨宿主提醒，以及冷启动、暂停、compact/交接前的强制检查或同步协议。
- 当前 Butler 仓 dogfood、状态审计和完整 CI 接线。

# Out of Scope
- 不捕获从未落入项目文件的纯聊天内容，不承诺所有宿主都有 stop/compact hook。
- 不实现 MILE-0010 R2/R3 的五位编号或台账分片。
- 不处理独立的五件套固定化候办。

# Acceptance Checklist
- [ ] AC1: 工具从 task-state、当前台账、活里程碑和当前阶段产物建立有界快照，同一输入生成完全相同的 handoff 正文。
- [ ] AC2: 生成正文严格使用 handoff-spec 的 H1 与六个固定 H2，内容只给断点、决策、风险、唤醒动作和状态指针，不复制历史或日志。
- [ ] AC3: 同步以原子替换写 handoff 与机器 receipt；receipt 记录 schema、来源 SHA-256 集合和正文 SHA-256，重复同步幂等。
- [ ] AC4: 零写 `check` 能区分 fresh、来源变化、正文篡改、缺失/损坏 receipt，并用稳定 JSON 与退出码报告。
- [ ] AC5: 陈旧 handoff 不得被冷启动当真；协议要求先 check，stale 时从权威状态 sync 后再读，恢复不依赖旧正文。
- [ ] AC6: 写入 task-state、ITERATIONS、MILESTONES、活 MILESTONE 或四件套后，PostToolUse advisory 能提醒 handoff 已可能陈旧；提醒 fail-open、不自动篡改状态。
- [ ] AC7: 无 active 迭代、无里程碑台账和 legacy 未部署 receipt 均有明确退化；新机制不追罚历史项目，存在 receipt 时状态审计必须校验。
- [ ] AC8: 路径越界、symlink、非法 UTF-8、坏 ledger/current 和畸形 receipt 均 fail-closed，失败不留下半写文件。
- [ ] AC9: 工具专项、hook 专项、状态审计与完整 CI 覆盖正向、负向、幂等和本仓 dogfood；规则文档与部署入口指向同一工具真源。

# Verification Method
- AC1–AC5、AC7–AC8: `tools/handoff/tests/test_handoff.py` 使用隔离项目验证快照、渲染、sync/check/repair、退化和安全边界。
- AC6: `templates/hooks/tests/test_handoff_freshness.py` 与 dispatcher 集成测试验证目标集合、去重和 fail-open。
- AC7、AC9: `scripts/test-audit-project-state.py`、本仓 `sync → check`、Markdown/双宿主检查与 `bash scripts/verify-ci.sh`。
- AC9: `git diff --check` 与完整 P5 evidence 捕获。

# External References
- N/A

# Open Questions / Risks
- 宿主能力不一致，R1 以 advisory + 冷启动 fail-closed 自愈覆盖共同底线；原生 stop hook 只作可选加速，不作为正确性前提。

