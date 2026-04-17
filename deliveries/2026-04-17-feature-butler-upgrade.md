# Butler 规则仓库 feature: /butler-upgrade 交付总结

> 日期：2026-04-17
> 任务：新增 `/butler-upgrade` 命令 —— 已部署项目主动同步到最新版 butler
> 状态：已完成，可交付

## 本次交付目标

在 v0.1.0-first-stable 里程碑（audit 周期完成）之后，响应用户需求新增一个**显性升级命令**，让已部署过 butler 的老项目能通过 `/butler-upgrade` 或语义词触发，主动把自己的 `CLAUDE.md` 与 `.ai/` 结构同步到最新版 butler，同时保护项目特定内容不被覆盖。

## 已完成内容

| # | 动作 | 产物 / 影响点 |
|---|---|---|
| 1 | 新建升级协议 | `Coder/20_Workflow_Lifecycle/butler-upgrade.md`（8 段完整规则：目标 / 触发 / 侦察 / 首次升级 / 常规升级 / `.ai/` 升级 / 验证回退 / 边界） |
| 2 | 引入保护区标记 | `templates/CLAUDE.md.template` 用 `<!-- user-managed -->` / `<!-- /user-managed -->` 包裹"项目特定约束"整章 |
| 3 | 部署契约起点 | `mcv-deployment.md § 3` 第 4 步明确部署时生成保护区标记，作为未来升级契约的起点 |
| 4 | 命令触发注册 | `logic-protocol.md § 4` 注册 `/butler-upgrade` + 语义词"升级 butler / 同步到新版 / 同步 butler 规则" |
| 5 | 目录与说明注册 | `Coder/README.md` 目录结构 + "其中："说明双处注册 |

## 关键变更 / 用户可感知变化

- **老项目主动升级的显性命令**：用户只需在项目里说"升级 butler"或敲 `/butler-upgrade`，AI 会自动侦察项目状态、对比 butler 仓最新、生成升级清单 ACK 后执行。
- **保护区契约**：新部署的项目（本 feature 之后）自带 `<!-- user-managed -->` / `<!-- /user-managed -->` 保护区；用户项目特定约束放保护区内**永远不被覆盖**。
- **老项目首次升级不踩坑**：无保护区标记的老项目走"备份 + 交互 ACK"流程 —— 先备份再对比差异，每个"butler 不识别的段落"都向用户确认是否保留。零损失 + 全掌控。
- **基地车生命周期三阶段闭环**：
  - `mcv-deployment.md` — 初次部署
  - `butler-upgrade.md` — 跨版本升级 ← **本次新增**
  - `mcv-update.md` — `.ai/` 内部维护
- **`.ai/` 升级粒度**：命名升级（自动处理 `SESSION_HANDOFF.md` → `02_SESSION_HANDOFF.md` 等）+ schema 必填字段补齐；累积型文件（CHANGELOG / BUG_LOG）内容不动。

## 高层影响范围

**新建 1 个文件**：
- `Coder/20_Workflow_Lifecycle/butler-upgrade.md`（升级协议，6792 字节）

**修改 4 个文件**：
- `templates/CLAUDE.md.template`（加保护区标记）
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`（第 4 步措辞更新）
- `Coder/00_System_Prompt/logic-protocol.md § 4`（新命令触发注册）
- `Coder/README.md`（目录 + 说明双处注册）

**未影响**：`templates/rule-card.md`（SSOT 保持）、其他 schema 文件、Extension、Domain Profiles、scripts、任务产物文件。

## 验证方式与结果摘要

| 验证动作 | 结果 |
|---|---|
| `butler-upgrade.md` 8 段结构 | 全部齐全 ✅ |
| `grep 'user-managed' CLAUDE.md.template` | 2 处命中（开闭）✅ |
| `grep 'user-managed' mcv-deployment.md` | L70 第 4 步 ✅ |
| `grep 'butler-upgrade\|升级 butler' logic-protocol.md` | § 4 L80 注册就位 ✅ |
| `grep 'butler-upgrade' Coder/README.md` | 2 处（目录 + 说明）✅ |

详细验证记录见 `.ai/VERIFY_REPORT.md`。

## 已知剩余风险 / 延后事项

### butler 自身未自举保护区（显式不做）

butler 仓根的 `CLAUDE.md` 不加保护区标记。理由：`butler-upgrade.md § 8 边界说明`明确 —— butler 仓自身演进由 audit 流程管理，不走 butler-upgrade。保护区是**为目标项目设计**的契约，butler 仓作为规则源不需要。

### 首次实跑待验证

本 feature 的完整升级流程尚无实际老项目 dogfooding。协议按最高清晰度文档化，但首次实跑可能暴露边界情况。

### 协议维护日常

未来 butler 新增文件重命名或 schema 字段变更时，需要同步更新 `butler-upgrade.md § 6.1` 的"已知重命名清单"。属规则维护日常，不需要独立工单。

## 可选引用

- 产物链：`.ai/CONCEPT.md`、`AC_LIST.md`、`TECH_PLAN.md`、`VERIFY_REPORT.md`
- 新规则文件：`Coder/20_Workflow_Lifecycle/butler-upgrade.md`
- 关联修改：
  - `templates/CLAUDE.md.template`
  - `Coder/20_Workflow_Lifecycle/mcv-deployment.md § 3`
  - `Coder/00_System_Prompt/logic-protocol.md § 4`
  - `Coder/README.md`
- 前期里程碑：
  - `v0.0.8`（Must Fix + Should Fix 全闭环）
  - `v0.1.0-first-stable`（audit 周期完成）
- 前 8 份交付：
  - `deliveries/2026-04-17-must-fix-repair.md`
  - `deliveries/2026-04-17-should-fix-bucket-{a,b,c,d,e}.md`
  - `deliveries/2026-04-17-nice-to-have-bucket-{f,g}.md`
