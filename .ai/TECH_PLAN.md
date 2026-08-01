<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0100

方案状态: pass
方案审查日期: 2026-08-01
方案审查方式: user-ack

## Design Decisions

**Goal**

- 支撑 AC1–AC12：两个宿主共用一套 Router 规则，并用可回滚的确定性工具完成「会话结晶后领取迭代」。

**Files / Modules to Change**

| 模块 | 计划改动 | 服务 AC |
|---|---|---|
| `Coder/00_System_Prompt/workflow-router.md` | 新增 Router 的候选选择、消歧、返回状态和高风险边界真源 | AC1、AC5–AC7 |
| `Coder/20_Workflow_Lifecycle/iteration-intake.md` | 新增会话结晶、开工意图门、active 分流和确定性工具调用规则 | AC8–AC11 |
| `Coder/README.md`、`docs/codex-compatibility.md` | 登记两份新规则、共同内核与宿主边界 | AC1、AC12 |
| `workflows/registry.json` | 升为 schema v2，新增顶层 `router`、每个 workflow 的 `routing` 和 `iteration` 工作流 | AC2、AC5–AC8 |
| `scripts/sync-workflow-registry.py` | 校验 Registry v2，生成 Router / iteration 投影、Skill UI 元数据、软链和人读表 | AC2–AC5、AC8、AC12 |
| `.claude/commands/butler.md` | 新增 Claude `/butler` Router 薄入口 | AC1、AC3、AC5–AC7 |
| `.claude/commands/butler/iteration.md` | 新增 Claude `/butler:iteration` 薄入口 | AC8–AC11 |
| `plugins/butler/skills/butler-router/` | 新增 Codex / ChatGPT Router Skill 和 `agents/openai.yaml` | AC1、AC4–AC7 |
| `plugins/butler/skills/butler-iteration/` | 新增会话转迭代 Skill 和 `agents/openai.yaml` | AC8–AC11 |
| `tools/iteration-intake/` | 新增 `plan/apply` 执行器、spec schema、事务回滚和 fixture 测试 | AC9–AC11 |
| `scripts/configure-global-install.py` | 在现有命名空间目录软链外，安全管理 Claude 根命令 `butler.md` 软链 | AC3、AC12 |
| `scripts/test-workflow-registry.py`、`test-configure-global-install.py`、`verify-codex-workflows.sh`、`verify-dual-host.sh` | 扩展 schema、投影、安装、高风险和双宿主回归 | AC2–AC8、AC12 |
| `plugins/butler/.codex-plugin/plugin.json`、`docs/workflows.md` | 更新能力摘要和生成的工作流表 | AC4、AC8、AC12 |

**Interface / Contract**

- Registry 升为 `schema_version: 2`，顶层固定为 `schema_version / plugin / router / workflows`。
- `router` 固定包含 `rule_source`、四个返回状态、`allow_implicit_invocation: true`、Claude 投影和 Codex 投影；它不进入 `workflows` 候选集。
- 每个 workflow 新增 `routing`：`priority` 为有界整数，`negative_triggers`、`conflicts_with`、`prerequisites` 为 workflow ID 或字符串数组。冲突关系对称，前置图无环，未知 ID 拒绝。
- Router 内部结果为 `{status, primary_workflow, followups, reason, risk, host_entry, requires_confirmation}`；`status` 只允许 `routed / ambiguous / explicit-required / not-butler`。
- 具体 Claude Command 或 Codex Skill 显式命中时不调 Router。Router 每次只选一个 `primary_workflow`，后续工作在当前工作流完成后重新评估。
- `loop` 和 `dangerous` 继续使用现有 `allow_implicit_invocation=false`；Router 命中它们时只返回 `explicit-required`。
- `iteration-intake` spec 固定分开 `confirmed_decisions`、`model_recommendations`、`open_questions`、`in_scope`、`out_of_scope`，不接受 raw transcript 字段。
- `tools/iteration-intake/intake.py plan --project-root <root> --spec <json>` 默认零写入，输出预计迭代号、分流、milestone 归属、将改文件和拒绝原因。
- `apply` 只接受通过 plan 的 spec，对台账、五件套、task-state、state index 和 handoff 执行同一事务；任一步失败恢复写入前字节。
- 项目已有 active 迭代时，`plan` 返回 `active-exists` 且 `apply` 拒绝。Skill 根据当前阶段提示并入 P1、迭代内修订或扩张转新迭代，不自动绕过生命周期。

