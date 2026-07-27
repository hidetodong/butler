# MILESTONE — MILE-0012 · 轻量 TDD 配对证据

> 方向性产物（非冻结、不走 ACK）。按奥卡姆剃刀先做最小可用版本：当某个任务明确采用 TDD 时，必须留下同一条测试命令先失败、后通过的机器记录；不提前建设完整的过程审计平台。

## 5.1 范围评估

**In Scope（版本级）**

- 只在单迭代 TECH_PLAN 明确声明的任务上启用 TDD，不先增加项目级默认开关。
- 每个 TDD cycle 声明稳定名称、对应 AC、测试 argv 与 cwd；不自动识别测试框架。
- 直接复用 verification evidence v1：Red 和 Green 各保存一个现有格式的 evidence record，不增加 sidecar、第二台账或新日志格式。
- 以稳定 evidence ID 命名约定配对 Red/Green；P5 检查 Red 先发生且为 `failed`、Green 后发生且为 `passed`，两者 argv/cwd 完全一致。
- 某任务既然显式选择 TDD，缺少有效配对记录就阻止其工程义务完成；未声明 TDD 的任务保持现有收口语义。
- 用 Butler 自身 pytest 规则逻辑完成 dogfood，并验证未启用 TDD 时现有项目、旧产物和完整 CI 行为不变。

**Out of Scope（版本级）**

- 不证明生产代码绝对没有在 Red 前修改，不绑定迭代起点 baseline。
- 不检查测试文件是否在 Red 后被修改或弱化，不保存测试/生产文件哈希。
- 不判断失败是否一定来自目标行为缺失；依赖错误、语法错误等“有效 Red”分类留待后续增强。
- 不新增 Generic Runner、adapter schema、`.ai/tdd-config.json`、复杂状态机或独立 TDD skill。
- 不自动把最终生产代码 diff 与 cycle 全量对账，不处理并行 cycle、同文件测试或 Monorepo workspace 映射。
- 不增加“没有 Red 就禁止源码写入”的 PreToolUse 硬门。

**关键交付目标**

- AI 不能只口头声称“按 TDD 开发”；声明使用 TDD 的任务必须交回真实 Red/Green evidence 配对。
- V1 只依赖现有 evidence record 的时间、outcome、argv 与 cwd，不引入尚未证明必要的新基础设施。
- Red 缺失、Green 缺失、顺序颠倒、outcome 不符或命令漂移都会被 P5 明确拒绝。
- 未声明 TDD 时零新增文件、零新增门禁、零行为变化。
- pytest dogfood 和负向 fixture 证明最小闭环可用，再决定是否启动后续可信度增强候办。

## 5.2 理解阐释

Butler 已经能保存真实测试命令的成功和失败 evidence，但目前不会把同一任务的一次失败与后续通过解释成 TDD 配对。原候办把这个缺口扩展成 baseline、文件哈希、adapter、状态机和 diff 对账组成的完整审计平台，概念和实现成本过高。

本里程碑先回答一个更小的问题：轻量 Red→Green 配对是否真的能改善 AI 开发纪律。V1 不声称证明整个开发历史绝对清白，只证明 Butler 亲自记录到同一测试命令先失败、后通过。若真实使用中出现“改弱测试换绿”“无关失败冒充 Red”等具体问题，再从独立候办逐步增强。

## 5.3 拆分路线图

| 路线项 | 主题 / 范围切片 | 实际 ITER | 状态 |
|---|---|---|---|
| R1 | 轻量配对合同与检查器：TECH_PLAN cycle 声明、evidence ID 约定、Red/Green 顺序/outcome/argv/cwd 校验及负向 fixture | ITER-0091 | closed |
| R2 | 生命周期接线与 dogfood：P5/Goal 完成门、VERIFY 投影、pytest 真实使用、关闭态兼容、双宿主规则同步与完整 CI | ITER-0092 | closed |

## 5.4 范围演进记录

- 2026-07-24：由“以 opt-in 方式记录可信 Red→Green”的讨论建立原始候办方向。
- 2026-07-24：审计发现完整 baseline/adapter/状态机/diff 方案概念过重；用户确认遵循奥卡姆剃刀，从简单实现开始逐步增强。
- 2026-07-24：将 V1 轻量配对提升为 MILE-0012；防测试改弱、有效 Red、跨语言 Adapter 与 diff 对账拆回独立候办。
- 2026-07-26：开启 R2，绑定 ITER-0092，进入 P5 / Goal 接线与 pytest dogfood。
- 2026-07-26：R2 通过 TDD 真实 dogfood、完整 CI 与 Goal 机械裁决；MILE-0012 两个路线项全部收口。
