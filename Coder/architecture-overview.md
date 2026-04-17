---
title: Coder 规则架构总览
audience: AI / 开发者
scope: Coder 子系统中 SOP Core、Domain / Stack Profiles、Business Extension 的分层关系与启用顺序说明
---

# Rules Architecture Overview

## 1. 目标

`Coder/` 不是某个单一技术栈的默认开发规范，而是一套**通用需求开发 SOP**。

它把规则拆成三层：

- **SOP Core**：定义通用流程、质量门禁与上下文治理。
- **Domain / Stack Profiles**：定义特定工程形态或技术栈下的执行细则。
- **Business Extension**：定义当前业务语义下的最高优先级约束。

## 2. 三层分工

### 2.1 SOP Core

包含：

- `00_System_Prompt/`
- `20_Workflow_Lifecycle/`
- `30_Quality_Gate/`
- `40_Context_Management/`

职责：

- 决定任务如何推进。
- 决定验收如何定义。
- 决定质量如何验证。
- 决定长任务如何记录、交接与压缩上下文。

这部分默认适用于大多数工程任务。

### 2.2 Domain / Stack Profiles

包含：

- `10_Domain_Stack_Profiles/` 下的所有 profile 文件，按当前项目命中的技术栈、语言或构建形态按需启用。

职责：

- 在命中对应项目类型后，补充更细的实现约束。
- 约束组件写法、类型建模、构建协作等特定领域问题。
- 不作为所有任务默认前置必读。

### 2.3 Business Extension

包含：

- `99_Business_Extension/*.md`

职责：

- 表达具体业务语义、业务边界与业务优先级。
- 作为最高优先级业务约束参与当前任务。
- 不替代 SOP Core，也不直接把技术实现细节提升为通用规则。

## 3. 启用顺序与生效规则

具体读取顺序以 `README.md § 读取顺序` 为准；本文件仅负责说明三层分工的职责边界与 profile 条件生效的语义。生效规则：

- **默认生效**：SOP Core。
- **条件生效**：Domain / Stack Profiles。
- **高优先级业务约束**：Business Extension。

换句话说：

- 先按通用 SOP 定义任务怎么做。
- 再按业务约束决定任务为什么这样做。
- 最后按命中的 profile 细化任务具体怎么落地。

## 4. 在生命周期中的作用点

- **P1 Analysis**：识别项目类型，并决定是否启用 profile。
- **P2 Acceptance**：只把已激活 profile 对应的完成定义纳入 AC。
- **P3 Design**：将已激活 profile 作为设计约束。
- **P4 Execute**：执行时只应用已激活的 profile 细则。
- **P5 Verify**：按“通用质量门禁 + 已激活 profile”进行验证。

## 5. 判断原则

当某条规则看起来像“前端规范”“Vue 规范”或“构建规范”时，不应默认套用到所有项目。

应先问：

- 当前项目是否真的命中了这个技术栈？
- 这条规则属于通用 SOP，还是属于某个 profile？
- 如果当前项目未命中，该规则是否应完全不启用？

若答案指向特定技术栈，则应把它视为 `10_Domain_Stack_Profiles/` 中的条件规则，而不是通用底座。
