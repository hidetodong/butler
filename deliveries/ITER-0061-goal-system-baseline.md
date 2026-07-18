# ITER-0061 · 目标体系现状审计与失败模型

> 迭代交付（小版本） · 2026-07-18 · MILE-0008 R1 · 危险模式自主 ACK / 完整审查

## 本次交付目标

先把 Butler 现在怎样表达目标、计划、进度和完成画清楚，并固定一组“任务做完但 Goal 绝不能完成”的反例，为后续 Goal Contract、方案准入、问题回流、完成裁决和双宿主接线提供共同事实基线。

## 已完成内容

- 盘点 12 类目标相关载体，分别标明层级、权威度、消费者、完成语义和来源等级。
- 固化方向、范围、完成定义、方案、执行投影、证据与审查的唯一回答位置，明确宿主 Goal/Task 只能投影项目真相。
- 新增 8 个机器可读假完成 case，覆盖方案未通过、AC 漏覆盖、证据缺失、Must Fix、关键阻断风险、范围漂移、宿主状态漂移和任务清单假完成。
- 区分 Butler 已有保障与六项缺口，并给 R2–R6 留下输入和依赖顺序。
- 明确延期最终 Goal 存储形态、状态机、方案 verdict 落点、回流 action、裁决器形态和宿主 API，避免 R1 抢跑设计。

## 关键变更 / 用户可感知变化

- 现在可以精确解释为什么“所有任务已完成”仍不等于“Goal 已达成”。
- Codex 当前 Goal 能力只标记为本会话观察；Claude 映射未知，不再凭名称相似假设双端对称。
- 危险模式北极星被明确为跨迭代自治方向，不是完成裁决器。
- 后续每条 Goal 强化规则都可以用稳定 case ID 做反证，不必重新靠散文争论假完成边界。

## 高层影响范围

- 新增一份 `docs/research/` 人读基线和一份严格 JSON 负向 fixture。
- 更新 ITER-0061 的 `.ai/` 产物、证据、审计与台账。
- 没有修改 `Coder/**` 运行规则、hook、plugin、workflow registry、宿主入口或版本号；R1 还没有给项目增加 Goal 门禁。

## 验证方式与结果摘要

- 9 个 verification evidence record 全部 passed；严格检查 8 个唯一 case、字段集合、类别覆盖、人读/JSON ID 对账和来源等级。
- 强审前后两次固定工具链完整矩阵均通过；最终包含 955 个 Markdown 文件/43 个链接、8 skills/plugin、127 hook tests 和统一双宿主部署矩阵。
- active state audit 两次通过并保留 `UNRELEASED` 亮牌；三次 diff check 通过。
- 强审发现并修复 1 个 Should Fix：危险模式北极星原先没有独立列明角色。最终 Must Fix 0、Should Fix 0。

## 已知剩余风险 / 延后事项

- 本轮只完成问题基线，假完成尚未被新机制拦截；Goal Contract、方案 verdict、回流引擎、完成裁决器和双宿主同步分别留给 R2–R6。
- 没有执行 fresh-context 独立复核；主 agent 完成危险模式完整强审，并如实标注审查强度。
- Codex Goal 合同需要 R6 按当时环境复核，Claude 原生 Goal/Task 映射仍为 unknown。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0061/AC_LIST.md`
- `.ai/iterations/ITER-0061/TECH_PLAN.md`
- `.ai/iterations/ITER-0061/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0061/evidence/`
- `docs/research/2026-07-18-goal-system-baseline.md`
- `docs/research/goal-failure-cases.v1.json`
- checkpoint `ab075fe`
