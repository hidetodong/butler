<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0110 变更流

> 最小可执行领域合同与双冲突试点（MILE-0015 R4） · closed · 2026-08-13

## ADD

- `Coder/30_Quality_Gate/bounded-convergence.md` — 新增共享「有界 P4 收敛策略」（定量熔断 + RCA 单一真源）→ AC3/AC4
- `tools/domain-contract/domains.v1.json` — 新增领域合同注册表（6 entry + 关系 + 断言）→ AC1/AC2
- `tools/domain-contract/domain_contract.py` — 新增领域合同检查器（fail-closed 校验重复/悬空/越界/复制型载荷 + 断言）→ AC1/AC2
- `tools/domain-contract/tests/test_domain_contract.py` — 新增 11 例正负 fixture（逐类命中具体诊断）→ AC7
- `tools/domain-contract/README.md` — 新增工具说明 → AC1/AC2

## EDIT

- `Coder/65_Extension_Dangerous/dangerous-engine.md §4/§6/§9` — Dangerous P4 复用共享有界收敛策略、与 Loop 并列 → AC3/AC4
- `Coder/55_Extension_ConvergenceLoop/convergence-loop-engine.md §6/§7/§8` — 熔断纪律指向共享策略、解除「被直接复用」包含 → AC3/AC4
- `Coder/30_Quality_Gate/correction-contract.md §3` — 无人值守行改引用共享有界收敛策略 → AC3/AC4
- `Coder/00_System_Prompt/logic-protocol.md` — Dangerous 描述去「以收敛闭环」必然组成 → AC3/AC4
- `Coder/README.md` — 目录结构/规则说明/工具列表注册 bounded-convergence 与 domain-contract → AC3/AC4/AC8
- `tools/artifact-pipeline/artifacts.v1.json` — verify_report.sections 加「人测道小结」段 → AC5
- `tools/artifact-pipeline/templates/VERIFY_REPORT.md` — 加「人测道小结」段（缺省 N/A）→ AC5
- `Coder/20_Workflow_Lifecycle/verify-schema.md §2/§3` — 人测段只解释触发/回填、去自立省略口径 → AC5
- `tools/artifact-pipeline/migration.py` — strict VERIFY 缺段确定性迁移 + 幂等 + 拒绝诊断 → AC6
- `tools/artifact-pipeline/tests/test_migration.py` — 加 5 例 strict 迁移测试 → AC6/AC7
- `scripts/verify-ci.sh` — 挂 domain-contract 测试 + check → AC8

## DELETE

- `.ai/project/debt.md` — 删除「verify-schema 人测段与 manifest 不一致」欠债条目 → AC5
- `.ai/project/debt.md` — 删除「危险模式与 Loop 规则语义错误耦合」欠债条目 → AC3
