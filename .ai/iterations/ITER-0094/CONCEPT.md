<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0094 · Butler 配置部署与 legacy 迁移

分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-28

> ⚠️ 危险模式：本产物由模型自主确认问题理解，未经用户逐项确认（ITER-0094，2026-07-28）

## Current Understanding

- R1 已提供严格 JSON schema 与单文件原子读写；R2 要让新部署直接拥有该配置，并让旧项目能从 `.ai/local-constraints.md` 无损提取开关和 Active Profiles。
- 迁移后 `local-constraints.md` 只保留需要人解释的项目类型、约束、范围例外和外部资料；机器配置段与 Active Profiles 不再双写。
- R2 建立兼容读取和升级器事务动作，但不切换危险模式、独立复核、偏好或进度等消费端；这些统一留给 R3。

## Scope

- 扩展 `tools/project-config/`：严格解析 legacy Markdown、JSON 优先解析、显式冲突诊断和可供升级器调用的迁移计划。
- 扩展 `tools/butler-upgrade/`：新增有限的 `migrate_config` 项目 action，把 JSON 创建与 Markdown 收窄纳入既有备份/恢复事务。
- 更新基地车部署、本地约束 schema 和工具说明；新增迁移正负向测试，不提前登记未发布版本的 manifest action。

## Open Questions / Risks

- legacy `Active Profiles` 可能包含散文；迁移只接受明确的“无”或单 profile 标识列表，模糊内容必须 fail-closed，不能猜。
- 当前 VERSION 仍为 3.2.0；R2 只交付 action 能力，实际版本链登记由 R3 与发布接线统一处理，避免提前制造不可达迁移。
