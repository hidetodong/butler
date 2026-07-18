---
方案状态: pass
方案审查日期: 2026-07-18
方案审查方式: dangerous-self-review
---
> ⚠️ 危险模式结构化自审 pass（ITER-0066）。

# Goal
- 用共同规则卡和驻留工具完成薄宿主接线。

# Files / Modules to Change
- `goal-contract.md`、context persistence、mcv deployment/update、compatibility docs、rule-card、AGENTS template/README；`scripts/test-goal-host-wiring.py`、CI。

# Interface / Contract
- projection=`objective + derived_state + blocking_reason + next_step`；direction 永远 project→host。

# State / Boundary
- 宿主能力 discovered/absent 两态；absent 不建替代文件。

# Design Decisions
- 不新增 workflow/daemon；复用入口 renderer 保证双端同卡。
- R6 只交付源模板与重渲染路径，不伪造尚未发布 migration。

# Plan Admission
- AC Coverage：pass。
- Assumptions：两入口都由同一 rule-card renderer 生成，现有测试可隔离验证。
- Alternatives / Trade-offs：否决 host-specific GOAL 文件和双向同步；薄投影牺牲宿主 UI 细节换单一真相。
- Failure Modes：host 反写、入口漂移、无 API 假装同步、旧项目假报升级；均有合同/测试/披露。
- Impact / Scope Challenge：不加第九 workflow、不切版。
- Verification Blind Spots：无法冻结未来宿主 API，只验证当前入口合同与降级。
- Verdict：pass。

# Execution Steps
- [ ] T1 投影/降级/恢复合同与文档接线 → AC1–AC4、AC6
- [ ] T2 双入口 host wiring 测试与 CI → AC5、AC7
- [ ] T3 evidence/强审/迭代与 milestone 收口 → AC1–AC7

# Verification Plan
- 专项至少 7 tests；完整矩阵；adjudicator eligible；closed milestone state audit。

# Risks / Open Questions
- 外部旧项目等下次版本 migration，明确入账不冒充完成。
