---
状态: ack-frozen
ACK 日期: 2026-07-31
---
<!-- butler-artifact-template: 1.0.0 artifact=acceptance -->
# AC_LIST — ITER-0109

## Goal

- 建立一份可导航、可审计、不会成为第二真源的主链转换合同，让 PRD→AC→Plan→Evidence→Goal→Handoff 每次跨上下文交接都能回答“带什么、保什么、何时拒绝、谁负责、事实归谁”。

## In Scope

- 覆盖 PRD→AC、AC→TECH_PLAN、TECH_PLAN→Evidence、Evidence→Goal Verdict、Goal/权威状态→Handoff 五段转换。
- 每段声明源/目标上下文、输入、输出、最小保真信息、失效条件、责任方以及权威/派生关系。
- 用薄指针连接现有 schema、工具和不变量，并以确定性检查捕获合同缺段、漏字段、错误权威方向和重复定义回归。

## Out of Scope

- 不复制 PRD、AC、TECH_PLAN、Evidence、Goal 或 Handoff 的字段全集、状态枚举和执行算法。
- 不改变 P1→P5、Goal Assurance、evidence runner、handoff generator 或现有 PRD 工具的运行行为。
- 不处理 dangerous/loop 解耦、人测 schema/manifest 所有权、宿主遥测或并行执行；这些属于后续路线或独立方向。

## Acceptance Checklist

- [ ] AC1: 主链合同完整登记 5 段转换；每段都包含源上下文、目标上下文、输入、输出、保真、失效、责任方、权威关系和直接真源指针，缺任一项即不合格。
- [ ] AC2: PRD→AC 明确以钉版的 `prd_id + prd_version + module_slugs` 作为需求集合保真锚点；非 PRD 流保持合法，冻结 AC 不随 live PRD 自动漂移，缺失/冲突引用 fail-closed。
- [ ] AC3: AC→TECH_PLAN 明确方案逐项映射冻结 AC，并继承同一 PRD 钉版引用；方案不得自行升级版本、扩大模块或用执行任务替代 AC，实质改动使旧方案 verdict 失效。
- [ ] AC4: TECH_PLAN→Evidence 明确验证围绕 AC 和方案对齐产生机器 record；失败记录保留但不能打绿，只有通过且强度如实的 evidence 才能覆盖自动道 AC。
- [ ] AC5: Evidence→Goal Verdict 明确 Goal 是聚合派生视图；裁决必须同时核 AC、plan、calibration、evidence、review、blocker 与收口事实，`eligible` 只授权收口、不等于 `complete`，宿主任务状态不能反写。
- [ ] AC6: Goal/权威状态→Handoff 明确 handoff 只由工具从权威状态单向生成并带新鲜度校验；陈旧或源状态非法时拒绝消费，handoff 不得反写生命周期、验收或完成状态。
- [ ] AC7: 合同统一区分权威事实、受控投影、派生视图和叙述摘要；每个失效条件都能路由回唯一修复真源，不在导航层复制字段全集、状态枚举或算法。
- [ ] AC8: 主链合同接入 L0/L1 渐进导航和完整 CI；确定性正负测试至少覆盖五段齐全、必填维度、权威方向、直接真源存在/仓内边界与禁止递归展开，现有完整验证保持通过。

## Verification Method

- AC1: 运行主链合同检查器，断言转换数恰为 5、身份唯一且每段九个维度非空；删除任一段或维度的 fixture 必须失败。
- AC2: 静态合同断言 PRD 钉版三元组、非 PRD 分支、冻结不漂移与 fail-closed 语义均存在，并核指针回到 references/acceptance 真源。
- AC3: 静态合同断言 AC 映射、钉版继承、禁止扩张、任务非替代和 verdict 失效语义；负例改变权威方向必须失败。
- AC4: 静态合同断言 AC/evidence 对应、record、失败保留不打绿与证据强度；核指针回到 verify/evidence 真源。
- AC5: 静态合同断言 Goal 聚合输入、`eligible ≠ complete`、host 单向投影和收口条件；核指针回到 goal/goal-assurance 真源。
- AC6: 静态合同与现有 handoff 单测共同验证生成方向、新鲜度和非法源拒绝；核指针回到 handoff 真源。
- AC7: 检查器拒绝未知事实分类、缺修复真源、复制型长定义或指向仓外/不存在的直接真源；人工对账现有 invariants 无相反结论。
- AC8: 运行专项单测、上下文预算检查、artifact contract、Markdown 链接、状态审计、`git diff --check` 与 `bash scripts/verify-ci.sh`，全部通过。

## External References

- N/A

## Open Questions / Risks

- 合同只列“最小保真信息”，字段细节一律回指现有 schema；若实现时发现必须复制字段全集才能检查，应退回 P3 重审，而不是扩大导航文档。
- 本轮证明静态合同一致性，不声称已获得宿主运行时的逐次读取或转换遥测。
