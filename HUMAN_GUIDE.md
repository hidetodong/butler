# Butler 使用指南

> 面向人类用户的操作手册。帮助你在实际项目中正确引用 Butler 规则体系，并获得稳定的 AI 协作结果。

## 1. Butler 是什么

Butler 是一个 Markdown 规则仓库，定义了一套**通用需求开发 SOP**，用于规范 AI 辅助工程开发的协作流程。

它的核心价值：把 AI 从"自由发挥的编码助手"变成"按流程交付的工程协作者"。

AI 在各阶段呈现方案 / 选项 / 分析时遵循统一的**对话输出呈现格式**（结论先行、标号统一、多方案用表格、结尾给下一步，见 `Coder/00_System_Prompt/presentation-protocol.md`），便于你快速阅读与决策；简短问答和 P5 交付摘要不受此约束。

### 三个子系统

| 子系统 | 入口 | 用途 |
|---|---|---|
| **Coder** | `Coder/README.md` | 工程开发与 AI 协作 |
| Learner | `Learner/README.md` | 学习事务管理 |
| Composer | `Composer/README.md` | 其他杂项事务 |

本指南重点介绍 **Coder** 子系统。

## 2. 核心工作流（必须理解）

所有非极小任务默认走 **P1-P5 流程**：

```
P1 Analysis → P2 Acceptance → P3 Design → P4 Execute → P5 Verify
  理解问题      定义完成        确认方案      编码实现      验证交付
```

### 每个阶段做什么

| 阶段 | AI 产出 | 你需要做什么 |
|---|---|---|
| **P1 Analysis** | `.ai/CONCEPT.md` — 问题理解 | 确认 AI 理解正确 |
| **P2 Acceptance** | `.ai/AC_LIST.md` — 验收清单 | **必须 ACK 才能继续** |
| **P3 Design** | `.ai/TECH_PLAN.md` — 技术方案 | **必须 ACK 才能继续** |
| **P4 Execute** | 代码 / 配置 / 文档 | 观察进度 |
| **P5 Verify** | `.ai/VERIFY_REPORT.md` — 验证报告 | 确认交付 |

**关键点**：P2 和 P3 结束时，AI 必须等你确认（ACK）后才能进入下一阶段。这是你控制交付质量的核心杠杆。

### 简化路径

如果任务完全不命中以下任何升级信号，可以走简化路径（合并 P1+P2，口头确认 P3）：

- 需求有歧义
- 预计修改 ≥ 3 个文件
- 涉及接口 / API / 数据结构变更
- 涉及认证、权限、支付等关键路径
- 跨模块影响
- 需要在多个方案间取舍

**建议**：除非你非常确定任务很小，否则走完整流程。AI 倾向于高估自己的理解、低估任务复杂度。

### 迭代号与固定需求

每一轮 P1-P5 是一个**迭代**，有一个确定的迭代号 `ITER-NNNN`（单调递增，记在 `.ai/ITERATIONS.md` 台账里）。它的意义是把"这一轮固定了哪些需求、产出了哪套文档"钉死，方便回溯：

- **固定需求**：你在 P2 ACK 验收清单后，这一迭代的范围就**冻结**了。之后小幅改动可以重新 ACK（记一条修订记录）；但影响面明显扩大时，AI 会开**下一个迭代号**承接，而不是把范围悄悄塞进当前迭代。
- **落对应文档**：当前迭代的四件套（CONCEPT / AC_LIST / TECH_PLAN / VERIFY_REPORT）始终在 `.ai/` 固定路径；迭代收口时它们会被快照进 `.ai/iterations/ITER-NNNN/` 冻结归档，并落一份 `deliveries/ITER-NNNN-<slug>.md` 交付总结，外加一份同名 `.html` 固定格式阅读视图（双击即可在浏览器里读）。
- **你的杠杆**：想开新一轮需求时，直接说"这算新迭代"；想确认当前进度时，让 AI 读 `.ai/ITERATIONS.md` 台账即可。

## 3. 安装（一次性）

在 butler 仓库目录下执行：

```bash
./scripts/setup.sh
```

它会自动完成五件事：

