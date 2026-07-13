---
状态: ack-frozen
ACK 日期: 2026-07-13
---

# Goal
- 让 butler slash 命令在任意目标项目里可发现可执行，走**全局软链**装法闭掉分发缺口；命令正文跨 cwd 健壮；边界与升级动作如实记录。

# In Scope
- `scripts/setup.sh` 加「软链 `.claude/commands/*.md` → `~/.claude/commands/`」步骤（幂等）。
- `.claude/commands/butler-prd.md` 加「规则路径相对 `$BUTLER_PATH` 解析、`.ai/` 落当前项目」约定（不改路由逻辑）。
- `README.md` + `HUMAN_GUIDE.md` 注册「setup 装全局命令、命令全局可用」。
- 折叠 `capabilities`/`frontier`/`debt`；独立发布提交切 MINOR v2.5.0（VERSION / CHANGELOG / migration）。

# Out of Scope
- 不改任何 `Coder/**` 规则正文、不动 `templates/`（不进逐项目部署面）、不改四件套 schema / hook / `.gitignore`。
- 不把命令逐项目下发（不进基地车部署）；分发是**全局**、非 per-project。
- 不把 `/milestone` / `/prd` 等其它散文命令一并落文件（本轮只打通 `/butler-prd` 的分发链路）。

# Acceptance Checklist
- [ ] AC1: `setup.sh` 跑完（隔离 HOME 实测）后，`$HOME/.claude/commands/butler-prd.md` 作为**软链**存在、指向 `$BUTLER_DIR/.claude/commands/butler-prd.md`、可解引用读到正确内容；butler 仓 `.claude/commands/` 下每个 `*.md` 都被逐一软链过去。
- [ ] AC2: 软链步骤**幂等**——`setup.sh` 连跑两次不报错、不产生重复/损坏链接（`ln -sfn` 原子替换）；且**逐文件**软链，不接管整个 `~/.claude/commands/` 目录（预置在该目录的非 butler 命令文件原样保留、不被删）。
- [ ] AC3: 命令目录**为空或缺失时优雅降级**——`.claude/commands/` 无 `*.md` 时 setup 打印「跳过」而非报错退出（`set -euo pipefail` 下不崩）。
- [ ] AC4: `.claude/commands/butler-prd.md` 正文含明确的**路径约定**：引用的 `Coder/…` 规则相对 `$BUTLER_PATH` 解析（不是当前项目路径）、产出的 `.ai/references/prd/…` 落当前项目；原三分支路由逻辑（第 0 步契约读 + 留空/贴PRD=prd-split·update=prd-update·status=prd-update §7 + 「不复述」声明）**逐条保留未破坏**。
- [ ] AC5: 文档注册齐——`README.md` 快速上手/结构处注明 `setup.sh` 现在也装全局 slash 命令；`HUMAN_GUIDE.md` §3 安装列出「装全局命令」这件事，并点明命令**全局可用**（所有项目，不再限 butler 本仓）。措辞守 `artifact-style §2` 说人话。
- [ ] AC6: 边界与升级动作如实——`migrations/v2.5.0.md` 写清：对目标项目 `.ai/` 部署面 `[no-op]`+`[restamp]`，但有一个**机器级动作**「重跑 `./scripts/setup.sh` 装全局软链」；`frontier`/`capabilities` 更新为「全局下发」、`debt` 第 3 笔「未下发」欠债**删除**（已还）。不夸大也不隐瞒。
- [ ] AC7: 收口 + 切版一致性——四件套说人话、收口五步齐（归档 / 交付 .md+.html / 台账 closed·current:none / 折叠三产物 / 6 不变量自检）；v2.5.0 三处版本载体对齐（`VERSION` == tag `v2.5.0` == `CHANGELOG` 顶条 `## [2.5.0]`）；迭代 feat 提交与 chore(release) 提交分离。

# Verification Method
- AC1/AC2/AC3: 隔离 HOME 实跑——`env HOME=<tmp> bash scripts/setup.sh`，`readlink` 核软链目标 + 解引用读内容；连跑两次核幂等；临时清空/移开 `.claude/commands/*.md` 核跳过分支不崩。另在 tmp HOME 的 `commands/` 预置一个非 butler `*.md`、跑后确认仍在。
- AC4: 读 `.claude/commands/butler-prd.md` 核路径约定段存在 + 三分支/第0步/「不复述」逐条仍在；`git diff` 核只加约定、未删路由。
- AC5: 读 README / HUMAN_GUIDE 改动段核注册句。
- AC6: 读 `migrations/v2.5.0.md` 核 `[no-op]`+`[restamp]`+机器级重跑 setup 说明；读 `debt.md` 确认第 3 笔已删、`frontier`/`capabilities` 已改「全局下发」。
- AC7: 收口后跑 6 不变量自检；切版后 `git tag --points-at HEAD` + 三载体比对；`git show --stat` 核两提交分离。

# Open Questions / Risks
- 软链在使用者机器上有效，但若用户挪走/删掉 butler 仓则链接悬空——可接受（BUTLER_PATH 本机器本地、butler 按机器装）；不在本轮加自愈。
- Claude Code 是否跟随软链发现命令：主流实现读目录即跟随符号链接，AC1 实测解引用可读即证装法成立；命令能否在补全菜单真正列出属 Claude Code 运行时行为，非本仓可断言项，验证止于「文件在对的位置、内容可读、frontmatter 合法」。
