# 更新日志 (Changelog)

本文件记录 butler 规则仓库的发布历史。版本号遵循[语义化版本](Coder/20_Workflow_Lifecycle/versioning-schema.md)：`MAJOR.MINOR.PATCH`。

每个版本聚合自上次发布以来收口的若干迭代（ITER），**只引用** `.ai/ITERATIONS.md` 与 `deliveries/`，不复述迭代细节。版本号机器真源是仓库根 `VERSION` 文件。

## [3.4.0] - 2026-08-01

向后兼容的工作流与宿主集成增强版，聚合 ITER-0096–ITER-0101：新增旁路工作回执、统一语义 Router 与会话转迭代入口，完善开源入口和沟通风格，并修复升级器 hook 摘要、Codex plugin 校验运行时及 UTF-8 setup 回声。迭代时间线见 `.ai/ITERATIONS.md`，升级动作见 `migrations/v3.4.0.md`。

## [3.3.0] - 2026-07-28

向后兼容的项目配置结构化版本，聚合 MILE-0013 的 ITER-0093–ITER-0095。版本级交付路径为 `deliveries/milestones/MILE-0013-project-config-structure.md`，迭代时间线见 `.ai/ITERATIONS.md`，升级动作见 `migrations/v3.3.0.md`。

## [3.2.0] - 2026-07-26

向后兼容的能力新增版，聚合 ITER-0090–ITER-0092：新增 Butler 机器级 setup 命令，并完成 MILE-0012 轻量 TDD Red→Green 配对证据、P5/Goal 收口门与 pytest dogfood。版本级交付见 `deliveries/milestones/MILE-0012-lightweight-tdd-pair-evidence.md`，迭代时间线见 `.ai/ITERATIONS.md`，升级动作见 `migrations/v3.2.0.md`。

## [3.1.0] - 2026-07-23

向后兼容的能力新增版，聚合 MILE-0010、MILE-0011 的 ITER-0083–ITER-0089。版本级交付见 `deliveries/milestones/MILE-0010-long-horizon-scale-governance.md` 与 `deliveries/milestones/MILE-0011-deterministic-artifact-pipeline.md`，迭代时间线见 `.ai/ITERATIONS.md`，升级动作见 `migrations/v3.1.0.md`。

## [3.0.0] - 2026-07-22

不兼容的需求治理契约升级版，聚合 MILE-0009 的 ITER-0075–ITER-0082。Butler 从单份 PRD 持续改版升级为需求收件箱、独立多 PRD 版本、钉版引用、事务化更新与 Monorepo 工作区范围门禁的完整链路；既有项目需要显式迁移旧 PRD 结构并刷新 hook，不能直接把新结构视为已部署。

升级步骤见 `migrations/v3.0.0.md`，迁移指南见 `docs/prd-migration-guide.md`，版本级交付见 `deliveries/milestones/MILE-0009-prd-inbox-monorepo-governance.md`。

## [2.18.0] - 2026-07-20

向后兼容的能力新增版，聚合 ITER-0068–ITER-0071。

- **ITER-0068**：里程碑候办区与延迟编号——讨论稿不占号，开工才领号，未绑迭代可退回候办。
- **ITER-0069**：多方向候办拆分——一方向一候办键、一索引块、一草稿文件，禁止混装。
- **ITER-0070**：Pi 宿主适配器——TypeScript 扩展拦截 write/edit 调 Python 门禁，setup.sh 安装，文档多宿主化。
- **ITER-0071**：说人话补「自造缩写」标准——artifact-style 收编掐短词/自造缩写，产物范例常驻。

升级见 `migrations/v2.18.0.md`，迭代交付见 `.ai/ITERATIONS.md`。

## [2.17.0] - 2026-07-18

向后兼容的工程化能力新增版，聚合 MILE-0007 的 ITER-0056–ITER-0060。版本级交付见 `deliveries/milestones/MILE-0007-engineering-hardening.md`，迭代时间线见 `.ai/ITERATIONS.md`，升级动作见 `migrations/v2.17.0.md`。

## [2.16.0] - 2026-07-17

