---
状态: ack-frozen
ACK 日期: 2026-06-19
---

# Goal
- 把里程碑的录入交互从"零散对话 + 散文操作"升级为"一次性 brief（对话 / `origin/` 文件两通道）→ 模型合成 `.ai/MILESTONE.md` 概述 + 拆分路线图"，并提供轻量命令 `/milestone` 与现有语义触发并存，全程不破坏里程碑松耦合、不冻结、不被 hook 拦的定位。文件通道靠 scaffolding 时创建的 `origin/` 收件箱承载，用户无需手动建文件。

# In Scope
- scaffolding（`mcv-deployment.md` §2）部署时新建 `origin/` 收件箱：人类原始概念输入区，与 AI 处理的 `.ai/references/` 区分。
- `milestone-schema.md` 新增"里程碑意图书 (Brief) 录入"机制：两通道（对话 / `origin/` 文件）、brief 非权威输入定位、brief→MILESTONE.md 三段合成协议、soft 对齐非硬门。
- 轻量命令 `/milestone`（开启/录入）+ `/milestone status`（只读看板），与语义触发等价并存。
- 路线图沿用 §5.3 不预先占号：主题切片 R1/R2… + 预计 ITER 跨度，「实际 ITER」开启时绑。
- SSOT 传播：`templates/rule-card.md` 里程碑段更新（模板经占位符自动继承）。
- 文档同步：`HUMAN_GUIDE.md` §4 目录结构 + §5 里程碑段、`Coder/README.md`、`lifecycle.md` §P1 里程碑提议段。
- dogfood：ITER-0005 走完整 P1→P5 并收口。

# Out of Scope
- 给里程碑加冻结门 / hook 校验（违背松耦合定位，不做）。
- 推翻 §5.3 改成硬预分配全局迭代号（若用户坚持需另开议题）。
- `iteration-schema.md` 锁定纪律、phase_gate hook、其它扩展模块、Composer/Learner。
- 里程碑 close/abandon/evolve 的命令化（本轮仍走语义；命令面只覆盖最高频的 open/status）。

