<!-- butler-artifact-template: 1.0.0 artifact=changelog -->
# ITER-0111 变更流

> 领域治理接线与真实 dogfood（MILE-0015 R5） · closed · 2026-08-17

## ADD

- `Coder/30_Quality_Gate/review-standard.md` §5「领域变更 (Domain Change)」：新增审计维度，含触发范围（4 份领域文件 + 3 份 L0 载体）、四项强制声明（唯一所有者 / 兼容影响 / 迁移路径 / 负向样例）与两道机器门的边界说明 → AC1
- `Coder/20_Workflow_Lifecycle/migration-schema.md` §5「领域变更的升级处置」：新增判据表（运行时实时读 vs 注入目标项目）+ 术语改名的旧名落档判定 + 无影响也须显式落 `## 不需要动作` → AC6
- `tools/domain-contract/domain_contract.py` `_validate_coverage()`：新增条目覆盖门，未被任何断言或关系锚住即 fail-closed 并指名条目 id → AC2
- `tools/domain-contract/domains.v1.json` `assertions[]`：新增 5 条——桥四态机器码枚举、桥输入/输出契约小节（补两条此前零覆盖条目的锚点）、review-standard 维度与四项声明、review-engine 回指锚点、migration-schema 升级判据 → AC1/AC2/AC6
- `AGENTS.md`「核心概念渐进读取（L0）」+ `templates/rule-card.md`「核心概念渐进读取（L0）」：新增 L0 标记块，正文为 `Coder/README.md` 的字节投影 → AC4/AC5
- `tools/context-budget/context_budget.py` `_l0_block()` / `L0_SOURCE` / `L0_PROJECTIONS`：新增 L0 提取函数与三处字节一致校验，metrics 增 `l0_projections` → AC4
- `tools/domain-contract/tests/test_domain_contract.py`：新增 6 例（未覆盖负例 / owner 锚点 / source 锚点 / relation 锚点 / 桥条目回归锁 / 治理接线断言注册与篡改） → AC7
- `tools/context-budget/tests/test_context_budget.py`：新增 3 例（两处投影各自被改、真源被改致两处同时失配、投影侧标记缺失 fail-closed） → AC7

## EDIT

- `Coder/README.md`「核心概念渐进读取（L0）」：标题移出 `butler-context-l0` 标记块之外，标记内只留 5 条规则正文，使三处宿主入口可各用自己的标题层级；L0 正文 694 → 656 字节 → AC4
- `Coder/README.md` `tools/domain-contract/` 条：补覆盖门语义（登记条目必须至少被一条断言或关系锚住） → AC2
- `Coder/README.md` `60_Extension_CodeReview/review-engine.md` 条：补「领域变更」维度登记与口径指针 → AC1
- `Coder/60_Extension_CodeReview/review-engine.md` §3.3 / §7：多维评审列表新增「领域变更」项并回指 `review-standard.md §5`；关系表注明口径由 review-standard 独占、本文件只登记 → AC1
- `Coder/30_Quality_Gate/review-standard.md`：原 §5「领域专项审计」顺延为 §6 → AC1
- `Coder/20_Workflow_Lifecycle/migration-schema.md`：原 §5「幂等与漂移契约」顺延为 §6、原 §6「与切版 / 升级流程的关系」顺延为 §7 → AC6
- `Coder/40_Context_Management/project-digest-schema.md` R6 条：两处 `migration-schema.md §6` 因上条顺延改为 `§7`（全仓唯一受影响的活引用） → AC6
- `tools/context-budget/tests/test_context_budget.py` `setUp()`：临时根拷贝清单补 `AGENTS.md` 与 `templates/rule-card.md` → AC4
- `tools/domain-contract/domain_contract.py` 模块 docstring：补覆盖门语义 → AC2

## DELETE

- N/A
