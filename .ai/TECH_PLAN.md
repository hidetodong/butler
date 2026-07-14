# TECH_PLAN — ITER-0050（MILE-0005 R4 收官落 /butler:loop + /butler:dangerous）

> 标准模式，P2 AC_LIST 经用户 ACK（三默认全收：MINOR→v2.10.0 / `/loop`·`/dangerous` 全迁外科式〔排除 harness-`/loop`〕/ 一迭代做完两命令 + dangerous 空参=开启）。无危险横幅。里程碑收官迭代。

# Goal

套薄壳范本落两个高风险命令 `/butler:loop`（收敛闭环死磕）+ `/butler:dangerous`（无人值守自治）。**唯一新面是风险闸**——命令化不得降低「郑重显式触发」门槛：薄壳不复述护栏（守 DRY），改用 frontmatter ⚠️ + 第 0 步前置风险提醒 + 把真正的闸交回引擎。收口即整体收 MILE-0005。

# Files

- **新增**：`.claude/commands/butler/loop.md`（近乎无参）+ `dangerous.md`（on/off/status 分派 + 风险闸委托）。
- **改·迁触发名**（`/loop`·`/dangerous`→`/butler:*`，命令名非算法；斜杠前缀已把命令引用与 `dangerous:` 字段名 / `Dangerous` 目录名天然隔开）——见 DD4 全清单（**22 文件**）。
- **改·文档**：`.ai/project/capabilities.md` 补两行、`README.md` 扩展模式表 + `butler/` 子树 + Coder 目录 `55/65` 行（与迁触发名合并处理）。
- **发布层**：`VERSION`、`CHANGELOG.md`、`migrations/v2.10.0.md`。
- **里程碑收官层**：`deliveries/milestones/MILE-0005-*.md`（聚合交付）、`.ai/milestones/MILE-0005/MILESTONE.md`（归档）、`MILESTONES.md`（active→closed）。
- **不碰（守边界）**：`templates/**`（含 `rule-card.md`、`templates/preference/profile.md`——**部署面故意保留 `/loop`·`/dangerous` 散文**，见 DD7）、`setup.sh`、四件套 schema 结构、hook、两引擎 §algorithm、`local-constraints-schema` 的 `dangerous:` 字段定义、其他命令。

# Interface（两命令路由设计）

**`/butler:loop`** — frontmatter `description` 带 ⚠️「高强度死磕、长时、消耗大」；`argument-hint "[留空=开启收敛闭环死磕（跑到全绿或熔断）]"`。第 0 步优雅降级（没接 butler → 一句话说清 loop 是 butler P4 升档能力、需先装）。无参数分派——空参=委托 `convergence-loop-engine.md`（§3 闭环 / §6 定量熔断）开启；多余参数→一句提示 loop 无子命令。**不复述闭环 / 熔断算法**。

**`/butler:dangerous`** — frontmatter `description` 带 ⚠️「实验性·无人值守自治·风险高于标准·建议隔离/可回滚环境」；`argument-hint "[留空=开启（走引擎风险闸）| off 关闭 | status 只读看状态]"`。第 0 步优雅降级 + 前置风险提醒。按 `$ARGUMENTS`：

| `$ARGUMENTS` | 分支 | 委托真源 |
|---|---|---|
| 空 | 开启（回写 `dangerous: on` + 对话层显式回声进入 + 承接 announce-on-read 语义） | §3 激活 + §3.1 + §7 护栏 |
| `off` | 关闭（回写 `dangerous: off` + 回声退出） | §3 关闭 |
| `status` | 只读回声当前 `dangerous` 开关态（读 `.ai/local-constraints.md`，**不改开关**） | §3 状态 + local-constraints-schema §4.1 |
| 其它未知 | 兜底列合法参数（留空 / `off` / `status`），不瞎猜执行 | — |

**风险闸交回引擎、不复述护栏**（审计日志 §7.1 / checkpoint §7.2 / P5 强制完整审查 §7.3 一律委托，不在薄壳重写）。

# State

无运行时状态。命令是静态 Markdown 薄壳；`$ARGUMENTS` 由 Claude Code 注入。`/butler:loop` 无持久态（一次性 P4 升档）；`/butler:dangerous` 的持久开关落**当前项目** `.ai/local-constraints.md`「Butler 功能开关」`dangerous`（命令委托引擎读写、自身不落盘、不改字段 schema），跨会话由引擎 §3.1 announce-on-read 承接。两命令随 R1 `~/.claude/commands/butler` 目录软链自动全局可达。

