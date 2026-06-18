> 分流: 完整 | 命中升级信号: 多文件改动(≥3) / 契约变更(里程碑产物链新增 Brief 录入载体) / 设计取舍(录入通道·命令面·迭代号预分配口径) | 2026-06-19

# Goal
- 优化里程碑模式的**人机录入交互**：让用户能在一处一次性把"想推进的某个大版本"说清楚，由模型据此生成里程碑概述（`.ai/MILESTONE.md`：范围评估 + 理解阐释 + 拆分路线图），并把大版本拆成有序的迭代承接规划，方便后续逐个迭代开发。录入支持两通道：① 对话直接输入；② 在一个 md 文件里一次性阐述。操作风格走**轻量命令 `/milestone` + 现有语义触发并存**。

# Current Understanding
- 现状：里程碑全靠 `milestone-schema.md §6.1` 四个启动信号语义触发 + AI 主动提议 + soft 对齐，开启/推进/收口全是散文驱动；**没有命令入口**（不像 `/ideation`、`/loop` 等扩展模式），也**没有一次性录入载体**——用户想表达大版本意图只能零散地在对话里说，模型再边问边拼。
- 用户诉求拆成三步：① 一处说清（对话 or md 文件）；② 模型生成里程碑概述文件；③ 模型拆分路线图、规划迭代承接，方便后面开发。文件通道**不要**让用户手动在 `.ai/` 下建单个 brief 文件，而是 scaffolding 时就建好一个 `origin/` 收件箱，用户平时把原始概念文件丢进去，`/milestone` 从那儿读。`origin/` 是通用的"人类原始输入收件箱"，里程碑是它的首个消费者。
- butler 的"命令"本质是规则里的**语义约定**（仓库无 `.claude/commands/` 文件），在引擎/schema 文件定义、在 `HUMAN_GUIDE.md` 与 `templates/rule-card.md` 成体登记。故 `/milestone` 同样是语义约定，不是真实 slash-command 文件。
- 关键张力："拆分分配具体的迭代号" vs `milestone-schema.md §5.3` 的**不预先占号**纪律（迭代号单调递增、开启时才从台账绑定、路线图「实际 ITER」列留空）。预分配全局迭代号是脆的（中途插独立迭代 / 计划变更即失真）。倾向：路线图给主题切片 + 预计 ITER 跨度（方向性），真号开启时绑——既满足"拆好规划方便开发"，又不破坏单调计数纪律。

# Constraints
- 显性约束：
  - 不破坏三层分层（SOP Core / Domain / Business）与 P1→P5 产物链；新增规则/命令必须在 `Coder/README.md` 注册（CLAUDE.md 工程约束）。
  - 模板 SSOT 是 `templates/rule-card.md`，经 `{{RULE_CARD_CONTENT}}` 占位符注入 `CLAUDE.md.template`，改强制约束只改 rule-card、不手工双写。
  - 里程碑层**不冻结、不被 hook 拦截**（保持松耦合、方向性、可选）——本次优化不得给里程碑加冻结门或 hook 校验。
  - `§5.3` 不预先占号纪律不得被推翻；`iteration-schema.md` 锁定纪律不受影响。
- 隐性约束：
  - 文档有界：brief 载体不得跨里程碑纵向堆积（与 `§3` 文档有界原则一致）。
  - 轻量命令不得喧宾夺主——`/milestone` 是入口糖，触发的仍是既有生命周期，不新增阶段、不阻塞流程。
  - brief 是非权威输入，合成后 `.ai/MILESTONE.md` 仍是唯一真源，避免双真源。

# Impact Scope
- 确定改：
  - `Coder/20_Workflow_Lifecycle/milestone-schema.md`：新增"里程碑意图书(Brief)录入 + brief→MILESTONE.md 合成协议 + `/milestone` 命令"小节，并在 §6 启动/§7.1 开启处接入；文件通道源为 `origin/`。
  - `Coder/20_Workflow_Lifecycle/mcv-deployment.md` §2 Scaffold：部署时新建 `origin/` 收件箱（定位为人类原始输入区，与 AI 处理的 `.ai/references/` 区分）。
  - `templates/rule-card.md`：里程碑段补"一次性 brief 录入（对话 / `origin/` 文件）+ `/milestone` 命令"要点（SSOT，模板自动继承）。
  - `HUMAN_GUIDE.md`：§4 目录结构补 `origin/`；§5 里程碑段更新使用方式；扩展模式表补 `/milestone` 行。
  - `Coder/README.md`：milestone-schema 描述纳入 brief 录入与命令，登记 `/milestone`。
  - `Coder/20_Workflow_Lifecycle/lifecycle.md` §P1 里程碑提议段：补一句命令等价路径（一句话级）。
- 新增 input 载体：`origin/` 收件箱（scaffolding 时创建；存放用户原始概念文件；非权威、不属四层落盘、不归档、用户自管；AI 只读不重塑）。
- 明确不影响：`iteration-schema.md` 锁定纪律、hook 体系（phase_gate 不变）、其它扩展模块（ideation/loop/review/dangerous/preference）、Composer/Learner 子系统。

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）。
- 未命中任何 Domain / Stack Profile，仅按通用 SOP 推进。

# Open Questions
- Q1（origin 位置）：`origin/` 放项目根（与 `deliveries/` 平级，人类输入↔人类可读输出对称、不混入"AI 的 .ai/"）还是 `.ai/origin/`（与 `references/` 同居 .ai 下）？倾向**项目根 `origin/`**——它是人类自管的原始概念区、AI 只读不重塑，放根更贴近"你的空间"。需用户确认。
- Q2（命令面范围）：核心是 `/milestone`（无参 = 开启/录入意图；可带意图文本或指向 brief 文件）。是否一并加只读看板 `/milestone status`（轻量、直接服务"方便后面开发"——看当前范围/路线图进度/含迭代/下一个 planned）？倾向：加，但保持最小。其余 close/abandon/evolve 仍走语义。
- Q3（迭代号口径）：沿用 §5.3 不预先占号——路线图给主题切片 R1/R2… + 预计 ITER 跨度，「实际 ITER」开启时绑。即"拆分规划"而非"硬占全局号"。需用户确认是否接受（若坚持硬预分配，需另议且会动 §5.3）。
