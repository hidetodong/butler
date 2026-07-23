# TECH_PLAN — ITER-0089

方案状态: pass

# Design Decisions
- migrate 只接受 H2 集合是 canonical 子集的 legacy；同名段正文注入模板。
- `.ai/.artifact-migration-backups/<id>/` 保存 pre bytes 与 receipt；post hash 门控 rollback。
- dogfood 先 snapshot 历史 tree hash，再迁移 live 五件套并 strict check。

# Failure Paths
- 未知/重复段、symlink、半写、receipt/hash 漂移全部拒绝。

# Test Strategy
- plan/apply/idempotence/rollback/tamper + current repo check + full CI/audit。

# References Compliance
- N/A
