<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0109

方案状态: pass

## Design Decisions

- **产物落点**：新增 `Coder/context-map.md` 作为按需读取的主链上下文映射；它不是执行真源，只登记四类事实层级和 5 个转换块。每块固定九个字段：源上下文、目标上下文、输入、输出、最小保真、失效条件、责任方、权威关系、直接真源。
- **导航接线**：`Coder/README.md` 注册该按需入口；`Coder/domain-model.md` 的“主链关系”改为薄摘要 + 指针；`Coder/architecture-overview.md` 只补职责回指。L0 不直接展开合同，普通任务仍停在专项规则，跨上下文任务经 L1 再进入映射。
- **机械检查**：扩展 `tools/context-budget/context_budget.py`，复用现有 Markdown 解析、仓内路径解析和 symlink 防逃逸；检查恰好 5 段、九字段齐全、四类事实层级合法、失效条件含修复真源、直接真源存在且位于项目根、合同体量有界且禁止递归展开。
- **测试与说明**：扩展 `tools/context-budget/tests/test_context_budget.py` 的 fixture 和负例，更新 `tools/context-budget/README.md`。`scripts/verify-ci.sh` 已运行该单测与基线检查，不增加第二个 CI 入口。
- **不改运行算法**：不修改 PRD、artifact、evidence、Goal Assurance 或 handoff 工具；合同只描述它们之间已经成立的交接责任。R4 的 dangerous/loop 和人测试点保持未实现。
- **AC 映射**：合同结构覆盖 AC1；五段正文分别覆盖 AC2–AC6；事实分层、修复真源与防双写覆盖 AC7；导航、检查器、负例和完整 CI 覆盖 AC8。
- **替代方案与取舍**：否决把五段塞回 `domain-model.md`，因为会突破 L1 导航职责并增加冷启动成本；否决新增 JSON/YAML registry，因为本轮没有执行消费者，先用受检查的 Markdown 验证收益；否决独立新 checker，因为现有 context-budget 已拥有渐进加载和真源安全边界。
- **Plan Admission**：AC1–AC8 均有文件落点和验证动作；唯一关键假设是固定字段块足以机械校验而无需复制 schema，经现有 parser 能力可验证。范围未扩张，已知 Must Fix=0，verdict=`pass`；2026-07-31 经 `user-ack` 准入。

## Failure Paths

- 合同缺转换、重复转换、缺字段、空字段或未知上下文/事实分类：检查器 fail-closed，并指出转换与字段。
- 失效条件没有明确“修复到哪份权威真源”，或直接真源不存在、越出项目根、经 symlink 逃逸：检查器拒绝。
- 导航文档复制状态表/字段全集、允许递归展开或合同体量超过预算：结构/体量守卫拒绝；若必须复制才能表达，退回 P3 重审，不放宽门槛。
- 扩展检查破坏 R2 的 L0/L1 预算或 20 术语/5 上下文/4 路径基线：现有 context-budget 基线测试直接失败。
- 完整 CI 暴露现有工具行为与合同相反：登记 Goal Calibration，按事实回退 P1/P2/P3，而不是改文档掩盖冲突。

## Test Strategy

- 不声明 TDD cycle；使用实现后正负回归。
- 专项单测：基线 5 段通过；删除转换/字段、重复身份、未知分类、缺修复真源、坏路径、仓外 symlink、递归措辞和超预算均失败。
- 合同基线：`python3 tools/context-budget/context_budget.py check --project-root .`，同时验证 R2 与 R3 指标。
- 仓库门禁：artifact contract、Markdown 链接、state audit、`git diff --check`、`bash scripts/verify-ci.sh`。
- P5 逐 AC 生成 evidence；失败记录保留但不覆盖绿色 AC，同上下文审查至少核语义对账、防双写和路径安全。

## References Compliance

- N/A：本迭代来源是 Butler 仓内规则真源与普通对话 brief，不存在外部 PRD 或 `.ai/references/` 钉版输入。
