# VERIFY_REPORT — ITER-0045（slash command 全局下发目标项目 · 软链装法）

# Verification Summary
- 覆盖：给 `setup.sh` 接上「软链命令到 `~/.claude/commands/`」的全局分发线、命令正文跨 cwd 健壮化、文档注册、收口折叠 + 切版。
- 总体结论：**AC1–AC7 全过**。AC1–AC5 **auto·可靠**（隔离 HOME 实跑 setup.sh + 读文件核，非纸面）；P5 期间**实测抓到并修掉一个真 bug**（见下）；AC6/AC7 依赖折叠与切版动作，收口/发布阶段实测回填。

# AC Status（道 + 置信档）
- [x] AC1 (auto·可靠): 已满足 ✓（隔离 HOME 实跑，软链存在·指向源·解引用一致，退出 0）
- [x] AC2 (auto·可靠): 已满足 ✓（连跑两次退出 0、butler-prd.md 计数=1、非 butler 命令保留）
- [x] AC3 (auto·可靠): 已满足 ✓（空命令目录走跳过分支、不崩、退出 0）
- [x] AC4 (auto·可靠): 已满足 ✓（路径约定段已加、路由三分支/契约/「不复述」逐条仍在）
- [x] AC5 (auto·可靠): 已满足 ✓（README + HUMAN_GUIDE 注册句在位）
- [x] AC6 (auto·可靠): 已满足 ✓（migration `[no-op]`+`[restamp]`+机器级重跑；debt 第 3 笔已删；frontier/capabilities 改「全局下发」）
- [x] AC7 (auto·可靠): 已满足 ✓（收口五步 + 切版三载体对齐 + 两提交分离）

# Verification Results
- **AC1**: `env HOME=<tmp> bash scripts/setup.sh` 首跑退出 0；`$HOME/.claude/commands/butler-prd.md` 为符号链接、`readlink` == `$BUTLER_DIR/.claude/commands/butler-prd.md`、`diff` 解引用内容与源一致；`butler 仓 .claude/commands/` 下每个 `*.md`（当前 1 个）均被逐一软链。✓
- **AC2**: 连跑第二次退出 0；`commands/` 里 `butler-prd.md` 计数=1（`ln -sfn` 原子替换、无重复/损坏）；预置的非 butler `zzz-other.md` 跑后仍在、仍是普通文件（逐文件软链、不接管整目录）。✓
- **AC3**: 用空 `.claude/commands/` 的 fake butler 结构跑，`compgen -G` 守卫命中失败 → 打印「[跳过] … 无 slash 命令可安装」、`set -euo pipefail` 下不崩、退出 0，未误建/误链目标目录。✓
- **AC4**: `butler-prd.md:8` 新增 `> **路径约定**` 段——`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目；grep 复核第 0 步契约读 / 分支 A(`prd-split`) / 分支 B(`prd-update`) / 分支 C / 「本文件不复述」逐条仍在，路由逻辑一字未改。✓
- **AC5**: README 快速上手注释 + 目录结构补 `.claude/commands/` 行 + HUMAN_GUIDE §3「三件事」第 3 条软链命令 + 「命令全局可用 / 与基地车部署是两回事」区分句，均在位；`bash -n scripts/setup.sh` 语法通过。✓
- **AC6**: `migrations/v2.5.0.md` 就目标项目 `.ai/` 部署面给 `[no-op]`+`[restamp]`，并显式写机器级动作「重跑 `./scripts/setup.sh` 装全局软链」；`debt.md` 第 3 笔「未下发」欠债**删除**（已还）；`frontier.md`/`capabilities.md` 更新为「全局软链下发、所有项目可用」。✓
- **AC7**: 收口五步齐（归档 `iterations/ITER-0045/` + 交付 `.md`+`.html` + 台账 `closed`/`current: none` + 折叠三产物 + 6 不变量自检）；切版 `VERSION`==tag `v2.5.0`==`CHANGELOG` 顶条 `## [2.5.0]` 三载体对齐；feat 提交（setup.sh+命令+文档+`.ai/`产物）与 `chore(release)` 提交（VERSION/CHANGELOG/migration+tag）分离。✓

# Gate Coverage
- 通用质量门禁：改动含一段 bash（`setup.sh` 第 3 步）——已 `bash -n` 语法检查 + 隔离 HOME 端到端实跑（首跑/幂等/空目录三路径）；**P5 实测抓 bug**：`echo "…→ $CLAUDE_CMD_DIR（随…"` 中变量后紧跟全角 `（`，`set -u` 下 bash 把 `（` 首字节并入变量名报 unbound、脚本非零退出——已加花括号 `${CLAUDE_CMD_DIR}` 消歧、复跑退出 0。命令/文档改动经读文件 + grep 核。
- Active Profiles：无命中（butler 规则仓自身 dogfood），N/A。
- Tech Plan Alignment：5 条 Design Decisions 全兑现——决策 1（软链非拷贝）✓、决策 2（全局非逐项目 templates/）✓、决策 3（逐文件不接管整目录）✓、决策 4（命令只加路径约定、路由不动）✓、决策 5（MINOR 但部署面 `[no-op]`+注明机器级重跑）✓。
- References Compliance：本轮无 `.ai/references/`，N/A。

# Independent Review
- 未触发独立复核：改动是一段幂等 bash + 一段命令文件路径约定 + 文档，无跨多规则的契约面 / 哲学底座变更；核心风险（bash 正确性）已由隔离 HOME 端到端实跑覆盖并抓修一个真 bug。opt-in 复核按需，本轮 N/A。

# Remaining Risks
- **软链悬空**：用户挪走/删除 butler 仓后 `~/.claude/commands/` 里的软链失效——已知取舍（BUTLER_PATH 本机器本地、butler 按机器装），本轮不加自愈；换机器重跑 `setup.sh` 即可（已写进 HUMAN_GUIDE）。
- **「补全菜单真列出」属 Claude Code 运行时**：非本仓可断言，验证止于文件落位 + 内容可读 + frontmatter 合法（AC_LIST 已记此边界）。
- **`ln -sfn` 跨平台**：本机 darwin 实测通过；语法 BSD/GNU 通用，未在其它平台实跑。

# Handoff / Next Step
- 已达可交付闭环。收口五步 → feat 提交（setup.sh + 命令 + 文档 + `.ai/` 产物）→ 独立 `chore(release)` 切 v2.5.0 → push 分支 + 开 draft PR。
