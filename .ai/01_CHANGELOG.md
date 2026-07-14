# 01_CHANGELOG

> **ITER-0050 已收口**（MILE-0005 R4 收官·`/butler:loop` + `/butler:dangerous` 两高风险命令）。对象级变更流（ADD/EDIT/DELETE），绑 AC、文件+章节级粒度，仅承载**当前开放迭代**的热数据。开新迭代时整体覆写；本迭代收口时归档至 `iterations/ITER-0050/CHANGELOG.md`。
>
> 上一迭代 ITER-0049 已收口，变更流见 `iterations/ITER-0049/CHANGELOG.md`。**本迭代收口即整体收 MILE-0005**（里程碑聚合交付见 `deliveries/milestones/MILE-0005-command-namespace-system.md`）。

## ADD

- `.claude/commands/butler/loop.md`（AC1/AC2/AC5）——全批**最薄**的高风险薄壳命令：一次性 P4 升档（无持久态、无 `off`、跑到验证全绿或 §6 定量熔断自然结束），近乎无参（空参=开启、多余参数一句提示）。**风险闸三招之①②**：frontmatter `description` 带显式 ⚠️（高强度·长时·消耗大·郑重触发）+ 第 0 步前置风险提醒（高强度升档、命令化不降门槛）。委托真源 `55_Extension_ConvergenceLoop/convergence-loop-engine.md` §3/§4/§6 不复述算法（**招③闸交回引擎**）。
- `.claude/commands/butler/dangerous.md`（AC1/AC2/AC3/AC5）——on/off/status 分派 + 风险闸薄壳：空参→开启（回写 `dangerous: on` + §3 回声 + §7 护栏）、`off`→关闭、`status`→只读回声（不改开关）、未知参数→兜底。**空参=开启**与 preference 空参=只读回声**有意不同**（引擎 §3 定义 bare=开启）。风险闸三招齐（frontmatter ⚠️「实验性·风险显著高于标准·建议隔离/可回滚环境」+ 第 0 步风险提醒 + 闸交回引擎 §3/§3.1 announce-on-read/§7 护栏）。含跨 cwd 路径约定段（状态外化当前项目 `.ai/local-constraints.md` `dangerous` 字段）、第 0 步双重降级（没接 butler / 无 `.ai/`）。
- `migrations/v2.10.0.md`（AC9）——区间 `v2.9.0→v2.10.0`，部署面 `[no-op]`+`[restamp]`；新命令由 R1 整目录软链自动托管、无需重跑 `setup.sh`；触发名迁移刻意不碰 `templates/` → 无 `[regen-claude]`；`/loop` 与 Claude Code 自带 `/loop` 撞名一处精确保留不迁。

## EDIT

- `Coder/65_Extension_Dangerous/dangerous-engine.md`（AC4/AC6）——作命令引用的 `/dangerous`→`/butler:dangerous`（scope/§3.1 announce 示例/§7.4 岔口等）+ §152 `/loop`→`/butler:loop`（butler 交叉引用）；**§21 harness 级 `/loop` 精确保留不迁**并加澄清注「harness 自带的循环，非 butler 的收敛闭环命令 `/butler:loop`」（良性增补·自文档化）。**引擎 §3/§4/§5/§7 自治/自审门/护栏算法一字未动**（8 行改动逐行核仅触发名 + 1 处加注）。
- `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md`（AC4/AC6）——作命令引用的 `/loop`→`/butler:loop`（scope/§2/§8·3 行）。**§3 核心逻辑/§4 闭环程序/§6 定量熔断算法一字未动**。
- `Coder/00_System_Prompt/logic-protocol.md`（AC4）——§89 收敛闭环、§92 危险模式激活段命令名迁移 + 各加旧名识别注（`/butler:loop`〔旧名 `/loop` 仍识别〕、`/butler:dangerous`〔旧名 `/dangerous` 仍识别〕）。
- 触发名迁移（AC4·仅命令引用、非算法）——`Coder/60_Extension_CodeReview/review-engine.md`、`Coder/70_Extension_Preference/preference-probe-engine.md`、`Coder/30_Quality_Gate/correction-contract.md`、`Coder/30_Quality_Gate/testing-strategy.md`、`Coder/62_Extension_Agents/independent-review.md`、`Coder/20_Workflow_Lifecycle/{lifecycle,local-constraints-schema,human-test-bridge,verify-schema,iteration-schema,mcv-deployment,acceptance-schema}.md`、`Coder/README.md`、`HUMAN_GUIDE.md`、`.ai/project/{architecture,constraints}.md`——`/dangerous`·`/loop`→`/butler:*`（负向前瞻 `(?!-)` 护 `/dangerous-engine.md` 路径不腐蚀）。
- `.ai/project/capabilities.md`（AC7）——命令表 24–25 行从「指引擎」升级为 `/butler:loop`·`/butler:dangerous` **一等入口**（真源指命令文件 + 引擎章节、注风险闸/参数/持久态、原名 /loop·/dangerous、MILE-0005 R4）。
- `README.md`（AC7）——扩展模式表两行迁 `/butler:*` + `butler/` 子树补 `loop.md`/`dangerous.md`（带 ⚠️、`└──` 收尾）+ Coder 目录 `55/65` 行迁。
- `.ai/project/frontier.md`（AC4/知识前滚）——命令引用迁移 + 前滚至 v2.10.0 / **8 命令** / R4 收口 / **MILE-0005 整体收口**。
- `VERSION`（AC9）——`2.9.0`→`2.10.0`；`CHANGELOG.md` 顶条 `[2.10.0] - 2026-07-14`（MINOR、聚合 ITER-0050、MILE-0005 R4 收官）。

## DELETE

- 无——R4 纯新增，不删文件。**`templates/`（`rule-card.md`、`templates/preference/*`）的 `/loop`·`/dangerous` 刻意保留不迁**（DD7 边界：命令不下发目标项目，目标项目侧靠散文旧名 + logic-protocol 旧名识别兜底）；**`dangerous-engine.md:21` harness 级 `/loop` 刻意保留不迁**（DD5：非 butler 命令，是 Claude Code 自带循环）。
