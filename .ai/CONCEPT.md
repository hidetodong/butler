> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-18

# 一句话

- R3 把“方案看起来写完了”与“方案真的获准执行”分开：TECH_PLAN 必须主动反证并得出可机读 verdict，未通过就不能进入 P4。

# Goal

- 为 Butler 的 P3 建立结构化方案准入合同、状态机与双宿主共享源码写门禁。

# Current Understanding

- 现有 P3 只要求 TECH_PLAN 存在并等待 ACK；危险模式也只有散文式自审，没有可供 Goal 或 hook 消费的判定。
- verdict 应住在 TECH_PLAN 自身，避免新增审批文件；`Plan Admission` 记录覆盖、假设、替代方案、失败路径、影响面和验证盲区。
- 用户 ACK 或危险模式自审都不能覆盖已知缺陷：只有没有 Must Fix 的方案才可置 `pass`。

# Constraints

- `draft / pass / revise / blocked` 是封闭状态；`revise` 回 P3，`blocked` 诚实停机。
- 已通过方案发生实质修改后必须退回 `draft` 重审。
- 旧版 TECH_PLAN 无状态字段时暂时放行，避免模板升级前误杀既有项目；新 schema 不允许省略。
- R3 不实现执行中问题回流、最终完成裁决或宿主 Goal 同步。

# Impact Scope

- 修改 P3 schema/lifecycle/危险模式/Goal 合同/规则卡与部署说明；增强 Claude/Codex 共用 `phase_gate`；增加专项结构测试与 hook 回归。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具；无领域 profile；危险模式 ON。

# Open Questions

- 无阻塞问题。兼容窗口何时移除留给后续升级里程碑，不在 R3 强拆旧项目。
