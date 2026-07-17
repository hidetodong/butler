---
状态: ack-frozen
ACK 日期: 2026-07-17
---

# Goal

让 Butler 基地车和所有迭代台账严格落在本次任务对应的项目根，不再把会话启动目录默认当成施工目标。

# In Scope

- 项目根解析优先级、证据与 fail-closed 约束。
- MCV 部署真源、浓缩规则卡和相关宿主入口/工作流路由的一致接线。
- 能检查显式目标、Git 子目录、多仓聚合目录和跨 cwd 部署的自动化验证。
- 删除 `research/.ai/iterations/ITER-0051` 空残留链。

# Out of Scope

- 不处理 `research/*/.ai` 中各项目自己的台账。
- 不强制所有新项目先创建 Git 仓库。
- 不扩展 hook 安全边界，不处理 shell/MCP 的通用防写。

# Acceptance Checklist

- [ ] **AC1（根目录契约）**：MCV 真源明确区分“会话启动目录”与“施工项目根”；任何基地车/台账写入前必须先解析并回声唯一目标。
- [ ] **AC2（优先级）**：用户明确点名的仓库或路径优先于 `cwd`；未点名时可以从子目录定位唯一 VCS/项目根，但不得仅凭 `pwd` 授权展开。
- [ ] **AC3（歧义即停）**：聚合目录含多个候选项目、路径不存在/不可写、或证据冲突时 fail-closed；在用户确认前不创建 `.ai/`、`deliveries/`、`origin/`、`CLAUDE.md` 或 `AGENTS.md`。
- [ ] **AC4（单一落点）**：一旦目标解析，本任务的台账、四件套、归档、交付和项目入口全部键控到同一根目录；目标可在 `cwd` 之外。
- [ ] **AC5（宿主一致）**：规则卡、Claude/Codex 项目入口与 Butler 工作流共用同一根目录契约，不在两宿主各造一套判定算法。
- [ ] **AC6（回归）**：自动化覆盖显式外部目标优先、Git 子目录定位、单项目目录、多仓父目录拒绝与重跑幂等；并复跑双宿主完整矩阵。
- [ ] **AC7（事故清理）**：`/Users/cyborgno2/Documents/research/.ai` 误展开空目录已移除，各子项目 `.ai` 无改动；Butler 本迭代台账只存在 Butler 仓根。

# Verification Method

- AC1–5：规则真源、宿主入口和单一路由实现的结构对账。
- AC3–6：隔离临时目录的可执行测试，确认拒绝分支零写入。
- AC6：`bash scripts/verify-dual-host.sh` 与 hook/plugin 现有回归。
- AC7：绝对路径存在性检查 + Butler Git diff 作用域检查。

# Open Questions / Risks

- 无 Git 的新目录只能靠用户显式点名或明确确认，这是防误展开必须付出的一次性交互成本。
- 项目标记若设得过宽，普通资料夹会被误认为项目；P3 应只采用强证据并对多候选拒绝猜测。
