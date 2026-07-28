# 多 active 迭代运行时：迭代级真源、Batch 与跨迭代集成审计

候办键: multi-active-iteration-runtime
候办状态: deferred

## 范围评估

### In Scope（版本级）

- 在单迭代并行 P4 经真实使用证明有稳定收益后，评估并实现多个写集合可证明不相交的迭代同时处于执行态。
- 将 live 四件套、task-state 和 evidence 从根级全局单例演进为迭代级真源；根级文件仅在兼容期作为当前观察焦点的派生投影。
- 把单个 `current` 演进为可审计的 active 集合与 integration focus，同时保持迭代号、归档、交付和 Goal 身份唯一。
- 引入 Batch、迭代依赖图、写集合求交、共享契约前驱、P4 前分区审计和合并前跨迭代审计。
- 改造 artifact pipeline、phase gate、handoff、state ledger、Goal/evidence、progress、归档与收口审计，使所有消费者显式按迭代身份读取。
- 对共享契约、数据库迁移、生成文件和版本级组合行为执行跨迭代一致性验证；证明不了可串行化时退回单迭代串行路径。

### Out of Scope（版本级）

- 不在单迭代并行 P4 尚未稳定、缺少真实吞吐收益数据时启动本方向。
- 不允许仅因目录不重叠就判定迭代可并行；行为契约、读后写依赖和运行资源冲突同样参与准入。
- 不让每个迭代自行写共享台账、里程碑或集成焦点；共享状态仍由 Coordinator 单写。
- 不要求默认启用多 active；该能力必须显式开启，任何不确定都坍缩回已验证的串行模式。
- 不把多个 active 迭代混成一个 Goal、一个归档目录或一份交付。

### 关键交付目标

- 每个 active 迭代拥有独立、可冷启动恢复的 P1–P5 真源，任一工具都不会因根级“当前文件”读错迭代。
- 一批并行迭代的最终结果可证明等价于某个合法串行顺序；声明不相交与实际 diff 不相交均有机器证据。
- 单条迭代越界可局部退回；两条干净迭代仍无法组合时，能识别为缺共享基座或契约关系问题，而不是强行合并。
- Batch 中任一失败不会破坏其他迭代归档、共享台账和主分支，且始终可安全退回单 active 模式。
- 串行项目和旧版部署有明确迁移/兼容路径，未启用该模式时不承担多活复杂度。

## 理解阐释

多个 active 迭代不是“再多开几个 Agent”，而是对 Butler 固定路径产物链和单 current 不变量的系统性迁移。现有 `.ai/CONCEPT.md`、AC、TECH_PLAN、VERIFY、task-state、evidence 热区、handoff 和 Goal 裁决都默认只有一个活跃身份；只改台账枚举会让工具在多个迭代之间读错真源，产生比串行慢更危险的假完成。

此前预研把并行放在里程碑外壳，用 worktree 和 Batch 保护每条完整迭代；本轮 ideation 则建议先从单迭代内部并行 P4 获取较小、较安全的收益。两者不是同一个首版：只有前置方向完成并积累足够真实场景后，才有依据承担迭代级 live 产物、全工具显式寻址和跨迭代收口审计的迁移成本。

本候办因此单独保存，不混入 `parallel-p4-execution-slots`。启动信号应来自真实度量：并行 P4 仍长期被单 active 迭代阻塞、存在至少两个可独立交付的版本切片、且其写集合和共享契约能够在 P4 前冻结。若多数任务最终仍需要共享基座或组合调试，本方向继续 deferred。

设计来源为 `.ai/00_IDEATION.md` 的“多迭代并行后续形态”和 `docs/research/2026-06-16-parallel-iteration-concept.md`；正式启动前必须先做 supersede/兼容决策，消除两份预研之间的口径冲突。

## 拆分路线图

预计 4 个迭代承接；实际迭代号在启动时绑定，且整体依赖 `parallel-p4-execution-slots` 的真实 dogfood 结论。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 多活身份与迁移决策：统一既有预研，定义 Batch、active 集合、integration focus、迭代级路径和串行兼容/回退合同 | — | planned |
| R2 | 迭代级 live 产物与显式寻址：迁移四件套、task-state、evidence、artifact pipeline、phase gate、handoff 和 progress 读取层 | — | planned |
| R3 | Batch 准入与恢复：写集合/依赖图、共享基座、P4 前审计、逐 lane diff、局部退回与关系型冲突升级 | — | planned |
| R4 | Goal/收口与版本级集成：多迭代 evidence/Goal 裁决、台账/归档/交付、跨迭代组合验证、迁移 fixture 和真实仓 dogfood | — | planned |

## 范围演进记录

- 2026-07-28：从单迭代并行 P4 方向中拆出独立候办；因涉及全局产物寻址和状态机迁移，等待前置 dogfood 与真实收益信号后再决定启动。