向后兼容的能力新增版，聚合 ITER-0055。基地车现在严格区分会话启动目录与施工项目根：用户点名路径优先，否则只接受最近已部署 Butler 根或 Git 根，目标不唯一时零写入退出。Claude/Codex 的 16 个工作流入口、MCV/升级协议与 Codex patch adapter 共用同一解析契约；绝对 target 可跨 cwd，相对路径不能从聚合目录偷渡选中子仓。迁移见 `migrations/v2.16.0.md`，交付见 `deliveries/ITER-0055-project-root-deployment-boundary.md`。

## [2.15.0] - 2026-07-17

向后兼容的能力新增版，聚合危险模式自治完成的 ITER-0054（MILE-0006 R4/收官）。`scripts/setup.sh` 现在统一安装两宿主：保留 Claude 全局配置、命令和沟通风格，在 Codex CLI 可用时同时安装/刷新个人 Butler plugin；无 Codex 时明确跳过，不破坏 Claude 安装。

新增标准库 `render-project-entrypoints.py`，从 CLAUDE/AGENTS 两模板和单一 rule-card 幂等生成或升级目标项目双入口。外层 Butler 管理区、各自 user-managed 内容、管理区外用户前后缀和文件权限都有确定保护；marker 异常 fail-closed。MCV 首次部署、butler-upgrade 和 migration schema 共用该工具，并新增 `[regen-entrypoints]` / `[global-install]` typed 操作，历史 `[regen-claude]` 升级为双入口兼容动作。

隔离回归覆盖 renderer 7 场景、setup 有/无 Codex 两分支、R1–R3 scripts、124 hook tests 与官方 plugin validator。至此 MILE-0006 的规则发现、8 skills、apply_patch hooks、统一安装和双入口部署升级全部闭环。边界不变：hook trust 仍由用户完成，PreToolUse 不是 sandbox。升级见 `migrations/v2.15.0.md`，迭代交付见 `deliveries/ITER-0054-dual-host-deployment-upgrade.md`，里程碑交付见 `deliveries/milestones/MILE-0006-codex-dual-host-compatibility.md`。

## [2.14.0] - 2026-07-17

向后兼容的能力新增版，聚合危险模式自治完成的 ITER-0053（MILE-0006 R3）。Butler 共享 hook dispatcher 新增 canonical `apply_patch` 输入适配：支持 add/update/delete/move、多文件和多 hunk，逐 target 复用现有 PreToolUse 门禁与 PostToolUse 提醒；ledger 的非法状态、双 active 和同 patch 关旧开新也能按 patch 增量判断。

Codex plugin 默认发现 `hooks/hooks.json`，通过薄包装器从 `BUTLER_PATH` 调用共享 Python 真源，并分别保持 gate fail-closed、advisor fail-open。pytest 从 109 扩到 124 个用例；真实 Codex 已验证无四件套 phase deny、protected-path deny、冻结四件套 allow，以及 MILESTONE advisory 上下文注入。

本版仍不是完整安全边界或全面兼容：hook 首次启用须用户审阅信任，PreToolUse 不替代 sandbox，也不保证覆盖 shell/MCP；setup、目标项目双入口和既有升级归 R4。升级执行 `[global-install] bash scripts/install-codex-plugin.sh` + `[restamp]`，目标项目部署结构本身 `[no-op]`。详见 `migrations/v2.14.0.md` 与 `deliveries/ITER-0053-codex-apply-patch-hooks.md`。

## [2.13.0] - 2026-07-17

向后兼容的能力新增版，聚合危险模式自治完成的 ITER-0052（MILE-0006 R2）。新增 `plugins/butler/` Codex plugin，内含 PRD、review、milestone、upgrade、ideation、preference、loop、dangerous 八个 focused skills；仓库 `.agents/skills/` 用相对软链暴露同一份实体源，避免 repo discovery 与 plugin 分发双写漂移。

新增 `scripts/install-codex-plugin.sh`，使用官方 plugin creator、cachebuster、validator 与 `codex plugin add` 完成个人 marketplace 的幂等安装/刷新，并用安装版本后置断言防 CLI 假成功；新增 `scripts/verify-codex-workflows.sh` 做 8 skills、软链和高风险 invocation policy 回归。`butler-loop` 与 `butler-dangerous` 禁止隐式触发，保持郑重显式门槛。

