# `/butler:loop` + `/butler:dangerous` 落地：两个高风险命令的「命令化不降门槛」风险闸——MILE-0005 收官

> ITER-0050 · MILE-0005 R4（里程碑第四也是**收官**迭代，收口即整体收 MILE-0005）· 收口 2026-07-14 · dogfood butler 自身 · 标准模式（P2 用户 ACK 三默认）· 判 MINOR·聚合切 v2.10.0（目标项目部署面 `[no-op]`+`[restamp]`）

## 本次交付目标

- R1（地基）→ R2（批量三命令）→ R3（最宽参数 preference）之后，命名空间里只剩最后两个、也是唯一带风险的能力：**收敛闭环死磕** `/loop`（把 P4 执行升到高强度「执行→探测→反思→修正」死磕到全绿或熔断）与**无人值守长程自治** `/dangerous`（模型自审替人 ACK、自动拆迭代跑完整生命周期）。它俩的独特难点不是参数，而是**风险闸**——把散文暗号做成随手可敲的 slash 命令，**绝不能降低它们「郑重、显式触发」的门槛**（否则等于把高风险能力变成手滑就开）。
- 本次验证一件事：**薄壳范式能不能在「不复述护栏（守 DRY）」与「不降风险门槛」之间两全**。做法定为三招——① frontmatter 描述带显式 ⚠️ 让补全菜单里一眼见风险；② 第 0 步前置一段风险提醒（点明高强度/无人值守/建议隔离环境）；③ **真正的闸交回引擎**（薄壳不重写确认对话/护栏/熔断算法，只把显式意图接进引擎）。R4 收口即整体收 MILE-0005。

## 已完成内容

- **新落 2 个高风险薄壳命令**（结构与 R1–R3 同构：读对规则进上下文 → 按 `$ARGUMENTS` 分派 → 委托真源不复述算法〔守 DRY 红线〕→ 第 0 步优雅降级），但都多戴了风险闸：
  - **`/butler:loop`**——全批**最薄**：一次性 P4 升档，**无持久态、无 `off`**（跑到验证全绿或 §6 定量熔断自然结束），近乎无参（空参=开启、多余参数一句提示无子命令）。委托 `convergence-loop-engine.md` §3 核心逻辑 / §4 闭环程序 / §6 定量熔断。
  - **`/butler:dangerous`**——on/off/status 三路分派：空参→开启（回写 `dangerous: on` + §3 回声 + §7 护栏）、`off`→关闭、`status`→只读回声当前开关态（**不改开关**）、未知参数→兜底列合法参数。状态外化到**当前项目** `.ai/local-constraints.md` 的 `dangerous` 字段、跨会话（§3.1 announce-on-read）。委托 `dangerous-engine.md` §3/§3.1/§7。
- **风险闸三招齐、逐命令核**：两命令 frontmatter 均带显式 ⚠️（loop=「高强度·长时·消耗大·郑重触发」、dangerous=「实验性·风险显著高于标准·建议隔离/可回滚环境」）；第 0 步均前置风险提醒；护栏/确认/熔断算法**一律不在薄壳复述**、交回引擎——薄壳只接显式意图、不省风险提醒（**门槛不降**）也不重写护栏（**守 DRY**）。
- **`/butler:dangerous` 空参=开启，与 preference 空参=只读回声有意不同**：引擎 §3 已定义 bare `/dangerous`=开启，薄壳不擅改语义；这是范式内的**受控差异**、非漏写。
- **旧触发名 `/loop`·`/dangerous` 全仓活文档迁成 `/butler:*`（22 文件）**：两引擎 + `logic-protocol`（§89/§92 加旧名识别注）+ `review-engine`/`preference-probe-engine`/`correction-contract`/`testing-strategy`/`independent-review`/`lifecycle`/`local-constraints-schema`/`human-test-bridge`/`verify-schema`/`iteration-schema`/`mcv-deployment`/`acceptance-schema`/`Coder/README`/`HUMAN_GUIDE`/`README` + 项目 digest。迁移用负向前瞻 `(?!-)` 保护 `/dangerous-engine.md` 路径引用不被腐蚀。
- **`/loop` 与 Claude Code 自带 `/loop` 撞名精确处理**：`dangerous-engine.md:21` 引用的是 **harness 级** `/loop`（Claude Code 自带循环、非 butler 收敛闭环），**保留裸 `/loop` 不迁**并加澄清注——不会被误读成 `/butler:loop`。
- **刻意不碰 `templates/` 部署面**：`templates/rule-card.md`、`templates/preference/*` 里的 `/loop`·`/dangerous` **保留不迁**——命令是靠全局软链的个人工具、不下发目标项目，目标项目里保证生效的是散文旧名（迁后 logic-protocol 仍认作旧名触发）。迁 templates 会破边界 + 触发 `[regen-claude]`、违反 ACK。
- **文档更新**：`capabilities.md` 命令表把 `/butler:loop`·`/butler:dangerous` 两行从「指引擎」**升级**为一等入口（真源指命令文件 + 引擎章节、注风险闸/参数/持久态）；`README.md` `butler/` 子树补两命令（带 ⚠️）+ 扩展模式表 + Coder 目录 `55/65` 行迁。
- **迁移配方 + 切版**：`migrations/v2.10.0.md`（部署面 `[no-op]`+`[restamp]`；新命令由 R1 目录软链自动托管、无需重跑 setup.sh、触发名迁移不碰 templates 故无 `[regen-claude]`、harness-`/loop` 精确保留）；VERSION 2.9.0→2.10.0、CHANGELOG 顶条 `[2.10.0]`（判 MINOR）。

