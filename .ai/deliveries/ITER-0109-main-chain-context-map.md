# 上下文映射与主链转换合同

## 本次交付目标

把 PRD→AC→TECH_PLAN→Evidence→Goal→Handoff 主链从分散的规则暗示，收敛为可按需读取、可机械检查且不复制既有 schema 的跨上下文转换合同。

## 已完成内容

- 建立权威事实、受控投影、派生视图、叙述摘要四类事实，以及五段主链转换。
- 每段统一记录源/目标上下文、输入、输出、最小保真、失效条件、责任方、权威关系和直接真源九个维度。
- 扩展 context-budget 检查器与 9 项正负测试，校验转换数量、分类方向、唯一修复真源、仓内路径、体量及渐进读取约束。

## 关键变更 / 用户可感知变化

- 跨阶段设计时可以只打开 `Coder/context-map.md` 的相关转换块，再首批读取最多 3 份直接真源；不需要递归展开整套领域文档。
- 主链每次转换都能回答“从哪里来、保留什么、何时失效、出错回哪修”，Goal 与 handoff 等派生视图不能反写真源。
- `domain-model.md` 仍是轻量 L1 地图，只增加一个按需指针；L0 冷启动预算没有增长。

## 高层影响范围

- 规则导航：`Coder/context-map.md`、`Coder/domain-model.md`、`Coder/README.md`、`Coder/architecture-overview.md`。
- 工程门禁：`tools/context-budget/context_budget.py` 及其测试与说明。
- 项目知识：`.ai/project/architecture.md`、`.ai/project/invariants.md`、`.ai/project/frontier.md`。

## 验证方式与结果摘要

- AC1–AC8 均有 passed 机器证据；13 个 evidence ID 的完整性校验通过并已归档。
- 专项 9/9、主链合同、Markdown 链接、artifact contract、state audit、diff check 和完整 CI 均通过。
- Goal Assurance 为 `eligible`；同上下文审查发现的严格分类缺口已修复，最终 Must Fix=0、Should Fix=0。

## 已知剩余风险 / 延后事项

- 当前证明的是静态合同和真源一致性，还没有宿主运行时读取/转换遥测。
- `independent_review=false`，本轮未执行 fresh-context 独立复核。
- 高风险身份、状态和引用的机器合同，以及 dangerous/loop、人测所有权两个试点留给 MILE-0015 R4。

## 引用（只引用，不嵌入）

- `.ai/iterations/ITER-0109/AC_LIST.md`
- `.ai/iterations/ITER-0109/TECH_PLAN.md`
- `.ai/iterations/ITER-0109/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0109/CHANGELOG.md`
- `.ai/iterations/ITER-0109/evidence/`
