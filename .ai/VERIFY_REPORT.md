# VERIFY_REPORT — ITER-0050（`/butler:loop` + `/butler:dangerous` 两个高风险命令 · MILE-0005 R4 收官）

> 标准模式：P2 AC_LIST 经用户 ACK（三默认全收——MINOR→v2.10.0 / `/loop`·`/dangerous` 全迁外科式〔排除 harness-`/loop`〕/ 一迭代做完两命令 + dangerous 空参=开启）。风险集中两点：① **风险闸**——命令化不得降低「郑重显式触发」门槛（本迭代成败点）；② **触发名迁移面 22 文件最宽 + `/loop` 与 Claude Code 自带撞名**。其余为复制 R1–R3 已验薄壳范式。P5 走标准复核（自评 + 客观隔离 HOME 实跑 + 全仓残留普查 + 路径腐蚀专项守卫），未升格强制独立复核——两风险点均已定向验证（风险闸三招逐条核、迁移双轮普查 + harness 保留专项核 + 路径腐蚀守卫）、无 shaky 处、不触发升格。

# Verification Summary
- 覆盖：新建两薄壳命令 `loop.md`（一次性 P4 升档、无持久态/无 off、近乎无参）+ `dangerous.md`（空/off/status 分派 + 风险闸委托）套 R1 范本；`/loop`·`/dangerous`→`/butler:*` 全仓活文档迁移（22 文件，含全批最宽迁移面）；`templates/` **刻意保留**旧名；`/loop` 与 Claude Code 自带 `/loop` **撞名的 harness 引用精确保留** + 加注澄清；capabilities 两行升级为一等入口 + README 扩展模式表/子树/Coder 目录；`migrations/v2.10.0.md`（`[no-op]`+`[restamp]`）；MINOR 切版三载体 → **v2.10.0**（十进位）；**MILE-0005 里程碑收官**。
- 总体结论：**AC1–AC9 全过**。P4 实测：隔离假 HOME 实跑 `setup.sh`（exit 0）**8/8 命令经目录软链可达**、无套娃；`git diff` 边界守恒（`templates/` 与 `scripts/setup.sh` 零改，两引擎仅触发名行改动、算法零改）；真源锚点（loop §3/§6、dangerous §3/§3.1/§7）逐一回引擎核无捏造；`/loop`·`/dangerous` 全仓残留普查零裸旧命令名 + harness-`/loop` 保留。
- **计划-实际差异 1 处（记录·非缺陷）**：ACK 口径「71 处」，实测触发名分布 **22 文件**（`/dangerous` 22 + `/loop` 12，多为 SOP-core schema 交叉引用）。已按 TECH_PLAN DD4 上前枚举全集迁移、按 DD7 刻意留 templates——差异是 ACK 口径按「occurrence 数」表述、实际按「文件数」看更宽，仍在 ACK 的「全迁外科式·命名空间统一」意图内，非范围外扩张（全迁正是用户选 full over conservative 的原意）。
- **良性内容增补 1 处（记录·非算法）**：`dangerous-engine.md:21` harness-`/loop` 除保留不迁外，**加了一句澄清注**「harness 自带的循环，非 butler 的收敛闭环命令 `/butler:loop`」——自文档化防未来误迁，是有益增补非算法变更。

