> 分流: 完整 | 命中升级信号: 多文件改动、契约变更、跨模块影响、设计取舍 | 2026-07-18

# 一句话

- R2 把 R1 发现的散落目标事实组合成一份逻辑合同和派生状态机。目标状态不另存第二份，而从既有阶段产物推导，避免 Goal 与 AC、验证、台账各说各话。

# Goal

- 定义 Butler 通用 Goal Contract、状态优先级和完成候选语义，并把它接入生命周期与状态持久化规则。

# Current Understanding

- 新增 `.ai/GOAL.md` 虽直观，却会复制 objective、scope、AC、plan 和 evidence；R1 已证明这些各有真源，故选择派生视图。
- Goal Contract 是“既有真源如何共同回答目标状态”的组合协议，不是新文件格式。
- R2 只定义状态与读取/写入纪律；P3 方案 verdict、执行问题回流、完成裁决器和宿主同步仍属 R3–R6。

# Constraints

- 状态必须确定性优先：abandoned/blocked/at-risk/completion-candidate/active/complete 不得由模型凭语气挑选。
- `complete` 只能由迭代/里程碑收口事实派生；task-state 或宿主 complete 不能反向写项目真相。
- 极小任务不增加文件税；无持久产物时只做对话级目标/验证说明。
- 不在 R2 实现机械完成裁决器。

# Impact Scope

- 新增共同规则 `Coder/20_Workflow_Lifecycle/goal-contract.md`，接入 Coder 读序、lifecycle、schema 与 context persistence，并增加结构合同测试。
- 不修改 hook、plugin、宿主 API 或目标项目模板。

# Project Type / Active Profiles

- Markdown 规则仓 + Python/Bash 工具；无领域 profile；危险模式 ON。

# Open Questions

- `at-risk` 的问题分类与 phase 回流 action 由 R4 细化；R2 只定状态语义。
