> 分流: 完整 | 命中升级信号: 补分发缺口（`/butler-prd` 只在 butler 仓可用、目标项目看不到）+ 改 setup.sh 装法 + 命令正文跨 cwd 健壮化 | 2026-07-13

# 一句话
- `/butler-prd` 现在住 butler 仓自己的 `.claude/commands/`，只有在**编辑 butler 仓时**才能用；目标项目里敲不出来——这正是 debt.md 记的分发缺口。
- 本迭代把它**全局下发**：`setup.sh` 加一步，把 butler 仓 `.claude/commands/*.md` 软链进 `~/.claude/commands/`，所有项目都能用；同时把命令正文的规则路径改成相对 `$BUTLER_PATH` 解析，保证在目标项目（cwd≠butler 仓）里也跑得通。

# Goal
- 让 butler 的 slash 命令（当前是 `/butler-prd`，及将来新增的 `butler-*` 命令）在**任意目标项目**里都能被 Claude Code 发现并执行，闭掉「命令只对 butler 本仓成立」的分发缺口。
- 分发走**全局软链**（与 butler 现有「全局引用、不逐项目拷贝」的规则分发模型一致），不进 `templates/`、不改逐项目基地车部署面。
- 命令正文**跨 cwd 健壮**：引用的 butler 规则一律相对 `$BUTLER_PATH` 解析、产出的 `.ai/` 一律落当前项目，二者不混。

# Current Understanding
- **病根（已核）**：Claude Code 只从 `~/.claude/commands/`（全局）与 `<项目>/.claude/commands/`（逐项目）发现命令。butler 仓的 `.claude/commands/butler-prd.md` 两者都不是——只在 cwd==butler 仓时命中。全仓 `Coder/`、`templates/`、`scripts/` 对 `.claude/commands` **零引用**，分发从未接过线。
- **现有全局装法（已读 setup.sh）**：`setup.sh` 是「一次性全局安装」，只写两样——shell rc 的 `BUTLER_PATH` 环境变量 + `~/.claude/CLAUDE.md` 的全局配置块（让所有项目发现 butler 规则）。**完全没碰 slash 命令**。
- **选型（已与用户确认）**：走**全局软链**，不走逐项目模板下发。逐项目那条唯一好处「命令随目标仓走、队友 clone 也有」是空的——命令正文要读 `$BUTLER_PATH/Coder/…`，队友机器没装 butler 照样跑不起来；而全局软链和 butler 分发规则的方式完全一致、最 DRY、butler 一改自动生效、零漂移。
- **命令正文现状（已读）**：正文写 `读 Coder/40_Context_Management/references-schema.md` 等 **butler 仓相对路径**。在目标项目里 cwd 不是 butler 仓，这些路径解析不到——必须声明「相对 `$BUTLER_PATH` 解析」。输出端 `.ai/references/prd/` 本就该落目标项目，正确、不动。

# Constraints
- **最小实现 + 影响面守恒**：只动分发装法（`setup.sh`）+ 命令正文路径约定 + 文档注册（README/HUMAN_GUIDE）+ 知识文件夹折叠；**不**改任何 `Coder/**` 规则正文、**不**动 `templates/`（不进逐项目部署面）、**不**改四件套 schema / hook / `.gitignore`。
- **软链装法幂等**：`setup.sh` 可反复重跑；已存在的软链原子替换（`ln -sfn`）、命令目录为空时优雅跳过、逐文件软链不整目录接管（不误删用户在 `~/.claude/commands/` 里的其它非 butler 命令）。
- **DRY**：命令正文仍是薄壳，路径约定只加一句「相对 `$BUTLER_PATH` 解析」，不把任何真源算法搬进来。
- **不部署逐项目**：命令是**全局**能力（机器级一次性安装），不进 `templates/`、不进基地车逐项目部署——目标项目 `.ai/` 部署面零变化。已部署项目升级到本版：`.ai/` 部署面 `[no-op]`+`[restamp]`，但**多一个机器级动作**——重跑一次 `./scripts/setup.sh` 装上全局软链。这条要在 migration 配方里如实写清（与 v2.4.0 配方里「将来进 templates/ 才算下发」的预测不同：本版走的是全局软链、非模板下发）。

# Impact Scope
- 改（分发装法）：`scripts/setup.sh`（加第 3 步：软链 `.claude/commands/*.md` → `~/.claude/commands/`）。
- 改（跨 cwd 健壮）：`.claude/commands/butler-prd.md`（加「路径相对 `$BUTLER_PATH`」约定，不改路由逻辑）。
- 改（文档注册）：`README.md`（快速上手/结构注明 setup 装全局命令）、`HUMAN_GUIDE.md`（§3 安装列出第 3 件事 + 点明命令全局可用）。
- 折（知识文件夹）：`.ai/project/capabilities.md`（`/butler-prd` 行改「全局下发」+ setup 能力）、`frontier.md`（刷 v2.5.0）、`debt.md`（删掉已还的第 3 笔「未下发」欠债）。
- 明确不影响：`Coder/**` 规则正文、`templates/**`、四件套 schema 字段结构、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机、基地车逐项目部署产物。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.4.0→2.5.0、`CHANGELOG.md` 顶条、`migrations/v2.5.0.md`。

# Project Type / Active Profiles
- butler 规则仓库自身 dogfood——编辑仓库资产本身（分发脚本 + 命令文件 + 文档），非用规则开发软件。
- 无 Domain / Stack Profile 命中；按通用 SOP + 仓库 `CLAUDE.md` 编辑约定推进。改的是一段 bash，验证走脚本实跑（隔离 HOME）。

# Open Questions
- 是否顺手把 `/milestone` / `/prd` 等其它散文命令也落成真实 `butler-*` 命令文件、一并全局下发？→ **本轮不做**：只把已成型的 `/butler-prd` 打通分发链路、验证「全局软链」这套装法可用；成体系铺开命令是后续独立方向（记 frontier）。
- 软链 vs 拷贝？→ 已定**软链**（butler 一改自动生效、零漂移；与规则分发同模型）。代价：用户挪走/删掉 butler 仓则软链悬空——可接受（BUTLER_PATH 本就机器本地、butler 按机器安装）。