# Design Decisions

- **DD1（严格套范本）**：两命令逐段对齐 `preference.md`/`review.md` 骨架——frontmatter 说人话 → 薄壳三件事声明 + DRY 红线 → 跨 cwd 路径约定段 → 第 0 步优雅降级 → 路由 → 收尾。→ AC5
- **DD2（真源锚点真实）**：委托带具体 section 号——loop §3/§6、dangerous §3/§3.1/§7（写前已读两引擎核实这些节存在）。→ AC2/AC5
- **DD3（风险闸设计·本迭代脊柱）**：命令化不降门槛靠三招，均可核——① 两命令 frontmatter `description` 带显式 ⚠️（菜单可见）；② 第 0 步前置风险提醒（dangerous=实验性/无人值守/建议隔离环境、loop=高强度/长时/消耗大）；③ **闸交回引擎、不复述**——薄壳不重写确认对话/护栏/熔断算法（守 DRY），也不省风险提醒（不降门槛）。这是薄壳纪律与「郑重触发」门槛的共存点。→ AC2
- **DD4（触发名迁移面·一次列全 22 文件，杜绝漏数）**：`/loop`·`/dangerous` 作命令引用处全迁 `/butler:*`。斜杠前缀天然只命中命令引用（`dangerous:` 字段名、`65_Extension_Dangerous` 目录名无斜杠或大写 D，不误命中）。清单——
  - **引擎/规则（Coder/）**：`00_System_Prompt/logic-protocol.md`（§89 loop / §92 dangerous 激活行 + 加旧名注）、`55_Extension_ConvergenceLoop/convergence-loop-engine.md`、`65_Extension_Dangerous/dangerous-engine.md`（**除 §21 harness-`/loop`**，DD5）、`60_Extension_CodeReview/review-engine.md`、`70_Extension_Preference/preference-probe-engine.md`、`Coder/README.md`、`30_Quality_Gate/correction-contract.md`、`30_Quality_Gate/testing-strategy.md`、`62_Extension_Agents/independent-review.md`、`20_Workflow_Lifecycle/{lifecycle,local-constraints-schema,human-test-bridge,verify-schema,iteration-schema,mcv-deployment,acceptance-schema}.md`。
  - **面向人 + digest**：`README.md`、`HUMAN_GUIDE.md`、`.ai/project/{architecture,capabilities,frontier,constraints}.md`。
  - 迁法同 R3 二次替换但更简：`/dangerous` 无撞名、无既存 `/butler:dangerous`，可全域 `s#/dangerous#/butler:dangerous#`（`off` 参数随后原样保留）；`/loop` 须排除 harness 行（DD5）。→ AC4
- **DD5（harness-`/loop` 撞车排除·R4 独有）**：`dangerous-engine.md:21`「Claude Code 的 `/loop`、后台任务」指 **harness 级** loop（非 butler 收敛闭环），**保留不迁**；执行时对每处 `/loop` 核上下文是否 harness 语境（专项核对）。→ AC4
- **DD6（区分命令名 vs 非命令·不误迁）**：`dangerous: on|off`（local-constraints **字段名**）、`preference-*.sh`/`*-engine.md`（文件名）、`65_Extension_Dangerous`（目录名）一律不动——斜杠前缀已隔开，只迁 `/loop`·`/dangerous` 斜杠命令引用。→ AC4/AC6
- **DD7（templates 部署面故意保留·守边界）**：`templates/rule-card.md`、`templates/preference/profile.md` 的 `/loop`·`/dangerous` **不迁**。理由同 R3 DD5：命令是靠全局软链的**个人工具、不下发目标项目**；目标项目靠散文旧名兜底（logic-protocol 保留旧名识别）。迁 templates 会破边界 + 触发 `[regen-claude]`。→ AC6
- **DD8（dangerous 空参=开启·loop 无参数）**：`/butler:dangerous` 空参=开启（走引擎 §3 回声闸），**与 preference 空参=只读回声有意不同**——引擎 §3 已定义 bare `/dangerous`=开启，薄壳擅改成 no-op 是发明语义；`status` 提供只读看态的安全入口。`/butler:loop` 无参数分派（一次性升档、无子命令、无 off）是真实结构差异（良性），非漏写。→ AC3/AC5
- **DD9（MINOR→v2.10.0 + 迁移配方 + 里程碑收官）**：纯新增 2 命令、无破坏面 → MINOR；`v2.9.0`→`v2.10.0`（**十进位，非 2.1.0**）；配方部署面 `[no-op]`+`[restamp]`。R4 收口后整体收 MILE-0005（聚合交付 + 归档 MILESTONE + MILESTONES active→closed）。→ AC9
- **DD10（不动 setup.sh）**：R1 目录软链托管全套，靠 AC8 隔离 HOME 实跑证明两新命令自动可达（这次 8 命令）。→ AC8

