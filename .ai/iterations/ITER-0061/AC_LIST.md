---
状态: ack-frozen
ACK 日期: 2026-07-18
---

> ⚠️ 危险模式：本产物由模型自主 ACK（已过验收自审门），未经用户逐项确认（ITER-0061，2026-07-18）。

# Goal

- 以可复核、可转成后续测试输入的形式冻结 Butler 目标体系现状、缺口、层级边界和假完成失败模型。

# In Scope

- 共同规则、运行态和双宿主入口中的目标/计划/进度/完成载体盘点。
- 当前会话可观察的 Codex Goal 合同与未知宿主能力边界。
- 结构化失败样本、层级矩阵、已具备保障与缺失保障。
- R2–R6 的输入/责任分界，不提前实现后续路线。

# Out of Scope

- 不定义最终 Goal Contract 或状态枚举。
- 不修改 P1–P5、review、dangerous、hook、auditor 或宿主适配行为。
- 不宣称宿主能力跨版本稳定，不制造“100% 置信”字段。

# Acceptance Checklist

- [ ] AC1：基线逐项列出 milestone、iteration、CONCEPT Goal、AC、TECH_PLAN、task-state、VERIFY/review、dangerous 北极星与宿主 goal/task 载体，标明角色、权威度、消费者和现有完成语义。
- [ ] AC2：边界矩阵明确方向层、范围层、完成定义、方案、执行进度、证据/裁决各自真源，并指出不得互相替代的关系。
- [ ] AC3：至少固化 8 个假完成反例；每例含稳定 ID、前置事实、错误声明、预期处置、阻断原因和未来承接路线，覆盖方案未通过、AC 未覆盖、证据缺失、Must Fix、阻断风险、范围漂移、宿主状态漂移和任务清单假完成。
- [ ] AC4：双宿主审计诚实区分当前会话可观察 Codex Goal 合同、Butler plugin/skill 能力和 Claude 未建立的映射；不把未知写成支持。
- [ ] AC5：基线给出 R2–R6 的最小输入与依赖顺序，并明确 R1 不选择“独立 Goal 文件”或“派生视图”方案。
- [ ] AC6：人读基线与机器可读 fixture 一致，JSON 可解析、ID 唯一、必填字段闭合，仓库 Markdown/状态审计和完整验证入口不因本轮文档产物回归。

# Verification Method

- AC1–AC2：用固定关键词/表头检查基线矩阵，并由主 agent 对照规则真源逐项复核。
- AC3：Python 标准库校验 fixture 恰好覆盖要求类别、ID 唯一、字段集合严格，逐例对照人读报告。
- AC4：检查报告含 `observed-current-session` / `documented-butler` / `unknown` 来源等级，且无 Claude 原生 Goal 已支持的肯定声明。
- AC5：检查 R2–R6 输入映射齐全，R1 决策栏明确 deferred。
- AC6：运行 fixture 校验、Markdown 链接检查、状态审计、`git diff --check` 与 `bash scripts/verify-ci.sh`，用 verification evidence 捕获。

# Open Questions / Risks

- 当前 Codex Goal 工具合同来自本会话可观察能力，不等同于公开、跨版本稳定 API；R6 必须再按当时宿主能力适配。
- R1 只提供失败 oracle，不会立刻阻止假完成；机械拒绝要到 R5 才闭环，交付中必须如实标为后续路线。
