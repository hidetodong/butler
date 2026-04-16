---
title: 验收清单规范
audience: AI / 开发者
scope: P2 阶段验收清单的模板、编写规则与完成判定口径
---

# Acceptance Schema

## 1. 目标

验收清单用于定义“什么叫完成”，并作为设计、实现、验证的共同依据。

## 2. 交付约定

- 必须产出：`.ai/AC_LIST.md`
- 必填字段：`Goal`、`In Scope`、`Out of Scope`、`Acceptance Checklist`、`Verification Method`、`Open Questions / Risks`
- 可选字段：`External References`（当存在外部参考资料时必填）

## 3. 标准模板

```md
# Goal
- 本次任务要解决什么问题

# In Scope
- 本次明确包含的内容

# Out of Scope
- 本次明确不处理的内容

# Acceptance Checklist
- [ ] AC1: 功能完成项
- [ ] AC2: 结构正确项
- [ ] AC3: 质量达标项

# Verification Method
- AC1: 如何验证
- AC2: 如何验证
- AC3: 如何验证

# External References
- .ai/references/api-xxx.md — API 接口契约来源
- .ai/references/design-xxx.md — UI 设计规格来源

# Open Questions / Risks
- 当前未决问题
- 当前剩余风险
```

## 4. 编写规则

- 每条 AC 必须可验证，禁止模糊表述。
- 每条 AC 应尽量绑定一个明确验证动作。
- AC 应覆盖功能完成、结构正确、质量达标三类要求。
- AC 不得混入未来愿景、长期规划或下一阶段任务。
- 超出范围但相关的事项，应放进 `Out of Scope` 或 `Open Questions / Risks`。
- 若存在已处理的外部参考资料（`.ai/references/`），必须在 `External References` 中列出，并标注哪些 AC 项源自该参考资料。

## 5. 判定口径

一个任务可视为完成，至少应满足：

- 目标已被覆盖。
- 所有 In Scope 项已有明确落点。
- Acceptance Checklist 已全部可勾选。
- 每个 AC 都有对应验证结果。
- 剩余风险已显式说明。

## 6. 与执行流程的关系

- P2 阶段必须产出 `.ai/AC_LIST.md`，作为后续所有阶段的共同依据。
- P2 从 `.ai/CONCEPT.md` 读取输入（简化路径下，Goal 与 Constraints 直接写入 `AC_LIST.md`）。
- 若任务先经过 `/ideation`，只有已确认的决策才能被折叠进 Goal / In Scope / Acceptance Checklist / Verification Method。
- P3 阶段的技术方案必须逐项映射 AC。
- P4 阶段的实现不得脱离 AC 扩张范围。
- P5 阶段必须按 AC 回填验证结果。