1. 在 `~/.zshrc`（或 `~/.bashrc`）中写入 `BUTLER_PATH` 环境变量
2. 在 `~/.claude/CLAUDE.md` 中写入全局配置，让 Claude Code 在所有项目中都能自动发现 butler
3. 把 butler 的 slash 命令（`.claude/commands/butler/` 命名空间目录，如 `/butler:prd`）整个**软链**到 `~/.claude/commands/butler`，让它们在**所有项目**里都能用——不再只有编辑 butler 仓时才能敲。用软链而非拷贝：butler 仓一加/改命令，全局立即生效、无需重装
4. 在 `~/.claude/CLAUDE.md` 的全局配置里 `@import` 一行**沟通风格正本**（`communication-style.md`），规定 AI 该怎么跟你说话（语气、详略、说人话）。它跟着 butler 仓走、每个会话常开、跨机器同步；想调说话风格，改这个文件即可
5. 若检测到 Codex CLI，安装或刷新个人 Butler plugin（8 个 skills + hooks）；未安装 Codex 时明确跳过，不影响前四项

执行完后重启终端（或 `source ~/.zshrc`）。之后你**不需要再告诉 AI butler 在哪**，`/butler-*` 命令也随处可用，AI 也按你的沟通风格说话。

> 命令是**全局**安装（机器级、一次到位），跟逐项目的「基地车部署」是两回事——它不进目标项目的 `.ai/`，也不随目标仓走。换机器用 butler，重跑一次 `setup.sh` 即可。

安装器会先检查全部用户配置，再开始写入。遇到下面三类情况会停止并保留原文件，不会猜测或强行覆盖：

- `~/.claude/CLAUDE.md` 的 `<!-- butler-global-config -->` 不是完整一对：先修复或删除残缺的 Butler 管理区，再重跑。
- shell 配置里有多条生效的 `export BUTLER_PATH=...`：手工合并为一条，再重跑；注释里提到 `BUTLER_PATH` 不算配置。
- `~/.claude/commands/butler` 是真实文件/目录、无关软链或来源已经无法确认的断链：先确认所有权并改名/清理，Butler 不会替你删除。

每个用户文件都在同目录写完临时内容后再原子替换，并保留原权限。Codex plugin 是随后执行的独立组件；如果它失败，脚本会明确写“部分完成”，保留已经安全完成的 Claude/shell 配置，修复 Codex 错误后重跑即可。

### Codex 支持状态

v2.15.0 起，`./scripts/setup.sh` 同时安装 Claude 与 Codex 的机器级能力；基地车首次部署和 `/butler:upgrade` 会用同一渲染器维护项目根的 `CLAUDE.md` + `AGENTS.md`，两份项目特定约束各自保留。`plugins/butler/` 包含 8 个 skills、PreToolUse 门禁与 PostToolUse 提醒；安装后新开 Codex 会话，并在首次启用时审阅、信任 hook。

兼容边界：

- 8 个入口已完成：`$butler-prd`、`$butler-review`、`$butler-milestone`、`$butler-upgrade`、`$butler-ideation`、`$butler-preference`、`$butler-loop`、`$butler-dangerous`。后两个高风险入口只允许显式调用。
- hooks 只覆盖运行时实际报告的 `apply_patch`/兼容编辑事件；PreToolUse 不是 sandbox，也不能保证拦住 shell、MCP 或未来新增的所有写路径。
- `BUTLER_PATH` 缺失时 PreToolUse 门禁会 fail-closed；PostToolUse 提醒会 fail-open。若出现门禁不可用，先修正环境变量，不要用永久 trust/bypass 掩盖配置问题。

共同内核、两端适配层和验证矩阵见 [`docs/codex-compatibility.md`](docs/codex-compatibility.md)。需要只刷新 plugin 时仍可单独运行 `scripts/install-codex-plugin.sh`。

### 本地验证与 GitHub required check

开发 Butler 规则仓时，本地和 CI 都只跑这一条完整入口：

```bash
bash scripts/verify-ci.sh
```