# AC Status（道 + 置信档）
- [x] **AC1（两命令成立·可达）**(auto·可靠)：`.claude/commands/butler/loop.md` + `dangerous.md` 建立；命名空间映射结构正确；隔离 HOME 实跑 `setup.sh`（exit 0）经目录软链 `test -e` 报 **8 个 /butler:* 命令**（prd/review/milestone/upgrade/ideation/preference/loop/dangerous）全绿、无 `butler/butler` 套娃。
- [x] **AC2（风险闸·本迭代脊柱）**(人读三招核)：命令化不降门槛，三招齐——① 两命令 frontmatter `description` 均带显式 ⚠️（loop=「高强度·长时·消耗大、郑重触发」、dangerous=「实验性·风险显著高于标准、建议隔离/可回滚环境」，菜单可见）；② 第 0 步前置风险提醒（loop 点明高强度升档/耗时/消耗大、dangerous 点明实验性/无人值守/建议隔离环境）；③ **闸交回引擎、不复述**——loop 委托 §3/§4 闭环 + §6 定量熔断、dangerous 委托 §3 回声 + §3.1 announce-on-read + §7 护栏（审计/checkpoint/P5 强制完整审查），薄壳**不重写**确认对话/护栏/熔断算法（守 DRY），也**不省**风险提醒（不降门槛）。
- [x] **AC3（参数分派）**(人读路径清单核)：`/butler:dangerous`——空参→开启（回写 `dangerous: on` + §3 对话层回声 + §7 护栏）、`off`→关闭（§3）、`status`→只读回声当前开关态（读 `.ai/local-constraints.md`，**不改开关**）、未知参数→兜底列合法参数不瞎猜；**空参=开启与 preference 空参=只读回声有意不同**（引擎 §3 已定义 bare=开启，薄壳不擅改）。`/butler:loop`——空参→开启闭环（无 off、无持久态），多余参数→一句提示无子命令。
- [x] **AC4（触发名迁移 + harness 撞车排除）**(auto·可靠)：`/loop`·`/dangerous` 作命令引用处全迁 `/butler:*`（22 文件）；**路径腐蚀守卫**：负向前瞻 `(?!-)` 保护 `/dangerous-engine.md` 路径引用不被误迁（专项 grep `butler:dangerous-engine`=0）；**harness-`/loop` 专项保留**：`dangerous-engine.md:21` 的 Claude Code 自带 `/loop` 仍为裸 `/loop` + 加澄清注；logic-protocol §89/§92 加旧名注；全仓活文档普查零裸旧命令名（文件名引用 + harness-`/loop` + templates 刻意保留 + 历史归档 除外）；分隔符假阳性（`loop/dangerous` 类）专项 grep 已清零。
- [x] **AC5（范式一致性）**(人读同构核 + auto 锚点核)：两命令与 `prd.md`/`review.md`/`preference.md` 同构——① 薄壳声明 + DRY 红线 ✓；② 跨 cwd 路径约定段 ✓；③ 第 0 步优雅降级（没接 butler → 一句话说清、不报错不空跑；dangerous 另有「无 `.ai/` → 提示先部署」）✓；④ frontmatter 说人话（带 ⚠️）✓；⑤ 委托锚点 loop §3/§6、dangerous §3/§3.1/§7 回引擎核**真实存在**、零捏造 ✓。**良性差异如实**：`loop` 无参数分派（一次性升档、无子命令、无 off）是真实结构差异，非漏写。
- [x] **AC6（边界守恒）**(auto·可靠)：两引擎 `convergence-loop-engine.md`/`dangerous-engine.md` 仅触发名行改动（`git diff` 逐行核：convergence 3 行 = §scope/§2/§8 的 `/loop`；dangerous 8 行 = scope/announce 示例/岔口/关系等 `/dangerous` + §152 `/loop` + §21 harness 加注），**算法（闭环/熔断/自治/自审门/护栏）零改**；`local-constraints-schema` 的 `dangerous:` 字段定义、`scripts/setup.sh`、`templates/**`、四件套 schema、hook、其他命令**一行未动**（`git diff --stat -- templates/` 与 `-- scripts/setup.sh` 均空）。
- [x] **AC7（文档更新）**(auto + 人读)：`capabilities.md` 命令表把 `/butler:loop`·`/butler:dangerous` 两行**升级**为一等入口（真源指命令文件 + 引擎章节、注风险闸/参数/持久态）；`README.md` 扩展模式表两行迁 `/butler:*` + `butler/` 子树补两命令（带 ⚠️、`└──` 收尾正确）+ Coder 目录 `55/65` 行迁。
- [x] **AC8（目录软链自动托管·实跑）**(auto·可靠)：隔离假 HOME 实跑 `setup.sh`（exit 0），两新命令经目录软链 `test -e` 通过、R1–R3 的 6 命令仍可达（**8/8**）、**未改 `setup.sh` 一行**、无套娃——续验 R1「整目录软链」红利（这次 8 命令）。
- [x] **AC9（切版三载体对齐）**(auto·可靠)：判 **MINOR → v2.10.0**（纯新增 2 命令、无破坏面）；`VERSION`=2.10.0、`CHANGELOG.md` 顶条 `[2.10.0] - 2026-07-14`、`migrations/v2.10.0.md` 区间 `v2.9.0→v2.10.0` 三者一致；git tag v2.10.0 于发布提交时打（见 Handoff）；migration 对部署面 `[no-op]`+`[restamp]`。**里程碑收官**——本版收口后 MILE-0005 整体收（聚合交付 + 归档 + MILESTONES active→closed）。

