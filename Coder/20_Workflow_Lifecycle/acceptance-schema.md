---
title: 验收清单规范
audience: AI / 开发者
scope: P2 阶段验收清单的模板、编写规则与完成判定口径
---

# Acceptance Schema

> 结构机器真源：`tools/artifact-pipeline/artifacts.v1.json` + `templates/AC_LIST.md`。本文件解释字段语义；新 live 产物的 H2/表头/状态字段由 manifest 固定，条件段 N/A 不删除，legacy 归档不追溯改写。

## 1. 目标

验收清单用于定义“什么叫完成”，并作为设计、实现、验证的共同依据。

## 2. 交付约定

- 必须产出：`.ai/AC_LIST.md`
- 顶部冻结状态（frontmatter）：`状态`（取值 `draft` | `ack-frozen`）与 `ACK 日期`。完整路径必填；简化路径可选（省略即按 legacy 处理，详见 §4 与 §7）。
- 必填字段：`Goal`、`In Scope`、`Out of Scope`、`Acceptance Checklist`、`Verification Method`、`Open Questions / Risks`
- 可选字段：`External References`（当存在外部参考资料时必填）
- 可选 frontmatter：`prd_refs`（需求集合的新写法）——列表中每项固定 `prd_id`、ACK 时的 `prd_version` 与本迭代引用的 `module_slugs`，详见 §4/§5。legacy 单 PRD 只读兼容仍认单值 `prd_version`；两字段禁止并存。非 PRD / 对话驱动迭代两者都不写。

## 3. 标准模板

```md
---
状态: draft        # draft=写完待 ACK；用户 ACK 后改 ack-frozen
ACK 日期: —        # 置 ack-frozen 时填写
prd_refs:          # 可选；需求集合引用时整块填写；非 PRD 迭代省略
  - prd_id: 2026-07-22-user-login
    prd_version: v1.1
    module_slugs: [login-flow, validation-copy]
  - prd_id: 2026-07-23-batch-import
    prd_version: v2.0
    module_slugs: [import-rules]
---

> 分流: 简化 | 命中升级信号: 均未命中 | YYYY-MM-DD   （仅简化路径写在此；完整路径的分流记录写进 CONCEPT.md）

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
- .ai/references/prd/2026-07-22-user-login/login-flow.md — PRD 切片来源（版本与模块均取 frontmatter prd_refs）；支撑 AC2

# Open Questions / Risks
- 当前未决问题
- 当前剩余风险
```

## 4. 冻结状态字段（`状态` / `ACK 日期`）

- 语义：`draft` = AC 已写完、等待用户 ACK；`ack-frozen` = 用户（或 `/butler:dangerous` 自审门）已 ACK、本迭代验收范围冻结。
- 流程：AC_LIST 写完先置 `draft`；用户 ACK 后改为 `ack-frozen` 并填 `ACK 日期`，方可进入 P3。
- hook 联动：在部署了 butler hook 的项目，AC_LIST 处于 `draft` 时源码写操作会被 `phase_gate` 拦截，直到置 `ack-frozen`。无该字段的旧 AC_LIST 按 legacy 放行，不被误杀。
- amend 退回：迭代内小幅修订（`iteration-schema.md §5.3`）必须把 `状态` 退回 `draft`、重新等待 ACK 后再置 `ack-frozen`。
- `prd_refs` 绑定（需求集合引用适用）：置 `ack-frozen` 时逐项把 `prd_id + prd_version + module_slugs` **绑定到当刻事实**，之后钉住；需求 A 改版不能带动需求 B 的版本，也不能把模块从一项串到另一项。本迭代 P3/P5 对每项各自解析。amend 重冻时可显式增删项或重绑受影响项，未受影响项保持不变；完整改版仍走 `prd-update.md`。
- legacy `prd_version`：仅给迁移前单 PRD 旧产物继续读；它与 `prd_refs` 互斥。新集合产物不得因为只引用一份需求就继续写 legacy 字段。
- 简化路径：`状态` 字段可选；省略即按 legacy 放行。简化路径的一行分流记录写在 AC_LIST 顶部（格式见 §3）。

## 5. 编写规则

- 每条 AC 必须可验证，禁止模糊表述。
- 每条 AC 应尽量绑定一个明确验证动作。
- AC 应覆盖功能完成、结构正确、质量达标三类要求。
- AC 不得混入未来愿景、长期规划或下一阶段任务。
- 超出范围但相关的事项，应放进 `Out of Scope` 或 `Open Questions / Risks`。
- 若存在已处理的外部参考资料（`.ai/references/`），必须在 `External References` 中列出，并标注哪些 AC 项源自该参考资料。
- 需求集合的完整锚点是 `prd_id + prd_version + module_slug`。`prd_refs` 是唯一钉版表：每个 `prd_id` 最多一项，`module_slugs` 非空且项内不重复；正文路径不再重复版本。live 版本吻合时读 `prd/<prd_id>/<module_slug>.md`，否则读 `prd/<prd_id>/.archive/<prd_version>/<module_slug>.md`。
- `External References` 与 AC 正文必须使用带 `prd_id` 的集合路径，并能在 `prd_refs` 找到同项 module；未登记、跨项借同名模块或版本缺失均 fail-closed。P3/P5 使用同一列表，禁止另立版本。
- legacy 旧产物仍按 `prd_version + prd/<module_slug>.md` 解析；迁移后由 migration receipt 把隐式单 PRD 身份映射到唯一 `prd_id`，再按该需求 live/archive 取文件。解析真源与 CLI 见 `40_Context_Management/references-schema.md §8`。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）。

## 6. 判定口径

一个任务可视为完成，至少应满足：

- 目标已被覆盖。
- 所有 In Scope 项已有明确落点。
- Acceptance Checklist 已全部可勾选。
- 每个 AC 都有对应验证结果。
- 剩余风险已显式说明。

这些条目是 Goal 的 outcome obligations，不是 Goal 状态本身。即使 AC 表面全勾，也仍须按 `goal-contract.md` 核 proof、review 与收口事实；tasks done 或宿主 complete 都不能替代本清单。

## 7. 与执行流程的关系

- P2 阶段必须产出 `.ai/AC_LIST.md`，作为后续所有阶段的共同依据。
- P2 的用户 ACK 物化为 `状态: ack-frozen`，是进入 P3 的硬门（详见 `lifecycle.md` P2 与 `iteration-schema.md §5.2`）；未冻结时部署了 hook 的项目会拦截源码写操作。
- P2 从 `.ai/CONCEPT.md` 读取输入（简化路径下，Goal 与 Constraints 直接写入 `AC_LIST.md`）。
- 若任务先经过 `/ideation`，只有已确认的决策才能被折叠进 Goal / In Scope / Acceptance Checklist / Verification Method。
- P3 阶段的技术方案必须逐项映射 AC。
- P4 阶段的实现不得脱离 AC 扩张范围。
- P5 阶段必须按 AC 回填验证结果。
