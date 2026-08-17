<!-- butler-artifact-template: 1.0.0 artifact=tech_plan -->
# TECH_PLAN — ITER-0110

方案状态: pass
方案审查日期: 2026-08-13
方案审查方式: user-ack

## Design Decisions

### Goal（支撑哪些 AC）

- 本轮把 ITER-0110 的 AC1–AC8 落成三块可执行改动：① 新增一个只登记「身份—所有者—真源」的最小领域合同薄工具；② 解除 Dangerous/Loop 的错误包含关系，抽出共享「有界 P4 收敛策略」；③ 把 VERIFY「人测道小结」的结构所有权写回 artifact manifest/template，并给 strict live VERIFY 补确定性迁移。
- 一句话：不改任何 MILE-0014 状态机、不建全仓术语 DSL、不追改历史归档，只让高风险身份/状态/引用各有唯一所有者 + 可执行检查。

### Files / Modules to Change

- 新增 `tools/domain-contract/`（`domains.v1.json` 注册表 + `domain_contract.py` 检查器 + `tests/test_domain_contract.py` 正负 fixture + `README.md`）——领域合同的机器真源与门禁。
- 新增 `Coder/30_Quality_Gate/bounded-convergence.md`——共享「有界 P4 收敛策略」（定量熔断 5 轮 / 死锁 3 轮 / 环境阻塞 + RCA 格式），Dangerous 与 Loop 各自引用、互不包含。
- 修规则耦合措辞（5 个文件）：`65_Extension_Dangerous/dangerous-engine.md`（frontmatter scope、§4 第 4 步、§6、§9）、`55_Extension_ConvergenceLoop/convergence-loop-engine.md`（§6/§7/§8）、`30_Quality_Gate/correction-contract.md`（§3 无人值守行）、`00_System_Prompt/logic-protocol.md`（Dangerous Mode 描述行）、`Coder/README.md`（L0 危险模式 bullet + 目录结构注册新文件/新工具）。
- 修 VERIFY 结构所有权（3 个文件）：`tools/artifact-pipeline/artifacts.v1.json`（verify_report.sections 加「人测道小结」+ conditional_sections）、`tools/artifact-pipeline/templates/VERIFY_REPORT.md`（加「## 人测道小结」段，缺省 N/A）、`Coder/20_Workflow_Lifecycle/verify-schema.md`（只解释触发/回填，删除「无则整段省略」的自立结构口径）。
- 迁移与测试：`tools/artifact-pipeline/migration.py`（strict VERIFY 缺段时确定性插入「人测道小结」）、`tools/artifact-pipeline/tests/test_migration.py`、`tools/artifact-pipeline/tests/test_contract.py`（同步 verify_report 段表预期）。
- CI 与项目知识：`scripts/verify-ci.sh`（挂 domain-contract 测试 + check）、`.ai/project/debt.md`（删除两条已还欠债）。

### Interface / Contract（领域合同 schema + CLI）

- `domains.v1.json` 顶层：`schema_version`、`contexts`（五上下文封闭枚举）、`contract_types`（封闭枚举：模式身份 / 状态枚举 / 结构所有权 / 桥输入输出 / 共享策略）、`entries[]`、`relations[]`、`assertions[]`。
- 每条 `entry`：`id`（稳定、唯一）、`concept`、`context`（∈ contexts）、`type`（∈ contract_types）、`owner`（唯一所有者，仓内路径）、`source`（执行真源，仓内路径）。**不允许**出现 `values` / `fields` / `enum` 等复制型载荷字段（未知字段 fail-closed，落实 AC2「只存导航/关系、不复制正文」）。
- `relations[]`：`kind`（并列 / 共享策略）、引用既有 entry id（悬空引用 fail）。
- `assertions[]`：`file` + `must_contain[]` / `must_not_contain[]`（子串匹配）+ `reason`，把 Dangerous/Loop 错绑、人测段所有权的回归检查数据化。
- `domain_contract.py check --project-root .`：校验注册表完整性（重复 id / 每 entry 唯一且非空 owner / 未知 context·type / source 缺失或越界仓外 → 均 fail-closed）+ 校验 relations 引用 + 逐条执行 assertions。退出码 0/1/2，输出 JSON，与 `contract.py` / `context_budget.py` 同风格。

