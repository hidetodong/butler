# CONCEPT — ITER-0089 · 五件套兼容迁移与 dogfood

## Current Understanding
- 迁移必须把 legacy 每个已识别 H2 正文映射进 canonical 同名段，未知/重复段拒绝，不静默丢内容。
- 当前 Butler live 五件套作为真实 dogfood，迁移后 strict check 必须全绿；历史归档不改。

## Scope
- migrate plan/apply、备份/回滚、幂等、正文 hash、当前仓 dogfood、升级文档和最终里程碑验证。

## Open Questions / Risks
- N/A
