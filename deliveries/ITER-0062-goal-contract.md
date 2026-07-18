# ITER-0062 · Goal Contract 与派生状态机

> 迭代交付（小版本） · 2026-07-18 · MILE-0008 R2 · 危险模式自主 ACK / 完整审查

## 本次交付目标

把 Butler 已有的目标、范围、AC、方案、进度、证据和审查组合成一份 Goal Contract，让“任务做完”只能进入完成候选，不能直接冒充目标完成。

## 已完成内容

- 新增 `goal-contract.md`，定义 iteration/milestone 两层派生 Goal 视图，不新增 `.ai/GOAL.md`。
- 定义六状态、终态优先与非终态风险优先级，并明确允许/禁止跃迁。
- 明确宿主 Goal/Task 只是可重建投影，冲突时项目 `.ai/` 获胜。
- 以窄指针接入生命周期、CONCEPT/AC、milestone、context persistence 和 Coder 读序。
- 新增 7 项结构测试并接入固定 CI 入口。

## 关键变更 / 用户可感知变化

- tasks done 现在明确只等于 `completion-candidate`；AC、证据、review、风险和收口未闭合就不能 complete。
- milestone 最后一条路线 closed 也不会直接 complete，必须做版本级收口。
- 无宿主原生 Goal 能力时仍可只靠 `.ai/` 工作，不产生第二套真相。

## 高层影响范围

- 修改共同生命周期规则和验证入口；未修改 hook、plugin、宿主 API 或部署模板。

## 验证方式与结果摘要

- 强审前 6/6、修复后 7/7；两次完整矩阵 passed，覆盖 955 个 Markdown 文件/44 链接、8 skills/plugin、127 hooks。
- 强审修复 1 Must Fix（目录树漏注册）和 1 Should Fix（milestone candidate 消歧）；最终均清零。

## 已知剩余风险 / 延后事项

- 当前是规则合同，不是机械裁决器；R3–R6 继续完成方案准入、回流、裁决与宿主接线。
- 未执行 fresh-context 独立复核。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0062/`
- `Coder/20_Workflow_Lifecycle/goal-contract.md`
- checkpoint `4c6d99c`
