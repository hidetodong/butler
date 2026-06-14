# Butler 收敛闭环重构交付总结

> 日期：2026-06-14
> 任务：按 Loop Engineering 理念重构 P4 纠错机制——Ralph-Loop 正名为收敛闭环，纠错纪律下沉为常驻契约
> 状态：已完成，可交付

## 本次交付目标

诊断出原 Ralph-Loop"没被用起来"的结构性根因——一条本应普世的纠错纪律被错误地打包进一个默认关、靠关键词唤醒的 opt-in 模式，导致日常迭代既享受不到纪律、又因命名（借用 canonical Ralph 之名却名不副实）造成认知混乱。本次按 Loop Engineering 的"验证不可省"理念重构：把纪律与强度拆包，纪律下沉为默认常驻，强度保留为 opt-in，并完成正名。

## 已完成内容

| # | 改动 | 落地 |
|---|---|---|
| 1 | 新增常驻底线契约 | `30_Quality_Gate/correction-contract.md`：修到真过、探测绑 AC、禁止降级修复、诚实停，每次 P4 默认生效、无需触发 |
| 2 | 收敛闭环升档层 | `55_Extension_RalphLoop/` → `55_Extension_ConvergenceLoop/convergence-loop-engine.md`，重写为叠在契约之上的 `/loop` 升档（`[Loop #N]` + 定量熔断 + RCA） |
| 3 | 正名同步 | Ralph-Loop → 收敛闭环：logic-protocol §4、lifecycle P4、dangerous（6 处复用）、review、maintenance-boundaries、mcv-deployment、README×2、HUMAN_GUIDE |
| 4 | 注入层触达 | `templates/rule-card.md` 执行纪律补「禁止降级修复 + 诚实停」，经 `{{RULE_CARD_CONTENT}}` 占位符自动注入新项目，无需双写 |

## 关键变更 / 用户可感知变化

- **普通迭代默认变较真**：P4 标准执行从"单次探测、报错即甩给用户"升级为"遵循纠错收口契约修到真过"；任何迭代都禁止 `ts-ignore` / 跳测试 / 伪造结果作弊。
- **`/loop` 语义收窄**：不再用来"开启较真"，而是纯强度档（死磕 + 正式 5 轮熔断 + RCA）。
- **熔断两层化**：底线用定性"诚实停"（无计数器、无强制 RCA 文件），升档用定量熔断（5 轮 / 死锁 / 环境阻塞）。
- **dangerous / review 基本无感**：行为不变，仅复用对象改名、并显式继承常驻契约。
- **新项目自动继承 no-cheat 底线**；已部署老项目需各自 `/butler-upgrade` 同步。

## 高层影响范围

- **新增**：`Coder/30_Quality_Gate/correction-contract.md`、`Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md`
- **删除**：`Coder/55_Extension_RalphLoop/ralph-loop-engine.md`
- **修改**：`logic-protocol.md`、`lifecycle.md`、`maintenance-boundaries.md`、`mcv-deployment.md`、`review-engine.md`、`dangerous-engine.md`、`Coder/README.md`、根 `README.md`、`HUMAN_GUIDE.md`、`templates/rule-card.md`
- **未动**：`deliveries/`（本文件除外）、`docs/superpowers/specs/`（历史记录）、`10_Domain_Stack_Profiles/`、`40_Context_Management/`、`50/70_Extension`、`scripts/`、`Learner/`、`Composer/`

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| 全仓 grep `ralph` / `55_Extension_RalphLoop` / `ralph-loop-engine`（排除历史目录） | 活规则 0 残留 ✅ |
| 新文件落位检查 | 2 个新文件存在 ✅ |
| 旧目录删除检查 | `55_Extension_RalphLoop/` 已消失 ✅ |
| 新名引用计数 | 收敛闭环 / 契约引用覆盖 11 个文件 ✅ |
| rule-card SSOT 占位符确认 | `CLAUDE.md.template` 含 1 处 `{{RULE_CARD_CONTENT}}`，无需双写 ✅ |
| CLAUDE.md#3 注册检查 | 新契约文件已注册进 `Coder/README.md` 目录结构 ✅ |

## 已知剩余风险 / 延后事项

- **已部署老项目不自动更新**：需各自跑 `/butler-upgrade` 才能拿到新 rule-card；本仓库无法代为完成。
- **诚实停是定性判断**：底线层"无实质进展"由模型自判，可能偏早停或多磨一轮；需要更强坚持时用户应 `/loop` 升档——此为设计取舍，非缺陷。
- **延后未做（本轮范围外）**：Loop Engineering 讨论中识别的两个新能力接缝——A 心跳 / harness 绑定契约、B 工作发现前端——本轮未触及，留待单独立项。

## 引用

- 提交：commit `aece7aa`，合并 `7f5b547`（分支 `refactor/convergence-loop` → `main`）
- 核心规则：`Coder/30_Quality_Gate/correction-contract.md`、`Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md`
- 规范依据：`Coder/20_Workflow_Lifecycle/delivery-summary.md`
