> R4 两帮手定义 + 接线（ITER-0030）· active · —

本文件是**当前活跃迭代 ITER-0030**（MILE-0003 R4）的对象级变更流（ADD/EDIT/DELETE）。收口时归档至 `iterations/ITER-0030/CHANGELOG.md`。

## ADD

- `Coder/62_Extension_Agents/knowledge-fold.md` — 更新说明帮手完整定义（收尾把本迭代 delta 按主题折进 `.ai/project/`、只写该目录；六段式镜像 independent-review；G1–G4 回指 overview）→ AC1
- `Coder/62_Extension_Agents/drift-check.md` — 查过时帮手完整定义（冷启动/收口对着真实代码抽查说明过时、只读、输出漂移清单落 `.ai/references/`；六段式；G1–G4 回指 overview）→ AC2

## EDIT

- `Coder/62_Extension_Agents/overview.md §2` — 名册表更新说明 / 查过时两行状态 🔜 R4 → ✅ 本轮立；删占位说明句（co-edit）→ AC3
- `Coder/20_Workflow_Lifecycle/iteration-schema.md §5.5 步④` — 文件夹态折叠句加"（可唤 knowledge-fold 帮手 fresh-context 执行）"最小回指，折叠必做语义不变 → AC4
- `Coder/40_Context_Management/context-persistence.md 第 6 不变量` — 加"（可唤 drift-check 帮手抽查）"最小回指，漂移强制语义不变 → AC4
- `Coder/README.md` — 目录树 `/62_Extension_Agents` 补两文件 + 分文件说明补两行 → AC8

## DELETE

- 无
