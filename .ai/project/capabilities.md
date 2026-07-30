# capabilities（现在真能做哪些事）

> R2 新增层（旧单文件没有）：从现状盘"butler 落地后到底能干什么"。引擎正文指各扩展模块，此处只给清单 + 一句话 + 指针。

## 项目级 Butler 配置（MILE-0013）

- `tools/project-config/config.py` 提供标准库 `inspect`、`resolve`、`init`、`set` 与可导入函数，固定读取显式项目根下的 `.ai/butler.config.json`。缺失配置可严格投影 legacy Markdown；已有配置损坏、字段缺失/未知、类型错误或未知版本一律 fail-closed。
- `tools/project-config/butler-config.schema.json` 固定 schema v1 的五字段扁平合同：`schema_version`、三个布尔开关和去重非空 `profiles` 数组。写入使用同目录临时文件与原子发布，初始化不覆盖已有文件，更新失败保持原配置字节不变。
- 新部署直接生成 JSON，`local-constraints.md` 只留人类可读差异；危险模式、独立复核、偏好、进度和双宿主规则统一经 `resolve` 读取，持久修改只经 JSON `set` 写入。`butler-upgrade` 的 v3.3.0 `migrate_config` action 在同一事务内创建 JSON、收窄 Markdown并检测配置漂移；兼容期不双写。

## 轻量 TDD 配对证据（MILE-0012）

- `tools/verification-evidence/evidence.py check-tdd` 读取 TECH_PLAN `Test Strategy` 内的版本化 cycle 表，按 `tdd-<cycle>-red/green` 找现有 evidence v1 record，并校验 Red=`failed`、Green=`passed`、先后顺序及 argv/cwd/AC 完全一致。未声明 TDD 时返回 N/A、零写；`--source archive` 支持关闭态复核。V1 只证明同命令先失败后通过，不证明代码修改时序、失败原因或测试未被弱化。
- TECH_PLAN 声明 cycle 时，P5 在 VERIFY `TDD Pair Status` 投影结果并引用两条 record；`tools/goal-assurance/goal.py evaluate` 会独立复用配对检查，配对无效即 ineligible。未声明时仍为 N/A。

## 确定性五件套产物链（MILE-0011）

- `tools/artifact-pipeline/artifacts.v1.json` 与五份 canonical 模板共同定义 live 五件套的版本化结构合同；`contract.py render/init/reset/check` 按阶段安全生成并零写验形，hook advisory、状态审计和 CI 共用该合同；`migration.py plan/apply/verify/rollback` 以备份 receipt 和 hash 门控无损迁移 legacy live，历史归档只读不追罚。

## 可信 handoff 与有界状态台账（MILE-0010）

- `tools/handoff/` 从权威状态确定性生成 `.ai/02_SESSION_HANDOFF.md`，receipt 可检测来源变化、快照漂移和成品篡改；`check` 陈旧即拒绝，`sync` 幂等重建。
- `tools/state-ledger/` 把 ITER/MILE 双台账迁移为最多 20 行的根热表、固定 50 号区间冷片和有界 `.ai/state-index.json`；每片有独立 hash 回执，迁移事务化、幂等并跨分片拒绝重复。
- 身份号至少四位、超过四位自然增长，最大号和排序只看数字部分。

## 旁路工作回执（ITER-0096）

- 用户主动发起、脱离主上下文完成的代码/调研混合工作，可按 `Coder/40_Context_Management/sidework-receipt.md` 在 `.ai/sidework/` 写一份六段短回执；canonical 骨架为 `templates/sidework-receipt.md`。用户把路径交给主 Agent 后定向续接，不自动扫描目录，也不建立模型的接受/拒绝状态。
- 回执只传最终结论、成果指针、验证事实和续接入口，不提供额外代码写权限。旁路执行仍受宿主与当前 Butler 范围约束；同名使用 create-only 短序号，共享工作区如实按低归属强度披露。静态合同检查 `scripts/test-sidework-receipt.py` 已接入完整 CI。

## Claude/Codex 双宿主适配（v2.12.0–v2.16.0）

- Codex 在 Butler 仓根可原生发现 `AGENTS.md`，按固定顺序恢复 `.ai/` 状态并钻取 `Coder/` 真源；`scripts/verify-codex-foundation.sh` 可做结构回归。
- `scripts/render-project-entrypoints.py` 从两模板和单一 rule-card 幂等维护目标项目 CLAUDE.md + AGENTS.md，保留管理区外原文与两份 user-managed 内容；MCV 和 upgrade 共用该契约。
- `scripts/resolve-project-root.py` 在任何项目级读写前解析唯一施工根：用户点名路径 → 最近已部署 Butler 根 → Git 根 → 拒绝。多仓父目录不再因会话从那里启动就被当成项目。