# Execution Steps

- [ ] T1 写 `butler/loop.md`（frontmatter ⚠️ + 第0步风险提醒 + 无参委托 §3/§6 不复述）→ AC1/AC2/AC5
- [ ] T2 写 `butler/dangerous.md`（frontmatter ⚠️ + 第0步风险提醒 + 空/off/status/未知 分派 + 闸交回 §3/§3.1/§7 不复述）→ AC1/AC2/AC3/AC5
- [ ] T3 迁 `/dangerous`→`/butler:dangerous`（22 文件全域，除 templates）→ AC4
- [ ] T4 迁 `/loop`→`/butler:loop`（12 文件，**排除 dangerous-engine.md:21 harness-`/loop`**，逐处核上下文）→ AC4/DD5
- [ ] T5 logic-protocol §89/§92 加「旧名 `/loop`·`/dangerous` 仍识别」注（照 §93 preference 范本）→ AC4
- [ ] T6 capabilities 补两行 + README 扩展模式表两行迁 + `butler/` 子树补两命令 + Coder 目录 `55/65` 行迁 → AC7
- [ ] T7 全仓 grep `/loop`·`/dangerous` 核残留（templates + 文件名 + harness-`/loop` + 历史归档 + 本迭代规划稿 除外）+ 专项核 harness-`/loop` 仍在 → AC4
- [ ] T8 写 `migrations/v2.10.0.md`（`[no-op]`+`[restamp]`）+ 切版三载体（VERSION→2.10.0 + CHANGELOG 顶条 MINOR）→ AC9
- [ ] T9 隔离 HOME 实跑 setup.sh 验 8 命令经目录软链可达 + 范式一致性人读核 + `git diff --stat` 边界守恒 → AC1/AC6/AC8

# Verification

- 结构核：读两命令核薄壳要点齐 + 风险闸三招（frontmatter ⚠️ / 第0步风险提醒 / 闸交回引擎不复述）+ dangerous 四路径 + 真源 loop §3/§6、dangerous §3/§3.1/§7 锚点回引擎逐一核（无捏造）。
- 隔离 HOME 实跑 `setup.sh` → `test -e` 两新命令 + 报 8 命令。
- grep `/loop`·`/dangerous` 活文档无残留裸命令名（templates + 文件名 + **harness-`/loop`** + 历史归档 + 规划稿 除外）；专项核 dangerous-engine.md:21 harness-`/loop` 仍在。
- `git diff --stat` 边界守恒（templates/schema结构/hook/setup.sh/两引擎算法 未动）。
- P5 标准复核（自评 + objective 实跑）；迁移面 22 文件最宽 + harness 撞车，P5 专盯触发名残留普查 + harness 保留正确性 + 风险闸三招齐；如发现存疑再升格独立复核。

# Risks

- 命令菜单可见性 headless 不可实敲——沿用 R1–R3 代理验法。
- **迁移面 22 文件最宽 + harness-`/loop` 撞车是本迭代最大出错点**：DD4 清单一次列全 + DD5 撞车排除 + T4 逐处核上下文 + T7 grep 兜底 + 专项核 harness 仍在。**计划-实际提示**：ACK 口径「71 处」实测分布 22 文件（多为 SOP-core schema 交叉引用），全迁是 ACK 的「命名空间统一」意图落实、非范围外扩张——VERIFY_REPORT 显著记录实际面。
- 「命令化不降门槛」是本迭代成败点——DD3 三招写成 AC2 可核检查点；若某招缺失即 AC2 不过。
- dangerous 空参=开启（走引擎闸）与 preference 空参=只读回声的有意不同——VERIFY_REPORT 记录此设计分歧（引擎 §3 已定义 bare=开启）。
