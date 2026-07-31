---
状态: ack-frozen
ACK 日期: 2026-07-31
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0099

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0099，2026-07-31）。

## Goal

- 建立一份能指导后续设计的 Butler 领域地图和语言审计结果，让核心概念的所属上下文、定义真源、非职责与已知冲突可查、可验证，并且不制造第二份执行真源。

## In Scope

- 验证需求治理、交付生命周期、可信保证、宿主运行时、知识连续性五个候选上下文，允许基于证据合并、拆分或改名。
- 审计约 15–20 个跨边界、高风险或需要机器判断的核心概念；明确上下文限定、所有者、定义真源、允许别名、非职责和冲突状态。
- 新增领域地图的人读真源并注册入口；地图只保存边界、关系和指针，字段枚举与执行算法继续留在既有 schema、manifest、registry 和规则真源。
- 用现有真实语义冲突反向验证地图，并把实质修复明确路由到 R2、R3 或独立候办。
- 只修正不改变行为的导航与同义措辞；运行行为、状态转换、公开命令和机器合同保持不变。

## Out of Scope

- 不在 R1 解除 dangerous 与 loop 的错误绑定，不修人测残余的 schema/manifest 冲突。
- 不实现跨上下文转换合同、机器术语 registry、状态门禁或迁移逻辑。
- 不重排 `Coder/` 目录，不引入 DDD 框架、面向对象模式、微服务、知识图谱或通用 DSL。
- 不登记只在单一文件局部使用、没有歧义也不参与机器判断的普通名词。
- 不吞并 `state-transition-trust-gate` 等能够独立启动的候办方向。

## Acceptance Checklist

- [ ] AC1: 领域地图给出经证据校正后的上下文集合；每个上下文都有目的、拥有的概念、明确不负责的内容、主要真源和与其他上下文的关系，且说明它与 SOP Core / Domain Profiles / Business Extension 规则分层不是同一维度。
- [ ] AC2: 统一语言审计覆盖 15–20 个高风险概念；每项包含上下文限定、白话定义、唯一所有者、定义真源、允许别名、非职责和冲突状态。像 `active`、`pass` 这类跨命名空间词必须拆成上下文限定项，不能用一个模糊总定义抹平差异。
- [ ] AC3: 审计表中每个定义真源路径真实存在并与原文语义一致；领域地图不复制状态枚举、字段表或执行算法，不与 schema、manifest、registry、工具 README 建立双写真源。
- [ ] AC4: 至少用 dangerous/loop 错误绑定和人测残余 schema/manifest 冲突两个现存问题做反向验证；每个问题都能从领域地图定位概念所有者、冲突证据、影响边界和后续路线，不在 R1 偷做实质修复。
- [ ] AC5: 领域地图采用有 `audience`、`scope` frontmatter 的独立文档，并在 `Coder/README.md` 的入口、目录结构或读取导航中注册；`architecture-overview.md` 继续负责规则分层，两份文档的分工和互链清楚，不引入隐式依赖。
- [ ] AC6: 实际改动仅限领域地图、必要导航/无行为措辞、外部参考指针与本迭代状态产物；P1→P5、Goal Assurance、PRD、Workspace Scope、hook、工具、公开命令和状态值行为零变化，仓库完整 CI 保持通过。
- [ ] AC7: Fowler 文章只作为 DDD 战略设计的概念来源并通过 `.ai/references/domain-driven-design-fowler.md` 引用；产物不把面向对象战术模式或微服务当成 Butler 必须采用的实现，也不复制来源的大段原文。

## Verification Method

- AC1: 对领域地图逐个上下文检查目的、拥有、排除、真源和关系字段；与 `Coder/README.md`、`Coder/architecture-overview.md` 和现有模块职责交叉核对，记录任何合并、拆分或改名依据。
- AC2: 用确定性检查提取审计表，验证条目数为 15–20、必填列非空、所有者唯一；人工复核跨命名空间词已拆分限定，没有用同名掩盖不同状态语义。
- AC3: 对审计表中的仓库相对路径逐项做存在性检查，并抽查定义与目标真源原文一致；扫描领域地图不得复制封闭枚举表、完整 schema 字段或算法步骤。
- AC4: 分别从两个已知冲突出发，仅依赖领域地图和其指针定位所有者、证据、影响与后续路线；核对 dangerous/loop 仍路由 R3，人测冲突仍路由 R3，R1 diff 不含对应行为修复。
- AC5: 检查新文档 frontmatter；核对 `Coder/README.md` 已注册文件和读法，`architecture-overview.md` 与领域地图双向说明分工；运行仓库 Markdown 链接检查。
- AC6: 用 `git diff --name-only` 和内容审查对账实际影响面；运行 `git diff --check`、artifact contract check 和 `bash scripts/verify-ci.sh`，确认没有行为代码、机器合同或公开接口变化。
- AC7: 核对 External References 与参考资料文件；扫描领域地图没有把 Entity、Value Object、Aggregate、微服务列为强制设计，也没有大段复刻来源正文。

## External References

- `.ai/references/domain-driven-design-fowler.md` — Martin Fowler 对统一语言、限界上下文、战略设计和演化式领域模型的概述；支撑 AC1、AC2、AC4、AC7。

## Open Questions / Risks

- 推荐将长期领域地图落在 `Coder/domain-model.md`；最终文件结构和表格合同在 P3 决定，但不得把字段真源复制进地图。
- “15–20 个概念”是防止 R1 退化为全仓词典整理的硬上限；若发现更多问题，只登记后续候选，不在本轮扩张。
- 自动检查只能证明表格完整、路径存在和禁用模式未出现，不能独自证明上下文划分正确；AC1、AC4 仍需要基于真实冲突的语义审查。
- 本轮不声明 TDD cycle；产物是规则文档和审计结果，使用结构检查、负向断言、完整 CI 与 P5 审查验证。