## Codex 工作流与 hooks（v2.13.0–v2.15.0）

- `plugins/butler/` 可安装 12 个 skills：inbox/prd/review/milestone/upgrade/init/setup/ideation/preference/loop/dangerous/progress；`.agents/skills/` 软链让仓内直接发现同一真源。
- `/butler:setup` / `$butler-setup` 在确认机器级写入后只委托 `scripts/setup.sh`，分别报告 Claude/Codex/Pi 安装、跳过或部分失败；首次空白机器 bootstrap 仍从仓库脚本进入。
- `scripts/install-codex-plugin.sh` 安装/刷新个人 plugin；`scripts/verify-codex-workflows.sh` 做结构回归。loop/dangerous 禁隐式调用。
- `plugins/butler/hooks/hooks.json` 默认注册 PreToolUse/PostToolUse；共享 dispatcher 已能解析 canonical `apply_patch` 的 add/update/delete/move、多文件与多 hunk，并对每个 target 复用既有门禁/提醒规则。`scripts/verify-codex-hooks.sh` 做包装器和配置回归。
- Claude/Codex 写入适配器按每个目标的真实 Butler/Git 根重建 Context：项目内继续跑该项目门禁，无法归属项目的真实路径退出 Butler 判定并交宿主权限，缺失/坏输入仍 fail-closed；一个 Codex patch 可跨多个项目根逐根校验，任一拒绝即整次拒绝。
- 真实 Codex 已验证 phase deny、protected-path deny、allow 和 advisory 上下文注入。边界只覆盖送入 hook 的工具事件，不替代 sandbox，也不保证覆盖 shell/MCP。

## 工作流注册与分发治理（MILE-0007 R5）

- `workflows/registry.json` 恰好登记 12 个 workflow 的 Claude/Codex 名称与路径、规则真源、风险、隐式策略、语义触发、legacy aliases 和 plugin/distribution 边界。
- `scripts/sync-workflow-registry.py --write` 原子生成/校正窄元数据投影并在失败时回滚；`--check` 零写入报告 command/SKILL/openai/doc/软链/plugin/hooks/installer 漂移。
- `docs/workflows.md` 是唯一工作流人读能力表；loop/dangerous 显式禁隐式，旧 `/loop` 只登记 harness collision、不生成实体。repo discovery 和个人 plugin 可用，team/public 明确未配置。
- 专项与完整矩阵已接入 `verify-ci.sh`；源码 plugin 保持精确 VERSION，个人安装副本单独加 cachebuster。

## 持续验证与状态自证（MILE-0007 R2–R3）

- `bash scripts/verify-ci.sh` 是开发机和 GitHub Actions 的唯一完整入口：固定 Python 3.12.12、uv 0.9.28 与 `uv.lock`，运行安装、状态/证据、双宿主、hooks、Markdown 和 CI contract 全矩阵。
- `.github/workflows/ci.yml` 在 PR、`main` 与 `v*` tag 上编排 `ubuntu-24.04` / `macos-14`，Actions 固定完整 SHA；稳定汇总 check 名为 `Butler required checks`。
- `tools/codex-validators/` 固定 OpenAI Codex 官方 plugin/skill validators 的 commit、SHA-256 和许可证；空 HOME 也完整执行，缺失/篡改 fail-closed。
- `scripts/check-markdown-links.py` 离线检查仓内相对目标和 GitHub 风格 fragment，不把外网波动纳入合并门禁。
- 远端 required status checks 当前受私有仓库套餐限制；仓内能力状态为 check-provided，不能称 required-enabled。

## 可执行项目升级（MILE-0007 R4）

- `migrations/manifest.json` 是可执行迁移数据真源：从 v1.0.0 连续登记到当前版本，每个 action 有稳定 ID、有限类型、固定 domain、参数和前置条件；全部人读 recipe 一一覆盖。
- `tools/butler-upgrade/upgrade.py` 提供 inspect/plan/apply/global-install。plan 输出机器 JSON 且项目/HOME 零写入；apply 做 before-hash、排他锁、backup/restore/journal、原子替换和故障恢复。
- 双入口重生成、hook/settings、rename/add-field、restamp/no-op 是有限项目 action；split 是人工 decision，global install 是独立 machine action。未知类型、protected path、marker/hook/current drift、symlink/TOCTOU 都 fail-closed。
- Claude `/butler:upgrade` 与 Codex `$butler-upgrade` 只路由同一 CLI，不再由模型解释 Markdown 后手工迁移；16 项历史/负向/事务专项已纳入 `verify-ci.sh`。

