# 更新日志 (Changelog)

本文件记录 butler 规则仓库的发布历史。版本号遵循[语义化版本](Coder/20_Workflow_Lifecycle/versioning-schema.md)：`MAJOR.MINOR.PATCH`。

每个版本聚合自上次发布以来收口的若干迭代（ITER），**只引用** `.ai/ITERATIONS.md` 与 `deliveries/`，不复述迭代细节。版本号机器真源是仓库根 `VERSION` 文件。

## [2.6.1] - 2026-07-13

不改变行为的修订版（PATCH）。收紧 v2.6.0 新增的沟通风格正本 `communication-style.md` 的措辞与结构——头部 5 行说明压成 1 行、各节去掉解释性铺陈只留祈使规矩、4 条「说人话」的 ❌/✅ 例子由各占两行并成一行；篇幅 77→51 行（约减三分之一）。**规矩与全部 ❌/✅ 例子逐条保留，无一条增删或语义改动**——纯排版 / 措辞打磨，故取 **PATCH**。非完整迭代、无 ITER 号（简化直改），聚合提交 `d87b0d2`（`style(voice)`）。对目标项目零影响、`migrations/v2.6.1.md` 为 `[no-op]`+`[restamp]`；正本走全局 `@import`、路径不变，本机随 git 更新内容即生效、无需重跑 `setup.sh`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.6.1.md`（`[no-op]`+`[restamp]`）。

[2.6.1]: 自 v2.6.0 起聚合 style(voice) 收紧提交 d87b0d2

## [2.6.0] - 2026-07-13

向后兼容能力新增版。聚合 ITER-0046（自 v2.5.0 起新收口的唯一迭代，独立迭代、无所属里程碑）。本迭代把过去散在本机 Matrix 输出风格（只有切到该输出风格才生效）与多个记忆文件里的「AI 该怎么跟用户说话」规矩，**收敛成 butler 仓根唯一正本 `communication-style.md`**（随 git 跨机器同步），并由 `setup.sh` 在全局 `~/.claude/CLAUDE.md` 配置块内 `@import` 它，使其**每会话每项目常开**、与「切没切某个输出风格」无关。正本 = 原 Matrix 7 节逐字保真 ＋ 两条真增量（「话砍到骨头」折进详略、「别急着抛选择菜单」独立成节），说人话每条带一对 ❌/✅。按 semver「新增常开能力」取 **MINOR**。分发与 ITER-0045 同模型（全局机器级、不进 `templates/`、不逐项目部署）：对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.6.0.md` 为 `[no-op]`+`[restamp]`），既有安装升级需一个**机器级动作**——重跑 `./scripts/setup.sh` 装上 @import。Matrix 输出风格作为过渡产物退休（本机一次性迁移：删 `~/.claude/output-styles/matrix.md` + 拆 `claudep` 的 `--settings` 参数 + 掏薄壳三风格记忆）。

### 本版新增

- **个人沟通风格常开正本（ITER-0046 · 独立迭代）**：新增 `communication-style.md`（仓根唯一正本，8 节：基调 / 详略〔含话砍到骨头〕/ 抓重点 / 说人话〔4 条各带 ❌/✅〕/ 别急着抛选择菜单〔讨论 + 执行两侧〕/ 格式 / 结尾决策块 / 边界）；`scripts/setup.sh` 受管 heredoc 加一行 `@$BUTLER_DIR/communication-style.md`（绝对路径、幂等）；README/HUMAN_GUIDE 注册。AC1–AC6 实测（隔离 HOME 实跑 setup.sh 核 @import 行恒=1 + 幂等 + 抽路径 test -f；本机迁移后读文件核 matrix 退休 / claudep 拆参 / 记忆薄壳）；未触发独立复核（幂等 bash + 手写正本 + 文档、无契约面）。收敛去重后规矩正文只此一份（DRY），记忆改留来龙去脉薄壳、指向正本。详见 `deliveries/ITER-0046-communication-style-voice-file.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.6.0.md`（`[no-op]`+`[restamp]`；沟通风格走全局 @import、目标项目 `.ai/` 零改动，但需重跑一次 `setup.sh` 装上 @import；Matrix/claudep 本机清理为可选手动步）。

[2.6.0]: 自 v2.5.0 起聚合 ITER-0046

## [2.5.0] - 2026-07-13