## 关键变更 / 用户可感知变化

- **多了两个命令**：`/butler:loop`（留空=开启收敛闭环死磕，无 off、跑到全绿或熔断自然结束）、`/butler:dangerous`（留空=开启无人值守自治、`off` 关、`status` 只看状态）。补全菜单里两条描述都带 ⚠️、一眼见风险。
- **`/loop`·`/dangerous` 改敲 `/butler:*`**：路由行为一字未改（闭环/熔断/自治/自审门/护栏算法引擎里没动），只是换了命名空间触发名并加了风险闸包装；旧名 `/loop`·`/dangerous` 与「死磕 / 放手做」自然语言触发照常识别。
- **`/butler:loop` 与你熟的 Claude Code `/loop` 不是一回事**：敲 `/loop` 命中的是 harness 自带循环、敲 `/butler:loop` 才是 butler 收敛闭环——命名空间前缀天然消歧，引擎里也加了注。
- **无需任何安装动作就能用**：R1 已把整个命令目录软链进全局，这两个新命令**自动**在所有项目可用。**唯一例外**：从没跑过 R1 的 setup.sh 就补跑一次。
- **对已部署项目**：`.ai/` 结构零变化，规则卡文案里的 `/loop`·`/dangerous` 也原样不变、旧名仍工作（命令是个人工具、不下发）。

## 高层影响范围

- 新增（命令层）：`.claude/commands/butler/loop.md`、`.claude/commands/butler/dangerous.md`。
- 改（活文档·触发名 22 文件，仅命令引用非算法）：两引擎（`convergence-loop-engine.md` 3 行、`dangerous-engine.md` 8 行含 harness-`/loop` 保留加注）、`logic-protocol.md`（§89/§92 + 旧名注）、`review-engine`/`preference-probe-engine`/`correction-contract`/`testing-strategy`/`independent-review`/`lifecycle`/`local-constraints-schema`/`human-test-bridge`/`verify-schema`/`iteration-schema`/`mcv-deployment`/`acceptance-schema`/`Coder/README`/`HUMAN_GUIDE`/`.ai/project/{architecture,constraints}`。
- 改（活文档·命令表/目录树/前滚）：`.ai/project/capabilities.md`（行升级）、`README.md`（子树补两命令 + 扩展模式表 + Coder 目录）、`.ai/project/frontier.md`（前滚 v2.10.0/8 命令/里程碑收口）。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.9.0→2.10.0、`CHANGELOG.md` 顶条、`migrations/v2.10.0.md`。
- 没碰（守最小影响面 / AC6 边界守恒）：两引擎**算法**（§3/§4/§6 闭环熔断、§3/§4/§5/§7 自治/自审门/护栏）、`local-constraints-schema` 的 `dangerous:` 字段管辖、`templates/**`（含 `rule-card.md`、`preference/` 刻意保留旧名）、四件套 schema、`templates/hooks/**`、**`setup.sh`（R1 目录软链已托管，一行未动）**、harness-`/loop`（`dangerous-engine.md:21` 精确保留）——`git diff --stat -- templates/` 与 `-- scripts/setup.sh` 均空。

