# ITER-0064 · Goal 运行时校准与问题回流

> 迭代交付 · 2026-07-18 · MILE-0008 R4 · 危险模式自主 ACK / 完整审查

## 本次交付目标

让执行、测试和审查发现的坏消息改变 Goal 状态并回到正确阶段，而不是只写一句风险后沿旧计划做完。

## 已完成内容

- 新增六类校准信号与 task-state 六字段活跃投影，不建第二问题台账。
- 按事实性质路由 P1 objective、P2 AC、P3 plan、P4 implementation、P5 proof/review 或诚实停。
- open/blocked 信号派生 Goal at-risk/blocked；tasks done、风险备注和危险模式不能覆盖。
- 明确 AC 重 ACK、方案重准入、扩张/closed 新迭代及新 evidence/review 才 resolved。
- 接入九个消费者，新增结构测试并纳入固定 CI。

## 验证方式与结果摘要

- 最终结构合同 8/8，完整矩阵检查 975 个 Markdown 文件/43 链接、8 skills/plugin、135 hooks 与双宿主矩阵，全部通过。
- 强审修复 1 Must Fix（伪枚举占位行）和 1 Should Fix（错误章节引用），最终清零。

## 已知剩余风险 / 延后事项

- R4 不是自动分类器；R5 将机械消费未闭合信号并裁决完成资格。
- 未执行 fresh-context 独立复核。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0064/`
- `Coder/20_Workflow_Lifecycle/goal-calibration.md`
- checkpoint `9883f7d`
