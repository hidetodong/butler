<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0100 变更流

## ADD

- `Coder/domain-glossary.md`：新增 L2 20 项核心术语查询表，保留上下文限定、所有者、定义真源与非职责（AC3、AC5）。
- `tools/context-budget/context_budget.py`：新增 L0/L1 预算、五上下文、四路径、升级回执、L2 术语与真源边界的确定性检查（AC1–AC7）。
- `tools/context-budget/tests/test_context_budget.py`：新增基线和 6 组 fail-closed 负向测试（AC1–AC3、AC5–AC7）。
- `tools/context-budget/README.md`：新增命令、退出码、稳定代理与非能力边界说明（AC7）。

## EDIT

- `Coder/README.md`：增加 L0 渐进读取块，注册 L1/L2 入口与按需读法（AC1、AC5、AC6）。
- `Coder/domain-model.md`：从 R1 综合审计收敛为预算内 L1 五上下文地图、四路径和分批升级合同（AC2、AC4、AC5）。
- `Coder/architecture-overview.md`：更新 L1/L2 与规则分层的薄导航，不复制定义（AC6）。
- `scripts/verify-ci.sh`：接入 context-budget 单元测试与项目基线检查（AC7、AC8）。

## DELETE

- N/A
