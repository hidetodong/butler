---
状态: ack-frozen
ACK 日期: 2026-07-23
---

# Goal
- 让五件套结构漂移可被零写检查、hook、审计和 CI 机械发现。

# In Scope
- check CLI、hook、auditor、CI 与文档接线。

# Out of Scope
- legacy migration 留 R4。

# Acceptance Checklist
- [ ] AC1: check artifact/project 零写验证 marker、段落、字段和表头，稳定 JSON/exit code。
- [ ] AC2: 未标记 legacy live 文件明确 skipped，不误报；标记文件漂移 fail-closed。
- [ ] AC3: hook 对五件套结构漂移给出共享规则结果，Claude/Codex 共用真源。
- [ ] AC4: 状态审计和 verify-ci 调用 project check，strict 项目漂移阻断。
- [ ] AC5: 正负向集成测试、现有 hook 矩阵和完整 CI 通过。

# Verification Method
- artifact/hook/audit 专项与完整 CI。

# External References
- N/A

# Open Questions / Risks
- N/A
