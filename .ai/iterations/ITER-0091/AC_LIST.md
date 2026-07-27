---
状态: ack-frozen
ACK 日期: 2026-07-25
---
> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户确认（ITER-0091，2026-07-25）
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0091

## Goal

- 建立可机械复核的轻量 TDD Red→Green 配对合同，让显式声明的 cycle 不能只靠口头声称完成。

## In Scope

- TECH_PLAN cycle 声明格式、evidence ID 约定、只读配对检查器、正负向 fixture 与 R1 文档。

## Out of Scope

- 不接 P5/Goal 收口门，不改 evidence record v1，不新增 sidecar/台账，不证明代码修改时序或 Red 原因有效性。

## Acceptance Checklist

- [ ] AC1: TECH_PLAN 可在 `Test Strategy` 中用版本化 marker + 固定表头声明 cycle 名、AC、argv JSON 与项目相对 cwd；无声明时明确为未启用 TDD。
- [ ] AC2: 每个 cycle 只认 `tdd-<cycle>-red` 与 `tdd-<cycle>-green` 两条现有 evidence v1 record，cycle 名和声明重复/非法时 fail-closed。
- [ ] AC3: 检查器要求 Red outcome=`failed`、Green outcome=`passed`，且 Red 完整结束后 Green 才开始。
- [ ] AC4: Red/Green 的 argv、cwd 与声明完全一致，record 的 iteration、AC 与文件完整性继续复用现有 verifier 校验。
- [ ] AC5: 缺 Red/Green、outcome 错、顺序颠倒、命令或 cwd 漂移、AC 漂移、坏 JSON/坏路径等负向 fixture 全部拒绝并给出可操作诊断。
- [ ] AC6: 不改变 `run/verify/archive/reopen` 现有行为；未声明 TDD 的 TECH_PLAN 零新增文件、检查结果为 N/A/pass。
- [ ] AC7: evidence 专项测试、artifact 合同检查、完整 CI 与 diff check 通过。

## Verification Method

- AC1–AC6：`tools/verification-evidence/test_evidence.py` 正负向 CLI fixture。
- AC7：专项 unittest、artifact contract、完整 CI 与 diff check。

## External References

- N/A

## Open Questions / Risks

- N/A
