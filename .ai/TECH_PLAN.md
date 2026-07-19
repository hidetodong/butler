---
迭代: ITER-0069
方案状态: pass
准入方式: dangerous-ack
---

# Plan Summary

在既有“索引行 ↔ 草稿文件”集合对账上增加候办块语义：录入时按独立启动边界拆分，审计时把 frontmatter 身份收紧为恰好一个键和一个状态。

# Design Decisions

- 候办块以“可否独立决定开工/提升”为拆分判据，不按段落数量或路线项数量机械切。
- 台账继续保持紧凑表格索引；“不同块”由不同索引行和不同草稿文件共同表达，不在台账内嵌长正文。
- 草稿 identity 使用行级正则精确计数，避免正文提到 `候办键` 时误报。
- 已有路径、slug、非软链与集合对账保持不变。

# Alternatives and Trade-offs

- 每个候办建子目录：隔离更强，但当前每个候办只有一份方向稿，目录层级没有收益，暂不采用。
- 单文件多二级标题：写入少，但无法独立提升与删除，直接违背用户目标，否决。

# Failure Paths

- 多方向边界不清：先分别提炼可独立启动的方向，不确定时保守保持同一里程碑并在路线图拆项。
- 任一草稿或索引写失败：不得留下半套候办集合，状态审计报漂移。
- 草稿重复身份字段：审计失败，不能进入完成态。

# Impact Surface

- `Coder/20_Workflow_Lifecycle/milestone-schema.md`
- `.claude/commands/butler/milestone.md`
- `plugins/butler/skills/butler-milestone/SKILL.md`
- `workflows/registry.json` 及生成投影
- `scripts/audit-project-state.py`
- `scripts/test-audit-project-state.py`

# Verification Plan

- 运行状态审计专项。
- 运行 workflow registry 对账与 `git diff --check`。
- 运行 `bash scripts/verify-ci.sh` 并交 Goal adjudicator 裁决。

# Execution Steps

- [x] T1：更新候办块和多方向拆分真源 → AC1–AC2
- [x] T2：同步双宿主与 registry 投影 → AC3
- [x] T3：收紧草稿身份审计并补正负回归 → AC4–AC5
- [x] T4：完整验证、强审、归档交付与知识折叠 → AC1–AC5

# Plan Admission

- AC 覆盖：5/5。
- 假设：独立方向可以用“能否单独启动/提升”稳定区分。
- 反证：按路线项切会把同一版本拆碎，已明确排除。
- Must Fix：0。
- Verdict：pass。
