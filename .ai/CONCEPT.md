# Goal

- 修复 Butler Nice to Have Bucket F（低风险文档级精简与微调）5 条问题：`architecture-overview § 3` 空旷、`logic-protocol § 4.2` 三段已接近独立子节、`architecture-overview § 2.2` 硬编码 profile 文件名、`HUMAN_GUIDE` 规则速查图偏粗、`context-persistence § 3` task-state 双形式（JSON/MD）。

# Current Understanding

- 本任务是 Butler 规则仓维护的第七轮（已通过 v0.0.8 里程碑）。
- 5 条改动都是文档级精简或微调，无契约变更（除 N-7 task-state 单选算轻度契约调整）。
- 其中 2 条存在设计取舍（N-1 § 3 处理方式、N-7 task-state 选 .md 还是保留双选），其他 3 条路径相对清晰，可作为推荐方案直接 ACK。
- 本轮整体 ROI 高、成本低；主要用于把仓库进一步收敛到"无冗余、无空旷段、无双形式选项"的状态。

# Constraints

- 显性约束：
  - 不重组 `10_Domain_Stack_Profiles/` 目录（属于 Bucket H 范畴，本轮 out of scope）。
  - 不新增 schema 文件（属于 Bucket G 范畴，N-5 不在本轮）。
  - 不改变 lifecycle / 产物链 / mcv-deployment 等核心规则的语义。
- 隐性约束：
  - 文档美观与可读性优先；任何改动都应该让规则更清晰、不更复杂。

# Impact Scope

预计修改文件：
- `Coder/architecture-overview.md`（N-1 § 3 重构 + N-3 § 2.2 通用化）
- `Coder/00_System_Prompt/logic-protocol.md`（N-2 § 4.2 拆 H4）
- `HUMAN_GUIDE.md`（N-4 速查图扩展）
- `Coder/40_Context_Management/context-persistence.md`（N-7 载体单选）

不影响：所有其他规则文件、templates、scripts、Extension、Domain Profiles、`.ai/` 产物链结构。

# Project Type / Active Profiles

- 项目类型：Markdown 规则仓库。
- 未命中任何 Domain Profile。

# Open Questions

- **N-1** `architecture-overview § 3` 处理方式需用户拍板。
- **N-7** `task-state` 单选 `.md` 还是保留双选需用户拍板。
- 其余 3 条（N-2 / N-3 / N-4）按推荐方案执行（详见 AC_LIST）。
