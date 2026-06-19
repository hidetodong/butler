> 分流: 完整 | 命中升级信号: 多文件改动(≥3) / 契约变更(新增功能开关配置契约 + 改 dangerous 跨会话语义) / 关键路径(危险模式无人值守自治) / 跨模块影响(local-constraints·logic-protocol·dangerous-engine·部署) / 设计取舍(配置归宿·危险跨会话·preference 取舍) | 2026-06-19

# Goal
- 把 butler 的**持久运行模式状态**从"只活在对话里"外化为**项目级可读可写的持久配置**，落点统一在现有 `.ai/local-constraints.md`（新增"Butler 功能开关"段），让 AI 在会话起始读取并据此执行；同时把里程碑"active 自动归属 / closed 不再写入"的现有行为显式化（Ask A）。

# Current Understanding
- **病根**：`logic-protocol.md §4` 把 Dangerous / Preference 标为"持久 Mode"，但**无任何文件记录该持久状态**——新会话无从得知上次开着什么。与 ITER-0004 外化 ACK/分流同源（控制状态不外化，违背"不依赖对话记忆"立身原则）。
- **用户诉求**：① 一个**统一**的地方对 butler 功能做项目级持久化配置（用户点名希望复用已有落点而非新造文件）；② AI 读取后遵循执行；③ 可对话 NL 触发改、也可手改。
- **落点已定（用户拍板）**：扩展 `.ai/local-constraints.md`——它本就是"项目级持久化配置/与通用 SOP 的差异"，已含 `Review Policy: independent_review` 开关先例，部署时即建、在 `.ai/`，正好满足"统一 + 部署建好默认"。新建独立文件会与之并列成两个配置文件，反而背离"统一"。
- **关键冲突（已向用户澄清并由其裁决）**：`dangerous-engine.md §3` **故意**规定危险模式"会话结束即回 Standard、不自动续开"，是防误触无人值守的安全闸。用户诉求反转它（跨会话持久 + 自动生效）。用户知情后选择：**跨会话读到 `dangerous: on` → 显式声明后直接自动生效**（以"读到即声明 + /dangerous off 显式关"作缓解），需相应改写 §3。
- **preference 取舍**：偏好系统是**跨项目**的（外置 `$BUTLER_PREF` 存储、跨项目通识），其 on/off 不是项目级配置，**不纳入** local-constraints 功能开关；在 schema 注明其状态归外置存储。

# Constraints
- 显性约束：
  - 不破坏三层分层与 P1→P5 产物链；新增配置字段/语义须在 `Coder/README.md` 注册。
  - 模板 SSOT 是 `templates/rule-card.md`，改强制约束经占位符传播、不手工双写。
  - local-constraints 仍是"差异/配置"而非"规则复制器"；功能开关是配置项，不复制引擎规则。
  - 向后兼容：已部署项目的旧 local-constraints（仅有 `Review Policy` 或无功能开关段）须按 legacy 兼容，不被误判；迁移走 `butler-upgrade`，本轮不强制回填。
- 隐性约束：
  - 危险模式跨会话自动生效是**降低安全冗余**的取舍，必须用 announce-on-read 硬性兜底（每会话起始显式声明、绝不静默），并在 §3 与人类文档如实标注风险。
  - 功能开关读取必须真正接线进会话起始流程，否则"写了没人读"=无效外化。
  - 里程碑/迭代的 active 真源仍是台账 `current`，**不进** local-constraints（避免第二真源）。

# Impact Scope
- 确定改：
  - `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`：新增"Butler 功能开关"段（`dangerous`、`independent_review` 整合）+ 字段语义 + 写入/读取/手改口径 + preference 排除说明 + legacy 兼容；更新目标段为"本地化适配 + 功能开关"。
  - `Coder/00_System_Prompt/logic-protocol.md`：§1 增"已部署项目会话起始读取 local-constraints 功能开关并据此激活模式"；§4 更新 Dangerous（持久态落 local-constraints、跨会话 announce+auto-apply）、注明 independent_review 落点。
  - `Coder/65_Extension_Dangerous/dangerous-engine.md` §3：改写"不跨会话续开"为"持久态外化到 local-constraints `dangerous`，跨会话读到 on → 显式声明后自动生效"，`/dangerous on|off` 回写开关。
  - `Coder/20_Workflow_Lifecycle/mcv-deployment.md` §4：local-constraints 生成含功能开关段、安全默认（`dangerous: off`、`independent_review: off`）。
  - `Coder/20_Workflow_Lifecycle/lifecycle.md` §P1 + `milestone-schema.md` §7.2/§7.4：显式化 Ask A——active 里程碑自动归属新迭代、closed（`current: none`）后新迭代独立不写入。
  - `templates/rule-card.md`：补一句 local-constraints 持有项目级功能开关（dangerous/review）+ dangerous announce-on-read。
  - `HUMAN_GUIDE.md`：文档统一配置用法（NL/手改）、dangerous 跨会话声明行为、自动归属。
  - `Coder/README.md`：更新 local-constraints-schema 描述。
- 明确不影响：preference 引擎数据流（外置存储不动）、phase_gate hook、iteration-schema 锁定纪律、台账 `current` 真源地位、其它扩展模块本体逻辑。

# Project Type / Active Profiles
- 项目类型：Markdown 规则仓库（butler 自身）。未命中 Domain/Stack Profile，按通用 SOP。

# Open Questions
- 均已 ACK 前置澄清并定稿：配置归宿=扩展 local-constraints；危险跨会话=声明后自动生效（改 §3）；preference 不纳入；落点 `.ai/`、部署建好默认。无遗留待决。
