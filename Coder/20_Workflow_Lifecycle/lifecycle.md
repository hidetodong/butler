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

## 2. 分流：三档路径与升级信号

收到任务后，AI 必须先做一次**分流判定**：按升级信号把任务归入 极小 / 简化 / 完整 三档之一，并为非极小任务留一行可审计的分流记录。

### 2.1 升级信号（命中任一条即触发完整流程）

| 信号 | 判断依据 |
|---|---|
| 需求有歧义 | 存在开放性问题，实现方式不唯一 |
| 多文件改动 | 预计修改 ≥ 3 个文件 |
| 契约变更 | 涉及接口、Props、API、数据结构或状态边界的新增/修改 |
| 关键路径 | 涉及认证、权限、支付、数据迁移等不可逆或高敏感逻辑 |
| 跨模块影响 | 改动会影响其他模块的输入、输出或行为 |
| 设计取舍 | 需要在多个可行方案中做选择 |

### 2.2 三档边界

| 档位 | 进入条件 | 产物要求 |
|---|---|---|
| 极小 | 零升级信号，且同时满足：单文件改动、纯文案或局部改动、零契约变更、可单轮闭合 | 免强制产物，但仍须口头说明目标与验证方式；不单独领迭代号 |
| 简化 | 零升级信号，但不满足极小全部条件 | 合并 P1 + P2，只产出一份 `AC_LIST.md`（含 Goal 与 Constraints）。P3 可口头确认，不强制 `TECH_PLAN.md`；P5 简要验证，不强制 `VERIFY_REPORT.md` |
| 完整 | 命中任一升级信号 | 走完整状态机与强制产物链（`CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`） |

无论哪一档，都不能跳过：**目标理解、完成定义、验证方式**。

非极小任务同时启用 `goal-contract.md`：Goal 是既有阶段产物的派生视图，不是新的 `.ai/GOAL.md`。任务清单做完最多进入 `completion-candidate`；AC、evidence、review 与收口事实未闭合前不得标成 `complete`。

### 2.3 分流记录（一行，可审计）

非极小任务必须在产物顶部留一行分流记录，格式：

`分流: <简化|完整> | 命中升级信号: <列出命中项 / 均未命中> | <日期>`

落点：

- 完整路径 → 写进 `CONCEPT.md` 顶部。
- 简化路径 → 写进 `AC_LIST.md` 顶部。
- 极小路径 → 免产物，分流判定在对话中口头说明即可，不强制落盘。

### 2.4 升级转换（低档 → 高档）

分流是初始判定，不是终身判定。若简化或极小路径在执行中命中任一升级信号（典型：发现要改 ≥3 文件、出现契约变更、影响面跨模块），必须就地升级到对应高档，**不得在原档硬撑**：

1. 补齐目标档位缺失的强制产物（极小 → 简化补 `AC_LIST.md`；→ 完整再补 `CONCEPT.md` / `TECH_PLAN.md`）。
2. 若原本未领迭代号，按 `iteration-schema.md §5.1` 补领并开启迭代。
3. 把已完成的工作折叠进新产物（已写的代码映射回新 `AC_LIST.md`），再继续按高档流程推进。

升级转换与 §5 回退规则正交：回退是"同档内退回某阶段重新对齐"，升级是"换更高档位、补更强产物"。

## 3. 状态机（完整流程）

`P1 Analysis -> P2 Acceptance -> P3 Design -> P4 Execute -> P5 Verify`

### P1 Analysis

**必须产物**：`.ai/CONCEPT.md`。必填字段参考 `concept-schema.md`。

AI 必须回答：

- 我对目标、约束、影响范围的理解是否完整？
- 目前有哪些显性约束和隐性约束？
- 需求里有没有伪需求、投入产出比过低或不合逻辑的部分？该剥离、缩到 MVP（最小可用版本），还是提替代方案？
- 是否存在需要先澄清的问题？
- 当前项目属于哪类工程形态，是否需要启用特定 domain / stack profile？

> **质询时机**：主动质疑需求（上面第 3 问）发生在 **P1**——此刻需求尚未冻结，该问就问、该提替代就提。这与 `iteration-schema.md §5`「固定需求锁定」不冲突：锁定在 **P2 用户 ACK 冻结之后**才生效，冻结后不再擅自推翻。P1 质询 → P2 冻结 → 之后守住，是三个先后动作，不是互相矛盾。

P1 讨论可能跨多轮对话。讨论结束后，AI 必须将结论结晶为 `.ai/CONCEPT.md` 并呈交用户确认，而非依赖对话记忆衔接下一阶段。