入口会拒绝不匹配的 uv 版本，并使用仓库提交的 Python 版本与 `uv.lock`，不会在每次测试时临时解析 pytest/PyYAML 最新版。Codex plugin 和 8 个 skills 使用 `tools/codex-validators/` 中按 OpenAI Codex commit、SHA-256 与 Apache-2.0 许可证固定的官方 validator 快照，因此空 HOME 的 CI 也不会漏掉校验。

GitHub Actions 在 Linux 与 macOS 上运行同一入口，最终汇总 check 名固定为 **`Butler required checks`**。仓库管理员应先让 workflow 至少运行一次，再到 `main` 的 Ruleset/Branch protection 中把这个精确名称设为 required，并从设置页或只读 GitHub API 复核。

注意状态口径：workflow 入仓只代表 `check-provided`；保护设置尚未查询或尚未配置时必须写 `pending external configuration`。只有远端设置证据明确包含 `Butler required checks`，才能写 `required-enabled`。

## 4. 接入新项目

安装完成后，在任何项目中启动 AI 会话，直接给任务即可：

```
帮我实现用户登录功能
```

AI 会自动走完整个链路：

1. 从全局配置发现 butler 路径 → 读取 `Coder/README.md` 入口
2. 按读取顺序建立规则上下文（identity → logic-protocol → lifecycle …）
3. 先解析唯一施工项目根：你在任务中点名的路径优先；否则只接受当前位置所在的已部署 Butler 根或 Git 根
4. 若目标无法唯一证明（例如在包含多个仓库的父目录启动），AI 会先请你指定项目，不创建 `.ai/`
5. 已确认项目没有 `.ai/` 时才触发基地车部署，然后按 P1-P5 推进

部署完成后，项目根目录会同时生成 CLAUDE.md 与 AGENTS.md（同一浓缩规则卡 + 各宿主完整指针）。后续会话从对应入口读取规则，`.ai/` 状态由两端共享，**全局配置不再参与项目规则注入**。

你也可以显式说"部署基地车"来手动触发部署，效果一样。

> **多仓目录要点名项目**：如果你从 `~/Documents/research` 这类父目录启动会话，任务是改其中某个仓库或其他路径的仓库，请直接说项目名/路径。会话从哪里启动不等于台账应该写到哪里。

### 部署后的目录结构

```
你的项目/
├── CLAUDE.md               # Claude Code 入口（Butler 管理区 + 用户保护区）
├── AGENTS.md               # Codex 入口（同一规则卡 + Codex 冷启动读序）
├── .ai/
│   ├── CONCEPT.md          # P1 产物 = 当前迭代工作区
│   ├── AC_LIST.md           # P2 产物 = 当前迭代工作区
│   ├── TECH_PLAN.md         # P3 产物 = 当前迭代工作区
│   ├── VERIFY_REPORT.md     # P5 产物 = 当前迭代工作区
│   ├── ITERATIONS.md        # 迭代台账（迭代号/状态/所属 milestone/交付链接）
│   ├── iterations/          # 各迭代收口快照（ITER-NNNN/，按需产生）
│   ├── MILESTONES.md        # 里程碑台账（大版本，按需产生）
│   ├── MILESTONE.md         # 当前里程碑工作区：范围评估/理解阐释/拆分路线图（按需产生）
│   ├── milestones/          # 各里程碑收口快照（MILE-NNNN/，按需产生）
│   ├── local-constraints.md # 本地化约束
│   ├── 00_IDEATION.md       # 脑暴产物（/ideation 模式）
│   ├── 01_CHANGELOG.md      # 技术决策日志
│   ├── 02_SESSION_HANDOFF.md # 跨会话恢复入口
│   ├── 03_BUG_LOG.md        # RCA 报告
│   ├── task-state.md        # 运行时状态
│   └── references/          # 外部参考资料（按需创建）
├── deliveries/              # 交付总结归档（每份 .md 另有同名 .html 固定格式阅读视图）
│   ├── ITER-NNNN-<slug>.md  #   迭代交付（小版本），平铺即时间线
│   ├── ITER-NNNN-<slug>.html #  └ 同名固定格式阅读视图，双击即可浏览器打开
│   └── milestones/          #   里程碑交付（大版本），MILE-NNNN-<slug>.md(+.html)
└── origin/                  # 人类原始概念输入收件箱（你自管，AI 只读不重塑）
```

