---
状态: ack-frozen
ACK 日期: 2026-07-23
---

# Goal
- 建立五件套结构的唯一机器真源与 canonical 模板。

# In Scope
- manifest、模板、合同测试、schema 注册。

# Out of Scope
- 生成器、hook/审计接线、项目迁移留后续路线。

# Acceptance Checklist
- [ ] AC1: manifest 以版本化 JSON 唯一定义五件套路径、阶段、固定一级段落顺序、必需 frontmatter/字段与表头。
- [ ] AC2: 五份 canonical 模板与 manifest 完全对账，条件段固定存在并以 N/A 占位。
- [ ] AC3: 合同测试拒绝未知产物、重复段、缺段、换序、坏表头、坏版本与模板/manifest 漂移。
- [ ] AC4: schema 文档和 Coder/README 注册机器 SSOT，明确新产物严格、legacy 归档不追罚。
- [ ] AC5: 完整 CI 与 diff check 通过。

# Verification Method
- AC1–AC4：artifact contract 单测与 manifest/template 静态对账。
- AC5：完整 CI。

# External References
- N/A

# Open Questions / Risks
- N/A
