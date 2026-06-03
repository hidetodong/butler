---
title: 验收导向生命周期
audience: AI / 开发者
scope: 阶段状态机、强制产物链、升级信号与回退规则
---

# Workflow Lifecycle

## 1. 目标

所有任务默认走**验收导向流程**，而不是直接进入编码。

核心原则：

- 先对齐问题理解。
- 再对齐完成定义。
- 再确认技术方案。
- 最后进入实现与验证。

## 2. 升级信号与简化路径

收到任务后，AI 必须先跑一遍升级信号清单。**命中任一条 → 完整流程；零命中 → 简化路径。**

### 升级信号（命中任一条即触发完整流程）

| 信号 | 判断依据 |
|---|---|
| 需求有歧义 | 存在开放性问题，实现方式不唯一 |
| 多文件改动 | 预计修改 ≥ 3 个文件 |
| 契约变更 | 涉及接口、Props、API、数据结构或状态边界的新增/修改 |
| 关键路径 | 涉及认证、权限、支付、数据迁移等不可逆或高敏感逻辑 |
| 跨模块影响 | 改动会影响其他模块的输入、输出或行为 |
| 设计取舍 | 需要在多个可行方案中做选择 |

### 简化路径（零信号命中）

合并 P1 + P2，只产出一份 `AC_LIST.md`（含 Goal 与 Constraints）。P3 可口头确认，不强制 `TECH_PLAN.md`。P5 简要验证，不强制 `VERIFY_REPORT.md`。

但即使走简化路径，也不能跳过：

- 目标理解
- 完成定义
- 验证方式

## 3. 状态机（完整流程）

`P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify`

### P1 Analysis

**必须产物**：`.ai/CONCEPT.md`。必填字段参考 `concept-schema.md`。

AI 必须回答：

- 我对目标、约束、影响范围的理解是否完整？
- 目前有哪些显性约束和隐性约束？
- 是否存在需要先澄清的问题？
- 当前项目属于哪类工程形态，是否需要启用特定 domain / stack profile？

P1 讨论可能跨多轮对话。讨论结束后，AI 必须将结论结晶为 `.ai/CONCEPT.md` 并呈交用户确认，而非依赖对话记忆衔接下一阶段。

进入 P1 即开启一个迭代：从 `.ai/ITERATIONS.md` 领下一个迭代号 `ITER-NNNN` 并置 `active`，本迭代的 `CONCEPT.md` / `AC_LIST.md` 产在工作区四件套中。迭代号分配、台账字段与锁定纪律以 `iteration-schema.md` 为准。极小、零升级信号的简化路径任务可不单独开迭代号。

若任务属于新项目接入、显式要求部署基地车，或需要建立跨会话维护设施，应在 P1 同步参考 `mcv-deployment.md` 完成侦察与部署判断。
若任务涉及已有 `.ai/` 维护文件的升级、迁移或归档整理，应在 P1 同步参考 `mcv-update.md` 完成升级判断。
若识别到明确技术栈或工程形态，应在 P1 记录本任务命中的 `10_Domain_Stack_Profiles/` profile，未命中时仅按通用 SOP 推进。

### P2 Acceptance

**必须产物**：`.ai/AC_LIST.md`。必填字段参考 `acceptance-schema.md`。

**输入来源**：从 `.ai/CONCEPT.md` 读取，不从对话记忆推断。

若用户在 P2 阶段提供了外部参考资料（API 文档、设计稿等），AI 应按 `logic-protocol.md` 的参考资料注入规则处理并存入 `.ai/references/`，然后将参考资料中的约束纳入 AC 定义。例如：API 文档中的接口契约影响 In Scope 和 Verification Method；设计稿中的交互规格影响功能验收项。

AI 必须回答：

- 如果以下条目全部勾选，任务是否可视为完成？
- 每条验收项要如何验证？
- 哪些验收项来自通用 SOP，哪些来自已激活的 profile？
- 哪些验收项来自外部参考资料？（若有）

强制规则：

- **必须等待用户 ACK，才能进入 P3。**
- `AC_LIST.md` 被 ACK 即视为本迭代需求**冻结**：进入 P3/P4 后默认不再扩张范围。冻结后的修订与扩张分流规则参考 `iteration-schema.md` §5 与本文件 §5 回退规则。
- 长任务或多子任务场景下，P2 结束后应形成一次阶段结晶，具体触发规范参考 `40_Context_Management/context-persistence.md`。
- profile 相关验收项只在当前项目类型命中时纳入 AC，不得把无关领域规则前置成默认完成标准。

### P3 Design

**必须产物**：`.ai/TECH_PLAN.md`。必填字段参考 `tech-plan-schema.md`。

**输入来源**：从 `.ai/AC_LIST.md` 读取，逐项映射验收项。若 `.ai/references/` 下存在已处理的参考资料（API 文档、设计稿等），P3 必须同时读取，将其中的接口契约、数据结构、UI 规格等约束纳入技术方案。

AI 必须回答：

- 我打算改哪些模块或文件？
- 接口契约、状态边界、扩展点分别是什么？
- 我会如何验证这些改动？
- 当前方案受哪些已激活 profile 约束？

强制规则：

- **必须等待用户 ACK，才能进入 P4。**
- 若任务链路较长，应在 P3 结束时明确子任务拆分、handoff 方式与状态同步策略，具体接力规则参考 `progressive-handoff.md` 与 `40_Context_Management/context-persistence.md`。
- 若未命中任何 profile，则仅按通用 SOP 与质量门禁设计方案。

### P4 Execute

交付物：代码、配置或文档实现。直接落在目标代码、配置或文档文件中，实现结果必须可映射回 `.ai/AC_LIST.md` 与 `.ai/TECH_PLAN.md`。