# Acceptance Checklist
- [ ] AC0: `mcv-deployment.md` §2 Scaffold 部署时**新建 `origin/` 收件箱**：定位为人类原始概念输入区（用户自管、AI 只读不重塑），与 AI 处理改名注入的 `.ai/references/` 显式区分；说明它是 `/milestone` 等录入流的文件通道源。位置以 ACK 确认为准（默认项目根 `origin/`）。
- [ ] AC1: `milestone-schema.md` 新增"里程碑意图书 (Brief) 录入"小节，明确定义：① 两录入通道（对话直接输入 / `origin/` 下原始概念文件一次性阐述）；② brief 是**可选、非权威、一次性输入**，不属 §3 四层落盘、不归档、不跨里程碑纵向堆积；③ 合成后 `.ai/MILESTONE.md` 是唯一真源。
- [ ] AC2: 同小节定义 **brief → `.ai/MILESTONE.md` 合成协议**：模型读 `origin/` 文件（或对话输入）把意图解析落到三段——范围评估（In/Out/关键交付目标）、理解阐释（核心问题/背景价值/系统影响）、拆分路线图；信息不足处显式列为待澄清而非臆造；产出后向用户 soft 对齐（非硬门、可演进）。
- [ ] AC3: 合成协议中的路线图明确沿用 §5.3——按主题切片排序 R1/R2…、标「预计 ITER 跨度」、「实际 ITER」列留空待开启时绑定；显式声明这是"拆分规划"而非"预先占号"，与 §5.3 不矛盾（可加交叉引用）。
- [ ] AC4: 引入轻量命令 `/milestone`：无参 = 开启/录入里程碑意图（按 §6.1 走启动信号判定与 soft 对齐）；可带意图文本或指向 brief 文件。命令与语义触发**等价并存**（命令是入口糖，触发的仍是既有生命周期，不新增阶段、不阻塞流程）。在 `milestone-schema.md` 注明。
- [ ] AC5: 引入只读看板 `/milestone status`：让模型读 `.ai/MILESTONES.md` + `.ai/MILESTONE.md` 汇报"当前里程碑：范围 / 路线图进度 / 已含迭代 / 下一个 planned 路线项"，不写任何文件、不改状态。在 `milestone-schema.md` 注明。
- [ ] AC6: `templates/rule-card.md` 里程碑段补"一次性 brief 录入（对话 / `origin/` 文件）+ `/milestone` 开启 / `/milestone status` 看板"要点；不手工改 `CLAUDE.md.template`（经 `{{RULE_CARD_CONTENT}}` 占位符自动继承）。
- [ ] AC7: `HUMAN_GUIDE.md` 更新：① §4「部署后的目录结构」补 `origin/`（人类原始概念输入区）；② §5「里程碑（大版本）」段说明两通道一次性录入、`/milestone` 与 `/milestone status` 用法、模型如何据 brief 生成概述与路线图；③ §5 扩展模式表补一行 `/milestone`（或在里程碑段内成体登记命令）。
- [ ] AC8: `Coder/README.md` 中 milestone-schema 的职责描述纳入 brief 录入与命令；`/milestone` 命令在文档中登记（满足"新增规则/命令必须注册"约束）。
- [ ] AC9: `lifecycle.md` §P1 里程碑提议段补一句：`/milestone` 命令是开里程碑的等价显式入口（与启动信号语义触发并列），不改其余推进规则。
- [ ] AC10: 不破坏既有约束——里程碑层仍不冻结、不被 hook 拦截；§5.3 不预先占号、§7 生命周期五动作、四层落盘结构、文档有界原则均保持；`origin/` 与 `.ai/references/` 角色不混淆（前者人类自管只读、后者 AI 处理注入）；`iteration-schema.md` 与 phase_gate 零改动。
- [ ] AC11: dogfood——本迭代 `.ai/CONCEPT.md` 带分流记录、`.ai/AC_LIST.md` 走 draft→ack-frozen、产出 `.ai/TECH_PLAN.md` 与 `.ai/VERIFY_REPORT.md`，ITER-0005 按 `iteration-schema.md §5.5` 收口（归档 + `deliveries/ITER-0005-<slug>.md` + 台账置 closed）。

# Verification Method
- AC0：阅读 `mcv-deployment.md` §2 diff，确认 `origin/` 列入部署创建目录且与 `references/` 角色区分到位。
- AC1 / AC2 / AC3 / AC4 / AC5：阅读 `milestone-schema.md` diff，确认新小节字段/协议/命令按 AC 落地，且与 §3/§5.3/§6/§7 无矛盾（grep 关键词 + 人工 review 交叉引用一致）。
- AC6：对比 `templates/rule-card.md` 里程碑段与 `CLAUDE.md.template` 占位符，确认 SSOT 单写、模板未被手工双写。
- AC7 / AC8 / AC9：阅读 `HUMAN_GUIDE.md` / `Coder/README.md` / `lifecycle.md` diff，确认登记与措辞到位、命令在 README 注册。
- AC10：grep 确认未引入里程碑冻结/hook 文案、§5.3 原文保留；`git diff` 确认 `iteration-schema.md`、`templates/hooks/` 零改动。
- AC11：检查 `.ai/iterations/ITER-0005/` 快照、`deliveries/ITER-0005-*.md`、`ITERATIONS.md` 该行 `closed`。

# Open Questions / Risks
- 已 ACK 定稿（2026-06-19）：Q1 `origin/` 置**项目根**（与 `deliveries/` 平级）；Q2 纳入 `/milestone status` 看板；Q3 迭代号沿用 §5.3 不预先占号（路线图给主题切片 + 预计跨度，真号开启时绑）。
- 风险：`origin/` 部署时创建空目录——git 不跟踪空目录，目标项目无碍（首次放文件即出现）；butler 自身是规则仓库、非部署目标，不在本仓库建 `origin/`。
- 风险：命令是语义约定而非真实 slash-command，AI 在长上下文下可能识别不稳——靠 rule-card 高注意力区登记 + README 注册缓解，与现有 `/ideation` 等同源同风险，不新增机制。
