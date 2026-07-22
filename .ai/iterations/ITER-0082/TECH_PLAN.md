---
方案状态: pass
方案审查日期: 2026-07-22
方案审查方式: dangerous-self-review
---

> ⚠️ 危险模式：本方案已过完整 Plan Admission 并由模型自主放行（ITER-0082，2026-07-22）。

# Goal

- 以一个零依赖共享解析内核支撑 AC1–AC10：CLI 负责发现/校验/计划/diff，PreToolUse rule 负责逐目标写前拒绝，e2e 证明 R1–R8 组合成立。

# Files / Modules to Change

- `templates/hooks/lib/workspace_scope.py`：工作区地图、Path Ownership、AC `prd_refs`、钉版 PRD/模块范围、TECH_PLAN 写计划、路径归属与 manifest 发现的共享只读内核。
- `tools/workspace-scope/`：`discover|validate|check-plan|check-paths|check-diff` CLI、README 和隔离行为测试。
- `templates/hooks/rules/workspace_scope.py`、dispatcher/tests：PRD-backed 迭代的写前范围门禁；Claude 部署副本随现有 hooks 同步，Codex wrapper 直接调用 Butler 真源。
- `workspace-scope-schema.md`、TECH_PLAN/VERIFY/部署与 Coder 入口：补精确 Module Workspace Scope、Path Ownership、Write Plan 和双层覆盖口径。
- `tools/mile0009-e2e/`：组合 inbox、PRD collection/update/migration、范围工具和 apps 临时副本的版本级 fixture。
- `scripts/verify-ci.sh` 与结构合同：固定接入专项和端到端组。

# Interface / Contract

- CLI：`workspace_scope.py discover|validate|check-plan|check-paths|check-diff --project-root ROOT`；所有命令只读、stdout 单一稳定 JSON，0=通过，1=发现/计划未就绪，2=合同或执行错误。
- 地图保留既有 Workspaces 表；新增可选 `## Path Ownership` 表，字段精确为 `path_pattern | workspace_key | path_kind | evidence`，pattern 仅接受项目相对精确路径或 `/**` 目录前缀。
- 单需求入口新增可选 `## Module Workspace Scope` 表；一行给完整四类列表，模块未列则继承需求级范围，切片原文不加 metadata。
- TECH_PLAN 新增 `# Workspace Write Plan` 表，字段精确为 `workspace_key | access | path_patterns | rationale`；access 只接受 `primary_write/supporting_write`。
- AC `prd_refs` 是范围选择真源；live 版本不符时按该 `prd_id/.archive/<version>/00_INDEX.md` 解析，legacy 无 `prd_id` 不进入强门禁。

# State / Boundary

- 所有消费者只读；`discover` 只提议候选，不写 `.ai/project/workspaces.md`。
- 写允许条件为：目标有唯一 workspace owner ∩ owner 在钉版范围允许写 ∩ owner/access/path 命中 Write Plan。无引用时 N/A；有引用但任一事实缺失/歧义则拒绝。
- 显式 `excluded/read_only` 与另一个引用的显式 write 冲突即拒绝；另一个 PRD 未提该键不算冲突，避免多需求互相把所有包否掉。
- `.ai/`、deliveries 和宿主配置继续由既有黑名单豁免范围 rule；项目流程状态仍由原有 rules 管理。
- apps 原仓只读；复制到系统临时目录的最小完整快照才允许迁移写入，结束后临时目录自然清理。

# Design Decisions

- 把共享内核放在 `templates/hooks/lib/`：Claude 部署时拿到自包含副本，Codex 和驻留 CLI 都复用 Butler 仓中的同一文件，不复制算法。
- 采用显式前缀 pattern，不引入通用 glob：可解释、可做唯一归属和重叠检测，足以覆盖 workspace 目录、根级共享配置与生成文件。
- hook 同时核 scope 和 Write Plan，而非只核 scope：Scope 是最大授权，Plan 是本迭代承诺；只做前者仍允许在整个配套包随手改。
- Git diff 对账作为 shell 等未经过 hook 的 P5 兜底；两层互补，交付不夸大 hook 覆盖。
- apps dogfood 用真实只读源 + 临时副本，而不是改真实仓后回滚：避免把回滚成功误当零影响，也符合冻结授权上限。

# Plan Admission

- AC Coverage：共享内核/CLI 覆盖 AC1–AC5；hook/扩张规则覆盖 AC6–AC7；组合 fixture 与 apps dogfood 覆盖 AC8–AC9；接线/完整收口覆盖 AC10。
- Assumptions：npm root 的 `workspaces` 是 apps 的拓扑入口，已只读确认；现有 prd-migrate 能在副本处理扁平 PRD，若非标准 queued 阻断则应以明确报告而非放宽 parser 解决。
- Alternatives / Trade-offs：独立 daemon 过重；只在 P5 检 diff 太晚；把 parser 复制进 CLI/hook 会漂移；任意 glob 难以唯一归属。选择共享纯函数 + CLI + hook rule + P5 diff。
- Failure Modes：symlink/路径逃逸、manifest pattern 过宽、重复包名、嵌套 workspace、ownership 重叠、archive 钉版缺失、跨 PRD权限冲突、rename 双路径、untracked 漏检、apply_patch 多项目、旧项目无引用，全部有负向 fixture。
- Impact / Scope Challenge：不改宿主权限算法、不拦 shell、不自动写地图/范围；R8 是既有声明合同的消费者与版本级证明，没有引入新的产品工作流。
- Verification Blind Spots：真实 apps 原仓不能写，因此证明的是“真实输入可发现 + 临时副本可迁移且原仓零变化”，不是用户项目已升级；此边界写进交付。
- Verdict：pass；AC 有直接落点，边界和失败恢复明确，无已知 Must Fix。

# Execution Steps

- [ ] T1 实现共享地图/ownership/钉版范围/计划/路径解析内核与 CLI → AC1–AC5
- [ ] T2 接入 workspace_scope hook rule、部署说明与双宿主集成回归 → AC6–AC7
- [ ] T3 建 MILE-0009 组合 e2e 与 apps 只读/临时副本 dogfood → AC8–AC9
- [ ] T4 同步规则/README/CI，执行完整强审、证据归档和迭代/里程碑双收口 → AC10

# Verification Plan

- `python3 -m unittest discover -s tools/workspace-scope/tests -v`
- `python3 -m pytest templates/hooks/tests/test_workspace_scope_gate.py templates/hooks/tests/test_workspace_scope_execution_contract.py -q`
- `python3 -m unittest discover -s tools/mile0009-e2e/tests -v`
- `bash scripts/verify-ci.sh`、`git diff --check`、Goal/state audit。

# Risks / Open Questions

- 当前 milestone 全部改动仍未提交，无法提供干净 Git 回滚锚点；P4 只使用 `apply_patch`、临时目录和只读检查，不执行 reset/checkout/stash/提交。
- 若真实 apps 的非标准状态让现有 migration inspect 都无法读取，将记录为兼容 finding，并在不修改原仓的前提下补工具的只读兼容或明确诊断测试。
