# TECH_PLAN — ITER-0049（MILE-0005 R3 落最宽参数命令 /butler:preference）

> 标准模式，P2 AC_LIST 经用户 ACK（三默认全收：MINOR / `/preference` 全迁 `/butler:preference` 含用户可见文案 / 空参采纳只读状态回声）。无危险横幅。

# Goal

套薄壳范本落 `/butler:preference`——全批参数面最宽的命令。把偏好探针 4 子命令 + 空参只读回声用一个薄壳分派清楚、覆盖全路径、委托 `preference-probe-engine` 真源不复述算法、收尾回声状态。验证薄壳范本能吃下二级嵌套参数。

# Files

- **新增**：`.claude/commands/butler/preference.md`（薄壳，含二级参数分派）。
- **改·迁触发名**（`/preference`→`/butler:preference`，命令名非算法）——见 DD3 全清单：
  - `Coder/70_Extension_Preference/preference-probe-engine.md`（引擎，§2.2/§2.3 表/§2.4/§2.5/§4.1/§7/§8/§10 作命令引用处 + §2.3 表主行加旧名注）
  - `Coder/00_System_Prompt/logic-protocol.md`（Preference Mode 激活行）
  - `Coder/20_Workflow_Lifecycle/local-constraints-schema.md`（`/preference off` 全局开关引用）
  - `Coder/65_Extension_Dangerous/dangerous-engine.md`（§与 Preference 关系标题）
  - `Coder/README.md`（命令清单行）
  - `HUMAN_GUIDE.md`（Preference 行 + §偏好探针小节命令引用）
  - `README.md`（能力表 + 目录树注释）
  - `.ai/project/architecture.md` / `capabilities.md` / `frontier.md`（digest）
- **改·文档**：`.ai/project/capabilities.md` 命令表 `/preference` 行转换、`README.md` 目录树补 preference.md（与上条 capabilities/README 迁触发名合并处理）。
- **发布层**：`VERSION`、`CHANGELOG.md`、`migrations/vX.Y.Z.md`。
- **不碰（守边界）**：`templates/**`（含 `rule-card.md`、`templates/preference/*`——**部署面故意保留 `/preference`**，见 DD5）、`preference-init.sh`、`setup.sh`、四件套 schema、hook、引擎 §1/§3–§10 算法、`local-constraints` 开关语义、其他命令。

# Interface（preference 的二级参数路由设计）

frontmatter：`description` 偏好探针开关说人话、`argument-hint "[留空=看当前状态 | on/off 隐私总开关 | reback on/off 反哺 | distill 手动蒸馏]"`。

第 0 步优雅降级：说清「实验性能力 + 数据外置 `$PREF`（`$BUTLER_PREF` 或 `~/.butler/preferences/`）+ 开关全局、不强依赖当前项目 `.ai/`」；butler 不可达（读不到引擎）才提示。

按 `$ARGUMENTS` 首 token 路由（**二级**：首 token=`reback` 时再读第二 token）：

| `$ARGUMENTS` | 分支 | 委托真源 |
|---|---|---|
| 空 | 只读状态回声（读 `$PREF/config.md` consent + reback 态 + 本项目 `preference` 抑制态），**不写** | §2.3 状态回声精神 + §4.2 存储布局（只读） |
| `on` / `off` | 隐私总开关（`on` 首次触发 §2.4 一次性同意协议，委托不复述） | §2.3 + §2.4 |
| `reback on` / `reback off` | 影响回路开关（默认关） | §2.2 + §7 |
| `distill` | 手动蒸馏 + 维护（§8 安全边界触发） | §6 |
| `reback`（裸·无第二 token） | 兜底：回声当前 reback 态 + 提示补 `on`/`off`，**不误动开关** | §2.2 |
| 其它未知 | 优雅提示合法参数集，不瞎猜执行 | — |

收尾：任何开关变更**当回合回声当前状态**（§2.3 硬要求）。

# State

无运行时状态。命令是静态 Markdown 薄壳；`$ARGUMENTS` 由 Claude Code 注入；偏好数据全在外置 `$PREF`、命令只委托引擎读写、自身不落盘。新命令随 R1 `~/.claude/commands/butler` 目录软链自动全局可达。

# Design Decisions