本版仍不是全面兼容：Codex hooks 与 `apply_patch` 机械门禁归 R3，目标项目双入口部署/升级归 R4。对既有部署项目为 `[no-op]` + `[restamp]`；需要全局 Codex 工作流的维护者另执行 `[global-install] bash scripts/install-codex-plugin.sh`。详见 `migrations/v2.13.0.md` 与 `deliveries/ITER-0052-codex-workflow-plugin.md`。

## [2.12.0] - 2026-07-17

向后兼容的能力新增版，聚合 ITER-0051（MILE-0006 R1）。Butler 仓根新增 Codex 原生 `AGENTS.md`，让 Codex 能自动发现这是规则仓、按固定顺序恢复共同 `.ai/` 状态，再按指针读取 `Coder/` 真源；同时新增未来目标项目使用的 `templates/AGENTS.md.template`、双宿主架构说明和零依赖结构自检脚本。

本版只叫“Codex 兼容地基”，不宣称全面兼容：8 个 skills/plugin 留给 R2，Codex hooks 与 `apply_patch` 输入适配留给 R3，目标项目首次部署与升级时自动生成双入口留给 R4。Claude Code 的入口、命令、hooks、setup 与 Python 规则算法没有行为变化，既有 109 个 hook 测试全部通过。

对已部署项目为 `[no-op]` + `[restamp]`：不自动新增 `AGENTS.md`，只需按现有版本戳机制更新到 v2.12.0；详见 `migrations/v2.12.0.md`。交付见 `deliveries/ITER-0051-codex-compatibility-foundation.md`。

## [2.11.0] - 2026-07-16

能力增量版，给「说人话」硬标准加了第四条，从三条变四条。

起因是 butler 写出来的中文——不管产物还是对话——常带一股英语思维直译的味道：把一整句判断压成生造的名词（像"两态坐实""零行为变化"），拿冒号、引号、箭头顶替"因为 / 所以 / 还是"这类连词，英文变量光秃秃塞在句子里，还为了显精练把字砍到读着发紧发卡。原来的说人话三条只管到词一层（术语解释、比喻落地、英文别裸奔），管不到"整句是不是中文的造句法"，所以这种句子能顺利通过自检。

这一版新增**标准四·说中文，不写翻译腔**，落在真源 `Coder/20_Workflow_Lifecycle/artifact-style.md §2`，配了一个好使的自检——把句子读出声，不像一个人当面会说的话就是翻译腔，重写。同时收紧了「反啰嗦」的边界（§3）：反的是注水和重述，不是砍连词、砍喘息、把句子压成名词串，流畅优先于省字。

因为 §2 是跨对话与文档的通则、被好几处按数引用，这一版把引用点一起对齐到"四条"——对话层的 `presentation-protocol.md`、目录说明 `Coder/README.md`、下发目标项目的浓缩规则卡 `templates/rule-card.md`，并给仓根对话风格文件 `communication-style.md` 的「把话说顺」补了同方向两条（别写翻译腔、流畅优先于省字），让对话和产物守同一条口径。

本版为简化直改、无 ITER 号（单一主题的书写口径增补）。对已部署项目：规则卡内容变了，升级时要重新注入目标 `CLAUDE.md` 的 butler 管理区并重戳版本，不改任何 schema 字段、产物链、hook 或命令语义。老项目升级动作见 `migrations/v2.11.0.md`（`[regen-claude]`+`[restamp]`）。

## [2.10.1] - 2026-07-15

修订版，不改变任何行为。这一版收紧了 butler 仓根的个人配置文件 `communication-style.md`，给它加了一节「把话说顺（短 ≠ 碎）」。新规矩要求叙述用连贯的中文逻辑：话可以短，但要让人顺着一条逻辑线读下去，因果、转折、递进用连词接起来，别用破折号插入、括号套括号、斜杠堆名词把话切成碎片。这一节放在「说人话」和「别抛菜单」之间，与「说人话（简短 ≠ 好懂）」做对仗的姊妹条，反例取自真实病文、正例是它顺过来的样子；开头索引行也补上了「叙述连贯」。其余规矩与全部 ❌/✅ 例子逐条保留，没有语义删改。因为这个文件走全局 `@import`、不进 `templates/`、也不下发目标项目，所以对已部署项目零结构影响；正本随 `git pull` 更新后，下一个会话就会读到新版，无需重跑 `setup.sh`。老项目升级动作见 `migrations/v2.10.1.md`（`[no-op]`+`[restamp]`）。