**输入来源**：从 `.ai/TECH_PLAN.md` 读取执行计划与边界约束。

**标准执行**：根据方案编码，执行单次 Probe 验证。若报错，将原始错误反馈给用户。

**Loop 增强**：仅在用户显式激活 `55_Extension_RalphLoop/ralph-loop-engine.md` 时，进入"执行-探测-反思-修正"的闭环，直到验证全绿或触发熔断。

执行阶段必须保证：

- 当前已实现哪些 AC、尚未实现哪些 AC，应可识别。
- 改动落点必须与 `.ai/TECH_PLAN.md` 中约定的文件范围、接口契约与状态边界一致。
- 探测动作必须能回溯到具体 AC。
- 若出现新增接口、状态边界变化或影响面扩大，应回到 P3 更新方案。

执行原则：

- 实现必须能映射回已确认的验收项。
- 不得在执行阶段偷偷扩张范围。
- 不得跳过探测直接交付未经验证的实现。
- 若影响面变化，应回到 P3。
- 若本阶段涉及 `.ai/` 维护文件写入，应遵守 `maintenance-boundaries.md` 中定义的触发阈值与批处理策略。
- 领域执行细则只来自已在 P1 / P3 明确激活的 profile，不默认套用前端或特定技术栈规则。
- 若缺少明确探测命令或环境能力不足，应先向用户确认验证方式。
- 若任务命中 `40_Context_Management/context-persistence.md` 中定义的激活条件（新项目接入、跨会话继续、多阶段推进、需要等待 ACK 或外部结果、无法单轮闭合等），执行过程中**必须**按其"运行时增量"规则同步 `.ai/task-state.md`，不得仅依赖对话记忆保留阶段状态。

### P5 Verify

**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。生成 Delivery Summary 时，P5 对话回应必须同时遵守 `delivery-summary.md § 8` 的对话层风格约束，不得把文件层的编号小节结构原样复述到对话框内。

**迭代收口**：当本轮达到可交付闭环、确认收口当前迭代时，必须执行三步，缺一不可（详见 `iteration-schema.md` §5.5）：① 把工作区四件套快照复制到 `.ai/iterations/ITER-NNNN/`；② 生成 `deliveries/ITER-NNNN-<slug>.md` 交付总结；③ 在 `.ai/ITERATIONS.md` 把该迭代置 `closed`、填收口日期与交付链接、`current` 置 `none`。若本轮只是中途暂停或等待，不收口、不归档、不更新台账状态。

**输入来源**：从 `.ai/AC_LIST.md` 逐项回填验证结果。

AI 必须回答：

- 哪些验收项已满足？
- 每项是如何验证的？
- 是否还存在未关闭风险？
- 当前验证依据中，哪些来自通用质量门禁，哪些来自已激活的 profile？

P5 阶段默认触发 `60_Extension_CodeReview/review-engine.md` 简要自评（用户明确要求跳过时除外）。

长任务在 P5 结束后，应补充 checkpoint 或 handoff summary，确保验证结论可直接被下一阶段继承。
若生成 `02_SESSION_HANDOFF.md`，其内容结构应符合 `40_Context_Management/handoff-spec.md`。
若任务只是中途暂停、等待用户 ACK、等待外部结果或尚未闭环，则继续使用 checkpoint / handoff，不生成 Delivery Summary。

## 4. 强制产物链

阶段产物是**决策记录**，不是临时文档。它们在 `.ai/` 下持续存在，供复盘、审计与跨阶段引用。

```
P1 → .ai/CONCEPT.md → P2 从此读入
P2 → .ai/AC_LIST.md → P3 从此读入
P3 → .ai/TECH_PLAN.md → P4 从此读入
P5 → .ai/VERIFY_REPORT.md → 最终验证记录
```

每个阶段**必须从上一阶段的产物文件读取**，不得仅凭对话记忆衔接。

工作区四件套（`.ai/CONCEPT.md` 等固定路径）始终对应**当前活跃迭代**。迭代收口时，这四件套会被快照复制到 `.ai/iterations/ITER-NNNN/` 冻结归档，工作区原位保留供下一迭代覆写。迭代号、台账与归档机制以 `iteration-schema.md` 为准。

产物文件与运行态文件（`02_SESSION_HANDOFF.md`、`task-state.md`、`CHANGELOG.md`、`ITERATIONS.md` 等）职责不同：

- **产物文件**：决策记录，随任务存续，可复盘、可审计。
- **运行态文件**：操作状态，随会话更新，任务结束后可归档。

## 5. 强制回退规则

出现以下情况时，必须回退流程：

- 目标理解变化：回到 P1，更新 `.ai/CONCEPT.md`。
- 验收标准变化：回到 P2，更新 `.ai/AC_LIST.md`。
- 设计影响面扩大：回到 P3，更新 `.ai/TECH_PLAN.md`。
- 新业务扩展文档出现：重新执行 Context Discovery，并至少回看 P1 / P2。

回退发生在已冻结迭代内时，按"允许修订、扩张才开新迭代"分流（详见 `iteration-schema.md` §5）：

- **小幅修订**（未突破原影响面）：在当前迭代号内更新 `AC_LIST.md`、重新等待 ACK，并在其顶部"修订记录"追加一行。
- **影响面扩大**（命中上表的跨模块、契约级、关键路径变化）：先收口或废弃当前迭代，再开下一个迭代号承接，**不得**把扩张内容塞进已冻结迭代。拿不准时按扩张处理。

## 6. 研发与扩展原则

- 一次改动只解决一个明确问题。
- 先分边界，再写代码。
- 先定契约，再做扩展。
- 先保语义，再谈复用。
- 先本地验证，再进入交付。
- 长任务应子任务化推进，并为每个阶段保留可交接结论。
