# 个人沟通风格常开正本：一份 `communication-style.md`，一次 `setup.sh` 让 AI 到处都按你的说话规矩说话

> ITER-0046 · 独立迭代（无所属里程碑）· 收口 2026-07-13 · dogfood butler 自身 · 判 MINOR·聚合切 v2.6.0（全局 @import、目标项目部署面 `[no-op]`）

## 本次交付目标

- 「AI 该怎么跟你说话」的规矩此前**散在两处**：本机 Matrix 输出风格（`~/.claude/output-styles/matrix.md`，只有切到该输出风格才生效）装了整套基调/详略/说人话/结尾块；几个记忆文件又各记一条（话砍到骨头、别抛选择菜单），说人话还和 matrix **各写一份**。散、条件生效、还双写。
- 本次把这套规矩**收敛成一份唯一正本** `communication-style.md`（住 butler 仓根、随 git 跨机器同步），由 `setup.sh` 写一行 `@import` 进全局 `~/.claude/CLAUDE.md`，让它**每个会话、每个项目、每台装了 butler 的机器都常开**——跟切没切某个输出风格无关。Matrix 输出风格作为过渡产物退休。

## 已完成内容

- **新增沟通风格唯一正本 `communication-style.md`（仓根）**：开篇写清定位（唯一正本 / 常开 / 跨机器同步 / 只管说话方式 / 以后反馈往这写），下辖 8 节——基调、详略（含并入的「话砍到骨头」）、抓重点、说人话（术语先解释 / 比喻要落地 / 别让英文变量裸奔 / 别把词掐短，**4 条各带一对 ❌/✅**）、别急着抛选择菜单（**新增**，讨论 + 执行两侧都别甩菜单，带 ❌/✅ 与 grill 例外）、格式、结尾决策块、边界。原 Matrix 7 节措辞逐字保真搬入，只新增两条真增量。
- **`setup.sh` 接上 @import 常开线**：在既有 `<!-- butler-global-config -->` 受管配置块（awk 删旧块 + heredoc 重写、幂等）里加一行 `@$BUTLER_DIR/communication-style.md`。路径用绝对 `$BUTLER_DIR` 展开——随 setup 在每台机器上正确、随 butler 仓走。
- **Matrix 输出风格退休（本机一次性迁移）**：删 `~/.claude/output-styles/matrix.md`；把 `claudep` 启动命令里为启用它加的 `--settings '{"outputStyle":"Matrix"}'` 参数从 fish（`~/.config/fish/config.fish`）与 zsh（`~/.zshrc`）两处都拆掉（保留 `proxyon` + `claude`，`claudep` 退回成纯「开代理起 claude」的启动器）；查 `~/.claude/settings.json` 无 Matrix 残留。
- **三风格记忆掏薄壳**：`style-concise` / `style-plain-language` / `discussion-mode-no-forced-menus` 三个记忆文件的规矩正文删除，只留「哪天因为什么事定的」来龙去脉 + 一句「规矩正文见 `communication-style.md`」；`MEMORY.md` 三条索引同步改；`style-plain-language` 内指向 butler 内部 MILE-0003 的引用原样保留。
- **文档注册**：`README.md`（目录结构树登记正本一行 + 快速上手注释）、`HUMAN_GUIDE.md` §3 安装（「三件事」改「四件事」+ 第 4 条讲清 @import 沟通风格正本）。
- **知识文件夹前滚**：`capabilities.md`（加「个人沟通风格全局常开正本 + setup @import 能力」）、`frontier.md`（刷 v2.6.0、记「沟通风格收敛为单一正本 + 常开」）。

## 关键变更 / 用户可感知变化

- **AI 现在到处都按你的沟通风格说话，且不依赖切输出风格**：重跑一次 `./scripts/setup.sh`，之后任意项目、任意会话，AI 都读同一份 `communication-style.md`——不用再手动切到某个输出风格才生效。
- **想调说话风格，只改一个文件**：改 `communication-style.md` 即全局生效、跨机器同步；不用再在输出风格文件和几个记忆文件之间来回改、也不会两处写拧。
- **换机器只需重跑 setup**：正本随 butler 仓走，新机器装好 butler、跑一次 `setup.sh`，沟通风格即到位。
- **Matrix 输出风格不再需要**：`claudep` 现在就是「开代理起 claude」；风格改由常开的 @import 提供。
- **对已部署项目**：目标项目 `.ai/` 结构零变化（升级配方 `[no-op]`+`[restamp]`）；要拿到常开沟通风格，做一个**机器级动作**——重跑 `./scripts/setup.sh`。

