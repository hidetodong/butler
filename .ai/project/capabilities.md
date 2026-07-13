# capabilities（现在真能做哪些事）

> R2 新增层（旧单文件没有）：从现状盘"butler 落地后到底能干什么"。引擎正文指各扩展模块，此处只给清单 + 一句话 + 指针。

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
| `/ideation` | 独立脑暴、不进执行主线 | `50_Extension_Ideation/ideation-engine.md` |
| `/loop` | 收敛闭环，死磕式高强度纠错升档 | `55_Extension_ConvergenceLoop/convergence-loop-engine.md` |
| `/review` | 独立复核（干净上下文子 agent、验证者≠实现者、逐 AC 核对） | `60_Extension_CodeReview/review-engine.md` + `62_Extension_Agents/independent-review.md` |
| `/dangerous` | 无人值守长程自治（自审门替 ACK、强制 P5 全审护栏） | `65_Extension_Dangerous/dangerous-engine.md` |
| `/preference` | 偏好探针开关（`on`/`off`/`reback`/`distill`） | `70_Extension_Preference/preference-probe-engine.md` |
| `/milestone` | 里程碑录入 / `status` 只读看板；**brief 是大 PRD 时并进触发 `prd-split` 切成 `references/prd/`**（一份输入喂方向层路线图 + 细节层切片，MILE-0004 R3） | `20_Workflow_Lifecycle/milestone-schema.md`（§6.4 步 6 并进分支 / §5.3 路线项↔slug 交叉指针） |
| `/prd update` / `/prd status` | PRD **改版同步**（出新版 V→V+1：变更检测清单优先+diff兜底 / 重新派生 / 先冻旧版快照再更 live / 登记表认亲（新增·消失 + 松边改名/合并/拆分启发式提候选→确认、绝不自动认，R6）/ 三态影响面亮牌不自动 / 受影响活路由重冻·扩张）；`status` 只读看板（MILE-0004 R5–R6） | `40_Context_Management/prd-update.md`（§4.2 松边、首切见 `prd-split.md`、钉版见 `acceptance-schema` 的 `prd_version`；非回归门见 `references-schema §9`） |
| `/butler-prd` | **butler 第一个真实命令文件**（ITER-0044）——PRD 先行动作的薄壳路由器：第 0 步强制读 `references-schema` 契约 → 按参数三分支（留空/贴 PRD=首切 / `update`=改版 / `status`=只读看板），委托真源不复述算法。**全局下发（ITER-0045·v2.5.0）**：`setup.sh` 软链进 `~/.claude/commands/`，**所有项目可用**（不再限编辑 butler 仓）；正文含「`Coder/…` 相对 `$BUTLER_PATH` 解析、`.ai/…` 落当前项目」路径约定，跨 cwd 成立 | `.claude/commands/butler-prd.md`（薄壳，真源 `references-schema.md` / `prd-split.md` / `prd-update.md`） |
| `/butler-upgrade` | 已部署项目升级到最新 butler 版（按 `migrations/` 区间幂等执行） | `20_Workflow_Lifecycle/butler-upgrade.md`（**注：从未真跑，见 debt**） |

## 部署与维护能力

- **全局安装（`scripts/setup.sh`）**：一次性、机器级——写 shell rc 的 `BUTLER_PATH` + `~/.claude/CLAUDE.md` 全局配置（让所有项目发现 butler 规则）+ **软链 `.claude/commands/*.md` → `~/.claude/commands/`**（让 `/butler-*` 命令全局可用，ITER-0045）。与逐项目基地车部署**不同层**：命令是全局软链、不进目标项目 `.ai/`。
- **基地车部署**：把 butler 规则装进目标项目——建 `.ai/`（含空 `.ai/project/` 知识文件夹种子）/ `deliveries/` / `origin/`、注入 CLAUDE.md + hooks。真源 `20_Workflow_Lifecycle/mcv-deployment.md`。
- **维护升级**：`mcv-update.md`（维护文件升级）、`maintenance-boundaries.md`（成本 / 批处理边界）。
- **hook 机械门禁**（部署项目侧）：PreToolUse 拦截跳阶段 / 未冻结 AC 写源码 / 越界写 / 双 active 迭代 / 台账非法状态值。真源 `templates/hooks/` + `mcv-deployment §5`。

## 驻留工具

- `tools/delivery-selftest/` — 交付自测**人测回传桥**（Node 零依赖）：读 manifest JSON → 生成 GitHub 风格分步流程页 → 收人工四态回传（通过 / 未通过 / 延后 / 跳过）→ 写 `results.json` + 自退。P5 人测道下游接线协议 `20_Workflow_Lifecycle/human-test-bridge.md`，契约真源 `tools/delivery-selftest/README.md`。

## 帮手（临时子 agent，不下发到项目）

当前住册三帮手，用时读定义、临时起干净上下文子 agent 执行：复核（`independent-review`，只读、接 P5）/ 更新说明（`knowledge-fold`，收尾把改动折进 `.ai/project/`、只写该目录）/ 查过时（`drift-check`，抽查说明是否过时、只读）。名册与通用规矩真源 `62_Extension_Agents/overview.md`。
