> ⚠️ 危险模式：本方案由模型过 dangerous-engine §5.2 设计自审门后自主 ACK，未经用户逐项确认（ITER-0016，2026-06-30）。P2 已由用户显式 ACK。

# Goal

- 支撑 AC1–AC6：把 tasks（任务分解）能力以方案 A 轻量织入既有 `TECH_PLAN.Execution Steps` + `task-state`，不新增产物、不动 hook、不改四件套字段结构。

# Files / Modules to Change

- 改 `Coder/20_Workflow_Lifecycle/tech-plan-schema.md` —— §3 模板 `Execution Steps` 块升级为可勾选任务清单；§4 编写规则补"绑 AC / 依赖并行 / 粒度随迭代大小 / 书写口径指针引用 artifact-style"（AC1/AC2/AC5）。
- 改 `Coder/40_Context_Management/context-persistence.md` —— §4 运行时增量「最小记录集合」补"任务清单镜像"条 + 一句"AC 仍是验收脊柱、task-state 不取代 AC 回填"（AC3/AC5）。
- 改 `Coder/20_Workflow_Lifecycle/artifact-style.md` —— 新增一小节「Execution Steps 任务清单书写」（AC4）。

# Interface / Contract

- **Execution Steps 任务清单契约**（计划态，P3 写）：可勾选项 `- [ ] T<n> <动词开头任务> → AC<k>`；可选依赖标注（"依赖 T<m>"）与可并行标注 `[P]`；任务编号 `T<n>` 建议但不强制（小迭代可省）。
- **task-state 镜像契约**（运行态，P4 更）：当 TECH_PLAN 含任务清单时，task-state 的「已完成逻辑点 / 下一步入口」按任务粒度镜像完成态；AC 勾选（context-persistence §5 阶段结晶）与 P5 AC 回填不变，仍是验收脊柱。
- 不新增字段、不改四件套字段结构——Execution Steps 是 TECH_PLAN 既有必填字段，仅强化其内容口径。

# State / Boundary

- 三处职责切分（不双重记账）：Execution Steps = 计划态任务清单；task-state = 运行态镜像；AC = 验收脊柱。任务清单单一存放于 Execution Steps，不开第三处。
- 不碰：四件套字段结构、hook、lifecycle 分流、verify-schema、rule-card 强制约束集、README（无新文件）。

# Design Decisions

- **强化既有字段而非新增产物**：方案 A 的最小落点——Execution Steps 本就承载"实现顺序 / 子任务拆分"，把它结构化为可勾选 / 绑 AC / 可并行即可，避免第五件套（破坏四件套不变量、双重记账，即评估中否掉的 B/C）。
- **粒度随迭代大小（proportionate）**：大迭代展开到任务级，小 / 简化迭代保持粗粒度。与 lifecycle 极小 / 简化 / 完整三档分流一致，防过度工程。
- **Q1 任务编号 T1/T2**：建议但不强制——给出便于 task-state 精确引用，小迭代可省。
- **Q2 不动 verify-schema**：AC 回填保持以 AC 为单位，不引入"任务→AC"二级映射，保 AC 脊柱纯粹、不扩范围。
- **书写口径单一来源**：任务清单怎么写归 artifact-style（与四 schema 既有分工一致——schema 管填哪些字段、artifact-style 管字段里的话怎么写），tech-plan-schema 指针引用、不双写。

# Execution Steps

- [ ] T1 改 tech-plan-schema §3 模板 Execution Steps 块为可勾选任务清单样例 → AC1
- [ ] T2 改 tech-plan-schema §4 编写规则补 4 条（绑 AC / 依赖并行 / 粒度随迭代 / 口径指针）→ AC1/AC2/AC5
- [ ] T3 [P] 改 context-persistence §4 最小记录集合补任务镜像条 + AC 脊柱声明 → AC3/AC5
- [ ] T4 [P] artifact-style 加「Execution Steps 任务清单书写」小节 → AC4
- [ ] T5 收口前自检：grep 确认四件套字段 / hook / lifecycle / rule-card 未动 + 本仓五约束 → AC6
- （注：T1/T2 同文件有序；T3/T4 与之独立可并行——本清单本身即 dogfood 方案 A 的新格式）

# Verification Plan

- 按 `AC_LIST.md` Verification Method 逐项核对；P5 升格为完整审查 + 独立复核（fresh-context 子 agent，dangerous §7.3）。

# Risks / Open Questions

- 任务清单与 task-state 镜像靠 AI 读取遵守、无 hook 机械强制（同 artifact-style / 分层既有取舍，可接受）。
- 无遗留未决项（Q1/Q2 已在 Design Decisions 定）。
