---
状态: ack-frozen
ACK 日期: 2026-08-13
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0110

## Goal

- 建立一份小而可执行的领域合同，让本轮涉及的高风险身份、状态和引用都能被机器定位到唯一所有者与真源；完成 Dangerous/Loop 解耦和 VERIFY 人测结构所有权统一，同时保持现有公开入口、安全强度与 MILE-0014 行为不回退。

## In Scope

- 为本轮双试点涉及的领域概念登记稳定身份、所属上下文、合同种类、唯一所有者和执行真源，并提供确定性校验。
- 把 Dangerous Mode 与 Convergence Loop 的激活语义改为并列；两者可依赖同一有界 P4 收敛策略，但互不自动开启、互不拥有对方状态。
- 让 artifact manifest 独占 VERIFY 段落结构，delivery-selftest 合同独占桥的 manifest/results 字段与四态机器码，verify schema 和 human-test bridge 只解释消费语义。
- 为 strict live 产物补确定性兼容迁移，并覆盖重复所有者、悬空引用、非法合同类型、旧包含关系、模板漂移和迁移失败等负例。
- 更新必要规则、工具说明、项目知识与完整 CI。

## Out of Scope

- 不修改 `tools/decision-map/`、`tools/decision-work/`、`tools/decision-promotion/` 的状态机或 MILE-0014 已冻结的 Explore→Delivery 边界。
- 不建立全仓术语 DSL、知识图谱或完整状态总注册表，不复制现有状态枚举、JSON 字段表和执行算法。
- 不提前接入 R5 的 review 治理入口、双宿主投影、项目升级 dogfood或运行时效果度量。
- 不处理多 active iteration、并行 P4、状态落档可信门或其他 milestone backlog。

## Acceptance Checklist

- [ ] AC1: 最小领域合同只覆盖本轮双试点所需的高风险身份、状态和引用；每项都有稳定 ID、五上下文之一、受控合同种类、唯一所有者和仓内执行真源，重复 ID、重复所有者、未知上下文/种类、缺失或越界真源均 fail-closed。
- [ ] AC2: 最小领域合同保持“导航/关系而非第二真源”边界：不得复制 Dangerous/Loop 激活枚举、bridge manifest/results 字段全集、四态枚举或 artifact 算法；机器检查能以负例证明复制型合同或悬空引用不会被接受。
- [ ] AC3: Dangerous Mode 与 Convergence Loop 在规则和机器合同中是两个并列模式：各自保留现有显式入口和激活条件，互不读写对方激活状态；共同使用的 P4 重试/探测/熔断纪律落在明确共享策略或底层合同中，不能再用“Dangerous 自动包含/开启 Loop”表达。
- [ ] AC4: 解耦不降低 Dangerous 的既有安全和收敛强度：无人值守 P2/P3 自审、P5 强制审查、人测残余准入、P4 有界重试、死锁/环境熔断与 RCA 交还仍有真源和回归断言；普通 P4 与显式 Loop 的既有行为保持不变。
- [ ] AC5: VERIFY 人测结构只有一个结构所有者：artifact manifest 和 canonical template 固定“人测道小结”的位置与空值口径；verify schema 只解释触发/回填，human-test bridge 只解释等待与四态路由，delivery-selftest README 继续独占 manifest/results JSON 和 `pass/fail/defer/skip` 机器码。
- [ ] AC6: 现有带 artifact marker 的 strict live VERIFY 可通过确定性、幂等、保内容的迁移进入新结构；重复/错位人测段、未知 marker 或无法安全迁移时拒绝并给出可定位诊断，legacy 无 marker 产物及历史归档不被追改。
- [ ] AC7: 正负 fixture 至少覆盖合同身份/所有者/真源校验、Dangerous/Loop 错绑回归、人测段 manifest/template/schema 对账、旧 strict VERIFY 迁移与幂等；失败 fixture 必须证明门禁因预期原因失败，不能只断言非零退出。
- [ ] AC8: MILE-0014 的 Explore、Decision Map、Decision Work、Decision Promotion 和 Router 合同保持通过，R2/R3 的上下文预算与主链合同不回退；artifact contract、Markdown 链接、状态审计、`git diff --check` 与完整 `scripts/verify-ci.sh` 全部通过。

## Verification Method

- AC1: 运行领域合同 checker，核登记集合、字段、上下文、种类、唯一所有者与真源路径；分别注入重复 ID/所有者、未知值、缺失路径和仓外 symlink fixture，断言具体错误码或诊断。
- AC2: 用 checker 的禁止字段/体量/内容规则和负例确认合同只保存关系元信息；对照既有 manifest、delivery-selftest README 与模式规则，确认执行枚举仍只存在原真源。
- AC3: 运行模式边界合同测试，扫描公开触发与规则关系；构造“Dangerous 自动激活 Loop”旧语义 fixture 必须失败，并证明两种模式各自入口仍可独立解析。
- AC4: 对 Dangerous 关键护栏和 P4 有界收敛条款做结构断言，重跑现有 workflow/config/规则合同；删除任一自审、审查、人测准入、熔断/RCA 指针的 fixture 必须失败。
- AC5: 运行 artifact manifest、canonical template、verify schema、human-test bridge 与 delivery-selftest 契约对账；断言结构/消费/桥 I/O 三类所有权唯一且没有字段全集双写。
- AC6: 在临时项目分别迁移旧 strict VERIFY、重复运行迁移、注入已有/错位/重复人测段和未知 marker；核内容 hash/段落保真、幂等、拒绝诊断和 legacy/归档零写。
- AC7: 专项单测输出逐类 fixture 名和命中诊断；P5 以机器 evidence 捕获正向检查与负向套件结果。
- AC8: 重跑 Decision 三 Module、workflow registry、context-budget 和 artifact pipeline 相关测试，再运行 Markdown 链接、state audit、diff check 与完整 CI；核实际 diff 不含 MILE-0014 状态机实现。

## External References

- N/A

## Open Questions / Risks

- 领域合同最终复用 context-budget checker 还是形成独立薄工具，由 P3 按职责内聚、迁移成本和负例可读性裁决；AC 不预设文件名。
- artifact template/version 的兼容策略由 P3 在阅读现有 migration 工具后确定，但不得通过追改历史归档或把 strict 检查降成 legacy 放行满足 AC6。
- 本轮验证静态合同和确定性迁移，不声明已覆盖各宿主模型实际加载了哪些领域文件；运行时读取遥测留给 R5。