向后兼容能力新增版。聚合 ITER-0045（自 v2.4.0 起新收口的唯一迭代，独立迭代、无所属里程碑）。本迭代闭掉 v2.4.0 遗留的分发缺口——`/butler-prd` 之前只住 butler 仓自身 `.claude/`、仅编辑本仓时可用，现经 `setup.sh` **全局软链**进 `~/.claude/commands/`，在**所有项目**可用；命令正文加「`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目」路径约定使其跨 cwd 成立。按 semver「新增分发能力」取 **MINOR**。选型全局软链（不进 `templates/`、不逐项目部署）：对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.5.0.md` 为 `[no-op]`+`[restamp]`），但既有安装升级到本版需一个**机器级动作**——重跑一次 `./scripts/setup.sh` 装上全局软链。

### 本版新增

- **slash command 全局下发目标项目（ITER-0045 · 独立迭代）**：`scripts/setup.sh` 加第 3 步——逐文件把 `.claude/commands/*.md` 软链进 `~/.claude/commands/`（幂等 `ln -sfn`、`compgen -G` 空目录守卫、逐文件不接管整目录、不误删用户自有命令）；`.claude/commands/butler-prd.md` 加路径约定段（路由三分支一字未改）；README/HUMAN_GUIDE 注册全局命令安装。7/7 AC，P5 隔离 HOME 端到端实跑 setup.sh 并抓修一个 `set -u` 下变量后接全角括号触发 unbound 的真 bug；未触发独立复核（幂等 bash + 文档、无契约面）。详见 `deliveries/ITER-0045-slash-command-global-distribution.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.5.0.md`（`[no-op]`+`[restamp]`；命令走全局软链、目标项目 `.ai/` 零改动，但需重跑一次 `setup.sh` 装全局命令）。

[2.5.0]: 自 v2.4.0 起聚合 ITER-0045

## [2.4.0] - 2026-07-13

向后兼容能力新增版。聚合 ITER-0044（`/butler-prd` 一等命令入口纳管，自 v2.3.0 起新收口的唯一迭代，独立迭代、无所属里程碑）。本迭代把已成型的未跟踪原型 `.claude/commands/butler-prd.md` 正式纳入版本管理，成 butler **第一个真实 Claude Code slash command 文件**——补齐历史「命令只是规则正文里的散文触发词、补全菜单零存在感」的缺。按 semver「新增命令」取 **MINOR**；但命令住 butler 自身 `.claude/`、**未进部署模板 `templates/`、未下发目标项目**，对已部署项目零结构影响（`migrations/v2.4.0.md` 为 `[no-op]`+`[restamp]`）。

### 本版新增

- **`/butler-prd` 一等命令入口纳管（ITER-0044 · 独立迭代）**：`.claude/commands/butler-prd.md` 从未跟踪原型纳管为真命令文件——PRD 先行薄壳路由器（第 0 步强制读 `references-schema` 契约 → 按 `$ARGUMENTS` 三分支 留空/贴 PRD=`prd-split` 首切·`update`=`prd-update` 改版·`status`=`prd-update §7` 只读看板 → 委托真源、声明「算法以被指向规则为准、本文件不复述」守 DRY），菜单可见 `description`/`argument-hint` 已说人话（去「薄壳/首切/真源」术语）。本迭代不改文件内容、只追认纳管 + 逐 AC 对真实文件/git 状态核（6/6 AC，未触发独立复核）。**命令 butler 自用、未下发目标项目**（记 `debt`）。详见 `deliveries/ITER-0044-butler-prd-slash-command.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.4.0.md`（`[no-op]`+`[restamp]`，命令未进部署面、目标项目零改动）。

[2.4.0]: 自 v2.3.0 起聚合 ITER-0044

## [2.3.0] - 2026-07-12

向后兼容能力新增版。聚合 ITER-0043（自 v2.2.0 起新收口的唯一迭代，独立迭代、无所属里程碑）。本迭代把用户提供的一份外部「工程宪法」prompt 用奥卡姆剃刀做减法——13 条里 butler 已有 10 条（照搬即违反其自身 DRY），只吸收 3 条真增量到哲学层与 P1 口径。全为规则正文的原则增强（无新命令 / 新产物 / 字段结构变更 / 部署面变化），按 semver 取 **MINOR**。

### 本版新增

