> 分流: 完整 | 命中升级信号: 破坏性改名, 多文件跨目录产物, shell 脚本改造, 涉及发布切版 | 2026-07-14

# 一句话
把 butler 现在「只有一个真命令 `/butler-prd`」的局面，升级成一套 `/butler:xxx` 命名空间命令系统的**地基**。这一迭代不补齐所有命令，只搭骨架：建命名空间目录、把已有的 `/butler-prd` 干净迁进来、改 `setup.sh` 让整个命名空间目录随软链全局可用，并落第一个新命令 `/butler:review` 证明「薄壳路由器」范式在命名空间下可复制。先做地基，因为后面 R2–R4 批量加命令都依赖这套骨架与迁移范本先稳下来。

# Goal
- 建 `.claude/commands/butler/` 命名空间子目录，让 `butler/<name>.md` 自动成为 `/butler:<name>` 命令。
- 把 `/butler-prd`（连字符、v2.4.0 发布）**破坏性迁**为 `/butler:prd`：移动文件 → `butler/prd.md` + 清旧全局软链 + 更新正文/文档引用 + 出 `[rename]` 迁移配方。
- 改 `scripts/setup.sh`：软链逻辑从「逐个软链 `.claude/commands/*.md`」改为「软链整个 `butler/` 目录到 `~/.claude/commands/butler`」——一条目录软链托管全套，butler 仓加命令自动全局生效、无需重跑 setup。
- 落第一个新命令 `/butler:review`（纯薄壳路由器），委托 `60_Extension_CodeReview` / `62_Extension_Agents` 真源，验证范式可复制。
- 固化「薄壳路由器」范本，供 R2–R4 批量复制。

# Current Understanding
- **现状**：butler 只有 `.claude/commands/butler-prd.md` 一个真命令；其余能力（milestone / review / loop / dangerous 等）还是散在规则正文里的「散文触发词」。`setup.sh` 已把 `.claude/commands/*.md` 逐个软链到全局（ITER-0045 验证 `/butler-prd` 全局可用），但这个 `*.md` 通配是**扁平的、不进子目录**——命令进 `butler/` 子目录后会漏软链。
- **已查证的地基事实**：Claude Code 里子目录＝命名空间，`butler/prd.md`→`/butler:prd`，冒号是真调用分隔符；user 级（`~/.claude/commands/butler/`）同理；frontmatter（`description`/`argument-hint`/`$ARGUMENTS`）照常；command 的 `.md` 软链已由 ITER-0045 实跑验证可用（故维持 commands 路线、**不迁 skills**）。
- **预期产出**：命名空间目录 + `butler/prd.md`（迁自 `butler-prd.md`，内部路径引用相应调整）+ `butler/review.md`（新）+ 改造后的 `setup.sh` + `migrations/vX.Y.Z.md`（`[rename]`）+ 正文/文档引用更新。
- **只做 R1 骨架**，不补 R2–R4 的其余命令。

# Constraints
- **薄壳只路由、不复述算法**：`review.md` 委托 `review-engine.md` 等真源，守 butler DRY 红线，不抄算法（同 `butler-prd.md` 范式）。
- **破坏性改名要清干净**：迁 `/butler-prd`→`/butler:prd` 必须清掉旧全局软链 `~/.claude/commands/butler-prd.md`、扫掉正文/文档里所有 `/butler-prd` 旧引用，不留双源。
- **不下发目标项目**：命令是个人工具，不进 `templates/`、目标项目部署面零影响（沿用 ITER-0044 边界）。
- **不改真源规则算法**：`Coder/**` 规则正文语义一律不动。
- **没接 butler 优雅降级**：`review.md` 薄壳要处理「当前项目没 `.ai/` 迭代产物」的情形（复核依赖迭代产物），给清晰提示而非报错。
- **setup.sh 改造要幂等**（可重复跑不炸），且不接管 `~/.claude/commands/` 根下你自己放的其它命令——只软链 `butler/` 子目录。

# Impact Scope
- **改动**：新建 `.claude/commands/butler/`（`prd.md` 迁入 + `review.md` 新建）；删 `.claude/commands/butler-prd.md`（迁移，非遗留）；改 `scripts/setup.sh`（软链逻辑）；新增 `migrations/vX.Y.Z.md`（`[rename]`）；更新**活规则 / 面向人文档**里对 `/butler-prd` 的引用（待 grep 定位）。
- **发布层**：`VERSION` / `CHANGELOG.md` / tag（切版；bump 判定见 Open Questions）。
- **不碰**：`Coder/**` 任何规则算法、`templates/**`、四件套 schema、hook 体系、核心 P1–P5 状态机。
- **本机一次性动作**：清旧全局软链 `~/.claude/commands/butler-prd.md` + 重跑 `setup.sh` 装新的目录软链。

# Project Type / Active Profiles
- 项目形态：Markdown 规则仓库（butler 自身 dogfood），非应用代码工程；本迭代另涉及一个 shell 脚本（`setup.sh`）改造。无 Domain / Stack Profile 命中（不涉及 vue3 / typescript 等技术栈）。按通用 SOP + butler 自身开发约定（仓库 `CLAUDE.md`）推进。

# Open Questions
- **切版号**：MINOR（命名空间是新增能力）还是要标破坏性？`/butler-prd`→`/butler:prd` 对「已在用旧命令的你自己」是 breaking，但对目标项目部署面是 no-op。倾向 MINOR + 迁移配方 `[rename]` 讲清个人命令层的破坏动作——待 P2/P3 定。
- **`/butler:review` 参数面**：`review-engine` 区分默认同上下文自评 vs 独立复核（opt-in、fresh-context 子 agent）。薄壳要不要吃参数区分 `default`/`independent`？待 P2 定路由粒度。
- **正文引用更新边界**：`/butler-prd` 旧引用要改成 `/butler:prd`，但**历史归档**（`deliveries/`、`.ai/iterations/` 冻结快照）是否也改？倾向「活规则 + 面向人文档改、历史归档快照不动」（快照是冻结的），待 P2 定。
