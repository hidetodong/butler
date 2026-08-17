# MILE-0015 · Butler 领域模型治理：统一语言、限界上下文与可执行边界

- 交付级别：里程碑交付（大版本）
- 收口日期：2026-08-17
- 含迭代：ITER-0107、ITER-0108、ITER-0109、ITER-0110、ITER-0111

## 本次交付目标

Butler 的流程、产物、状态和验证机制早就成熟了，但核心概念散落在规则正文、schema、manifest、registry、hook 和工具实现里。真正的风险不再是“缺一条规则”，而是同一个词在不同模块含义不同、派生视图被当成权威状态、两个本来独立的能力被某段规则错写成包含关系。

这一版吸收 DDD 的战略设计——统一语言解决“大家说的是不是同一件事”，限界上下文允许同一个东西在不同问题范围有不同模型，上下文映射规定这些模型怎么交换信息——只做一件事：把已有概念的所有权和边界讲清，再用真实冲突验证它能约束实现。不为采用 DDD 重构全仓，不引入面向对象框架，不建包罗万象的企业术语库。

## 已完成内容

- **划定边界**（R1）：五个限界上下文——需求与范围、交付生命周期、可信保证、宿主运行时、知识连续性；20 个高风险概念逐项标明上下文限定、白话定义、唯一所有者、定义真源、允许别名和非职责。
- **分层加载**（R2）：完整审计不常驻。冷启动只读 L0 路由，跨上下文任务再读 L1 地图，术语有歧义才定向查 L2 术语表，历史审计才进 L3 归档；首批最多展开 3 份真源，不够时给出可见回执再续批。
- **主链合同**（R3）：把 PRD→AC→TECH_PLAN→Evidence→Goal→Handoff 从散文暗示收敛为五段转换，每段都记源/目标上下文、输入、输出、最小保真、失效条件、责任方、权威关系和直接真源九个维度；同时定下权威事实、受控投影、派生视图、叙述摘要四类事实的单向流动。
- **机器合同与双冲突试点**（R4）：`tools/domain-contract/` 只登记“身份—上下文—种类—唯一所有者—真源”加关系与断言，fail-closed 抓重复、悬空、越界和复制型载荷。两个真实冲突同时闭环——Dangerous Mode 与 Convergence Loop 解除错误包含改为并列，VERIFY「人测道小结」的结构所有权统一归 artifact manifest。
- **治理接线与自测**（R5）：评审新增「领域变更」维度并要求四项声明；领域合同加条目覆盖门；L0 内核在 `Coder/README.md`、`AGENTS.md`、`templates/rule-card.md` 三处字节一致并随部署入口下发；迁移配方补领域变更的升级判据。再用本迭代自身量一次真实成本。

## 关键变更 / 用户可感知变化

- **`/butler:dangerous` 不再被写成“自动复用 Loop”**：两者是并列模式，各自显式触发、互不读写激活状态，只共用有界收敛纪律。这是本版唯一改变既有运行语义的地方。
- **VERIFY 报告多一个固定的「人测道小结」段**（没有人测就填 N/A）：结构由机器清单统一，不再出现“写进去被判错、不写又违规”的死锁；旧报告可走确定性迁移补段。
- **部署项目冷启动多读约 234 token 的读取纪律**（占规则卡全文 3.8%）：撞上领域术语时按层读，不再全量吞。这是这一版加给普通项目的全部常驻代价。
- **四道机器门进了完整 CI**：身份/所有者/真源合法性、登记条目覆盖、L0 三处字节一致、分层体量预算。任一处被单独改动都会被指名。
- **下个发布版切版必须含 `[regen-entrypoints]`**：R5 改了 `templates/rule-card.md`，已部署项目不重新生成宿主入口就拿不到新的 L0，不得记 `[no-op]`。

## 高层影响范围

- **新增规则**：`Coder/domain-model.md`（L1 地图）、`Coder/domain-glossary.md`（L2 术语查询）、`Coder/context-map.md`（主链转换合同）、`Coder/30_Quality_Gate/bounded-convergence.md`（共享有界收敛）、`review-standard.md §5`（领域变更审计口径）、`migration-schema.md §5`（领域变更升级处置）。
- **新增工具**：`tools/context-budget/`（体量、结构与 L0 一致性）、`tools/domain-contract/`（最小领域合同校验）。
- **修改入口**：`Coder/README.md`、`Coder/architecture-overview.md`、`AGENTS.md`、`templates/rule-card.md`、`scripts/verify-ci.sh`。
- **顺带收拾**：Dangerous/Loop 耦合措辞涉及的 5 个规则文件、artifact manifest 与 template 的人测段所有权、`.ai/project/debt.md` 还掉两条欠债。
- **没动的**：P1→P5 阶段流程、Goal Assurance、PRD 治理、Workspace Scope、状态台账、多 Agent 执行能力，以及 MILE-0014 的 Decision Map / Work / Promotion 状态机。公开命令、文件路径和状态值零变化。