进入 P1 即开启一个迭代：从 `.ai/ITERATIONS.md` 领下一个迭代号 `ITER-NNNN` 并置 `active`，本迭代的 `CONCEPT.md` / `AC_LIST.md` 产在工作区四件套中。**开启时工作区四件套必须以本迭代内容整体覆写，严禁保留或追加上一迭代内容**（overwrite-only，详见 `iteration-schema.md` §5.1）。迭代号分配、台账字段与锁定纪律以 `iteration-schema.md` 为准。极小、零升级信号的简化路径任务可不单独开迭代号。

若当前存在 `active` 里程碑（台账 `current = MILE-NNNN`），本迭代**一律自动归属**之、无需逐次确认：在 `.ai/ITERATIONS.md`「所属 milestone」列填该里程碑号，并按 `milestone-schema.md` §7.2 同步里程碑台账「含迭代」列与 `.ai/MILESTONE.md` 拆分路线图。反之，里程碑收口后（台账 `current: none`）开启的迭代**不归属**该已收口里程碑、不回写其台账，按独立迭代处理。若任务命中 `milestone-schema.md` §6.1 启动信号（跨 ≥2 迭代、版本主题、先评估后拆分、显式里程碑）而尚无 active 里程碑，应在 P1 之前先提议开里程碑并 soft 对齐；零信号则直接走独立迭代，不开里程碑。用户也可用显式命令 `/milestone`（与语义触发等价，见 `milestone-schema.md` §6.5）主动开里程碑，录入通道与 brief 合成协议见其 §6.4。

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

- **必须等待用户 ACK，才能进入 P3。** ACK 物化为 AC_LIST 顶部 `状态` 字段：写完先置 `draft`，用户 ACK 后改 `ack-frozen` 并填 `ACK 日期`，方可进入 P3。部署了 hook 的项目，AC_LIST 处于 `draft` 时源码写操作会被 `phase_gate` 拦截（字段定义见 `acceptance-schema.md §4`）。（例外：仅在 `/butler:dangerous` 危险模式下，该 ACK 由 `65_Extension_Dangerous/dangerous-engine.md` §5.1 的强制验收自审门替代，由模型自主置 `ack-frozen`，并照其 §7 留审计与回滚痕迹。）
- `AC_LIST.md` 被 ACK（即置 `ack-frozen`）即视为本迭代需求**冻结**：进入 P3/P4 后默认不再扩张范围。迭代内小幅修订须把 `状态` 退回 `draft` 重新 ACK；冻结后的修订与扩张分流规则参考 `iteration-schema.md` §5 与本文件 §5 回退规则。
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
- 方案是否已逐项挑战 AC 覆盖、关键假设、替代方案、失败路径、影响面与验证盲区？

强制规则：

- TECH_PLAN 先置 `方案状态: draft`，按 `tech-plan-schema.md # Plan Admission` 完成结构化反证并给出 verdict。只有没有已知 Must Fix 的方案才能置 `pass`；`revise` 回 P3 修订，`blocked` 诚实停机，两者均不得进入 P4。
- **必须等待用户 ACK，才能把已通过结构审查的方案置 `pass` 并进入 P4。** ACK 不能覆盖已知 Must Fix。（例外：仅在 `/butler:dangerous` 危险模式下，该 ACK 由 `65_Extension_Dangerous/dangerous-engine.md` §5.2 的强制设计自审门替代，由模型自主判定并照其 §7 留审计与回滚痕迹。）
- 方案 `pass` 后若发生实质修改，必须退回 `draft`，重新执行 Plan Admission 与对应 ACK；部署 hook 的项目会拒绝显式非 `pass` TECH_PLAN 下的源码写。
- 若任务链路较长，应在 P3 结束时明确子任务拆分、handoff 方式与状态同步策略，具体接力规则参考 `progressive-handoff.md` 与 `40_Context_Management/context-persistence.md`。
- 若未命中任何 profile，则仅按通用 SOP 与质量门禁设计方案。

### P4 Execute

交付物：代码、配置或文档实现。直接落在目标代码、配置或文档文件中，实现结果必须可映射回 `.ai/AC_LIST.md` 与 `.ai/TECH_PLAN.md`。

**输入来源**：从 `.ai/TECH_PLAN.md` 读取执行计划与边界约束。

