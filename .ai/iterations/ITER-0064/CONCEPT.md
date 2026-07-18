> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-18

# 一句话

- R4 让执行中新发现的问题改变真实计划和 Goal 状态，而不是只留一句风险后继续把任务勾完。

# Goal

- 定义运行时校准信号、单一投影格式和确定回流路由，把“发现问题”闭合为“回正确阶段修、重审或停机”。

# Current Understanding

- Goal Contract 已有 at-risk/blocked，P3 已有 verdict，但尚无规则决定测试失败、假设失效或审查意见该回哪一层。
- 新事实的权威真源仍是 CONCEPT/AC/TECH_PLAN/代码/evidence/review；task-state 只保存未闭合信号和下一动作，不能成为第二问题台账。
- 问题严重度不能由“能否继续写代码”替代；只要会阻止完成，就必须使 Goal 至少 at-risk。

# Constraints

- 分层回写必须确定：目标错回 P1，完成定义错回 P2，方案错回 P3，实现错留 P4，证明错回 P5，真阻塞停机。
- AC/方案实质变化必须复用既有 draft→ACK / draft→Plan Admission 门，不另造旁路。
- 已关闭迭代出现新事实不得改历史，开新迭代承接。
- R4 不实现 R5 最终 completion CLI，也不做 R6 宿主投影。

# Impact Scope

- 新增共同规则 `goal-calibration.md`，接入 lifecycle、correction、context persistence、verify、review、dangerous 与规则卡；增加结构测试。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具；无领域 profile；危险模式 ON。

# Open Questions

- 无阻塞问题。R5 再把 unresolved signal 接入机械完成裁决器。