> `origin/` 与 `.ai/references/` 别混：`origin/` 放**你自己的**原始想法/概念文件（AI 只读取、不改写）；`references/` 放**外部第三方资料**（API 文档、设计稿），由 AI 处理改名后注入。

### Butler 版本（规则源版本与升级）

Butler 规则仓库本身有**硬版本号**，遵循语义化版本 `MAJOR.MINOR.PATCH`：

- **在哪看**：仓库根 `VERSION`（机器真源，单行版本号）、`CHANGELOG.md`（人读发布史，按版本聚合迭代）、git tag `vX.Y.Z`（每次发布的锚点）。
- **三级含义**：MAJOR = 破坏性变更（文件重命名/删除、契约或命令语义不兼容，升级可能要手工迁移）；MINOR = 向后兼容的能力新增（新 schema/命令/模式）；PATCH = 措辞澄清与不改行为的修订。
- **部署会留下版本戳**：CLAUDE.md 与 AGENTS.md 顶部都会标注"规则源：butler vX.Y.Z"；升级会先对账两者，再共同重戳。
- **升级先计划再写**：输 `/butler:upgrade` 或使用 `$butler-upgrade` 时，两宿主都会调用同一 `tools/butler-upgrade/upgrade.py`。它从 `migrations/manifest.json` 算版本队列，dry-run 回报逐文件变化、冲突、`[split]` 决定和机器级待办；显式放行后才事务 apply。失败会从项目内 backup 恢复，不靠模型解释 Markdown 或 `git reset`。
- **人工/机器边界不假绿**：`[split]` 可明确暂缓；选择现在迁时仍由有人做语义路由。`[global-install]` 会改 HOME，必须单独确认，项目升级不会暗中执行。版本 gap 只决定队列，marker/hash/所有权检查决定能否安全写。

## 5. 扩展模式

Butler 提供若干可选扩展模式，通过指令或语义触发，默认不启用：

| 模式 | 触发方式 | 用途 |
|---|---|---|
| **Ideation** | `/ideation` 或 "脑暴"、"完善需求"、"想不清楚"、"还没想好" | 需求脑暴与完善 |
| **收敛闭环** | `/butler:loop` 或 "死磕"、"必须变绿" | 高强度纠错升档（死磕到绿 + 定量熔断）；底线由常驻纠错收口契约保证 |
| **Review** | `/review` 或 "看看写得怎么样"、"代码审查" | 代码审计：P5 默认同上下文轻量自评；**独立复核**（fresh-context 第三方 agent）手动 `/review` 或项目配置开启，详见下方 |
| **Dangerous** ⚠️ | `/butler:dangerous` 或 "放手做"、"自己跑完"、"别等我确认" | 实验性无人值守长程自治：自动拆迭代连续推进、P2/P3 ACK 由自审门替代，附审计/回滚/P5 强制审查护栏。仅在可隔离、可回滚环境用 |
| **Preference** ⚠️ | `/butler:preference on`/`off`(隐私总关) · `reback on`/`off` · `distill` | 实验性偏好探针：采集你的设计取舍、蒸馏跨项目通识，在**有监督**工作里改进提议。采集经一次同意默认开、反哺 opt-in，详见下方 |

### 项目级功能开关（持久配置）

butler 的持久模式开关，统一记在 `.ai/local-constraints.md` 的「**Butler 功能开关**」段里——这是"对 butler 功能做项目级持久化配置"的**一处统一落点**（部署时即建好，默认全 off）：

| 开关 | 含义 |
|---|---|
| `dangerous: on\|off` | 无人值守长程自治模式 |
| `independent_review: on\|off` | 每次 P5 收口自动起独立复核 |
| `preference: on\|off` | 本项目偏好探针采集开关（默认 on；off = 本项目不采集/蒸馏/反哺） |

**两种改法，等价**：① 对话里用自然语言/命令说（如 `/butler:dangerous`、"以后这个项目都开严格复核"），AI 帮你回写；② 你直接手改这个文件。AI **每个会话开始都会读它**，据此决定这一会话怎么跑——状态不再只活在对话里、关掉窗口就忘。

