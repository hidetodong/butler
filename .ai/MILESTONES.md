# 里程碑台账

current: none

| 里程碑号 | 标题 | 状态 | 开启 | 收口 | 含迭代 | 交付 |
|---|---|---|---|---|---|---|
| MILE-0015 | Butler 领域模型治理：统一语言、限界上下文与可执行边界 | closed | 2026-07-31 | 2026-08-17 | ITER-0107, ITER-0108, ITER-0109, ITER-0110, ITER-0111 | deliveries/milestones/MILE-0015-domain-model-governance.md |
| MILE-0014 | Butler Explore 决策地图接入：把持久化决策探索衔接到 Milestone 与 Iteration | closed | 2026-08-01 | 2026-08-02 | ITER-0102, ITER-0103, ITER-0104, ITER-0105, ITER-0106 | deliveries/milestones/MILE-0014-explore-decision-map-integration.md |
| MILE-0013 | 项目级 Butler 配置结构化：从本地约束中拆出扁平 JSON 配置 | closed | 2026-07-28 | 2026-07-28 | ITER-0093, ITER-0094, ITER-0095 | deliveries/milestones/MILE-0013-project-config-structure.md |
| MILE-0012 | 轻量 TDD 配对证据：复用现有 evidence 记录同一测试命令先失败、后通过并接入收口检查 | closed | 2026-07-24 | 2026-07-26 | ITER-0091, ITER-0092 | deliveries/milestones/MILE-0012-lightweight-tdd-pair-evidence.md |
| MILE-0011 | 确定性五件套产物链：固定结构、阶段生成与机械校验 | closed | 2026-07-23 | 2026-07-23 | ITER-0086, ITER-0087, ITER-0088, ITER-0089 | deliveries/milestones/MILE-0011-deterministic-artifact-pipeline.md |
| MILE-0010 | Butler 长期规模治理：可信 handoff、长编号与有界双台账 | closed | 2026-07-22 | 2026-07-22 | ITER-0083, ITER-0084 | deliveries/milestones/MILE-0010-long-horizon-scale-governance.md |
| MILE-0009 | 需求收件箱、多 PRD 与 Monorepo 范围治理 | closed | 2026-07-22 | 2026-07-22 | ITER-0075, ITER-0076, ITER-0077, ITER-0078, ITER-0079, ITER-0080, ITER-0081, ITER-0082 | deliveries/milestones/MILE-0009-prd-inbox-monorepo-governance.md |
| MILE-0008 | Butler 目标可信闭环：让 Goal 从“任务做完”升级为经方案准入、执行校准、证据与反证审查后才可完成的可审计承诺 | closed | 2026-07-18 | 2026-07-18 | ITER-0061, ITER-0062, ITER-0063, ITER-0064, ITER-0065, ITER-0066 | deliveries/milestones/MILE-0008-goal-assurance-loop.md |
| MILE-0007 | Butler 规则仓工程化加固：安全安装、状态自证、持续验证、可执行升级与双宿主治理收敛 | closed | 2026-07-18 | 2026-07-18 | ITER-0056, ITER-0057, ITER-0058, ITER-0059, ITER-0060 | deliveries/milestones/MILE-0007-engineering-hardening.md |
| MILE-0006 | Codex 双宿主兼容层：保留 Claude Code 能力，同时让规则注入、命令工作流、hooks 与部署升级在 Codex 中原生可用 | closed | 2026-07-17 | 2026-07-17 | ITER-0051, ITER-0052, ITER-0053, ITER-0054 | deliveries/milestones/MILE-0006-codex-dual-host-compatibility.md |
| MILE-0005 | butler 命令命名空间系统：把散落的散文触发词收敛成 `/butler:xxx` 一整套真实 slash 命令、全局任意项目可用（薄壳路由器 + 命名空间隔离撞名） | closed | 2026-07-14 | 2026-07-14 | ITER-0047, ITER-0048, ITER-0049, ITER-0050 | deliveries/milestones/MILE-0005-command-namespace-system.md |
| MILE-0004 | PRD 先行 + references 版本化改版同步：给参考资料补索引/渐进读待遇 + PRD 切分/钉版 + `/prd update` 改版同步协议 | closed | 2026-07-08 | 2026-07-09 | ITER-0036, ITER-0037, ITER-0038, ITER-0039, ITER-0040, ITER-0041 | deliveries/milestones/MILE-0004-prd-first-versioned-references.md |
| MILE-0003 | 项目知识文件夹升级 + 帮手名册 + 说人话：PROJECT.md → .ai/project/ 主题文件夹 + 帮手名册（复核 / 更新说明 / 查过时）+ 讲人话扩到所有面向人输出 | closed | 2026-07-05 | 2026-07-08 | ITER-0026, ITER-0028, ITER-0029, ITER-0030, ITER-0031, ITER-0032, ITER-0033, ITER-0034 | deliveries/milestones/MILE-0003-knowledge-folder-agents-plainlang.md |
| MILE-0002 | 自动化测试最大化 + 人测 web 回环：竭尽自动化 + JSON 驱动的 butler 驻留人测桥 + 后台等待续跑 | closed | 2026-07-02 | 2026-07-03 | ITER-0021, ITER-0022, ITER-0023, ITER-0024, ITER-0025 | deliveries/milestones/MILE-0002-automation-and-human-test-loop.md |
| MILE-0001 | 冷启动可恢复性与收口知识固结：补全"项目全貌"产物 + 给收口加门槛 | closed | 2026-06-30 | 2026-07-02 | ITER-0017, ITER-0018, ITER-0019 | deliveries/milestones/MILE-0001-coldstart-recoverability.md |

