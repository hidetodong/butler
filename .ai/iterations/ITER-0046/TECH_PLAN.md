# TECH_PLAN — ITER-0046（个人沟通风格常开正本 · communication-style.md + setup.sh @import + matrix 退休）

# Goal
- 支撑 AC1–AC8：新建收敛后的沟通风格正本、给 `setup.sh` 接上「@import 正本进全局 CLAUDE.md」这条常开分发线、注册文档、退休 matrix（本机迁移 + 拆 claudep 参数）、掏薄壳记忆、折叠收口、独立切 MINOR v2.6.0。

# Files / Modules to Change
- **`communication-style.md`**（新增，仓根 · 唯一正本）：开篇 `>` 定位块（唯一正本 / 常开 / 跨机器同步 / 只管说话方式 / 反馈往这写）＋ 8 节：`## 基调`（照 matrix 逐字）`## 详略`（照 matrix + 折入「话砍到骨头」：默认往短写、三句能说清不写一段、一表能说清不铺长文、反感凑篇幅的铺垫客套流水账）`## 抓重点`（照 matrix）`## 说人话`（照 matrix，4 条各留一对 ❌/✅）`## 别急着抛选择菜单`（**新增**，并入 discussion-mode-no-forced-menus，含一对 ❌/✅）`## 格式`（照 matrix）`## 结尾决策块`（照 matrix）`## 边界`（照 matrix，强化「只改说话方式、不动工程/工具/butler 规矩、交付正式文档另有模板」）。支撑 AC1。
- **`scripts/setup.sh`**（分发装法）：第 2 步受管 heredoc（第 63–75 行 `cat >> ... << EOF ... EOF`）内，在 butler 规则说明段之后加一行 `@$BUTLER_DIR/communication-style.md` + 一句注释说明它是常开的个人沟通风格正本；末尾「使用方式」提示可补一句。因走既有 awk 删旧块 + heredoc 重写机制，天然幂等、绝对路径。支撑 AC2/AC3。
- **`README.md`**：目录结构树登记 `communication-style.md` 一行（标个人全局配置、经 setup @import 常开、**不进** Coder SOP 阅读顺序）。支撑 AC4。
- **`HUMAN_GUIDE.md`** 安装节：点明「重跑 `setup.sh` 同时装上全局常开的沟通风格配置（`@import` communication-style.md）」+ 一句它管什么。支撑 AC4。
- **折叠（收口 step 4）**：`.ai/project/capabilities.md`（加「个人沟通风格全局常开正本 + setup @import 能力」；沟通风格从「散在 matrix/记忆」改「收敛单一正本」）、`frontier.md`（刷 v2.6.0 + 战线）。支撑 AC7/AC8。
- **发布层（独立 chore(release)）**：`VERSION`(2.5.0→2.6.0)、`CHANGELOG.md`(顶条 v2.6.0)、`migrations/v2.6.0.md`(`[no-op]`+`[restamp]`+机器级重跑 setup + 本机手动清理清单)。支撑 AC7/AC8。
- **本机迁移（不进仓提交，验证时执行并读本机文件核）**：删 `~/.claude/output-styles/matrix.md`；`~/.config/fish/config.fish` + `~/.zshrc` 两处 `claudep` 去 `--settings '{"outputStyle":"Matrix"}'`；查 `~/.claude/settings.json`；三记忆掏薄壳 + `MEMORY.md`。支撑 AC5/AC6。
- **不改**：`Coder/**`、`templates/**`、schema、hook、`.gitignore`、`preference-*`。

# Interface / Contract
- **@import 契约**：全局 `~/.claude/CLAUDE.md` 内一行 `@<绝对路径>` 触发 Claude Code 把该文件内容并入记忆（支持绝对路径、跟随软链、≤4 跳；已查证）。路径由 heredoc 里 `$BUTLER_DIR` 展开为绝对路径，随 setup 在每台机器上正确。
- **受管块幂等**：沿用 setup.sh 现有机制——有 `<!-- butler-global-config -->` 标记则 awk 删旧块、再 heredoc 追加新块；`@import` 行在块内，重跑即删后重写，恒定一行、无重复。
- **claudep 契约变更**：去掉 `--settings '{"outputStyle":"Matrix"}'` 后，`claudep` = `proxyon` + `claude <args>`；语义从「开代理 + 强制 Matrix 风格起 claude」变为「开代理起 claude」，风格改由常开 @import 提供，不再依赖 CLI 参数。
- 无 butler 侧新 schema/hook；不改四件套字段结构。

# State / Boundary
- 迭代 feat 提交（communication-style.md + setup.sh + README + HUMAN_GUIDE + `.ai/` 收口产物）与 release 提交（VERSION/CHANGELOG/migration + tag）**分离**（守 `versioning-schema §5.2/§6.1`）。
- 分发是**全局机器级**、非逐项目——正本不进 `templates/`、不进基地车部署。目标项目 `.ai/` 部署面零结构变化。
- 本机迁移（matrix/claudep/settings/记忆）落在 `~/` 下本机配置，**不在** butler 仓 diff 内；作为一次性手动步写进 migration + 交付，与 ITER-0045「机器级重跑 setup」同类。
- 边界强化：正本全局常开后更要防渗进工程行为——「边界」节明确只管说话方式。