## 验证方式与结果摘要

- **9 项验收（AC1–AC9）全过**，`auto·可靠`为主 + 结构核/人读三招核：
  - **隔离假 HOME 实跑 `setup.sh`（exit 0）8/8 命令经目录软链可达**：两新命令 loop/dangerous + R1–R3 的 prd/review/milestone/upgrade/ideation/preference 全部 `test -e` 通过、无 `butler/butler` 套娃、**`setup.sh` 未改一行**——续验 R1 目录软链红利（这次 8 命令）（AC1/AC8）。
  - **风险闸三招逐命令核**（AC2·本迭代脊柱）：frontmatter ⚠️ 可见 + 第 0 步风险提醒 + 闸交回引擎不复述——三招齐、门槛不降、DRY 不破。
  - **参数分派逐路径核**（AC3）：dangerous 空/off/status/未知四路 + loop 空/多余二路，委托锚点 loop §3/§6、dangerous §3/§3.1/§7 回引擎**逐一真实存在**、零捏造。
  - **触发名迁移双轮普查 + 专项守卫**（AC4）：`/loop`·`/dangerous` 全仓活文档残留**零裸旧命令名**（templates 刻意保留 / 文件名引用 / harness-`/loop` / 历史归档 均合法）；路径腐蚀专项 grep `butler:dangerous-engine`=0；分隔符假阳性 `[A-Za-z0-9]/butler:`=0；harness-`/loop` 仍在且加注。
  - 两引擎 `git diff` 逐行核**仅触发名 + 1 处 harness 加注、算法零改**（AC6）；capabilities 两行升级、README 子树 8 命令齐（AC7）；VERSION/CHANGELOG/migration 三载体一致 v2.10.0（AC9）。
- **标准模式复核**：两处真实新面——风险闸「命令化不降门槛」、22 文件最宽迁移面 + harness 撞名——均已定向复核（AC2 三招逐条、AC4 双轮普查 + 路径守卫 + harness 保留专项核）。P5 自评 + 客观隔离 HOME 实跑无 shaky 处，未升格强制独立复核。

## 已知剩余风险 / 延后事项

- **计划-实际差异 1 处（已记 VERIFY_REPORT）**：ACK 口径「71 处」，实测触发名分布 22 文件（多为 SOP-core schema 交叉引用）；已按 TECH_PLAN DD4 上前枚举全集迁移、按 DD7 刻意留 templates，差异为 ACK 口径按 occurrence 数表述、实际按文件数看更宽，仍在「全迁外科式·命名空间统一」ACK 意图内、非范围外扩张。
- **良性内容增补 1 处（非算法）**：`dangerous-engine.md:21` harness-`/loop` 除保留不迁外加了句澄清注，自文档化防未来误迁。
- **双名并存（引擎说 `/butler:*`、templates 保留旧名）**：靠 logic-protocol §89/§92 保留旧名识别接住，目标项目侧规则卡文案不变、旧名仍工作（DD7 决策 + migration 说明覆盖，非缺陷）。
- **命令菜单「可见性」headless 不可实敲**：沿用 R1–R3 代理验法（文件存在 + 命名空间结构正确 + 经目录软链可达 + `setup.sh` exit 0）。真正菜单可见需在**主检出**跑过 R1 的 setup.sh。
- **两命令运行时行为未新验**：命令只落触发入口、未改引擎算法，收敛闭环死磕 / 无人值守自治的端到端运行时行为由两引擎既有实现保证；`/butler:dangerous` 端到端从未真跑的历史欠债见 `debt.md` 仍悬。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0050/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 命令（新）：`.claude/commands/butler/loop.md` / `.claude/commands/butler/dangerous.md`
- 触发名迁移（22 文件）：两引擎 `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md` / `Coder/65_Extension_Dangerous/dangerous-engine.md`、`Coder/00_System_Prompt/logic-protocol.md`（§89/§92）等——详见归档 `CHANGELOG.md`
- 文档：`.ai/project/capabilities.md`（命令表）、`README.md`（`butler/` 子树 8 命令 + 扩展模式表）、`.ai/project/frontier.md`（前滚）
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.10.0]`）、`migrations/v2.10.0.md`
- 里程碑：`.ai/MILESTONE.md`（MILE-0005 §5.3 路线图 R4·收官）、`deliveries/milestones/MILE-0005-command-namespace-system.md`（聚合交付）