- **工程原则增量吸收（ITER-0043 · 独立迭代）**：① **Trade-off 意识普适化**——`identity §3.1` 新增「任何方案都须交代取舍成本与潜在技术债」价值 + `presentation §5` 把「代价·取舍」从「仅 ≥2 方案对比时列」松绑为「给任何方案都须交代」；② **KISS 可操作判据**——`identity §3.1`「可解释性高于魔法」条并入「复杂到一句话讲不清就该重构」；③ **剥离伪需求 / MVP 质询**——`lifecycle P1` 新增主动质疑伪需求 / 低 ROI / MVP 的一问 + P1 质询 vs P2 冻结锁定的时序消歧。守 DRY 不双写已有原则、③ 只落 lifecycle 不碰 `concept-schema`。独立复核 APPROVE-with-nits（9/9 AC、0 refute）。详见 `deliveries/ITER-0043-engineering-principles-absorption.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.3.0.md`（`[no-op]`+`[restamp]`，部署面模板零改动）。

[2.3.0]: 自 v2.2.0 起聚合 ITER-0043

## [2.2.0] - 2026-07-12

向后兼容能力新增版。聚合 ITER-0042（自 v2.1.0 起新收口的唯一迭代，独立迭代、无所属里程碑）。本迭代修 v2.1.0 PRD 先行子系统的一个实战缺陷——给一份 Confluence 文档地址、经 MCP 直读当 `/milestone` brief 时，MILESTONE 合成了却从没切 `references/prd/`、PRD 逐字规格没落盘。修法在补规则的同时**新增一整套 PostToolUse 提醒 hook**（与既有 PreToolUse 门禁分离、fail-open、只提醒不阻断），属能力新增；且**不动任何既有非 PRD 流与现有 PreToolUse 门禁**（非回归门 `references-schema §9` 机器核过），按 semver 取 **MINOR**。

### 本版新增

- **PRD 先行触发加固（ITER-0042 · 独立迭代）**：三层一起补堵住「Confluence + MCP 直读 + /milestone」漏切通道——① `logic-protocol` 外部资料注入表从"按来源一步定落点"重构为**两拍**（来源只是取内容手段 → 落点只由内容类型决定，立"来源 ≠ 落点"命门）；② `milestone-schema §6.4` 把 PRD 分类判断从末尾默认跳过的附录步**前移**为合成 MILESTONE 前的必过闸；③ **新增 PostToolUse 提醒 hook** `templates/hooks/butler_advisor.py` + `rules/prd_split_reminder.py`（写完 MILESTONE 若 `references/prd/` 未建则经 `additionalContext` 注入条件式自检）+ `Advisory` 类型 + pytest 覆盖（109 passed）+ 部署/settings/README 接线。详见 `deliveries/ITER-0042-prd-trigger-hardening.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.2.0.md`（**首个含 `[sync-hooks]` 的配方**——既有部署需补 PostToolUse hook 副本 + settings.json PostToolUse 键 + `[restamp]`）。

[2.2.0]: 自 v2.1.0 起聚合 ITER-0042

## [2.1.0] - 2026-07-09

向后兼容能力新增版。聚合 ITER-0035 ~ ITER-0041（自 v2.0.0 起新收口），并**收口里程碑 MILE-0004「PRD 先行 + references 版本化改版同步」**（其下 R1~R6 = ITER-0036/0037/0038/0039/0040/0041，另含正交独立迭代 ITER-0035）。本里程碑给参考资料区 `.ai/references/` 补上"索引 + 渐进读"待遇，并新建 **PRD 先行一等入口 + 版本化改版同步协议**：一份 PRD 从导入→切片→挂里程碑→钉版→验收→改版同步全链路可走，细节逐字保真、跨改版可审计、已冻结/已收口工作不被静默破坏。全部为新增能力（新 schema / 新命令 / 新模块 / 可选字段），且**不动任何既有非 PRD 流**（非回归门显式保证），取区间最高级别为 **MINOR**。

### 本版新增