## [2.10.0] - 2026-07-14

向后兼容能力新增版。聚合 ITER-0050（自 v2.9.0 起新收口的唯一迭代，**MILE-0005「butler 命令命名空间系统」R4·收官**）。本迭代落最后两个高风险命令——`/butler:loop`（收敛闭环死磕）+ `/butler:dangerous`（无人值守长程自治），把命名空间补齐、**MILE-0005 整体收口**。**唯一新面是风险闸**：命令化后敲一下就触发的便利**不得降低**它们「该被郑重、显式触发」的门槛——薄壳不复述护栏 / 熔断 / 自审门算法（守 DRY），改用 ① frontmatter `description` 带显式 ⚠️（菜单可见）、② 第 0 步前置风险提醒（dangerous=实验性/无人值守/建议隔离环境、loop=高强度/长时/消耗大）、③ 把真正的闸交回引擎（dangerous 走 §3 回声 + §3.1 announce-on-read + §7 护栏；loop 走 §6 定量熔断）。两命令结构不同：`/butler:loop` 一次性 P4 升档（无持久态·无 `off`·跑到全绿或熔断、近乎无参），`/butler:dangerous` 空参=开启（走引擎风险闸）/ `off` 关 / `status` 只读，持久开关外化当前项目 `.ai/local-constraints.md` `dangerous`、跨会话 announce-on-read。同时把活规则与人读文档里作命令引用的旧名 `/loop`·`/dangerous` **统一迁为 `/butler:*`**（22 文件，含全批最宽迁移面）；**`/loop` 与 Claude Code 自带 `/loop` 撞名的一处 harness 引用刻意保留不迁并加注澄清**；旧名仍作触发被识别。**触发名迁移刻意不碰 `templates/` 部署面**（`rule-card.md` / `templates/preference/profile.md` 保留 `/loop`·`/dangerous`）——命令是靠全局软链的个人工具、不下发目标项目，目标项目里保证生效的是散文旧名，故不触发 `[regen-claude]`、部署契约零变化。按 semver「新增两条命名空间命令能力」取 **MINOR**（`v2.9.0`→`v2.10.0`，十进位）。新命令仍由 R1 整目录软链自动托管、**无需**重跑 `setup.sh`。对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.10.0.md` 为 `[no-op]`+`[restamp]`）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`；MILE-0005 里程碑级交付见 `deliveries/milestones/MILE-0005-command-namespace-system.md`。老项目升级动作见 `migrations/v2.10.0.md`（`[no-op]`+`[restamp]`）。

[2.10.1]: 自 v2.10.0 起 style(voice) 收紧 communication-style.md（加「把话说顺（短 ≠ 碎）」一节，PATCH）
[2.10.0]: 自 v2.9.0 起聚合 ITER-0050（MILE-0005 R4·里程碑收官）

## [2.9.0] - 2026-07-14

向后兼容能力新增版。聚合 ITER-0049（自 v2.8.0 起新收口的唯一迭代，**MILE-0005「butler 命令命名空间系统」R3**；里程碑余项 R4 待续，故本版为里程碑进行中的一次迭代切版）。本迭代落全批**参数面最宽**的命令 `/butler:preference`——偏好探针开关的薄壳路由器：4 子命令 `on`/`off`（隐私总开关）、`reback on|off`（影响回路开关，全批**唯一二级参数**：首 token 是 `reback` 时再读第二 token）、`distill`（手动蒸馏），外加空参=只读状态回声（薄壳新增默认，纯读不写、与 `/butler:milestone status` 同构）。薄壳委托 `preference-probe-engine` 真源、不复述同意协议 / 采集蒸馏反哺算法 / 安全底线，收尾按 §2.3 硬要求回声状态。同时把活规则与人读文档里作命令引用的旧名 `/preference` **统一迁为 `/butler:preference`**（引擎 / logic-protocol / local-constraints-schema / dangerous-engine / Coder README / HUMAN_GUIDE / README / 项目 digest 约 13 处；旧名仍作触发被识别）。**触发名迁移刻意不碰 `templates/` 部署面**（`rule-card.md` / `templates/preference/*` 保留 `/preference`）——`/butler:preference` 是靠全局软链的个人命令、不下发目标项目，目标项目里保证生效的是散文旧名，故不触发 `[regen-claude]`、部署契约零变化。按 semver「新增一条命名空间命令能力」取 **MINOR**。新命令仍由 R1 整目录软链自动托管、**无需**重跑 `setup.sh`。对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.9.0.md` 为 `[no-op]`+`[restamp]`）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.9.0.md`（`[no-op]`+`[restamp]`）。

