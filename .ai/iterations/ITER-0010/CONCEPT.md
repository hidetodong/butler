> 分流: 完整 | 命中升级信号: 契约变更（delivery-summary 收口产出契约扩展）、多文件改动（≥6 个规则/模板文件）、跨模块影响（delivery/iteration/milestone/lifecycle schema + templates + HUMAN_GUIDE）、设计取舍（HTML 生成方式：模板手填 vs 转换脚本，已由用户裁定为模板手填） | 2026-06-20

# Goal

- 让 butler 的迭代 / 里程碑交付总结，除现有 Markdown 外，**额外产出一份固定格式的 HTML 阅读视图**，方便人类直接打开阅读。
- HTML 必须是**固定格式**（统一布局与样式），保证每份交付看起来一致；格式有唯一 SSOT，不在每次收口手搓飘移。
- 不破坏现有产物链与「交付总结只引用产物路径、不嵌入全文、体量恒定」的硬约束。

# Current Understanding

- 现状：迭代收口三步之一是「生成 `deliveries/ITER-NNNN-<slug>.md`」；里程碑收口同理产 `deliveries/milestones/MILE-NNNN-<slug>.md`。两者都是 Markdown，结构由 `delivery-summary.md §4`（迭代级）与 §4.8（里程碑级聚合口径）定义。
- 用户诉求：Markdown 在终端 / 编辑器里看尚可，但要给人「方便阅读」的呈现，需要一份固定排版的 HTML。
- 已与用户裁定的四个设计分叉：
  1. **生成方式 = 固定模板手填**：在 `templates/` 放一份固定 HTML 模板（`{{占位符}}` + 内联 CSS、单文件自包含），收口时 AI 按 §4 结构填槽生成。无运行时依赖（不引入 node/python/pandoc），纯 markdown 仓库友好，复用现有 `{{占位符}}` SSOT 范式（同 `CLAUDE.md.template` 的 `{{RULE_CARD_CONTENT}}`）。
  2. **覆盖范围 = 迭代级 + 里程碑级**：ITER 与 MILE 两类交付都产 HTML，两层阅读体验一致。
  3. **触发时机 = 每次收口强制产**：HTML 与 MD 并列，成为收口标准产物（收口三步中「写交付总结」那一步同时产 `.md` + 同名 `.html`），不是 opt-in。
  4. **存量回填 = 不回填**：仅对 ITER-0010 起及之后的收口生效，历史 13 份交付保持原 `.md` 现状。
- 预期产出：
  - 新增固定 HTML 模板 SSOT 文件（`templates/` 下）。
  - 规则侧把「收口产出契约」从「写一份 `.md`」扩展为「写一份 `.md`（引用真源）+ 同名 `.html`（固定格式阅读视图）」，并贯通到所有引用该契约的规则 / 模板 / 指南。

# Constraints

- **显性约束**：
  - HTML 与 MD **并存**，MD 仍是**引用真源**（`AC_LIST/TECH_PLAN/VERIFY_REPORT` 等只能以路径指针引用，不嵌入全文）；HTML 是 MD 的渲染/阅读投影，不引入第二真源、不复制四件套全文。HTML 同样遵守 `delivery-summary.md §4.7` 的「只引用不嵌入、体量恒定」硬约束。
  - 固定格式必须有**唯一 SSOT**（模板文件），收口时填槽，不在规则文件里散落多份 HTML 范式。
  - HTML 必须**单文件自包含**（内联 CSS、零外部依赖），双击即可打开、可归档、可离线阅读。
  - 收口仍是**三步**，不新增第四步——「写交付总结」那一步从单产出 `.md` 扩为双产出 `.md` + `.html`，三步框架不变。
- **隐性约束**：
  - 不破坏分层：模板归 `templates/`，规则语义归 `20_Workflow_Lifecycle/delivery-summary.md`，不把大段 HTML 塞进规则正文。
  - 不破坏现有 hook 契约（phase_gate 只管迭代工作区四件套与 AC 冻结，HTML 在 P5 收口产出，AC 早已 ack-frozen，零 hook 改动）。
  - 模板单一来源纪律（CLAUDE.md 编辑约束 #4）：HTML 固定格式以模板文件为 SSOT，规则只引用不重述其结构。
  - 写作风格用「必须/不得/应」，措辞面向 AI 执行。

# Impact Scope

- **会改**（规则语义 + 传播面）：
  - 新增 `templates/delivery.html.template`（固定 HTML 模板 SSOT）。
  - `Coder/20_Workflow_Lifecycle/delivery-summary.md`（主规则：新增 HTML 阅读视图小节 + §3 命名/存放补 `.html` 同名兄弟文件 + 收口产出契约 + §8 对话引用口径）。
  - `Coder/20_Workflow_Lifecycle/iteration-schema.md`（§3 三层落盘「人类交付」行 + §5.5 收口三步 step 2 双产出）。
  - `Coder/20_Workflow_Lifecycle/milestone-schema.md`（§7.4 收口三步 step 2 双产出 + §9 交付文档结构树补 `.html`）。
  - `Coder/20_Workflow_Lifecycle/lifecycle.md`（P5 收口 step ② 措辞双产出）。
  - `templates/rule-card.md`（浓缩规则卡 ITER / MILE 收口三步描述）。
  - `HUMAN_GUIDE.md`（deliveries 结构说明 + 交付视图描述）。
  - 可能微调：`Coder/README.md`（delivery-summary 职责一行）、仓库根 `CLAUDE.md`（templates/ 内容物描述补 delivery.html.template）。
- **明确不影响**（零改动护栏）：
  - 产物链四件套 schema（concept/acceptance/tech-plan/verify）字段语义。
  - hook 体系（phase_gate / ledger_status）契约与脚本。
  - 迭代 / 里程碑号分配、台账枚举、ACK 冻结纪律、overwrite-only。
  - 历史 13 份 `deliveries/` 文件（不回填、不重命名）。
  - `VERSION` / `CHANGELOG.md`：本轮不发版，累积到下次切版（预计 MINOR：向后兼容新增可选交付产物，legacy 无 `.html` 的旧交付照常放行）。
  - 各扩展模块（ideation/loop/review/dangerous/preference）。

# Project Type / Active Profiles

- 项目形态：**Markdown 规则仓库**（butler 自身），编辑的是协作 SOP 规则本身，非用软件栈开发应用。
- 命中的 Domain / Stack Profiles：**无**。`10_Domain_Stack_Profiles/` 下的 vue3 / typescript / build-tooling 均不适用，仅按通用 SOP + 本仓库 `CLAUDE.md` 编辑约束推进。
- HTML 模板里的内联 CSS 是「固定排版资产」，不引入前端工程栈，不触发前端 profile。

# Open Questions

- 模板占位符的粒度与 MILE 特有的「拆分路线图回填」段如何在同一模板里安放（单模板 + 可选路线图段 vs ITER/MILE 两个薄变体）——倾向单模板 + 可选段，留待 P3 TECH_PLAN 定稿。
- HTML 模板从何处读取以填槽：倾向「butler 仓库 `templates/delivery.html.template` 为 SSOT，收口时 AI 读取填槽」，与部署/升级读 `$BUTLER` 同源假设；是否需要在基地车部署时复制进目标项目（避免 $BUTLER 不可达），留待 P3 评估（默认：不复制，避免副本漂移）。
- 以上均为方案层细节，不改变 Goal 与验收范围，进入 P2 不阻塞。