**State / Boundary**

- 会话语义由模型结晶；编号、active 不变量、文件重置、台账、回滚和 handoff 由确定性工具负责。两类职责不混写。
- 工具不保存会话原文；只把 spec 中的结晶结果写入 CONCEPT 和状态文件。
- 单纯总结请求不产生 spec 并不调 `apply`；只有同时存在明确开工意图时才允许写盘。
- Pi 继续发现现有 `.agents/skills/`，但本迭代不声称 Pi Router 完成，也不改 `plugins/butler-pi/`。
- 无 `prd_refs`，Workspace Write Plan 不适用。未命中 Domain / Stack Profile，只按通用 SOP、Python 安全边界和已有仓库验证门禁推进。

**Design Decisions**

- Router 使用「确定性约束 + 模型语义判断」两层：Registry 先排除禁止隐式调用、负向触发和前置不满足项，模型再在合法候选中按语义选择。不引入向量检索或网络分类服务。
- Router 是元入口，`iteration` 是真正的业务工作流。这样既避免 Router 路由到自身，又让重复需求可独立显式调用。
- 不把 `iteration` 塞进 milestone Skill。Milestone 管跨多迭代的版本方向，iteration intake 管一次需求的开启，两者的号码、状态和用户意图不同。
- Claude 同时管理 `~/.claude/commands/butler` 目录软链和 `~/.claude/commands/butler.md` 文件软链。两个目标的所有权、断链、旧 checkout 迁移和 TOCTOU 检查复用现有安全安装模型。
- Codex Router 的 Skill description 覆盖「用户选择 Butler 总入口、需求未指定具体工作流」；`butler-iteration` description 覆盖「总结当前会话并现在开迭代」。两者都允许隐式调用，但写盘意图门仍由 iteration-intake 真源复核。

**Plan Admission**

- **AC Coverage**：AC1 由两份 Coder 真源与薄适配器引用检查覆盖；AC2–AC8 由 Registry v2、Router 四状态、双宿主投影和高风险负向样例覆盖；AC9–AC11 由 iteration spec、plan/apply 事务和 active fixture 覆盖；AC12 由同步幂等、安装矩阵、官方 Skill 校验和完整 CI 覆盖。
- **Assumptions**：仓内可以验证命令 / Skill 的结构和共享路由契约，但不能单靠静态测试证明每次 LLM 语义判断都相同；真实 ChatGPT `@Butler` 界面行为也需宿主环境验证。P5 必须按「仓内可靠 + 宿主待人」分级，不把结构检查写成界面端到端通过。
- **Alternatives / Trade-offs**：只依赖 13 个 Skill description 最省改动，但无法统一处理模糊请求、串联和高风险退路；把全部语义编码成硬规则可机械测试，但多语言自然语言会迅速膨胀成脆弱词表。采用共享约束 + 模型语义判断，用 fixture 校验可机械部分，并如实保留宿主验证盲区。
- **Failure Modes**：见下节，包括命令命名冲突、Router 自路由、高风险误开启、会话误结晶、双 active、事务半失败和生成投影漂移。
- **Impact / Scope Challenge**：没有必要在本迭代引入 Pi Router、向量库或学习系统。但如果不改 Claude 全局安装，`/butler` 只会存在于源码而无法全局使用；如果不加确定性 iteration 执行器，就会继续重复手工改多份状态文件的旧问题。两者都是闭环所需，不属范围膨胀。
- **Verification Blind Spots**：静态 fixture 不能完全复制 Claude / ChatGPT 的真实语义调用；Claude 是否接受同名根命令文件和命名空间目录必须在实际 Claude Code 中验证。若当场无法取得证据，仓内交付只标弱验证，不宣称完整可用。
- **Verdict**：`pass` — AC 映射、文件边界、事务策略和验证路径已完整，没有已知 Must Fix；等待用户 ACK 后才把顶部状态置为 `pass` 并进入 P4。

**Execution Steps**

