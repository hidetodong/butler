> 分流: 完整 | 命中升级信号: 触碰 Coder 真源触发词（迁移面最宽 71 处 + 命名撞车）, 涉及发布切版, 两命令加风险闸不得降门槛 | 2026-07-14

# 一句话

给 MILE-0005 命名空间落**最后一个路线项 R4**：两个高风险命令 `/butler:loop`（收敛闭环死磕）+ `/butler:dangerous`（无人值守自治），用薄壳路由器落地，但**命令化不得把「郑重显式触发」的门槛降低**——收口即整体收 MILE-0005。

# Goal

MILE-0005 R4：把最后两个还停在散文触发词的高风险能力落成 `/butler:*` 命令。R1–R3 证明了薄壳范本能吃扁平参数（R2）和二级嵌套参数（R3）；R4 的**唯一新面**不是参数，而是**风险闸**——`/loop`（高强度长时死磕、消耗大）和 `/dangerous`（无人值守自治、风险显著高于标准流程）命令化后，敲一下就触发的便利**绝不能**稀释它们「该被郑重、显式触发」的分量。当初特意把这俩从低风险批（R2）拆出、单开一迭代，就为把这道闸设计对。

# Current Understanding

- **两命令结构截然不同**（已读两引擎确认）：
  - **`/butler:loop`**（真源 `convergence-loop-engine.md`）：P4 执行阶段的**一次性升档**，**无持久状态、无 off**——敲 `/loop` 即开启死磕闭环，跑到验证全绿或 §6 定量熔断（连续 5 轮 / 死锁 / 环境阻塞）自然结束。结构上最薄（近似 `ideation`：读规则 + 委托，几乎无参数分派）。风险点：高强度、长时、token 消耗大，但**危险度低于 dangerous**（只管 P4、有熔断兜底）。
  - **`/butler:dangerous`**（真源 `dangerous-engine.md`）：**持久开关**，状态外化到 `.ai/local-constraints.md`「Butler 功能开关」`dangerous: on|off`（**注意：落项目级 local-constraints，不是 preference 的外置 `$PREF`**），**跨会话**（§3.1 announce-on-read：新会话读到 `on` 必须当回合显式声明后才自动进入、绝不静默续开）。结构近似 `preference` 的 on/off，但**风险高一个量级**——无人值守长程自治、P2/P3 用户 ACK 被自审门替代。
- **风险闸怎么和「薄壳只路由不复述」共存**（本迭代核心设计）：薄壳**不**重写确认对话、**不**复述护栏算法（那会破 DRY），而是用两招把门槛守住：
  1. **frontmatter `description` 带显式 ⚠️ 风险标记**（说人话）——让补全菜单本身亮明「这是危险的那道门」。这是入口处的诚实标注，不是复述算法。
  2. **第 0 步前置一句风险提醒 + 把真正的闸交回引擎**——薄壳点明前置条件（可隔离 / 可回滚环境，`dangerous-engine` §7.2 / 开篇 ⚠️），然后委托引擎自己的闸：`/dangerous` 走 §3 回写 `on` + 对话层显式回声 + §3.1 announce-on-read + §7 护栏（审计日志 / checkpoint / P5 强制完整审查）。薄壳只保证「不把危险伪装成随手一敲」，闸门机制仍在引擎里。
- **`/dangerous` 空参已有引擎定义语义**：`dangerous-engine §3` 明确 bare `/dangerous` = 开启（走回声闸）、`/dangerous off` = 关闭。故 `/butler:dangerous` **空参 = 开启（走引擎闸）**、`off` = 关闭、另加 `status` = 只读回声当前开关态。**这与 `/butler:preference` 空参 = 只读状态回声有意不同**——preference 的空参回声是薄壳新增（引擎没定义空参），dangerous 的空参已被引擎 §3 定义为开启，薄壳擅自改成 no-op 状态回声反而是发明语义、违背「薄壳只路由」。
- **命名空间落地后 logic-protocol 已同构**：§89 `/loop`、§92 `/dangerous` 已作触发模式登记，§93 `/butler:preference` 是迁后带「旧名仍识别」注的范本——照抄。

# Constraints