- **references 索引化基座（ITER-0036 · MILE-0004 R1）**：新建 `Coder/40_Context_Management/references-schema.md`——`references/prd/00_INDEX` 契约（入口 + 模块登记表 slug↔标题/章节↔首见版本）+ digest-and-point 读纪律 + "索引可摘要 / 切片必逐字原文"硬区分 + `live` 目录 vs `.archive/vN/` 版本落盘契约。详见 `deliveries/ITER-0036-references-index-schema.md`。
- **PRD 切分机制（ITER-0037 · R2）**：新建 `prd-split.md`（履行 R1 契约的产生动作层）——按 PRD 自身语义/模块边界切 `prd/<slug>.md`（逐字保真、**绝不切碎一条完整规则**）+ slug 首切分配（终身身份）+ 写 `00_INDEX`/登记表 + 小 PRD 单模块退化态 + soft 对齐（提议→确认→落盘）。详见 `deliveries/ITER-0037-prd-split-mechanism.md`。
- **首切并进 `/milestone` + 两海拔交叉指针（ITER-0038 · R3）**：`milestone-schema §6.4` 加"brief 是大 PRD"并进分支（除合成路线图外触发 `prd-split` 切片，一份输入喂方向层路线图 + 细节层切片）+ 路线项 ↔ 模块 slug 双向交叉指针。详见 `deliveries/ITER-0038-milestone-prd-entry.md`。
- **AC 钉版 `prd_version` + P2/P3/P5 接线（ITER-0039 · R4）**：`acceptance-schema` frontmatter 加**可选**字段 `prd_version`（冻结绑定、之后钉住；非 PRD 迭代逐字不变、hook 不校验）+ 版本化引用锚点（slug + 全局版本）+ `tech-plan`/`verify` 版本化引用继承与"对钉住版核而非 live 最新"（回溯读 `.archive/vN/`）。详见 `deliveries/ITER-0039-ac-prd-version-pinning.md`。
- **改版同步 `/prd update`（ITER-0040 · R5）**：新建 `prd-update.md` 改版同步动作层——变更检测（修改项清单优先 + 逐字 diff 兜底 + 对账，分歧必亮）+ 重新派生 + **先冻旧版 `.archive/v<旧版>/` 全量快照再更 live** + 三态影响面报告（没开工/进行中/已收口，**亮牌不自动**）+ 受影响活路由（amend 重冻 / 开新迭代 / 无动作）+ `/prd status` 只读看板。详见 `deliveries/ITER-0040-prd-update-revision-sync.md`。
- **登记表认亲边缘 + 非回归门 + 收尾（ITER-0041 · R6·收官）**：`prd-update §4.2` 加改名/合并/拆分跨版本认亲松边（启发式提候选→用户确认、**绝不自动认**、改名保留旧 slug、拿不准退回基础态）+ `references-schema §9` 非回归门（列不得触碰的非 PRD 流 + 判据 `git diff` 为空）+ HUMAN_GUIDE PRD 先行用法节 + 说人话自检。详见 `deliveries/ITER-0041-recognition-edge-and-nonregression-gate.md`。
- **补 `[split]` 升级接线缺口（ITER-0035 · 独立迭代，与本里程碑正交）**：`butler-upgrade §5/§6` 加 `[split]` 执行细则（起始态校验 + opt-in 迁移选择闸 + 冲突即停 + git add 拆出文件）+ 定死 `[split]` 是 opt-in 非自动 + `migration-schema §4` 交叉引用。详见 `deliveries/ITER-0035-split-upgrade-wiring.md`。