### State / Boundary

- 新增的「有界 P4 收敛策略」只定义纪律（重试/探测/熔断/RCA），**不拥有** Dangerous 或 Loop 的激活状态、入口或用户语义；两者激活仍分别由 `/butler:dangerous` 与 `/butler:loop` 显式触发、状态各自落 `dangerous` 开关 / 显式指令。
- 领域合同只登记「身份—所有者—真源」元信息，是导航层，**不复制** Dangerous/Loop 激活枚举、bridge manifest/results 字段全集、四态枚举或 artifact 算法。
- 明确 Out of Scope：不改 `tools/decision-*`、`tools/explore-dogfood/` 状态机；不建全仓术语 DSL / 知识图谱；不接 R5 review 治理 / 双宿主投影 / 升级 dogfood；不吞并 milestone backlog 候办。

### 关键设计取舍 + Plan Admission

- **复用裁决（AC1/AC2）**：不复用 `context-budget/context_budget.py`——它专司 L0/L1/L2 预算与术语表/主链合同，语义不匹配「通用概念注册」；独立薄工具职责内聚、负例可读性好、迁移成本低。选择「JSON 注册表 + 子串断言」而非全正则 DSL，降低实现与审查成本。
- **「唯一所有者」口径（AC1）**：每 entry 恰好一个 owner（同 entry 多 owner 判「重复所有者」fail）；同一 owner 文件可合法拥有多个概念（`delivery-selftest/README.md` 独占四态 + bridge JSON），全局不做「一文件一概念」限制——否则会误伤 AC5 既定的合法独占。
- **共享策略落点（AC3/AC4）**：新增 `30_Quality_Gate/bounded-convergence.md` 承载定量熔断，而非塞进常驻 `correction-contract.md`——后者是「诚实停」定性底线（无硬计数器），混入定量熔断会破坏「常驻 vs opt-in」边界。Dangerous 引用该策略 = 「复用同一纪律、不开启 Loop 模式」。
- **人测段结构所有权（AC5）**：采纳 debt 已列的「改 manifest 加段」方案（而非「折进 Verification Results」），让 manifest/template 拥有位置与空值口径，verify-schema 只解释触发/回填，human-test-bridge 只解释等待与四态路由，delivery-selftest README 继续独占 JSON 字段与机器码。
- **迁移策略（AC6）**：在 `migration.py` 增加「strict 但缺段」分支——带 marker 的 verify_report 缺「人测道小结」时，按 manifest 顺序确定性插入空值段，其余段落字节级保真；已存在错位/重复人测段、未知 marker、无法定位插入点时拒绝并给路径级诊断；legacy 无 marker 与 `.ai/iterations/` 归档零写。
- **Alternatives（已否）**：① 把四态/桥字段复制进领域合同——违背 AC2 单一真源，弃；② 用正则 DSL 表达断言——过度工程，弃；③ 追改全部历史归档满足新结构——违背 AC6 legacy 只读，弃。
- **Assumptions**：`context_budget.py` 的 L2 固定 20 术语保持不变（本轮不新增术语行，避免扰动 R2 门禁）；`verify_report` 段表改动只影响 verify_report，不影响其余四件套。
- **Impact / Scope Challenge**：影响面收敛在规则措辞 + artifact 结构 + 一个薄工具 + CI；未触碰 MILE-0014 三 Module 与 Router 的实现代码，AC8 用全量 `verify-ci.sh` 证明不回退。
- **Verification Blind Spots**：本轮只证明静态合同与确定性迁移；不声称覆盖各宿主运行时实际加载了哪些领域文件（运行时遥测留 R5）。
- **Verdict**：`pass`（已获用户确认 2026-08-13）——无已知 Must Fix。

