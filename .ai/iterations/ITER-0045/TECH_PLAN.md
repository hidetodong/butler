# TECH_PLAN — ITER-0045（slash command 全局下发目标项目 · 软链装法）

# Goal
- 支撑 AC1–AC7：给 `setup.sh` 接上「软链命令到 `~/.claude/commands/`」这条分发线、把命令正文改成跨 cwd 健壮、注册文档、折叠收口、独立切 MINOR v2.5.0。

# Files / Modules to Change
- **`scripts/setup.sh`**（分发装法核心）：现有第 1 步（BUTLER_PATH 环境变量）、第 2 步（`~/.claude/CLAUDE.md` 全局配置）之后，加**第 3 步**——逐文件软链 `$BUTLER_DIR/.claude/commands/*.md` → `$HOME/.claude/commands/`；末尾「使用方式」提示补一句命令全局可用。支撑 AC1/AC2/AC3。
- **`.claude/commands/butler-prd.md`**（跨 cwd 健壮）：在开篇薄壳说明后、第 0 步前，插入一段 `> **路径约定**`——`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目。路由三分支正文一字不改。支撑 AC4。
- **`README.md`**：快速上手第 1 条 `setup.sh` 注释 + 目录结构 `.claude/commands/` 一行，注明全局命令安装。支撑 AC5。
- **`HUMAN_GUIDE.md`** §3 安装：把「自动完成两件事」改「三件事」，加第 3 条软链命令 + 一句「命令全局可用（所有项目）」。支撑 AC5。
- **折叠（收口 step 4）**：`.ai/project/capabilities.md`（`/butler-prd` 行 + setup 能力改「全局下发」）、`frontier.md`（刷 v2.5.0 + 战线）、`debt.md`（**删**第 3 笔「未下发」欠债）。支撑 AC6/AC7。
- **发布层（独立 chore(release)）**：`VERSION`(2.4.0→2.5.0)、`CHANGELOG.md`(顶条 v2.5.0)、`migrations/v2.5.0.md`(`[no-op]`+`[restamp]`+机器级重跑 setup)。支撑 AC6/AC7。
- **不改**：`Coder/**`、`templates/**`、schema、hook、`.gitignore`。

# Interface / Contract
- **软链契约**：`ln -sfn "$src" "$dest"`——`-s` 符号链接、`-f` 强制替换已存在目标、`-n` 不解引用已存在的目录符号链接（BSD/macOS 与 GNU 均支持）。目标 `$dest = $HOME/.claude/commands/$(basename src)`。源为 butler 仓真实路径（软链常青、butler 改即生效）。
- **空目录守卫**：`compgen -G "$BUTLER_CMD_DIR/*.md"` 测存在性（bash 内建，脚本 shebang 为 bash），无匹配走 else 分支打印跳过，`set -euo pipefail` 下不触发非零退出。
- 命令契约不变：Claude Code 命令 frontmatter `description`+`argument-hint`、`$ARGUMENTS` 承参。无 butler 侧新契约、无 schema/hook 变更。

# State / Boundary
- 迭代 feat 提交（装 setup.sh + 命令文件 + README + HUMAN_GUIDE + `.ai/` 收口产物）与 release 提交（VERSION/CHANGELOG/migration + tag）**分离**（守 `versioning-schema §5.2/§6.1`）。
- 分发是**全局机器级**、非逐项目——命令不进 `templates/`、不进基地车部署。目标项目 `.ai/` 部署面零结构变化。
- 边界写进 migration + 交付：升级只需「重跑 setup.sh」这一个机器级动作。

# Design Decisions
- **决策 1：软链，不拷贝**。理由：与 butler 分发规则的方式（全局引用 `$BUTLER_PATH`、不逐项目拷贝）同构；软链使命令永远追随 butler 仓当前版本，零漂移、免 `/butler-upgrade` 同步命令副本。代价（仓库被挪则悬空）可接受，BUTLER_PATH 本机器本地。
- **决策 2：全局 `~/.claude/commands/`，不逐项目 `templates/`**。理由：逐项目唯一好处「随目标仓走」是空的——命令依赖 `$BUTLER_PATH/Coder/…`，无 butler 的机器跑不起来；全局装法一次到位、所有项目可见（正治「记不住用」）、不给每个项目留副本与升级债。
- **决策 3：逐文件软链、不整目录 symlink/接管**。理由：用户 `~/.claude/commands/` 可能已有自己的命令；只软链 butler 的 `butler-*.md`，不碰别人。
- **决策 4：命令正文只加「路径约定」一句、不重写路由**。理由：DRY + 最小实现；路由三分支逐条保留，只补 cwd 无关的解析规则，让同一薄壳在 butler 仓内（cwd==BUTLER_PATH）与目标项目（cwd≠）都成立。
- **决策 5：判 MINOR、migration 部署面 `[no-op]`+`[restamp]` 但注明机器级重跑 setup**。理由：`versioning-schema §2` 新增分发能力=MINOR；目标项目 `.ai/` 无结构变化=`[no-op]`；但「装上命令」需重跑 setup，是既有项目升级要知道的真实动作，如实写、不藏。

# Execution Steps
- [ ] T1 开 ITER-0045：`.ai/ITERATIONS.md` 领号 active + `current` 指向、`task-state` 状态块、`01_CHANGELOG` 重置 → 随四件套开启
- [ ] T2 [P] 改 `scripts/setup.sh` 加第 3 步软链 + 提示 → AC1/AC2/AC3
- [ ] T3 [P] 改 `.claude/commands/butler-prd.md` 加路径约定段（不动路由）→ AC4
- [ ] T4 [P] 注册文档 `README.md` + `HUMAN_GUIDE.md` → AC5
- [ ] T5 隔离 HOME 实跑 setup.sh 验证（软链目标/解引用/幂等连跑两次/空目录跳过/非butler命令保留）→ 回填 VERIFY AC1–AC3
- [ ] T6 收口五步：归档 `iterations/ITER-0045/` → 交付 `.md`+`.html` → 台账 closed/current:none → 折叠 `capabilities`+`frontier`+`debt`（删第3笔）→ 6 不变量自检 → AC6/AC7
- [ ] T7 feat 提交（setup.sh + 命令 + 文档 + `.ai/` 产物）；提交后 `git show --stat` 核 → 回填 AC7
- [ ] T8 独立切 v2.5.0：VERSION / CHANGELOG / migration → `chore(release)` 提交 + tag `v2.5.0` → 三载体对齐自检 → AC6/AC7
- [ ] T9 push 分支 + 开 draft PR（本 job 在 worktree、需 ship）

# Verification Plan
- AC1/AC2/AC3：`env HOME=$CLAUDE_JOB_DIR/tmp/fakehome bash scripts/setup.sh` 实跑；`readlink` 核 `$dest` 指向仓内源、`cat` 解引用核内容一致；连跑两次核幂等无重复；在 fakehome `commands/` 预置 `zzz-other.md` 跑后确认仍在；临时把命令挪空核 else 跳过不崩。
- AC4：读命令文件核路径约定段 + `git diff` 核路由三分支未动、只加约定。
- AC5：读 README/HUMAN_GUIDE 改动段核注册句在。
- AC6：读 migration 核三标签语义 + 机器级重跑说明；`debt.md` 确认第 3 笔已删。
- AC7：6 不变量自检；`git tag --points-at HEAD` 含 `v2.5.0`；`VERSION`==tag==CHANGELOG 顶条；两提交分离。

# Risks / Open Questions
- 两个 Open Question 已在本阶段关闭（决策 1 软链 / 决策 2 全局；批量落其它命令记 frontier 不做）。
- `ln -sfn` 跨 BSD/GNU 语义一致性：两平台 `-sfn` 均支持，实测在 macOS（本机 darwin）跑通即够；不承诺其它平台但语法通用。
- 「补全菜单真列出」属 Claude Code 运行时，非本仓可断言——验证止于文件落位 + 内容可读 + frontmatter 合法（AC_LIST 已记此边界）。