[2.9.0]: 自 v2.8.0 起聚合 ITER-0049（MILE-0005 R3）

## [2.8.0] - 2026-07-14

向后兼容能力新增版。聚合 ITER-0048（自 v2.7.0 起新收口的唯一迭代，**MILE-0005「butler 命令命名空间系统」R2 批量铺开**；里程碑余项 R3–R4 待续，故本版为里程碑进行中的一次迭代切版）。R1 打好命名空间地基后，本迭代照 `/butler:review` 范本**批量落三个薄壳命令**：`/butler:milestone`（里程碑录入 / `status` 只读看板，大 PRD 并进 `prd-split`）、`/butler:upgrade`（已部署项目主动升级，走 `migrations/` 区间幂等）、`/butler:ideation`（需求脑暴、不进执行主线、不冻结）——三者均为薄壳路由器：读对规则进上下文、按 `$ARGUMENTS` 分流、委托真源不复述算法。同时把规则正文里 `/butler-upgrade` 这个此前从来只是散文触发词、并无真实命令文件的旧名，**统一迁为 `/butler:upgrade`**（首次为它落真命令文件）。按 semver「新增三条命名空间命令能力」取 **MINOR**——触发名迁移的破坏面被关在**维护者个人命令别名**这一层，butler 的 semver 按目标项目部署契约定范围，那一面零变化。**新命令由 R1 的「整目录软链」自动托管**：v2.7.0 已把整个 `.claude/commands/butler/` 目录软链进全局，本版新增命令**自动**在所有项目可用、**无需**重跑 `setup.sh`——这正是 R1 选整目录软链而非逐文件软链的兑现点。对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.8.0.md` 为 `[no-op]`+`[restamp]`）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.8.0.md`（`[no-op]`+`[restamp]`）。

[2.8.0]: 自 v2.7.0 起聚合 ITER-0048（MILE-0005 R2）

## [2.7.0] - 2026-07-14

向后兼容能力新增版。聚合 ITER-0047（自 v2.6.1 起新收口的唯一迭代，**MILE-0005「butler 命令命名空间系统」R1 地基**；里程碑余项 R2–R4 待续，故本版为里程碑进行中的一次迭代切版）。本迭代把 butler 的 slash 命令从扁平单文件升级为 **`/butler:` 命名空间体系**（Claude Code 里子目录即命名空间前缀、冒号分隔）：命令文件由 `.claude/commands/butler-prd.md` 收进 `.claude/commands/butler/prd.md`、破坏性改名 `/butler-prd`→`/butler:prd`（路由三分支一字未改）；新增 `/butler:review` 薄壳命令作命名空间第二个成员兼后续迁移范本（默认当前上下文自检 / `independent` 另起干净子 agent 独立复核）；`scripts/setup.sh` 由逐文件软链改为软链整个 `butler/` 命名空间目录、并含旧扁平软链的迁移清理。按 semver「新增 `/butler:` 命名空间这一可扩展能力」取 **MINOR**——改名的破坏面被关在**维护者个人命令别名**这一层，butler 的 semver 按目标项目部署契约定范围，那一面零变化。分发与 ITER-0045/0046 同模型（全局机器级软链、不进 `templates/`、不逐项目部署）：对目标项目 `.ai/` 部署面零结构影响（`migrations/v2.7.0.md` 为 `[rename]`〔个人命令层〕+`[no-op]`+`[restamp]`〔部署面〕），既有安装升级需一个**机器级动作**——重跑 `./scripts/setup.sh`（自动清旧软链 + 装命名空间目录软链）。

聚合迭代清单见 `.ai/ITERATIONS.md`，各迭代人类可读交付见 `deliveries/`。老项目升级动作见 `migrations/v2.7.0.md`（`[rename]`+`[no-op]`+`[restamp]`）。

[2.7.0]: 自 v2.6.1 起聚合 ITER-0047（MILE-0005 R1）

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