**⚠️ 危险模式跨会话**：`dangerous: on` 会**跨会话保留**。新会话一开，AI 读到它会**先显式声明**"危险模式当前 ON、本会话将无人值守执行，要关说 `/butler:dangerous off`"，**声明后才自动进入**——绝不静默。代价是：你若忘了关，下次进来它声明完就自己跑。所以只在可隔离、可回滚的环境（独立分支/worktree）里留着 `on`。

**关于 `preference`**：偏好探针的总开关、同意状态与数据是**跨项目**的（外置 `$BUTLER_PREF`），但**本项目可用 `preference: off` 单独抑制**——它只关掉这一个项目的采集，不影响全局同意和别的项目。注意 `on` ≠ 强制采集：没给过全局同意时，即便 `on` 也不会采。consent/数据真源始终在外置存储，这个开关只是本项目的采集闸。

### 里程碑（大版本）

迭代之上还可套一层**里程碑** `MILE-NNNN`，作为"大可交付版本"。当一批需求跨多个迭代、需要先整体圈定范围再拆分推进时，AI 会提议开里程碑：先写一份范围评估 + 理解阐释 + 拆分路线图（`.ai/MILESTONE.md`），与你 soft 对齐后，期间开启的迭代自动归属它；大版本收口时聚合各迭代产出一份版本级交付（`deliveries/milestones/MILE-NNNN-<slug>.md`，同样附一份同名 `.html` 固定格式阅读视图）。里程碑是可选、松耦合的：不影响你按迭代推进的习惯，迭代历史在 `deliveries/` 根仍是一条连续时间线。

**自动归属的边界**：里程碑还**开着**的期间，你新提的迭代都**自动并进**这个里程碑、不用每次确认；一旦它**收口**，之后再开的迭代就是**独立**的，不会再塞进这个已关闭的里程碑（除非你显式开新里程碑或回挂到另一个进行中的里程碑）。

**怎么开一个里程碑——一次性说清，模型帮你拆**

你不用零散地边聊边拼。想推进一个大版本时，**在一处把想法一次性讲清**，模型据此生成里程碑概述（范围/理解/路线图）并拆出迭代承接规划。两条录入通道任选：

- **对话**：直接说，或输 `/milestone <你想做的大版本是什么>`。
- **文件**：把原始概念/想法写成文件丢进项目根的 `origin/` 收件箱（自由格式、随便几份），然后输 `/milestone` 让模型读它合成。

模型会把你的意图落成 `.ai/MILESTONE.md` 三段（范围评估 / 理解阐释 / 拆分路线图），信息不够的地方会显式标"待澄清"而不是替你瞎编，产出后跟你 soft 对齐（认方向即可，不用逐条 ACK）。拆分路线图按主题切片排序、标"预计 ITER 跨度"，但**不预先把迭代号钉死**——真号在每个迭代开启时才分配（避免中途插任务/改计划就失真）。

**两个命令**（轻量入口，跟自然语言等价，可选）：

| 命令 | 作用 |
|---|---|
| `/milestone` | 开启 / 录入里程碑（从对话或 `origin/` 文件取你的想法合成概述） |
| `/milestone status` | 只读看板：当前里程碑范围、路线图进度、已含哪些迭代、下一个该开的迭代——一眼看清进度，不改任何东西 |

收口、废弃、调整方向仍用自然语言说即可（不强制走命令）。`origin/` 里的文件是你的原材料、归你管，合成后真源以 `.ai/MILESTONE.md` 为准。

### PRD 先行（大规格版本化）

如果你的项目是**一份大 PRD**（产品需求文档）驱动的，光有里程碑那张"有损路线图"扛不住组件级的精确细节（精确文案、校验规则）——它是路线图，天生会把细节磨掉。PRD 先行给你补上这条：把 PRD 按模块**逐字切成切片**存进 `.ai/references/prd/`（一字不改、可跨改版审计），路线图管方向、切片管细节，各司其职。这是**可选加层**——项目要用才用，不用则整套按兵不动，不影响你原来的迭代/里程碑习惯。

