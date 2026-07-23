---
状态: ack-frozen
ACK 日期: 2026-07-23
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0089

## Goal


- 无损迁移 legacy live 五件套并完成真实仓 strict dogfood。

## In Scope


- migration plan/apply/rollback、备份、幂等、fixture、当前仓 dogfood与升级说明。

## Out of Scope


- 不改历史 `.ai/iterations/` 归档。

## Acceptance Checklist


- [ ] AC1: migrate plan 零写报告同名段映射、缺失/未知/重复和 apply readiness。
- [ ] AC2: apply 备份原文件并原子写 canonical；已识别正文逐段保留，未知/重复 fail-closed。
- [ ] AC3: 重复 apply 幂等，rollback 只在当前仍等于 post hash 时恢复，漂移拒绝。
- [ ] AC4: legacy 历史归档字节不变，当前 Butler 五件套迁移后 project check strict 全绿。
- [ ] AC5: 迁移、hook、audit、完整 CI、state audit、diff check 全部通过并收口 MILE-0011。

## Verification Method


- 隔离 migration fixture + 当前仓迁移前后 hash + 完整 CI/审计。

## External References


- N/A

## Open Questions / Risks


- N/A