## 拆分路线图回填

| 路线 | 交付切片 | 承接迭代 | 结果 |
|---|---|---|---|
| R1 | 领域地图与语言审计：五个候选上下文用真实冲突校正，概念标明所有者、真源、别名与边界 | [ITER-0107](../ITER-0107-domain-model-boundaries.md) | closed |
| R2 | 上下文预算与渐进注入：冷启动收敛为 L0 路由，地图/术语/审计分层，建体量回归门 | [ITER-0108](../ITER-0108-progressive-context-loading.md) | closed |
| R3 | 上下文映射与主链合同：五段转换的九维合同，四类事实单向流动，与既有不变量对账 | [ITER-0109](../ITER-0109-main-chain-context-map.md) | closed |
| R4 | 最小可执行领域合同与双试点：机器合同工具，Dangerous/Loop 解耦，人测段所有权统一，补迁移与负例 | [ITER-0110](../ITER-0110-minimal-domain-contract.md) | closed |
| R5 | 治理接线与真实 dogfood：接入评审、CI、双宿主投影与升级兼容，用 Butler 自身衡量成本收益 | [ITER-0111](../ITER-0111-domain-governance-wiring.md) | closed |

## 验证方式与结果摘要

- 五个承接迭代全部 closed，各自有四件套归档、Markdown + HTML 交付、机器 evidence 记录和知识折叠回执。
- 累计 40 条 AC 全绿（R1 七条、R2 八条、R3 八条、R4 八条、R5 九条），每轮 Goal 裁决均为 `eligible`。
- 每轮收口都跑完整 `scripts/verify-ci.sh` 退出码 0，`git diff --check` 干净；分层预算、主链合同、领域合同、L0 一致性四类检查已成为常驻回归。
- 四道门在本版内各自抓到过真实问题：覆盖门一开门就抓到两条零覆盖条目（四态机器码、人测桥输入输出契约），Goal 门拒绝给只有散文的 R5 AC1/AC6 打绿、逼出三条常驻断言，L0 一致性门在投影建立当轮就验证过被单独改动会失配。这些是真实拦截，不是演习。
- 里程碑收口前跑 `audit-project-state.py`，确定性漂移清零（保留预期的 `UNRELEASED` 亮牌）。

## 已知剩余风险 / 延后事项

- **最关键的那半没拿到**：能证明文件结构一致、能证明 L0 进了部署入口，但没有任何运行时观测能说明某个宿主在真实会话里确实照分层读了、有没有因此少走弯路。“衡量歧义减少”最实的一半留给 `butler-slim-down` 候办的 usage instrumentation。
- **成本收益判断是“继续，但不再扩建”**：领域治理本体到此为止，不再新增上下文、术语或合同种类。若将来使用数据显示这四道门长期零命中，本里程碑的产物应当被裁掉，而不是继续加固。
- **体量指标是稳定代理，不是精确 token**：bytes、非空行和指针数在不同模型 tokenizer 下都不等于真实 token 数。
- **机器只能查声明在不在，查不出想没想对**：四项声明里“兼容影响”和“迁移路径”写得对不对、有没有漏掉依赖方，仍靠执行者自觉；覆盖门也只是文件级粒度，条目蹭到同文件的无关断言会被误判为已覆盖。
- **五个上下文不是冻结答案**：它们是当前证据下的稳定切法，后续真实冲突可能要求改名、合并或拆分。
- **全程 `independent_review=false`**：五个迭代都用同上下文复核加机器证据收口，没有执行 fresh-context 独立复核，也没有冒称执行过。
- **不吞并 `state-transition-trust-gate` 候办**：运行时事实与落档投影是否一致，仍由那个候办负责。

## 引用（只链接，不嵌入）

- `.ai/milestones/MILE-0015/MILESTONE.md`
- `deliveries/ITER-0107-domain-model-boundaries.md`
- `deliveries/ITER-0108-progressive-context-loading.md`
- `deliveries/ITER-0109-main-chain-context-map.md`
- `deliveries/ITER-0110-minimal-domain-contract.md`
- `deliveries/ITER-0111-domain-governance-wiring.md`
