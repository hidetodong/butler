---
状态: ack-frozen
ACK 日期: 2026-07-23
---

# Goal
- 实现按阶段安全生成五件套骨架的确定性 CLI。

# In Scope
- init/render/reset、原子写、幂等、正文保护和阶段限制。

# Out of Scope
- hook/审计接线与 legacy migration。

# Acceptance Checklist
- [ ] AC1: CLI 可按 artifact/phase 渲染 canonical 骨架并替换 iteration/title 槽。
- [ ] AC2: init 只写缺失目标，重复执行字节幂等；dry-run 零写。
- [ ] AC3: 非显式 reset 不覆盖已有文件；reset 对含用户正文目标 fail-closed，除非明确 force。
- [ ] AC4: 写入使用同目录临时文件原子替换，注入失败不留下半文件。
- [ ] AC5: 非当前/下游越阶段生成被拒绝，完整测试与 CI 通过。

# Verification Method
- CLI 隔离 fixture + 完整 CI。

# External References
- N/A

# Open Questions / Risks
- N/A
