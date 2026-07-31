<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0101 变更流

## ADD

- `Coder/context-map.md`：新增四类事实层级与五段主交付链转换合同，每段固定九个维度并回指唯一执行真源（AC1–AC7）。

## EDIT

- `Coder/domain-model.md`：把主链关系收敛为 L1 薄摘要，并按需指向上下文映射（AC8）。
- `Coder/README.md`、`Coder/architecture-overview.md`：注册主链合同入口与职责边界，不把正文复制进冷启动导航（AC7、AC8）。
- `tools/context-budget/context_budget.py`：扩展四类事实、五段转换、九字段、方向、修复真源、仓内路径、体量与渐进加载检查（AC1–AC8）。
- `tools/context-budget/tests/test_context_budget.py`：扩展 fixture 与 3 组主链合同负向测试，专项合计 9 项（AC1、AC7、AC8）。
- `tools/context-budget/README.md`：登记主链映射检查范围和边界（AC8）。

## DELETE

- N/A
