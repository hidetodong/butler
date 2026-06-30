> 分流: 完整 | 命中升级信号: 多文件改动（3）、契约变更（TECH_PLAN schema 字段口径强化） | 2026-06-30

# 一句话

按 SDD（规范驱动开发）范式参照、评估后选定「方案 A」轻量引入 tasks（任务分解）能力——不新增独立产物、不新增 hook 门禁、不破坏四件套，而是把 TECH_PLAN 里既有的 `Execution Steps` 字段从"实现顺序"强化成"可勾选、绑 AC、可标依赖/并行"的任务清单，并让 P4 在 `task-state.md` 里镜像勾选进度。butler 的验收脊柱（AC）不变，tasks 只作执行层辅助分解，按迭代大小可深可浅。

# 背景与判断

- SDD（Spec Kit / OpenSpec）四步：Specify → Plan → **Tasks** → Implement。butler 现状 P1+P2(Specify) → P3(Plan) → P4(Implement)，唯独没有独立 Tasks 步。
- 评估结论：butler 是**验收导向**（AC 是贯穿 P2→P4→P5 的脊柱），SDD 是**任务导向**（tasks.md 是执行脊柱）。tasks 的三职能（拆分 / 排序 / 活进度）在 butler 已分摊到 `Execution Steps` + `task-state.md` + `AC 勾选`。
- 故不引入 SDD 那种独立强制第五件套（会破坏四件套不变量、动 hook、双重记账，性价比差）；选轻量方案 A，闭合唯一真实缺口：完整路径大迭代缺一份"细粒度、有序、可勾选、活的"执行清单。

# Goal

- G1 强化 tech-plan-schema 的 `Execution Steps` 字段：从"实现顺序 / 子任务拆分"升级为可勾选任务清单——每条绑 AC、可标依赖与可并行（`[P]`），并明确"展开粒度随迭代大小"（大迭代细展、小迭代保持粗粒度）。
- G2 让 context-persistence 运行时增量明确：当 TECH_PLAN 含任务清单时，P4 在 `task-state.md` 镜像任务完成态（已完成 / 进行中 / 下一条）作为活进度板；AC 仍是验收脊柱。
- G3 artifact-style 增补任务清单书写口径（一行一任务、绑 AC、标记克制、不过度拆分小迭代）。

# Constraints

- 不新增产物文件、不新增 hook 门禁、不改四件套字段结构（只强化既有 Execution Steps 字段口径）。
- 不把 AC 脊柱改成 task 脊柱：tasks 是执行辅助，验收与回填仍以 AC 为单位。
- 不引入双重记账：任务清单单一存放于 TECH_PLAN.Execution Steps，活进度镜像于 task-state.md，二者职责不同（计划态 vs 运行态），不开第三处。
- 守本仓 CLAUDE.md 五约束。

# Impact Scope

- 改：`tech-plan-schema.md`（Execution Steps 字段口径 + 模板）、`context-persistence.md`（运行时增量补任务镜像）、`artifact-style.md`（任务清单书写口径）。
- 评估是否同步：`rule-card.md`（不新增强制约束则不动）、`README.md`（无新文件，不动）。
- 不影响：四件套字段结构、hook、lifecycle 分流、AC / 验收脊柱、迭代 / 里程碑 / 版本机制。

# Project Type / Active Profiles

- 形态：Markdown 规则仓库（butler 自己）。Profiles：无。

# Open Questions

- Q1 任务清单是否需稳定编号（T1/T2…）便于 task-state 精确引用？倾向：建议但不强制，小迭代可省。（P3 定）
- Q2 是否在 verify-schema 也提一句"AC 回填可顺带标注由哪些任务支撑"？倾向：不动 verify，保持 AC 脊柱纯粹、避免范围扩张。（P3 定）
