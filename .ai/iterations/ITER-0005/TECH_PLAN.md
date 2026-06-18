# Goal
- 支撑 AC0–AC11：在不破坏里程碑松耦合/不冻结/不被 hook 拦定位的前提下，落地"`origin/` 收件箱 + 两通道 brief 录入 + brief→MILESTONE.md 合成协议 + `/milestone` 与 `/milestone status` 命令"，并经 SSOT 传播到模板与人类文档。

# Files / Modules to Change
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md` — §2 Scaffold 加 `origin/`（部署时创建，与 references 区分）。【AC0】
- `Coder/20_Workflow_Lifecycle/milestone-schema.md` — 新增 §6.4 Brief 录入与合成、§6.5 命令；§7.1 开启交叉引用 §6.4。【AC1/AC2/AC3/AC4/AC5】
- `templates/rule-card.md` — 里程碑段（现 L27）补 brief 录入 + 命令要点（SSOT 单写）。【AC6】
- `HUMAN_GUIDE.md` — §4 目录树加 `origin/`；§5 里程碑段更新用法 + 成体登记命令。【AC7】
- `Coder/README.md` — milestone-schema 职责描述（现 L127）纳入 brief/命令；mcv-deployment 描述（现 L117）提 `origin/`。【AC8】
- `Coder/20_Workflow_Lifecycle/lifecycle.md` — §P1 里程碑提议段（现 L86）补一句 `/milestone` 等价入口。【AC9】
- `.ai/`（dogfood）— ITER-0005 四件套 + 收口归档 + 台账 + `deliveries/ITER-0005-<slug>.md`。【AC11】
- **零改动（守 AC10）**：`iteration-schema.md`、`templates/hooks/**`、`acceptance-schema.md`、其它扩展模块。

# External References
- 无（`.ai/references/` 下无参考资料）。

# Interface / Contract
- **`origin/` 目录契约**：项目根、部署时创建的空目录；人类自管原始概念输入；AI 只读、不写不改不重塑不归档；非 §3 四层落盘成员。与 `.ai/references/`（外部第三方资料、AI 处理改名注入）角色互斥。
- **Brief 契约**：`origin/` 下任意命名/数量的原始概念文件，或对话直接输入；可选、非权威、一次性；合成后 `.ai/MILESTONE.md` 为唯一真源。
- **合成协议（brief → `.ai/MILESTONE.md`）**：① 收集输入（origin 文件 / 对话；多份未指明则汇总相关并回述确认）→ ② 解析落 §5 三段（范围评估 / 理解阐释 / 拆分路线图）→ ③ 信息缺口显式列"待澄清"，不臆造 → ④ soft 对齐（非硬门，演进按 §5.4/§7.3）。
- **`/milestone` 命令**：无参或带意图文本 = 开启/录入，按 §6.1 信号判定 + §6.4 合成 + §7.1 开启；与语义触发**等价**（入口糖，不新增阶段、不阻塞流程）。
- **`/milestone status` 命令**：只读看板，读 `.ai/MILESTONES.md` + `.ai/MILESTONE.md` 报当前里程碑标题/状态、范围摘要、路线图各项进度、含迭代、下一个 `planned` 项；无 active 里程碑时如实报"无"；不写文件、不改状态。

# State / Boundary
- 命令面**只覆盖** open / status 两个最高频动作；close / abandon / evolve 仍走 §7.3/§7.4/§7.5 语义，不命令化。
- 里程碑层不冻结、不被 hook 拦：本次不加任何冻结门或 phase_gate 校验。
- §5.3 不预先占号纪律不动：路线图给主题切片 + 预计 ITER 跨度，「实际 ITER」开启时绑。
- 不在 butler 本仓库创建 `origin/`（butler 是规则仓库、非部署目标）。

# Design Decisions
- **新增小节用 §6.4/§6.5**（挂在"§6 启动信号与时机"下），不另起顶层节，避免 §7/§8/§9 整体重排号。
- **录入合成集中写在 §6.4，§7.1 仅交叉引用**：避免开启动作与录入协议双写；§7.1 既有"产出 MILESTONE.md + soft 对齐"措辞保留，补一句指向 §6.4 录入通道。
- **命令登记在里程碑段内、不进 HUMAN_GUIDE §5 扩展模式表**：里程碑是工作流层、非"扩展模式"，进扩展表会误分类（AC7 的"或"分支选此）。
- **rule-card 增量克制**：里程碑段是 SSOT 浓缩，只加一句 brief+命令要点，控 token；模板经 `{{RULE_CARD_CONTENT}}` 自动继承，不手工改 `CLAUDE.md.template`。
- **origin 与 references 显式对照**：在 mcv-deployment §2 与 HUMAN_GUIDE 各点一句区分，防止两者职责混淆（守 AC10）。

# Execution Steps
1. `mcv-deployment.md` §2：加 `origin/` 创建与职责、references 对照。【AC0】
2. `milestone-schema.md`：插 §6.4（Brief 录入与合成协议）、§6.5（命令）；§7.1 补交叉引用句。【AC1–AC5】
3. `templates/rule-card.md`：里程碑段补 brief + 命令要点。【AC6】
4. `HUMAN_GUIDE.md`：§4 目录树加 `origin/`；§5 里程碑段更新 + 命令登记。【AC7】
5. `Coder/README.md`：milestone / mcv-deployment 两条描述更新。【AC8】
6. `lifecycle.md` §P1：补 `/milestone` 等价入口句。【AC9】
7. 一致性自检（grep 交叉引用、SSOT 单写、§5.3/hook 零改动）。【AC10】
8. P5：dogfood 收口 ITER-0005。【AC11】

# Verification Plan
- AC0：读 `mcv-deployment.md` §2 diff，确认 `origin/` 入部署创建清单 + references 对照句。
- AC1/AC2/AC3：读 `milestone-schema.md` §6.4，确认两通道、brief 非权威定位、三段合成协议、§5.3 交叉引用与不矛盾。
- AC4/AC5：读 §6.5，确认 `/milestone` 等价语义、`/milestone status` 只读看板字段、无 active 兜底。
- AC6：对比 `rule-card.md` 里程碑段与 `CLAUDE.md.template`，确认 SSOT 单写、占位符未手工双写。
- AC7/AC8/AC9：读 `HUMAN_GUIDE.md`/`README.md`/`lifecycle.md` diff，确认目录树、用法、命令登记、README 注册、P1 等价入口句到位。
- AC10：`git diff --stat` 确认 `iteration-schema.md`、`templates/hooks/` 零改动；grep 确认无里程碑冻结/hook 文案、§5.3 原文在。
- AC11：检查 `.ai/iterations/ITER-0005/` 快照、`deliveries/ITER-0005-*.md`、`ITERATIONS.md` 该行 `closed`、`current: none`。

# Risks / Open Questions
- 命令为语义约定（非真实 slash-command），长上下文下识别可能不稳——靠 rule-card 高注意力登记 + README 注册缓解，与现有 `/ideation` 同源同险，不新增机制。
- 无其它未决项（Q1–Q3 已 ACK 定稿）。
