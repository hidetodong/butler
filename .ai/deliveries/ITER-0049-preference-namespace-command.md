# `/butler:preference` 落地：一个薄壳吃下全批最宽的参数面（含唯一的二级嵌套参数）

> ITER-0049 · MILE-0005 R3（里程碑第三个迭代、里程碑仍进行中）· 收口 2026-07-14 · dogfood butler 自身 · 标准模式（P2 用户 ACK 三默认）· 判 MINOR·聚合切 v2.9.0（目标项目部署面 `[no-op]`+`[restamp]`）

## 本次交付目标

- R1（ITER-0047）打地基、R2（ITER-0048）批量铺开三个**扁平参数**命令后，命名空间里还剩一个真正难啃的：偏好探针 `/preference`——它是全批**参数面最宽**的能力（`on`/`off` 隐私总开关、`reback on|off` 反哺开关、`distill` 手动蒸馏），其中 `reback on|off` 是全批**唯一的二级嵌套参数**（先看第一个词是不是 `reback`，是才再读第二个词 `on`/`off`）。R2 的命令全是 0–1 层扁平分支，这是把它单独拆成一个迭代的原因。
- 本次照 R1/R2 的**薄壳路由器**范本落 `/butler:preference`，验证一件事：**同一套薄壳范式能不能吃下二级嵌套参数**——不新造能力，只把散文暗号 `/preference` 落成命名空间真命令、覆盖全路径、委托引擎真源不复述算法。同时把活规则与人读文档里作命令引用的旧名 `/preference` 统一迁成 `/butler:preference`。

## 已完成内容

- **新落 1 个薄壳命令 `/butler:preference`**（结构与 R1/R2 同构：读对规则进上下文 → 按 `$ARGUMENTS` 分派 → 委托真源不复述算法〔守 DRY 红线〕→ 第 0 步优雅降级），委托 `preference-probe-engine.md`，**六条路径**全覆盖：
  - **空参** → 只读状态回声（读外置 `$PREF/config.md` 的 consent + reback 态 + 本项目抑制态，**纯读不写**）——薄壳新增的默认档，与 `/butler:milestone status`、`/butler:review` 的只读默认同构。
  - **`on` / `off`** → §2.3 隐私总开关（首次 `on` 触发 §2.4 一次性同意协议，委托引擎披露、不复述）。
  - **`reback on` / `reback off`** → §2.2/§7 影响回路开关（**二级嵌套参数**：第一个词是 `reback` 才再读第二个词）。反哺默认关、仅作用于有监督工作。
  - **`distill`** → §6 手动蒸馏（§8 安全边界）。
  - **裸 `reback`（缺第二个词）** → 兜底回声当前反哺态 + 提示补 `on`/`off`，**不误开关**。
  - **未知参数** → 兜底列出合法参数集、不瞎猜执行。
  收尾按引擎 §2.3 硬要求当回合回声当前状态。