# Design Decisions
- **决策 1：单一正本走「全局 CLAUDE.md @import」，不走输出风格**。理由：输出风格**不支持 @import**（已查证）且只有被选中才生效；用户要「永远在 + 跨机器同步」，唯有落随 git 走的仓内文件 + 常开的 CLAUDE.md 导入满足。与 ITER-0045「全局引用、不逐项目拷贝」同模型。
- **决策 2：收敛去重，规矩正文只此一份**。理由：说人话此前 matrix/记忆双写、正是漂移之源；matrix 7 节 + 记忆两条真增量并进正本，matrix 清空退休、记忆掏薄壳（只留原因）。DRY 到底。
- **决策 3：matrix 直接删、不留指路壳；claudep 同步拆参数**。理由：matrix 是过渡产物，留空壳是噪音；但删风格必须**同时**拆掉 claudep 里 `--settings '{"outputStyle":"Matrix"}'`，否则命令指向不存在的风格。settings.json 一并查残留。
- **决策 4：带 ❌/✅ 例子**。理由：用户实证——光写规矩不带例子管不住（matrix 最初只写「要简洁」压不住黑话，补具体病症对照才治住）；每条留一对，不铺一堆，token 换「规矩能落地」值。
- **决策 5：名字 `communication-style.md`、放仓根、不进 Coder SOP 阅读顺序**。理由：「preference/偏好」已被工程决策探针占用，须避让；它是个人全局配置、非工程 SOP 规则，故登记结构树但不进 SOP 读序。
- **决策 6：判 MINOR、migration 部署面 `[no-op]`+`[restamp]` + 注明机器级重跑 setup + 本机手动清理**。理由：`versioning-schema §2` 新增常开能力=MINOR；目标项目 `.ai/` 无结构变化=`[no-op]`；但「装上 @import」需重跑 setup，本机迁移需手动清 matrix/claudep——如实写、不藏（与 ITER-0045 配方同型）。

# Execution Steps
- [ ] T1 开 ITER-0046：`.ai/ITERATIONS.md` 领号 active + `current` 指向、`task-state` 状态块、`01_CHANGELOG` 重置 → 随四件套开启
- [ ] T2 [P] 新建 `communication-style.md`（8 节，先把 matrix 逐字搬全 + 折入两条增量 + 开篇定位）→ AC1
- [ ] T3 改 `scripts/setup.sh` 受管 heredoc 加 `@import` 行 → AC2/AC3（依赖 T2 的文件名/路径确定）
- [ ] T4 [P] 注册文档 `README.md` + `HUMAN_GUIDE.md` → AC4
- [ ] T5 隔离 HOME 实跑 setup.sh 验证（@import 行计数=1 / 幂等连跑两次仍=1 / 抽路径 test -f 为真）→ 回填 VERIFY AC2/AC3
- [ ] T6 本机迁移：先核 matrix 各节已全在正本（内容不丢）→ 删 matrix.md → 拆 fish+zsh 两处 claudep 参数 → 查 settings.json → 掏薄壳三记忆 + 改 MEMORY.md → 读文件核 → AC5/AC6
- [ ] T7 收口五步：归档 `iterations/ITER-0046/` → 交付 `.md`+`.html` → 台账 closed/current:none → 折叠 `capabilities`+`frontier` → 6 不变量自检 → AC7/AC8
- [ ] T8 feat 提交（communication-style.md + setup.sh + 文档 + `.ai/` 产物）；提交后 `git show --stat` 核 → 回填 AC8
- [ ] T9 独立切 v2.6.0：VERSION / CHANGELOG / migration → `chore(release)` 提交 + tag `v2.6.0` → 三载体对齐自检 → AC7/AC8
- [ ] T10 push 分支 + 开 draft PR（本 job 在 worktree、需 ship）

# Verification Plan
- AC1：读 `communication-style.md` 核 8 节齐、说人话 4 条各 ❌/✅、别抛菜单节 ❌/✅、开篇定位在；通读确认边界干净（无工程/工具规矩）。
- AC2/AC3：`env HOME=$CLAUDE_JOB_DIR/tmp/fakehome-0046 bash scripts/setup.sh` 实跑；`grep -c '@.*communication-style.md' <fakehome>/.claude/CLAUDE.md` == 1；连跑两次再核 == 1；`sed`/`awk` 抽该行路径 → `test -f` 为真。
- AC4：读 README/HUMAN_GUIDE 改动段核注册句在、说人话。
- AC5：迁移前逐节 diff 核 matrix→正本无遗漏；`test ! -e ~/.claude/output-styles/matrix.md`；`grep outputStyle ~/.config/fish/config.fish ~/.zshrc ~/.claude/settings.json` 无 Matrix 残留。
- AC6：读三记忆 + MEMORY.md 核薄壳化、MILE-0003 引用留存。
- AC7：读 migration 核三事项（`[no-op]`+`[restamp]` / 机器级重跑 setup / 本机手动清理清单）。
- AC8：6 不变量自检；`git tag --points-at HEAD` 含 `v2.6.0`；三载体对齐；两提交分离。

# Risks / Open Questions
- Open Questions 已在本阶段关闭（决策 1 走 @import / 决策 3 直接删 matrix + 拆 claudep / 结尾块保留 / 记忆留薄壳）。
- @import 运行时并入属 Claude Code 行为，非本仓可断言——验证止于路径正确 + 文件存在 + 受管块合法（AC3 已记边界）。
- 本机迁移跨机器不自动传播——migration 配方写清换机器需同样清理，但新机器不依赖 matrix。