## 核心：P1–P5 开发 SOP（默认主线）

非极小任务同时具备**派生 Goal Contract**：从 milestone/CONCEPT、AC、TECH_PLAN、task-state、VERIFY/evidence、review 与收口事实组合 objective/obligations/plan/progress/proof/verdict，不新增 GOAL 台账。六状态含 `completion-candidate`，tasks done 或宿主 complete 均不能直跳项目 complete。真源 `20_Workflow_Lifecycle/goal-contract.md`。

引用 PRD 需求集合时，AC 可用 `prd_refs` 同时钉住多份需求各自的版本与模块；P3/P5 逐项继承，legacy `prd_version` 只读兼容且两者互斥。迁移后的旧路径由 receipt/resolver 还原，不回写 closed 历史。

P4/P5 同时启用**Goal 运行时校准**：实现偏差、假设失效、范围漂移、验证失败、review finding、外部阻塞六类信号投影到 task-state，再按事实性质回 P1–P5 或诚实停；open/blocked 信号使 Goal at-risk/blocked。真源 `20_Workflow_Lifecycle/goal-calibration.md`。

P5 收口前可运行 `tools/goal-assurance/goal.py evaluate`：只读聚合 active ledger、AC、plan、calibration、hot evidence、TDD 配对（仅声明时）、review 和 completion blockers，JSON 输出 eligible/ineligible；GFC-001–008 与 TDD 负向场景全部拒绝。eligible 只准进入收口，不等于 complete。

Claude/Codex 读取同一 Goal 真相并只投影 objective/state/reason/next；原生能力缺失或失败时靠 task-state/handoff 诚实降级。目标项目从共同 rule-card 获得 `$BUTLER_PATH/tools/goal-assurance/goal.py` 驻留调用，不存工具副本。

任何非极小任务默认走五阶段状态机，每阶段产一份"产物"、下一阶段只从上一阶段的**文件**读（不靠对话记忆）：

| 阶段 | 干什么 | 产物 |
|---|---|---|
| P1 Analysis | 分析需求、识别项目类型、**主动质询伪需求/低 ROI（该剥离/缩 MVP/提替代）** | `.ai/CONCEPT.md` |
| P2 Acceptance | 定验收标准（AC）、冻结 | `.ai/AC_LIST.md`（`状态: ack-frozen`） |
| P3 Design | 技术方案 + 结构化反证；只有 `方案状态: pass` 可执行 | `.ai/TECH_PLAN.md` |
| P4 Execute | 按步骤写码，常驻纠错 + 最小实现底线 | 源码 + `.ai/01_CHANGELOG.md` |
| P5 Verify | 分道验证（自动 / 人测）+ 分级置信 | `.ai/VERIFY_REPORT.md` |

阶段定义真源 `20_Workflow_Lifecycle/lifecycle.md` + 各 schema。

## 命令（显式触发的扩展能力）