- **旧触发名 `/preference` 全仓活文档迁成 `/butler:preference`**：引擎 `preference-probe-engine.md` 作命令引用的 11 处（含 §2.4 同意披露给用户看的「怎么关」文案）+ `logic-protocol.md`、`local-constraints-schema.md`、`dangerous-engine.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、`README.md`、项目 digest。引擎 §2.3 命令表主行加「旧名 `/preference` 仍作触发被识别、留空=只读回声」注；保留「记住这条偏好 / 学我的取舍」等自然语言触发。
- **刻意不碰 `templates/` 部署面**：`templates/rule-card.md`、`templates/preference/*` 里的 `/preference` **保留不迁**——`/butler:preference` 是靠全局软链的个人命令、不下发目标项目，目标项目里保证生效的是散文旧名（迁后 logic-protocol 仍认作旧名触发）。迁 templates 会破「命令不下发目标项目」边界、触发 `[regen-claude]`、违反 ACK 的「不碰 templates」。
- **文档更新**：`capabilities.md` 命令表把 `/preference` 行**转换**为 `/butler:preference` 一等入口（注参数面最宽·唯一二级参数·只管全局层开关，本项目抑制开关走 `local-constraints`）；`README.md` `butler/` 子树补 `preference.md` + 扩展模式表 + Coder 目录行迁。
- **迁移配方 + 切版**：`migrations/v2.9.0.md`（部署面 `[no-op]`+`[restamp]`；点明新命令由 R1 目录软链自动托管、无需重跑 setup.sh、触发名迁移不碰 templates 故无 `[regen-claude]`）；VERSION 2.8.0→2.9.0、CHANGELOG 顶条 `[2.9.0]`（判 MINOR）。

## 关键变更 / 用户可感知变化

- **多了一个命令**：`/butler:preference`——留空看当前状态、`on`/`off` 开关隐私总闸、`reback on|off` 开关反哺、`distill` 手动蒸馏。
- **`/preference` 改敲 `/butler:preference`**：路由行为一字未改（采集/蒸馏/反哺/安全底线算法引擎里没动），只是换了命名空间触发名；旧名 `/preference` 与「记住这条偏好」自然语言触发照常识别。
- **留空不再是「没用法」而是「看状态」**：敲 `/butler:preference` 不带参数，会只读回声当前同意态 / 反哺开关 / 本项目抑制态，纯读不写。
- **无需任何安装动作就能用**：R1 已把整个命令目录软链进全局，这个新命令**自动**在所有项目可用。**唯一例外**：从没跑过 R1 的 setup.sh 就补跑一次。
- **对已部署项目**：`.ai/` 结构零变化，规则卡文案里的 `/preference` 也原样不变、旧名仍工作（命令是个人工具、不下发）。

## 高层影响范围

- 新增（命令层）：`.claude/commands/butler/preference.md`。
- 改（活文档·触发名）：`Coder/70_Extension_Preference/preference-probe-engine.md`（§2.x·11 处，算法未动）、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、`.ai/project/architecture.md`、`.ai/project/frontier.md`。
- 改（活文档·命令表/目录树）：`.ai/project/capabilities.md`（行转换）、`README.md`（子树补命令 + 扩展模式表 + Coder 目录）。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.8.0→2.9.0、`CHANGELOG.md` 顶条、`migrations/v2.9.0.md`。
- 没碰（守最小影响面 / AC6 边界守恒）：引擎 §1、§3–§10 **算法**、`local-constraints-schema` 的 `preference:` 字段管辖、`templates/**`（含 `preference/`、`rule-card.md` 刻意保留 `/preference`）、`preference-init.sh`、四件套 schema、`templates/hooks/**`、**`setup.sh`（R1 目录软链已托管，一行未动）**——`git diff --stat -- templates/` 与 `-- scripts/setup.sh` 均空。

## 验证方式与结果摘要

- **9 项验收（AC1–AC9）全过**，`auto·可靠`为主 + 结构核/人读：
  - **隔离假 HOME 实跑 `setup.sh`（exit 0）6/6 命令经目录软链可达**：新命令 preference + R1/R2 的 prd/review/milestone/upgrade/ideation 全部 `test -e` 通过、目录软链指向仓库命名空间目录、无 `butler/butler` 套娃、**`setup.sh` 未改一行**——续验 R1 目录软链红利（AC1/AC8）。
  - 薄壳六要点齐（薄壳声明 + DRY / 跨 cwd 路径约定段 / 第 0 步降级 / frontmatter 说人话 / `$ARGUMENTS` 含二级嵌套路由 / 委托锚点），**六条路径 + 裸 reback 兜底 + 未知参数**逐条核「有分支 + 委托对的 §」；委托的真源 §2.2/§2.3/§2.4/§6/§7 回引擎**逐一真实存在**、零捏造（AC2/AC4/AC5）。
  - `/preference` 全仓活文档残留普查**零裸旧命令名**（`templates/` 刻意保留 / `~/.butler/preferences/` 存储路径 / 命令表旧名注 / 本迭代规划稿 / 历史归档 均合法）（AC3）；capabilities 行已转换、README 子树 6 命令齐（AC7）；VERSION/CHANGELOG/migration 三载体一致（AC9）；`git diff --stat` 无越界（AC6）。
- **标准模式复核**：两处真实新面——`reback` 二级嵌套参数分派、比 R2 宽的迁移面——均已定向复核（AC2 路径清单逐条核 `reback` 分派、T5+P5 双轮普查清残留）。P5 自评 + 客观隔离 HOME 实跑无 shaky 处，未升格强制独立复核。

## 已知剩余风险 / 延后事项

- **计划-实际差异 1 处（已记 VERIFY_REPORT）**：ACK 口径「引擎约 7–8 处」，实测触发名分布约 13 处（引擎 11 + 5 份活文档）；已按 TECH_PLAN DD3 上前枚举全集迁移、按 DD5 刻意不碰 templates，差异为 ACK 口径低估分布面、非范围外扩张。
- **引擎说 `/butler:preference`、templates 保留 `/preference` 的双名并存**：有意的分层——靠 logic-protocol 保留旧名识别接住，目标项目侧规则卡文案不变、旧名仍工作（DD5 决策记录 + migration 说明覆盖，非缺陷）。
- **命令菜单「可见性」headless 不可实敲**：沿用 R1/R2 代理验法（文件存在 + 命名空间结构正确 + 经目录软链可达）。真正菜单可见需在**主检出**跑过 R1 的 setup.sh。
- **偏好探针反哺/蒸馏标实验性**：命令只落触发入口、未改引擎算法，运行时行为由引擎 §2/§6/§7 既有实现保证（本迭代未新验其运行时行为）。
- **MILE-0005 仍进行中**：R4（`loop`/`dangerous` 加风险闸）待后续迭代，设计未锁、不擅自连跑。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0049/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 命令（新）：`.claude/commands/butler/preference.md`
- 触发名迁移：`Coder/70_Extension_Preference/preference-probe-engine.md`（§2.x）、`Coder/00_System_Prompt/logic-protocol.md`、`Coder/20_Workflow_Lifecycle/local-constraints-schema.md`、`Coder/65_Extension_Dangerous/dangerous-engine.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、`.ai/project/architecture.md` / `frontier.md`
- 文档：`.ai/project/capabilities.md`（命令表）、`README.md`（`butler/` 子树 + 扩展模式表）
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.9.0]`）、`migrations/v2.9.0.md`
- 里程碑：`.ai/MILESTONE.md`（MILE-0005 §5.3 路线图 R3）