里程碑级聚合交付见 `deliveries/milestones/MILE-0004-prd-first-versioned-references.md`；聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.1.0.md`（`[no-op]` + `[restamp]`，部署面模板零改动）。

[2.1.0]: 自 v2.0.0 起聚合 ITER-0035 ~ ITER-0041（含 MILE-0004 收口）

## [2.0.0] - 2026-07-08

破坏性重构版（首个 MAJOR 之后的大版本）。聚合 ITER-0026 ~ ITER-0034（自 v1.7.0 起新收口），并**收口里程碑 MILE-0003「项目知识文件夹升级 + 帮手名册 + 说人话」**（其下 R1~R8 = ITER-0026/0028/0029/0030/0031/0032/0033/0034，另含正交独立迭代 ITER-0027）。本里程碑**重写了冷启动第一读、项目全貌产物契约与收口维护回路**——把单文件薄索引 `.ai/PROJECT.md` 升级为 `.ai/project/` 主题知识文件夹，按 semver 属**破坏性**（要求已部署老项目按迁移配方文件夹化），取区间最高级别为 **MAJOR**。

### 破坏性变更（需老项目迁移）

- **冷启动全貌产物：单文件 → 知识文件夹（ITER-0028 R2 起，butler 自身 ITER-0034 R8 落地）**：`.ai/PROJECT.md` 薄索引契约整体改写为 `.ai/project/` 知识文件夹契约（`00_INDEX` 入口 + 推荐主题集 + 每份边界 + digest-and-point 密度 + 收口按主题强制折叠 + overwrite 禁历史层）。哲学从"摘要不是百科·按需微调"反转为"越补越全的知识地图·每次收口折叠 delta"。已部署老项目须按 `migrations/v2.0.0.md`（`[split]`）把单文件文件夹化；**两态并存**——R6 前部署、尚未迁移的老项目仍受单文件分支支持，不强制立即迁。详见 `deliveries/milestones/MILE-0003-knowledge-folder-agents-plainlang.md`。

### 本版新增

- **帮手名册（ITER-0026 R1 + ITER-0030 R4）**：新建 `Coder/62_Extension_Agents/`——`overview.md` 名册总述（帮手是什么 + 通用规矩 G1–G4 唯一真源 + 触发式加载）+ 三帮手完整定义（复核 `independent-review` / 更新说明 `knowledge-fold` / 查过时 `drift-check`）。帮手 = 一份中立定义资料、用时读、临时起干净子 agent 执行、不下发到项目。详见 `deliveries/ITER-0026-agent-roster-review-split.md` / `deliveries/ITER-0030-fold-drift-helpers.md`。
- **知识文件夹维护回路（ITER-0029 R3）**：收口步④泛化为两态（文件夹态按主题必做折叠 / 单文件态按需前滚）+ 冷启动一致性自检加第 6 条「知识文件夹漂移自检」（条件不变量、单文件项目 N/A）。详见 `deliveries/ITER-0029-maintenance-loop-wiring.md`。
- **冷启动读序两态切换 + digest-and-point 读纪律（ITER-0031 R5）**：`context-persistence §6` 第一读泛化为两态（文件夹态先读 `00_INDEX` + 按需主题 / 单文件态读 `.ai/PROJECT.md`），落读地图→定向钻取→指针钻代码、不 slurp。详见 `deliveries/ITER-0031-coldstart-read-order-switch.md`。
- **部署种子 + 文件夹化迁移配方（ITER-0032 R6）**：部署即建空 `.ai/project/` 种子（`00_INDEX` 不 stub、首收口前滚生）+ `migration-schema §4` 补 `[split]` typed 标签 + 文件夹化配方形态（`[rename]`+`[split]`+`[restamp]`）。详见 `deliveries/ITER-0032-deploy-seed-and-folder-migration.md`。
- **说人话三条硬标准 + 发长文前自检（ITER-0033 R7）**：`artifact-style §2` 立「说人话三条」（术语先解释 / 比喻要落地 / 别让英文·变量裸奔）为跨对话与文档的通则·单一真源，适用面从四件套扩到所有面向人落地文档；`presentation-protocol §7` 对话层引用同守（不双写）。详见 `deliveries/ITER-0033-plain-language-standards.md`。
- **butler 自身 dogfood 迁知识文件夹（ITER-0034 R8）**：butler 拿自己当第一个真实用户，把自身 `.ai/PROJECT.md` 迁成 `.ai/project/`（`00_INDEX` + 7 主题），对齐全仓"butler 还是单文件"的旧说法，验证知识文件夹设计第一次真实落地。详见 `deliveries/ITER-0034-dogfood-knowledge-folder-migration.md`。
- **最小实现纪律（ITER-0027 · 独立迭代，与本里程碑正交）**：新增 `30_Quality_Gate/implementation-discipline.md`（P4 常驻底线——最小实现阶梯 + `butler-min:` 有意简化标记 + 修根因不打症状补丁）。详见 `deliveries/ITER-0027-implementation-discipline.md`。

里程碑级聚合交付见 `deliveries/milestones/MILE-0003-knowledge-folder-agents-plainlang.md`；聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.0.0.md`。

[2.0.0]: 自 v1.7.0 起聚合 ITER-0026 ~ ITER-0034（含 MILE-0003 收口）

## [1.7.0] - 2026-07-03

向后兼容能力新增版。聚合 ITER-0021 ~ ITER-0025（自 v1.6.0 起新收口），并**收口里程碑 MILE-0002「自动化测试最大化 + 人测 web 回环」**（其下 R1/R2/R3/R4/R5 = ITER-0021/0022/0023/0024/0025）。五个迭代均为向后兼容的规则正文新增 / 新增 butler 驻留工具 / 新增产物与文档，无破坏性变更，按 semver 取区间最高级别为 MINOR。

### 本版新增

