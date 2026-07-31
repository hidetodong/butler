<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0107

> ⚠️ 危险模式：本产物由模型自主 ACK（已过设计自审门），未经用户确认（ITER-0107，2026-07-31）。

方案状态: pass

方案审查日期: 2026-07-31
方案审查方式: dangerous-self-review

## Design Decisions

**Goal**：支撑 AC1–AC7，用一份独立领域地图和两处入口接线完成 R1；只定义概念边界、所有权和真源指针，不改变 Butler 的运行语义。

**Files / Modules to Change**

| 文件 | 改动性质 | 服务 AC |
|---|---|---|
| `Coder/domain-model.md` | 新增领域地图、20 项统一语言审计、两个冲突反证和演进纪律 | AC1–AC4、AC7 |
| `Coder/README.md` | 在入口、目录结构、职责说明和读取导航中注册领域地图 | AC5 |
| `Coder/architecture-overview.md` | 明确规则分层与领域上下文是两个正交维度，并互链领域地图 | AC1、AC5 |
| `.ai/references/domain-driven-design-fowler.md` | 保存外部概念参考的消化摘要和来源指针 | AC7 |

迭代状态产物、RUN_LOG、交付和归档按生命周期更新，不计入规则功能面。R1 不修改 `dangerous-engine.md`、`convergence-loop-engine.md`、artifact manifest、workflow registry、hook、工具或公开命令。

**Domain Map Contract**

- `Coder/domain-model.md` 使用现有规则正文要求的 `title`、`audience`、`scope` frontmatter。
- 上半部分为上下文地图。每个上下文必须给出目的、拥有概念、不负责内容、主要真源和上下文关系；五个候选上下文可以基于审计改名，但不为迎合目录结构强行一一对应。
- 下半部分为恰好 20 行的统一语言审计。固定列为“概念、上下文限定、白话定义、所有者、定义真源、允许别名、明确不代表、冲突状态”。每行只有一个语义所有者；跨命名空间同名词拆成限定概念。
- 定义真源使用仓库相对路径，必要时带章节文字；地图只摘一句语义和指针，不复制封闭枚举、完整字段表或执行算法。
- 冲突反证单列 dangerous/loop 和人测残余 schema/manifest，记录所有者、证据、影响和后续路线；本轮状态保持 `open → R3`，不修改冲突真源。

**Context Decisions**

- 保留五个上下文，但将名称收敛为“需求与范围、交付生命周期、可信保证、宿主运行时、知识连续性”。现有证据表明它们拥有不同的状态与真源，暂不需要合并。
- `AC`、Goal、Evidence、Review 和完成资格归可信保证；生命周期消费这些结果，但不拥有其证明语义。
- Milestone、Route Item、Iteration、Phase 和阶段产物归交付生命周期；知识连续性只拥有其持久化入口、摘要和恢复投影，不重新定义生命周期状态。
- PRD、外部参考和 Workspace Scope 归需求与范围；宿主运行时只执行项目根、权限和 scope 门禁，不反向改需求语义。
- dangerous 与 loop 都归宿主运行时的扩展模式，但二者是并列能力；当前规则中的自动包含关系记为冲突证据，不在 R1 修正。

**Plan Admission**

- **AC Coverage**：AC1 由上下文地图覆盖；AC2 由 20 行语言审计覆盖；AC3 由真源路径检查和禁止复制规则覆盖；AC4 由双冲突反证覆盖；AC5 由 README/architecture 两处接线覆盖；AC6 由允许文件集、结构检查和完整 CI 覆盖；AC7 由 reference 指针和禁止战术模式强制化覆盖。
- **Assumptions**：① 现有规则文件仍是各概念定义真源；② R1 可以新增人读导航文件但不能夺取机器合同所有权；③ 当前两个已知冲突足以验证地图的定位能力，不要求本轮修复。
- **Alternatives / Trade-offs**：把全部内容塞进 `architecture-overview.md` 会混淆规则分层与领域边界，否决；现在新增 JSON 术语 registry 能机械约束，但会提前进入 R3 并增加迁移成本，否决；按上下文重排 `Coder/` 目录影响过大且没有收益证据，否决。
- **Failure Modes**：见下节。
- **Impact / Scope Challenge**：三份规则文档足以闭合 R1；任何状态、工具或行为代码改动都是范围扩张，必须停止并留给后续迭代。
- **Verification Blind Spots**：机器检查能验证表格、数量、路径和禁用词，不能证明领域边界一定最优；因此 AC1、AC4 还需完整语义审查，用真实冲突从地图反向定位。
- **Verdict**：`pass` — AC 全覆盖，影响面收敛，没有未决外部条件或已知 Must Fix；允许进入 P4。

**Execution Steps**

- [x] T1 新增领域地图，写清五个上下文及其关系 → AC1
- [x] T2 完成恰好 20 项统一语言审计与真源指针 → AC2、AC3
- [x] T3 写入 dangerous/loop、人测 schema/manifest 双冲突反证和后续路线 → AC4
- [x] T4 在 Coder README 和规则架构总览注册并说明正交分工 → AC5
- [x] T5 运行结构、路径、禁止复制、允许文件集、链接、diff 与完整 CI 检查 → AC1–AC7

## Failure Paths

- **地图成为第二真源**：如果表格开始复制状态枚举、完整字段或算法步骤，后续会与机器合同漂移。处理方式是删掉复制内容，只保留白话语义、所有权和真源指针。
- **上下文按目录硬切**：`20/30/40` 是规则分层，不是领域上下文；若地图只是换名复述目录树，AC1 失败。必须按概念所有权和真实状态边界校正。
- **同名词被强行统一**：`active`、`pass` 等词在不同命名空间有不同含义。必须使用限定概念，不能用一个总定义覆盖差异。
- **审计顺手修行为**：发现 dangerous/loop 或人测冲突后若直接改规则算法，会突破 R1 冻结范围。只登记证据与 R3 路线。
- **真源路径陈旧**：文档移动后指针会失效。P5 逐路径检查并接入 Markdown 链接；未来变更由领域模型评审纪律维护。
- **DDD 过度设计**：若产物引入战术对象模式、微服务或通用 DSL，删除对应内容；本轮只采用统一语言和限界上下文等战略概念。

## Test Strategy

- **结构合同**：用标准库脚本解析 `Coder/domain-model.md`，断言 frontmatter、五个上下文字段、语言审计表固定列、恰好 20 行和两个冲突条目齐全。
- **真源路径**：从审计表提取反引号包围的首个仓库相对路径，逐项确认存在；人工抽查白话定义与对应真源语义一致。
- **防双写与禁用边界**：断言领域地图没有复制状态枚举表、artifact 字段表或算法步骤；Entity、Value Object、Aggregate、微服务只能出现在“不采用”语境，不能成为强制实现。
- **范围对账**：P4 规则改动只允许 `Coder/domain-model.md`、`Coder/README.md`、`Coder/architecture-overview.md`；状态、参考、证据、交付文件按生命周期另计。检查两个冲突真源没有被 R1 修改。
- **导航与链接**：运行 `python3 scripts/check-markdown-links.py --root .` 和 `git diff --check`。
- **完整回归**：通过 verification-evidence 捕获 `bash scripts/verify-ci.sh`；P5 再运行 artifact contract、state audit 和 Goal 裁决。
- 本迭代不声明 TDD cycle，`TDD Pair Status` 写 N/A。

## References Compliance

- `.ai/references/domain-driven-design-fowler.md` 只支撑统一语言、限界上下文、战略设计和演化式模型；不复制来源大段正文，不把 DDD 战术模式提升为 Butler 约束。
