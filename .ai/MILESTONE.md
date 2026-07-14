# MILESTONE — MILE-0005 · butler 命令命名空间系统

> 方向性产物（非冻结、不走 ACK）。把 butler 散落在规则正文里的「散文触发词」（`/milestone`、`/review`、`/loop` 等写在文档里当暗号、却没有真实命令文件的引用）收敛成一整套 `/butler:xxx` 命名空间下的真实 slash command——补全菜单可见、全局任意项目可用、`butler:` 前缀天然隔离撞名。设计共识见本文件 §5.3 各路线项与 §5.4 演进记录；地基事实（子目录＝冒号命名空间、user 级全局同理、frontmatter 照常、软链已实跑验证）经 2026-07-14 claude-code-guide 查证。

## 5.1 范围评估

**In Scope（版本级）**
- **命名空间骨架**：新建 `.claude/commands/butler/` 子目录；Claude Code 按目录自动把 `butler/<name>.md` 映射为 `/butler:<name>`（冒号是真实调用分隔符），一套命令聚成 `/butler:*` 族。
- **8 个真实命令文件**（全部走「薄壳路由器」范式——只做三件事：把对的规则读进上下文、按 `$ARGUMENTS` 分派、委托真源规则执行，不复述算法）：`prd` / `milestone` / `review` / `upgrade` / `preference` / `ideation` / `loop` / `dangerous`。
- **`/butler-prd` 破坏性迁入命名空间**：现有 `.claude/commands/butler-prd.md`（连字符、v2.4.0 发布）改名迁为 `butler/prd.md` → `/butler:prd`；走 `[rename]` 迁移配方 + 清旧全局软链 `~/.claude/commands/butler-prd.md` + 扫更正文/文档里对 `/butler-prd` 的引用。
- **setup.sh 软链改造**：现逻辑「逐个软链 `.claude/commands/*.md`」是扁平的、不进子目录 → 改为**软链整个 `butler/` 目录** → `~/.claude/commands/butler`；一条目录软链管全套，butler 仓里加命令自动全局生效、无需重跑 setup。
- **子命令走参数**：`/butler:preference on|off|reback|distill`、`/butler:milestone status`、`/butler:dangerous on|off` 一律走 `$ARGUMENTS` 路由（同现 `/butler-prd` 处理 `status`/`update` 的范式），**不拆多级命名空间**（避免文件爆炸、背离薄壳）。
- **没接 butler 时优雅降级**：每个命令薄壳统一先判「当前项目是否已部署 butler（有 `.ai/`）」，没接就清晰提示「先部署基地车」而非报错（`/butler-prd` 已有此边界，其余照抄）。
- **高风险命令加闸**：`loop`（死磕闭环）、`dangerous`（无人值守自治）的薄壳保留/前置风险提示与确认，**不照抄低风险命令的轻壳**——命令化不得降低其「郑重显式触发」的门槛。

**Out of Scope（版本级）**
- **不下发到目标项目仓库**（沿用 ITER-0044 边界）：命令是个人工具，全局装在 user 级 `~/.claude/commands/`，**不进 `templates/`、不污染目标项目仓、目标项目升级零影响**。
- **不改真源规则算法**：薄壳只路由，各命令委托的 `Coder/**` 规则正文语义一律不动（本里程碑不重写任何执行规则）。
- **不做团队协作者共享**：把命令拷进项目自身 `.claude/commands/`（project 级、随项目仓走）那条路本版不做，另议。
- **不新造命令能力**：只把既有散文触发词落成真实文件，不发明新命令、不扩既有命令语义。

**关键交付目标**
- 8 个 `/butler:xxx` 命令在**任意项目**补全菜单可见可用（全局软链 + 命名空间保证）；`/butler-prd` 干净迁成 `/butler:prd`、无残留旧软链/旧引用；`setup.sh` 一条目录软链托管全套；薄壳路由器范本固化、可被后续命令复制。

## 5.2 理解阐释