- **自动化优先纪律 + 测试分道（ITER-0021 · MILE-0002 R1）**：`30_Quality_Gate/testing-strategy.md` 从"分层建议"升级为"竭尽一切自动化"硬纪律（含浏览器自动化 / headless 覆盖 UI、交互）；`verify-schema.md` 令每条 AC 显式分「自动道 / 人测道」回填，人测道界定为机器不可测残余。详见 `deliveries/ITER-0021-automation-first-testing-lanes.md`。
- **分级置信 + 代理验证 + 依赖感知准入（ITER-0022 · MILE-0002 R2）**：`VERIFY_REPORT.md` 增「可靠 / 弱 / 待人」分级置信档；感知类造弱自动检查（截图 diff / VLM 判图）earned 弱档不冒充绿；`dangerous-engine §7.4` 无人残余依赖感知准入闸（不阻塞异步入账 / 卡下游不硬闯 / 红线绝不假绿）。详见 `deliveries/ITER-0022-graded-confidence-proxy-and-admission.md`。
- **交付自测桥工具（ITER-0023 · MILE-0002 R3）**：新增 butler 驻留工具 `tools/delivery-selftest/`（Node 零依赖）——JSON 清单 → GitHub 风格分步流程页 → 每项四态（通过 / 未通过 / 跳过 / 延后）+ 备注 → 写 results.json → 自退；定义输入 / 输出契约。详见 `deliveries/ITER-0023-delivery-selftest-bridge.md`。
- **等待-回收-续跑接线（ITER-0024 · MILE-0002 R4）**：`human-test-bridge.md` 定义 P5 下游接线协议——`run_in_background` 起桥 + 阻塞等待 + 读结果 + 四态路由（通过→收口 / 未通过→`correction-contract` 纠错 / 跳过→N/A / 延后→入账不阻塞）+ 外部项目调用形态。详见 `deliveries/ITER-0024-human-test-bridge-wiring.md`。
- **部署 / 使用文档 + dogfood（ITER-0025 · MILE-0002 R5）**：`mcv-deployment.md §6`「butler 驻留工具调用」+ `HUMAN_GUIDE.md §5 人测回环` + `Coder/README` 注册 + 桥 `example/manifest.json` 补齐四态样例；外部调用形态端到端 dogfood 跑通（headless 四态齐全回路 exit 0）。详见 `deliveries/ITER-0025-bridge-usage-docs.md`。

里程碑级聚合交付见 `deliveries/milestones/MILE-0002-automation-and-human-test-loop.md`；聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.7.0]: 自 v1.6.0 起聚合 ITER-0021 ~ ITER-0025（含 MILE-0002 收口）

## [1.6.0] - 2026-07-02

向后兼容能力新增版。聚合 ITER-0017 ~ ITER-0020（自 v1.5.0 起新收口），并**收口里程碑 MILE-0001「冷启动可恢复性与收口知识固结」**（其下 R1/R2/R3 = ITER-0017/0018/0019）+ 独立迭代 ITER-0020。四个迭代均为向后兼容的规则正文新增 / 新增 hook 规则 / 新增产物，无破坏性变更，按 semver 取区间最高级别为 MINOR。

### 本版新增

- **`.ai/PROJECT.md` 冷启动全貌产物（ITER-0017 · MILE-0001 R1）**：新增状态取向的项目常驻摘要 + `40_Context_Management/project-digest-schema.md` + 冷启动读序接线 + 收口前滚维护 + 部署种子，补长寿项目冷启动"全貌"缺口。详见 `deliveries/ITER-0017-project-digest.md`。
- **每迭代 changelog 正式化（ITER-0018 · MILE-0001 R3）**：`.ai/01_CHANGELOG.md` 重定义为严格 ADD/EDIT/DELETE 对象级变更流 + `changelog-schema.md` + Should-Fix 迁 `VERIFY_REPORT.Remaining Risks`。详见 `deliveries/ITER-0018-changelog-formalization.md`。
- **收口门槛（ITER-0019 · MILE-0001 R2）**：新增 hook 规则 `single_active_iteration`（写 ITERATIONS 后 active 行 >1 即 deny）+ 冷启动一致性自检 5 不变量 + 原子收口仪式（`iteration-schema §5.5` 五步）。详见 `deliveries/ITER-0019-close-gate.md`。
- **提交与切版 SOP（ITER-0020 · 独立迭代）**：`versioning-schema.md`（更名「提交与版本治理协议」）新增 §5 提交规约（`type(scope): 中文描述 (ITER-NNNN)` / `chore(release)` / 非 hook 门禁 / `Co-Authored-By` 署名）+ §6 切版流程扩到 git 操作层（切版前预检复用一致性自检 → add/commit/tag/push 序列 → 切版后自检 / 提交≠切版两路径）。详见 `deliveries/ITER-0020-commit-release-sop.md`。

里程碑级聚合交付见 `deliveries/milestones/MILE-0001-coldstart-recoverability.md`；聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.6.0]: 自 v1.5.0 起聚合 ITER-0017 ~ ITER-0020（含 MILE-0001 收口）

