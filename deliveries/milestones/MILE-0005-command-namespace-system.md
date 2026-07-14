# butler 命令命名空间系统：散文触发词收敛成一整套 `/butler:*` 真实 slash 命令（MILE-0005）

> MILE-0005 · 里程碑交付（跨版本聚合）· 收口 2026-07-14 · 逐迭代各自切版 v2.7.0 → v2.8.0 → v2.9.0 → v2.10.0（每项均 **MINOR·向后兼容能力新增**，末项 v2.10.0 收官）· 含迭代 ITER-0047 / ITER-0048 / ITER-0049 / ITER-0050

## 本次交付目标

- 一条主线，补 butler 长期停在「散文触发词」的缺口。缺口有三层：① 规则正文里 `/milestone`、`/review`、`/dangerous`、`/loop`、`/preference` 等到处当暗号被引用，但**只有 `/butler-prd` 一个真实命令文件**，其余在补全菜单里零存在感——用户看不见、记不住、敲不出来；② 全局安装用通用名（`/milestone`、`/review`、`/loop`）**易与别的插件 / 用户自定义命令撞名**；③ 没有统一命名空间，命令能力零成体系。
- 里程碑目标：把整套 butler 能力都获得**一等命令入口**——`.claude/commands/butler/` 子目录＝Claude Code 的 `/butler:<name>` 命名空间（冒号是真实调用分隔符），`butler:` 前缀天然隔离撞名，`setup.sh` 一条目录软链托管全套、**任意项目补全菜单可见可用**、加命令自动全局生效。全部走**薄壳路由器**范式（只做三件事：把对的规则读进上下文、按 `$ARGUMENTS` 分派、委托真源不复述算法），**不改任何 `Coder/**` 规则算法、不下发目标项目**（个人工具边界沿用 ITER-0044）。因全是新增能力（命名空间目录 + 8 命令 + 目录软链），按 semver 逐项属 **MINOR**。

## 已完成内容

- 四个路线项（R1~R4）一条主线闭环，逐项见下方回填表。链路顺序：**地基 + prd 迁移 + 首命令验证（R1）→ 批量补低风险纯薄壳命令（R2）→ 最宽参数命令〔二级嵌套参数〕（R3）→ 高风险命令加风险闸〔收官〕（R4）**。全程复用同一薄壳路由器范本，逐轮抬升复杂度证明范式够用：R1 立范本、R2 证批量可复制、R3 证吃得下二级嵌套参数、R4 证扛得住风险闸——无平行机制。

## 关键变更 / 用户可感知变化

