> R3 维护回路接线（ITER-0029）· active · —

本文件是**当前活跃迭代 ITER-0029**（MILE-0003 R3）的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0029/CHANGELOG.md`。

## ADD

- `Coder/40_Context_Management/context-persistence.md §冷启动一致性自检` — 新增**第 6 条「知识文件夹漂移自检」**（条件不变量：采用 `.ai/project/` 的项目核对近期 delta 是否都已折进对应 topic、有无被取代结论残留；单文件 PROJECT.md 项目 N/A）→ AC3

## EDIT

- `Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5` — 步④「按需前滚 PROJECT.md」泛化为两态（文件夹态按主题路由 delta 折进 `.ai/project/` 必做 / 单文件暂态前滚）；步内引用 `project-digest-schema.md §5`→`§6`；步⑤ 一致性自检计数 5→6 + 列举补第 6 条 → AC1/AC4/AC5
- `Coder/20_Workflow_Lifecycle/milestone-schema.md §7.4` — 步④ 两态泛化（注明迭代级已增量折、里程碑保版本级全貌）；引用 §5→§6 → AC2/AC5
- `Coder/20_Workflow_Lifecycle/lifecycle.md §迭代收口` — 步④ 语义对齐两态 + 步⑤ 计数 5→6 → AC4
- `Coder/20_Workflow_Lifecycle/versioning-schema.md §切版自检` — 一致性自检 5→6 + 列举补第 6 条（条件） → AC4
- `Coder/40_Context_Management/project-digest-schema.md §6/§9` — R3 前向指针 待→已接线（指向 iteration-schema §5.5 / context-persistence 第 6 不变量）→ AC6
- `.ai/PROJECT.md 关键长期决策与不变量` — 收口前滚：收口仪式步④两态 + 一致性自检 5→6 + 知识文件夹 R3 已接线（收口步④，若判据成立）

## DELETE

- 无
