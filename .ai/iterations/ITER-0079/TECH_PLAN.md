---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 用一个标准库工具同时承载引用解析与 legacy 事务迁移，完成 AC1–AC9。

# Files / Modules to Change

- `acceptance-schema.md`、`tech-plan-schema.md`、`verify-schema.md`：多 PRD 钉版与继承/核对。
- `tools/prd-migrate/`：inspect/plan/apply/verify/rollback + reference resolve + tests。
- `references-schema.md`：迁移 receipt、兼容解析与 legacy 状态翻转。
- `docs/prd-migration-guide.md`、`HUMAN_GUIDE.md`、Coder README：人类操作入口。
- 结构/行为 tests、完整 CI。

# Interface / Contract

- `prd_refs` 为 YAML 列表，每项固定 `prd_id`、`prd_version`、`module_slugs`；与 legacy `prd_version` 互斥。
- CLI：`inspect|plan|apply|verify|rollback|resolve`，`--project-root` 必填；plan/inspect/resolve/verify 零写。
- migration receipt 保存 schema/id/prd_id/title/时间、legacy tree hash、迁移树 hash、backup、文件映射与引用影响面。
- JSON stdout；0 成功、1 verify/plan 不满足、2 输入/事务错误。

# State / Boundary

- 只写 `PROJECT_ROOT/.ai/references/` 内 PRD 根、backup/receipt；扫描其他 `.ai` 文件只读。
- apply 前完整 preflight/staging；切换失败立即恢复，成功后 backup 留存。
- closed/frozen 历史绝不自动改；resolver 用 receipt 补 implicit legacy prd_id。
- R6/R7 动作算法不改。

# Design Decisions

- 多行 YAML 比 JSON 单行更人读；工具用窄解析器只认定义形态，未知 YAML fail-closed，不引入运行依赖。
- migration 与 resolver 同工具共享 receipt/路径语义，避免指南和 schema 各造一套兼容算法。
- backup 不自动删除；verify 只证明迁移一致，清理由用户按指南另行决定。
- 不用 symlink 作为唯一兼容层；旧路径的逻辑解析由 receipt 保证，平台行为一致。

# Plan Admission

- AC Coverage：schema AC1–2，resolver AC3/7，migration AC4–7，guide AC8，fixtures/CI AC9。
- Assumptions：legacy 是一份 PRD；若根含日期化子目录或多个身份信号，plan 拒绝。
- Alternatives / Trade-offs：只写散文无法证明事务；原地 move 无恢复；完整 YAML parser增加依赖。选择窄 schema + 标准库事务工具。
- Failure Modes：日期猜错、混合布局、symlink、staging 中断、rename 第二步失败、迁移后漂移 rollback、历史引用断链。逐项有拒绝/恢复测试。
- Impact / Scope Challenge：不把 split/update 顺手塞入 R5；迁移只解决已有 legacy 的结构与引用。
- Verification Blind Spots：真实 apps 项目的历史变体/权限只在 R8 dogfood 验证。
- Verdict：pass；边界、事务与负向矩阵完整，无已知 Must Fix。

# Execution Steps

- [ ] T1 更新三阶段 schema 与 references 兼容合同 → AC1, AC2, AC7
- [ ] T2 实现 resolver 与 fixture → AC3, AC7, AC9
- [ ] T3 实现 inspect/plan/apply/verify/rollback 事务迁移 → AC4–AC7, AC9
- [ ] T4 编写迁移指南并接 HUMAN_GUIDE/Coder README → AC8
- [ ] T5 完整验证、强审、Goal 与状态收口 → AC1–AC9

# Verification Plan

- `python3 -m unittest tools.prd_migrate.tests...`（模块路径最终按目录名确定）。
- `python3 -m pytest templates/hooks/tests/test_multi_prd_migration_contract.py -q`。
- `bash scripts/verify-ci.sh`、`git diff --check`、Goal/state audit。

# Risks / Open Questions

- Python 包目录不能用连字符；CLI 路径可 `tools/prd-migrate/`，测试用 importlib 或独立包名，实施时统一一种可维护入口。