## [1.5.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0015 ~ ITER-0016（自 v1.4.0 起新收口），两个迭代均为向后兼容的规则正文新增 / 既有字段口径强化，无破坏性变更，按 semver 取区间最高级别为 MINOR。

### 本版新增

- **handoff 格式契约补全（ITER-0015）**：`Coder/40_Context_Management/handoff-spec.md` 新增 §4 模板骨架（H1 锁死 `# Session Handoff` + 6 个固定顺序 H2 + 模板规则）与 §5 蒸馏生成流程（5 步不得跳步 + 4 条反模式）；`context-persistence.md §6` 补一行指针指向骨架与流程。补全此前"有字段、无骨架、无步骤"的半截契约，字段语义与 hook 未动。详见 `deliveries/ITER-0015-handoff-template-and-flow.md`。
- **tasks 步骤轻量引入 · 方案 A（ITER-0016）**：参照 SDD（Specify → Plan → Tasks → Implement）评估后不引入强制第五件套，而是强化 `tech-plan-schema.md` 既有 `Execution Steps` 字段——升级为可勾选 / 绑 AC / 可标依赖与并行（`[P]`）的任务清单，粒度随迭代大小；`context-persistence.md §4` 补 `task-state.md` 任务镜像作 P4 活进度板并声明 AC 仍是验收脊柱；`artifact-style.md` 新增 §5 任务清单书写口径。四件套字段结构 / hook / rule-card / README 零改动。本迭代 P2 用户 ACK、自 P3 起 `/dangerous` 自治，P5 独立复核 6/6 confirm。详见 `deliveries/ITER-0016-tasks-step-lite.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.5.0]: 自 v1.4.0 起聚合 ITER-0015 ~ ITER-0016

## [1.4.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0014（自 v1.3.0 起新收口），向后兼容新增，按 semver 为 MINOR。

### 本版新增

- **版本升级 SOP 化（ITER-0014）**：新增 `Coder/20_Workflow_Lifecycle/migration-schema.md` 定义"迁移配方"格式——配方落仓库根 `migrations/vX.Y.Z.md`、用 typed 标签（`[rename]` / `[add-field]` / `[regen-claude]` / `[sync-hooks]` / `[restamp]` / `[no-op]`）列出已部署项目升级到该版的幂等步骤，附"先校验起始态、漂移退回 ACK"契约，并回填 `migrations/v1.1.0 ~ v1.3.0`；`butler-upgrade.md` 由"现场推导差异"改为"按版本区间收集配方、按序幂等执行"（含 `.claude/hooks/` 副本同步，补 `mcv-deployment.md §5.4` 缺口），无版本戳老项目保留全量首次升级兜底；`versioning-schema.md §5` 切版流程新增"写迁移配方"必做步（无影响也写 `[no-op]`）。本迭代在 `/dangerous` 危险模式下自治完成，P5 独立复核查出并修复 v1.1.0 漏 `[regen-claude]`。详见 `deliveries/ITER-0014-migration-ledger.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.4.0]: 自 v1.3.0 起聚合 ITER-0014

## [1.3.0] - 2026-06-30

向后兼容能力新增版。聚合 ITER-0012 ~ ITER-0013（自 v1.2.0 起新收口），两个迭代均为向后兼容新增，按 semver 为 MINOR。

### 本版新增

- **四件套讲人话 + 反啰嗦（ITER-0012）**：新增 `Coder/20_Workflow_Lifecycle/artifact-style.md` 作为四件套字段正文书写口径单一来源——正文须让不懂内部机制者也读得懂（反黑话）、一律 bullet / 嵌套 ≤2 / 不复述 / 宁缺毋滥（反注水），VERIFY 用 `[x] ACn ✓ 一句话证据` 紧凑式；接线四 schema 编写规则 + `rule-card` + `Coder/README`。字段结构未动。详见 `deliveries/ITER-0012-artifact-plain-language.md`。
- **CONCEPT 分层 / 渐进展开（ITER-0013）**：`artifact-style.md` 增「渐进展开与分层」节（顶部一句话意图 + 一行一意 / 拆箭头链 + 承重引用首次解释 + 散文层与精度层不串味 + 不啰嗦 ≠ 极限压缩）；`concept-schema` 模板顶部增「一句话」块（散文意图速览，与 `Goal` 分工、向后兼容 legacy）。把「对人友好 / 对 AI 友好」统一为同一目标，唯一偏差用分层吸收。详见 `deliveries/ITER-0013-concept-layering.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.3.0]: 自 v1.2.0 起聚合 ITER-0012 ~ ITER-0013

## [1.2.0] - 2026-06-22

向后兼容能力新增版。聚合 ITER-0011（自 v1.1.0 起新收口），按 semver 为 MINOR。

### 本版新增

- **对话输出呈现协议（ITER-0011）**：新增 `Coder/00_System_Prompt/presentation-protocol.md`，把 P1-P3 方案 / 分析 / 选项类对话输出统一为「结论先行 + 统一标号 + 选项表格 + 结尾下一步」，默认固定 + 弹性、仅管较长输出；接线至 `identity` / `logic-protocol` / `rule-card`（高注意力区）/ `Coder/README`，与 `delivery-summary §8`（P5 交付摘要散文化）分场景共存。详见 `deliveries/ITER-0011-presentation-protocol.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.2.0]: 自 v1.1.0 起聚合 ITER-0011

