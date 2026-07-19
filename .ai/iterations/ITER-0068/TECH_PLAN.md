---
迭代: ITER-0068
方案状态: pass
准入方式: dangerous-ack
---

# Plan Summary

在正式里程碑生命周期之前增加一个轻量候办层：台账末尾索引未编号候办项，独立草稿文件保留已合成内容；提升到 active 时才领号。

# Design Decisions

- 候办索引仍放在 `.ai/MILESTONES.md`，让用户要的“待办区”在同一看板可见；详细内容放 `.ai/milestone-backlog/<slug>.md`，避免台账膨胀。
- 候办键直接用稳定 slug，不新增另一套数字号码；索引行包含标题、暂缓日期、草稿路径和原因。
- 正式编号只从正式表分配；候办键、草稿文件名与对话里曾经称呼的临时号都不参与计算。
- 退回候办是“开启前撤销”，不是新的 paused 状态；必须同时通过最新号、零迭代、零归档、零交付四个检查。
- 扩展既有只读状态审计，同时核对正式号连续性与候办索引/草稿集合。
- 收口裁决严格区分“证据包完整”和“证据能打绿”：失败诊断记录必须保留且校验完整，但只有 `passed` 记录能提供 AC 覆盖。

# Alternatives and Trade-offs

- 给正式里程碑加 `paused`：它仍占号，没解决问题，而且会扩大 active 归属语义，否决。
- 把候办详情全塞进 `MILESTONES.md`：文件会随讨论内容无界增长，否决。
- 只留一行候办标题：简单，但丢失已讨论的范围和路线图，无法跨会话恢复，否决。

# Failure Paths

- 候办 slug 重复、路径越界或草稿缺失：停止写入/提升，先修复台账。
- 误开里程碑已有任何迭代引用：禁止退回，改走 closed 或 abandoned。
- 删除中间正式号造成缺口：状态审计拒绝。
- 候办草稿和索引只更了一边：状态审计拒绝。
- 自动验证先失败、后续重试通过：两份 record 都保留；裁决器验证全部记录完整性，只聚合通过记录的 AC 覆盖。

# Impact Surface

- `Coder/20_Workflow_Lifecycle/milestone-schema.md`
- `Coder/20_Workflow_Lifecycle/lifecycle.md`
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md`
- `Coder/20_Workflow_Lifecycle/goal-contract.md`
- `.claude/commands/butler/milestone.md`
- `plugins/butler/skills/butler-milestone/SKILL.md`
- `templates/rule-card.md`
- `Coder/README.md`
- `.ai/project/capabilities.md`
- `scripts/audit-project-state.py`
- `scripts/test-audit-project-state.py`
- `tools/goal-assurance/goal.py`
- `tools/goal-assurance/test_goal.py`

# Verification Plan

- 状态审计单测：正常候办通过；缺草稿、孤立草稿、编号缺口、候办偷用 `MILE-NNNN` 均失败。
- 结构检查：真源、双宿主入口、规则卡和能力摘要同时包含候办/开工领号边界。
- 完整验证：`bash scripts/verify-ci.sh` 和 `git diff --check`。
- 完整路径证据由 verification evidence runner 生成，最终由 Goal adjudicator 裁决收口资格。

# Execution Steps

- [x] T1：修改里程碑真源和寿命周期接线 → AC1–AC6
- [x] T2：同步 Claude/Codex 入口、规则卡、部署说明与能力摘要 → AC6, AC8
- [x] T3：扩展状态审计和回归 fixture → AC3–AC7
- [x] T4：运行专项/完整验证、强审、归档和交付 → AC1–AC8

# Plan Admission

- AC 覆盖：8/8。
- 关键假设：正式里程碑号的价值是表达开工/交付顺序，候办顺序不需另一套数字时间线。
- 替代方案：`paused` 不能解决占号；单行候办不能保真；候办详情全进台账会无界增长。
- 影响面：已列出规则真源、双宿主入口、审计器与项目投影；不涉及 hook 或外部项目升级。
- 验证盲区：AI 的语义路由无法只靠 Python 单测证明，因此用真源+双宿主投影结构检查和状态 fixture 共同约束。
- Must Fix：0。
- Verdict：pass。
- P5 修订：收口裁决器与 `verify-schema.md` 的失败证据保留契约冲突，方案短暂退回 `draft`；补上“全记录校验、只通过记录覆盖”及三类回归后重审，Must Fix 0，再次 pass。
