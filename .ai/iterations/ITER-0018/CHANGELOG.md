> 每迭代 changelog 正式化：01_CHANGELOG 重定义为严格 ADD/EDIT/DELETE 变更流 · active · —

## ADD
- `Coder/20_Workflow_Lifecycle/changelog-schema.md` — 新增迭代变更日志格式契约（格式 / 粒度 / 噪声地板 / 四产物分工 / 产出归档） → AC1 AC2 AC8
- `.ai/01_CHANGELOG.md` — 本迭代变更流，dogfood 新格式 → AC7
- `.ai/iterations/ITER-0017/CHANGELOG.md` — 回填 ITER-0017 变更日志作范例 → AC7

## EDIT
- `Coder/20_Workflow_Lifecycle/mcv-deployment.md §43` — 01_CHANGELOG 语义由"技术决策与需求增量"改为对象级 ADD/EDIT/DELETE → AC3
- `Coder/20_Workflow_Lifecycle/maintenance-boundaries.md §15` — CHANGELOG 行重定义为 ADD/EDIT/DELETE 触发口径，删除 Should Fix 输入 → AC3 AC4
- `Coder/20_Workflow_Lifecycle/iteration-schema.md §4.4 §5.5` — 措辞对齐对象级变更 + 完整路径收口必产 01_CHANGELOG 并归档 → AC3 AC5
- `Coder/20_Workflow_Lifecycle/lifecycle.md §165` — 收口 step ① 改为必产 changelog 切片 → AC3 AC5
- `Coder/20_Workflow_Lifecycle/mcv-update.md §5.1` — 加 changelog-schema 指针，消"决策快照"旧义残留 → AC3
- `Coder/60_Extension_CodeReview/review-engine.md §71` — Should Fix 改记入 VERIFY_REPORT 的 Remaining Risks → AC4
- `Coder/65_Extension_Dangerous/dangerous-engine.md §121` — Should Fix 改记入 VERIFY_REPORT 的 Remaining Risks → AC4
- `Coder/20_Workflow_Lifecycle/verify-schema.md §4` — 收端补 Remaining Risks 承载 Should Fix 口径，契约双向闭合 → AC4
- `Coder/20_Workflow_Lifecycle/delivery-summary.md §边界` — 明确与 changelog 分工（高层/细粒度）+ 指针 → AC8
- `Coder/README.md §目录树 §描述` — 注册 changelog-schema.md → AC6

## DELETE
- 无