**首切怎么进**：不用单独一个命令。你开里程碑时（`/milestone`），只要喂进去的 brief 就是一份大 PRD，AI 会认出来、提议把它切成切片，跟你确认拆法后落盘——一份输入同时喂路线图和切片两个海拔。

**PRD 出了新版怎么办**——这是最需要协议兜底的地方，两个命令：

| 命令 | 作用 |
|---|---|
| `/prd update` | **改版同步**：给新版原文 + 说一句改了啥 → AI 检测到底哪些模块变了（**以你说的改动清单为主，机器逐字 diff 作防漏网**，两边对不上会当场问你）→ 重新切受影响的切片，但**先把旧版整份冻进快照**（`.archive/`）再更新最新版，旧规格永远查得回 → 报一份**三态影响面**：这次改动牵连到的活分"还没开工 / 正在做 / 已经收口"三类摆给你看，每步都等你确认 |
| `/prd status` | 只读看板：PRD 当前版本号、各模块现状、最近一次改版影响到了谁——一眼看清，不改任何东西 |

**关键保证——绝不静默动你冻结过的活**：改版最危险的是"你按旧版验收过的工作被悄悄架空"。所以三态影响面只**亮牌给你定夺**，AI 绝不自动去重改任何已冻结 / 已收口的迭代。正在做的迭代要不要按新版重走、已收口的要不要开新迭代承接，都由你拍板。机制真源在 `Coder/40_Context_Management/prd-update.md`，这里只讲怎么用。

### `/review` 与独立复核

平时 P5 收口会做一次**同上下文简要自评**——便宜、快，但本质是"AI 给自己写的代码换个口吻打分"，盲点可能照样在。想要**真·独立**的复核时：

- **手动单跑**：任何时候输 `/review`，AI 会**另起一个全新上下文的子 agent** 来审。这个子 agent 只拿到规格（`AC_LIST` / `TECH_PLAN`）、产物（`git diff`）和 AI 的自评结论，**看不到 AI 原来的推理过程**——所以它不会跟着原作者一起想当然，而是拿验收清单逐条核对：这条 AC 到底兑现了没有？拿不准就判没过。
- **项目级常开**：某个项目你希望长期严格把关，就在 `.ai/local-constraints.md` 写 `Review Policy: independent_review: on`，之后**每次 P5 收口自动**跑独立复核，不用每轮重输。默认是关的——不是每个项目都值得这道成本。
- **牙齿**：独立复核 refute 掉一条"已满足"的 AC，或发现 Must Fix，就**阻断收口**，退回去修（修到真过、不许降级蒙混）。
- **诚实边界**：如果运行环境起不了子 agent，AI **不会**偷偷用自评冒充独立复核，而是如实标"独立复核未执行"，让你自己决定要不要另起 agent 复核。

### `/butler:preference` 偏好探针（实验性）

让 AI 在长期协作中**学习你的设计风格**，并在你**在场**时用它给出更合你意的提议。

**它怎么工作**

1. **采集**（经一次同意后默认开）：AI 在你做关键决策时（选项选择、打回方案、直接纠正）把你的**取舍倾向**记成信号。首次会问你一次是否同意，答应后就默认在 butler 项目里自动攒，随时可 `/butler:preference off` 全关。
2. **蒸馏**（默认开）：在迭代/里程碑收口或你说 `/butler:preference distill` 时，把信号归纳成偏好。**一条偏好要在 ≥2 个不同项目里一致出现，才会晋级为"跨项目通识"**——单项目重复不算，避免把局部口味当普适。
3. **反哺**（默认关，`/butler:preference reback on` 才开）：开启后，AI 只在**有监督**工作里（P2/P3 提案、选项排序）参考你的风格，把你常选的前置或设默认——你随时能否决。

**关键边界**

