# 单迭代多 Agent 并行 P4：执行槽、证据与集成隔离

候办键: parallel-p4-execution-slots
候办状态: deferred
规模: milestone

## 范围评估

### In Scope（版本级）

- 保持单个 `active` 迭代和 P1→P3 串行决策不变，把已经准入的 P4 实现拆成多个边界明确、可独立验证的执行槽并行推进。
- 为执行槽建立机器可解析的身份、AC 映射、唯一写路径、只读范围、接口契约、依赖、合并顺序、失败返回条件和槽级验证要求。
- 定义不可变 dispatch snapshot：所有 worker 从同一基线读取冻结 AC、通过准入的方案与槽合同；worker 的 `.ai/` 副本不得参与合并。
- 明确权限真实边界：宿主权限、需求 Workspace Scope、TECH_PLAN Write Plan 与槽 Owned Paths 取交集；现有 hook 无法识别 Agent 身份、shell 不受写前门禁时，必须以契约约束和最终 diff 审计诚实兜底，不冒称硬隔离。
- 建立 worker 固定回执、先审后合并的临时集成分支、冲突/漂移回流和失败后可丢弃的集成恢复机制。
- 在 evidence v1 尚未绑定 slot/commit/baseline 的 MVP 中，worker 验证只作执行反馈；关闭 AC 的机器证据由 Coordinator 在集成提交上统一重跑生成。
- 接入 artifact pipeline、Workspace Scope、hook/diff 对账、Goal/P5 和多宿主适配，并用真实并行任务 dogfood。

### Out of Scope（版本级）

- 不解除“同一时刻最多一个 active 迭代”的约束，不迁移根级四件套真源。
- 不让子 Agent 修改 CONCEPT、AC、TECH_PLAN、VERIFY、task-state 或 ITER/MILE 台账，也不允许其宣布 Goal/迭代完成。
- 不允许 worker 直接合并主分支，不把槽级测试结果直接当作迭代 P5 证据。
- 不承诺 shell 写入能被现有 PreToolUse hook 完全阻断；未有宿主级能力前不得把事后审计包装成强权限。
- 不为理论完整性预建通用调度平台、分布式队列或跨机器执行系统。

### 关键交付目标

- 对任一并行槽，都能机械回答：由谁执行、从哪个基线开始、允许改什么、实际改了什么、服务哪些 AC、返回了什么结果。
- 并行失败只能污染当前槽或一次性集成分支，不污染其他槽、权威 `.ai/` 状态或主分支。
- 即使文件路径不重叠，行为契约冲突也会在准入或集成门被识别；无法证明可并行时自动坍缩回串行。
- 最终 P5、Goal 裁决和独立复核仍只面对一个完成集成的迭代状态，现有收口可信度不降低。
- 未启用并行执行时，现有 TECH_PLAN、hook、evidence 和串行 P4 行为零变化。

## 理解阐释

当前 Butler 已允许 TECH_PLAN 的 Execution Steps 标注可并行，但没有把“可并行”提升为可派发、可约束、可归因和可集成的机器合同。主 Agent 可以临时分工，却无法可靠证明每个 worker 是否从同一冻结基线开始、是否只改了分配范围、其测试是否对应最终被集成的代码。

讨论形成的方向是“控制面串行、执行面并行”：Coordinator 继续独占需求、方案、状态和收口决策；worker 只执行 P3 已准入的工作包。审计确认方向成立，同时发现四个前置缺口：现有 hook 没有 Agent/slot 身份且 shell 可绕开；独立 worktree 缺少 `.ai/` 启动快照和运行资源隔离；evidence v1 不记录 slot/commit/baseline；TECH_PLAN 的 H2 又受 artifact manifest 严格固定，不能直接自由追加新段落。

因此本方向不能从“多起几个 Agent”开始，而要先建立身份与真源，再补权限/对账，最后才开放扇出。最小实现优先复用现有结构：槽合同若能放入 TECH_PLAN 现有固定段落，就不另建 manifest；只有机器解析和生命周期确实需要独立真源时才新增文件。证据侧先采用集成后统一复现，等真实使用证明 worker 证据绑定有独立价值后再升级 schema。

设计与审计来源为 `.ai/00_IDEATION.md` 和 `.ai/00_IDEATION.html`；候办草稿只保存可启动方向，不把讨论过程复制成第二份历史。

## 拆分路线图

预计 4 个迭代承接；实际迭代号在启动时绑定。

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 执行槽与 dispatch snapshot 合同：决定槽真源落点，定义身份、AC/路径/契约/依赖/回执字段，并同步 artifact manifest、模板、schema 与迁移边界 | — | planned |
| R2 | Worktree 与权限/范围闭环：同基线启动、`.ai/` 不合并、端口/DB/临时目录隔离、Owned Paths 检查、shell 边界亮牌和逐槽 diff 归因 | — | planned |
| R3 | 集成队列与证据闭环：一次性集成分支、先审后合并、拒绝/重试/漂移回流，集成提交统一 evidence、P5 与 Goal 裁决 | — | planned |
| R4 | 多宿主接线与真实 dogfood：受控扇出、能力降级、负向冲突 fixture、完整 CI、独立复核及并行收益/协调成本测量 | — | planned |

## 范围演进记录

- 2026-07-28：由 Butler 并行执行 ideation 与同上下文审计建立候办；按审计结论将身份、证据和集成隔离前置，MVP 保持单 active 迭代。
