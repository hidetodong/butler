---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

# Goal

- 用一个新 schema 固化 AC1–AC7，不把工作区范围算法散进 references、TECH_PLAN 或 hook。

# Files / Modules to Change

- `Coder/40_Context_Management/workspace-scope-schema.md`：唯一契约真源。
- `Coder/40_Context_Management/references-schema.md`：单需求索引增加范围指针，不复制算法。
- `Coder/README.md`：目录树和导航注册。
- `templates/hooks/tests/test_workspace_scope_contract.py`：结构合同测试。
- `.ai/*`：迭代状态、归档与交付。

# Interface / Contract

- 项目地图：`.ai/project/workspaces.md`。
- 稳定键：`workspace_key`；优先为 manifest package identity，路径只作当前解析值。
- 需求范围：`primary_write`、`supporting_write`、`read_only`、`excluded`，值均为 workspace key 集合。
- 可写集合：`primary_write ∪ supporting_write`；其他键默认 deny-write。
- 模块范围必须是需求范围逐类子集，且不能解除需求级 excluded。

# State / Boundary

- schema 定义数据和不变量；R8 才实现 TECH_PLAN/diff 消费与门禁。
- 工作区 scope 不扩大危险模式冻结的项目根授权，也不替代宿主权限。
- PRD 继续按需求存放，不按 workspace 重排。

# Design Decisions

- 新建独立 schema：工作区范围横跨 PRD、TECH_PLAN、门禁与项目知识，塞进 references 会让外部规格契约承担代码拓扑职责。
- 地图落 `.ai/project/`：它描述项目当前拓扑，目录移动时覆写当前路径；历史 PRD 只保存稳定键。
- 四类集合而非 allow/deny 二态：主实现与配套写入需要审查时可区分，read-only 与 excluded 也有不同读取语义。
- 未声明默认不可写；安全边界不从“没写禁止”推导允许。

# Plan Admission

- AC Coverage：schema 直接覆盖 AC1–AC6，README/references/test/CI 覆盖 AC7。
- Assumptions：manifest package name 在多数 monorepo 中可作稳定证据；无 manifest 时允许显式稳定键，避免把工具栈假设写死。
- Alternatives / Trade-offs：把路径直接写进每份 PRD 更直观但目录移动会污染历史；全局 allowlist 太粗，无法表达每份需求边界。选择稳定键 + 当前地图，代价是需要一次解析跳转。
- Failure Modes：重复键/路径、`../` 逃逸、未知键、集合重叠、模块扩权、越界后补票。全部 fail-closed 成文并由结构测试保护。
- Impact / Scope Challenge：不修改 TECH_PLAN schema/hook，因为没有 R8 的行为测试就接门禁会把声明式契约与执行耦合。
- Verification Blind Spots：结构测试不能证明真实 monorepo discovery 或 git diff 对账；R8 必须补 fixture 和真实 apps dogfood。
- Verdict：pass。边界清楚、无 Must Fix，可进入 P4。

# Execution Steps

- [x] T1 盘点 R1 契约与项目知识层边界 → AC1–AC3
- [x] T2 设计稳定键、四类集合、子集和扩张纪律 → AC1–AC6
- [x] T3 完成危险模式 P2/P3 自审 → AC1–AC7
- [ ] T4 新增 schema 并接线 references/README → AC1–AC7
- [ ] T5 新增测试并运行完整证据矩阵 → AC1–AC7
- [ ] T6 强审、Goal 裁决与原子收口 → AC1–AC7

# Verification Plan

- `python3 -m unittest templates.hooks.tests.test_workspace_scope_contract -v`
- `bash scripts/verify-ci.sh`
- `git diff --check`、Goal adjudicator、state auditor。

# Risks / Open Questions

- R8 需要明确 generated files 和仓根配置文件如何映射 workspace key；本轮不抢跑。