# Verification Results
- AC1/AC8：隔离假 HOME `HOME=<tmp> bash scripts/setup.sh`（exit 0）——目录软链 8 命令 `test -e` 全绿、无套娃。
- AC2/AC3/AC5：读两命令核风险闸三招 + dangerous 四路径 + loop 无参兜底；委托锚点 loop §3/§6、dangerous §3/§3.1/§7 回引擎逐一真实存在。
- AC4：`perl -i -pe 's#/dangerous(?!-)#...#'`（负向前瞻护路径）+ `/loop` 逐文件（排除 dangerous-engine.md，其 §152 手迁、§21 harness 手留加注）；`grep` 普查残留全合法（templates 刻意保留 / 文件名 / harness-`/loop` / 历史归档 / 规划稿）；专项 grep `butler:dangerous-engine`=0（路径未腐蚀）、`[A-Za-z0-9]/butler:`=0（无分隔符假阳性）、harness-`/loop` 仍在。
- AC6：`git diff --stat` 24 改 + 3 新（2 命令 + migration）；两引擎 diff 逐行核仅触发名 + harness 加注、算法零改；`-- templates/`、`-- scripts/setup.sh` 均空。
- AC7：读 capabilities 两行（已升级为一等入口）+ README（扩展模式表 + `butler/` 子树 8 命令齐 + Coder 目录已迁）。
- AC9：`cat VERSION`=2.10.0、CHANGELOG 顶条 `[2.10.0] - 2026-07-14`、`migrations/v2.10.0.md` 首行区间 `v2.9.0 → v2.10.0` 一致。

# Gate Coverage
- 通用质量门禁：不破坏分层（命令层改动不入 `Coder/` 算法、不入 `templates/`）✓ / 两新命令 README 目录树注册（无隐式依赖）✓ / 文件名互引不写绝对路径 ✓ / frontmatter 说人话（带 ⚠️ 风险标记）✓ / 产物链未动 ✓。
- Active Profiles：无（规则仓，未命中 domain profile）。
- Tech Plan Alignment：DD1/DD2/DD3/DD5/DD6/DD8/DD9/DD10 全兑现；**DD4 计划-实际差异**：ACK 口径「71 occurrence」实测分布 22 文件（多为 SOP-core schema 交叉引用），已按 DD4 上前枚举全集迁移；**DD7 边界刻意执行**：`templates/rule-card.md`、`templates/preference/profile.md` 的 `/loop`·`/dangerous` **保留不迁**（命令不下发目标项目、目标项目靠散文旧名兜底、logic-protocol 保留旧名识别），迁 templates 会破边界 + 触发 `[regen-claude]`。T1–T9 全落。
- References Compliance：N/A（无外部参考资料）。

# Independent Review（标准模式·未升格）
- 本迭代主体为复制 R1–R3 已验薄壳范式 + 触发名字符串迁移 + 幂等切版，两处真实新面——**风险闸「命令化不降门槛」** 与 **22 文件最宽迁移面 + harness 撞车**——均已定向复核（AC2 风险闸三招逐条核、AC4 双轮普查 + 路径腐蚀守卫 + harness 保留专项核 + 分隔符假阳性清零）。P5 自评 + 客观隔离 HOME 实跑无 shaky 处，按标准模式**不强制**独立复核。里程碑收官，无后续路线项遗留。

# Remaining Risks
- 命令菜单「可见性」headless 不可实敲——沿用 R1–R3 代理验法（文件存在 + 命名空间结构正确 + 经目录软链可达 + `setup.sh` exit 0）。
- **引擎/文档说 `/butler:*`、templates 保留 `/loop`·`/dangerous` 的双名并存**：靠 logic-protocol §89/§92 保留旧名识别接住（自然语言触发「死磕 / 放手做」+ 旧名散文触发照常）。目标项目侧规则卡文案不变、旧名仍工作；风险已由 DD7 决策 + migration 说明覆盖，非缺陷。
- **`/butler:loop` 与 Claude Code 自带 `/loop` 的用户心智撞名**：命令层用 `/butler:loop` 消歧、dangerous-engine.md:21 加注澄清；但用户敲 `/loop` 时命中的是 harness 自带循环、敲 `/butler:loop` 才是 butler 收敛闭环——此为 Claude Code 命名空间机制的固有现象，非本迭代缺陷，已在引擎注明。
- **两命令运行时行为未新验**：命令只落触发入口、未改引擎算法，收敛闭环/无人值守自治的端到端运行时行为由两引擎既有实现保证（本迭代未新验其运行时行为，`/butler:upgrade`/`/dangerous` 端到端历史欠债见 `debt.md` 仍悬）。

# Handoff / Next Step
- P5 通过（AC1–AC9 全过、0 阻断项）→ 进原子收口五步（归档四件套 + 交付 md/html + 台账/路线图 + 知识文件夹前滚 + 收口自检）+ **里程碑收官**（聚合 MILE-0005 交付 + 归档 MILESTONE + MILESTONES active→closed）+ 切版 git 仪式（feat 提交 + 独立 chore(release) 提交 + 本地 tag v2.10.0）。
- **MILE-0005 达成即整体收口**（R1–R4 全落、`/butler:*` 命名空间 8 命令齐）。标准模式授权范围：ACK 的 R4 scope 一路推到收口 + 里程碑收官 + 提交 + 推分支 + PR #3 增长（应转 ready 或标注可合并）；**不合并 main、不推 tag v2.10.0 到远端**（待用户授权）。