- **命名空间地基 + `/butler-prd` 破坏性迁入**（R1）：建 `.claude/commands/butler/` 子目录；`/butler-prd`（连字符、v2.4.0 发布）`git mv` 迁成 `butler/prd.md`→`/butler:prd`（`[rename]` 配方 + 清旧全局软链 + 正文引用更新）；`setup.sh` 从「逐文件软链 `*.md`」改为**软链整个 `butler/` 目录**——一条目录软链管全套、butler 仓加命令自动全局生效、无需重跑 setup。同轮落 `/butler:review` 验证范本可复制。
- **批量补三个低风险纯薄壳命令**（R2）：`/butler:milestone`（+`status` 参数，里程碑录入 / 只读看板）、`/butler:upgrade`（已部署项目按 `migrations/` 区间幂等升级，原 `/butler-upgrade` 一并迁触发名）、`/butler:ideation`（模糊需求脑暴收敛）。各含「没接 butler 优雅降级」+ 跨 cwd 路径约定段。隔离 HOME 实跑坐实 R1 目录软链自动托管（5/5 可达、`setup.sh` 未改一行）。
- **最宽参数命令 `/butler:preference`**（R3）：一个薄壳吃下全批**参数面最宽**的能力——`on`/`off`（隐私总开关）、`reback on|off`（影响回路开关，全批**唯一二级嵌套参数**：首 token 是 `reback` 才读第二 token）、`distill`（手动蒸馏）、空参=只读状态回声（薄壳新增默认，与 milestone status/review 同构）。委托 `preference-probe-engine` 真源不复述同意协议/采集蒸馏/安全底线。证明薄壳范式吃得下二级嵌套参数。
- **高风险命令加风险闸〔收官〕**（R4）：`/butler:loop`（收敛闭环死磕，无参 / 无持久态 / 无 off，跑到全绿或定量熔断）+ `/butler:dangerous`（无人值守自治，空=开启 / off / status 只读，持久态外化 `.ai/local-constraints.md`、跨会话）。**唯一新面是风险闸**——命令化不得降低「郑重、显式触发」门槛，做法定为三招：① frontmatter 描述带显式 ⚠️（菜单里一眼见风险）+ ② 第 0 步前置风险提醒 + ③ 把真正的闸交回引擎（薄壳不复述护栏、守 DRY，也不省风险提醒、门槛不降）。`/butler:loop` 与 Claude Code 自带 `/loop` 靠命名空间前缀消歧、harness 引用精确保留加注。
- **散文触发名成体系迁移**：R1–R4 逐轮把活规则/人读文档里作命令引用的旧名（`/butler-prd`、`/butler-upgrade`、`/preference`、`/loop`、`/dangerous`）迁成 `/butler:*`，并在 `logic-protocol` 保留旧名识别——旧名与自然语言触发照常工作、新名是命名空间一等入口。
- **对不装/不用的人无感**：命令是靠全局软链的个人工具，**不进 `templates/`、不下发目标项目、目标项目 `.ai/` 部署面零变化**（逐迭代 `[no-op]`+`[restamp]`）；规则卡文案里的旧名原样保留、仍工作。

## 高层影响范围

- 新增（命令层·8 个薄壳命令）：`.claude/commands/butler/` 下 `prd`（迁入）/ `review` / `milestone` / `upgrade` / `ideation` / `preference` / `loop` / `dangerous`。
- 改（分发）：`scripts/setup.sh`（R1 一次性改成目录软链，此后 R2–R4 未再动一行——新命令自动托管）。
- 改（活文档·触发名迁移，仅命令引用非算法）：两引擎（`convergence-loop-engine` / `dangerous-engine`）、`logic-protocol`、`preference-probe-engine`、`review-engine`、多份 `20_Workflow_Lifecycle` schema、`Coder/README`、`HUMAN_GUIDE`、`README`、`.ai/project/*` digest。
- 改（文档·命令表/目录树）：`.ai/project/capabilities.md`（命令表逐轮转换为 `/butler:*` 一等入口）、`README.md`（`butler/` 子树 8 命令 + 扩展模式表 + Coder 目录）。
- 未动（守里程碑 Out of Scope）：**所有 `Coder/**` 规则算法**（薄壳只路由、委托既有真源；两引擎的闭环/熔断/自治/自审门/护栏算法一字未改）、`templates/**`（含 `rule-card`、`preference/` 刻意保留旧名）、四件套 schema 结构、`templates/hooks/**`、harness 级 `/loop`（精确保留）。逐迭代 `git diff --stat -- templates/` 均空。
- 发布层：逐迭代独立 chore(release) 提交 + 本地 tag（v2.7.0/v2.8.0/v2.9.0/v2.10.0）+ 各自 `migrations/vX.Y.Z.md`（均部署面 `[no-op]`+`[restamp]`）。

## 拆分路线图回填