- **核心问题**：butler 的命令长期停在「散文触发词」——规则正文里 `/milestone`（引用 32 次）、`/review`（32）、`/dangerous`（56）等到处当暗号，但只有 `/butler-prd` 一个真实命令文件；其余在补全菜单里零存在感、用户看不见也记不住。且没有统一命名空间，全局安装通用名（`/milestone`、`/review`、`/loop`）易与别的插件 / 用户自定义命令撞名。
- **背景与价值**：ITER-0044 落了第一个真命令 `/butler-prd`、ITER-0045 打通全局软链分发，「薄壳路由器 + 全局安装」模式已实跑验证。现在把它**成体系推广**：整套 butler 能力都获得一等命令入口，`butler:` 前缀隔离撞名，用户在任何项目随手可敲。
- **整体影响判断**：改动集中在**新增文件**（`.claude/commands/butler/` 下 8 个命令）+ `scripts/setup.sh`（软链逻辑）+ `migrations/`（prd 改名配方）+ 正文/文档里对 `/butler-prd` 的引用更新。**不碰 `Coder/**` 任何规则算法**——薄壳只做路由、委托既有真源规则。真新增仅：命名空间目录结构、7 个新薄壳命令、setup.sh 目录软链、prd 破坏性改名迁移。风险点两处：① 破坏性改名要清干净旧软链 + 旧引用；② `loop`/`dangerous` 命令化要加风险闸、不降触发门槛。

## 5.3 拆分路线图

> 路线项扁平原子（一项 ≈ 一迭代），按依赖排序。「实际 ITER」开启时才绑号、现留空（不预先占号）。预计跨度 ITER-0047 ~ ITER-0050（方向性，真源以「实际 ITER」列 + 台账为准）。

| 路线项 | 主题（方向 → 一个迭代） | 实际 ITER | 状态 |
|---|---|---|---|
| **R1** | **命名空间地基 + prd 迁移 + 首个新命令验证**：建 `.claude/commands/butler/` 骨架 + `/butler-prd`→`/butler:prd`（`[rename]` 迁移 + 清旧全局软链 + 正文/文档引用更新）+ 改 `setup.sh` 软链整目录 + 顺带落 `/butler:review`（纯薄壳，验证「薄壳路由器」范式在命名空间下可复制） | ITER-0047 | active |
| **R2** | **批量补低风险纯薄壳命令**：`/butler:milestone`（+ `status` 参数）、`/butler:upgrade`、`/butler:ideation`——三个语义清晰、无风险闸的命令，套 R1 固化的范本批量产出 + 各自「没接 butler 优雅降级」 | — | planned |
| **R3** | **`/butler:preference`（子命令最多）**：`on`/`off`/`reback`/`distill` 四子命令全走 `$ARGUMENTS` 参数路由，委托 `70_Extension_Preference` 真源；单开一迭代因参数面最宽、要把参数分派写扎实 | — | planned |
| **R4** | **高风险命令加闸**：`/butler:loop` + `/butler:dangerous`（含 `on`/`off`）——命令薄壳前置风险提示与确认闸，委托 `55_Extension_ConvergenceLoop` / `65_Extension_Dangerous` 真源；单独设计以确保命令化不降低「郑重显式触发」门槛 | — | planned |

## 5.4 范围演进记录

- 2026-07-14 · 开启 MILE-0005（承 MILE-0004 于 2026-07-09 收口、`current` 为 none，开题闸解除）。方向源自 2026-07-13~14 对话：用户要「一套 `/butler:xxx` 命名空间命令系统」。地基事实经 claude-code-guide 查证：子目录＝冒号命名空间、`~/.claude/commands/butler/` user 级全局同理、多级可嵌套、frontmatter（description/argument-hint/`$ARGUMENTS`）照常、command `.md` 软链已由 ITER-0045 实跑验证可用（故维持 commands 路线、不迁 skills）。已 soft 对齐的关键决策：命令清单 8 个、子命令走参数不拆多级、`loop`/`dangerous` 加风险闸、`/butler-prd` 破坏性改名一并迁入、命令仍不下发目标项目（个人工具边界沿用 ITER-0044）。
