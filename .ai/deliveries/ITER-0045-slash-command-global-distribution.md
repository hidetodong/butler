# slash command 全局下发目标项目：一次 `setup.sh` 让 `/butler-*` 在所有项目可用

> ITER-0045 · 独立迭代（无所属里程碑）· 收口 2026-07-13 · dogfood butler 自身 · 判 MINOR·聚合切 v2.5.0（全局软链、目标项目部署面 `[no-op]`）

## 本次交付目标

- `/butler-prd`（ITER-0044 落为 butler 第一个真命令文件）之前住 butler 仓自己的 `.claude/commands/`，只有在**编辑 butler 仓时**才能用——目标项目里敲不出来。这正是 `debt.md` 记的分发缺口。
- 本次把它**全局下发**：给 `setup.sh` 接上一条软链线，把 butler 仓的 slash 命令软链进 `~/.claude/commands/`，让 `/butler-*` 在**所有项目**里可用；同时让命令正文跨目录健壮，在目标项目（当前目录不是 butler 仓）里也跑得通。

## 已完成内容

- **`setup.sh` 加第 3 步「全局软链命令」**：逐文件把 `$BUTLER_DIR/.claude/commands/*.md` 软链到 `~/.claude/commands/`。用**软链**而非拷贝——butler 仓一改命令，全局立即生效、零漂移、无需再逐项目同步副本。装法**幂等**（`ln -sfn` 原子替换、连跑不重复）、命令目录为空时**优雅跳过**（`compgen -G` 守卫、`set -euo pipefail` 下不崩）、**逐文件**软链不接管整个 `~/.claude/commands/`（你自己的其它命令原样保留）。
- **命令正文加「路径约定」，跨 cwd 健壮**：`.claude/commands/butler-prd.md` 开篇补一句——引用的 `Coder/…` 规则一律相对 `$BUTLER_PATH` 解析（不是当前项目路径），产出的 `.ai/references/prd/…` 一律落**当前项目**。原来的三分支路由（第 0 步契约读 + 首切/改版/看板 + 「不复述」DRY 声明）**一字未改**。
- **文档注册**：`README.md`（快速上手 + 目录结构注明 setup 装全局命令）、`HUMAN_GUIDE.md` §3 安装（「两件事」改「三件事」+ 点明命令**全局可用**、与逐项目「基地车部署」是两回事）。
- **知识文件夹前滚**：`capabilities.md`（`/butler-prd` 行 + 部署节改「全局软链下发」）、`frontier.md`（刷 v2.5.0、记「分发缺口已闭」）、`debt.md`（**删掉**已还的第 3 笔「未下发」欠债）。

## 关键变更 / 用户可感知变化

- **`/butler-prd` 现在在所有项目里都能用了**：重跑一次 `./scripts/setup.sh`，之后在任意项目敲 `/butler-prd`，补全菜单都能看到、也能执行——不再只有编辑 butler 仓时才有。
- **换机器只需重跑 setup**：命令是全局机器级安装（软链），不随目标仓走；到新机器装好 butler、跑一次 `setup.sh` 即可。
- **对已部署项目**：目标项目的 `.ai/` 结构零变化（升级配方 `[no-op]`+`[restamp]`）；要拿到命令，做一个**机器级动作**——重跑 `./scripts/setup.sh`。

## 高层影响范围

- 改（分发装法）：`scripts/setup.sh`（+第 3 步软链）。
- 改（跨 cwd 健壮）：`.claude/commands/butler-prd.md`（+路径约定，路由不动）。
- 改（文档注册）：`README.md`、`HUMAN_GUIDE.md`。
- 知识文件夹前滚：`.ai/project/capabilities.md` / `frontier.md` / `debt.md`（删第 3 笔）。
- 发布层（独立 chore(release) 提交）：`VERSION` 2.4.0→2.5.0、`CHANGELOG.md` 顶条、`migrations/v2.5.0.md`。
- 没碰（守最小影响面）：任何 `Coder/**` 规则正文、`templates/**`、四件套 schema 字段结构、`templates/hooks/**`、`.gitignore`、核心 P1–P5 状态机——`git status` 核清。

## 验证方式与结果摘要

- **7 项验收（AC1–AC7）全过**，AC1–AC5 **auto·可靠**、隔离 HOME 端到端实跑 `setup.sh`（非纸面）：软链存在·指向仓内源·解引用内容一致（AC1）；连跑两次退出 0·计数=1·预置的非 butler 命令保留（AC2 幂等+不接管）；空命令目录走跳过分支·不崩·退出 0（AC3）；命令路由三分支逐条仍在、只加路径约定（AC4）；README/HUMAN_GUIDE 注册句在位 + `bash -n` 语法通过（AC5）。
- **P5 实测抓到并修掉一个真 bug**：`setup.sh` 里 `echo "…→ $CLAUDE_CMD_DIR（随…"` 变量后紧跟全角 `（`，`set -u` 下 bash 把 `（` 首字节并进变量名报 `unbound variable`、脚本非零退出（软链已建但没干净收尾）——加花括号 `${CLAUDE_CMD_DIR}` 消歧后复跑退出 0。这正是隔离实跑而非纸面声明的价值。
- **AC6/AC7**：`migrations/v2.5.0.md` 就目标项目部署面给 `[no-op]`+`[restamp]` 并注明机器级动作「重跑 `setup.sh`」；`debt.md` 第 3 笔已删；收口五步齐 + v2.5.0 三载体（`VERSION` == tag `v2.5.0` == `CHANGELOG` 顶条）对齐 + feat 与 chore(release) 提交分离。
- **未触发独立复核**：改动是一段幂等 bash + 命令路径约定 + 文档，无跨多规则契约面 / 哲学底座变更；核心风险（bash 正确性）已由隔离实跑覆盖并抓修一个 bug。

## 已知剩余风险 / 延后事项

- **软链悬空**：用户挪走/删掉 butler 仓后 `~/.claude/commands/` 里的软链失效——已知取舍（BUTLER_PATH 本机器本地、butler 按机器装），本轮不加自愈；换机器/挪仓后重跑 `setup.sh` 即可（已写进 HUMAN_GUIDE）。
- **「补全菜单真列出」属 Claude Code 运行时**：非本仓可断言，验证止于文件落位 + 内容可读 + frontmatter 合法。
- **命令成体系化未做**：本轮只打通分发链路 + 以 `/butler-prd` 为范本；把 `/milestone`·`/prd`·`/review` 等散文命令逐个落成真实 `butler-*` 文件是后续独立方向（记 `frontier`）——一旦落文件，随 `setup.sh` 自动全局可用，无需再改分发。

## 引用（只引用路径，不嵌全文）

- 归档四件套 + 变更流：`.ai/iterations/ITER-0045/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `CHANGELOG.md`
- 分发装法：`scripts/setup.sh`（第 3 步）
- 命令文件：`.claude/commands/butler-prd.md`（路径约定段）
- 文档：`README.md`、`HUMAN_GUIDE.md`（§3 安装）
- 发布元数据：`VERSION`、`CHANGELOG.md`（`## [2.5.0]`）、`migrations/v2.5.0.md`