| 命令 | 干什么 | 真源 |
|---|---|---|
| `/butler:inbox` | 零写扫描或登记 `origin/` 来源，逐项分类并经确认/危险自审路由；活工作区冲突项等待，无依赖 sibling 继续 | `.claude/commands/butler/inbox.md`（薄壳，真源 `40_Context_Management/inbox-workflow.md`；机械事实由 `tools/inbox/inbox.py` 管理） |
| `/butler:ideation` | 独立脑暴、不进执行主线、不冻结（贴模糊需求 / 想法，或留空进对话）；MILE-0005 R2 迁入命名空间 | `.claude/commands/butler/ideation.md`（薄壳，真源 `50_Extension_Ideation/ideation-engine.md §3`） |
| `/butler:loop` | 收敛闭环、死磕式高强度纠错升档（**高强度·长时·消耗大、郑重触发**）；原名 `/loop`，MILE-0005 R4 迁入命名空间。一次性 P4 升档（无持久态·无 `off`·跑到全绿或定量熔断）；薄壳近乎无参、frontmatter ⚠️ + 第 0 步风险提醒、委托真源**不复述**闭环/熔断算法 | `.claude/commands/butler/loop.md`（薄壳，真源 `55_Extension_ConvergenceLoop/convergence-loop-engine.md` §3/§6） |
| `/butler:dangerous` | 无人值守长程自治（**实验性**·自审门替 ACK·强制 P5 全审护栏）；每次任务启动冻结宿主预授权上限，上限内可动态追加施工项目、范围外隔离或诚实交还。空参=开启 / `off` 关 / `status` 只读；项目开关由 `.ai/butler.config.json` 持久化，读取走 `resolve`、写入走 `set`，跨会话 announce-on-read | `.claude/commands/butler/dangerous.md`（薄壳，真源 `65_Extension_Dangerous/dangerous-engine.md` §3/§3.2/§7） |
| `/butler:preference` | 偏好探针开关（`on`/`off` 隐私总开关 / `project on\|off` 项目开关 / `reback on\|off` 反哺 / `distill` 手动蒸馏；**留空=只读状态回声**）；全局数据仍外置，本项目开关由 `.ai/butler.config.json` 持久化 | `.claude/commands/butler/preference.md`（薄壳，真源 `70_Extension_Preference/preference-probe-engine.md` §2.2/§2.3/§2.4/§6/§7） |
| `/butler:milestone` | 里程碑录入、未编号候办、`start <候办键>` 提升与 `status` 只读看板。多个可独立启动方向会拆成平级候办块，一方向一个键、一行索引、一份文件；讨论稿不占 `MILE-NNNN`，明确开工才领连续号，已绑迭代的号不回收。**brief 是大 PRD 时仍并进触发 `prd-split`** | `.claude/commands/butler/milestone.md`（薄壳，真源 `20_Workflow_Lifecycle/milestone-schema.md` §4.5/§6.4–§7.6） |
| `/butler:prd` | PRD 集合的双宿主薄入口：split 先判四态并要求首次日期证据，再把身份/模块/Workspace Scope 一次对齐；`status [prd_id] [--workspace key]` 调同一只读 CLI；`update <prd_id>` 以确认 spec 调确定性 plan/apply，强制显式目标与影响处置 | `.claude/commands/butler/prd.md` / `plugins/butler/skills/butler-prd/SKILL.md`；真源 `references-schema.md` / `prd-split.md` / `prd-status.md` / `prd-update.md` |
| `/butler:review` | **命名空间第二个真命令**（ITER-0047·MILE-0005 R1）——代码 / 产物复核薄壳路由器：默认（留空）当前上下文快速自检、`independent` 另起 fresh 子 agent 独立复核（验证者≠作者）；第 0 步没接 butler 优雅降级、委托真源不复述算法。作后续命令的复制范本 | `.claude/commands/butler/review.md`（薄壳，真源 `review-engine.md §5` / `independent-review.md` / `62_Extension_Agents/overview.md §3`） |
| `/butler:upgrade` | 已部署项目升级到最新 Butler：机器 manifest 先 dry-run，再事务 apply；split/global 分域，不解析 Markdown 散文执行 | `.claude/commands/butler/upgrade.md`（薄壳，执行真源 `tools/butler-upgrade/upgrade.py`，交互真源 `20_Workflow_Lifecycle/butler-upgrade.md`） |
| `/butler:progress` | 只读聚合当前项目进度——里程碑、迭代、Goal、验收、执行、验证、风险一页看完；`brief` 一行摘要，留空完整 9 段报告。纯只读不改文件 | `.claude/commands/butler/progress.md`（只读聚合器，数据源 `.ai/task-state.md` / `MILESTONES.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md` / `01_CHANGELOG.md`） |

## 部署与维护能力

- **全局安装（`scripts/setup.sh`）**：一次性、机器级——由 `configure-global-install.py` 先全量预检 marker/export/软链所有权，再逐对象原子维护 `BUTLER_PATH`、Claude 全局配置、命令目录软链和沟通风格；冲突零破坏停机。Codex plugin 是后续独立组件，失败时明确报告部分完成，不假报总成功。
- **个人沟通风格正本（`communication-style.md`，仓根）**：把过去散在本机 Matrix 输出风格与多个风格记忆文件里的「怎么跟用户说话」规矩，收敛成**唯一正本**（DRY，改说话风格只改这一处）；随 git 跨机器同步、经上面的 @import 常开。含 9 节（基调 / 详略 / 抓重点 / 说人话〔4 条带例〕/ 把话说顺 / 别急着抛选择菜单 / 格式 / 结尾决策块 / 边界）。只管说话方式、不渗工程行为。Matrix 输出风格作为过渡产物已退休（本机迁移）。
- **基地车部署**：先解析并回声唯一 `PROJECT_ROOT`，再只在它下建 `.ai/`（含空 `.ai/project/` 种子）/ `deliveries/` / `origin/`，用统一 renderer 注入 CLAUDE.md + AGENTS.md，最后部署 Claude hooks。真源 `20_Workflow_Lifecycle/mcv-deployment.md`。
- **维护升级**：`mcv-update.md`（维护文件升级）、`maintenance-boundaries.md`（成本 / 批处理边界）。
- **hook 机械门禁**（部署项目侧）：PreToolUse 拦截跳阶段 / 未冻结 AC / 显式非 pass TECH_PLAN 写源码 / 业务扩展保护 / 双 active 迭代 / 台账非法状态值；真实项目外路径由宿主权限处理，坏输入仍拒绝。方案四态与七项 Plan Admission 真源 `tech-plan-schema.md`；Claude/Codex 共用 `phase_gate`，旧版无字段暂按 legacy 放行。

