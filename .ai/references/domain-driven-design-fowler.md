# Domain-Driven Design · Martin Fowler

## Source

- URL: https://martinfowler.com/bliki/DomainDrivenDesign.html
- Author: Martin Fowler
- Published: 2020-04-22
- Accessed: 2026-07-31
- Content type: 外部概念参考；不是逐字权威 PRD，不进入 `.ai/references/prd/`。

## Relevant Ideas

- 复杂领域需要一套能进入系统实现并随理解演进的领域模型，而不是只停留在前期图纸上。
- 统一语言要求业务交流、规则和实现使用同一套严谨概念，并通过真实使用持续检验。
- 战略设计通过限界上下文拆开过大的统一模型；每个上下文内部保持自洽，上下文之间显式映射。
- DDD 的战略概念不依赖面向对象，适用于 Butler 这种由规则、状态文件、schema、manifest、hook 和工具共同组成的系统。

## Use in ITER-0099

- 支撑 AC1：用限界上下文检验 Butler 的领域边界，而不是按目录结构直接推断业务边界。
- 支撑 AC2：用统一语言审计高风险术语的所有权、定义真源和上下文限定。
- 支撑 AC4：用真实语义冲突反向检验领域地图能否定位责任边界。
- 不采用 Entity、Value Object、Aggregate 等战术代码模式；R1 不引入 DDD 框架，也不据此重排仓库。