## [1.1.0] - 2026-06-22

向后兼容能力新增版。聚合 ITER-0008 ~ ITER-0010——三个迭代均为向后兼容新增（无破坏性变更），按 semver 取区间最高级别为 MINOR。

### 本版新增

- **迭代状态封闭三态 + 机械门禁（ITER-0008）**：迭代台账状态固化为 `active` / `closed` / `abandoned` 封闭枚举，新增 `ledger_status` hook 拦截越界值（`planned` 等里程碑路线项不得写入迭代台账）。详见 `deliveries/ITER-0008-iteration-status-enum-lockdown.md`。
- **preference 项目级抑制开关（ITER-0009）**：`.ai/local-constraints.md`「Butler 功能开关」新增 `preference: on|off`（默认 on）作 per-project 采集闸；consent / 数据真源仍外置 `$BUTLER_PREF`（跨项目唯一真源），本开关不双写。详见 `deliveries/ITER-0009-preference-per-project-toggle.md`。
- **交付总结固定格式 HTML 阅读视图（ITER-0010）**：迭代 / 里程碑收口在 `.md` 之外并列产出同名 `.html`（固定格式模板 SSOT `templates/delivery.html.template`、单文件自包含、双击可离线打开）；`.md` 仍为引用真源，HTML 同守只引用不嵌入。详见 `deliveries/ITER-0010-delivery-html-view.md`。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.1.0]: 自 v1.0.0 起聚合 ITER-0008 ~ ITER-0010

## [1.0.0] - 2026-06-19

首个正式版本基线。聚合 ITER-0001 ~ ITER-0007，为 butler 规则仓库确立硬版本概念（VERSION / CHANGELOG / git tag），并把版本接入部署产物与升级协议。

### 能力基线（本版已具备）

- **三层规则体系**：SOP Core（00/20/30/40）+ Domain / Stack Profiles（10）+ Business Extension（99），职责分明不混层。
- **五阶段产物链**：P1 CONCEPT → P2 AC_LIST → P3 TECH_PLAN → P4 Execute → P5 VERIFY_REPORT，阶段间经文件传递、不依赖对话记忆。
- **迭代化需求管理**：ITER-NNNN 台账 + 工作区/归档/交付三层落盘 + "固定需求"锁定纪律；**里程碑**（MILE-NNNN）作为松耦合、可选、方向性不冻结的大版本范围层，支持对话 / `origin/` 双通道录入与 `/milestone` 命令。
- **控制状态外化**：ACK 冻结门禁、入口分流可审计、项目级 butler 功能开关（`dangerous` / `independent_review`）统一落 `.ai/local-constraints.md` 并跨会话持久。
- **基地车生命周期三协议**：部署（mcv-deployment）/ 升级（butler-upgrade）/ 维护（mcv-update），配合 PreToolUse hook 机械门禁（产物缺失 / AC 未冻结拦截源码写）。
- **扩展模块**：ideation（脑暴）/ convergence-loop（死磕闭环）/ code-review（含 opt-in 独立复核，验证者≠实现者）/ dangerous（无人值守长程自治）/ preference（偏好探针，外置存储）。
- **本版新增（ITER-0007）**：硬版本概念落地——根 `VERSION` 为版本号 SSOT、`CHANGELOG.md` 为人读发布史、git tag `vX.Y.Z` 为发布锚点；部署把规则源版本戳进目标 `CLAUDE.md`（`{{BUTLER_VERSION}}`）；`butler-upgrade` 升级为版本感知（读目标戳 vs 仓库 VERSION 报 gap、升级后重戳，版本号为辅、内容差异为主）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。

[1.0.0]: 基线版本（无前序版本可比较）