- **只学你亲手的选择，不学模型自己的**。`/butler:dangerous` 无人值守模式**完全不碰偏好**：既不参考、也不把模型的自主决策记成你的偏好。偏好是"人在回路"的东西，模型自己跑的时候用不上它。
- **反哺只是参考，不是命令**。偏好永远压不过你当下的明确指令；你这次怎么说就怎么来，AI 还会把这次"偏好让位于指令"记下来修正自己。
- **数据存在 butler 仓库之外**（默认 `~/.butler/preferences/`，可用 `BUTLER_PREF` 指定），跨项目共用、与规则仓库解耦。只记决策倾向的抽象，**不记业务数据或敏感内容**。
- **不碰你的迭代**。探针是旁路观察者，从不写 `.ai/`、不卡流程，坏了也不影响迭代。
- 想看它学到了什么，让 AI 读 `~/.butler/preferences/profile.md` 的"通识层"即可。（首次采集会自动初始化外置存储；也可手动跑 `./scripts/preference-init.sh`。）

### 自动测试证据（无证据不算通过）

P5 里写“测试跑过了”“127 tests passed”只是结论，不再单独算证据。完整迭代的自动测试会由 Butler 驻留工具实际执行，并在项目 `.ai/verification-evidence/` 留下机器 record：准确 argv、工作目录、起止时间、子进程退出码、stdout/stderr、字节数和 SHA-256。`VERIFY_REPORT.md` 必须逐 AC 引用 evidence ID；收口后证据整包进入 `.ai/iterations/ITER-NNNN/evidence/`。

复核时会明确标出三种强度：`reported`（只听到声称，不能打绿）、`captured`（证据文件和摘要已校验）、`reproduced`（复核者真的重跑并生成新证据）。只有第三种能说“复核者复现”。

证据日志会进入项目历史，所以**不要捕获可能输出 token、密钥或用户数据的命令**；应把测试改成只输出安全的机器摘要。日志超出上限会标 `incomplete`，不会假装通过。具体 schema 与命令见 `tools/verification-evidence/README.md`。

收口还会运行只读状态审计器，对账台账、归档、交付、证据、知识折叠和 Butler 发布元数据。Butler 自身在提交前可用 `--allow-unreleased`，但输出会明确标 `UNRELEASED`；切版前仍要在干净工作树无此参数再审一次，二者不能混称。

### 人测回环（交付自测桥）

验证（P5）时总有一小撮东西**机器测不了**——真机上的视觉观感、动画顺不顺、真人主观感受、依赖外部通道（短信、第三方人工审核）之类。这些 AI 会尽量先用自动化 / 弱验证顶，实在顶不了、只能你亲自看一眼的，就走**交付自测桥**让你来拍板：

- **会发生什么**：AI 自动在你本机**弹出一个浏览器页面**（GitHub 风格的分步流程页），把每个待你确认的项列清楚——测什么、一步步怎么操作、期望看到什么。
- **你要做什么**：对每一项选一个**四态**，可加备注：

  | 你的选择 | 含义 | AI 之后怎么做 |
  |---|---|---|
  | **通过** | 你验了，没问题 | 计入收口 |
  | **未通过** | 有问题（备注写现象） | 拿你的备注当线索去返修，修好再来 |
  | **延后处理** | 现在没法测 | 记一笔欠债、**不挡收口**，等你有空再清 |
  | **跳过** | 这次不测、也不算欠债 | 记 N/A，略过 |

- **提交后**：页面自动收走，**AI 立刻继续**——它这段时间一直在后台等你提交，你一点"提交"它就接着往下跑。
- **无人值守时（危险模式）**：没人能当场点，AI **不会弹页面**（否则会一直卡着），而是把这些残余**如实记进欠债账、绝不假装通过**，等你回来按迭代补测。

> 这个桥是 butler 自带的小工具（Node 零依赖），**不会往你项目里拷文件**——AI 直接调用 butler 仓里的那一份。你什么都不用装。

## 6. 常见问题与对策

### AI 跳过了 P1-P5 直接写代码

**原因**：AI 把任务判定为"极小"走了简化路径，或者根本没读规则。

**对策**：
- 确认 CLAUDE.md / .cursorrules 已正确配置
- 明确要求："请按 P1 开始分析"
- 如果 AI 跳过，直接打断："回到 P1，先产出 CONCEPT.md"

### AI 读了规则但执行不稳定

**原因**：规则文件太多，AI 在长上下文下 instruction-following 退化。

