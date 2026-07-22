---
状态: ack-frozen
ACK 日期: 2026-07-22
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0075，2026-07-22）。

# Goal

- 把“一个项目包含多份独立需求、每份需求独立改版”固化为唯一、可验证的 references 契约地基。

# In Scope

- 项目级 PRD 总索引、日期化 `prd_id`、单需求内部结构。
- 全新需求与已有需求新版的身份判定及歧义停机规则。
- legacy 单 PRD 根结构的兼容定位与后续迁移边界。
- README 导航和结构测试。

# Out of Scope

- 不实现 monorepo 工作区范围、inbox、首切/更新命令适配、多 PRD AC 钉版、迁移执行或范围门禁。
- 不移动任何现有项目的 PRD 文件，不改非 PRD 扁平 references 流。
- 不为 `prd_id` 引入数据库、全局注册服务或内容寻址身份。

# Acceptance Checklist

- [ ] AC1：契约明确 `prd/00_INDEX.md` 是项目级需求总索引，并给出能路由到单份需求的最小登记字段。
- [ ] AC2：`prd_id` 严格采用 `YYYY-MM-DD-<requirement-slug>`；日期来源、slug 规则、首次分配和跨改版/改标题不变语义无歧义。
- [ ] AC3：单份需求落在 `prd/<prd_id>/`，拥有自己的 `00_INDEX.md`、模块切片与 `.archive/vN/` 全量历史；不同需求的版本号互不关联。
- [ ] AC4：契约给出“全新需求 / 已有需求新版”判定顺序、可用身份信号、重复输入和冲突/歧义的 fail-closed 处置。
- [ ] AC5：项目级索引与单需求模块索引职责分开；`prd_id` 与模块 `slug` 不混用、不复用，引用层级可唯一表达。
- [ ] AC6：旧 `prd/00_INDEX.md + <slug>.md + .archive/` 被明确标为 legacy 单 PRD 结构；R1 不静默迁移，兼容与迁移动作指向后续路线。
- [ ] AC7：README 导航与结构测试同步；测试机械校验目录示例、字段、稳定身份、独立版本、歧义停机和 legacy 边界，完整 CI 不回归。

# Verification Method

- AC1–AC6：标准库 unittest 读取 `references-schema.md`，校验固定章节、目录树、字段与关键 MUST/不得语义；主 agent 对照 MILE-0009 R1 逐项语义复核。
- AC7：运行新增专项测试、`bash scripts/verify-ci.sh`、`git diff --check` 和状态审计；确认 Out of Scope 文件无非状态性改动。

# Open Questions / Risks

- 日期化身份若误判后再改会破坏引用，因此真正的 intake 动作必须在 R4/R6 继续保留提议/确认或等价审查门；R1 只定 fail-closed 契约。
- legacy 兼容尚未由执行器证明，R1 只能声明“不迁、不假装已兼容”；迁移与真实样例验证由 R5/R8 完成。