**标准执行（常驻）**：根据方案编码并探测验证，遵循 `30_Quality_Gate/correction-contract.md`（纠错收口契约）——修到探测真过、探测绑 AC、禁止降级修复；当连续无进展 / 缺外部条件 / 需用户决策时，按"诚实停"如实交还。此契约默认每次迭代生效，无需触发。

**Loop 升档（opt-in）**：用户显式激活 `55_Extension_ConvergenceLoop/convergence-loop-engine.md` 时，在上述契约之上叠加高强度死磕——`[Loop #N]` 标注、连续闭环、定量熔断（5 轮 / 死锁 / 环境阻塞）与 RCA 报告。

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

**必须产物**：`.ai/VERIFY_REPORT.md`。必填字段参考 `verify-schema.md`；完整路径自动道还必须先由 verification evidence runner 生成机器 record，VERIFY 的 Evidence Index 逐 AC 引用，口头/手写“passed”不能替代。若本轮已经达到可交付、可验收的闭环状态，还应额外生成给人看的交付总结，结构参考 `delivery-summary.md`，**具体触发条件参考 `delivery-summary.md § 2 触发时机`**，并落在项目根目录 `deliveries/` 下。生成 Delivery Summary 时，P5 对话回应必须同时遵守 `delivery-summary.md § 8` 的对话层风格约束，不得把文件层的编号小节结构原样复述到对话框内。

**迭代收口**：当本轮达到可交付闭环、确认收口当前迭代时，必须执行以下收口步（收口原子仪式：前三步缺一不可、第四步前滚项目全貌产物[文件夹态必做 / 单文件态按需]、第五步自检；详见 `iteration-schema.md` §5.5）：① 校验证据热区并整包归档到 `.ai/iterations/ITER-NNNN/evidence/`，再把工作区四件套与 `01_CHANGELOG.md` 切片快照归档；② 生成 `deliveries/ITER-NNNN-<slug>.md` + 同名 `.html`，只引用产物/证据路径、不嵌全文或日志；③ 台账置 `closed`、填日期/交付、`current` 置 `none`，全局 changelog 收敛；④文件夹态把 delta 折进 topic 并写 fold receipt，单文件态按需前滚；⑤先跑 `audit-project-state.py` 机械检查，再跑一致性自检第 6 条语义漂移检查。若本轮只是中途暂停或等待，不收口、不归档、不更新台账状态。

**输入来源**：从 `.ai/AC_LIST.md` 逐项回填验证结果。

AI 必须回答：

- 哪些验收项已满足？
- 每项是如何验证的？
- 是否还存在未关闭风险？
- 当前验证依据中，哪些来自通用质量门禁，哪些来自已激活的 profile？

P5 阶段默认触发 `60_Extension_CodeReview/review-engine.md` 简要自评（用户明确要求跳过时除外）。在 `/butler:dangerous` 危险模式下，该简评升级为**不可跳过的完整多维审查门**，Must Fix 阻断迭代收口，详见 `65_Extension_Dangerous/dangerous-engine.md` §7.3。

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

产物文件与运行态文件（`02_SESSION_HANDOFF.md`、`PROJECT.md`、`task-state.md`、`CHANGELOG.md`、`ITERATIONS.md` 等）职责不同：

- **产物文件**：决策记录，随任务存续，可复盘、可审计。
- **运行态文件**：操作状态，随会话更新，任务结束后可归档。

## 5. 强制回退规则

出现以下情况时，必须回退流程：

- 目标理解变化：回到 P1，更新 `.ai/CONCEPT.md`。
- 验收标准变化：回到 P2，更新 `.ai/AC_LIST.md`。
- 设计影响面扩大：回到 P3，更新 `.ai/TECH_PLAN.md`。
- 新业务扩展文档出现：重新执行 Context Discovery，并至少回看 P1 / P2。

回退发生在已冻结迭代内时，按"允许修订、扩张才开新迭代"分流（详见 `iteration-schema.md` §5）：

- **小幅修订**（未突破原影响面）：在当前迭代号内更新 `AC_LIST.md`、把 `状态` 退回 `draft` 重新等待 ACK，并在其顶部"修订记录"追加一行。
- **影响面扩大**（命中上表的跨模块、契约级、关键路径变化）：先收口或废弃当前迭代，再开下一个迭代号承接，**不得**把扩张内容塞进已冻结迭代。拿不准时按扩张处理。

## 6. 研发与扩展原则

- 一次改动只解决一个明确问题。
- 先分边界，再写代码。
- 先定契约，再做扩展。
- 先保语义，再谈复用。
- 先本地验证，再进入交付。
- 长任务应子任务化推进，并为每个阶段保留可交接结论。