## 高层影响范围

- 新增（仓内正本）：`communication-style.md`（仓根）。
- 改（分发装法）：`scripts/setup.sh`（受管 heredoc +一行 @import）。
- 改（文档注册）：`README.md`、`HUMAN_GUIDE.md`。
- 知识文件夹前滚：`.ai/project/capabilities.md` / `frontier.md`。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.5.0→2.6.0、`CHANGELOG.md` 顶条、`migrations/v2.6.0.md`。
- 本机迁移（**不进仓提交**，是 `~/` 下本机配置）：删 `~/.claude/output-styles/matrix.md`；拆两处 `claudep` 的 `--settings` 参数；掏薄壳三个风格记忆 + 改 `MEMORY.md`。
- 没碰（守最小影响面）：任何 `Coder/**` 规则正文、`templates/**`、四件套 schema、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机、既有「偏好探针」子系统——`git status` 核清。

## 验证方式与结果摘要

- **8 项验收（AC1–AC8）全过**。AC1–AC6 **auto·可靠**、非纸面：
  - 正本 8 节齐、说人话 4 条各带例、别抛菜单节带例、开篇定位在、边界干净无工程规矩混入（AC1）。
  - 隔离 HOME 端到端实跑 `setup.sh`：受管块内 `@…communication-style.md` 行**恒为 1**、**连跑两次仍为 1**（幂等无重复）、退出 0（AC2）；从受管块抽出 `@` 行的绝对路径 `test -f` 为真、指向真实存在的正本（AC3）。
  - 文档注册句在位、说人话（AC4）。
  - **迁移前先逐节核 matrix→正本无遗漏（21 个关键锚点全 ✓）才删**；删后 `matrix.md` 不存在、两处 `claudep` 无 `--settings`/Matrix 残留、`settings.json` 无 Matrix（AC5）；三记忆规矩正文已删、只剩来龙去脉 + 指向正本，`MEMORY.md` 已改，MILE-0003 引用留存（AC6）。
- **AC7/AC8**：`migrations/v2.6.0.md` 就目标项目部署面给 `[no-op]`+`[restamp]` + 机器级重跑 setup 装 @import + 本机一次性清理 matrix/claudep 可选手动步；收口五步齐 + v2.6.0 三载体（`VERSION` == tag `v2.6.0` == `CHANGELOG` 顶条 `## [2.6.0]`）对齐 + feat 与 chore(release) 提交分离。
- **未触发独立复核**：改动是一段幂等 bash（@import 行）+ 一份手写风格正本 + 文档 + 本机配置迁移，无跨多规则契约面 / 哲学底座变更；核心风险（bash 正确性 + 内容不丢）已由隔离实跑与迁移前逐节核验覆盖。

## 已知剩余风险 / 延后事项

- **@import 运行时并入属 Claude Code 行为**：非本仓可断言，验证止于路径绝对正确 + 目标文件存在 + 受管块合法。真正生效需在**主检出**重跑一次 `setup.sh`（本机动作，migration 写清）。
- **本机迁移跨机器不自动传播**：`matrix.md` 与 `claudep` 都是本机配置；换机器若也有旧设置需同样清一遍。但新机器的沟通风格来源已是同步的正本 + @import，本身不依赖 matrix。
- **常驻 token 开销**：正本每会话加载（约 matrix 量级、几百 token）——用户已拍板「带例子换规矩能落地，值」。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0046/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 沟通风格正本：`communication-style.md`
- 分发装法：`scripts/setup.sh`（受管 heredoc 的 @import 行）
- 文档：`README.md`、`HUMAN_GUIDE.md`（§3 安装）
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.6.0]`）、`migrations/v2.6.0.md`
- 本机迁移（不在仓内）：`~/.claude/output-styles/matrix.md`（已删）、`~/.config/fish/config.fish` 与 `~/.zshrc` 的 `claudep`、风格记忆薄壳