## 驻留工具

- `tools/inbox/` — 需求收件箱确定性 scanner：plan 默认零写、apply 原子维护 `.ai/INBOX.md` managed block，按原始 bytes 做 SHA-256 并处理幂等、变化、缺失、symlink/损坏 ledger；不做语义分类、不改 `origin/`。
- `tools/prd-migrate/` — legacy 单 PRD 的 inspect/plan/apply/verify/rollback 与多 PRD/legacy 钉版 resolver；显式日期化身份、同父 staging/backup/rename、机器 receipt、历史影响面和路径越界拒绝。人类步骤见 `docs/prd-migration-guide.md`。
- `tools/prd-status/` — 多 PRD 确定性只读查询：项目列表、`prd_id` 下钻、workspace key 筛选与 legacy 退化；总索引、单需求目录和 active workspace map 交叉核验，混合/漂移/symlink fail-closed，稳定 JSON/退出码且零缓存。
- `tools/prd-update/` — 按显式 `prd_id` 和确认 JSON spec 执行零写 plan、整 PRD collection 事务 apply、持久 receipt、verify 与 hash-gated rollback；复用 status parser，逐路线扫描三态影响，重复执行幂等，故障或篡改 fail-closed。
- `tools/workspace-scope/` — 工作区范围只读执行器：从 npm/pnpm manifest 发现候选，校验地图与共享/生成路径 owner，解析 AC 钉版的多 PRD/模块范围，核 TECH_PLAN 写计划、显式路径和 Git diff。PreToolUse 对 apply_patch/Edit/Write/MultiEdit 复用同一 parser；shell 由 P5 `check-diff` 兜底。
- `tools/mile0009-e2e/` — 把 inbox、migration、status、update 与 workspace scope 串成单工程回归，并提供真实项目只读源 + 自动临时副本 migration/rollback dogfood runner。
- `tools/butler-upgrade/` — 已部署项目的确定性升级器：机器迁移链、JSON plan、项目事务、历史 fixture 与失败恢复；HOME 安装始终独立确认。
- `tools/verification-evidence/` — P5 **自动道证据工具**（Python 标准库）：按真实 argv 执行验证，生成有界 stdout/stderr、exit、时间与 SHA-256 record；只读校验后在收口时整包从热区移入迭代归档，失败记录保留但不能覆盖绿 AC。默认只认 current；显式 `--allow-closed` 仅在 `current: none` 且目标迭代 closed 时允许补捕获/移动收口态检查。
- `tools/delivery-selftest/` — 交付自测**人测回传桥**（Node 零依赖）：读 manifest JSON → 生成 GitHub 风格分步流程页 → 收人工四态回传（通过 / 未通过 / 延后 / 跳过）→ 写 `results.json` + 自退。P5 人测道下游接线协议 `20_Workflow_Lifecycle/human-test-bridge.md`，契约真源 `tools/delivery-selftest/README.md`。
- `scripts/audit-project-state.py` — 收口/切版的**只读状态审计器**：机械对账台账、路线、归档、交付、Evidence Index、fold receipt 与 Butler 发布元数据；VERSION tag 必须实际指向 HEAD 才算已发布，工作树干净但提交领先 tag 仍亮 `UNRELEASED`。

## 帮手（临时子 agent，不下发到项目）

当前住册三帮手，用时读定义、临时起干净上下文子 agent 执行：复核（`independent-review`，只读、接 P5）/ 更新说明（`knowledge-fold`，收尾把改动折进 `.ai/project/`、只写该目录）/ 查过时（`drift-check`，抽查说明是否过时、只读）。名册与通用规矩真源 `62_Extension_Agents/overview.md`。
