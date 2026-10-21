# butler 命令命名空间地基：一套 `/butler:xxx` 命令的起点，`/butler-prd` 干净迁成 `/butler:prd`

> ITER-0047 · MILE-0005 R1（里程碑首个迭代、里程碑仍进行中）· 收口 2026-07-14 · dogfood butler 自身 · ⚠️ 危险模式自治（P2 用户 ACK，P3 起自审门 + P5 升格独立复核）· 判 MINOR·聚合切 v2.7.0（个人命令层 `[rename]`、目标项目部署面 `[no-op]`）

## 本次交付目标

- butler 的命令长期停在「一个真命令 + 一堆散文触发词」：ITER-0044 落了第一个真命令文件 `/butler-prd`（连字符扁平命名），ITER-0045 打通全局软链让它在所有项目可用。但整套 butler 能力（`/milestone`、`/review`、`/loop`、`/dangerous` 等）仍只是规则正文里的暗号，补全菜单里看不见；且扁平通用名全局装易和别的插件撞名。
- 本次搭起 **`/butler:xxx` 命名空间体系的地基**（MILE-0005 第一步）：新建 `.claude/commands/butler/` 命名空间目录（Claude Code 里子目录＝冒号前缀，`butler/<name>.md`→`/butler:<name>`），把 `/butler-prd` 破坏性迁成 `/butler:prd`，改 `setup.sh` 让整个命名空间目录随一条软链全局可用，并落第一个新命令 `/butler:review` 证明「薄壳路由器」范式在命名空间下可复制——为后续 R2–R4 批量加命令铺好骨架与迁移范本。

## 已完成内容

- **新建命名空间目录 `.claude/commands/butler/`**：子目录名即冒号前缀。`butler:` 前缀天然隔离撞名——全局安装通用名（`/review`、`/loop`）不再和别的插件/用户自定义命令冲突。
- **`/butler-prd` 破坏性迁成 `/butler:prd`**：`git mv .claude/commands/butler-prd.md → butler/prd.md`，**正文 byte-identical 零改**（三分支路由 留空/贴 PRD=首切·`update`=改版·`status`=只读看板 一字未动；原文本就从不自称命令名，故无需改自称）。旧全局软链 `~/.claude/commands/butler-prd.md` 由 `setup.sh` 迁移清理段兜底删除。
- **新落 `/butler:review`（纯薄壳路由器范本）**：命名空间第二个成员，也是后续命令的复制样板。只做三件事——把对的规则读进上下文、按 `$ARGUMENTS` 分派、委托真源不复述算法（守 DRY）：默认（留空）→ 当前上下文快速自检（`review-engine §5`）；`independent` → 另起干净子 agent 独立复核（`independent-review` + `overview §3`，验证者≠作者）。第 0 步先判「当前项目有没有接 butler」，没接就优雅提示而非报错。
- **`setup.sh` 软链改造**：从「逐个软链 `.claude/commands/*.md`」改为 **`ln -sfn` 软链整个 `butler/` 命名空间目录 → `~/.claude/commands/butler`**——一条目录软链托管全套，butler 仓里加/改命令即全局生效、无需重跑。含**迁移清理段**（`-L` 判定只删旧扁平软链 `butler-prd.md`、绝不误删用户自放的真文件）+ `-n` 防 `butler/butler` 套娃 + 命令计数提示。
- **4 处活文档引用更新**：`README.md`（目录树重构出 `butler/` 子树含 prd+review）、`HUMAN_GUIDE.md`（软链描述改命名空间目录）、`.ai/project/capabilities.md`（命令名+路径+setup 机制句）、`.ai/project/frontier.md`（版本史/战线/下一步 3 处）。历史「原名 `/butler-prd`」陈述与 setup.sh 迁移清理代码合法保留旧名；冻结归档（`deliveries/**`、`.ai/iterations/**`、既有 `migrations/`、CHANGELOG 旧条目）一律不动。
- **迁移配方 + 切版**：`migrations/v2.7.0.md`（个人命令层 `[rename]` + 部署面 `[no-op]`+`[restamp]` + `[global-install]` 机器动作）；VERSION 2.6.1→2.7.0、CHANGELOG 顶条 `[2.7.0]`（判 MINOR）。

## 关键变更 / 用户可感知变化