- [x] T1 新增 Router 和 iteration intake 两份共享规则，并在 Coder 入口与兼容文档登记边界 → AC1、AC7、AC9–AC11
- [x] T2 升级 Registry v2，新增 Router 元入口、routing 元数据、iteration 工作流和严格 schema 校验 → AC2、AC5–AC8
- [x] T3 实现 Claude `/butler` / `/butler:iteration` 与 Codex `butler-router` / `butler-iteration` 薄适配器 → AC1、AC3–AC9
- [x] T4 实现 iteration-intake `plan/apply`、spec 校验、active 拒绝、号码分配、五件套重置、状态同步和失败回滚 → AC9–AC11
- [x] T5 扩展 Registry 投影、Claude 全局安装、plugin 能力摘要和人读表 → AC2–AC4、AC8、AC12
- [x] T6 补齐 Router、iteration 事务、Registry、安装器和双宿主正负 fixture，包含故障注入 → AC2–AC12
- [x] T7 运行专项回归、官方 Skill / plugin 校验、完整 CI 和可用的真实宿主探测，生成按 AC 绑定的 evidence → AC3–AC12

## Failure Paths

- **Claude 根命令与目录命名冲突**：先用临时 HOME 验证两个软链可共存，再做实际 Claude 发现探测。如宿主不支持，回 P3 改成可验证的显式名称，不伪造 `/butler` 可用。
- **Router 路由到自身**：Registry schema 把 Router 放在顶层独立对象，候选遍历只读 `workflows`；自路由 fixture 必须失败。
- **高风险误开启**：确定性筛选先读 `allow_implicit_invocation`；即使语义高度相似，Router 也只能返回 `explicit-required`。
- **把模型建议写成用户决定**：spec 三分类是强制字段，不能合并成一段 summary；fixture 对账三类在 CONCEPT 中的落点。
- **总结请求误写盘**：Skill 先判断是否同时存在明确开工动词；只读 fixture 对比全项目树哈希。
- **双 active**：`plan` 和 `apply` 都重新读复合台账，任一 active 都拒绝；apply 提交前再做 TOCTOU 对账。
- **部分文件已写入后失败**：apply 先保存所有受影响路径的字节、模式和软链信息，任一子步异常时逆序恢复；故障注入覆盖每个提交点。
- **Registry 投影半更新**：继续复用现有 `apply_projections()` 的快照与逆序回滚，并把 Router 特殊路径纳入同一投影集。
- **宿主语义表现无法稳定复现**：仓内只对共享规则、候选约束和投影一致性打可靠证据；真实宿主结果只在可实测时记录，否则留为待人验证。

## Test Strategy

- **Registry v2**：扩展 `scripts/test-workflow-registry.py`，覆盖顶层 Router、13 个业务 workflow、routing 严格 schema、对称冲突、无环前置、高风险政策、投影幂等与失败回滚。
- **Router 合同**：新增共用 fixture，覆盖直接入口优先、普通单候选、多候选、前置不满足、`loop/dangerous`、非 Butler 请求和一次一主路由。静态测试验证合同和候选集，不冒充 LLM 端到端证据。
- **Iteration intake**：在临时项目覆盖零写 plan、正常 apply、复合台账取号、active milestone 归属、五件套整体重置、handoff 新鲜、只读总结、P1/P2 active 拒绝与全提交点故障注入回滚。
- **Claude 安装**：扩展 `test-configure-global-install.py` 和 `verify-dual-host.sh`，检查目录软链 + 根文件软链的首装、幂等、旧 checkout 迁移、非 Butler 冲突保留、断链和预检失败零部分写入。
- **Codex Plugin / Skills**：让 `verify-codex-workflows.sh` 从 registry 验证 13 个业务 Skill + 1 个 Router Skill，逐个运行仓内钉版的官方 plugin / Skill validator，检查 Router 与 iteration 允许隐式调用。
- **综合回归**：运行 `python3 scripts/test-workflow-registry.py`、iteration-intake 专项测试、`python3 scripts/test-configure-global-install.py`、`bash scripts/verify-codex-workflows.sh`、`bash scripts/verify-dual-host.sh`、`git diff --check` 和 `bash scripts/verify-ci.sh`。
- **真实宿主探测**：当前环境能调用 Claude / Codex 时，分别验证总入口发现、直接入口优先和高风险退路；不能调用时在 VERIFY 中标为待人验证。
- 本迭代不声明 TDD cycle，`TDD Pair Status` 写 N/A。

## References Compliance

- N/A — 本迭代无 `.ai/references/` 外部参考资料；设计依据均为仓内 `Coder/`、Registry、同步器、安装器与已有测试契约。
