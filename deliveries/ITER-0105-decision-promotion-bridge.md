# Decision Map 到 Milestone / Iteration 的确定性交接

## 本次交付目标

把已解决的 Decision Map 切片可靠地交给 Butler 既有交付生命周期，同时避免让模型自行判断需求清晰度、体量或目标路线。

## 已完成内容

- 新增驻留工具 `tools/decision-promotion/`，以 `inspect`、`plan`、`apply`、`verify` 管理确定性交接。
- 提供两个显式 adapter：`route-reference` 只给既有 planned Milestone 路线增加 Decision 引用；`iteration-start` 复用既有 iteration-intake，从 P1 创建一次 Iteration。
- 以 resolved Decision roots 的传递闭包形成 source slice；允许局部 Map 交付，但所有引用决定都必须已解决且依赖闭合。
- 用不可变 promotion receipt 绑定 source digest、target digest 与结果；同一请求可幂等重放，目标变化后旧 plan 会 fail-closed。
- 增加项目根 inode guard、`.ai` 内锁与 pending journal，覆盖 intake 回滚替换 `.ai` 以及强杀留下不完整意图的恢复场景。

## 关键变更 / 用户可感知变化

- Decision Map 最终是可引用的决策来源，不会替代 Milestone 路线、Iteration CONCEPT、冻结 AC 或 P1→P5。
- 交接不再依赖模型给需求贴“清晰 / 大小”标签；调用方必须明确选择 adapter、Decision roots 和既有路线或新 Iteration 参数。
- `route-reference` 不会自动创建 Milestone 或路线；`iteration-start` 不会跳入 P2。active Milestone 存在时必须从其既有 planned 路线启动。
- P2 冻结后的新结论不静默改当前交付：实质变化走 amend / re-ACK，未来方向进入后续路线或迭代。

## 高层影响范围

- 新增 Decision Promotion 深 Module、CLI、合同文档和 18 项专项测试。
- 更新生命周期、Milestone、Iteration、部署、Ideation 及 Decision Map / Work 边界说明。
- 将专项测试、编译检查和边界断言接入完整 CI，但没有新增用户入口、workflow ID、Router 自动分流或外部 tracker。

## 验证方式与结果摘要

- 18 项专项测试通过，覆盖两种 adapter、闭包与 digest、幂等、stale target、并发、回滚、强杀 pending 与不完整状态核验。
- P5 同上下文复核发现的 lock inode 连续性与强杀意图缺口均已修复；最终 Must Fix 0、Should Fix 0。
- 最终 `full-ci-r3` 在 Python 3.12.12 / uv 0.9.28 下 exit 0；先前 `full-ci-r2` 的失败记录作为纠正轨迹保留，不用于覆盖绿色验收。
- 9 份 evidence 已整体归档并通过 archive verifier，AC1–AC10 与 Goal Assurance 均通过。

## 已知剩余风险 / 延后事项

- SIGKILL 后残留 pending journal 会阻止继续 promotion，需要人工核查后处理；这是刻意的 fail-closed，而非自动修复。
- 同一 resolved source slice 可被显式引用到多个路线；当前合同保留该能力，不替业务方判断是否重复规划。
- Router 接线、Butler 自身真实大需求 dogfood 与外部 tracker 价值评估留给 MILE-0014 R5；R5 尚未启动。

## 引用

- `.ai/iterations/ITER-0105/CONCEPT.md`
- `.ai/iterations/ITER-0105/AC_LIST.md`
- `.ai/iterations/ITER-0105/TECH_PLAN.md`
- `.ai/iterations/ITER-0105/VERIFY_REPORT.md`
- `.ai/iterations/ITER-0105/CHANGELOG.md`
- `.ai/iterations/ITER-0105/evidence/`
- `tools/decision-promotion/README.md`