- **不改引擎算法**：`convergence-loop-engine.md §1–§8`、`dangerous-engine.md §1–§10` 的闭环 / 熔断 / 自治 / 自审门 / 护栏一字不动。唯一可能动的是触发词 `/loop`·`/dangerous` → `/butler:*`（**触发名非算法**，迁移面待 P2 定，见 Open Questions 2）。
- **迁移面最宽 + 命名撞车（R4 独有风险）**：`/dangerous` 在活文档 **52 处**、`/loop` **19 处**（共 71，远超 R3 的 13），且 **butler 的 `/loop` 与 Claude Code 自带 `/loop` 撞名**——`dangerous-engine.md:21` 明确引用「Claude Code 的 `/loop`、后台任务」指的是 **harness 级** loop，**绝不能迁**成 `/butler:loop`。这是 R3 没有的普查陷阱，迁移要精确排除 harness 引用。
- **不下发目标项目**：命令不进 `templates/`、部署面零影响（沿用 ITER-0044/0047/0048/0049 边界）。
- **不动 `setup.sh`**：R1 目录软链已托管全套，R4 只往目录里加两个文件。
- **薄壳纪律 + 门槛不降**：两命令都守「读对规则 + 委托真源 + 第 0 步优雅降级」；额外硬要求——**不得照抄低风险命令的轻壳**，risk 命令的 frontmatter 与第 0 步必须前置风险标记、把闸交回引擎（不复述护栏、也不省略风险提醒）。

# Impact Scope

- **新增**（命令层）：`.claude/commands/butler/loop.md` + `dangerous.md`（2 个薄壳，dangerous 含 on/off/status 分派 + 风险闸委托，loop 近乎无参数 + 风险提醒）。
- **可能改**（待 P2 定，见 Open Questions 2）：`/loop`·`/dangerous` 触发词 → `/butler:*`（活文档 71 处，**精确排除 harness-`/loop`**）、logic-protocol §89/§92 加「旧名仍识别」注、`capabilities.md` 命令表补两行、README 扩展模式表 + `butler/` 子树补两命令 + Coder 目录 `55/65` 行迁。
- **发布层**：VERSION + CHANGELOG + `migrations/vX.Y.Z.md`（切版号待定，倾向 MINOR → **v2.10.0**）。
- **不碰**：`setup.sh`、`templates/**`（含 rule-card 里 `/loop`·`/dangerous` 散文——同 R3 DD5，命令不下发目标项目、目标项目靠散文旧名兜底、故无 `[regen-claude]`）、四件套 schema、hook、其他命令、两引擎算法、`local-constraints-schema`（`dangerous:` 字段仍归它管，命令只读写开关值不改 schema）。

# Project Type

Markdown 规则仓库 dogfooding（butler 编辑自身命令层）。无代码编译，验证靠：两命令文件结构核（薄壳要点齐 + 风险闸在 frontmatter/第0步前置 + dangerous 的 on/off/status 分派覆盖 + 真源锚点真实）+ 隔离 HOME 实跑 `setup.sh` 确认新命令经目录软链可达（这次预期 **8 命令**）+ `/loop`·`/dangerous` 触发名残留普查（**harness-`/loop` 保留核对**）+ `git diff` 边界守恒。

# Open Questions（呈 ACK 时请一并确认三默认）

1. **切版号**：R4 纯新增 2 命令、无破坏面，判 **MINOR → v2.10.0**（新增能力，与 R1–R3 同类）。倾向 MINOR。
2. **`/loop`·`/dangerous` 触发名迁移策略**（R4 最需拍板处）：迁移面 71 处、最宽，且有 harness-`/loop` 撞车。倾向**全迁但外科手术式**——把作 butler 命令引用的 `/loop`·`/dangerous` 一致迁 `/butler:*`（保命名空间统一、不留半迁状态），但**精确排除** `dangerous-engine.md:21` 的 harness-`/loop`、保留 logic-protocol 旧名识别 + 自然语言触发（「放手做 / 死磕」照常）。**备选（更保守）**：只加两命令文件 + logic-protocol 旧名注 + 迁面向人文档（README/HUMAN_GUIDE/capabilities），引擎正文密集交叉引用保留散文（避免 71 处大改 + 撞车风险）。二者都不改算法，差别在活文档要不要全域一致。
3. **一迭代做完两命令 + `/dangerous` 空参语义**：倾向**一个迭代 ITER-0050 做完 loop+dangerous**、收口即整体收 MILE-0005（同 R2 一迭代落 3 命令的先例）。`/butler:dangerous` 空参 = **开启（走引擎 §3 风险闸）** / `off` 关 / `status` 只读回声——**与 preference 空参=只读回声有意不同**（dangerous 的 bare 已被引擎定义为开启，薄壳不擅改）；`/butler:loop` 空参 = 开启闭环、无 off。若你想把 loop、dangerous 拆两迭代分开切版，或想让 dangerous 的 bare 也走「只读回声、要 on 才开」更保守姿态，可在此否掉。
