---
title: 技术方案模板
audience: AI / 开发者
scope: P3 Design 阶段的技术方案模板、边界字段与验证规划口径
---

# Tech Plan Schema

## 1. 目标

用于在进入实现前，把改动边界、关键设计决策与验证方式说明清楚。

## 2. 交付约定

- 必须产出：`.ai/TECH_PLAN.md`
- 必填字段：`Goal`、`Files / Modules to Change`、`Interface / Contract`、`State / Boundary`、`Design Decisions`、`Execution Steps`、`Verification Plan`、`Risks / Open Questions`
- 可选字段：`External References`（当 `.ai/references/` 下存在参考资料时必填）

## 3. 标准模板

```md
# Goal
- 本阶段要支撑哪些 AC

# Files / Modules to Change
- 计划修改的文件、模块或目录
- 每个改动点的职责

# External References
- .ai/references/api-xxx.md — 接口契约来源，影响 Interface / Contract 定义
- .ai/references/design-xxx.md — UI 规格来源，影响 Files / Design Decisions

# Interface / Contract
- 涉及的接口契约
- 数据结构、输入输出或依赖关系
- 若接口定义来自外部参考资料，标注来源文件

# State / Boundary
- 状态边界
- 模块职责边界
- 明确不在本次处理范围内的扩展点

# Design Decisions
- 关键设计选择
- 取舍与原因
- 受哪些 active profiles 约束

# Execution Steps
- 实现顺序
- 子任务拆分方式

# Verification Plan
- 每个 AC 或关键改动点如何验证

# Risks / Open Questions
- 当前剩余风险
- 尚未关闭的问题
```

## 4. 编写规则

- 必须能映射回已确认的 AC，禁止脱离验收标准独立扩张。
- 文件范围、接口契约、边界与验证方式必须明确。
- 若存在 active profiles，应写明其约束点；未命中时只按通用 SOP 与质量门禁设计。
- 若 `.ai/references/` 下存在已处理的外部参考资料，必须在 `External References` 中列出，并在 `Interface / Contract` 和 `Design Decisions` 中标注哪些决策来源于参考资料。
- 不把执行细节写成流水账，重点保留关键设计与实现边界。

## 5. 与执行流程的关系

- P3 阶段必须产出 `.ai/TECH_PLAN.md`，作为 P4 执行的唯一边界依据。
- P3 从 `.ai/AC_LIST.md` 读取输入，逐项映射验收项。
- P4 阶段实现必须逐项遵循这里的边界与执行顺序。
- 若设计影响面扩大，应回退到 P3 更新此文件。
- 简化路径下可口头确认方案，不强制产出此文件。