- **DD1（严格套范本）**：逐段对齐 `prd.md`/`milestone.md` 骨架——frontmatter 两行说人话 → 薄壳三件事声明 + DRY 红线 → 跨 cwd 路径约定段 → 第 0 步优雅降级 → `$ARGUMENTS` 路由 → 收尾回声。→ AC4
- **DD2（真源锚点真实）**：每处委托带具体 section 号（§2.2/§2.3/§2.4/§6/§7/§8），写前已 grep 核对引擎确有该节。→ AC2/AC4
- **DD3（触发名迁移面·一次列全，杜绝 R2 DD3 漏数）**：`/preference` 作**命令引用**处全迁 `/butler:preference`，清单 = 引擎（8 处：§2.2:32、§2.3:38-40 表、§2.4:48/50、§2.5:57、§4.1:87、§7:176、§8:189、§10:218）+ logic-protocol:93 + local-constraints-schema:66 + dangerous-engine:155 + Coder/README:146 + HUMAN_GUIDE（152/218/224/225/226/233 等命令引用）+ README:81/138 + architecture:24/38 + capabilities:26 + frontier:20。§2.3 表主行加「旧名 `/preference`」注。保留「偏好 / 记住这条」自然语言触发。→ AC3
- **DD4（区分命令名 vs 非命令引用·不误迁）**：`preference-init.sh`（脚本名）、`preference-probe-engine.md`（文件名）、`$PREF/`·`~/.butler/preferences/`（路径）、`preference: on|off`（local-constraints **字段名**，非命令）一律**不动**——只迁前有斜杠、作 slash 命令用的 `/preference`。→ AC3/AC6
- **DD5（templates 部署面故意保留 `/preference`·守边界）**：`templates/rule-card.md:70`、`templates/preference/README.md:5`、`templates/preference/config.md:11` 的 `/preference` **不迁**。理由：`/butler:preference` 是靠全局软链的**个人命令、不下发目标项目**；目标项目里保证生效的是散文 `/preference`（logic-protocol 迁后仍认作旧名触发）。迁 templates 会破坏「命令不下发目标项目」边界 + 触发 `[regen-claude]` 波及每个已部署项目 + 违反 ACK 的「不碰 templates」。故 templates 保留是**边界守恒的刻意排除**，非残留。→ AC6
- **DD6（空参只读默认·薄壳新增）**：引擎命令面无空参定义；薄壳给空参加「只读回声 consent/reback/本项目抑制态」默认，纯读不写、与 milestone/review 只读默认同构。→ AC2/AC5
- **DD7（不动 setup.sh）**：R1 目录软链托管全套，靠 AC8 隔离 HOME 实跑证明新命令自动可达（这次 6 命令）。→ AC8
- **DD8（MINOR + 迁移配方）**：纯新增 1 命令、无破坏面 → MINOR；配方部署面 `[no-op]`+`[restamp]`。→ AC9

# Execution Steps

- [ ] T1 写 `butler/preference.md`（6 路径 + 裸 reback 兜底 + 未知参数兜底 + 收尾回声）→ AC1/AC2/AC4/AC5
- [ ] T2 迁引擎 `preference-probe-engine.md` 8 处命令引用 → `/butler:preference` + §2.3 表加旧名注 → AC3
- [ ] T3 迁其余活文档命令引用（logic-protocol / local-constraints-schema / dangerous-engine / Coder README / HUMAN_GUIDE / README / architecture / frontier）→ AC3
- [ ] T4 capabilities 命令表 `/preference` 行转换为 `/butler:preference` 一等入口 + README 目录树补 preference.md → AC7
- [ ] T5 全仓 grep `/preference` 核无残留裸命令名（templates 部署面 + 脚本/文件/路径/字段名 + 历史归档 + 本迭代规划稿 除外）→ AC3
- [ ] T6 写 `migrations/vX.Y.Z.md`（`[no-op]`+`[restamp]`）→ AC9
- [ ] T7 切版三载体（VERSION bump + CHANGELOG 顶条 MINOR）→ AC9
- [ ] T8 隔离 HOME 实跑 setup.sh 验 6 命令经目录软链可达 + 范式一致性人读核 + `git diff --stat` 边界守恒 → AC4/AC6/AC8

# Verification

- 结构核：读 preference.md 核薄壳四要点齐 + 6 路径全覆盖 + 二级 reback 分派 + 真源 §2.2/§2.3/§2.4/§6/§7 锚点回引擎逐一核（无捏造）。
- 隔离 HOME 实跑 `setup.sh` → `test -e ~/.claude/commands/butler/preference.md` + 报 6 命令。
- grep `/preference` 活文档无残留裸命令名（DP5 templates + DD4 非命令 + 历史归档 + 规划稿 除外）。
- `git diff --stat` 边界守恒（templates/schema/hook/setup.sh/引擎算法 未动）。
- P5 标准复核（自评 + objective 实跑）；迁移面比 R2 宽，P5 专盯触发名残留普查 + templates 保留正确性；如发现存疑再升格独立复核。

# Risks

- 命令菜单可见性 headless 不可实敲——沿用 R1/R2 代理验法。
- **迁移面宽（~10 文件）是本迭代最大出错点**：DD3 清单一次列全 + T5 grep 兜底；DD4/DD5 划清「不迁」边界防误伤 templates 与非命令引用。
- `reback` 二级参数是分派最易漏点——Interface 路由表 + AC2 路径清单专盯裸 reback 兜底。
- 引擎迁后 §2.3 说 `/butler:preference`、templates 部署面仍 `/preference`：靠 logic-protocol 保留旧名识别兜底，两处**不矛盾**（旧名仍触发），VERIFY_REPORT 显著记录此边界。
