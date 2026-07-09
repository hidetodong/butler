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
- 顶部冻结状态（frontmatter）：`状态`（取值 `draft` | `ack-frozen`）与 `ACK 日期`。完整路径必填；简化路径可选（省略即按 legacy 处理，详见 §4 与 §7）。
- 必填字段：`Goal`、`In Scope`、`Out of Scope`、`Acceptance Checklist`、`Verification Method`、`Open Questions / Risks`
- 可选字段：`External References`（当存在外部参考资料时必填）
- 可选 frontmatter：`prd_version`（当本迭代引用 `references/prd/` 切片时必填）——记 ACK 冻结那一刻 PRD 的**全局版本号**（一份 PRD 一个版本号、非逐片编版），冻结绑定、之后**钉住**（详见 §4）。非 PRD / 对话驱动迭代**不写此行**、frontmatter 逐字不变。

## 3. 标准模板

```md
---
状态: draft        # draft=写完待 ACK；用户 ACK 后改 ack-frozen
ACK 日期: —        # 置 ack-frozen 时填写
prd_version: —     # 可选；引用 references/prd/ 切片时填（如 v1.1），冻结绑定、之后钉住，见 §4；非 PRD 迭代省略此行
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
- .ai/references/prd/save-validation.md — PRD 切片来源（版本＝frontmatter prd_version，正文不重复版本号）；支撑 AC2

# Open Questions / Risks
- 当前未决问题
- 当前剩余风险
```

## 4. 冻结状态字段（`状态` / `ACK 日期`）

- 语义：`draft` = AC 已写完、等待用户 ACK；`ack-frozen` = 用户（或 `/dangerous` 自审门）已 ACK、本迭代验收范围冻结。
- 流程：AC_LIST 写完先置 `draft`；用户 ACK 后改为 `ack-frozen` 并填 `ACK 日期`，方可进入 P3。
- hook 联动：在部署了 butler hook 的项目，AC_LIST 处于 `draft` 时源码写操作会被 `phase_gate` 拦截，直到置 `ack-frozen`。无该字段的旧 AC_LIST 按 legacy 放行，不被误杀。
- amend 退回：迭代内小幅修订（`iteration-schema.md §5.3`）必须把 `状态` 退回 `draft`、重新等待 ACK 后再置 `ack-frozen`。
- `prd_version` 绑定（仅引用 `references/prd/` 切片的迭代适用）：置 `ack-frozen` 时把 `prd_version` **绑定到当刻 PRD 的全局版本号**（如 `v1.1`），之后**钉住**——即锁死不随 PRD 后续改版漂移；本迭代 P3 设计、P5 核对全对着这一版（引用锚点与解析见 §5）。amend 重冻（上一条退回 `draft` 重新 ACK）时，若 PRD 期间已改版，`prd_version` **可随重冻重绑到新的当前版**。改版的完整同步协议（重新派生 + 影响面 + 主动重冻）属 `/prd update`，不在本字段展开。
- 简化路径：`状态` 字段可选；省略即按 legacy 放行。简化路径的一行分流记录写在 AC_LIST 顶部（格式见 §3）。

## 5. 编写规则

- 每条 AC 必须可验证，禁止模糊表述。
- 每条 AC 应尽量绑定一个明确验证动作。
- AC 应覆盖功能完成、结构正确、质量达标三类要求。
- AC 不得混入未来愿景、长期规划或下一阶段任务。
- 超出范围但相关的事项，应放进 `Out of Scope` 或 `Open Questions / Risks`。
- 若存在已处理的外部参考资料（`.ai/references/`），必须在 `External References` 中列出，并标注哪些 AC 项源自该参考资料。
- 引用 `references/prd/` 切片时，**版本化锚点 = slug + frontmatter 的全局 `prd_version`**：版本号只存 frontmatter 一处，`External References` 与各 AC 正文引用 `prd/<slug>.md` **不逐条重复版本号**（解析时用 frontmatter 补齐）。解析规则——PRD 仍在该版则 live `prd/<slug>.md` 即钉住版；PRD 已改版超过则读 `.archive/v<prd_version>/<slug>.md`（读侧「执行读最新」纪律见 `40_Context_Management/references-schema.md §5 步骤 2`、`.archive/vN/` 落盘契约见其 §7，此处不复述）。须标注哪些 AC 源自哪个 slug。
- 字段正文必须讲人话、不啰嗦，口径以 `artifact-style.md` 为准（单一来源，不在此重复）。

## 6. 判定口径

一个任务可视为完成，至少应满足：

- 目标已被覆盖。
- 所有 In Scope 项已有明确落点。
- Acceptance Checklist 已全部可勾选。
- 每个 AC 都有对应验证结果。
- 剩余风险已显式说明。

## 7. 与执行流程的关系

- P2 阶段必须产出 `.ai/AC_LIST.md`，作为后续所有阶段的共同依据。
- P2 的用户 ACK 物化为 `状态: ack-frozen`，是进入 P3 的硬门（详见 `lifecycle.md` P2 与 `iteration-schema.md §5.2`）；未冻结时部署了 hook 的项目会拦截源码写操作。
- P2 从 `.ai/CONCEPT.md` 读取输入（简化路径下，Goal 与 Constraints 直接写入 `AC_LIST.md`）。
- 若任务先经过 `/ideation`，只有已确认的决策才能被折叠进 Goal / In Scope / Acceptance Checklist / Verification Method。
- P3 阶段的技术方案必须逐项映射 AC。
- P4 阶段的实现不得脱离 AC 扩张范围。
- P5 阶段必须按 AC 回填验证结果。
