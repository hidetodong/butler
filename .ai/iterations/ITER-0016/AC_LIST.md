---
状态: ack-frozen
ACK 日期: 2026-06-30
---

> P2 由用户显式 ACK（真实确认，非危险模式自审）；本迭代自 P3 起在 `/dangerous` 危险模式下自治推进，P3/P5 产物留危险横幅与 `RUN_LOG.md` 审计。

# Goal

- 轻量引入 tasks 能力（方案 A）：强化 TECH_PLAN.Execution Steps 为"可勾选 / 绑 AC / 可标依赖并行"的任务清单 + task-state 镜像活进度，不破坏四件套与 AC 脊柱。

# Constraints

- 零新增产物、零 hook 改动、零四件套字段结构变更。
- AC 仍是验收 / 回填脊柱；tasks 仅执行辅助。
- 单一存放：任务清单只在 Execution Steps，活态只在 task-state，不开第三处（不双重记账）。

# Acceptance Checklist

- [ ] AC1: tech-plan-schema `Execution Steps` 字段口径强化——模板与编写规则明确：① 列为可勾选任务项 ② 每项标注所服务的 AC ③ 可选标注依赖顺序与可并行项（`[P]`）。
- [ ] AC2: tech-plan-schema 明确"展开粒度随迭代大小"——大迭代（多文件 / 可并行 / TDD）展开到任务级；小 / 简化迭代保持粗粒度实现顺序即可，不强制细拆（proportionate，避免过度工程）。
- [ ] AC3: context-persistence 运行时增量补一条——当 TECH_PLAN 含任务清单时，P4 须在 task-state.md 镜像任务完成态（已完成 / 进行中 / 下一条）作为活进度板；并显式声明 AC 仍是验收脊柱、task-state 不取代 AC 回填。
- [ ] AC4: artifact-style 增补任务清单书写口径——一行一任务、动词开头可执行、绑 AC、标记克制；明确"不过度拆分小迭代"。
- [ ] AC5: 不双重记账自证——三处文档明确职责切分：Execution Steps = 计划态任务清单（P3 写），task-state = 运行态镜像（P4 更），AC = 验收脊柱（P2 定 / P5 回填）；无新增产物、无新增 hook 门禁。
- [ ] AC6: 不破坏不变量——四件套字段结构未改、hook 未碰、lifecycle 分流未动、rule-card 强制约束集未扩（若无新增硬约束则 rule-card 不动）；本仓 CLAUDE.md 五约束自检通过。

# Verification Method

- AC1 / AC2: 读 tech-plan-schema，核对 Execution Steps 模板含勾选 / 绑 AC / 依赖并行标注 + 粒度随迭代大小的说明。
- AC3: 读 context-persistence 运行时增量，确认任务镜像条目 + "AC 仍是脊柱"声明。
- AC4: 读 artifact-style，确认任务清单书写口径段。
- AC5: 通读三处，确认职责切分表述无歧义、无第三处记账。
- AC6: git diff 确认未碰四件套字段 / hook / lifecycle；grep rule-card 确认强制约束集未扩；本仓五约束自检。
