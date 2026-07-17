# capabilities（现在真能做哪些事）

> R2 新增层（旧单文件没有）：从现状盘"butler 落地后到底能干什么"。引擎正文指各扩展模块，此处只给清单 + 一句话 + 指针。

## Codex 双宿主适配（v2.12.0–v2.14.0）

- Codex 在 Butler 仓根可原生发现 `AGENTS.md`，按固定顺序恢复 `.ai/` 状态并钻取 `Coder/` 真源；`scripts/verify-codex-foundation.sh` 可做结构回归。
- `templates/AGENTS.md.template` 已定义未来目标项目入口契约，但尚未接入部署/升级；目标项目双入口接线归 MILE-0006 R4。详细状态见 `docs/codex-compatibility.md`。

## Codex 工作流与 hooks（v2.13.0–v2.14.0）

- `plugins/butler/` 可安装 8 个 skills：prd/review/milestone/upgrade/ideation/preference/loop/dangerous；`.agents/skills/` 软链让仓内直接发现同一真源。
- `scripts/install-codex-plugin.sh` 安装/刷新个人 plugin；`scripts/verify-codex-workflows.sh` 做结构回归。loop/dangerous 禁隐式调用。
- `plugins/butler/hooks/hooks.json` 默认注册 PreToolUse/PostToolUse；共享 dispatcher 已能解析 canonical `apply_patch` 的 add/update/delete/move、多文件与多 hunk，并对每个 target 复用既有门禁/提醒规则。`scripts/verify-codex-hooks.sh` 做包装器和配置回归。
- 真实 Codex 已验证 phase deny、protected-path deny、allow 和 advisory 上下文注入。边界只覆盖送入 hook 的工具事件，不替代 sandbox，也不保证覆盖 shell/MCP；目标项目双入口仍未接部署，归 R4。

## 核心：P1–P5 开发 SOP（默认主线）

任何非极小任务默认走五阶段状态机，每阶段产一份"产物"、下一阶段只从上一阶段的**文件**读（不靠对话记忆）：

| 阶段 | 干什么 | 产物 |
|---|---|---|
| P1 Analysis | 分析需求、识别项目类型、**主动质询伪需求/低 ROI（该剥离/缩 MVP/提替代）** | `.ai/CONCEPT.md` |
| P2 Acceptance | 定验收标准（AC）、冻结 | `.ai/AC_LIST.md`（`状态: ack-frozen`） |
| P3 Design | 技术方案 + 执行步骤 | `.ai/TECH_PLAN.md` |
| P4 Execute | 按步骤写码，常驻纠错 + 最小实现底线 | 源码 + `.ai/01_CHANGELOG.md` |
| P5 Verify | 分道验证（自动 / 人测）+ 分级置信 | `.ai/VERIFY_REPORT.md` |

阶段定义真源 `20_Workflow_Lifecycle/lifecycle.md` + 各 schema。

## 命令（显式触发的扩展能力）

