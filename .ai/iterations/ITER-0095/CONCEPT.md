<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0095 · Butler 配置全链路接线与 3.3.0 发布准备

分流: 完整 | 命中升级信号: 跨模块消费端、项目状态迁移、发布元数据、兼容性验证 | 2026-07-28

> ⚠️ 危险模式：本产物由模型自主确认问题理解，未经用户逐项确认（ITER-0095，2026-07-28）

## Current Understanding

- R1 已建立严格 JSON 配置内核，R2 已建立部署与 legacy 事务迁移；R3 要让所有活消费端只通过该内核读取或回写，不再各自解析 Markdown。
- 兼容读取统一用 `resolve`：JSON 存在即为真源并报告 legacy 冲突，缺失才回退旧 Markdown；回写统一用 `set` 且只写 JSON，legacy 项目必须先升级，避免重新制造双写。
- 本仓应以真实当前值 dogfood 迁移：`dangerous=true`、`independent_review=false`、`preference=true`、`profiles=[]`，并从 `local-constraints.md` 移除机器段，保证当前自治语义不变。
- 版本链目标为向后兼容新增能力的 v3.3.0（MINOR）。本轮可准备版本、CHANGELOG、migration recipe/manifest 和验证，但没有 commit、tag、push 授权，因此最终必须明确标成 UNRELEASED。

## Scope

- 更新危险模式、独立复核、偏好、进度、review 与会话入口的规则/命令/skills，使读取统一委托 project-config `resolve`，写入统一委托 `set`。
- 更新 README、HUMAN_GUIDE、工作流与架构文档，消除活文档对 Markdown 机器段的旧指引；保留历史归档和历史 migration 的事实文本。
- 为消费合同增加机械结构测试；把 `migrate_config` 登记进 v3.3.0 迁移 manifest，并覆盖版本升级、缺失配置和 legacy 兼容路径。
- dogfood 迁移本仓，完成专项、完整 CI、状态审计、diff check、迭代/里程碑交付与发布候选元数据。

## Open Questions / Risks

- Markdown 命令本质是宿主协议，无法直接执行导入；必须用结构测试锁定唯一 CLI 入口、错误处理和“legacy 只读/JSON 回写”边界。
- 本仓当前危险模式为 on，迁移不得短暂落成默认 false；配置文件和 Markdown 收窄应作为同一逻辑变更审查。
- 版本元数据若先于交付生成会让 CHANGELOG 链接或审计短暂失配；先登记未来迁移配方，待 ITER/MILE 关闭后再对齐 VERSION、插件版本和根 CHANGELOG，并重跑关闭态完整验证。

---
状态: ack-frozen
ACK 日期: 2026-07-28
---
