<!-- butler-artifact-template: 1.0.0 artifact=concept -->
# CONCEPT — ITER-0101 · 上下文映射与主链转换合同

## Current Understanding

- Butler 的主交付链已经由 PRD、AC、TECH_PLAN、Evidence、Goal Verdict 和 Handoff 等成熟产物组成，但各段目前主要各自定义字段与门禁，缺少一张明确说明“上游什么事实进入下游、哪些字段必须保真、何时失效、谁负责拒绝”的跨上下文合同。
- 这不是要新建一套流水线或复制各 schema，而是建立上下文映射：需求与范围向交付生命周期交接钉版输入，生命周期把承诺投给可信保证，可信保证产出完成资格，知识连续性只保存可验鲜派生视图。
- 预期结果应让维护者沿主链定位责任：发生信息丢失、版本漂移、证据不足、派生摘要陈旧时，能判断应该在哪个边界失败并回到哪份权威真源修正。

## Scope

- In Scope：定义 PRD→AC、AC→TECH_PLAN、TECH_PLAN→Evidence、Evidence→Goal Verdict、Goal/权威状态→Handoff 五类转换的输入、输出、保真字段、失效条件、责任方和派生/权威关系。
- In Scope：把合同做成薄导航并与现有 schema、不变量和工具行为对账；为关键断裂场景建立可回归检查，确保导航不会复制字段全集或成为第二真源。
- Out of Scope：不改变 P1→P5 阶段算法，不重做 PRD、Goal、Evidence 或 Handoff 工具，不新增并行执行能力，不提前处理 dangerous/loop 解耦和人测所有权试点（属于 R4）。
- 工程形态：Butler Markdown 规则仓，使用通用 SOP；未命中 Vue / TypeScript / build-tooling profile。

## Open Questions / Risks

- P2 需要决定合同覆盖到“最小保真字段类别”还是逐字段列举；当前倾向前者，并只用指针回到 schema，避免双写漂移。
- 主链涉及四个限界上下文，后续将继续按每批最多 3 份直接真源下钻；若证据不足，会先写升级回执再续批，不以预算为由省略失效条件。