**对策**：
- 在 CLAUDE.md 中内联最关键的约束（而不是只写文件路径引用）
- 分阶段提醒："我们现在在 P2，请产出 AC_LIST.md"
- 每个阶段结束时显式 ACK，强化 AI 对流程的感知

### 基地车部署失败或不完整

**原因**：AI 没有先执行侦察（Scouting），直接开始创建文件。

**对策**：
- 明确要求："先侦察项目环境，再展开基地车"
- 检查 AI 是否先读了 `mcv-deployment.md`

### 跨会话丢失上下文

**原因**：上一个会话没有产出 `02_SESSION_HANDOFF.md`。

**对策**：
- 在结束会话前告诉 AI："请生成 02_SESSION_HANDOFF.md"
- 新会话开始时："请读取 .ai/02_SESSION_HANDOFF.md 恢复上下文"

## 7. 获得稳定结果的核心原则

1. **规则必须自动注入**：靠 CLAUDE.md 或等价机制，不要靠手动每次粘贴。
2. **核心约束内联到注入文件**：最关键的 3-5 条规则直接写在 CLAUDE.md 里，不要只留文件路径。
3. **按阶段推进**：不要一次性把任务和所有上下文倒给 AI。先 P1，确认后 P2，确认后 P3...
4. **显式 ACK 是你最强的杠杆**：P2 和 P3 的 ACK 机制保证 AI 不会跑偏。用好它。
5. **及时打断**：发现 AI 偏离流程时立即纠正，不要等它做完再返工。
6. **长任务分段交接**：超过一个会话能完成的任务，务必让 AI 生成 handoff 文件。

## 8. 规则体系速查

```
Coder/
├── 00_System_Prompt/          # 身份与总调度
│   ├── identity.md            # 角色定义与工程哲学
│   └── logic-protocol.md      # 读取协议、模块激活、流程总调度
├── 10_Domain_Stack_Profiles/  # 技术栈规则（按需启用）
├── 20_Workflow_Lifecycle/     # 核心工作流
│   ├── lifecycle.md           # P1-P5 状态机（最重要）
│   ├── concept-schema.md      # P1 产物模板
│   ├── acceptance-schema.md   # P2 产物模板
│   ├── tech-plan-schema.md    # P3 产物模板
│   ├── verify-schema.md       # P5 产物模板（分道回填 + 分级置信 可靠/弱/待人）
│   ├── iteration-schema.md    # 迭代号/台账/锁定纪律
│   ├── milestone-schema.md    # 里程碑（大版本）号/台账/路线图/版本级交付
│   ├── versioning-schema.md   # 提交规约 + 版本治理：commit 格式/VERSION/CHANGELOG/tag/semver/切版仪式/部署戳
│   ├── delivery-summary.md    # 交付总结规范（含固定格式 HTML 阅读视图 §9）
│   ├── mcv-deployment.md      # 基地车部署协议
│   ├── mcv-update.md          # 基地车升级协议
│   ├── progressive-handoff.md # 渐进式交接
│   └── maintenance-boundaries.md # 维护边界
├── 30_Quality_Gate/           # 质量门禁
│   ├── linting.md             # 提交前自检清单
│   ├── testing-strategy.md    # 自动化优先 + 分道口径 + 代理验证 + 验收映射
│   ├── review-standard.md     # 通用审计准则
│   └── correction-contract.md # 纠错收口契约（P4 常驻底线）
├── 40_Context_Management/     # 上下文治理（长任务必读）
│   ├── context-persistence.md # 状态外化与阶段结晶
│   ├── handoff-spec.md        # 02_SESSION_HANDOFF.md 格式契约
│   └── role-switch.md         # Architect/Coder/Reviewer 角色切换
├── 50_Extension_Ideation/     # 脑暴扩展
├── 55_Extension_ConvergenceLoop/ # 收敛闭环扩展（/butler:loop 升档）
├── 60_Extension_CodeReview/   # 代码审查扩展
├── 65_Extension_Dangerous/    # 无人值守长程自治扩展（实验性）
├── 70_Extension_Preference/   # 偏好探针扩展（实验性，外置存储）
└── 99_Business_Extension/     # 业务约束（最高优先级）
```