| 命令 | 干什么 | 真源 |
|---|---|---|
| `/butler:ideation` | 独立脑暴、不进执行主线、不冻结（贴模糊需求 / 想法，或留空进对话）；MILE-0005 R2 迁入命名空间 | `.claude/commands/butler/ideation.md`（薄壳，真源 `50_Extension_Ideation/ideation-engine.md §3`） |
| `/butler:loop` | 收敛闭环、死磕式高强度纠错升档（**高强度·长时·消耗大、郑重触发**）；原名 `/loop`，MILE-0005 R4 迁入命名空间。一次性 P4 升档（无持久态·无 `off`·跑到全绿或定量熔断）；薄壳近乎无参、frontmatter ⚠️ + 第 0 步风险提醒、委托真源**不复述**闭环/熔断算法 | `.claude/commands/butler/loop.md`（薄壳，真源 `55_Extension_ConvergenceLoop/convergence-loop-engine.md` §3/§6） |
| `/butler:dangerous` | 无人值守长程自治（**实验性**·自审门替 ACK·强制 P5 全审护栏）；原名 `/dangerous`，MILE-0005 R4 迁入命名空间。空参=开启（走引擎 §3 风险闸）/ `off` 关 / `status` 只读；持久开关外化 `.ai/local-constraints.md` `dangerous`、跨会话 announce-on-read。薄壳 frontmatter ⚠️ + 第 0 步风险提醒 + **闸交回引擎不复述护栏** | `.claude/commands/butler/dangerous.md`（薄壳，真源 `65_Extension_Dangerous/dangerous-engine.md` §3/§3.1/§7） |
| `/butler:preference` | 偏好探针开关（`on`/`off` 隐私总开关 / `reback on\|off` 反哺 / `distill` 手动蒸馏；**留空=只读状态回声**）；原名 `/preference`，MILE-0005 R3 迁入命名空间。参数面最宽（唯一二级参数 `reback`）；只管全局层开关，本项目抑制开关走 `local-constraints` | `.claude/commands/butler/preference.md`（薄壳，真源 `70_Extension_Preference/preference-probe-engine.md` §2.2/§2.3/§2.4/§6/§7） |
| `/butler:milestone` | 里程碑录入 / `status` 只读看板；**brief 是大 PRD 时并进触发 `prd-split` 切成 `references/prd/`**（一份输入喂方向层路线图 + 细节层切片，MILE-0004 R3）；MILE-0005 R2 迁入命名空间 | `.claude/commands/butler/milestone.md`（薄壳，真源 `20_Workflow_Lifecycle/milestone-schema.md` §6.4 步 6 并进分支 / §5.3 路线项↔slug 交叉指针 / §6.5 只读看板） |
| `/prd update` / `/prd status` | PRD **改版同步**（出新版 V→V+1：变更检测清单优先+diff兜底 / 重新派生 / 先冻旧版快照再更 live / 登记表认亲（新增·消失 + 松边改名/合并/拆分启发式提候选→确认、绝不自动认，R6）/ 三态影响面亮牌不自动 / 受影响活路由重冻·扩张）；`status` 只读看板（MILE-0004 R5–R6） | `40_Context_Management/prd-update.md`（§4.2 松边、首切见 `prd-split.md`、钉版见 `acceptance-schema` 的 `prd_version`；非回归门见 `references-schema §9`） |
| `/butler:prd` | **butler 第一个真实命令文件**（ITER-0044，原名 `/butler-prd`，MILE-0005 R1 迁入 `/butler:` 命名空间）——PRD 先行动作的薄壳路由器：第 0 步强制读 `references-schema` 契约 → 按参数三分支（留空/贴 PRD=首切 / `update`=改版 / `status`=只读看板），委托真源不复述算法。**全局下发（ITER-0045·v2.5.0）**：`setup.sh` 软链进 `~/.claude/commands/`，**所有项目可用**（不再限编辑 butler 仓）；正文含「`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目」路径约定，跨 cwd 成立 | `.claude/commands/butler/prd.md`（薄壳，真源 `references-schema.md` / `prd-split.md` / `prd-update.md`） |
| `/butler:review` | **命名空间第二个真命令**（ITER-0047·MILE-0005 R1）——代码 / 产物复核薄壳路由器：默认（留空）当前上下文快速自检、`independent` 另起 fresh 子 agent 独立复核（验证者≠作者）；第 0 步没接 butler 优雅降级、委托真源不复述算法。作后续命令的复制范本 | `.claude/commands/butler/review.md`（薄壳，真源 `review-engine.md §5` / `independent-review.md` / `62_Extension_Agents/overview.md §3`） |
| `/butler:upgrade` | 已部署项目升级到最新 butler 版（按 `migrations/` 区间幂等执行）；原名 `/butler-upgrade`，MILE-0005 R2 迁入命名空间 | `.claude/commands/butler/upgrade.md`（薄壳，真源 `20_Workflow_Lifecycle/butler-upgrade.md`；**注：升级协议从未真跑，见 debt**） |

## 部署与维护能力

- **全局安装（`scripts/setup.sh`）**：一次性、机器级——写 shell rc 的 `BUTLER_PATH` + `~/.claude/CLAUDE.md` 全局配置（让所有项目发现 butler 规则）+ **软链 `.claude/commands/butler/` 命名空间目录 → `~/.claude/commands/butler`**（让 `/butler:*` 命令全局可用；分发 ITER-0045·v2.5.0 打通，命名空间化 MILE-0005·v2.7.0）+ **在全局配置块内 `@import` 个人沟通风格正本 `communication-style.md`**（规定 AI 怎么跟用户说话：语气 / 详略 / 说人话 / 别抛菜单，每会话常开、跨机器同步，ITER-0046·v2.6.0）。与逐项目基地车部署**不同层**：命令与沟通风格都是全局机器级、不进目标项目 `.ai/`。
- **个人沟通风格正本（`communication-style.md`，仓根）**：把过去散在本机 Matrix 输出风格与多个风格记忆文件里的「怎么跟用户说话」规矩，收敛成**唯一正本**（DRY，改说话风格只改这一处）；随 git 跨机器同步、经上面的 @import 常开。含 8 节（基调 / 详略 / 抓重点 / 说人话〔4 条带例〕/ 别急着抛选择菜单 / 格式 / 结尾决策块 / 边界）。只管说话方式、不渗工程行为。Matrix 输出风格作为过渡产物已退休（本机迁移）。
- **基地车部署**：把 butler 规则装进目标项目——建 `.ai/`（含空 `.ai/project/` 知识文件夹种子）/ `deliveries/` / `origin/`、注入 CLAUDE.md + hooks。真源 `20_Workflow_Lifecycle/mcv-deployment.md`。
- **维护升级**：`mcv-update.md`（维护文件升级）、`maintenance-boundaries.md`（成本 / 批处理边界）。
- **hook 机械门禁**（部署项目侧）：PreToolUse 拦截跳阶段 / 未冻结 AC 写源码 / 越界写 / 双 active 迭代 / 台账非法状态值。真源 `templates/hooks/` + `mcv-deployment §5`。

## 驻留工具

- `tools/delivery-selftest/` — 交付自测**人测回传桥**（Node 零依赖）：读 manifest JSON → 生成 GitHub 风格分步流程页 → 收人工四态回传（通过 / 未通过 / 延后 / 跳过）→ 写 `results.json` + 自退。P5 人测道下游接线协议 `20_Workflow_Lifecycle/human-test-bridge.md`，契约真源 `tools/delivery-selftest/README.md`。

## 帮手（临时子 agent，不下发到项目）

当前住册三帮手，用时读定义、临时起干净上下文子 agent 执行：复核（`independent-review`，只读、接 P5）/ 更新说明（`knowledge-fold`，收尾把改动折进 `.ai/project/`、只写该目录）/ 查过时（`drift-check`，抽查说明是否过时、只读）。名册与通用规矩真源 `62_Extension_Agents/overview.md`。
