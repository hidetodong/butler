---
description: ⚠️ 无人值守长程自治（实验性）——留空开启（模型自审替 ACK、自动拆迭代跑完整生命周期）；off 关闭；status 只看状态。风险显著高于标准，建议只在可隔离/可回滚环境开
argument-hint: "[留空=开启（走引擎风险闸）| off 关闭 | status 只读看状态]"
---

你正在操作 butler 的 **危险模式开关**（无人值守长程自治）。本命令是**薄壳路由器**——只做三件事：① 保证把对的规则读进上下文，② 按参数分派到对的开关动作，③ 委托真源执行并回声状态。**自治闭环、自主 ACK 自审门、安全护栏（审计 / checkpoint / P5 强制完整审查）、终止与交还一律以被指向的规则文件为准，本文件不复述**（守 butler DRY 红线）。

> **路径约定（本命令可在任意项目里运行，当前目录不一定是 butler 仓）**：下文引用的 `Coder/…` 都是 **butler 规则仓库**里的文件，一律相对 `$BUTLER_PATH`（`setup.sh` 全局安装时写入的环境变量）解析。危险模式开关状态落**当前项目**的 `.ai/local-constraints.md`「Butler 功能开关」`dangerous`（持久、跨会话），作用于当前项目的自治执行。

> **项目根硬门**：读写开关前先按 `$BUTLER_PATH/Coder/20_Workflow_Lifecycle/mcv-deployment.md §0.1` 解析 `PROJECT_ROOT`。上文“当前项目”一律指该绝对路径；仅凭会话 `cwd` 不得选项目，歧义时不得硬建 `.ai/`。

## 第 0 步 先认清这是实验性、风险显著高于标准
危险模式让模型在**无人值守**下长时间自主推进：一次发布需求 → 自动拆迭代 → 以收敛闭环跑完整条 P1–P5 → 连续推进到整体交付，**P2/P3 的用户 ACK 被模型自审门替代**。风险显著高于标准流程——**建议只在可隔离、可回滚的环境（独立 git 分支 / worktree）开启**。命令化不降低这道门槛：本命令只把你的显式意图接进引擎，引擎自己的闸（进入回声 + 跨会话 announce-on-read + 全套护栏）照常响，本命令不省略、也不代替这层郑重。
- 读得到 `Coder/65_Extension_Dangerous/dangerous-engine.md`（butler 可达）→ 正常往下走。
- 没接 butler（`$BUTLER_PATH` 未设 / 读不到引擎）→ 一句话告诉用户「危险模式是 butler 能力，需先全局安装 butler（`setup.sh`）」。**不报错、不空跑。**
- 当前项目没有 `.ai/`（没部署基地车）→ 开关无处持久，提示「先在本项目部署 butler（基地车）再开危险模式」，不硬建。

## 按 `$ARGUMENTS` 路由
先读 `Coder/65_Extension_Dangerous/dangerous-engine.md`——所有分支的公共真源（§3 激活/关闭、§3.1 跨会话 announce-on-read、§4 自治闭环、§5 自主 ACK 自审门、§7 安全护栏、§8 终止交还）。取 `$ARGUMENTS` 的**首 token** 分派：

**分支 空 ── 开启（走引擎风险闸）**
委托 §3 激活：把 `.ai/local-constraints.md` 的 `dangerous` 开关**回写为 `on`**，并按 §3 在当回合**对话层显式回声进入危险模式**（一句即可关：`/butler:dangerous off`）。开启即同时强制 §7 全套护栏（§7.1 自主决策审计日志 / §7.2 checkpoint 与可回滚锚点 / §7.3 P5 强制完整审查门 / §7.4 无人残余处置）——**护栏算法一字不在本文件复述，照真源执行**。回滚锚点建不起来（非 git / 环境受限）时按 §7.2 显式告警「本次自治不可回滚」，交用户定夺。

**分支 off ── 关闭**
委托 §3 关闭：把 `dangerous` 开关回写为 `off`，并在当回合对话层显式回声退出、恢复逐道等待 ACK 与 P5 简评默认。

**分支 status ── 只读看状态**
**不改开关**。只读当前项目 `.ai/local-constraints.md`「Butler 功能开关」`dangerous`（字段读写口径见 `Coder/20_Workflow_Lifecycle/local-constraints-schema.md §4.1`），回报当前是 `on` 还是 `off`；`on` 时附一句「新会话读到 `on` 会 announce-on-read 后自动进入」提醒。

**兜底 未知参数** → 提示合法参数集（留空=开启 / `off` / `status`），不瞎猜执行。

## 收尾
任何开关变更后，**当回合**用一句话显式回声当前状态（危险模式现在是开还是关），让流式输出中用户可见、可叫停；`status` 只读分支直接把查到的状态报给用户。