## Failure Paths

- 注册表引入复制型载荷（`values`/`enum`）→ 未知字段 fail-closed，负例 fixture 证明「因复制型合同被拒」而非仅非零退出。
- 真源指针悬空 / 越界仓外（symlink 逃逸）→ 解析失败或 `is_relative_to(root)` 拒绝，报具体 entry。
- 人测段迁移遇到已有错位/重复「人测道小结」或未知 marker → 拒绝 + 路径诊断，不半写；重复运行迁移（幂等）→ 第二次 no-op。
- Dangerous/Loop 措辞回退成旧包含语义 → assertions `must_not_contain` 命中即 fail，CI 兜住。
- 模板/manifest 漂移（改了一边没改另一边）→ `contract.py check` 的 `validate_templates` 对账失败。
- 依赖的 fixture 里 symlink 解析被 shell 差异影响 → 测试用 `Path.resolve(strict=...)` + `is_relative_to`，不依赖 shell `readlink`。

## Test Strategy

### Execution Steps（可勾选，绑 AC）

- [ ] T1 新增 `Coder/30_Quality_Gate/bounded-convergence.md`，写清定量熔断纪律与 RCA 格式 → AC3/AC4
- [ ] T2 新增 `tools/domain-contract/domains.v1.json`（6 条 entry + relations + assertions）与 `domain_contract.py check` → AC1/AC2
- [ ] T3 新增 `tools/domain-contract/tests/test_domain_contract.py` 正负 fixture（重复 id / 重复 owner / 未知 context·type / 越界 source / 复制型载荷 / 悬空引用 / 旧包含措辞 / 新共享指针）→ AC7
- [ ] T4 修 `dangerous-engine.md` 4 处 + `convergence-loop-engine.md` §6/§7/§8 + `correction-contract.md` + `logic-protocol.md` + `Coder/README.md` 的耦合措辞 → AC3/AC4
- [ ] T5 改 `artifacts.v1.json` + `templates/VERIFY_REPORT.md` + `verify-schema.md`（人测段结构所有权统一）→ AC5
- [ ] T6 改 `migration.py` + `test_migration.py`（strict VERIFY 缺段确定性插入 + 幂等 + 拒绝诊断）→ AC6
- [ ] T7 改 `test_contract.py`（verify_report 段表预期）、`scripts/verify-ci.sh`（挂 domain-contract）、`debt.md`（删两条已还欠债）→ AC8

### Verification Plan

- AC1/AC2：跑 `domain_contract.py check`；注入重复 id/owner、未知 context/type、缺失/越界 source、复制型载荷 fixture，断言具体诊断而非仅非零退出。
- AC3/AC4：跑 mode-boundary 断言，构造「Dangerous 复用 Loop」旧措辞 fixture 必须 fail；证明 `/butler:dangerous` 与 `/butler:loop` 入口仍各自可解析、互不引用激活状态。
- AC5：跑 `contract.py check project`（manifest/template 对账）+ 断言 verify-schema 不再自立结构、human-test-bridge 只解释等待/四态。
- AC6：临时项目迁移旧 strict VERIFY → 重复迁移 → 注入已有/错位/重复人测段与未知 marker → 核内容 hash/段落保真、幂等、拒绝诊断、legacy/归档零写。
- AC7：`python -m unittest discover -s tools/domain-contract/tests` 输出逐类 fixture 名与命中诊断。
- AC8：全量 `bash scripts/verify-ci.sh`（含 `verify-dual-host.sh` 的 decision-map/work/promotion/explore-dogfood、markdown 链接、state audit）+ `git diff --check`；核实际 diff 不含 MILE-0014 状态机实现。

## References Compliance

- N/A