- **命令改名**：`/butler-prd` 停用、改敲 `/butler:prd`（路由行为一字未改）。重跑一次 `./scripts/setup.sh` 即完成切换（自动清旧软链 + 装命名空间目录软链）；若跳过重跑仍敲旧名会找不到命令——重跑即好。
- **多了个 `/butler:review`**：给当前迭代的改动做复核——默认当前上下文快速自检，或 `/butler:review independent` 另起干净上下文做更狠的独立复核（验证者≠作者）。
- **以后加命令更省事**：`setup.sh` 现在软链整个 `butler/` 目录，butler 仓里往 `butler/` 丢一个新 `.md`，它就自动在所有项目全局可用，无需再动分发、无需重跑 setup。
- **对已部署项目**：目标项目 `.ai/` 结构零变化（命令是个人工具、不下发、不进 `templates/`）；要拿到新命名空间命令，做一个**机器级动作**——重跑 `./scripts/setup.sh`。

## 高层影响范围

- 新增（命令层）：`.claude/commands/butler/`（目录）、`.claude/commands/butler/review.md`。
- 改名（命令层）：`.claude/commands/butler-prd.md` → `butler/prd.md`（`git mv`、正文零改）。
- 改（分发装法）：`scripts/setup.sh`（§3 目录软链 + 迁移清理段 + 收尾提示）。
- 改（活文档）：`README.md`、`HUMAN_GUIDE.md`、`.ai/project/capabilities.md`、`.ai/project/frontier.md`。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.6.1→2.7.0、`CHANGELOG.md` 顶条、`migrations/v2.7.0.md`。
- 没碰（守最小影响面 / AC8 边界守恒）：任何 `Coder/**` 规则算法与状态机、`templates/**`、四件套 schema、`templates/hooks/**`、核心 P1–P5——`git diff dc6fa11 --stat` 核清。

## 验证方式与结果摘要

- **8 项验收（AC1–AC8）全过**，`auto·可靠`为主 + 结构核/人读：
  - **隔离假 HOME 实跑 `setup.sh` ×3 场景（旧软链迁移 / 幂等重跑 / 全新装）16/16 断言全绿**：旧扁平软链清理、用户自放真文件不误删、`~/.claude/commands/butler` 指向仓库命名空间目录、prd+review 经软链可达、无 `butler/butler` 套娃、重跑退出 0 指向不变（AC4）。
  - `git show dc6fa11:...butler-prd.md` 与现 `butler/prd.md` **byte-identical**（AC3）；`butler/` 目录 + prd+review 在、旧文件已删（AC1）。
  - 活文档 grep `butler-prd` 仅剩合法处（「原名」历史陈述 + setup.sh 迁移清理代码）（AC2）；`review.md` 薄壳四要点齐、真源 section 锚点逐字对上（AC5）；`migrations/v2.7.0.md` 标签齐（AC6）；VERSION/CHANGELOG/migration 三载体一致（AC7）；`git diff --stat` 无越界（AC8）。
- **P5 升格独立复核（危险模式 §7.3）**：起 fresh-context 子 agent（验证者≠实现者），spec-only 逐 AC + **自写隔离 HOME 压测 18/18** + byte-level diff + 全树对抗 grep + 真源锚点逐一核。结论 **confirm 8 / refute 0 / 0 Must Fix / 0 Should Fix**，可收口；3 Nice-to-Have（`[rename]` 标签措辞、tag 发布补打、argument-hint 可更白话）均不阻断。

## 已知剩余风险 / 延后事项

- **命令菜单「可见性」无法在 headless 实敲**：用「文件/软链存在 + 命名空间结构正确 + 经软链可达」作可靠代理（命名空间机制经 claude-code-guide 查证 + 隔离 HOME 实跑，同 ITER-0044 验法）。真正在菜单里可见需在**主检出**重跑 `setup.sh`（本机动作，migration 写清）。
- **本机改名切换跨机器不自动传播**：旧软链清理与新命名空间软链都是本机动作；换机器重跑一次 `setup.sh` 即到位。
- **MILE-0005 仍进行中**：本迭代只交付 R1 地基；R2（批量补 milestone/upgrade/ideation）、R3（preference 子命令）、R4（loop/dangerous 加风险闸）待后续迭代，设计未锁、不擅自连跑。
- **危险模式自治交付披露**：本迭代 P3 起由自审门替代 ACK、自主执行到收口；P5 已升格独立复核兜底（0 Must Fix）。审计轨迹见 `.ai/RUN_LOG.md` ITER-0047。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0047/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 命令：`.claude/commands/butler/prd.md`（迁自 `butler-prd.md`）、`.claude/commands/butler/review.md`（新）
- 分发装法：`scripts/setup.sh`（§3 命名空间目录软链 + 迁移清理）
- 文档：`README.md`、`HUMAN_GUIDE.md`（§3 安装）、`.ai/project/capabilities.md` / `frontier.md`
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.7.0]`）、`migrations/v2.7.0.md`
- 里程碑：`.ai/MILESTONE.md`（MILE-0005 §5.3 路线图 R1）
- 危险模式审计：`.ai/RUN_LOG.md`（ITER-0047 段）