| 路线项 | 主题 | 实际 ITER | 状态 | 切版 | 落点 |
|---|---|---|---|---|---|
| R1 | 命名空间地基 + `/butler-prd`→`/butler:prd` 迁移 + `setup.sh` 目录软链 + 首命令 `/butler:review` 验证范本 | ITER-0047 | ✅ closed | v2.7.0 | `deliveries/ITER-0047-command-namespace-foundation.md` |
| R2 | 批量补低风险纯薄壳命令 `/butler:milestone`（+status）/`upgrade`/`ideation` | ITER-0048 | ✅ closed | v2.8.0 | `deliveries/ITER-0048-namespace-commands-batch.md` |
| R3 | 最宽参数命令 `/butler:preference`（`on`/`off`/`reback on\|off` 二级嵌套/`distill` + 空参只读回声） | ITER-0049 | ✅ closed | v2.9.0 | `deliveries/ITER-0049-preference-namespace-command.md` |
| R4 | 高风险命令加风险闸 `/butler:loop` + `/butler:dangerous`〔收官〕 | ITER-0050 | ✅ closed | v2.10.0 | `deliveries/ITER-0050-risk-gate-commands.md` |

- 四路线项全部达成。执行顺序 R1 → R2 → R3 → R4（先立地基与范本，再批量复制、抬到二级嵌套参数、末位扛住风险闸收官）。全程单主线、无正交子项、逐轮抬复杂度验证同一范式。

## 验证方式与结果摘要

- 四路线项其下迭代各自 P1–P5 闭环、各自收口交付（见上表链接）、各自 P2 用户 ACK 冻结。R1 走危险模式自治全程 + 独立复核 0 Must Fix；R2–R4 标准模式，两处以上真实新面（批量复制 / 二级嵌套参数 / 风险闸 + 最宽迁移面）均定向复核。
- **命名空间可达性逐轮实跑坐实**：隔离假 HOME 实跑 `setup.sh`（exit 0），命令数从 R1 起逐轮增长、**末轮 R4 达 8/8 命令经目录软链可达、无 `butler/butler` 套娃、`setup.sh` 自 R1 后未改一行**——「往 `butler/` 丢一个薄壳 `.md` 即全局可用」这条红利连续四轮验证。
- **边界守恒逐轮核**：`Coder/**` 规则算法（两引擎逐行 `git diff` 仅触发名 + 1 处 harness 加注）、`templates/**`、`setup.sh`（R2 起）均 `git diff` 为空。
- 里程碑收口前确认 §5.3 路线图 R1–R4 四项全 closed、8 命令齐、一致性自检 6 不变量全绿。

## 已知剩余风险 / 延后事项

- **命令入口已成体系，运行时行为多数未新验**：8 命令的入口都已结构验证 + 经目录软链可达，但命令只是把既有引擎能力摆上菜单、委托真源执行——**未改也未新验引擎运行时行为**。尤其 `/butler:dangerous`（无人值守自治端到端）、`/butler:upgrade`（真实老项目端到端升级）两笔历史欠债仍悬（见 `debt.md`），命令化没消除欠债。
- **命令菜单「可见性」headless 不可实敲**：全程用代理验法（文件存在 + 命名空间结构正确 + 经目录软链可达 + `setup.sh` exit 0）。真正菜单可见需在**主检出**跑过 R1 的 `setup.sh`。
- **双名并存（引擎/文档说 `/butler:*`、templates 保留旧名）**：有意分层——靠 `logic-protocol` 保留旧名识别接住，目标项目侧规则卡文案不变、旧名仍工作（逐迭代 DD 决策 + migration 说明覆盖，非缺陷）。
- **`/butler:loop` 与 Claude Code 自带 `/loop` 用户心智撞名**：命令层用 `/butler:loop` 消歧、`dangerous-engine.md:21` 加注澄清，但这是 Claude Code 命名空间机制的固有现象、非缺陷。

## 引用

- 里程碑产物快照：`.ai/milestones/MILE-0005/MILESTONE.md`
- 其下迭代交付：见上方回填表 4 条 `deliveries/ITER-00NN-*.md`
- 发布：`CHANGELOG.md` [2.7.0]/[2.8.0]/[2.9.0]/[2.10.0]、`migrations/v2.7.0.md`~`v2.10.0.md`、`.ai/ITERATIONS.md`、`.ai/MILESTONES.md`
