---
状态: ack-frozen
ACK 日期: 2026-07-28
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0094

> ⚠️ 危险模式：本验收清单由模型完成反证、自洽性与可验证性审查后自主 ACK，未经用户确认（ITER-0094，2026-07-28）

修订记录: 2026-07-28 · 明确 legacy `Review Policy` 也属于待移除机器段；仍在原迁移影响面内，自审后重新冻结。

## Goal

- 让新项目直接采用 JSON 配置，并让旧项目能在不丢开关、profile 或人类约束正文的前提下事务迁移到新结构。

## In Scope

- legacy 解析、JSON 优先兼容读取、冲突诊断、升级器有限 action、新部署/本地约束规则和迁移测试。

## Out of Scope

- 不切换现有配置消费端，不登记未发布版本 migration，不修改外置偏好数据或任务运行状态。

## Acceptance Checklist

- [ ] AC1: legacy parser 能确定性读取三个开关与 Active Profiles；段缺失采用安全默认，模糊值、重复/非法 profile 和未知开关值 fail-closed。
- [ ] AC2: 兼容读取在 JSON 存在时以 JSON 为真源并报告与 legacy 的字段冲突；JSON 缺失时回退 legacy，二者都缺失时返回规范默认且零写。
- [ ] AC3: 迁移计划生成规范 `.ai/butler.config.json`，并只从 `local-constraints.md` 删除 Active Profiles、Butler 功能开关和 legacy Review Policy 机器段，其余字节和段落顺序保持不变。
- [ ] AC4: 升级器新增 schema 化 `migrate_config` 项目 action；plan 零写，apply 把 JSON 与 Markdown 变更放进同一备份/恢复事务，冲突、symlink 和故障均不留下半迁移。
- [ ] AC5: 新项目部署规则直接生成安全默认 JSON，并让 `local-constraints.md` 回归人类可读职责，不再要求机器开关段或 Active Profiles 双写。
- [ ] AC6: 迁移幂等；已有合法同值 JSON 可安全收窄 Markdown，已有冲突/损坏 JSON 拒绝，旧文件没有可迁移段时也有明确结果。
- [ ] AC7: project-config 与 upgrader 专项覆盖正常/缺失/冲突/损坏/模糊/事务回滚，完整 CI、artifact/state 检查和 diff check 不回归。

## Verification Method

- AC1–AC3, AC6：`tools/project-config/tests/test_config.py` 覆盖 parser、resolve 和 migration plan。
- AC4, AC6：`scripts/test-butler-upgrade.py` 注入 `migrate_config` action，验证零写、事务应用、幂等和故障恢复。
- AC5：规则/模板合同测试与 Markdown 链接检查。
- AC7：两组专项、完整 `scripts/verify-ci.sh`、状态审计和 `git diff --check`。

## External References

- N/A

## Open Questions / Risks

- N/A