## 待办区（未编号）

| 候办键 | 标题 | 暂缓日期 | 草稿 | 暂缓原因 |
|---|---|---|---|---|
| butler-slim-down | Butler 瘦身与重造：砍 fold 与死码、重造 inbox、装监视器 | 2026-08-17 | .ai/milestone-backlog/butler-slim-down.md | 由本轮 `/grill-me` audit 收敛：`.ai/project/` fold 长期无消费与校准（作者不读、drift-check 几无触发、MILE-0014 已知失真三周未发现）、progress 与旧 inbox / origin 长期零使用、根 layout 臃肿、无 usage instrumentation 导致不可淘汰。当前 MILE-0015 仍 active，按单 active 约束先入待办，R5 收口后提升为正式 MILE-NNNN。 |
| prd-impact-reconciliation | PRD 改版的实现面对账：从切片变化推到代码落点，并证明没有漏 | 2026-08-06 | .ai/milestone-backlog/prd-impact-reconciliation.md | 由 signal-assistant 一次真实漏项收敛而来；当前 MILE-0015 仍 active，按单 active 约束先入待办。首版只做枚举、四态判定与双向覆盖，静态分析和自动改码明确留待以后。 |
| upgrade-convergence-engine | Butler 升级收敛引擎：文件所有权、确定性迁移与可恢复诊断 | 2026-08-04 | .ai/milestone-backlog/upgrade-convergence-engine.md | 方向已完成 ideation；当前 MILE-0015 仍 active，按单 active 约束先入待办，待现里程碑处理完后再独立提升。 |
| prd-evidence-check | PRD 原文疑问检索：基于当前版本给出带证据的四态判断 | 2026-08-04 | .ai/milestone-backlog/prd-evidence-check.md | 方向已完成 ideation；本轮只入候办、不开工，历史版本查询与版本对比明确留待以后。 |
| codex-structured-question-cards | Codex 结构化提问卡片：让 Butler 的有限选项确认可点击，并在宿主不支持时可靠降级 | 2026-08-01 | .ai/milestone-backlog/codex-structured-question-cards.md | Codex 当前原生能力受运行模式和单选限制，且卡片由宿主而非 skill 控制；先建立能力合同、文字降级和真实使用证据，再决定是否值得建设自定义 UI。 |
| ai-user-experience-driven-iteration | AI 用户体验驱动迭代：从结果目标到黑盒体验、修复与复验 | 2026-07-30 | .ai/milestone-backlog/ai-user-experience-driven-iteration.md | 方向价值高但 AI 小白代表性、自评偏差与真实改善尚未验证；先用现有能力完成真实 dogfood，再决定是否产品化。 |
| parallel-p4-execution-slots | 单迭代多 Agent 并行 P4：执行槽、证据与集成隔离 | 2026-07-28 | .ai/milestone-backlog/parallel-p4-execution-slots.md | 方向已完成 ideation 与审计；需先补齐身份、worktree 真源、证据和集成隔离合同，再决定正式启动。 |
| multi-active-iteration-runtime | 多 active 迭代运行时：迭代级真源、Batch 与跨迭代集成审计 | 2026-07-28 | .ai/milestone-backlog/multi-active-iteration-runtime.md | 属高成本后续形态；等待单迭代并行 P4 的真实 dogfood 与收益数据，避免提前迁移全局状态机。 |
| prd-future-route-fulfillment | PRD 改版到未启动里程碑路线项的确定性兑现闭环 | 2026-07-23 | .ai/milestone-backlog/prd-future-route-fulfillment.md | 先保留方向：当前只识别并记录 future disposition，路线项启动时尚无机械消费与兑现门禁。 |
| state-transition-trust-gate | 关键节点状态可信闭环：防止 AI 宣称已更新但落档仍陈旧 | 2026-07-24 | .ai/milestone-backlog/state-transition-trust-gate.md | 先保留方向：现有审计能验证结构与哈希，但会放过节点后权威记录、摘要和真实环境之间的确定性矛盾。 |
| tdd-evidence-hardening | TDD 证据增强：防测试改弱、有效 Red、跨语言 Adapter 与实际改动对账 | 2026-07-24 | .ai/milestone-backlog/tdd-evidence-hardening.md | V1 先验证轻量 Red→Green 配对的实际价值；更强的过程证明等真实使用暴露需要后再推进。 |
