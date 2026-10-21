# tasks 步骤轻量引入（方案 A）：强化 Execution Steps 为可勾选任务清单

> ITER-0016 · 迭代交付（小版本） · 收口 2026-06-30

> ⚠️ **危险模式自治披露**：本迭代 P2 由用户显式 ACK（真实确认 6 条 AC + 改动预览），自 P3 起在 `/dangerous` 自治下推进——P3 的 ACK 由模型自审门替代，P5 经强制完整审查 + 独立复核（另起一个不带本会话上下文的子 agent 逐 AC 裁决）。自治轨迹见 `.ai/RUN_LOG.md`。

## 本次交付目标

- 参照 SDD（规范驱动开发）Specify → Plan → **Tasks** → Implement 四步评估：butler 缺一个独立的 Tasks（任务分解）步。评估结论是 butler 本就是**验收导向**（AC 贯穿 P2→P4→P5），不需要 SDD 那种强制的第五件套。
- 唯一真实缺口：完整路径的大迭代缺一份"细粒度、有序、可勾选、活的"执行清单。本迭代用方案 A 轻量补上——只强化 TECH_PLAN 既有的 `Execution Steps` 字段，不新增产物、不动 hook、不破坏四件套。

## 已完成内容

- `tech-plan-schema.md`：§3 模板的 `Execution Steps` 块从"实现顺序 / 子任务拆分"升级为可勾选任务清单样例（`[ ] T<n> 动作 → ACn`，可标"依赖 T<m>"与可并行 `[P]`，编号可选）；§4 补 4 条编写规则（绑 AC / 粒度随迭代大小 / 计划态单一存放 + task-state 镜像 / 书写口径指针引用 artifact-style）。
- `context-persistence.md`：§4 运行时增量最小记录集合补一条——TECH_PLAN 含任务清单时，按任务粒度镜像完成态（已完成 / 进行中 / 下一条）作 P4 活进度板；记录原则补一条——任务镜像不取代验收脊柱，AC 仍以 AC 为单位。
- `artifact-style.md`：新增 §5「Execution Steps 任务清单书写」6 条口径（一行一任务 / 绑 AC / 标记克制 / 编号可选 / 不过度拆分 / 计划态不反复改勾），原 §5–§7 顺延为 §6–§8。

## 关键变更 / 用户可感知变化

- 以后完整路径的大迭代，TECH_PLAN 的 `Execution Steps` 写成可勾选、绑 AC、可标依赖 / 并行的任务清单；P4 执行进度镜像到 `task-state.md`，断点续接看得见"做到哪条任务"。
- 小 / 简化迭代不受影响：粒度随迭代大小，保持粗粒度实现顺序即可，不强制细拆。
- 验收脊柱不变：AC 仍是 P2→P4→P5 的验收单位，tasks 只是执行侧投影；不引入双重记账——计划态在 TECH_PLAN、运行态在 task-state、验收在 AC，三处职责切分。
- 向后兼容：纯字段口径强化，没动四件套字段结构、没碰 hook，老迭代不受影响。

## 高层影响范围

- 规则层：改 `Coder/20_Workflow_Lifecycle/tech-plan-schema.md`、`Coder/20_Workflow_Lifecycle/artifact-style.md`、`Coder/40_Context_Management/context-persistence.md`，共 3 文件。
- 没碰：四件套字段结构、hook、lifecycle 分流、AC / 验收脊柱、rule-card、README、迭代 / 里程碑 / 版本机制。

## 验证方式与结果摘要

- 6 条验收项全部满足（逐项见 VERIFY_REPORT）：Execution Steps 口径强化（可勾选 + 绑 AC + 可标依赖并行）、粒度随迭代大小、task-state 镜像 + AC 脊柱声明、artifact-style 书写口径、三处职责切分不双重记账、不破坏不变量 + 五约束。
- 独立复核（dangerous §7.3）：fresh-context 子 agent spec-only 逐 AC + 多维审查，6/6 confirm、零 refute、无 Must Fix、无 Should Fix，结论可收口；2 条 Nit（模板编号示例、VERIFY 当时占位）已就地消解 / 补齐。
- git diff 确认改动集中 3 文件；四件套字段 / hook / lifecycle / rule-card / README 零改动；本仓五约束自检通过。

## 已知剩余风险 / 延后事项

- 任务清单与 task-state 镜像靠 AI 读取遵守、无 hook 机械强制（同 artifact-style / 分层既有取舍，可接受）。
- 本轮不切版；ITER-0015 + ITER-0016 累积，可在用户门控下发为 v1.5.0（MINOR）。

## 引用

- `.ai/iterations/ITER-0016/CONCEPT.md` / `AC_LIST.md` / `TECH_PLAN.md` / `VERIFY_REPORT.md`
- `.ai/RUN_LOG.md`（危险模式自治审计轨迹，ITER-0016 段）
- 改动规则：`Coder/20_Workflow_Lifecycle/tech-plan-schema.md`、`Coder/20_Workflow_Lifecycle/artifact-style.md`、`Coder/40_Context_Management/context-persistence.md`
