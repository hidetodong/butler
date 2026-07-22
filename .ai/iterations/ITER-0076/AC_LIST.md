---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0076，2026-07-22）。

# Goal

- 建立稳定、可机械消费的工作区地图和需求级代码范围契约。

# In Scope

- `.ai/project/workspaces.md` 的地图结构与稳定键。
- package identity 优先、目录移动、嵌套/冲突边界。
- primary/supporting/read-only/excluded 四类需求范围。
- 模块范围子集、默认拒绝和越界扩张审查。
- 单包退化态、README/references 接线和结构测试。

# Out of Scope

- 不实现实际写入门禁、diff 扫描、自动 workspace discovery 或迁移器。
- 不按包复制 PRD，不修改已冻结历史需求范围。
- 不把宿主文件权限或 Butler 项目根授权替换成 workspace scope。

# Acceptance Checklist

- [ ] AC1：契约定义项目级 `.ai/project/workspaces.md`，最小字段能稳定映射 workspace key、包身份、当前相对路径、类型与状态。
- [ ] AC2：工作区键优先复用 package manifest 身份，分配后跨目录移动不变；重复键、重复路径、未知键和路径逃逸 fail-closed。
- [ ] AC3：单需求 `<prd_id>/00_INDEX.md` 声明 `primary_write`、`supporting_write`、`read_only`、`excluded` 四类范围，集合互斥且键必须存在地图。
- [ ] AC4：写权限只等于 primary + supporting；read-only/excluded 和未声明工作区默认不可写，excluded 默认也不读取。
- [ ] AC5：模块级范围只能是需求级范围的同类或更窄子集，不能通过模块声明扩大写集合或解除排除。
- [ ] AC6：越界扩张必须先给出原因、影响、拟新增键和验证，更新范围后重新审查；目录移动只改地图，不改 PRD 历史身份。
- [ ] AC7：单包项目 `root` 退化态、references/README 接线及结构测试完整，完整 CI 不回归。

# Verification Method

- AC1–AC7：标准库 unittest 检查 schema 章节、表字段、四类集合、集合代数、fail-closed 和退化态；主 agent 逐项语义审查。
- AC7：运行专项测试、完整 CI、`git diff --check` 与状态审计。

# Open Questions / Risks

- package manager 对 workspace 的发现语法各异，R2 不实现解析器；契约只要求记录“证据来源”。
- 真正写入对账尚未交付，因此 R2 不能宣称越界会被 hook 自动阻止。
